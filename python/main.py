import zmq
import threading
import msgpack
import time
import random

def worker(worker_id, sleep):
    context = zmq.Context()
    pull_socket = context.socket(zmq.PULL)
    pull_socket.connect("tcp://127.0.0.1:5557")
    accepted = 0
    
    while True:
        message = pull_socket.recv()
        data = msgpack.unpackb(message)
        accepted += 1
        print(f"Worker {worker_id} received: {data}, total accepted: {accepted}")
        time.sleep(sleep * 2)


def main():
    num_workers = 3
    threads = []
    for i in range(num_workers):
        thread = threading.Thread(target=worker, args=(i,i+1,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
