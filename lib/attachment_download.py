import imaplib
import email
import os

# Function to download attachments from Gmail
def download_attachments(username, password, folder='INBOX', search_criteria='ALL', save_dir='../attachment'):
    # Connect to Gmail IMAP server
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(username, password)
    mail.select(folder)

    # Search for emails matching the search criteria
    result, data = mail.search(None, search_criteria)
    email_ids = data[0].split()

    # Iterate over email IDs
    for email_id in email_ids:
        # Fetch the email data
        result, data = mail.fetch(email_id, '(RFC822)')
        raw_email = data[0][1]

        # Parse the email
        msg = email.message_from_bytes(raw_email)

        # Iterate over email parts (attachments)
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            # Download attachment
            filename = part.get_filename()
            if filename:
                os.makedirs(save_dir, exist_ok=True)
                filepath = os.path.join(save_dir, filename)
                with open(filepath, 'wb') as f:
                    f.write(part.get_payload(decode=True))
                print(f"Downloaded attachment: {filename}")

    # Close connection
    mail.close()
    mail.logout()

# Replace placeholders with your Gmail credentials
username = 'automated_reports@tecreo.io'
password = 'TecReoReports@24'

# Call the function to download attachments
download_attachments(username, password)

