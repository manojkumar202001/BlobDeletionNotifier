import os
import logging
import azure.functions as func
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def main(event: func.EventGridEvent):
    logging.info(f"Event received: {event.get_json()}")

    try:
        event_data = req.get_json()
    except Exception as e:
        return func.HttpResponse(f"Invalid JSON: {str(e)}", status_code=400)

    # Just log the URL for testing
    blob_url = event_data.get("data", {}).get("url", "Unknown URL")
    logging.info(f"Blob URL: {blob_url}")

    return func.HttpResponse("Received event", status_code=200)
