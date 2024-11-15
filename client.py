from yadtq import YADTQ
import time
import sys
import json
import redis

def check_heartbeat(queue):
    status = queue.check_worker_health()
    if len(status): # print if workers are present
        print(status)


def main():
    queue = YADTQ(kafka_server='localhost:9092', redis_host='localhost', redis_port=6379)
    
    if len(sys.argv) > 5 or ("-s" in sys.argv and "-h" in sys.argv):
        print(len(sys.argv))
        print("Invalid syntax")
        exit()

    if sys.argv[-1] == "-h":
        check_heartbeat(queue)
        print("Goodbye!")
        exit()
    
    if sys.argv[-2] == "-s":
        task_key = sys.argv[-1]
        print(queue.get_task_status(task_key))
        exit()

    if sys.argv[-1] == "--help":
        print("Commands are:")
        print("si [P(₹),R(%),T(yrs)]  -> calculates simple interest")
        print("ci [P(₹),R(%),T(yrs)]  -> calculates compound interest")
        print("emi [P(₹),R(%),T(yrs)]  -> calculates simple interest")
        print("-s [task_id]  -> check task status by ID")
        print("-h            -> check worker health")
        exit()

    comm = sys.argv[-2]
    #print(comm)
    #print(sys.argv[-1],type(sys.argv[-1]))
    params = json.loads((sys.argv[-1]))
    #params = sys.argv[-1]

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
