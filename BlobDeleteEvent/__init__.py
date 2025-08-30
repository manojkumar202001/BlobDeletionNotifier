import os
import logging
import azure.functions as func
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def main(event: func.EventGridEvent):
    logging.info(f'Event received: {event.get_json()}')

    # Get blob URL and name
    blob_url = event.get_json().get("url")
    blob_name = blob_url.split('/')[-1] if blob_url else "Unknown"

    # Send email using SendGrid
    message = Mail(
        from_email='noreply@example.com',        # Replace with your sender email
        to_emails='admin@example.com',           # Replace with admin email
        subject='Blob Deleted Notification',
        plain_text_content=f'The blob {blob_name} was deleted.'
    )

    try:
        sg = SendGridAPIClient(os.environ['SENDGRID_API_KEY'])
        response = sg.send(message)
        logging.info(f'Email sent, status code: {response.status_code}')
    except Exception as e:
        logging.error(f'Error sending email: {e}')
