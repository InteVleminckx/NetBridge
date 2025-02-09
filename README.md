# NetBridge

An easy way to interact with your existing code using another script.

## Server setup

```py
from netbridge.server.api import start_server

# Has to be a class because uses the class instance as shared object
class SomeClass:
    # Starts server when function is called, server will be ended when function is done
    @start_server 
    def some_function(self, ..., check_client_messages):

        # Can whenever you want to read the client messages and update these
        check_client_messages()

    # In the class where the server is created add two functions
    def to_dict(self):
        # Add what you want to share with the client
        return {...}

    def from_dict(self, new_data):
        self.some_member = new_data["key of the member"]
```

## Client setup

```py
from netbridge.client.api import connect, get_state, update_state

# Doesn't has to be a class ... 
class AnotherClass:
    # Connects the client when the function is called, client will disconnect when the function ends
    @connect
    def some_function(self, ..., client):
        self.client = client
        ...

    # Two functions can be used like this

    def func1(self):

        # Gets the state of the instance that has created the server (the result of to_dict)
        data, info = get_state(self.client)

        # Updates a certain class member of the instance. 
        # lists, tuples, sets, and dicts will be extends with the given data. Other values will be overriden
        data, info = update_state(self.client, {"key of the member": False, "other key": [1, 2, 3]})
```

## Examples

install the requirements.txt and install netbridge with the setup.py.

Then run examples/client/dearpygui_app.py and examples/server/pygame_app.py as two different scripts.
