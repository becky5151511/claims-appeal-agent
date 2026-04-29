import anthropic
import json
from pathlib import Path


client = anthropic.Anthropic()

SYSTEM_PROMPT = """You are an expert in U.S. health insurance appeals. Your job is to analyze 
a claim denial and draft a formal appeal letter.

You must respond in JSON with this exact structure:
{
  "appeal_viable": true or false,
  "confidence": "high", "medium", or "low",
  "uncertainty_flags": ["list any areas where you're unsure or missing info"],
  "denial_reason_identified": "one sentence summary of why it was denied",
  "appeal_grounds": ["list each legal/clinical/administrative basis for appeal"],
  "appeal_letter": "the full draft letter text"
}

Critical rules:
- If you cannot identify a clear basis for appeal, set appeal_viable to false and explain why in uncertainty_flags.
- Never fabricate policy numbers, dates, or clinical details not present in the input.
- If key information is missing, flag it in uncertainty_flags rather than guessing.
- The appeal letter should cite specific grounds and use formal medical/administrative language."""


def load_case(denial_letter_path: str, claim_data_path: str) -> dict:
    denial_letter = Path(denial_letter_path).read_text()
    claim_data = Path(claim_data_path).read_text()
    return {"denial_letter": denial_letter, "claim_data": claim_data}


def build_prompt(case: dict) -> str:
    return f"""Please analyze this insurance claim denial and draft an appeal letter.

--- DENIAL LETTER ---
{case['denial_letter']}

--- CLAIM DATA ---
{case['claim_data']}

Respond only with the JSON structure specified. Do not include any text outside the JSON."""


def run_appeal_agent(denial_letter_path: str, claim_data_path: str) -> dict:
    case = load_case(denial_letter_path, claim_data_path)
    prompt = build_prompt(case)

    print("Analyzing denial and drafting appeal...\n")

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = response.content[0].text
    result = json.loads(raw)
    return result


def display_result(result: dict):
    print("=" * 60)
    print("APPEAL ANALYSIS")
    print("=" * 60)

    viable = result.get("appeal_viable")
    confidence = result.get("confidence", "unknown")
    print(f"Appeal viable:  {'YES' if viable else 'NO'}")
    print(f"Confidence:     {confidence.upper()}")

    if result.get("uncertainty_flags"):
        print("\n⚠ UNCERTAINTY FLAGS (review before submitting):")
        for flag in result["uncertainty_flags"]:
            print(f"  - {flag}")

    print(f"\nDenial reason identified:\n  {result.get('denial_reason_identified', 'N/A')}")

    if viable:
        print("\nAppeal grounds:")
        for ground in result.get("appeal_grounds", []):
            print(f"  • {ground}")

        print("\n" + "=" * 60)
        print("DRAFT APPEAL LETTER")
        print("=" * 60)
        print(result.get("appeal_letter", ""))
    else:
        print("\nNo viable appeal basis identified. See uncertainty flags above.")


def save_result(result: dict, output_path: str = "output/appeal_result.json"):
    Path(output_path).parent.mkdir(exist_ok=True)
    Path(output_path).write_text(json.dumps(result, indent=2))
    print(f"\nFull result saved to {output_path}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python agent.py <denial_letter.txt> <claim_data.txt>")
        print("Example: python agent.py examples/denial_letter.txt examples/claim_data.txt")
        sys.exit(1)

    result = run_appeal_agent(sys.argv[1], sys.argv[2])
    display_result(result)
    save_result(result)
