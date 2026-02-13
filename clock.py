import os
os.environ["SDL_AUDIODRIVER"] = "dummy"
import pygame
import math
import time
import sys
import urllib.request
import json
import subprocess

def get_temperature_celsius(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.load(response)
            return data['current_weather']['temperature']
    except Exception as e:
        print("Weather fetch failed:", e)
        return None
    

last_fetch = 0
cached_temp = None

def get_cached_temp():
    global last_fetch, cached_temp
    if time.time() - last_fetch > 600:  # 10 minutes
        cached_temp = get_temperature_celsius(32.0853, 34.7818)
        last_fetch = time.time()
    return cached_temp

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("B/W Analog Clock")
pygame.mouse.set_visible(False)

w, h = screen.get_size()
center = (w // 2, h // 2)
radius = int(min(w, h) * 0.4)

clock = pygame.time.Clock()

# Font for date
font_size = int(radius * 0.18)
font = pygame.font.Font('Vipnagorgialla Rg.otf', font_size)


def draw_glow_line(surface, start, end, main_width):
    for offset in [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (1,1)]:
        pygame.draw.line(
            surface,
            (120, 120, 120),
            (start[0] + offset[0], start[1] + offset[1]),
            (end[0] + offset[0], end[1] + offset[1]),
            main_width + 2
        )
    pygame.draw.line(surface, (255, 255, 255), start, end, main_width)


def draw_glow_circle(surface, center, radius, width):
    for r in range(radius - 1, radius + 2):
        pygame.draw.circle(surface, (120, 120, 120), center, r, width + 2)
    pygame.draw.circle(surface, (255, 255, 255), center, radius, width)


def draw_hour_ticks(surface):
    for hour in range(12):
        angle = -math.pi / 2 + hour * math.pi / 6

        outer = (
            center[0] + int(radius * math.cos(angle)),
            center[1] + int(radius * math.sin(angle))
        )
        inner = (
            center[0] + int(radius * 0.88 * math.cos(angle)),
            center[1] + int(radius * 0.88 * math.sin(angle))
        )

        pygame.draw.line(surface, (255, 255, 255), inner, outer, 4)

music_process = None
music_started_this_minute = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))
    t = time.localtime()

    # Clock face
    draw_glow_circle(screen, center, radius, 4)

    # Hour ticks
    draw_hour_ticks(screen)



    brand_image = pygame.image.load("croptal-logo-invert.png").convert_alpha()
    # Scale brand logo
    brand_max_height = int(radius * 0.5)  # adjust if needed
    scale_factor = brand_max_height / brand_image.get_height()
    brand_width = int(brand_image.get_width() * scale_factor)
    brand_height = int(brand_image.get_height() * scale_factor)

    brand_image_scaled = pygame.transform.smoothscale(brand_image, (brand_width, brand_height))
    brand_x = center[0] - brand_width // 2
    brand_y = center[1] - int(radius * 0.45) - brand_height // 2  # slightly above center
    brand_image_scaled.set_alpha(204)

    screen.blit(brand_image_scaled, (brand_x, brand_y))

    # Temperature display
    temp = get_cached_temp()
    if temp is not None:
        temp_text = f"{int(temp)}°"  # round for simplicity
        temp_font_size = int(radius * 0.18)
        temp_font = pygame.font.Font('Vipnagorgialla Rg.otf', temp_font_size)

        temp_surf = temp_font.render(temp_text, True, (255, 255, 255))
        temp_rect = temp_surf.get_rect()

        # Position: left of center towards 9 o'clock
        temp_x = center[0] - int(radius * 0.45)
        temp_y = center[1]
        temp_rect.center = (temp_x, temp_y)

        screen.blit(temp_surf, temp_rect)


    # Day of month (between center and 3 o'clock)
    day_text = str(t.tm_mday)

    text_surf = font.render(day_text, True, (255, 255, 255))  # white text
    text_rect = text_surf.get_rect()

    date_x = center[0] + int(radius * 0.45)
    date_y = center[1]
    text_rect.center = (date_x, date_y)

    # Background rectangle (outline only)
    padding_x = int(font_size * 0.4)
    padding_y = int(font_size * 0.25)

    bg_rect = text_rect.inflate(padding_x * 2, padding_y * 2)

    pygame.draw.rect(
        screen,
        (100, 100, 100),   # white outline
        bg_rect,
        width=2,           # outline thickness
        border_radius=6
    )

    screen.blit(text_surf, text_rect)

    # Hour hand
    hour_angle = -math.pi / 2 + (t.tm_hour % 12 + t.tm_min / 60) * math.pi / 6
    hour_end = (
        center[0] + int(radius * 0.5 * math.cos(hour_angle)),
        center[1] + int(radius * 0.5 * math.sin(hour_angle))
    )
    draw_glow_line(screen, center, hour_end, 6)

    # Minute hand
    min_angle = -math.pi / 2 + t.tm_min * math.pi / 30
    min_end = (
        center[0] + int(radius * 0.75 * math.cos(min_angle)),
        center[1] + int(radius * 0.75 * math.sin(min_angle))
    )
    draw_glow_line(screen, center, min_end, 4)

    # Seconds hand (long, thin, precise)
    sec_angle = -math.pi / 2 + t.tm_sec * math.pi / 30
    sec_end = (
        center[0] + int(radius * 0.95 * math.cos(sec_angle)),
        center[1] + int(radius * 0.95 * math.sin(sec_angle))
    )
    pygame.draw.line(screen, (255, 255, 255), center, sec_end, 1)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    t = time.localtime()
    current_sec = t.tm_sec

    # Start music exactly on first second tick

    if current_sec == 2 and not music_started_this_minute:
        if music_process and music_process.poll() is None:
            music_process.terminate()  # politely terminate
            music_process.wait()       # wait until fully stopped
        subprocess.Popen([
            "aplay",
            "-D", "default",
            "--buffer-size=96000",
            "--period-size=24000",
            "clock.wav"
        ])
        music_started_this_minute = True

    # # Reset flag at the start of a new minute
    if current_sec == 0:
        music_started_this_minute = False

    pygame.display.flip()
    clock.tick(1)
