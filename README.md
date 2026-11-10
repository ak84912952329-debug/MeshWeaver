# MeshWeaver
Zero-Dependency P2P Async Task Broker built with Python

A Python-based peer-to-peer task execution system that allows multiple peers to communicate, submit tasks, and receive execution results.

## Features

- Peer-to-peer communication using TCP connections.
- JSON-based message protocol.
- Task submission and result handling.
- Worker registration and task execution.
- Broker-based task distribution.
- Round-robin worker assignment.
- Error handling for failed tasks and connections.
- Unit testing for major components.

## Project Structure

```text
MeshWeaver/
│
├── broker.py
├── task.py
├── worker.py
├── peer.py
├── network.py
├── protocol.py
├── peer_integration.py
│
├── test_broker.py
├── test_worker.py
├── test_network.py
├── test_peer_integration.py
│
├── README.md
└── main.py
```

## Technologies Used

- Python 3
- Asyncio
- TCP Networking
- JSON
- Unittest

## How to Run

1. Clone the repository.
2. Open the project folder.
3. Run the tests using:

```bash
python -m unittest test_network -v
python -m unittest test_broker -v
python -m unittest test_worker -v
python -m unittest test_peer_integration -v
```

## Working

1. A peer establishes a connection with another peer.
2. The client sends a task request using the communication protocol.
3. The receiving peer validates the message.
4. The broker assigns the task to an available worker.
5. The worker executes the task.
6. The result is returned to the requesting peer.

## Conclusion

MeshWeaver demonstrates peer-to-peer communication and distributed task execution using Python. It combines networking, asynchronous communication, task management, and worker execution in one system.