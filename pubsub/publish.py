from google.cloud import pubsub_v1

project_id = "syscloud-355221"
topic_name = "pool"

publisher = pubsub_v1.PublisherClient()

topic_path = publisher.topic_path(project_id, topic_name)

future = publisher.publish(topic_path, b'9ed63637-6529-4795-88a1-397dc3c02993')

print(future.result())
print("Published messages.")
