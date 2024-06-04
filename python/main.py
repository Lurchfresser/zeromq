import zmq
import threading
import msgpack
import time
import random

def worker(context,worker_id):
    socket = context.socket(zmq.REP)
    socket.connect("tcp://127.0.0.1:5558")
    accepted = 0
    
    while True:
        message = socket.recv()
        data = msgpack.unpackb(message)
        accepted += 1
        reply = (f"Worker {worker_id} received: {data}, total accepted: {accepted}")
        time.sleep((worker_id +1) * 10)
        socket.send_string(reply)
        


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
