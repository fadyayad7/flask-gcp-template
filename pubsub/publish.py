from google.cloud import pubsub_v1

project_id = "syscloud-355221"
topic_name = "new-user"

publisher = pubsub_v1.PublisherClient()

topic_path = publisher.topic_path(project_id, topic_name)

future = publisher.publish(topic_path, b'root')

print(future.result())
print("Published messages.")
