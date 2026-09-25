export const meta = {
  name: 'design-fanout',
  description: 'Campaign Designer: one phase\'s per-entity fan-out — write, critique, fix (at most two loops), a second critic where the plan asks, then the phase critic and the wishes critic',
  whenToUse: 'Run by the blind conductor after `designer.py phase PN merge` absorbed the skeleton and `phase PN begin --json` listed the pending entities; pass that JSON as args. Also the `detail` path with one entity.',
  phases: [
    { title: 'Write', detail: 'one fresh agent per pending entity, prompt rendered by design_prompts.py' },
    { title: 'Critique', detail: 'one critic per entity (two on the premise, BBEG and lieutenants), a fix loop at most twice' },
    { title: 'Phase critique', detail: 'the cross-entity rubric and the wishes rubric' },
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
  `A critic returned "${verdict}" on your previous attempt. Read design/_staging/${a.phase}/${e.id}.critique.md (and the dm-only copy if the critic wrote one) and repair exactly what its findings name; keep every stamped field; this is fix loop ${loop} of ${MAX_FIX_LOOPS}. Overwrite the prose and rewrite the fragment last.`), {
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
      const second = await critique(r.e, 2, 1)
      r.verdicts.push(second ? 'c2:' + second.verdict : 'c2:critique_missing')
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
if (a.phase_critic && a.phase_critic.prompt_cmd && staged.length) {
  const pc = await agent(bootstrap('phase critic', a.phase_critic.prompt_cmd, { id: a.phase },
    `Save your return as design/_staging/${a.phase}/phase.critic1.json before returning it.`), {
    label: `${a.phase}.phase_critic`, phase: 'Phase critique', schema: CRITIC, effort: 'high',
  })
  phaseVerdict = pc ? pc.verdict : 'critique_missing'
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
  wishes_verdict: wishesVerdict,
  next: 'designer.py phase ' + a.phase + ' merge → check → card → approve',
}
