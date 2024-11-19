# RR-Team-13-yadtq (Yet Another Distributed Task Queue)

A distributed task queue implemented with Kafka and Redis, designed for efficient task distribution and management across multiple worker nodes.

## Team Members

- Srihari Krishna
- Srilakshmana Amaresh Mandavilli
- Tarun Kumar Dora
- Zhenkar Gowda K P

---

## Prerequisites

To run this project, ensure you have the following installed:

1. **Kafka** and **kafka-python**
    ```bash
    sudo systemctl start kafka
    # Install kafka-python
    pip install kafka-python       # For Python versions < 3.12.x
    pip install kafka-python-ng    # For Python versions 3.12.x and above
    ```

2. **Redis**
    ```bash
    # Install Redis server (Debian-based systems)
    sudo apt install redis-server
    sudo systemctl start redis

    # Install Redis Python client
    pip install redis
    ```
3. **Create a Kafka Topic with at Least 3 Partitions**

    Run the following command to create a Kafka topic named `TaskQueue` with 3 partitions:

    ```bash
    kafka-topics.sh --create --topic TaskQueue --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
    ```

    > **Note:** Adjust `--bootstrap-server` if your Kafka server is running on a different host or port. Also, change `--replication-factor` based on your desired replication settings. For N worker nodes in parallel there should be atleast N partitions

---

## How to Use

1. **Start the Worker Nodes**

    This repository contains one worker file: `worker.py`. To run the worker files follow the worker.py file with the worker's id like 1,2 or 3 etc 

    Command to run the worker files:
    python worker.py -ID
    ex-
    ```bash
    python worker.py -1
    python worker.py -2
    python worker.py -3
    ```
    
    > **Note:** The integer at the end of each execute command is used to identify the worker node.

3. **Check if Worker Nodes are Active**

    Run the following command in a separate terminal to check if the worker nodes are responsive:
    ```bash
    python client.py -h
    ```

4. **Send a Task to Worker Nodes**

    To send a task, such as finding simple interest, use the `client.py` script with the following syntax:
    ```bash
    python client.py -m si [1000,5,2] # for individual processing
    ```
    ```bash
    python client.py si [1000,5,2] # for batch processing
    ```

    This example sends a request to find the simple interest. Similarly, you can use `--help` for available tasks.

5. **Check status of a task**

   To check status of a task run the following command:
   ```bash
    python client.py -s task-*
    ```
5. **Check logs of each task**

   Upon running client.py, a log.txt file is created in the project directory. This file contains a record of all tasks that have been sent, their outputs, and the worker nodes on which they were executed.

    You can open log.txt to:

    -See all submitted tasks.
   
    -Check the outputs of completed tasks.
   
    -Identify the worker node responsible for processing each task.

---
