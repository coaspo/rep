#!/home/th/d/rep/w/apps/email-AI-app/.venv/bin/python
import json
import imaplib
import shlex
import email
from email.policy import default
from email.utils import parseaddr
from pathlib import Path
from email.utils import parseaddr, parsedate_to_datetime

class IMAPClient:
    def __init__(self, config_path=None):
        if config_path is None:
            config_path = Path(__file__).resolve().parent.parent / "config.json"
        with open(config_path, "r") as f:
            config = json.load(f)
        self.server = config["IMAP_SERVER"]
        self.port = int(config.get("IMAP_PORT", 993))
        self.email_address = config["EMAIL_ADDRESS"]
        self.password = config["APP_PASSWORD"]
        self.connection = None

    def connect(self):
        self.connection = imaplib.IMAP4_SSL(self.server, self.port)
        self.connection.login(self.email_address, self.password)

    def _parse_raw_email(self, msg_id_token: str, raw_bytes: bytes) -> dict:
        """Parses raw RFC822 email bytes into a clean dictionary for the UI table."""
        try:
            msg = email.message_from_bytes(raw_bytes, policy=default)

            # Extract and deduplicate sender name and email address
            raw_from = msg.get("From", "Unknown Sender")
            display_name, email_addr = parseaddr(raw_from)
            if display_name and display_name.lower() != email_addr.lower():
                sender = f"{display_name} ({email_addr})"
            else:
                sender = email_addr or raw_from

            subject = msg.get("Subject", "(No Subject)")
            raw_date = msg.get("Date", "")
            try:
                date_str = parsedate_to_datetime(raw_date).strftime("%b %d, %Y") if raw_date else "Unknown"
            except Exception:
                date_str = raw_date[:16] if raw_date else "Unknown"

            body_text = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        payload = part.get_payload(decode=True)
                        if payload:
                            body_text = payload.decode("utf-8", errors="ignore")
                        break
            else:
                payload = msg.get_payload(decode=True)
                if payload:
                    body_text = payload.decode("utf-8", errors="ignore")

            preview_text = body_text.strip()[:120].replace("\n", " ") or "Retrieved from inbox"

            return {
                "id": msg_id_token,
                "date": date_str,
                "sender": str(sender),
                "subject": str(subject),
                "preview": preview_text
            }
        except Exception as parse_err:
            return {
                "id": msg_id_token,
                "sender": "System Error",
                "subject": "Parse Failure",
                "context": str(parse_err)
            }

    def execute_raw_imap(self, raw_commands: tuple[str, ...]) -> list[dict]:
        if not self.connection:
            raise RuntimeError("Client not connected.")

        execution_chain = []
        for command_line in raw_commands:
            tokens = command_line.strip().split()
            if not tokens:
                continue

            command_verb = tokens[0].upper()
            args_str = command_line.strip()[len(command_verb):].strip()

            # Preserve parenthesized blocks for FETCH/STORE; tokenize criteria for SEARCH
            if command_verb in ("FETCH", "STORE"):
                command_args = args_str.split(maxsplit=1)
            elif command_verb == "SEARCH":
                command_args = shlex.split(args_str, posix=False)
            else:
                command_args = [args_str] if args_str else []

            self.connection.untagged_responses.clear()
            status, response_data = self.connection._simple_command(command_verb, *command_args)

            if command_verb == "SELECT" and status == "OK":
                self.connection.state = "SELECTED"
            elif command_verb == "CLOSE" and status == "OK":
                self.connection.state = "AUTH"

            real_data = self.connection.untagged_responses.get(command_verb, response_data)

            clean_responses = []
            if real_data:
                for item in real_data:
                    if isinstance(item, tuple) and len(item) > 1:
                        # item[0] is envelope e.g. b'1 (RFC822 {1234}', item[1] is raw email bytes
                        msg_envelope = item[0].decode("utf-8", errors="ignore") if isinstance(item[0], bytes) else str(item[0])
                        msg_id = msg_envelope.split()[0] if msg_envelope.split() else "Unknown"
                        clean_responses.append(self._parse_raw_email(msg_id, item[1]))
                    elif isinstance(item, bytes):
                        clean_responses.append(item.decode("utf-8", errors="ignore"))
                    else:
                        clean_responses.append(str(item))

            execution_chain.append({
                "command": command_line,
                "status": status,
                "responses": clean_responses
            })

            if status != "OK":
                break

        return execution_chain

    def disconnect(self):
        if self.connection:
            try:
                self.connection.close()
            except:
                pass
            self.connection.logout()
            self.connection = None

if __name__ == "__main__":
    client = IMAPClient()
    try:
        client.connect()
        test_commands = ("SELECT INBOX", "FETCH 1:2 (RFC822)")
        result = client.execute_raw_imap(test_commands)
        print("Success! Parsed reply payload:\n", json.dumps(result, indent=2))
    finally:
        client.disconnect()
