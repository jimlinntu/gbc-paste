import html
import mimetypes
from email.headerregistry import Address
from email.message import EmailMessage
from email.utils import make_msgid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from pathlib import Path
import smtplib
import getpass
import argparse
import paste

class SMTPWrapper():
    def __init__(self):
        self.smtp = self.initSMTP("gbc.life.tw@gmail.com")
        
    def initSMTP(self, sender):
        smtp = smtplib.SMTP("smtp.gmail.com:587")
        smtp.ehlo()
        smtp.starttls()
        password = getpass.getpass("Please input your password:")
        smtp.login(sender, password)
        return smtp

    def sendMsg(self, msg):
        self.smtp.send_message(msg)

    
    def dump_greeting_image(self, name, greeting_image_path):
        paste.paste(name, greeting_image_path)
        
    def create_message(self, name, greeting_image_path, dest_email):
        gmail_user = "gbc.life.tw@gmail.com"
        
        title = name
        path = Path(greeting_image_path)
        assert(path.exists())
        me = Address("life gbc", *gmail_user.rsplit('@', 1))

        msg = EmailMessage()
        msg['Subject'] = '懷恩堂生命助道會歡迎你！'
        msg['From'] = me
        msg['To'] = [dest_email]
        msg.set_content('[image: {title}]'.format(title=title))  # text/plain
        cid = make_msgid()[1:-1]  # strip <>    
        msg.add_alternative(  # text/html
            '<img src="cid:{cid}" alt="{alt}"/>'
            .format(cid=cid, alt=html.escape(title, quote=True)),
            subtype='html')
        maintype, subtype = mimetypes.guess_type(str(path))[0].split('/', 1)
        msg.get_payload()[1].add_related(  # image/png
            path.read_bytes(), maintype, subtype, cid="<{cid}>".format(cid=cid))

        # save to disk a local copy of the message
        Path('outgoing.msg').write_bytes(bytes(msg))
        return msg

    def create_message_mime(self, name, greeting_image_path, dest_email):
        gmail_user = "gbc.life.tw@gmail.com"
        
        title = name
        greeting_path = Path(greeting_image_path)
        gatherings = [Path("./gathering1.png"), Path("./gathering2.png")]
        assert(greeting_path.exists())

        msg = MIMEMultipart('related')
        msg['Subject'] = '懷恩堂生命助道會歡迎你！'
        msg['From'] = gmail_user
        msg['To'] = dest_email
        msg.preamble = 'This is a multi-part message in MIME format.'

        msgAlternative = MIMEMultipart('alternative')
        msg.attach(msgAlternative)

        msgText = MIMEText('This is the alternative plain text message.')
        msgAlternative.attach(msgText)
        
        # https://gist.github.com/jossef/2a4a46a899820d5d57b4

        with open("content.txt", "r") as f:
            content = "<div dir=\"ltr\">" + name + f.read().strip() + "</div>"
            msgText = MIMEText(content, 'html', "utf-8")
        msgAlternative.attach(msgText)
        
        with greeting_path.open("rb") as f:
            msgImage = MIMEImage(f.read(), name=title+".png")
        msgImage.add_header('Content-ID', '<greeting>')
        msg.attach(msgImage)

        with gatherings[0].open("rb") as f:
            msgImage = MIMEImage(f.read(), name="2019.7-9.png")
        msgImage.add_header('Content-ID', '<gathering1>')
        msg.attach(msgImage)

        with gatherings[1].open("rb") as f:
            msgImage = MIMEImage(f.read(), name="2019.10-12.png")
        msgImage.add_header('Content-ID', '<gathering2>')
        msg.attach(msgImage)

        # https://stackoverflow.com/questions/37019708/how-can-i-customize-file-name-in-python-mimeimage

        Path('outgoing.msg').write_bytes(bytes(msg))
        return msg



def main(args):
    smtp_wrapper = SMTPWrapper()
    name = args.name + "同學" if args.student else args.name
    print("=" * 70)
    print("Dumping a greeting card")
    print("=" * 70)
    smtp_wrapper.dump_greeting_image(name, args.output)
    print("=" * 70)
    print("Creating a message")
    print("=" * 70)
    msg = smtp_wrapper.create_message_mime(args.name, args.output, args.dest_email)
    print("=" * 70)
    print("Sending the message")
    print("=" * 70)
    smtp_wrapper.sendMsg(msg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name", type=str, help="Subject's name")
    parser.add_argument("dest_email", type=str, help="Destination email address")
    parser.add_argument("output", type=str, help="Image output path")
    parser.add_argument("--student", action="store_true", default=False)
    args = parser.parse_args()
    main(args)

