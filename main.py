import pygame
from pygame import event, display, QUIT, KEYDOWN, KEYUP, key, transform, image, font, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from buttons import Button
from settings import *
from sounds import load_sounds
from keys import draw_keys, create_key_rects
import webbrowser

# Открываем GitHub при запуске
try:
    webbrowser.open("https://github.com/DaniilTyp0k777")
except Exception as e:
    print(f"Не удалось открыть GitHub: {e}")

display.set_caption("Piano Game")

sounds = load_sounds(KEYS)
pygame.font.init()
my_font = font.SysFont("Arial", 24)
pressed_keys = set()

screen_mode = "main"           # "main" або "settings"
settings_menu = None

current_volume = 1.0
for s in sounds.values():
    try:
        s.set_volume(current_volume)
    except Exception:
        pass


num_keys = len(KEYS)  # Все клавиши доступны
keys_list = list(KEYS.keys())[:num_keys]
key_rects = create_key_rects(num_keys)

def apply_settings(volume: float, key_count: int):
    global current_volume, num_keys, keys_list, key_rects, pressed_keys, sounds
    current_volume = float(max(0.0, min(1.0, volume)))
    for s in sounds.values():
        try:
            s.set_volume(current_volume)
        except Exception:
            pass

    key_count = max(1, min(len(KEYS), int(key_count)))
    if key_count != num_keys:
        num_keys = key_count
        keys_list = list(KEYS.keys())[:num_keys]
        key_rects = create_key_rects(num_keys)
        # прибрати "зажаті" індекси, яких більше немає
        pressed_keys = {i for i in pressed_keys if i < num_keys}
    
    # Перезагружаем звуки на случай если были добавлены новые
    try:
        new_sounds = load_sounds(KEYS)
        for s in new_sounds.values():
            try:
                s.set_volume(current_volume)
            except Exception:
                pass
        sounds = new_sounds
    except Exception as e:
        print(f"Ошибка перезагрузки звуков: {e}")

def open_settings():
    global screen_mode, settings_menu
    screen_mode = "settings"
    settings_menu = SettingsMenu(
        screen.get_rect(),
        initial_volume=current_volume,
        initial_keys=num_keys,
        min_keys=1,
        max_keys=len(KEYS),
        on_change=apply_settings,
        on_back=lambda: _back_to_main(),
    )

def _back_to_main():
    global screen_mode, settings_menu
    screen_mode = "main"
    settings_menu = None

def draw_controls_help(screen, font):
    """Рисует инструкцию по управлению внизу главного меню"""
    help_lines = [
        "УПРАВЛЕНИЕ:",
        "Клавиши: A, B, C, D, E, F, G, Q, W, S, X",
        "Мышь: Кликай по клавишам для игры",
        "Настройки: Кнопка вверху слева"
    ]
    
    y_offset = WINDOW_HEIGHT - 120  # Позиция выше от низа экрана
    small_font = pygame.font.SysFont("Arial", 20)
    
    for line in help_lines:
        if "УПРАВЛЕНИЕ:" in line:
            text_color = (0, 0, 139)  # Синий для заголовка
        else:
            text_color = (50, 50, 50)  # Темно-серый для текста
            
        text = small_font.render(line, True, text_color)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, y_offset))
        screen.blit(text, text_rect)
        y_offset += 25

# кнопки меню
def exit_game(): quit()

SETTINGS_IDLE = transform.scale(
    image.load('assets/images/buttons/settings_unhover.png'), (50, 50)
)
SETTINGS_HOVER = transform.scale(
    image.load('assets/images/buttons/settings_hover.png'), (50, 50)
)

buttons = [
    Button(
        60, 20, 50, 50,            # позиція і розмір
        "",                        # текст не потрібен
        open_settings,             # дія
        img_idle=SETTINGS_IDLE,    # іконка "звичайна"
        img_hover=SETTINGS_HOVER   # іконка при наведенні
    )
]

running = True
while running:
    screen.fill(WHITE)
    if screen_mode == "settings" and settings_menu:
        # малюємо меню налаштувань
        settings_menu.draw(screen, my_font)
    else:
        # кнопки
        for button in buttons:
            button.draw(screen, my_font)
        # клавіші
        draw_keys(screen, key_rects, pressed_keys)
        
        # Инструкция по управлению
        draw_controls_help(screen, my_font)


    display.flip()

    for e in event.get():
        if e.type == QUIT:
            running = False

        # якщо ми в налаштуваннях — передаємо всі події туди й пропускаємо інше
        if screen_mode == "settings" and settings_menu:
            settings_menu.handle_event(e)
            continue

        # кнопки (Settings)
        for button in buttons:
            button.handle_event(e)

        # клавіатура (увага: індекс шукаємо лише серед активних keys_list)
        if e.type == KEYDOWN:
            k = key.name(e.key)
            if k in sounds and k in keys_list:
                sounds[k].play()
                idx = keys_list.index(k)
                pressed_keys.add(idx)

        if e.type == KEYUP:
            k = key.name(e.key)
            if k in sounds and k in keys_list:
                idx = keys_list.index(k)
                if idx in pressed_keys:
                    pressed_keys.remove(idx)

        # миша по клавішах
        if e.type == MOUSEBUTTONDOWN:
            pos = e.pos
            for i, rect in enumerate(key_rects):
                if rect.collidepoint(pos):
                    sounds[keys_list[i]].play()
                    pressed_keys.add(i)

        if e.type == MOUSEBUTTONUP:
            pos = e.pos
            for i, rect in enumerate(key_rects):
                if i in pressed_keys and rect.collidepoint(pos):
                    pressed_keys.remove(i)
