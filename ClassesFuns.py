 ###############################################################################
import json, requests
from collections import OrderedDict
                                    # FUNCTIONS AND CLASSES
# function to send email to gmail
def send_email(fromaddr, pwd, toaddr, Subject, body):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    # sender and recipeints
    fromaddr = fromaddr
    toaddr = toaddr
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = ', '.join(toaddr)
    msg['Subject'] = Subject
    # email text
    body = body
    msg.attach(MIMEText(body, 'plain'))
    # knit the email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, pwd)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

# Class to:
    # check if the get is successfull or not
    # loads the json
class checkGet_and_loads:
    # check if the get is successfull or not
    def get(self, url, file):
        # download the file
        self.r = requests.get(url)
        # check if file was downloaded with no errors
        if self.r.status_code != 200:
            emailBody = 'Sending email. Error with downloading the ' + file + ' file.'
            send_email( fromaddr = emailFrom, pwd = password, toaddr = emailTo, Subject = emailSubject, body = emailBody )
            print( 'Error: Unexpected response {}'.format(self.r) )
        else: pass
            # print( 'Not sending email. No errors found when downloading the ' + file + ' file.' )
    ##########################################
    # loads the json file
    def loads(self):# , url, file):
        
        # download the file
        # self.r = requests.get(url)
        
        # loads the json file
        to_loads = json.loads( self.r.text, object_pairs_hook = OrderedDict )
        return( to_loads )
                                    # /FUNCTIONS AND CLASSES
###############################################################################
