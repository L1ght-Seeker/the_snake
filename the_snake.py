from random import randint

import pygame as pg

# Размеры экрана и сетка
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
SNAKE_BODY_COLOR = (0, 250, 0)
APPLE_BODY_COLOR = (255, 0, 0)
BORDER_COLOR = (93, 216, 228)

# Скорость игры
SPEED = 10

# Настройка игрового окна
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля
pg.display.set_caption('Змейка')

# Настройка времени
clock = pg.time.Clock()


# Базовый класс игровых объектов
class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, body_color=None):
        """Инициализирует игровые объекты."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color or BOARD_BACKGROUND_COLOR

    def draw(self):
        """Отрисовывает объект на экране."""


# Класс Apple
class Apple(GameObject):
    """Представляет яблоко на игровом поле."""

    def __init__(self, occupied_positions=None):
        """Инициализирует яблоко и ставит его на случайную позицию."""
        super().__init__(body_color=APPLE_BODY_COLOR)
        self.randomize_position(occupied_positions or [])

    def randomize_position(self, occupied_positions):
        """Устанавливает случайную позицию яблока."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if self.position not in occupied_positions:
                break

    def draw(self):
        """Отрисовывает яблоко на экране."""
        apple_rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, apple_rect)
        pg.draw.rect(screen, BORDER_COLOR, apple_rect, 1)


# Класс Snake
class Snake(GameObject):
    """Описание поведения змеи на игровом поле."""

    def __init__(self):
        """Инициализирует змею и задаёт начальные параметры."""
        super().__init__(body_color=SNAKE_BODY_COLOR)
        self.reset()
        self.direction = RIGHT  # Начальное направление вон туда 👉

    def reset(self):
        """Восстанавливает изначальное состояние змеи."""
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.length = 1
        self.last = None

    def get_head_position(self):
        """Возвращает позицию головы змеи."""
        return self.positions[0]

    def move(self):
        """Производит перемещение змеи."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        self.positions.insert(
            0,
            ((head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH,
             (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT),
        )
        self.last = (
            self.positions.pop() if len(self.positions) > self.length else None
        )

    def draw(self):
        """Отрисовывает змею на экране."""
        for pos in self.positions:
            segment_rect = pg.Rect(pos, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, segment_rect)
            pg.draw.rect(screen, BORDER_COLOR, segment_rect, 1)
        if self.last is not None:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self, new_dir):
        """
        Устанавливает новое направление, если оно не противоречит текущему.

        :param new_dir: Новое направление
        """
        opposite_dirs = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}
        if new_dir != opposite_dirs[self.direction]:
            self.direction = new_dir


def handle_keys(event, snake):
    """Обрабатывает нажатия клавиш."""
    if event.type == pg.KEYDOWN:
        if event.key == pg.K_ESCAPE:  # Обработка клавиши ESC!!!! ура-ура :3
            pg.quit()
            quit()
        elif event.key == pg.K_UP:
            snake.update_direction(UP)
        elif event.key == pg.K_DOWN:
            snake.update_direction(DOWN)
        elif event.key == pg.K_LEFT:
            snake.update_direction(LEFT)
        elif event.key == pg.K_RIGHT:
            snake.update_direction(RIGHT)


# Основная функция игры
def main():
    """Основная функция запуска игры."""
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        screen.fill(BOARD_BACKGROUND_COLOR)

        clock.tick(SPEED)
        for event in pg.event.get():
            handle_keys(event, snake)

        snake.move()

        # Проверка попадания в яблоко
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        # Проверка столкновения с телом змеи
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)

        # Отрисовка всех элементов
        snake.draw()
        apple.draw()
        pg.display.flip()


if __name__ == '__main__':
    main()

    # P.S На ты не против, забыл сказать)
    # Мне нравится как ты всё объясняешь)
    # Желаю хорошего дня!
    # Выход на Esc)
