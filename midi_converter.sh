#!/bin/bash

# Папка с входными .wav файлами (например, от spleeter'а)
INPUT_DIR="$1"
# Папка для сохранения midi-файлов
OUTPUT_DIR="$2"

# Убедимся, что папка для midi существует
mkdir -p "$OUTPUT_DIR"

# Обход всех wav-файлов в INPUT_DIR
for wav_file in "$INPUT_DIR"/*.wav; do
    [ -e "$wav_file" ] || continue  # Пропустить, если нет файлов

    filename=$(basename -- "$wav_file")
    name="${filename%.*}"

    echo "Обрабатывается: $filename"

    # Вызов basic-pitch из Docker
    docker run --rm -v "$(pwd)":/app basic-pitch \
        --save-midi \
        "/app/$OUTPUT_DIR" \
        "/app/$wav_file"
done
