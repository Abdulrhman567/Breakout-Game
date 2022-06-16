import pygame
import os
import sys

pygame.font.init()

# RESOLUTION AND FPS
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600
FPS = 60

# FONTS
GAME_OVER_FONT = pygame.font.SysFont("comicsans", 100)

# EVENTS
BRICKS_EMPTY = pygame.USEREVENT + 1


class Sprite(pygame.sprite.Sprite):
    def __init__(self, img, x_pos, y_pos):
        """
        Creating Sprites and give each Sprite a location
        :param img: sprite img
        :param x_pos: x position of the sprite
        :param y_pos: y position of the sprite
        """
        super().__init__()
        self.image = pygame.image.load(os.path.join("Assets", img))
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos


class Game:
    def __init__(self):
        """
        Creating the window and set up all the Sprites and Rectangles
        """
        self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Breakout!")

        self.top_border = pygame.Rect(0, 0, SCREEN_WIDTH, 10)
        self.left_border = pygame.Rect(0, 0, 10, SCREEN_HEIGHT)
        self.right_border = pygame.Rect(SCREEN_WIDTH - 10, 0, 10, SCREEN_HEIGHT)

        self.clock = pygame.time.Clock()
        self.game_on = True

        self.bat_vel = 6
        self.bat_group = pygame.sprite.Group()
        self.bat = Sprite("bat.png", SCREEN_WIDTH/2 - 40, 500)
        self.bat_group.add(self.bat)

        self.ball_vel = [3, 3]
        self.ball_group = pygame.sprite.Group()
        self.ball = Sprite("ball.png", self.bat.rect.x + 40 - 17/2, self.bat.rect.y - 37)
        self.ball_group.add(self.ball)

        self.bricks_group = pygame.sprite.Group()
        bricks_pos_height = 100
        for _ in range(5):
            bricks_pos_width = 110
            for _ in range(12):
                brick = Sprite("brick.png", bricks_pos_width, bricks_pos_height)
                bricks_pos_width += 67
                self.bricks_group.add(brick)
            bricks_pos_height += 36

    def game_over(self):
        """
        Display the game over text and stops and delays the game for 2 seconds
        :return: None
        """
        game_over_text = GAME_OVER_FONT.render("Horayyy!", True, "White")
        self.window.blit(game_over_text, (SCREEN_WIDTH/2 - game_over_text.get_width()/2,
                                          SCREEN_HEIGHT/2 - game_over_text.get_height()/2))

        pygame.display.update()
        pygame.time.delay(2000)

    def ball_collision_movements(self, collided_rect):
        """
        Point out which direction the collision happened and change the ball direction according the collision direction
        :param collided_rect: the rect that the ball will collide with
        :return: None
        """
        collision_tolerance = 10
        if abs(collided_rect.top - self.ball.rect.bottom) < collision_tolerance and self.ball_vel[1] > 0:
            self.ball_vel[1] *= -1
        if abs(collided_rect.bottom - self.ball.rect.top) < collision_tolerance and self.ball_vel[1] < 0:
            self.ball_vel[1] *= -1
        if abs(collided_rect.right - self.ball.rect.left) < collision_tolerance and self.ball_vel[0] < 0:
            self.ball_vel[0] *= -1
        if abs(collided_rect.left - self.ball.rect.right) < collision_tolerance and self.ball_vel[0] > 0:
            self.ball_vel[0] *= -1

    def handle_bat_movement(self, key_pressed):
        """
        Moves the Bat left and right by pressing the left and right keys
        :param key_pressed: which key has been pressed
        :return: None
        """
        if key_pressed[pygame.K_LEFT] and self.bat.rect.x > self.left_border.width:
            self.bat.rect.x -= self.bat_vel
        if key_pressed[pygame.K_RIGHT] and\
                self.bat.rect.x < SCREEN_WIDTH - self.bat.image.get_width() - self.right_border.width:
            self.bat.rect.x += self.bat_vel

    def handle_ball_movement(self):
        """
        Takes care of the ball movements and collisions with different rects and sprites
        :return: None
        """
        self.ball.rect = self.ball.rect.move(self.ball_vel)
        if self.ball.rect.colliderect(self.top_border):
            self.ball_vel[1] *= -1
        if self.ball.rect.colliderect(self.left_border) or self.ball.rect.colliderect(self.right_border):
            self.ball_vel[0] *= -1
        if self.ball.rect.y > SCREEN_HEIGHT:
            self.ball.rect.x = self.bat.rect.x + 40 - 17/2
            self.ball.rect.y = self.bat.rect.y - 37

        if self.ball.rect.colliderect(self.bat.rect):
            self.ball_collision_movements(self.bat.rect)

        if self.bricks_group:
            for brick in self.bricks_group:
                if self.ball.rect.colliderect(brick.rect):
                    self.ball_collision_movements(brick.rect)
                    self.bricks_group.remove(brick)
        else:
            pygame.event.post(pygame.event.Event(BRICKS_EMPTY))

    def draw_window(self):
        """
        Displays the different Objects on the window
        :return: None
        """
        self.window.fill("Black")

        pygame.draw.rect(self.window, 'White', self.top_border)
        pygame.draw.rect(self.window, 'White', self.left_border)
        pygame.draw.rect(self.window, 'White', self.right_border)

        self.bat_group.draw(self.window)

        self.ball_group.draw(self.window)

        self.bricks_group.draw(self.window)

        pygame.display.update()

    def play_game(self):
        while self.game_on:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_on = False

                if event.type == BRICKS_EMPTY:
                    self.game_over()
                    play_again = Game()
                    play_again.play_game()

            key_pressed = pygame.key.get_pressed()
            self.handle_bat_movement(key_pressed)
            self.handle_ball_movement()

            self.draw_window()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.play_game()
