from yadtq import YADTQ
import time
import sys
import threading
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

file_name = "log.txt"

def send_heartbeat(worker_id, queue):
    while True:
        queue.redis_client.set(f"worker:{worker_id}:heartbeat", int(time.time()))
        time.sleep(10) # Send heartbeat every 10 seconds.


def process_task(task):
    # Define the task types the worker can process
    if task['type'] == "si":
        # Format: principal, rate, time
        principal, rate, T = map(float, task['args'])
        res = (principal * rate * T) / 100
        time.sleep(15)
        return round(res,2)
    
    elif task['type'] == "ci":
        # Format: principal, rate, time
        principal, rate, T = map(float, task['args'])
        res = principal * ((1 + rate / 100) ** T)
        time.sleep(15)
        return round(res,2)
    
    elif task['type'] == "emi":
        # Format: loan_amount, annual_rate, tenure_years
        loan_amount, annual_rate, tenure_years = map(float, task['args'])
        monthly_rate = annual_rate / (12 * 100)
        tenure_months = int(tenure_years * 12)
        res = (loan_amount * monthly_rate * (1 + monthly_rate) ** tenure_months) / ((1 + monthly_rate) ** tenure_months - 1)
        time.sleep(15)
        return round(res,2)

    else:
        raise ValueError("Unknown task type")

def main():
    try:
        worker_id = sys.argv[-1]
        worker_id = int(worker_id[1:])
    except:
        print("Wrong syntax. Try python worker.py -i (where 'i' is an integer)")
        exit()
    
    queue = YADTQ(kafka_server='localhost:9092', redis_host='localhost', redis_port=6379)

    heartbeat_thread = threading.Thread(target=send_heartbeat, args=(worker_id, queue))
    heartbeat_thread.daemon = True
    heartbeat_thread.start()

    consumer = queue.get_consumer()
    
    print("Worker waiting for tasks...")
    try:
        for message in consumer:
            task = message.value
            task_id = task['id']
            
            # Update status to 'processing'
            queue.redis_client.hset(task_id, "status", "processing")
            print(f'task_id : {task_id} , status : {(queue.get_task_status(task_id)) ["status"]}')
            try:
                result = process_task(task)
                queue.redis_client.hmset(task_id, {"status": "success", "result": str(result)})
                print(f"Task {task_id} completed successfully with result: {result} \n")
                with open(file_name, "a") as file:  
                    file.write(f"Task {task_id} completed successfully with result: {result} executed by worker:{worker_id} \n")
            except Exception as e:
                queue.redis_client.hmset(task_id, {"status": "failed", "result": str(e)})
                print(f"Task {task_id} failed with error: {e} \n")
                with open(file_name, "a") as file:  
                    file.write(f"Task {task_id} failed with error: {e} \n")

    except:
        print("GoodBye!")

if __name__ == "__main__":
    main()
