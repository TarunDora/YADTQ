from yadtq import YADTQ
import time

def process_task(task):
    # Define the task types the worker can process
    if task['type'] == "add":
        res = sum(task['args'])
        time.sleep(30)
        return res
    elif task['type'] == "subtract":
        res = task['args'][0] - task['args'][1]
        time.sleep(30)
        return res
    else:
        raise ValueError("Unknown task type")

def main():
    queue = YADTQ(kafka_server='localhost:9092', redis_host='localhost', redis_port=6379)
    consumer = queue.get_consumer()
    
    print("Worker waiting for tasks...")
    for message in consumer:
        task = message.value
        task_id = task['id']
        
        # Update status to 'processing'
        queue.redis_client.hset(task_id, "status", "processing")
        
        try:
            result = process_task(task)
            queue.redis_client.hmset(task_id, {"status": "success", "result": str(result)})
            print(f"Task {task_id} completed successfully with result: {result}")
        
        except Exception as e:
            queue.redis_client.hmset(task_id, {"status": "failed", "result": str(e)})
            print(f"Task {task_id} failed with error: {e}")

if __name__ == "__main__":
    main()
