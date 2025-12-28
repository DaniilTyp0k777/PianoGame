import pygame
import os
import subprocess
from buttons import Button
from ui.slider import Slider


class SettingsMenu:
    def __init__(self, screen_rect, initial_volume, initial_keys, min_keys, max_keys, on_change, on_back):
        self.screen_rect = screen_rect
        self.on_change = on_change
        self.on_back = on_back

        cx = screen_rect.centerx
        top = 140

        back_idle = pygame.transform.scale(
            pygame.image.load('assets/images/buttons/exit_unhover.png'), (48, 48)
        )
        back_hover = pygame.transform.scale(
            pygame.image.load('assets/images/buttons/exit_hover.png'), (48, 48)
        )

        self.back_btn = Button(
            40, 30, 48, 48,
            "",
            self._back,
            img_idle=back_idle,
            img_hover=back_hover
        )

        def volume_to_text(v):
            return f"{int(v * 100)}%"

        self.volume_slider = Slider(
            cx - 200, top, 400,
            0.0, 1.0, step=0.01, initial=initial_volume,
            label="Гучність",
            value_to_text = volume_to_text
        )
        self.volume_slider.set_on_change(self._on_volume)

        def keys_to_text(v):
            return str(int(v))

        self.keys_slider = Slider(
            cx - 200, top + 120, 400,
            min_keys, max_keys, step=1, initial=initial_keys,
            label="Кількість клавіш",
        value_to_text = keys_to_text
        )
        self.keys_slider.set_on_change(self._on_keys)

        # Кнопка открытия папки со звуками (в самом низу)
        self.sounds_btn = Button(
            cx - 100, 550, 200, 40,
            "Завантажити звуки",
            self._open_sounds_folder
        )

    def _on_volume(self, v):
        if self.on_change:
            self.on_change(float(v), int(self.keys_slider.value))

    def _on_keys(self, v):
        if self.on_change:
            self.on_change(float(self.volume_slider.value), int(v))

    def _back(self):
        if self.on_back:
            self.on_back()

    def _open_sounds_folder(self):
        """Открывает папку со звуками"""
        sounds_path = os.path.abspath("assets/sounds")
        try:
            # Для Windows
            if os.name == 'nt':
                os.startfile(sounds_path)
            # Для macOS
            elif os.name == 'posix':
                subprocess.run(['open', sounds_path])
            # Для Linux
            else:
                subprocess.run(['xdg-open', sounds_path])
        except Exception as e:
            print(f"Не удалось открыть папку: {e}")

    def draw(self, screen, font):
        title = font.render("Налаштування", True, (0, 0, 0))
        screen.blit(title, title.get_rect(center=(self.screen_rect.centerx, 80)))

        self.back_btn.draw(screen, font)
        self.volume_slider.draw(screen, font)
        self.keys_slider.draw(screen, font)
        self.sounds_btn.draw(screen, font)
        
        # Инструкция для добавления звуков
        instruction_lines = [
            "ВАЖНО!!!!!!!!!!!",
            "КАК ДОБАВИТЬ НОВЫЕ ЗВУКИ:",
            "1. Нажми кнопку 'Завантажити звуки' ниже",
            "2. Откроется папка assets/sounds",
            "3. Скопируй туда новые MP3 файлы",
            "4. Назови файлы правильно: h1.mp3, e4.mp3, c5.mp3",
            "5. Формат: буква+цифра (например: a3, b2, c6)",
            "6. Вернись в игру - звуки загрузятся автоматически",
            "7. Добавь клавиши в settings.py если нужно"
        ]
        
        y_offset = 300
        small_font = pygame.font.SysFont("Arial", 25)
        
        for line in instruction_lines:
            if "ВАЖНО" in line:
                text_color = (255, 0, 0)  # Красный для важного
                font_size = 23
            elif "КАК ДОБАВИТЬ" in line:
                text_color = (0, 0, 139)  # Синий для заголовка
                font_size = 15
            elif line.startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.")):
                text_color = (0, 100, 0)  # Темно-зеленый для пунктов
                font_size = 13
            else:
                text_color = (0, 0, 0)  # Черный для остального
                font_size = 19
                
            current_font = pygame.font.SysFont("Arial", font_size)
            text = current_font.render(line, True, text_color)
            text_rect = text.get_rect(center=(self.screen_rect.centerx, y_offset))
            screen.blit(text, text_rect)
            y_offset += 22

    def handle_event(self, event):
        self.back_btn.handle_event(event)
        self.volume_slider.handle_event(event)
        self.keys_slider.handle_event(event)
        self.sounds_btn.handle_event(event)
