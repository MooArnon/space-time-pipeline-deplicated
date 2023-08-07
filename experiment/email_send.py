#--------#
# Import #
#----------------------------------------------------------------------------#

from email.message import EmailMessage
import ssl
import smtplib

#----------#
# Variable #
#----------------------------------------------------------------------------#

sender_mail = "space.time.pipeline@gmail.com"
sender_password = "gtqduqktqpmhqqzp"

receiver_email = "oomarnon.000@gmail.com"

subject = "Test email"
body = """
    This email was send from python.
    In order to test the code.
"""


#------#
# Main #
#----------------------------------------------------------------------------#

em = EmailMessage()
em["From"] = sender_mail
em["To"] = receiver_email
em["Subject"] = subject

em.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)  as smtp:
    
    smtp.login(sender_mail, sender_password)
    
    smtp.sendmail(msg=em.as_string(), from_addr=sender_mail, to_addrs=receiver_email)