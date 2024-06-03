extern crate zmq;
extern crate serde;
extern crate rmp_serde;

use serde::{Serialize, Deserialize};
use std::thread;
use std::time::Duration;

#[derive(Serialize, Deserialize, Debug)]
struct Message {
    id: u32,
    content: String,
}

fn main() {
    let context = zmq::Context::new();
    let socket = context.socket(zmq::PUSH).unwrap();
    socket.bind("tcp://127.0.0.1:5557").unwrap();

    for i in 0..100 {
        let message = Message {
            id: i,
            content: format!("Message {}", i),
        };
        let serialized = rmp_serde::to_vec(&message).unwrap();
        socket.send(&serialized, 0).unwrap();
        println!("Sent: {:?}", message);
        thread::sleep(Duration::from_secs(1));
    }
}
