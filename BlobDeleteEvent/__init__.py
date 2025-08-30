import os
import logging
import azure.functions as func
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# This function triggers when a blob is deleted
def main(event: func.EventGridEvent):
    logging.info(f"Event received: {event.get_json()}")

    event_data = event.get_json()

    # Extract blob name and URL from event data
    blob_url = event_data.get("url", "Unknown URL")
    blob_name = blob_url.split("/")[-1]

    # Load SendGrid API key from environment variable
    sendgrid_api_key = os.environ["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"]

    # Email details
    message = Mail(
        from_email="manojselva592285@outlookcom",   # MUST be verified in SendGrid
        to_emails="manojselva7094@gmail.com.com",                  # Recipient
        subject="Azure Blob Deleted Notification",
        html_content=f"""
        <h3>Blob Deleted Alert</h3>
        <p><b>Blob Name:</b> {blob_name}</p>
        <p><b>Blob URL:</b> {blob_url}</p>
        """
    )

    try:
        sg = SendGridAPIClient(sendgrid_api_key)
        sg.send(message)
        logging.info("Email sent successfully via SendGrid")
    except Exception as e:
        logging.error(f"Error sending email: {str(e)}")
