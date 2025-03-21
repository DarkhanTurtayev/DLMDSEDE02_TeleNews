from kafka import KafkaConsumer

#simple tool to check if Kafka receiving messages

consumer = KafkaConsumer(
    "telegram_news",             # or trending_words, depends what to is needed
    bootstrap_servers="localhost:9092",  # or telenews-kafka-1:9092 or kafka:9092 if inside Docker
    auto_offset_reset="earliest", 
    enable_auto_commit=True,
    group_id="news_reader"
)

print("Waiting messages:")

for message in consumer:
    print(f"GET: {message.value.decode('utf-8')}")