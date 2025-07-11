import base64
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import os
from dotenv import load_dotenv

class EmailSender:
    def __init__(self):
        load_dotenv()
        self.configuration = sib_api_v3_sdk.Configuration()
        self.configuration.api_key['api-key'] = os.getenv('EMAIL_KEY')
        self.api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(self.configuration))
        self.sender_email = os.getenv('EMAIL_SENDER')

    def send_email(self, subject, html, to_address, receiver_username,attachment_path=None):
        sender = {"name": "BOT", "email": self.sender_email}
        to = [{"email": to_address, "name": receiver_username}]
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=to, html_content=html, sender=sender, subject=subject
        )
        # Attach PDF file if provided
        if attachment_path:
            attachments = []
            for path in attachment_path:
                with open(path, "rb") as attachment_file:
                    attachment_content = attachment_file.read()
                encoded_file = base64.b64encode(attachment_content).decode('utf-8')
                attachment = sib_api_v3_sdk.SendSmtpEmailAttachment(
                    name=os.path.basename(path),
                    content=encoded_file
                )
                attachments.append(attachment)
            
            send_smtp_email.attachment = attachments
        
        try:
            api_response = self.api_instance.send_transac_email(send_smtp_email)
            print(api_response)
            return {"message": "Email sent successfully!"}
        except ApiException as e:
            print(f"Exception when calling SMTPApi->send_transac_email: {e}\n")
            return {"message": "Failed to send email"}