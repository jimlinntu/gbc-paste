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
import re
from PIL import Image

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

    def create_message_mime(self, name, greeting_image_path, dest_email, gathering_path, gathering_name):
        gmail_user = "gbc.life.tw@gmail.com"
        
        title = name
        greeting_path = Path(greeting_image_path)
        assert(greeting_path.exists())
        gathering = Path(gathering_path)

        msg = MIMEMultipart('related')
        msg['Subject'] = '懷恩堂生命助道會歡迎你！'
        msg['From'] = gmail_user
        msg['To'] = dest_email
        msg.preamble = 'This is a multi-part message in MIME format.'

        msgAlternative = MIMEMultipart('alternative')
        msg.attach(msgAlternative)

        with open("plain.txt", "r") as f:
            plain_content = name + f.read()
            plain_content = re.sub("name_placeholder", name, plain_content)
            plain_content = re.sub("gathering1_placeholder", gathering_name, plain_content)
            msgText = MIMEText(plain_content)
        msgAlternative.attach(msgText)
        
        # https://gist.github.com/jossef/2a4a46a899820d5d57b4

        with open("content.txt", "r") as f:
            content = "<div dir=\"ltr\">" + name + f.read().strip() + "</div>"
            msgText = MIMEText(content, 'html', "utf-8")

        msgAlternative.attach(msgText)
        
        title_png = title + ".png"
        with greeting_path.open("rb") as f:
            msgImage = MIMEImage(f.read(), name=title_png)
        # https://stackoverflow.com/questions/37019708/how-can-i-customize-file-name-in-python-mimeimage
        # https://docs.python.org/3.6/library/email.message.html#email.message.EmailMessage.add_header
        msgImage.add_header('Content-Disposition', "attachment", filename=title_png)
        msgImage.add_header('Content-ID', '<greeting>')
        msg.attach(msgImage)

        with gathering.open("rb") as f:
            msgImage = MIMEImage(f.read(), name=gathering_name)
        msgImage.add_header('Content-Disposition', "attachment", filename=gathering_name)
        msgImage.add_header('Content-ID', '<gathering1>')
        msg.attach(msgImage)


        # https://stackoverflow.com/questions/37019708/how-can-i-customize-file-name-in-python-mimeimage

        Path('outgoing.msg').write_bytes(bytes(msg))
        return msg



def main(args):
    smtp_wrapper = SMTPWrapper()

    greeting_card_not_success = []
    with open(args.name_file, "r") as f:
        for line in f:
            line = line.strip()
            splitted = line.split(",")
            assert(len(splitted) == 2)
            name, dest_email = splitted
            name = name + "同學" if args.student else name
            print("=" * 70)
            print("Dumping a greeting card")
            print("=" * 70)
            smtp_wrapper.dump_greeting_image(name, args.output)
            if args.check_greeting_card:
                print("=" * 70)
                print("Please check if this greeting card is ok, and then press c to continue sending.")
                pil_image = Image.open(args.output)
                pil_image.show()
                response = input().strip()
                if response != "c":
                    greeting_card_not_success.append(line)
                    continue
                print("=" * 70)
            print("=" * 70)
            print("Creating a message")
            print("=" * 70)
            msg = smtp_wrapper.create_message_mime(name, args.output, dest_email, args.gathering_image_path, args.gathering_name)
            print("=" * 70)
            print("Sending the message")
            print("=" * 70)
            smtp_wrapper.sendMsg(msg)

    print("=" * 70)
    print("Not success list: ")
    print(greeting_card_not_success)
    print("=" * 70)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name_file", type=str, help="names and their corresponding emails")
    parser.add_argument("gathering_image_path", type=str, help="The gathering card")
    parser.add_argument("gathering_name", type=str, help="The gathering card's filename")
    parser.add_argument("output", type=str, help="Image output path")
    parser.add_argument("--student", action="store_true", default=False)
    parser.add_argument("--check_greeting_card", action="store_true", default=False)
    args = parser.parse_args()
    main(args)

