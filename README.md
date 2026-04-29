# AI Insurance Claims Appeal Agent

A Python tool that analyzes denied insurance claims and drafts structured appeal letters using Claude.

## Why I built this

I work in healthcare operations at a senior care center in New York. Every week I watch legitimate claims get denied — not for clinical reasons, but because of authorization gaps, coverage transition issues, or documentation mismatches. The appeals process exists, but drafting a good appeal takes time and requires knowing both the clinical record and the insurer's specific policy language.

Most of the logic is repetitive. The same types of denials come up again and again — prior auth expired, coverage gap during a plan switch, a member who traveled abroad and triggered an automatic residency flag. I built this to automate the first draft so that the human reviewing it can focus on what actually needs judgment: verifying the facts, checking the attachments, and deciding whether to file.

The plans I deal with most are HealthFirst, HomeFrist, VillageCareMAX, and River Spring — all Medicare Advantage and Medicaid managed care plans serving elderly members in New York. The examples in this repo reflect the kinds of denials I actually see.

## How it works

**Input:** A denial letter + the member's claim data (diagnosis, clinical notes, authorization history, coverage dates, etc.)

**Output:**
- Whether an appeal is viable, and confidence level
- The identified denial reason
- Specific appeal grounds (regulatory citations included where applicable)
- A list of recommended attachments for the appeal package
- A complete draft appeal letter

**Key design decision:** If the agent can't identify a clear basis for appeal, it says so and flags the uncertainty — rather than generating a letter that sounds plausible but isn't grounded in the actual policy. A bad appeal letter can close the window for a second attempt, and for elderly members on fixed incomes, that matters.

## Setup

```bash
git clone https://github.com/yourusername/claims-appeal-agent
cd claims-appeal-agent
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key_here
```

## Usage

```bash
python agent.py <denial_letter.txt> <claim_data.txt>
```

Example:
```bash
python agent.py examples/case3_prior_auth_expired/denial_letter.txt \
                examples/case3_prior_auth_expired/claim_data.txt
```

Output is printed to terminal and saved as JSON to `output/`.

## Examples

Three realistic, fully anonymized cases based on patterns I've seen in practice:

### Case 1 — Coverage Suspension (Member Traveled Abroad)
`examples/case1_coverage_suspension/`

HealthFirst VIP Medicare Advantage. Elderly member traveled to China for 7 weeks to visit family. HealthFirst automatically suspended coverage — likely triggered by a pharmacy claims gap during the travel period. The member returned to the U.S. six days before the denied appointment. Appeal argues the travel was temporary, primary residence was never in question, and the service date falls after the confirmed return.

### Case 2 — Insurance Transition Gap
`examples/case2_insurance_transition/`

Member switching from Fidelis Care to River Spring Health LIFE (PACE). Enrollment application submitted November 19; River Spring set effective date of January 4 — creating a 3-day gap over New Year's during which both plans denied personal care aide services for an 82-year-old with dementia. Appeal argues River Spring's processing delay caused the gap and that continuity-of-care obligations apply.

### Case 3 — Prior Authorization Expired (Plan Processing Delay)
`examples/case3_prior_auth_expired/`

HealthFirst Medicare Advantage. Provider submitted prior auth renewal 14 days before expiration (within plan's required window). HealthFirst took 36 days to process — issuing the approval 22 days after the original auth expired. Plan denied all claims during the gap. Appeal cites 42 CFR 422.568 and argues the plan's own processing failure caused the authorization gap.

Each example folder contains the denial letter, claim data, and the agent's output (`appeal_result.json`) so you can see what a real run looks like without needing an API key.

## What it doesn't do (yet)

- No direct EHR or insurer portal integration
- Doesn't handle external review or second-level appeals
- Insurer policy details must be provided in the input — no built-in policy database
- Not a substitute for legal or clinical review before submission

## Status

Working prototype. I've used outputs from this to draft real appeals, reviewed them manually, and submitted them. The feedback from that loop has shaped most of the prompt design — particularly the uncertainty flagging and the attachment recommendations, which turned out to be more useful than the letter draft itself in some cases.
