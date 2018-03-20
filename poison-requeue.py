import sys
import logging
from azure.storage.queue import QueueService
from settings import CONNECTION_STRING, ACCOUNT_NAME, ACCOUNT_KEY

if len(sys.argv) != 2:
    print("Queue name argument required")
    exit(2)

if CONNECTION_STRING is None and (ACCOUNT_NAME is None and ACCOUNT_KEY is None):
    print("Connection string or account name/key not provided")
    exit(2)

logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(message)s',
    level=logging.INFO,
    datefmt='%d-%m-%Y %H:%M:%S')

queue_name = sys.argv[1]
poison_queue_name = "%s-poison" % queue_name

if CONNECTION_STRING is not None:
    logging.info("Connecting with connection string `%s`" % CONNECTION_STRING)
    client = QueueService(connection_string=CONNECTION_STRING)
else:
    logging.info("Connecting to account `%s` with key `%s`" % (ACCOUNT_NAME, ACCOUNT_KEY))
    client = QueueService(
        account_name=ACCOUNT_NAME,
        account_key=ACCOUNT_KEY)

logging.info("Queue `%s`" % queue_name)
logging.info("Poison `%s`" % poison_queue_name)

if not client.exists(queue_name):
    logging.info("Queue `%s` does not exist" % queue_name)
    exit(1)

if not client.exists(poison_queue_name):
    logging.info("Poison queue `%s` does not exist" % poison_queue_name)
    exit(1)

logging.info("Both queues exist")

while len(client.peek_messages(poison_queue_name)) > 0:
    messages = client.get_messages(poison_queue_name, 32, 32*2)
    logging.info("Requeuing %s messages" % len(messages))
    for message in messages:
        client.put_message(queue_name, message.content)
        client.delete_message(poison_queue_name, message.id, message.pop_receipt)

logging.info("Poison queue empty")
exit(0)
