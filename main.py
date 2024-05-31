import os
import smtplib
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader

def send_email(to_email, subject, template_vars):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('template.html')
    
    # Render the template with the given variables
    body = template.render(template_vars)
    
    # Email setup
    from_email = os.getenv("MAIL_USERNAME")
    from_password = os.getenv("MAIL_PASSWORD")

    if not from_email or not from_password:
        raise Exception("Set Environment Variables")
    
    # Create the email message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    
    msg.attach(MIMEText(body, 'html'))
    
    # Send the email
    try:
        server = smtplib.SMTP('smtp-relay.sendinblue.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print(f'Email sent to {to_email}')
    except Exception as e:
        print(f'Failed to send email: {e}')

if __name__ == '__main__':
    load_dotenv()

    to_email = 'favas@zennode.com'
    subject = 'Welcome to Our Community!'
    template_vars = {
        'name': 'John Doe'
    }
    send_email(to_email, subject, template_vars)

