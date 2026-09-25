export const meta = {
  name: 'design-skeleton',
  description: 'Campaign Designer: one phase\'s single-writer skeleton agent (ids, stamps, matrices, assignments)',
  whenToUse: 'Run by the blind conductor after `designer.py phase PN begin --json` reports a pending skeleton; pass that JSON as args.',
  phases: [
    { title: 'Skeleton', detail: 'one agent reads its rendered prompt with the command the conductor passed and writes the phase plan' },
  ],
}

// The return schema of prompts/design/schemas/skeleton.json, inline (scripts cannot read files).
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

const result = await agent(bootstrap, {
  label: `${a.phase}.skeleton.a${attempt}`,
  phase: 'Skeleton',
  schema: SKELETON,
  effort: a.skeleton.effort === 'high' ? 'high' : 'medium',
})

if (!result) {
  log(`${a.phase} skeleton returned nothing (skipped or died); the conductor reruns it with --attempt ${attempt + 1}`)
  return { phase: a.phase, status: 'failed', roster: [], assignments: {}, fragments: [] }
}
log(`${a.phase} skeleton ${result.status}: roster ${result.roster.length}, assignments ${Object.keys(result.assignments).length}`)
return result
