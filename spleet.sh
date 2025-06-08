#!/bin/bash

# Папки
WAV_DIR="$1"
VOCAL_DIR="$2/vocals"
ACCOMP_DIR="$2/accomp"
TEMP_DIR="spleeter_temp"

# Создаём выходные папки
mkdir -p "$VOCAL_DIR" "$ACCOMP_DIR" "$TEMP_DIR"

# Проход по всем .wav файлам
for file in "$WAV_DIR"/*.wav; do
    filename=$(basename -- "$file")
    name="${filename%.*}"
    out_dir="$TEMP_DIR/$name"

    # Используем Docker для запуска spleeter
    docker run --rm -v "$(pwd)":/audio researchdeezer/spleeter separate \
        -p spleeter:2stems -o /audio/$TEMP_DIR -i /audio/$file

    # Перемещение вокала и аккомпанемента
    if [ -f "$out_dir/vocals.wav" ]; then
        mv "$out_dir/vocals.wav" "$VOCAL_DIR/${name}.wav"
    fi
    if [ -f "$out_dir/accompaniment.wav" ]; then
        mv "$out_dir/accompaniment.wav" "$ACCOMP_DIR/${name}.wav"
    fi

    # Удаляем временную папку
    rm -rf "$out_dir"
done

# Удаляем временную директорию, если пуста
rmdir "$TEMP_DIR" 2>/dev/null
