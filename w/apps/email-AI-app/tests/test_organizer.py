
from email_core.organizer import interpret_instruction


def test_interprets_move_receipts_instruction():
    result = interpret_instruction(
        "Put purchase receipts in the Receipts folder."
    )

    # Test Gemini's actual interpretation.
    assert result["action"].lower() == "move"
    assert "receipt" in result["criteria"].lower()
    assert result["destination"].strip().lower() == "receipts"
