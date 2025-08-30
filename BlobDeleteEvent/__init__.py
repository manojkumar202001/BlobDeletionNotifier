import os
import logging
import azure.functions as func
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Function triggered by Event Grid
def main(event: func.EventGridEvent):
    logging.info(f"Event received: {event.get_json()}")

    # ✅ Handle EventGrid subscription validation handshake
    if event.event_type == "Microsoft.EventGrid.SubscriptionValidationEvent":
        validation_code = event.get_json().get("validationCode")
        logging.info(f"Validation event received. Code: {validation_code}")
        return func.HttpResponse(
            body=f'{{"validationResponse":"{validation_code}"}}',
            mimetype="application/json"
        )

    # ✅ Handle blob deletion events
    if event.event_type == "Microsoft.Storage.BlobDeleted":
        event_data = event.get_json()
        blob_url = event_data.get("url", "Unknown URL")
        blob_name = blob_url.split("/")[-1]

        # Load SendGrid API key from environment variable
        sendgrid_api_key = os.environ["SENDGRID_API_KEY"]

        # Email details
        message = Mail(
            from_email="manojselva592285@outlook.com",   # must be verified in SendGrid
            to_emails="manojselva7094@gmail.com",        # recipient
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
            logging.info("✅ Email sent successfully via SendGrid")
        except Exception as e:
            logging.error(f"❌ Error sending email: {str(e)}")
