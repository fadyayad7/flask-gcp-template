from google.cloud import pubsub_v1

project_id = "esame-sac-lumetti"
subscription_name = "pool_sub"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_name)

def callback(message):
    print(f"Message received:\n{message}")
    message.ack()

streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

streaming_pull_future.result()

# try:
#     streaming_pull_future.result(timeout=10)
# except:
#     streaming_pull_future.cancel()
