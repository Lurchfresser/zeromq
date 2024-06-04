import zmq
import threading
import time
import random

def worker(context:zmq.SyncContext,worker_id):
    req_socket = context.socket(zmq.REQ)
    req_socket.connect("tcp://127.0.0.1:5556")
    push_socket = context.socket(zmq.PUSH)
    push_socket.connect("tcp://127.0.0.1:5557")
    accepted = 0
    
    while True:
        request = f"work request from worker {worker_id}"
        req_socket.send(request.encode(),0)
        message = req_socket.recv()
        data = message
        accepted += 1
        work = (f"{data} and now proccesed")
        time.sleep((worker_id +1) * 5)
        push_socket.send(work.encode(),0)
        


def main():
    num_workers = 3
    threads = []
    context = zmq.Context()
    for i in range(num_workers):
        thread = threading.Thread(target=worker, args=(context,i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
