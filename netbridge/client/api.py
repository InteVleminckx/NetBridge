from .client import Client
from .message_handler import handle_message, send_msg, recv_msg, send_request
from ..message import Message
from ..message_code import MessageCode
import uuid

def connect(func):
    """Decorator to handle client connection and disconnection."""
    def wrapper(self, *args, **kwargs):
        client = Client()
        client.connect()
        try:
            func(self, client, *args, **kwargs)
        finally:
            client.close()
    return wrapper


def get_state(client):
    """
    Sends a GET request to the server to retrieve the current state.

    This function creates a GET request message, sends it to the server, and waits for a response. 
    The response is then processed by `handle_message`, which handles the message based on its code.

    Args:
        client: The client object used to send and receive messages from the server.

    Returns:
        tuple: A tuple containing the data and information from the server's response, 
               as returned by the `handle_message` function.
    """

    m_id = str(uuid.uuid4())

    message = Message(
        code=MessageCode.GET,
        id=m_id
    )

    response = send_request(client, message)

    data, info = handle_message(response)  # Process the response message
    return data, info  # Return processed data and information


def update_state(client, update_data):
    """
    Sends a PUT request to the server to update the state with new data.

    This function creates a PUT request message with the provided update data, sends it to the server, 
    and waits for the response. The response is then processed by `handle_message`. 
    If the update is successful, it returns True and the information; otherwise, it returns False and the error information.

    Args:
        client: The client object used to send and receive messages from the server.
        update_data (dict): The dictionary containing the data to be updated on the server.

    Returns:
        tuple: A tuple containing a boolean indicating success or failure (True/False), 
               and the information from the server's response.
    """
    
    m_id = str(uuid.uuid4())

    # Create PUT request message with update data
    message = Message(
        code=MessageCode.PUT,
        data=update_data,
        id=m_id
    )

    response = send_request(client, message)

    data, info = handle_message(response)  # Process the response message
    if not data:  # If data is None or not valid, return failure
        return False, info
    return True, info  # Return success and the info from the server


