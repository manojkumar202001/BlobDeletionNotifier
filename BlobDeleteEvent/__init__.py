import os
import logging
import azure.functions as func
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("HTTP trigger received")

    try:
        event_data = req.get_json()
    except Exception as e:
        return func.HttpResponse(f"Invalid JSON: {str(e)}", status_code=400)

    # Extract blob info
    blob_url = event_data.get("data", {}).get("url", "Unknown URL")
    blob_name = blob_url.split("/")[-1]

    # SendGrid email
    sendgrid_api_key = os.environ.get("SENDGRID_API_KEY")
    message = Mail(
        from_email="manojselva592285@outlook.com",
        to_emails="manojselva7094@gmail.com",
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
        return func.HttpResponse("Email sent", status_code=200)
    except Exception as e:
        logging.error(f"Error sending email: {str(e)}")
        return func.HttpResponse(f"Error sending email: {str(e)}", status_code=500)
