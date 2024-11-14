from kafka import KafkaProducer, KafkaConsumer
import redis
import json
import time

class YADTQ:
    def __init__(self, kafka_server='localhost:9092', redis_host='localhost', redis_port=6379):
        self.producer = KafkaProducer(
            bootstrap_servers=kafka_server,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.redis_client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)
        self.kafka_server = kafka_server

    def send_task(self, task_type, args):
        task_id = f"task-{int(time.time())}"
        task_data = {
            "id": task_id,
            "type": task_type,
            "args": args,
            "status": "queued"
        }
        self.redis_client.hmset(task_id, {"status": "queued", "result": ""})  # Initialize in Redis
        self.producer.send("TaskQueue", task_data)
        print(f"Sent task {task_id} to Kafka with status 'queued'.")
        return task_id

    def get_task_status(self, task_id):
        return self.redis_client.hgetall(task_id)  # Returns the full task status and result
    
    def get_consumer(self):
        # This method returns a Kafka consumer configured to consume from the "TaskQueue" topic
        return KafkaConsumer(
            'TaskQueue',
            bootstrap_servers=[self.kafka_server],
            group_id='worker-group',
            value_deserializer=lambda v: json.loads(v.decode('utf-8'))
        )
