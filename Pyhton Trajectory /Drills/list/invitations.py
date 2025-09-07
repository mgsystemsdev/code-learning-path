# app.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from variables.mini_project_cafe_nova import run_demo

MESSAGE = (
    "Dear customer,\n\n"
    "Thank you for using our receipt organizer service. Your receipts have been "
    "successfully processed and stored securely. You can access, categorize, and "
    "manage your receipts at any time through your account dashboard.\n\n"
    "If you have any questions or need assistance, please contact our support team.\n\n"
    "Best regards,\nReceipt Organizer Team"
)


def main() -> None:
    print(MESSAGE)
    
    receipt_text = run_demo()
    print(receipt_text)


if __name__ == "__main__":
    main()
