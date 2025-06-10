import arcade
import random

# Fenstergröße und Zellgröße
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
CELL_SIZE = 40

# Richtungskonstanten
UP = (0, 1)
DOWN = (0, -1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class SnakeGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Snake Game – Präsentationsversion")

        # Hintergrund-Sprite aus den eingebauten Arcade-Ressourcen
        self.background_sprite = arcade.Sprite(":resources:images/tiles/grassCenter.png")
        self.background_sprite.center_x = SCREEN_WIDTH // 2
        self.background_sprite.center_y = SCREEN_HEIGHT // 2
        self.background_sprite.width = SCREEN_WIDTH
        self.background_sprite.height = SCREEN_HEIGHT

        # Hintergrund-SpriteList erstellen
        self.background_list = arcade.SpriteList()
        self.background_list.append(self.background_sprite)

        # SpriteList für den Apfel
        self.sprite_list = arcade.SpriteList()
        self.apple_sprite = arcade.Sprite(":resources:images/items/gold_1.png")
        self.apple_sprite.width = CELL_SIZE +20
        self.apple_sprite.height = CELL_SIZE +20
        self.sprite_list.append(self.apple_sprite)

        # Wir speichern hier den Pfad zur integrierten Textur für Schlangensegmente
        self.snake_texture_path = ":resources:/images/topdown_tanks/treeGreen_large.png"
        # Erstelle leere SpriteList für die Schlangensegmente
        self.snake_sprite_list = arcade.SpriteList()

        self.sound_coin = arcade.load_sound(":resources:/sounds/coin5.wav")
        self.sound_gameover = arcade.load_sound(":resources:/sounds/gameover3.wav")
        self.sound_begin = arcade.load_sound(":resources:/sounds/upgrade1.wav")

        self.reset()

    def reset(self):
        arcade.play_sound(self.sound_begin)
        self.direction = RIGHT
        self.snake = [(5, 5)]  # Startposition als Gitterkoordinaten
        self.food = self.place_food()
        self.game_over = False
        self.score = 0

        # Bewegungssteuerung
        self.move_interval = 0.2
        self.time_since_last_move = 0.0

        # Positioniere den Apfel anhand der Futterkoordinate
        self.apple_sprite.center_x = self.food[0] * CELL_SIZE + CELL_SIZE / 2
        self.apple_sprite.center_y = self.food[1] * CELL_SIZE + CELL_SIZE / 2

        # Aktualisiere die Schlangen-SpriteList
        self.update_snake_sprite_list()

    def update_snake_sprite_list(self):
        # Erstelle eine neue SpriteList für die Schlangensegmente
        self.snake_sprite_list = arcade.SpriteList()
        for x, y in self.snake:
            segment = arcade.Sprite(self.snake_texture_path)
            segment.width = CELL_SIZE
            segment.height = CELL_SIZE
            segment.center_x = x * CELL_SIZE + CELL_SIZE / 2
            segment.center_y = y * CELL_SIZE + CELL_SIZE / 2
            self.snake_sprite_list.append(segment)

    def place_food(self):
        while True:
            x = random.randint(0, SCREEN_WIDTH // CELL_SIZE - 1)
            y = random.randint(0, SCREEN_HEIGHT // CELL_SIZE - 1)
            if (x, y) not in self.snake:
                return (x, y)

    def on_draw(self):
        self.clear()


        self.background_list.draw()

        if self.game_over:
            arcade.draw_text("GAME OVER – Drücke [Leertaste] zum Neustart",
                             SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                             arcade.color.RED, 20, anchor_x="center")
            arcade.draw_text(f"Punkte: {self.score}",
                             SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 40,
                             arcade.color.WHITE, 16, anchor_x="center")
            return

        # Zeichne alle Schlangensegmente
        self.snake_sprite_list.draw()

        # Zeichne weitere Sprites (z. B. den Apfel)
        self.sprite_list.draw()

        # Punktestand anzeigen
        arcade.draw_text(f"Punkte: {self.score}",
                         10, SCREEN_HEIGHT - 30,
                         arcade.color.WHITE, 14)

    def on_update(self, delta_time):
        if self.game_over:
            return

        self.time_since_last_move += delta_time
        if self.time_since_last_move < self.move_interval:
            return
        self.time_since_last_move = 0

        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # Kollision mit dem eigenen Körper oder dem Spielfeldrand
        if (new_head in self.snake or
                new_head[0] < 0 or new_head[0] >= SCREEN_WIDTH // CELL_SIZE or
                new_head[1] < 0 or new_head[1] >= SCREEN_HEIGHT // CELL_SIZE):
            arcade.play_sound(self.sound_gameover)
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            arcade.play_sound(self.sound_coin)
            self.food = self.place_food()
            self.apple_sprite.center_x = self.food[0] * CELL_SIZE + CELL_SIZE / 2
            self.apple_sprite.center_y = self.food[1] * CELL_SIZE + CELL_SIZE / 2
        else:
            self.snake.pop()

        self.update_snake_sprite_list()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.UP and self.direction != DOWN:
            self.direction = UP
        elif symbol == arcade.key.DOWN and self.direction != UP:
            self.direction = DOWN
        elif symbol == arcade.key.LEFT and self.direction != RIGHT:
            self.direction = LEFT
        elif symbol == arcade.key.RIGHT and self.direction != LEFT:
            self.direction = RIGHT
        elif symbol == arcade.key.SPACE and self.game_over:
            self.reset()


if __name__ == "__main__":
    game = SnakeGame()
    arcade.run()