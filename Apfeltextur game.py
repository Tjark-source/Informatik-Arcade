import arcade
import random

# Fenstergröße und Zellgröße
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
CELL_SIZE = 20

# Richtungskonstanten
UP = (0, 1)
DOWN = (0, -1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class SnakeGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Snake Game – Präsentationsversion")
        arcade.set_background_color(arcade.color.BLACK)
        self.reset()

    def reset(self):
        self.direction = RIGHT
        self.snake = [(5, 5)]
        self.food = self.place_food()
        self.game_over = False
        self.score = 0

        # Bewegungssteuerung: die Zeit, die vor dem nächsten Schritt vergehen soll (in Sekunden)
        self.move_interval = 0.3  # Erhöhe diesen Wert, um die Schlange langsamer zu machen
        self.time_since_last_move = 0.0

    def place_food(self):
        while True:
            x = random.randint(0, SCREEN_WIDTH // CELL_SIZE - 1)
            y = random.randint(0, SCREEN_HEIGHT // CELL_SIZE - 1)
            if (x, y) not in self.snake:
                return (x, y)

    def on_draw(self):
        self.clear()

        if self.game_over:
            arcade.draw_text("GAME OVER – Drücke [Leertaste] zum Neustart",
                             SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                             arcade.color.RED, 20, anchor_x="center")
            arcade.draw_text(f"Punkte: {self.score}",
                             SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 40,
                             arcade.color.WHITE, 16, anchor_x="center")
            return

        # Zeichne die Schlange
        for x, y in self.snake:
            arcade.draw_lbwh_rectangle_filled(
                x * CELL_SIZE,  # linke untere X-Koordinate
                y * CELL_SIZE,  # linke untere Y-Koordinate
                CELL_SIZE,  # Breite
                CELL_SIZE,  # Höhe
                arcade.color.GREEN
            )

        # Zeichne das Futter
        fx, fy = self.food
        arcade.draw_lbwh_rectangle_filled(
            fx * CELL_SIZE,
            fy * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE,
            arcade.color.RED
        )

        # Punktestand anzeigen
        arcade.draw_text(f"Punkte: {self.score}",
                         10, SCREEN_HEIGHT - 30,
                         arcade.color.WHITE, 14)

    def on_update(self, delta_time):
        if self.game_over:
            return

        # Summiere die verstrichene Zeit
        self.time_since_last_move += delta_time

        # Bewege die Schlange nur, wenn das Intervall erreicht wurde
        if self.time_since_last_move < self.move_interval:
            return
        self.time_since_last_move = 0

        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # Kollisionserkennung: Wand oder Eigenkollision
        if (new_head in self.snake or
                new_head[0] < 0 or new_head[0] >= SCREEN_WIDTH // CELL_SIZE or
                new_head[1] < 0 or new_head[1] >= SCREEN_HEIGHT // CELL_SIZE):
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        # Prüfe, ob Futter gefressen wurde
        if new_head == self.food:
            self.score += 1
            self.food = self.place_food()
        else:
            self.snake.pop()

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