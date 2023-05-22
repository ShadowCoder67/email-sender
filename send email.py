import getpass
import smtplib
from email.message import EmailMessage
import ssl
import time

def send_email(sender_email, app_password, receiver_email, subject, body, attachments=None):
    message = EmailMessage()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.set_content(body)

    # Attachments
    if attachments:
        for attachment in attachments:
            with open(attachment, 'rb') as file:
                file_data = file.read()
                file_name = file.name
            message.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context()) as smtp:
            smtp.login(sender_email, app_password)
            print("Email prepared. You have a chance to cancel before it is sent.")
            time.sleep(10)  # Delay for 10 seconds, adjust as needed

            cancel_confirmation = input("Enter 'cancel' to abort sending the email or 'send' to proceed with sending: ")
            if cancel_confirmation.lower() == 'cancel':
                print("Email sending cancelled.")
                return
            elif cancel_confirmation.lower() == 'send':
                pass
            else:
                print("Invalid input. Email sending cancelled.")
                return

            smtp.send_message(message)
        print("Email sent successfully!")
    except smtplib.SMTPAuthenticationError:
        print("Failed to authenticate. Please check your email and password.")
    except smtplib.SMTPException as e:
        print(f"An error occurred while sending the email: {str(e)}")


while True:
    sender_email = input("Enter your email address: ")
    app_password = getpass.getpass("Enter your application-specific password: ")
    receiver_email = input("Enter the receiver email: ")
    subject = input("Enter the email subject: ")
    body = input("Enter the email body: ")
    attachments_input = input("Enter the file path(s) of the attachment(s) (comma-separated if multiple, leave empty if none): ")

    if attachments_input:
        attachments = attachments_input.split(',')
    else:
        attachments = []

    send_email(sender_email, app_password, receiver_email, subject, body, attachments)

    redo_confirmation = input("Do you want to redo? Enter 'yes' to redo or any other key to exit: ")
    if redo_confirmation.lower() != 'yes':
        break
