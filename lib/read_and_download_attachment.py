# Importing libraries
import datetime
import imaplib
import os
import email
import zipfile
import io
import logging
import argparse
import json

print(os.path.dirname(__file__))
with open(os.path.dirname(__file__) + '/../conf.json') as f:
    config = json.load(f)
    print(config)

user = config["emailApp"]["user"]
password = config["emailApp"]["password"]
imap_url = config["emailApp"]["imap_url"]
readonly = config["emailApp"]["readonly"]
dir_name = config["emailApp"]["dir_name"]

# printing logs
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

# command line argument settings
parser = argparse.ArgumentParser()
parser.add_argument('--since', required=False, dest='days', type=str, help='provide a number to check mail "1"')
parser.add_argument('--email_id', required=False, dest='email', type=str, help='provide a from email id')
args = parser.parse_args()

if args.days is not None:
    date = (datetime.date.today() - datetime.timedelta(int(args.days))).strftime("%d-%b-%Y")
else:
    date = (datetime.date.today() - datetime.timedelta(1)).strftime("%d-%b-%Y")


# Create a directory to download attachment
def create_directory(dir_path=None):
    if dir_path is not None:
        path = dir_path + "/" + dir_name
        is_exist = os.path.exists(path)
        if not is_exist:
            os.makedirs(path)
    else:
        # use default download path
        path = os.path.dirname(__file__) + "/" + dir_name
        is_exist = os.path.exists(path)
        # if download path does not exist, create a new one
        if not is_exist:
            os.makedirs(path + "/" + dir_name)
    logger.info(" checking if '{}' director exist in path: '{}' ".format(dir_name, path))
    return path


# search email ids for a key value pair or all with since 'date'
def search_mail_ids(connection, key=None, value=None, since=None):
    if key is not None and value is not None:
        logger.info(" scanning emails in 'Inbox' coming from email id:'{}' since: '{}'".format(value, since))
        resp_type, mail_id_bytes = connection.search(None, '(SINCE {0})'.format(since), key, '"{}"'.format(value), 
'UNSEEN')
        if resp_type == 'OK' and mail_id_bytes is not None:
            logger.info(
                " scanning status :'{}' matching email count: '{}'".format(resp_type, len(mail_id_bytes[0].split())))
    else:
        logger.info(" scanning emails in 'Inbox' coming from all email ids since: '{}'".format(since))
        resp_type, mail_id_bytes = connection.search(None, '(SINCE {0})'.format(since), 'UNSEEN')
        if resp_type == 'OK' and mail_id_bytes is not None:
            logger.info(
                " scanning status :'{}' matching email count: '{}'".format(resp_type, len(mail_id_bytes[0].split())))
    return mail_id_bytes


# converts byte literal to string
def convert_to_string(data_bytes):
    logger.info(" converting list byte literal to string removing 'b'")
    # converts list byte literal to string removing b''
    raw_email_string = data_bytes.decode('utf-8')
    # converting string to email message object '<class 'email.message.Message'>'
    email_message = email.message_from_string(raw_email_string)
    logger.info(" converting string to email message object with 'message_from_string' function")
    return email_message


def write_attachment(file_name, data):
    # remove special characters from file name
    bad_chars = [';', ':', '!', "*", " ", "-", "@", "#", "$", "%", "^", "&", "(", ")", "=", "+", ","]
    file_name = ''.join(i for i in file_name if i not in bad_chars)
    dir_path = create_directory()
    file_path = dir_path + "/" + file_name + ".csv"
    logger.info(" downloading the attachment in path : '{}' \n".format(file_path))
    f = open(file_path, "w")
    f.write(data)
    f.close()


# downloading attachments
def download_attachment(message):
    attachment_file = False
    msg_body = ""
    # checking inner part of the message has any attachment
    for part in message.walk():
        print("download_attachment 1")
        # if 'Content-Disposition' is None, this no attachment in mail
        if part.get('Content-Disposition') is not None:
            print("download_attachment 2")
            logger.info(" attachment file name : {}' ".format(part.get_filename()))
            filename: str = part.get_filename()
            # if there is file name decode the message and write the content in a file
            if filename is not None:
                print("download_attachment 3")
                if 'application/zip;' in part.get('Content-Type').strip():
                    print("STEP 1")
                    z = zipfile.ZipFile(io.BytesIO(part.get_payload(decode=True)))
                    print("STEP 2")
                    attach_data = z.read(filename.split(".")[0] + ".csv").decode('utf-8')
                    print("STEP 3")
                    write_attachment(filename.split(".")[0], attach_data)
                    print("STEP 4")
                else:
                    attach_data = part.get_payload(decode=True).decode('utf-8')
                    print("STEP 5")
                    write_attachment(filename.split(".")[0], attach_data)
                    print("STEP 6")
                attachment_file = True
            else:
                print("STEP 7")
                logger.info(" there is no attachment files in email ")
		#send email for fail...
        else:
            if part.get_payload(decode=True) is not None and len(part.get_payload(decode=True)) > 5:
                print("STEP 8")
                msg_body = part.get_payload(decode=True).decode('utf-8')
                print("STEP 9")
    if not attachment_file:
        print("STEP 10")
        logger.info(" there is no attachment files in email ")
	#send email for fail...
    print("STEP 191")
    logger.info(" email message : {}' ".format(msg_body))


# get all the emails data based on search criteria 'search_mail_ids'
def fetch_email(result_bytes):
    print("IN fetch_email 1")
    logger.info(" fetching emails details for email ids '{}' \n".format(str(result_bytes[0].decode("utf-8"))))
    print("IN fetch_email 2")
    for email_id in result_bytes[0].split()[::-1]:
        # fetch returns bytes list with two elements
        # email_data[0][0] returns mail id, format and mail length
        # email_data[0][1] returns actual email, headers and mail body
        logger.info(" emails details for email id '{}' ".format(str(email_id.decode("utf-8"))))
        resp_type, email_data = mail_con.fetch(email_id, '(RFC822)')
        logger.info(" fetch response status '{}' ".format(resp_type))
        print("IN fetch_email 3")
        if email_data is not None:
            # converting string email data to email message object '<class 'email.message.Message'>'
            # by calling function convert_to_string(bytes)
            message_obj = convert_to_string(email_data[0][1])
            logger.info(" email from :{}' ".format(message_obj.get_all('from')[0]))
            logger.info(" email subject: {}' ".format(message_obj.get_all('subject')[0]))
            logger.info(" email date: {}' ".format(message_obj.get_all('date')[0]))
            logger.info(" email content maintype : {}' ".format(message_obj.get_content_maintype()))
            # if a content type is multipart the chance of attachment in mail is high
            print("IN fetch_email 4")
            # need to access inner part of mail
            if message_obj.get_content_maintype() == 'multipart':
                logger.info(" scanning email for attachment ")
                print("IN fetch_email 44")
                download_attachment(message_obj)
                print("IN fetch_email 5")
            else:
                logger.info(" there is no attachment files in email ")
                logger.info(" email message : {}' ".format(message_obj.get_payload()))
            print("IN fetch_email 6")


print("IN fetch_email 2")
# this is done to make SSL connection with GMAIL
logger.info(" connecting to IMAP server ")
print("STEP 11")
try:
    mail_con = imaplib.IMAP4_SSL(imap_url)
    print("STEP 12")

    if isinstance(mail_con, imaplib.IMAP4_SSL):
        logger.info(" IMAP server connected successfully")
    else:
        logger.info(" IMAP server connection failed")

    print("STEP 13")
    # logging to gmail account
    logger.info(" login to gmail account email: '{}'".format(user))
    typ, login_status = mail_con.login(user, password)
    logger.info(" login status:'{}',{}".format(typ, str(login_status[0].decode("utf-8"))))

    # calling function to check for email under this label
    logger.info(" selecting Inbox to scan email in read only mode: '{}'".format(readonly))
    stype, msg_number = mail_con.select('Inbox', readonly)
    logger.info(" Inbox selection status '{}' email count:'{}'".format(stype, str(msg_number[0].decode("utf-8"))))

    print("STEP 14")
    if args.email is not None:
        # fetching emails from a particular 'email id'
        mail_ids = search_mail_ids(mail_con, 'FROM', '{}'.format(args.email), since=date)
    else:
        # fetching emails from all 'email ids'
        mail_ids = search_mail_ids(mail_con, since=date)
    print("STEP 15")
    #check befor calling this function 
    #if mail ids are available then only call this function
    fetch_email(mail_ids)
    print("STEP 16")
    logger.info(" end of scanning emails")
    print("STEP 17")

    if mail_ids != [b'']:
       logger.info(" changing mail status to seen") 
       for store_mail_status_id in mail_ids[0].split()[::-1]:
           print("====")
           raw_email_id = str(store_mail_status_id, encoding='utf-8')
           print("====111")
           ret, data = mail_con.store(raw_email_id,'+FLAGS','\\Seen')
           if ret == 'OK':
              logger.info("Set mail status to seen; Got OK: ")

    logger.info(" closing connection ")
    ctype, cdata = mail_con.close()
    logger.info(" connection closing status '{}' email close state:'{}'".format(ctype, cdata[0].decode("utf-8")))
    lg_type, lg_data = mail_con.logout()
    logger.info(" logging off from account ")
    logger.info(" logging off status '{}' logging off state:'{}'".format(lg_type, lg_data[0].decode("utf-8")))

except Exception as error:
    logger.info(" can not establish connection to IMAP server, server responded: '{}'".format(error))

# python3 read_and_download_attachment.py --since 1 --email_id smaato_statistics@smaato.com
