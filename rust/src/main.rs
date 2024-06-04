extern crate rmp_serde;
extern crate serde;
extern crate zmq;

use serde::{Deserialize, Serialize};
use std::thread;
use std::time::Duration;

#[derive(Serialize, Deserialize, Debug)]
struct Message {
    id: u32,
    content: String,
}

fn main() {
    let context = zmq::Context::new();
    let rep_socket = context.socket(zmq::REP).unwrap();
    rep_socket.connect("tcp://localhost:5555").unwrap();
    let pull_socket = context.socket(zmq::PULL).unwrap();
    pull_socket.bind("tcp://*:5557").unwrap();

    let poll_items = &mut [
        rep_socket.as_poll_item(zmq::POLLIN),
        pull_socket.as_poll_item(zmq::POLLIN),
    ];

    loop {
        zmq::poll(poll_items, -1).unwrap();
        if poll_items[0].is_readable() {
            let received = rep_socket.recv_string(0).unwrap().unwrap();
            let message = &(format!("Received: {:?}", received))[..];
            rep_socket.send(message, 0).unwrap();
            println!("Sent: {:?}", message);
        }
        if poll_items[1].is_readable() {
            let received = pull_socket.recv_string(0).unwrap().unwrap();
            println!("{:?} and received again", received);
        }
    }
}
