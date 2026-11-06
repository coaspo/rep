
import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def interpret_instruction(instruction):

    """Ask Gemini to interpret an email organization instruction."""

    print("==== ENTERED interpret_instruction ====", flush=True)
    prompt = f"""
Interpret the user's email organization instruction.

Return a JSON object with exactly these fields:
- action: the requested action, such as "move"
- criteria: a short description of which emails to select
- destination: the destination folder name

Do not claim to have accessed a mailbox or checked whether a
folder exists. Only interpret the instruction.

User instruction:
{instruction}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config={"response_mime_type": "application/json"},
    )

    result = json.loads(response.text)
    print ("====", response.text, flush=True)

    required_fields = {"action", "criteria", "destination"}
    return validate_interpretation(result, required_fields)

def validate_interpretation(result, required_fields):
    """Validate the structure and values of Gemini's response."""

    if not isinstance(result, dict):
        raise ValueError("AI response must be a JSON object.")

    if set(result.keys()) != required_fields:
        raise ValueError("AI response has missing or unexpected fields.")

    for field in ("action", "criteria"):
        if (
            not isinstance(result.get(field), str)
            or not result[field].strip()
        ):
            raise ValueError(
                f"AI response field '{field}' must be a non-empty string."
            )

    destination = result.get("destination")

    if destination is not None and (
        not isinstance(destination, str)
        or not destination.strip()
    ):
        raise ValueError(
            "AI response destination must be a non-empty string or null."
        )

    if result["action"] == "move" and not destination:
        raise ValueError("Move action requires a destination.")

    return result


def detect_provider(email_address):
    if not isinstance(email_address, str):
        return "unknown"

    email_address = email_address.strip().lower()

    if email_address.count("@") != 1:
        return "unknown"

    local_part, domain = email_address.rsplit("@", 1)

    if not local_part or not domain or "." not in domain:
        return "unknown"

    if domain == "gmail.com":
        return "gmail"

    microsoft_domains = {
        "outlook.com",
        "hotmail.com",
        "live.com",
        "msn.com",
    }

    if domain in microsoft_domains:
        return "outlook"

    return "unknown"
