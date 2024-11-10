from yadtq import YADTQ
import time

def main():
    queue = YADTQ(kafka_server='localhost:9092', redis_host='localhost', redis_port=6379)
    
    # Send a task
    task_id = queue.send_task("add", [10, 20])
    print(f"Client sent task with ID: {task_id}")
    
    # Check task status
    while True:
        status = queue.get_task_status(task_id)
        print(f"Task status: {status}")
        
        if status["status"] in ["success", "failed"]:
            print("Final result:", status)
            break
        time.sleep(2)

if __name__ == "__main__":
    main()
