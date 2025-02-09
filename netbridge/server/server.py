import asyncio
from .message_handler import handle_message, send_msg, recv_msg


class Server:
    def __init__(self, instance, host="localhost", port=8765):
        self.host = host
        self.port = port
        print(instance)
        self.instance = instance
        self.running = False
        self.clients = set()  # Track active client connections

    def is_running(self):
        return self.running

    async def handle_client(self, reader, writer):
        addr = writer.get_extra_info('peername')
        print(f"New connection from {addr}")

        # Add client to the active set
        self.clients.add(writer)

        try:
            while True:

                msg = await recv_msg(reader)
                if not msg: # Client disconnected
                    break  

                new_msg = handle_message(msg, self.instance)
                await send_msg(writer, new_msg)

        except asyncio.CancelledError:
            print(f"Connection with {addr} cancelled.")
        finally:
            # Remove client from active set when disconnected
            self.clients.discard(writer)
            writer.close()
            await writer.wait_closed()
            print(f"Connection from {addr} closed.")

    async def start(self):
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        print(f"Server is listening on {self.host}:{self.port}...")
        self.running = True

        async with server:
            await server.serve_forever()

