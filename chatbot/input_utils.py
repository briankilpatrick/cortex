# chatbot/input_utils.py

# Import threading and queue for handling input with a timeout
import threading
import queue


# Function to get user input with a timeout
def input_with_timeout(prompt, timeout):
    """
    Waits for the user to type input.
    If nothing is typed within `timeout` seconds, returns None.
    """
    q = queue.Queue()  # a safe way to share the input between threads

    # Inner function runs in a separate thread to get input
    def inner():
        q.put(input(prompt))  # put whatever user types into the queue

    thread = threading.Thread(target=inner, daemon=True)  # create a background thread
    thread.start()  # start the thread

    try:
        return q.get(timeout=timeout)  # wait for input until timeout
    except queue.Empty:
        return None  # if timeout occurs, return None
