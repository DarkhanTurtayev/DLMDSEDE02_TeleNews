import asyncio
import time
import os
from aiogram import Bot, Dispatcher, types
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY", "your_telegram_api_key")
bot = Bot(token=TELEGRAM_API_KEY)
dp = Dispatcher()

#wait for Kafka to init
def wait_for_kafka():
    max_retries = 10
    retries = 0
    while retries < max_retries:

        try:
            producer = KafkaProducer(
                bootstrap_servers="kafka:9092",
                acks="all",
                linger_ms=0,
                batch_size=0,
                request_timeout_ms=5000,
                retry_backoff_ms=500,
                max_block_ms=10000
            )
            print("SUCCESS: Kafka Connected")

            producer.send("telegram_news", "Kafka activation message".encode("utf-8"))
            producer.flush()
            print("Initial message sent to activate Kafka topic and db")

            return producer
        
        except NoBrokersAvailable:
            retries += 1
            print(f" Kafka await ({retries}/{max_retries})")
            time.sleep(5)

    print("Unable to connect to Kafka")
    return None

producer = wait_for_kafka()
message_queue = asyncio.Queue() #important when message arrrive at the same time, otherwise crashing

#message receiving logic
@dp.channel_post()
async def handle_message(message: types.Message):
    text = message.html_text or message.text or message.caption or ""
    print(f"Message received: {text}")
    await message_queue.put(text)
    print(f"Message queued: {text}")

async def kafka_worker():
    while True:
        text = await message_queue.get()
        if producer:
            try:
                await asyncio.to_thread(producer.send, "telegram_news", text.encode("utf-8"))
                await asyncio.to_thread(producer.flush)
                print(f"SUCCESS: Sent to Kafka {text}")
            except Exception as e:
                print(f"{e}")
        else:
            print("No Kafka connection found")
        message_queue.task_done()

async def main():
    asyncio.create_task(kafka_worker())
    print("Listen to Telegram Channels:")
    await dp.start_polling(bot, allowed_updates=["channel_post", "edited_channel_post"])

if __name__ == "__main__":
    asyncio.run(main())
