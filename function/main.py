import base64
from google.cloud import firestore

def hello_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    print(pubsub_message)

    db = firestore.Client()
    fake_users_ref = db.collection('fake-users')
    fake_users_ref.document().set({'username': pubsub_message})
