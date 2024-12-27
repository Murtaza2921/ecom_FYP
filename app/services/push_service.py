import firebase_admin
from firebase_admin import messaging, credentials
import os
cred_path = os.path.join(os.path.dirname(__file__), '../../ecom-50c5e-firebase-adminsdk-9ekxv-b995f3b3d9.json')

cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

 
def send_push_notification(token, title, body):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        token=token,
    )
    response = messaging.send(message)
    return response
