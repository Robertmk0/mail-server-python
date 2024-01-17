import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
import os

load_dotenv()
class EmailSender:
    def __init__(self):
        self.sender_email = os.getenv("sender_email")
        self.smtp_server = os.getenv("smtp_server")
        self.smtp_port = os.getenv("smtp_port")
        self.smtp_username = os.getenv("smtp_username")
        self.smtp_password = os.getenv("smtp_password")


    def create_message(self, receiver_email, subject, body, attachment_path=None):
        message = MIMEMultipart()
        message['From'] = self.sender_email
        message['To'] = receiver_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))
        if attachment_path:
            attachment = self._attach_file(attachment_path)
            message.attach(attachment)

        return message

    def _attach_file(self, file_path):
        attachment = MIMEBase('application', 'octet-stream')
        with open(file_path, 'rb') as file:
            attachment.set_payload(file.read())
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', f'attachment; filename={file_path.split("/")[-1]}')
        return attachment

    def send_email(self, receiver_email, subject, body, attachment_path=None):
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)

            email_message = self.create_message(receiver_email, subject, body, attachment_path)

            
            server.sendmail(self.sender_email, receiver_email, email_message.as_string())
            print('Email sent successfully!')
        except Exception as e:
            print(f'Error: {e}')
        finally:
           
            server.quit()



email_sender = EmailSender()      #initializing the class
receiver_email = 'receiversemail@gmail.com'
email_subject = 'The subject of the email'  #subject of the email
email_body = 'The Body '   #The body or text to be sent
attachment_path = 'yourfile.extention' #your file path ie if its in the same directory and 
                                       #filename == "main.pdf" it will be main.pdf on the attachment path


email_sender.send_email(receiver_email, email_subject, email_body, attachment_path)
