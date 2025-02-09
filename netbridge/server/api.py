from .server import Server


import asyncio

def start_server(func):
    def wrapper(self):
        # Create an instance of the server with access to self (instance of A)
        server = Server(self)

        async def run_server():
            """Start the asyncio server and keep it running."""
            await server.start()

        # Create a new event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Start the server as a background task
        server_task = loop.create_task(run_server())

        # Allow some time for the server to start
        while not server.is_running():
            loop.run_until_complete(asyncio.sleep(0.1))

        def check_client_messages():
            """This function can be called inside the while loop to check messages."""
            loop.run_until_complete(asyncio.sleep(0))  # Allow event loop to process messages

        try:
            # Call the original function, passing the check function
            func(self, check_client_messages)
        finally:
            # If func(self) finishes, stop the server and clean up
            print("Shutting down server...")

            # Cancel the server task
            server_task.cancel()

            try:
                loop.run_until_complete(server_task)
            except asyncio.CancelledError:
                pass  # Task was cancelled, ignore error

            # Close the event loop properly
            loop.close()
            print("Server stopped.")

    return wrapper

