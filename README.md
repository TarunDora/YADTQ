# RR-Team-13-yadtq (Yet Another Distributed Task Queue)

A distributed task queue implemented with Kafka and Redis, designed for efficient task distribution and management across multiple worker nodes.

## Team Members

- Srihari Krishna
- Srilakshmana Amaresh M
- Tarun Kumar D
- Zhenkar P Gowda

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

---

## How to Use

1. **Start the Worker Nodes**

    This repository contains three worker files: `worker1.py`, `worker2.py`, and `worker3.py`. To add your own worker files, ensure that the filename ends with an integer. 

    - Examples of valid filenames: `worker1.py`, `c1.py`, `file4.py`
    - Examples of invalid filenames: `worker.py`, `file.py`, `c.py`

    > **Note:** The integer at the end of each filename is used to identify the worker node.

2. **Check if Worker Nodes are Active**

    Run the following command in a separate terminal to check if the worker nodes are responsive:
    ```bash
    python client.py -h
    ```

3. **Send a Task to Worker Nodes**

    To send a task, such as adding two numbers, use the `client.py` script with the following syntax:
    ```bash
    python client.py add [10, 20]
    ```

    This example sends a request to add 10 and 20. Similarly, you can use `sub` for subtraction tasks.

---

This setup should get you started with running and interacting with the distributed task queue. Feel free to explore further or add new functionalities to suit your project's needs!
