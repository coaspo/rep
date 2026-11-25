#!/home/th/d/rep/w/apps/email-AI-app/.venv/bin/python
import json
from unittest.mock import MagicMock, patch, mock_open
from email.message import Message
from email_core.client import IMAPClient

# Minimal sample configuration payload
MOCK_CONFIG = {
    "IMAP_SERVER": "://test.com",
    "IMAP_PORT": 993,
    "EMAIL_ADDRESS": "test@test.com",
    "APP_PASSWORD": "mockpassword"
}

@patch("builtins.open", new_callable=mock_open, read_data=json.dumps(MOCK_CONFIG))
def test_fetch_latest_emails_success(mock_file):
    """Verifies client parses server payloads into standard dictionary formats."""
    # Build standard mock email components
    mock_msg = Message()
    mock_msg["Subject"] = "Hello Test"
    mock_msg["From"] = "sender@test.com"
    mock_msg["Date"] = "Mon, 9 Nov 2026 12:00:00 +0000"
    mock_msg.set_payload("This is a clean plain text email payload.")

    # Initialize client and inject mock IMAP connection structures
    client = IMAPClient()
    client.connection = MagicMock()

    # Mock IMAP server response steps (.search and .fetch)
    client.connection.search.return_value = ("OK", [b"1 2 3"])
    client.connection.fetch.return_value = ("OK", [(b"metadata", mock_msg.as_bytes()), b")"])

    # Execute target client method
    emails = client.fetch_latest_emails(limit=1)

    # Asset structural integrity metrics
    assert len(emails) == 1
    assert emails[0]["id"] == "3"
    assert emails[0]["subject"] == "Hello Test"
    assert emails[0]["sender"] == "sender@test.com"
    assert emails[0]["body"] == "This is a clean plain text email payload."

    # Verify core IMAP connection routines triggered correctly
    client.connection.select.assert_called_once_with("INBOX", readonly=True)
    client.connection.search.assert_called_once_with(None, "ALL")
