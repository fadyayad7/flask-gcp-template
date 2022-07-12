import base64
from google.cloud import firestore
from google.cloud import pubsub_v1
from datetime import datetime

def check_reservation(event, context):
    project_id = "syscloud-355221"
    topic_name = "pool"

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)

    db = firestore.Client()
    now_date = datetime.now().strftime("%Y-%m-%d")
    hour = int(datetime.now().strftime("%H"))
    if hour%2 == 0: hour -= 1
    hour = f"{hour}-{hour+2}"

    user_uuid = base64.b64decode(event['data']).decode('utf-8')
    reservation_ref = db.collection('reservations')
    reservation = reservation_ref.where("user_uuid", "==", user_uuid) \
            .where("date", "==", now_date) \
            .where("time", "==", hour).get()

    if reservation is None: result = False

    if len(reservation) > 1: result = False
    if len(reservation) == 1: result = True
    if len(reservation) == 0: result = False

    future = publisher.publish(topic_path, b'User has been checked', result=f"{result}")

