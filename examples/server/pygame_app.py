import pygame
from netbridge.server.api import start_server
import time

class PygameApp:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.WIDTH, self.HEIGHT = width, height
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Pygame + NetBridge Socket")
        self.squares = []  # List to store square positions
        self.running = True
        self.clock = pygame.time.Clock()
        self.fps = 0
        self.check = None

    def to_dict(self):
        return {
            "squares": self.squares,
            "running": self.running,
            "fps": self.fps
        }

    def from_dict(self, r_dict):
        self.squares = r_dict["squares"]
        self.running = r_dict["running"]

    @start_server
    def run(self, check_client_messages):
        while self.running:
            self.clock.tick()  # Limit the frame rate and get the time since the last call
            self.fps = self.clock.get_fps()  # Get the current FPS
            self.screen.fill((30, 30, 30))  # Clear the screen each frame

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Draw all squares
            for x, y in self.squares:
                pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(x, y, 50, 50))

            pygame.display.update()

            # Fetch messages from the server
            check_client_messages()

        pygame.quit()

if __name__ == "__main__":
    app = PygameApp()
    app.run()
