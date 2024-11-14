from yadtq import YADTQ
import time
import sys
import json

def check_heartbeat(queue):
    status = queue.check_worker_health()
    if len(status): # print if workers are present
        print(status)


def main():
    queue = YADTQ(kafka_server='localhost:9092', redis_host='localhost', redis_port=6379)
    
    if "-h" in sys.argv:
        check_heartbeat(queue)
        print("Goodbye!")
        exit()

    comm = sys.argv[-2]
    params = json.loads(sys.argv[-1])

    # Send a task
    task_id = queue.send_task(comm, params)
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
