# Manim presentation kit

Повторяемый стиль технических презентаций: тёмный фон, Inter / JetBrains Mono,
простая геометрия, единые цвета и переходы с сохранением объектов.
За основу взят [rw404/readingclub](https://github.com/rw404/readingclub), разбор DHE.

## Что сохранено

- `deckkit/tokens.py` — исходная палитра, размеры шрифтов, сетка 45 px, поля 135 px.
- `deckkit/components.py` — исходные компоненты, типографика и анимационные акценты.
- `deckkit/base.py` — непрерывные сцены, границы слайдов, тайминг и заметки.
- `manim.cfg` — 1920×1080, 60 fps, тёмный фон.
- `requirements.txt` и `requirements.lock.txt` — версии окружения.
- `scripts/setup.py` — шрифты и локальная настройка Fontconfig.
- `scripts/render.py` — черновая или финальная сборка.
- `examples/reactive-feed/scene.py` — исправленный пример: пять сцен, около минуты, без озвучки.
- `examples/reactive-feed/build/frames.json` — названия сцен и длительности.

Исходные файлы UCP, учётные данные, окружение и рендеры не включены.
Схема примера иллюстрирует механизмы, а не текущее включение всех веток в продакшене.
Высоты столбиков и доли потоков условны.

## Установка

Python 3.12. Системные зависимости на macOS:

```sh
brew install cairo pango pkg-config fontconfig ffmpeg
python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/setup.py
```

На Debian/Ubuntu вместо Homebrew: `sudo apt-get install libcairo2-dev libpango1.0-dev pkg-config fontconfig ffmpeg python3-dev`.
LaTeX для этого примера не нужен. Шрифты хранятся в `assets/`, системная установка не требуется.
`requirements.lock.txt` фиксирует использовавшееся окружение macOS; для другой ОС используйте `requirements.txt`.

## Сборка

```sh
.venv/bin/python scripts/render.py --draft
.venv/bin/python scripts/render.py
```

Финальный ролик: `media/videos/scene/1080p60/ReactiveFeed.mp4`.
Состояния пяти сцен: `examples/reactive-feed/build/slide-1.png` … `slide-5.png`.
Метаданные manim-slides: `slides/ReactiveFeed.json`.

## Правила оформления и проверки

Сохранять значения из `tokens.py`: Inter 40 для заголовка, JetBrains Mono 28 для подписей,
64 для крупного акцента; линии 2/4/8 px. Цвета имеют постоянный смысл.
Движение объясняет изменение: выбранный объект продолжается в следующей сцене.

Сначала проверить черновик и промежуточные состояния каждого перехода, затем Full HD.
Особенно проверять рамки, пересечения, путь движущихся объектов и текст во время превращений.
В исправленном вступлении у поста A отдельная ячейка; сетка исчезает перед перемещением,
а соединительная линия появляется после его завершения.

При новой теме скопировать пример, поменять сценарий и `frames.json`, сохранив визуальные токены.
Видео, кэш, шрифты и пути текущего компьютера не коммитить.

## Происхождение

См. `UPSTREAM.md`. Не приписывать себе авторство исходного `deckkit`.
