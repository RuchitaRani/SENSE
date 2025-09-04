import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import geocoder

def get_current_location():
    # Use geocoder to get latitude and longitude
    g = geocoder.ip('me')
    if g.latlng:
        return g.latlng
    else:
        return None

def send_email_with_location(to_email):
    # Email details
    sender_email = 'csk.050620002@gmail.com'
    sender_password = 'wuchhdadhoirpaaa'
    subject = 'Current GPS Location'

    # Get current location
    location = get_current_location()
    if not location:
        print("Could not retrieve location.")
        return

    # Compose message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = to_email
    message['Subject'] = subject

    # Create email body
    lat = 22.760460
    long = 75.885171
    body = f"Hi CHANDRA I need immediate assistance. Here is my current location: https://www.google.com/maps?q={lat},{long} Please send help as soon as possible.Thank you SENSE"
    message.attach(MIMEText(body, 'plain'))

    # Connect to SMTP server
    try:
        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)  
        smtp_server.starttls()
        smtp_server.login(sender_email, sender_password)

        # Send email
        smtp_server.sendmail(sender_email, to_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")
    finally:
        smtp_server.quit()

# Usage
if __name__ == "__main__":
    recipient_email = 'mohd.bilal.khan313@gmail.com'
    send_email_with_location(recipient_email)
