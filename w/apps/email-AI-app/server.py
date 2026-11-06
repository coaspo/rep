#!/home/th/d/rep/w/apps/email-AI-app/.venv/bin/python
from flask import Flask, render_template, jsonify
from email_core.sample_emails import SAMPLE_EMAILS
from email_core.organizer import interpret_instruction, detect_provider

app = Flask(__name__)

app.config["JSON_SORT_KEYS"] = False

@app.route("/")
def home():
    return render_template("index.html")


def candidates():
    emails = SAMPLE_EMAILS
    return jsonify(emails)



@app.route("/api/findCandiateEmails", methods=["POST"])
def find_candidates():
    from flask import request

    data = request.get_json() or {}
    instruction = data.get("instruction", "").strip()

    email_address = data.get("emailAddress", "").strip()
    provider = detect_provider(email_address)

    if provider == "unknown":
        return jsonify({
            "error": "Unsupported email account. Please use Gmail or Outlook/Hotmail."
        }), 400

    if not instruction:
        return jsonify({"error": "Please enter an instruction."}), 400

    try:
        # Ask Gemini to interpret the instruction.
        interpretation = interpret_instruction(instruction) #===================
        print("=====Gemini interpretation:", interpretation)
        criteria = interpretation["criteria"].lower()

        # Reuse the sample emails from the existing endpoint.
        emails = candidates().get_json()  #=====================================

        # First prototype: match receipt-related requests
        # against the subject, sender, reason, and email body.
        if "receipt" in criteria:
            matches = [
                email for email in emails
                if "receipt" in (
                    email["subject"] + " "
                    + email["sender"] + " "
                    + email["reason"] + " "
                    + email["body"]
                ).lower()
            ]
        else:
            # For other requests, match words from the criteria.
            words = [
                word.lower().strip(".,!?")
                for word in criteria.split()
                if len(word.strip(".,!?")) > 3
            ]

            matches = [
                email for email in emails
                if any(
                    word in (
                        email["subject"] + " "
                        + email["sender"] + " "
                        + email["reason"] + " "
                        + email["body"]
                    ).lower()
                    for word in words
                )
            ]

        return jsonify({
            "candidates": matches
        })

    except ValueError as error:
        return jsonify({
            "error": f"Could not understand your instruction: {error}"
        }), 400

    except Exception:
        app.logger.exception("Unexpected candidate search failure")
        return jsonify({
            "error": "An unexpected error occurred while searching."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
