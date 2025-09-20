from random import randint

import pygame

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
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)
BORDER_COLOR = (93, 216, 228)

# Задержка (скорость игры)
SPEED = 10

# Настройка игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля
pygame.display.set_caption('Змейка')

# Настройка времени
clock = pygame.time.Clock()


# Базовый класс игровых объектов
class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self):
        """Инициализирует игровые объекты."""
        self.position = []
        self.body_color = None

    def draw(self):
        """Отрисовывает объект на экране."""
        pass


# Класс Apple
class Apple(GameObject):
    """Представляет яблоко на игровом поле."""

    def __init__(self):
        """Инициализирует яблоко и ставит его на случайную позицию."""
        super().__init__()
        self.randomize_position()
        self.body_color = APPLE_COLOR

    def randomize_position(self):
        """Устанавливает случайную позицию яблока."""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self):
        """Отрисовывает яблоко на экране."""
        apple_rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, apple_rect)
        pygame.draw.rect(screen, BORDER_COLOR, apple_rect, 1)


# Класс Snake
class Snake(GameObject):
    """Описание поведения змеи на игровом поле."""

    def __init__(self):
        """Инициализирует змею и задаёт начальные параметры."""
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.score = 0

    def get_head_position(self):
        """Возвращает позицию головы змеи."""
        return self.positions[0]

    def reset(self):
        """Восстанавливает изначальное состояние змеи."""
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.score = 0

    def move(self):
        """Производит перемещение змеи."""
        current_pos = self.get_head_position()
        next_x = current_pos[0] + self.direction[0] * GRID_SIZE
        next_y = current_pos[1] + self.direction[1] * GRID_SIZE

        # Перемещаемся
        self.positions.insert(0, (next_x % SCREEN_WIDTH,
                                  next_y % SCREEN_HEIGHT))

        if len(self.positions) > self.score + 1:
            self.positions.pop()

        # Проверка столкновения с телом змеи
        if self.positions.count(self.get_head_position()) > 1:
            raise Exception('Неееет..Ты сожрал сам себя :(')

    def draw(self):
        """Отрисовывает змею на экране."""
        for pos in self.positions:
            segment_rect = pygame.Rect(pos, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, segment_rect)
            pygame.draw.rect(screen, BORDER_COLOR, segment_rect, 1)

    def update_direction(self, new_dir):
        """
        Устанавливает новое направление, если оно не противоречит текущему.

        :param new_dir: Новое направление
        """
        opposite_dirs = {
            UP: DOWN,
            DOWN: UP,
            LEFT: RIGHT,
            RIGHT: LEFT
        }
        if new_dir != opposite_dirs[self.direction]:
            self.direction = new_dir


# Функция обработки событий клавиатуры
def handle_keys(snake):
    """Обрабатывает нажатия клавиш."""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        snake.update_direction(UP)
    elif keys[pygame.K_DOWN]:
        snake.update_direction(DOWN)
    elif keys[pygame.K_LEFT]:
        snake.update_direction(LEFT)
    elif keys[pygame.K_RIGHT]:
        snake.update_direction(RIGHT)


# Основная функция игры
def main():
    """Основная функция запуска игры."""
    snake = Snake()
    apple = Apple()
    running = True

    while running:
        clock.tick(SPEED)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        handle_keys(snake)
        try:
            snake.move()
        except Exception as e:
            print(f'Ошибка: {e}')
            break

        # Проверка попадания в яблоко
        if snake.get_head_position() == apple.position:
            snake.score += 1
            apple.randomize_position()

        # Отрисовка
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
# ...
