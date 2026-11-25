#!/home/th/d/rep/w/apps/email-AI-app/.venv/bin/python
import os
import traceback
from flask import Flask, request, jsonify, render_template
from email_core.client import IMAPClient
from email_core.compiler import AiImapCompiler

app = Flask(__name__)
compiler = AiImapCompiler()
client = IMAPClient()

def format_emails_for_ui(raw_chain: list[dict]) -> list[dict]:
    """Extracts and formats parsed email dictionaries from the IMAP execution chain."""
    ui_emails = []
    for step in raw_chain:
        for item in step.get("responses", []):
            if isinstance(item, dict) and "id" in item:
                ui_emails.append({
                    "id": item.get("id", ""),
                    "date": item.get("date", ""),
                    "sender": item.get("sender", "Unknown Sender"),
                    "subject": item.get("subject", "(No Subject)"),
                    "preview": item.get("preview", "")
                })
    ui_emails.reverse()
    return ui_emails

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/api/submit", methods=["POST"])
def submit():
    data = request.get_json() or {}
    user_prompt = data.get("prompt", "").strip()

    if not user_prompt:
        return jsonify({"error": "Prompt input is empty. Please enter an instruction."}), 400

    try:
        # 1. Translate natural language into IMAP commands
        commands = compiler.compile(user_prompt)

        if not commands:
            return jsonify({"error": "The compiler generated an empty command chain."}), 500

        # Check if the action modifies the mailbox so the UI knows whether to dim rows
        destructive_verbs = {"STORE", "EXPUNGE", "APPEND", "CREATE", "DELETE", "RENAME", "COPY", "MOVE"}
        has_destructive_action = any(
            cmd.strip().split()[0].upper() in destructive_verbs
            for cmd in commands if cmd.strip()
        )

        # 2. Execute commands over the network socket and parse MIME bytes locally
        client.connect()
        raw_chain = client.execute_raw_imap(commands)
        client.disconnect()

        if has_destructive_action:
            return jsonify({"success": True, "action_applied": True, "emails": []})

        # 3. Format the parsed emails for the frontend table
        ui_emails = format_emails_for_ui(raw_chain)

        return jsonify({"success": True, "action_applied": False, "emails": ui_emails})

    except RuntimeError as re:
        print(f"[COMPILER SLAVE FAILURE] {str(re)}")
        return jsonify({"error": str(re)}), 422

    except Exception as global_exception:
        print("\n!!!!!!!!!!!!!!!! UNHANDLED SERVER CRITICAL RUNTIME EXCEPTION !!!!!!!!!!!!!!!!")
        traceback.print_exc()
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
        return jsonify({"error": f"Internal system failure: {str(global_exception)}"}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
