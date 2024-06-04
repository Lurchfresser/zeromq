fn main(){
    let context = zmq::Context::new();
    let requesters = context.socket(zmq::ROUTER).unwrap();
    requesters.bind("tcp://*:5556").unwrap();
    let repliers = context.socket(zmq::DEALER).unwrap();
    repliers.bind("tcp://*:5555").unwrap();
    
    zmq::proxy(&requesters, &repliers).unwrap();
}