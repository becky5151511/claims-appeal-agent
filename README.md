# AI Insurance Claims Appeal Agent

A Python tool that analyzes denied insurance claims and drafts structured appeal letters using Claude.

## Why I built this

I work in healthcare operations. Every week I watch legitimate claims get denied — not for clinical reasons, but because the documentation didn't match exactly what the insurer's system expected. The appeals process exists, but writing a good appeal letter takes time and requires understanding both the clinical record and the insurer's specific policy language. Most of the logic is repetitive.

I built this to automate the first draft. The goal isn't to remove human judgment — it's to make the human review faster and more focused. The agent flags what it's uncertain about so a reviewer knows exactly where to look before submitting.

## How it works

**Input:** A denial letter + the member's claim data (diagnosis, clinical notes, prior auth history, etc.)

**Output:**
- Whether an appeal is viable (and why)
- Confidence level + specific uncertainty flags
- The identified denial reason
- Legal/clinical/administrative grounds for appeal
- A complete draft appeal letter

**Key design decision:** If the agent can't find a clear basis for appeal, it says so rather than generating a letter anyway. A weak appeal can close the window for a second attempt, so flagging uncertainty is more useful than producing something that sounds plausible but isn't grounded in the actual policy.

## Setup

```bash
git clone https://github.com/yourusername/claims-appeal-agent
cd claims-appeal-agent
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key_here
```

## Usage

```bash
python agent.py examples/denial_letter.txt examples/claim_data.txt
```

The result is printed to terminal and saved as JSON to `output/appeal_result.json`.

## Example

The `examples/` folder contains a realistic (fully anonymized) scenario: a CGM device denied for a Type 2 diabetic member on insulin who has documented hypoglycemic episodes. The denial cites missing documentation of hypoglycemic unawareness — but that documentation exists in the clinical notes.

Running the agent on this case should identify the discrepancy and draft an appeal citing the documented episodes and physician's clinical judgment.

## What it doesn't do (yet)

- Doesn't pull directly from EHR systems or insurer portals
- Doesn't handle multi-stage appeals or external review requests
- Policy databases are not built in — it works from the documents you provide
- Not a substitute for legal or clinical review before submission

## Status

Working prototype. I've used outputs from this tool to draft real appeals, reviewed them manually, and submitted them. Still iterating on edge cases around insurer-specific policy language.
