import pygame
import pygame.camera
pygame.camera.init()


class Screen(pygame.Surface):
    def __init__(self, screen_w, screen_h, font, fontcolor):
        pygame.Surface.__init__(self, (screen_w, screen_h))

        self.screen_w = screen_w
        self.screen_h = screen_h

        # camera
        self.cameras = pygame.camera.list_cameras()
        self.webcam = pygame.camera.Camera(self.cameras[0])
        self.webcam.start()

        # surfaces
        self.screen = pygame.Surface((screen_w-60, screen_h-60))

    def draw(self):
        """Draws everything on itself. After resolving this module,
        object is ready to blit on designated surface"""

        self.fill((0, 0, 0))
        self.screen.fill((0, 0, 0))

        # cam
        img = self.webcam.get_image()
        img = pygame.transform.scale(img, (int(self.screen_w / 1.3), int(self.screen_h / 1.3)))
        self.screen.blit(img, (img.get_width() / 9, 0))

        self.blit(self.screen, (40, 20))
