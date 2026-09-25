export const meta = {
  name: 'design-skeleton',
  description: 'Campaign Designer: one phase\'s single-writer skeleton agent (ids, stamps, matrices, assignments)',
  whenToUse: 'Run by the blind conductor after `designer.py phase PN begin --json` reports a pending skeleton; pass that JSON as args.',
  phases: [
    { title: 'Skeleton', detail: 'one agent reads its rendered prompt with the command the conductor passed and writes the phase plan' },
    { title: 'Skeleton critique', detail: 'a critic reads the skeleton and its stubs; one fix loop; a second critic where the plan asks' },
  ],
}

// The return schema of prompts/design/schemas/skeleton.json, inline (scripts cannot read files).
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
const SKELETON = {
  type: 'object',
  required: ['phase', 'status', 'roster', 'assignments', 'fragments'],
  additionalProperties: false,
  properties: {
    phase: { type: 'string', pattern: '^P[0-9]$' },
    status: { type: 'string', enum: ['staged', 'failed'] },
    roster: { type: 'array', items: { type: 'string', pattern: '^[a-z]+_[a-z0-9_]+$' } },
    assignments: { type: 'object', additionalProperties: { type: 'string' } },
    fragments: { type: 'array', items: { type: 'string' } },
    skeleton_file: { type: 'string' },
    counts: { type: 'object', additionalProperties: { type: 'integer' } },
  },
}

// args = the JSON printed by `designer.py -c CAMP phase PN begin --json`
const a = args || {}
if (!a.skeleton || !a.skeleton.prompt_cmd) {
  throw new Error('design-skeleton: args.skeleton.prompt_cmd is missing; run `designer.py phase PN begin --json` first')
}
const attempt = a.attempt || 1

phase('Skeleton')
log(`${a.phase} skeleton for ${a.campaign} (attempt ${attempt})`)

const bootstrap = `You are the ${a.phase} skeleton agent of the Campaign Designer for campaign ${a.campaign} (attempt ${attempt}).
Your full instructions are rendered by a script. First run exactly this command with the Bash tool and read its output; it is your prompt and you follow it to the letter:

${a.skeleton.prompt_cmd}

Do not ask the conductor anything; everything you need is in the rendered prompt, the files it lists, the tables under data/design/ and the templates under templates/design/. Write your files, then return only the JSON the prompt ends with.`

let result = await agent(bootstrap, {
  label: `${a.phase}.skeleton.a${attempt}`,
  phase: 'Skeleton',
  schema: SKELETON,
  effort: a.skeleton.effort === 'high' ? 'high' : 'medium',
})

if (!result) {
  log(`${a.phase} skeleton returned nothing (skipped or died); the conductor reruns it with --attempt ${attempt + 1}`)
  return { phase: a.phase, status: 'failed', roster: [], assignments: {}, fragments: [], verdicts: [] }
}
log(`${a.phase} skeleton ${result.status}: roster ${result.roster.length}, assignments ${Object.keys(result.assignments).length}`)

// tuning birth 1: the skeleton went to the fan-out unread. A critic checks counts, roster, stubs and secret
// names against the rolls; a `fix` gets one loop; a second critic where the prompt asks for two.
const critique = (order, loop) => agent(`You are a critic agent of the Campaign Designer for campaign ${a.campaign}, phase ${a.phase}, the skeleton (attempt ${attempt}).
Your full instructions are rendered by a script. First run exactly this command with the Bash tool and read its output; it is your prompt and you follow it to the letter:

${order === 2 ? a.skeleton.critic2_cmd : a.skeleton.critic_cmd}

Save your return as design/_staging/${a.phase}/skeleton.critic${order}${loop > 1 ? '.loop' + loop : ''}.json before returning it. Do not ask the conductor anything. Return only the JSON the prompt ends with.`, {
  label: `${a.phase}.skeleton.critic${order}${loop > 1 ? '.loop' + loop : ''}`,
  phase: 'Skeleton critique',
  schema: CRITIC,
  effort: 'high',
})

const verdicts = []
if (result.status === 'staged' && a.skeleton.critic_cmd) {
  phase('Skeleton critique')
  let v = await critique(1, 1)
  verdicts.push(v ? v.verdict : 'critique_missing')
  if (v && v.verdict === 'fix') {
    const again = await agent(bootstrap + `

A critic returned "fix" on your skeleton. Read design/_staging/${a.phase}/skeleton.critique.md (and the dm-only copy if the critic wrote one) and repair exactly what its findings name: re-assign the ordinals, add the missing stubs, rename what leaks. Overwrite skeleton.json and the stub fragments; this is the one fix loop the skeleton gets.`, {
      label: `${a.phase}.skeleton.fix1`,
      phase: 'Skeleton',
      schema: SKELETON,
      effort: a.skeleton.effort === 'high' ? 'high' : 'medium',
    })
    if (again && again.status === 'staged') {
      result = again
      v = await critique(1, 2)
      verdicts.push(v ? v.verdict : 'critique_missing')
    }
  }
  if (a.skeleton.critics === 2 && a.skeleton.critic2_cmd) {
    const second = await critique(2, 1)
    verdicts.push(second ? 'c2:' + second.verdict : 'c2:critique_missing')
  }
  log(`${a.phase} skeleton critique: ${verdicts.join(' → ')}`)
}
result.verdicts = verdicts
return result
