import logging
import azure.functions as func
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

def main(event: func.EventGridEvent):
    logging.info(f"Event received: {event.get_json()}")

    event_data = event.get_json()
    blob_url = event_data.get("url", "Unknown URL")
    blob_name = blob_url.split("/")[-1]

    sendgrid_api_key = os.environ.get("SENDGRID_API_KEY")
    message = Mail(
        from_email="manojselva592285@outlook.com",
        to_emails="manojselva7094@gmail.com",
        subject="Azure Blob Deleted Notification",
        html_content=f"<h3>Blob Deleted Alert</h3><p><b>Blob Name:</b> {blob_name}</p><p><b>Blob URL:</b> {blob_url}</p>"
    )

    try:
        sg = SendGridAPIClient(sendgrid_api_key)
        sg.send(message)
        logging.info("Email sent successfully via SendGrid")
    except Exception as e:
        logging.error(f"Error sending email: {str(e)}")
