from cmath import exp
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# List of IP addresses to ping
ip_addresses = ['157.240.22.35', '8.8.8.8', '10.0.0.1']

# Set up the SMTP server
smtp_server = 'smtp.gmail.com'
port = 587 
sender_email = 'jacktaeed@gmail.com'
password = 'nwjjtohcrlrgcyyk'
receiver_email = 'saiddafou@gmail.com'

# Ping each IP address and check for failures
failure_count = 0
for ip_address in ip_addresses:
    response = subprocess.run(['ping', ip_address], capture_output=True, text=True)
    if 'Received = 4' not in response.stdout:
        failure_count += 1
    else:
        print (ip_address+' machine is up')
    # Send email notification if any failures occurred
    if failure_count > 0:
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = 'Ping email notification'
        body = 'The '+ip_address+' machine is down'
        message.attach(MIMEText(body, 'plain'))

        # Send the message
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(sender_email, password)
            text = message.as_string()
            result = server.sendmail(sender_email, receiver_email, text)
            if not result:
                print("Email sent successfully.")
            else:
                print("Email delivery failed.")

            # close the SMTP server connection
            server.quit()