import json
import pickle
import base64
from ..message import Message
from ..message_code import MessageCode

def send_msg(client_socket, message: Message):
    """
    Sends an encoded message to the server via the provided client socket (synchronous).
    This function encodes the given message and sends it over the socket.

    Args:
        client_socket: The socket object used to communicate with the server.
        message (Message): The message to send, which will be encoded before sending.
    """
    message.data = json.dumps(message.data)
    encoded = encode_msg(message)
    client_socket.send(encoded)

def recv_msg(client_socket) -> Message:
    """
    Receives an encoded message from the server via the provided client socket (synchronous).

    This function blocks until the message is received from the server. It decodes the received message and 
    returns the resulting `Message` object.

    Args:
        client_socket: The socket object used to receive data from the server.

    Returns:
        Message: The decoded message object, or None if no data is received.
    """
    encoded = client_socket.recv(1024)

    if not encoded:
        return None 

    return decode_msg(encoded)

def encode_msg(message: Message) -> bytes:
    """
    Encodes the message into a base64-encoded byte string (synchronous).

    Args:
        message (Message): The message to encode.

    Returns:
        bytes: The base64-encoded byte string of the message.
    """
    pickled = pickle.dumps(message)
    return base64.b64encode(pickled)

def decode_msg(encoded) -> Message:
    """
    Decodes a base64-encoded byte string into a Message object (synchronous).

    Args:
        encoded (bytes): The base64-encoded byte string.

    Returns:
        Message: The decoded message, or None if there is an error.
    """
    try:
        pickled = base64.b64decode(encoded)
        return pickle.loads(pickled) 
    except (pickle.UnpicklingError, base64.binascii.Error, TypeError) as e:
        print(f"Error decoding message: {e}")
        return None

def handle_message(message: Message):

    match message.code:
        case MessageCode.OK:
            return json.loads(message.data), "OK"
        case MessageCode.ERROR:
            return None, json.loads(message.data)
        case _:
            return None, "Invalid message code."

def send_request(client, message: Message):
    send_msg(client.client_socket, message)  # Send request to the server
    response = recv_msg(client.client_socket)  # Receive the server's response

    if message.id == response.id:
        return response

    return Message(
        code=MessageCode.ERROR,
        data=json.dumps("Error: received the wrong message"),
        id=message.id
    )

    return response
