from random import choice, randint

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
SNAKE_BODY_COLOR = (0, 255, 0)
APPLE_BODY_COLOR = (255, 0, 0)
BORDER_COLOR = (93, 216, 228)

# Задержка (скорость игры)
SPEED = 8

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
        pass


# Класс Apple
class Apple(GameObject):
    """Представляет яблоко на игровом поле."""

    def __init__(self, occupied_positions=None):
        """Инициализирует яблоко и ставит его на случайную позицию."""
        if occupied_positions is None:
            occupied_positions = []
        super().__init__(body_color=APPLE_BODY_COLOR)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions):
        """Устанавливает случайную позицию яблока."""
        while True:
            position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if position not in occupied_positions:
                break
        self.position = position

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

    def reset(self):
        """Восстанавливает изначальное состояние змеи."""
        center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.positions = [center]
        self.length = 1
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.last = None

    def get_head_position(self):
        """Возвращает позицию головы змеи."""
        return self.positions[0]

    def move(self):
        """Производит перемещение змеи."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        next_x = (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH
        next_y = (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT
        self.positions.insert(0, (next_x, next_y))
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


# Вспомогательная функция для обработки событий клавиатуры
def handle_keys(event, snake):
    """Обрабатывает нажатия клавиш."""
    if event.type == pg.KEYDOWN:
        if event.key == pg.K_UP:
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
        clock.tick(SPEED)
        for event in pg.event.get():
            handle_keys(event, snake)

        snake.move()

        # Проверка попадания в яблоко
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        # Логика проверки столкновений
        if snake.get_head_position() in snake.positions[1:]:
            break

        # Частичная отрисовка
        snake.draw()
        apple.draw()
        pg.display.flip()

    pg.quit()


if __name__ == '__main__':
    main()
