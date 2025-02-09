import json
import pickle
import base64
from ..message import Message
from ..message_code import MessageCode

async def send_msg(writer, message: Message):
    """
    Sends an encoded message to the provided writer (synchronous).

    This function encodes the given message and sends it over the provided
    writer object. It ensures the message is sent immediately by calling 
    `flush()` to clear the write buffer.

    Args:
        writer: The writer object (e.g., a socket or file-like object) used to send data (synchronous).
        message (Message): The message to send, which will be encoded before sending.
    """
    encoded = encode_msg(message)
    writer.write(encoded)  # Write the encoded message to the writer


async def recv_msg(reader) -> Message:
    """
    Receives an encoded message from the provided reader (synchronous).

    This function blocks until the message is received from the reader.
    It decodes the received message and returns the resulting `Message` object.

    Args:
        reader: The reader object (e.g., a socket or file-like object) used to receive data (synchronous).

    Returns:
        Message: The decoded message object, or None if no data is received.
    """
    encoded = await reader.read(1024)  # Read data from the reader synchronously
    if not encoded:
        return None  # Return None if no data is received

    return decode_msg(encoded)  # Decode and return the message


def encode_msg(message: Message) -> bytes:
    """
    Encodes a `Message` object into a base64-encoded byte string.

    This function serializes the message using `pickle`, and then encodes it 
    to base64 to ensure the data is suitable for transmission over networks.

    Args:
        message (Message): The message to encode.

    Returns:
        bytes: A base64-encoded byte string representing the serialized message.
    """
    pickled = pickle.dumps(message)  # Serialize the message
    return base64.b64encode(pickled)  # Base64 encode the serialized data


def decode_msg(encoded) -> Message:
    """
    Decodes a base64-encoded byte string into a `Message` object.

    This function reverses the process done by `encode_msg` and restores
    the original `Message` object from the base64-encoded byte string.

    Args:
        encoded (bytes): A base64-encoded byte string representing a serialized message.

    Returns:
        Message: The decoded `Message` object, or None if there is an error during decoding.
    """
    try:
        pickled = base64.b64decode(encoded)  # Decode the base64 string
        return pickle.loads(pickled)  # Deserialize and return the message object
    except (pickle.UnpicklingError, base64.binascii.Error, TypeError) as e:
        print(f"Error decoding message: {e}")  # Print error if decoding fails
        return None

def handle_message(message: Message, cls_instance) -> Message:
    """
    Handles incoming messages and routes them based on their message code.

    Depending on the message code:
    - Calls `handle_get` for GET requests.
    - Calls `handle_put` for PUT requests.
    - Calls `handle_invalid` for unknown codes.

    Args:
        message (Message): The incoming message object.
        cls_instance: The instance of the class to operate on.

    Returns:
        Message: A response message based on the processed request.
    """
    match message.code:
        case MessageCode.GET:
            return handle_get(cls_instance, message.id)
        case MessageCode.PUT:
            return handle_put(message.data, cls_instance, message.id)
        case _:
            return handle_invalid(message.id)

def handle_get(cls_instance, m_id) -> Message:
    """
    Handles GET requests by returning the serialized state of cls_instance.

    Args:
        cls_instance: The instance whose data should be retrieved.

    Returns:
        Message: A response containing the serialized data of cls_instance.
    """
    return Message(
        code=MessageCode.OK,
        data=dump_data(cls_instance.to_dict()),
        id=m_id
    )

def handle_put(data, cls_instance, m_id) -> Message:
    """
    Handles PUT requests by updating cls_instance with new data.

    - Loads `data` into a Python dictionary.
    - Compares it with the current state of `cls_instance`.
    - Merges new iterable values while preserving `cls_instance` modifications.
    - Updates `cls_instance` with the new merged data.

    Args:
        data (str): The JSON-encoded data to update the instance with.
        cls_instance: The instance to be updated.

    Returns:
        Message: A response confirming the update.
    """
    
    l_data = load_data(data)
    i_data = cls_instance.to_dict()
    i_data_new = update_data(i_data, l_data)
    cls_instance.from_dict(i_data_new)

    return Message(
        code=MessageCode.OK,
        data=dump_data("Instance successfully updated."),
        id=m_id
    )

def handle_invalid(m_id) -> Message:
    """
    Handles invalid message codes by returning an error response.

    Returns:
        Message: An error response message indicating an invalid code.
    """
    return Message(
        code=MessageCode.ERROR,
        data=dump_data("Invalid message code.")
    )

def load_data(data):
    """
    Deserializes a JSON-encoded string into a Python object.

    Args:
        data (str): The JSON string to decode.

    Returns:
        dict or list: The decoded Python object.
    """
    return json.loads(data)

def dump_data(data):
    """
    Serializes a Python object into a JSON-encoded string.

    Args:
        data (dict or list): The Python object to encode.

    Returns:
        str: The JSON string representation of `data`.
    """
    return json.dumps(data)

def update_data(i_data: dict, l_data: dict):
    """
    Updates i_data with changes from l_data while preserving local modifications.

    This function:
    - **Overwrites primitive values** (integers, strings, booleans) from l_data.
    - **Adds only new iterable elements** (lists, sets, tuples) after the last common value.
    - **Handles nested dictionaries** recursively.

    Args:
        i_data (dict): The original dictionary containing local modifications.
        l_data (dict): The updated dictionary with new data.

    Returns:
        dict: The updated i_data dictionary with changes from l_data applied.
    """

    for key, values in l_data.items():
        if isinstance(values, list):
            i_data[key].extend(values)
        elif isinstance(values, tuple):
            i_data[key] = tuple(list(i_data[key]) + list(values))
        elif isinstance(values, set):
            i_data[key].update(values)
        elif isinstance(values, dict):
            i_data[key].update(values)
        else:
            i_data[key] = values


    return i_data

