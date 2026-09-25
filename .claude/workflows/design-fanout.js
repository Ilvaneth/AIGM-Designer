export const meta = {
  name: 'design-fanout',
  description: 'Campaign Designer: one phase\'s per-entity fan-out — write, critique, fix (at most two loops), a second critic where the plan asks, then the phase critic and the wishes critic',
  whenToUse: 'Run by the blind conductor after `designer.py phase PN merge` absorbed the skeleton and `phase PN begin --json` listed the pending entities; pass that JSON as args. Also the `detail` path with one entity.',
  phases: [
    { title: 'Write', detail: 'one fresh agent per pending entity, prompt rendered by design_prompts.py' },
    { title: 'Critique', detail: 'one critic per entity (two on the premise, BBEG and lieutenants), a fix loop at most twice; the second critic\'s fix is acted on too' },
    { title: 'Phase critique', detail: 'the cross-entity rubric and the wishes rubric; entities the phase critic names get one targeted fix' },
  ],
}

// Return schemas of prompts/design/schemas/*.json, inline (scripts cannot read files).
const WRITER = {
  type: 'object',
  required: ['entity_id', 'status', 'fragment'],
  additionalProperties: false,
  properties: {
    entity_id: { type: 'string', pattern: '^[a-z]+_[a-z0-9_]+$' },
    status: { type: 'string', enum: ['staged', 'failed'] },
    fragment: { type: 'string' },
    counts: { type: 'object', additionalProperties: { type: 'integer' } },
  },
}
const CRITIC = {
  type: 'object',
  required: ['entity_id', 'verdict', 'findings'],
  additionalProperties: false,
  properties: {
    entity_id: { type: 'string' },
    verdict: { type: 'string', enum: ['pass', 'fix', 'rerun'] },
    findings: {
      type: 'array',
      items: {
        type: 'object',
        required: ['rubric_id', 'entity_id', 'verdict'],
        additionalProperties: false,
        properties: {
          rubric_id: { type: 'string' },
          entity_id: { type: 'string' },
          verdict: { type: 'string', enum: ['pass', 'fix', 'rerun', 'note'] },
          reason_code: { type: 'string' },
        },
      },
    },
    notes_file: { type: 'string' },
  },
}

const MAX_FIX_LOOPS = 2

const a = args || {}
if (!Array.isArray(a.entities)) {
  throw new Error('design-fanout: args.entities is missing; run `designer.py phase PN begin --json` first')
}
const attempt = a.attempt || 1
const entities = a.entities.filter(e => e && e.prompt_cmd)
const skipped = a.entities.length - entities.length
if (skipped) log(`${skipped} pending entit${skipped === 1 ? 'y has' : 'ies have'} no prompt and ${skipped === 1 ? 'is' : 'are'} not run`)
log(`${a.phase} fan-out for ${a.campaign}: ${entities.length} entities, attempt ${attempt}`)

function bootstrap(role, cmd, e, extra) {
  return `You are a ${role} agent of the Campaign Designer for campaign ${a.campaign}, phase ${a.phase}, entity ${e.id} (attempt ${attempt}).
Your full instructions are rendered by a script. First run exactly this command with the Bash tool and read its output; it is your prompt and you follow it to the letter:

${cmd}
${extra ? '\n' + extra + '\n' : ''}
Do not ask the conductor anything; everything you need is in the rendered prompt and the files it lists. Return only the JSON the prompt ends with.`
}

const writeStage = (e) => agent(bootstrap('writer', e.prompt_cmd, e), {
  label: `${a.phase}.${e.id}.a${attempt}`,
  phase: 'Write',
  schema: WRITER,
  effort: e.effort === 'high' ? 'high' : 'medium',
})

const critique = (e, order, loop) => agent(bootstrap('critic', order === 2 ? e.critic2_cmd : e.critic_cmd, e,
  `Save your return as design/_staging/${a.phase}/${e.id}.critic${order}${loop > 1 ? '.loop' + loop : ''}.json before returning it (the conductor records it from there).`), {
  label: `${a.phase}.${e.id}.critic${order}${loop > 1 ? '.loop' + loop : ''}`,
  phase: 'Critique',
  schema: CRITIC,
  effort: 'medium',
})

const fix = (e, loop, verdict) => agent(bootstrap('writer (fix loop)', e.prompt_cmd, e,
  `A critic returned "${verdict}" on your previous attempt. Read design/_staging/${a.phase}/${e.id}.critique.md (and the dm-only copy if the critic wrote one; the phase critic writes design/_staging/${a.phase}/phase.critique.md) and repair exactly what its findings name; keep every stamped field; this is fix loop ${loop} of ${MAX_FIX_LOOPS}. Overwrite the prose and rewrite the fragment last.`), {
  label: `${a.phase}.${e.id}.fix${loop}`,
  phase: 'Write',
  schema: WRITER,
  effort: e.effort === 'high' ? 'high' : 'medium',
})

// write → critique → (fix → critique)×≤2 → second critic; no barrier between entities
const results = await pipeline(entities,
  async (e) => {
    const w = await writeStage(e)
    return { e, write: w, loops: 0, verdicts: [] }
  },
  async (r) => {
    if (!r || !r.write || r.write.status !== 'staged') return r
    let verdict = await critique(r.e, 1, 1)
    r.verdicts.push(verdict ? verdict.verdict : 'critique_missing')
    while (verdict && verdict.verdict === 'fix' && r.loops < MAX_FIX_LOOPS) {
      r.loops += 1
      const again = await fix(r.e, r.loops, verdict.verdict)
      if (!again || again.status !== 'staged') { r.write = again || r.write; break }
      r.write = again
      verdict = await critique(r.e, 1, r.loops + 1)
      r.verdicts.push(verdict ? verdict.verdict : 'critique_missing')
    }
    if (r.e.critics === 2 && r.e.critic2_cmd) {
      let second = await critique(r.e, 2, 1)
      r.verdicts.push(second ? 'c2:' + second.verdict : 'c2:critique_missing')
      // tuning birth 1: the second critic's `fix` was recorded and ignored; it gets one loop of its own
      if (second && second.verdict === 'fix' && r.loops < MAX_FIX_LOOPS) {
        r.loops += 1
        const again = await fix(r.e, r.loops, 'fix (second critic)')
        if (again && again.status === 'staged') {
          r.write = again
          second = await critique(r.e, 2, 2)
          r.verdicts.push(second ? 'c2:' + second.verdict : 'c2:critique_missing')
        }
      }
    }
    return r
  },
)

const done = results.filter(Boolean)
const staged = done.filter(r => r.write && r.write.status === 'staged').map(r => r.e.id)
const failed = entities.map(e => e.id).filter(id => !staged.includes(id))
const loops = done.reduce((n, r) => n + (r.loops || 0), 0)
log(`${a.phase}: ${staged.length} staged, ${failed.length} failed, ${loops} fix loops`)

// the cross-entity rubric and the wishes rubric, once the fragments exist
phase('Phase critique')
let phaseVerdict = null
let wishesVerdict = null
let phaseFixes = []
if (a.phase_critic && a.phase_critic.prompt_cmd && staged.length) {
  const pc = await agent(bootstrap('phase critic', a.phase_critic.prompt_cmd, { id: a.phase },
    `Save your return as design/_staging/${a.phase}/phase.critic1.json before returning it.`), {
    label: `${a.phase}.phase_critic`, phase: 'Phase critique', schema: CRITIC, effort: 'high',
  })
  phaseVerdict = pc ? pc.verdict : 'critique_missing'
  // tuning birth 1: the phase critic's verdict was never acted on. Every staged entity a `fix` finding
  // names gets one targeted fix and one re-critique (loop 3, so the record stays distinct); the phase
  // critic is not re-run, the card shows its verdict and the fixes applied.
  if (pc && pc.verdict !== 'pass') {
    const named = [...new Set((pc.findings || []).filter(f => f.verdict === 'fix' || f.verdict === 'rerun').map(f => f.entity_id))]
    const targets = entities.filter(e => staged.includes(e.id) && named.includes(e.id))
    phaseFixes = await parallel(targets.map(e => () =>
      fix(e, 3, 'fix (phase critic)').then(async (w) => {
        if (!w || w.status !== 'staged') return { id: e.id, fixed: false }
        const v = await critique(e, 1, 3)
        return { id: e.id, fixed: true, verdict: v ? v.verdict : 'critique_missing' }
      })))
    phaseFixes = phaseFixes.filter(Boolean)
    log(`${a.phase}: phase critic said ${pc.verdict}; ${phaseFixes.length} targeted fix(es) applied`)
  }
}
if (a.wishes_critic && a.wishes_critic.prompt_cmd && staged.length) {
  const wc = await agent(bootstrap('wishes critic', a.wishes_critic.prompt_cmd, { id: a.phase },
    `Save your return as design/_staging/${a.phase}/wishes.critic1.json before returning it.`), {
    label: `${a.phase}.wishes_critic`, phase: 'Phase critique', schema: CRITIC, effort: 'medium',
  })
  wishesVerdict = wc ? wc.verdict : 'critique_missing'
}

return {
  phase: a.phase,
  attempt,
  staged,
  failed,
  fix_loops: loops,
  verdicts: Object.fromEntries(done.map(r => [r.e.id, r.verdicts])),
  phase_verdict: phaseVerdict,
  phase_fixes: phaseFixes,
  wishes_verdict: wishesVerdict,
  next: 'designer.py phase ' + a.phase + ' merge → check → card → approve',
}
