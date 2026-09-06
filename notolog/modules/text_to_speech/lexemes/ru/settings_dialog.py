# Russian lexemes settings_dialog.py
lexemes = {
    "module_text_to_speech_config_enabled_label": "Включить озвучивание текста",
    "module_text_to_speech_config_setup_label": "Настройка голоса",
    "module_text_to_speech_config_runtime_label": "Речевой движок",
    "module_text_to_speech_config_model_directory_label": "Папка моделей",
    "module_text_to_speech_config_tokenizer_directory_label": "Токенизаторы",
    "module_text_to_speech_config_details_label": "Подробности",
    "module_text_to_speech_config_model_license_label": "Лицензия модели",
    "module_text_to_speech_config_download_models_button": "Скачать модели",
    "module_text_to_speech_config_verify_models_button": "Проверить модели",
    "module_text_to_speech_config_cancel_button": "Отмена",
    "module_text_to_speech_config_stop_button": "Стоп",
    "module_text_to_speech_config_custom_models_label": "Свои файлы моделей",
    "module_text_to_speech_config_reading_label": "Чтение",
    "module_text_to_speech_config_language_label": "Язык",
    "module_text_to_speech_config_voice_label": "Голос",
    "module_text_to_speech_config_speed_label": "Скорость",
    "module_text_to_speech_config_announce_headings_label": "Объявлять заголовки",
    "module_text_to_speech_config_skip_inline_code_label": "Пропускать встроенный код",
    "module_text_to_speech_config_skip_multiline_code_label": "Пропускать многострочный код",
    "module_text_to_speech_config_test_voice_button": "Проверить голос",
    "module_text_to_speech_config_runtime_input_placeholder_text": "Выберите исполняемый файл…",
    "module_text_to_speech_config_model_input_placeholder_text": "Автоматически",
    "module_text_to_speech_config_get_runtime_link": "Скачать движок {version}",
    "module_text_to_speech_config_about_label": "О разделе «{title}»",
    "module_text_to_speech_config_choose_path_label": "Выбрать: {title}",
    "module_text_to_speech_config_status_checking_runtime": "Проверка речевого движка…",
    "module_text_to_speech_config_status_checking_models": "Проверка кэша и загрузка недостающих моделей…",
    "module_text_to_speech_config_status_models_verified": "Существующие модели проверены. Готово к чтению.",
    "module_text_to_speech_config_status_models_downloaded": "Модели скачаны и проверены. Готово к чтению.",
    "module_text_to_speech_config_status_models_found": "Файлы моделей найдены. Проверьте их или голос.",
    "module_text_to_speech_config_status_models_missing": "Нужны модели. Скачайте голос для начала чтения.",
    "module_text_to_speech_config_status_runtime_missing": (
        "Нужен движок. Выберите исполняемый файл или скачайте движок."
    ),
    "module_text_to_speech_config_status_download_cancelled": (
        "Отменено. Завершённые загрузки сохранены; повторите попытку."
    ),
    "module_text_to_speech_config_error_permission_denied": (
        "Доступ запрещён. Выберите папку с правом записи и проверьте доступ к файлам."
    ),
    "module_text_to_speech_config_error_file_access": "Не удалось открыть файл: {error}. См. подробности.",
    "module_text_to_speech_config_progress_elapsed": "Прошло {time}",
    "module_text_to_speech_config_progress_files_complete": "Готово файлов: {count}/3",
    "module_text_to_speech_config_progress_downloading": "Файл {number}/3 · Загрузка: {role} · {size} МиБ…",
    "module_text_to_speech_config_progress_cached": "Проверено файлов моделей в кэше: {count}/3…",
    "module_text_to_speech_config_progress_verifying": "Файл {number}/3 · Проверка загрузки…",
    "module_text_to_speech_config_download_role_voice": "речевая модель",
    "module_text_to_speech_config_download_role_codec": "аудиодекодер",
    "module_text_to_speech_config_download_role_tokenizers": "токенизаторы",
    "module_text_to_speech_config_download_role_model": "модель",
    "module_text_to_speech_config_runtime_required": "Сначала выберите речевой движок.",
    "module_text_to_speech_config_models_required": "Сначала скачайте модели.",
    "module_text_to_speech_config_enable_required": "Сначала включите озвучивание текста.",
    "module_text_to_speech_config_status_testing_voice": "Загрузка моделей и подготовка проверки голоса…",
    "module_text_to_speech_config_details_accessible_description": "Показать или скрыть журнал операции",
    "module_text_to_speech_config_setup_accessible_description": (
        "Выберите NeMo-Speech.cpp и скачайте MagpieTTS, NanoCodec и токенизаторы. У моделей отдельная "
        "лицензия."
    ),
    "module_text_to_speech_config_runtime_input_accessible_description": (
        "Требуется NeMo-Speech.cpp 0.1.0. Распакуйте архив и выберите bin/nemo-speech "
        "(bin/nemo-speech.exe в Windows)."
    ),
    "module_text_to_speech_config_model_directory_input_accessible_description": (
        "Модели скачиваются сюда. Существующие файлы проверяются и используются повторно. Нужны curl и "
        "около 550 МБ."
    ),
    "module_text_to_speech_config_custom_models_accessible_description": (
        "Укажите свои пути к моделям или очистите поля, чтобы использовать папку моделей."
    ),
    "module_text_to_speech_config_reading_accessible_description": (
        "Выберите голос, язык и скорость. Код можно заменить краткой голосовой меткой."
    ),
    "module_text_to_speech_config_language_input_accessible_description": (
        "Выберите язык документа; автоматического определения нет. По умолчанию английский. Для "
        "китайского и японского нужен движок с их поддержкой."
    ),
    "module_text_to_speech_config_voice_input_accessible_description": (
        "Голоса MagpieTTS: John, Sofia, Aria, Jason и Leo."
    ),
    "module_text_to_speech_config_speed_input_accessible_description": (
        "Скорость воспроизведения также меняет высоту голоса."
    ),
    "module_text_to_speech_config_announce_headings_accessible_description": (
        "Для заголовков Markdown и HTML уровней 1–4 произносятся Chapter, Section, Subsection и "
        "Sub-subsection, затем Heading level 5–6."
    ),
    "module_text_to_speech_config_skip_inline_code_accessible_description": (
        "Включено: произносится «Inline code block». Выключено: читается встроенный код. Для ограждённых"
        " блоков и блоков с отступом используется настройка многострочного кода."
    ),
    "module_text_to_speech_config_skip_multiline_code_accessible_description": (
        "Включено: произносится «Multiline code block». Выключено: читается код в ограждённых блоках и "
        "блоках с отступом."
    ),
    "module_text_to_speech_config_verify_models_accessible_description": (
        "Проверить существующие файлы и скачать недостающие или повреждённые."
    ),
    "module_text_to_speech_config_editor_required": "Откройте эти настройки из редактора, чтобы проверить голос.",
    "module_text_to_speech_config_context_length_label": "Длина контекста",
    "module_text_to_speech_config_context_whole_document": "Весь документ",
    "module_text_to_speech_config_context_characters": "{count} символов",
    "module_text_to_speech_config_context_length_accessible_description": (
        "Максимум символов в речевом запросе. Крайнее правое положение: весь документ с паузами перед "
        "заголовками. Большой контекст требует больше времени до начала чтения и памяти. Ограничения "
        "движка сохраняются."
    ),
    "module_text_to_speech_config_cancel_download_title": "Отменить загрузку?",
    "module_text_to_speech_config_cancel_download_confirmation": (
        "Закрытие настроек отменит загрузку. Загруженные файлы сохранятся. Закрыть настройки?"
    ),
    "module_text_to_speech_config_status_custom_models": (
        "Выбраны пользовательские файлы моделей. Загрузка выполняется в папку моделей."
    ),
}
