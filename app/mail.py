import ssl
import imapclient
from config import *
import quopri
from flask import jsonify
from email import message_from_bytes

def get_emails():
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.options |= ssl.OP_NO_SSLv2
    ssl_context.options |= ssl.OP_NO_SSLv3
    ssl_context.options |= ssl.OP_NO_TLSv1
    ssl_context.options |= ssl.OP_NO_TLSv1_1
    ssl_context.options |= ssl.OP_NO_TLSv1_3  # Opcjonalnie, w zależności od wymagań

    with imapclient.IMAPClient(EMAIL_SERVER, EMAIL_PORT, ssl=SSL, ssl_context=ssl_context) as client:
        client.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        client.select_folder('INBOX')
        messages = client.search(['UNDELETED'])
        email_data = []
        for msg_id, data in client.fetch(messages, ['ENVELOPE', 'RFC822']).items():
            envelope = data[b'ENVELOPE']
            msg_id = msg_id
            date_sent = envelope.date

            # Pobierz pełną treść wiadomości
            raw_message = data[b'RFC822']
            email_message = message_from_bytes(raw_message)
            body = ""
            if email_message.is_multipart():
                for part in email_message.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode('utf-8')
                        break
            else:
                body = email_message.get_payload(decode=True).decode('utf-8')

            email_data.append({'date_sent': date_sent, 'body': body, 'msg_id' : msg_id})
    return email_data

def delete_email(msg_id):
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.options |= ssl.OP_NO_SSLv2
    ssl_context.options |= ssl.OP_NO_SSLv3
    ssl_context.options |= ssl.OP_NO_TLSv1
    ssl_context.options |= ssl.OP_NO_TLSv1_1
    ssl_context.options |= ssl.OP_NO_TLSv1_3  # Opcjonalnie, w zależności od wymagań

    with imapclient.IMAPClient(EMAIL_SERVER, EMAIL_PORT, ssl=SSL, ssl_context=ssl_context) as client:
        try:
                client.login(EMAIL_USERNAME, EMAIL_PASSWORD)
                client.select_folder('INBOX')
                client.delete_messages([msg_id])

                # Zwróć odpowiedź JSON o powodzeniu
                return jsonify({'success': True}), 200
        except Exception as e:
            # Jeśli wystąpi błąd, zwróć odpowiedź JSON z informacją o błędzie
            return jsonify({'success': False, 'error': str(e)}), 500