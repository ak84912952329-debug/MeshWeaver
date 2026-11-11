"""MeshWeaver Streamlit Dashboard."""

import asyncio
import streamlit as st

from broker import Broker
from worker import Worker
from task import Task, TaskStatus
from peer import Peer
from peer_integration import PeerTaskServer, PeerTaskClient


# Streamlit configuration
st.set_page_config(
    page_title="MeshWeaver",
    page_icon="🌐",
    layout="wide"
)


# Initialize dashboard state
if "communication_log" not in st.session_state:
    st.session_state.communication_log = []

if "tasks" not in st.session_state:
    st.session_state.tasks = []


# Initialize broker and workers
if "broker" not in st.session_state:

    broker = Broker()

    worker1 = Worker("worker-1")
    worker2 = Worker("worker-2")

    worker1.register_function(
        "identify",
        lambda: "Executed by Worker 1"
    )

    worker2.register_function(
        "identify",
        lambda: "Executed by Worker 2"
    )

    broker.register_worker(worker1)
    broker.register_worker(worker2)

    st.session_state.broker = broker


broker = st.session_state.broker


# Execute tasks through peer communication
async def execute_through_peer(broker, task, logs):

    server = PeerTaskServer("dashboard-server", broker)
    peer = Peer("dashboard-client")

    try:
        host, port = await server.start()
        logs.append("Task server started.")

        logs.append("Connecting to remote peer...")

        await peer.connect(host, port)
        logs.append("Peer connection established.")

        client = PeerTaskClient(peer)

        logs.append(
            f"Task request sent: {task.task_id}"
        )

        result = await client.submit_task(task)

        logs.append(
            f"Task response received: {task.task_id}"
        )

        logs.append(
            f"Task execution status: {result.status.value}"
        )

        logs.append(
            f"Task result: {result.result}"
        )

        return result

    except Exception as error:

        logs.append(f"Communication error: {error}")
        raise

    finally:

        await peer.close()
        await server.close()

        logs.append("Peer connection closed.")
        logs.append("Task server stopped.")


# Dashboard heading
st.title("🌐 MeshWeaver")
st.subheader("Peer-to-Peer Task Execution Dashboard")

st.divider()


# Dashboard metrics
col1, col2, col3 = st.columns(3)

completed = sum(
    task.status == TaskStatus.COMPLETED
    for task in st.session_state.tasks
)

failed = sum(
    task.status == TaskStatus.FAILED
    for task in st.session_state.tasks
)

with col1:
    st.metric(
        "Registered Workers",
        len(broker.workers)
    )

with col2:
    st.metric(
        "Tasks Completed",
        completed
    )

with col3:
    st.metric(
        "Failed Tasks",
        failed
    )


st.divider()


# Worker status
st.header("👷 Worker Status")

for worker in broker.workers:
    st.success(
        f"{worker.worker_id} - Available"
    )


st.divider()


# Peer communication status
st.header("📡 Peer Communication")

col1, col2 = st.columns(2)

with col1:
    st.metric("Connected Peers", 1)
    st.write("Client Peer: dashboard-client")

with col2:
    st.metric("Task Server", "Running")
    st.write("Server Peer: dashboard-server")


st.divider()


# Task submission
st.header("📤 Submit a Task")

function = st.selectbox(
    "Select Function",
    ["identify"]
)

if st.button("Submit Task"):

    task = Task(function)

    try:

        with st.spinner(
            "Connecting to peer and executing task..."
        ):

            result = asyncio.run(
                execute_through_peer(
                    broker,
                    task,
                    st.session_state.communication_log
                )
            )

        st.session_state.tasks.append(result)

        if result.status == TaskStatus.COMPLETED:

            st.success("Task executed successfully!")

            st.write(
                "Execution Result:",
                result.result
            )

        else:

            st.error(
                f"Task failed: {result.error}"
            )

    except Exception as error:

        st.error(
            f"Task submission failed: {error}"
        )


st.divider()


# Task execution history
st.header("📋 Task Execution History")

if not st.session_state.tasks:

    st.info("No tasks submitted yet.")

else:

    for task in reversed(st.session_state.tasks):

        with st.container(border=True):

            st.write(f"**Task ID:** {task.task_id}")

            st.write(
                f"**Function:** {task.function_name}"
            )

            st.write(
                f"**Status:** {task.status.value}"
            )

            if task.status == TaskStatus.COMPLETED:

                st.success(
                    f"Result: {task.result}"
                )

            else:

                st.error(
                    f"Error: {task.error}"
                )


st.divider()


# Peer communication log
st.header("📡 Peer Communication Log")

if st.session_state.communication_log:

    for event in reversed(
        st.session_state.communication_log
    ):

        st.info(event)

else:

    st.write("No communication events yet.")