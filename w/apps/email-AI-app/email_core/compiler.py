#!/home/th/d/rep/w/apps/email-AI-app/.venv/bin/python
import json
from pathlib import Path
import json
from openai import OpenAI, APIError, APITimeoutError, APIConnectionError


class AiImapCompiler:
    def __init__(self, config_path=None):
        if config_path is None:
            config_path = Path(__file__).resolve().parent.parent / "config.json"
        with open(config_path, "r") as f:
            config = json.load(f)
        print ("====",json.dumps(config, indent=2))

        self.client = OpenAI(
            api_key=config["AI_API_KEY"],
            base_url=config["AI_BASE_URL"],
            max_retries=0,
            timeout=10.0
        )
        self.model = config["AI_MODEL"]

        self.system_instruction = (
            "Compile natural language requests into valid raw IMAP commands, one per line. "
            "Omit command tags (like A001) and output only plain text commands with no markdown or backticks.\n\n"
            "Current date: {today}.\n\n"
            "Examples:\n"
            "- 'get latest 5' ->\nSELECT INBOX\nSEARCH ALL\nFETCH 1:5 (RFC822)\n"
            "- 'find unread from boss' ->\nSELECT INBOX\nSEARCH UNSEEN FROM \"boss@co.com\"\nFETCH 1:100 (RFC822)\n"
            "- 'show receipts from last week' ->\nSELECT INBOX\nSEARCH SINCE 04-Nov-2026 TEXT \"receipt\"\nFETCH 1:100 (RFC822)\n"
            "- 'delete message 45' ->\nSELECT INBOX\nSTORE 45 +FLAGS (\\Deleted)\nEXPUNGE\n"
            "- 'purge trash' ->\nEXPUNGE\n\n"
            "Rules:\n"
            "1. Wrap text arguments and email addresses in double quotes (\"\").\n"
            "2. Convert relative dates (like yesterday or last week) into IMAP DD-Mon-YYYY format.\n"
            "3. If a request is unclear or unrelated to email, respond with 'INVALID:' followed by a brief explanation.\n"
            "4. Never use math operators ('-' or '+') in FETCH ranges; use fixed ranges like '1:5' or '1:100'.\n"
            "5. Never use IMAP 'SORT'.\n"
            "6. Always follow a SEARCH command with 'FETCH 1:100 (RFC822)'."
            "7. Use SENTSINCE, SENTON, and SENTBEFORE instead of SINCE, ON, and BEFORE when filtering by date."

        )
    def compile(self, user_prompt: str) -> tuple[str, ...]:
        try:
            print ("======", user_prompt)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_instruction},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.0
            )
            raw_text = response.choices[0].message.content.strip().replace("1:*", "1:100", 1)

            if raw_text.startswith("INVALID:"):
                error_explanation = raw_text[len("INVALID:"):].strip()
                raise RuntimeError(f"Prompt Rejected: {error_explanation}")

            reply = tuple(line.strip() for line in raw_text.splitlines() if line.strip())
            print ("======", reply)
            return reply

        except (APITimeoutError, APIConnectionError):
            raise RuntimeError("The AI service timed out or could not be reached. Please try again.") from None
        except APIError as e:
            raise RuntimeError(f"AI Compilation Engine Error: {str(e)}") from None
        except Exception as e:
            if not isinstance(e, RuntimeError):
                raise RuntimeError(f"Unexpected compilation failure: {str(e)}") from None
            raise e


if __name__ == "__main__":
    compiler = AiImapCompiler()
    compiler.compile("get the latest 10 emails")
    compiler.compile("what is the time")
