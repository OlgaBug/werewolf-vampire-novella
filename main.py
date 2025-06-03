import pygame
import sys
import os

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Любовь сквозь тьму")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

# Шрифты
font = pygame.font.Font(None, 32)
button_font = pygame.font.Font(None, 24)

# Загрузка изображений (замените на свои)
def load_image(name):
    try:
        image = pygame.image.load(f"images/{name}.jpg")
        return image
    except:
        print(f"Ошибка загрузки изображения: {name}")
        return pygame.Surface((WIDTH, HEIGHT))

backgrounds = {
    "forest": load_image("forest"),
    "mansion": load_image("mansion"),
}

characters = {
    "werewolf": load_image("werewolf"),
    "vampire": load_image("vampire"),
}

# Сюжетные сцены (можно расширить)
scenes = [
    {
        "background": "forest",
        "character": "werewolf",
        "text": "Вы — Алиса, молодая оборотень. Сегодня полнолуние, и вы тайно встречаетесь с вампиром Лукасом...",
        "choices": [
            {"text": "Пойти на встречу", "next_scene": 1},
            {"text": "Остаться дома", "next_scene": 2},
        ]
    },
    {
        "background": "mansion",
        "character": "vampire",
        "text": "Лукас ждёт вас в старом особняке. Его семья не одобряет ваши отношения...",
        "choices": [
            {"text": "Признаться в чувствах", "next_scene": 3},
            {"text": "Сбежать", "next_scene": 4},
        ]
    },
    # Добавьте больше сцен по аналогии...
]

current_scene = 0

# Основной цикл игры
def main():
    global current_scene

    running = True
    while running:
        screen.fill(BLACK)

        # Отрисовка текущей сцены
        scene = scenes[current_scene]
        screen.blit(backgrounds[scene["background"]], (0, 0))
        screen.blit(characters[scene["character"]], (300, 200))

        # Текст сцены
        text_surface = font.render(scene["text"], True, WHITE)
        screen.blit(text_surface, (50, 50))

        # Кнопки выбора
        for i, choice in enumerate(scene["choices"]):
            button_rect = pygame.Rect(100, 400 + i * 50, 600, 40)
            pygame.draw.rect(screen, GRAY, button_rect)
            choice_text = button_font.render(choice["text"], True, WHITE)
            screen.blit(choice_text, (110, 410 + i * 50))

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, choice in enumerate(scene["choices"]):
                    button_rect = pygame.Rect(100, 400 + i * 50, 600, 40)
                    if button_rect.collidepoint(mouse_pos):
                        current_scene = choice["next_scene"]

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()