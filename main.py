import pygame
import sys
import os

# Инициализация Pygame
pygame.init()


# Конфигурация игры
class Config:
    WIDTH, HEIGHT = 800, 600
    FPS = 60
    FONT_SIZE = 32
    BUTTON_FONT_SIZE = 24
    CHARACTER_POS = (300, 200)
    TEXT_POS = (50, 50)
    BUTTON_WIDTH = 600
    BUTTON_HEIGHT = 40
    BUTTON_START_Y = 400
    BUTTON_SPACING = 50


# Настройки окна
screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
pygame.display.set_caption("Любовь сквозь тьму")
clock = pygame.time.Clock()


# Цвета
class Colors:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (100, 100, 100)
    HIGHLIGHT = (150, 150, 150)


# Шрифты
font = pygame.font.Font(None, Config.FONT_SIZE)
button_font = pygame.font.Font(None, Config.BUTTON_FONT_SIZE)


def load_image(name: str) -> pygame.Surface:
    try:
        for ext in ['.jpg', '.png']:
            try:
                path = os.path.join("images", f"{name}{ext}")
                return pygame.image.load(path)
            except FileNotFoundError:
                continue
        raise FileNotFoundError
    except Exception as e:
        print(f"Ошибка загрузки изображения {name}: {e}")
        return pygame.Surface((Config.WIDTH, Config.HEIGHT))


# Функция для отрисовки текста
def render_text_box(text: str) -> pygame.Surface:
    words = text.split(' ')
    lines = []
    current_line = []

    for word in words:
        test_line = ' '.join(current_line + [word])
        if font.size(test_line)[0] <= Config.WIDTH - 100:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]

    if current_line:
        lines.append(' '.join(current_line))

    rendered_lines = [font.render(line, True, Colors.WHITE) for line in lines]
    text_surface = pygame.Surface((Config.WIDTH - 100, len(rendered_lines) * Config.FONT_SIZE), pygame.SRCALPHA)

    for i, line in enumerate(rendered_lines):
        text_surface.blit(line, (0, i * Config.FONT_SIZE))

    return text_surface


# Функция для отрисовки кнопок
def draw_button(text: str, position: int, mouse_pos: tuple) -> pygame.Rect:
    y = Config.BUTTON_START_Y + position * Config.BUTTON_SPACING
    button_rect = pygame.Rect(
        (Config.WIDTH - Config.BUTTON_WIDTH) // 2,
        y,
        Config.BUTTON_WIDTH,
        Config.BUTTON_HEIGHT
    )

    color = Colors.HIGHLIGHT if button_rect.collidepoint(mouse_pos) else Colors.GRAY
    pygame.draw.rect(screen, color, button_rect, border_radius=5)

    text_surface = button_font.render(text, True, Colors.WHITE)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

    return button_rect


# Загрузка ресурсов
class Assets:
    backgrounds = {
        "forest": load_image("forest"),
        "mansion": load_image("mansion"),
        "village": load_image("village"),
        "moonlight_clearing": load_image("moonlight_clearing"),
    }

    characters = {
        "werewolf": load_image("werewolf"),
        "vampire": load_image("vampire"),
        "vampire_father": load_image("vampire_father"),
        "werewolf_elder": load_image("werewolf_elder"),
    }


# Состояние игры
class GameState:
    def __init__(self):
        self.current_scene = 0
        self.choices_made = []
        self.relationship_score = 0
        self.werewolf_respect = 0
        self.vampire_acceptance = 0


game_state = GameState()

# Сюжетные сцены
scenes = [
    # Сцена 0: Начало
    {
        "background": "forest",
        "character": "werewolf",
        "text": "Вы — Алиса, молодая оборотень. Сегодня полнолуние, и вы тайно встречаетесь с вампиром Лукасом...",
        "choices": [
            {"text": "Пойти на встречу", "next_scene": 1, "effect": lambda: None},
            {"text": "Остаться дома", "next_scene": 2,
             "effect": lambda: setattr(game_state, 'werewolf_respect', game_state.werewolf_respect + 1)},
        ]
    },

    # Сцена 1: Встреча с Лукасом
    {
        "background": "moonlight_clearing",
        "character": "vampire",
        "text": "Лукас ждёт вас на поляне. Он выглядит встревоженным: 'Моя семья узнала о наших встречах...'",
        "choices": [
            {"text": "Признаться в чувствах", "next_scene": 3,
             "effect": lambda: setattr(game_state, 'relationship_score', game_state.relationship_score + 2)},
            {"text": "Предложить расстаться", "next_scene": 4,
             "effect": lambda: setattr(game_state, 'relationship_score', game_state.relationship_score - 1)},
            {"text": "Спросить о подробностях", "next_scene": 5, "effect": lambda: None},
        ]
    },

    # Сцена 2: Остаться дома
    {
        "background": "village",
        "character": "werewolf",
        "text": "Вы решили остаться дома. Старейшина вашей стаи хочет поговорить с вами...",
        "choices": [
            {"text": "Выслушать старейшину", "next_scene": 6,
             "effect": lambda: setattr(game_state, 'werewolf_respect', game_state.werewolf_respect + 2)},
            {"text": "Уйти и подумать", "next_scene": 7,  # Исправлено next_scene (было next_scene)
             "effect": lambda: setattr(game_state, 'werewolf_respect', game_state.werewolf_respect - 1)},
        ]
    },

    # Сцена 3: Признание в чувствах
    {
        "background": "moonlight_clearing",
        "character": "vampire",
        "text": "Вы признаётесь Лукасу в своих чувствах. Он улыбается: 'Я тоже люблю тебя, но...'",
        "choices": [
            {"text": "Предложить сбежать вместе", "next_scene": 8,
             "effect": lambda: setattr(game_state, 'relationship_score', game_state.relationship_score + 3)},
            {"text": "Попросить поговорить с семьёй", "next_scene": 9,
             "effect": lambda: setattr(game_state, 'relationship_score', game_state.relationship_score + 1)},
        ]
    },

    # Сцена 4: Разговор с отцом Лукаса
    {
        "background": "mansion",
        "character": "vampire_father",
        "text": "Отец Лукаса холодно смотрит на вас: 'Вы знаете, что такие отношения невозможны!'",
        "choices": [
            {"text": "Уйти, не споря", "next_scene": 10,
             "effect": lambda: setattr(game_state, 'vampire_acceptance', game_state.vampire_acceptance + 1)},
            {"text": "Отстаивать свою любовь", "next_scene": 11,
             "effect": lambda: [setattr(game_state, 'relationship_score', game_state.relationship_score + 2),
                                setattr(game_state, 'vampire_acceptance', game_state.vampire_acceptance - 1)]},
        ]
    },

    # Сцена 5: Подробности о семье Лукаса
    {
        "background": "moonlight_clearing",
        "character": "vampire",
        "text": "Лукас вздыхает: 'Отец говорит, что оборотни - дикари, а мать боится, что ты меня предашь...'",
        "choices": [
            {"text": "Обидеться и уйти", "next_scene": 12,
             "effect": lambda: setattr(game_state, 'relationship_score', game_state.relationship_score - 2)},
            {"text": "Пообещать доказать свою верность", "next_scene": 13,
             "effect": lambda: setattr(game_state, 'relationship_score', game_state.relationship_score + 1)},
            {"text": "Предложить встретиться с его семьёй", "next_scene": 14, "effect": lambda: None},
        ]
    },

    # Сцена 6: Разговор со старейшиной
    {
        "background": "village",
        "character": "werewolf_elder",
        "text": "Старейшина говорит: 'Я знаю о твоих встречах. Наша стая никогда не примет вампира. Выбирай - он или мы.'",
        "choices": [
            {"text": "Пообещать порвать с Лукасом", "next_scene": 15,
             "effect": lambda: setattr(game_state, 'werewolf_respect', game_state.werewolf_respect + 3)},
            {"text": "Отказаться выбирать", "next_scene": 16,
             "effect": lambda: setattr(game_state, 'werewolf_respect', game_state.werewolf_respect - 2)},
            {"text": "Признать свою любовь", "next_scene": 17,
             "effect": lambda: [setattr(game_state, 'werewolf_respect', game_state.werewolf_respect - 3),
                                setattr(game_state, 'relationship_score', game_state.relationship_score + 2)]},
        ]
    },

    # Сцена 7: Размышления
    {
        "background": "village",
        "character": "werewolf",
        "text": "Вы бродите по деревне, размышляя о своих чувствах. Луна зовёт вас, но вы боитесь последствий...",
        "choices": [
            {"text": "Всё же пойти на встречу", "next_scene": 1, "effect": lambda: None},
            {"text": "Остаться и попытаться забыть Лукаса", "next_scene": 18,
             "effect": lambda: setattr(game_state, 'relationship_score', game_state.relationship_score - 3)},
        ]
    },

    # Сцена 8: Побег
    {
        "background": "forest",
        "character": "vampire",
        "text": "Вы с Лукасом решаете бежать. 'Куда?' - спрашивает он. 'Подальше от всех, где нас не найдут.'",
        "choices": [
            {"text": "На север, в горы", "next_scene": "escape_end", "effect": lambda: None},
            {"text": "В большой город", "next_scene": "escape_end", "effect": lambda: None},
            {"text": "За границу", "next_scene": "escape_end", "effect": lambda: None},
        ]
    },

    # Сцена 9: Встреча с семьёй
    {
        "background": "mansion",
        "character": "vampire_father",
        "text": "Вы приходите в дом Лукаса. Его семья встречает вас холодно. 'Что ты хочешь, оборотень?'",
        "choices": [
            {"text": "Показать свою человеческую сторону", "next_scene": 22,
             "effect": lambda: setattr(game_state, 'vampire_acceptance', game_state.vampire_acceptance + 1)},
            {"text": "Гордо заявить о своей природе", "next_scene": 23,
             "effect": lambda: setattr(game_state, 'vampire_acceptance', game_state.vampire_acceptance - 2)},
            {"text": "Рассказать о своих чувствах", "next_scene": 24, "effect": lambda: None},
        ]
    },

    # Сцена 10: Уход
    {
        "background": "forest",
        "character": "werewolf",
        "text": "Вы уходите, подавленная. Лукас не пытается вас остановить. Может, он согласен с отцом?",
        "choices": [
            {"text": "Вернуться в деревню", "next_scene": 25, "effect": lambda: None},
            {"text": "Попытаться связаться с Лукасом", "next_scene": 26,
             "effect": lambda: setattr(game_state, 'relationship_score', game_state.relationship_score + 1)},
        ]
    },

    # Сцена 11: Конфликт с отцом
    {
        "background": "mansion",
        "character": "vampire_father",
        "text": "Вы горячо спорите с отцом Лукаса. Вдруг Лукас встаёт между вами: 'Хватит! Я сам решу свою судьбу!'",
        "choices": [
            {"text": "Поддержать Лукаса", "next_scene": 27,
             "effect": lambda: setattr(game_state, 'relationship_score', game_state.relationship_score + 3)},
            {"text": "Уйти, чтобы не усугублять конфликт", "next_scene": 28,
             "effect": lambda: setattr(game_state, 'vampire_acceptance', game_state.vampire_acceptance + 1)},
        ]
    },

    # ... (другие сцены)

    # Концовки
    {
        "id": "happy_end",
        "background": "moonlight_clearing",
        "character": "vampire",
        "text": "После долгих испытаний ваши семьи наконец принимают ваш союз. Вы и Лукас счастливы вместе, доказав, что любовь сильнее предрассудков.",
        "end": True,
        "conditions": lambda: game_state.relationship_score >= 8 and game_state.werewolf_respect >= 3 and game_state.vampire_acceptance >= 3
    },

    {
        "id": "escape_end",
        "background": "forest",
        "character": "vampire",
        "text": "Вы с Лукасом покидаете родные места, начинаете новую жизнь вдали от предрассудков. Хотя семьи не одобрили ваш выбор, вы счастливы быть вместе.",
        "end": True,
        "conditions": lambda: game_state.relationship_score >= 6
    },

    {
        "id": "sacrifice_end",
        "background": "village",
        "character": "werewolf",
        "text": "Ради мира в стае вы расстаётесь с Лукасом. Сердце разбито, но вы знаете, что поступили правильно. Годы спустя вы слышите, что Лукас так и не нашёл себе пару...",
        "end": True,
        "conditions": lambda: game_state.relationship_score <= 3 and game_state.werewolf_respect >= 5
    },

    {
        "id": "tragic_end",
        "background": "mansion",
        "character": "vampire_father",
        "text": "Конфликт между вашими семьями перерастает в насилие. Лукас, пытаясь защитить вас, погибает. Вы остаётся одна, проклиная предрассудки, которые привели к этой трагедии.",
        "end": True,
        "conditions": lambda: game_state.relationship_score >= 5 and (
                game_state.werewolf_respect <= -3 or game_state.vampire_acceptance <= -3)
    },

    {
        "id": "betrayal_end",
        "background": "moonlight_clearing",
        "character": "werewolf",
        "text": "Лукас неожиданно исчезает. Позже вы узнаёте, что он уехал по настоянию семьи. Боль предательства будет долго напоминать о себе в каждое полнолуние...",
        "end": True,
        "conditions": lambda: game_state.relationship_score <= 0 and game_state.vampire_acceptance <= -2
    },

    {
        "id": "neutral_end",
        "background": "village",
        "character": "werewolf",
        "text": "Время проходит, но ничего не меняется. Вы продолжаете тайно встречаться с Лукасом, но ваши отношения остаются в подвешенном состоянии, без будущего, но и без разрыва.",
        "end": True,
        "conditions": lambda: True
    }
]

# Словарь для быстрого доступа к сценам по ID
scenes_by_id = {scene["id"]: idx for idx, scene in enumerate(scenes) if "id" in scene}


def get_scene_index(scene_reference):
    """Получает индекс сцены по номеру или ID"""
    if isinstance(scene_reference, int):
        return scene_reference
    elif isinstance(scene_reference, str):
        return scenes_by_id.get(scene_reference, 0)
    return 0


def check_endings():
    """Проверяет, выполнены ли условия какой-либо концовки, кроме нейтральной"""
    # Не проверяем концовки, если мы уже в одной из них
    current_scene = scenes[game_state.current_scene]
    if current_scene.get("end"):
        return None

    # Проверяем все концовки, кроме нейтральной
    for scene in scenes:
        if scene.get("id") != "neutral_end" and scene.get("end") and scene["conditions"]():
            return scene
    return None


def main():
    # Начинаем игру с первой сцены
    game_state.current_scene = 0

    while True:
        mouse_pos = pygame.mouse.get_pos()

        # Получаем текущую сцену
        current_scene = scenes[game_state.current_scene]

        # Проверяем концовки только если мы не в одной из них
        if not current_scene.get("end"):
            ending_scene = check_endings()
            if ending_scene:
                game_state.current_scene = scenes.index(ending_scene)
                current_scene = ending_scene
        else:
            # Если мы в концовке, проверяем только нейтральную
            if current_scene.get("id") == "neutral_end" and not current_scene["conditions"]():
                # Если вдруг попали в нейтральную концовку без условий,
                # возвращаемся к последней сцене
                if game_state.choices_made:
                    game_state.current_scene = min(len(scenes) - 2, max(0, game_state.current_scene - 1))
                else:
                    game_state.current_scene = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if current_scene.get("end"):
                    pygame.quit()
                    sys.exit()

                for i, choice in enumerate(current_scene["choices"]):
                    button_rect = pygame.Rect(
                        (Config.WIDTH - Config.BUTTON_WIDTH) // 2,
                        Config.BUTTON_START_Y + i * Config.BUTTON_SPACING,
                        Config.BUTTON_WIDTH,
                        Config.BUTTON_HEIGHT
                    )
                    if button_rect.collidepoint(mouse_pos):
                        # Преобразуем next_scene в индекс
                        if isinstance(choice["next_scene"], str):
                            next_scene = scenes_by_id.get(choice["next_scene"], 0)
                        else:
                            next_scene = choice["next_scene"]

                        # Проверяем, что индекс в пределах
                        if 0 <= next_scene < len(scenes):
                            game_state.current_scene = next_scene
                        else:
                            # Если индекс вне диапазона, переходим к нейтральной концовке
                            game_state.current_scene = scenes_by_id["neutral_end"]

                        if choice["effect"]:
                            choice["effect"]()
                        game_state.choices_made.append(choice["text"])

        # Отрисовка игры
        screen.fill(Colors.BLACK)

        # Отрисовка фона
        if current_scene["background"] in Assets.backgrounds:
            screen.blit(Assets.backgrounds[current_scene["background"]], (0, 0))

        # Отрисовка персонажа
        if current_scene["character"] in Assets.characters:
            screen.blit(Assets.characters[current_scene["character"]], Config.CHARACTER_POS)

        # Отрисовка текста
        text_surface = render_text_box(current_scene["text"])
        screen.blit(text_surface, Config.TEXT_POS)

        # Отрисовка кнопок
        if not current_scene.get("end"):
            for i, choice in enumerate(current_scene["choices"]):
                draw_button(choice["text"], i, mouse_pos)
        else:
            draw_button("Завершить игру", 0, mouse_pos)

        # Отладочная информация
        debug_info = f"Отношения: {game_state.relationship_score} | Уважение: {game_state.werewolf_respect} | Принятие: {game_state.vampire_acceptance}"
        debug_surface = button_font.render(debug_info, True, Colors.WHITE)
        screen.blit(debug_surface, (10, Config.HEIGHT - 30))

        pygame.display.flip()
        clock.tick(Config.FPS)


if __name__ == "__main__":
    main()