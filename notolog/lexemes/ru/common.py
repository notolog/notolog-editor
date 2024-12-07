# Russian lexemes common.py
lexemes = {
    "app_title": "Редактор Notolog",
    "app_title_with_sub": "{app_title} - {sub_title}",

    "tree_filter_accessible_desc": "Поле фильтра файлов",

    "menu_action_copy_file_path": "Копировать путь файла",
    "menu_action_rename": "Переименовать",
    "menu_action_delete": "Удалить",
    "menu_action_delete_completely": "Удалить полностью",
    "menu_action_restore": "Восстановить",
    "menu_action_create_new_dir": "Создать новую директорию",

    "dialog_file_rename_title": "Переименовать файл",
    "dialog_file_rename_field_label": "Введите новое имя файла",
    "dialog_file_rename_button_ok": "Переименовать",
    "dialog_file_rename_warning_exists": "Файл с таким именем уже существует",

    "dialog_file_delete_title": "Удалить файл",
    "dialog_file_delete_text": "Удалить файл \"{file_name}\"?",
    "dialog_file_delete_completely_title": "Окончательно удалить файл",
    "dialog_file_delete_completely_text": "Окончательно удалить файл \"{file_name}\"?",
    "dialog_file_delete_error": "Невозможно удалить файл, произошла ошибка",
    "dialog_file_delete_error_not_found": "Файл не найден",

    "dialog_file_restore_title": "Восстановление файла",
    "dialog_file_restore_text": "Восстановить файл \"{file_name}\"?",
    "dialog_file_restore_error": "Не удалось восстановить файл, произошла ошибка",
    "dialog_file_restore_warning_exists": "Файл с именем {file_name} уже существует",

    "dialog_create_new_dir_title": "Создать новую директорию",
    "dialog_create_new_dir_label": "Имя новой директории",
    "dialog_create_new_dir_input_placeholder_text": "Введите имя директории",
    "dialog_create_new_dir_button_ok": "Создать",
    "dialog_create_new_dir_button_cancel": "Отмена",
    "dialog_create_new_dir_warning_empty_title": "Ошибка имени новой директории",
    "dialog_create_new_dir_warning_empty_text": "Имя директории не может быть пустым",
    "dialog_create_new_dir_warning_too_long_title": "Ошибка имени новой директории",
    "dialog_create_new_dir_warning_too_long_text": "Имя директории слишком длинное; максимально допустимое количество "
                                                   "символов: {symbols}!",
    "dialog_create_new_dir_error_existed": "Директория уже существует",
    "dialog_create_new_dir_error": "Не удается создать директорию. Убедитесь, что директория назначения "
                                   "{base_dir} доступна для записи",

    "dialog_message_box_title": "Сообщение",
    "dialog_message_box_button_ok": "Закрыть",

    "action_new_file_first_line_template_text": "Новый документ",
    "action_open_file_dialog_caption": "Открыть файл",
    "action_save_as_file_dialog_caption": "Сохранить файл",

    "dialog_save_empty_file_title": "Сохранить пустой файл",
    "dialog_save_empty_file_text": "Разрешить сохранение файла без содержимого?",

    "dialog_encrypt_file_title": "Зашифровать файл",
    "dialog_encrypt_file_text": "Зашифровать файл \"{file_name}\"?",
    "encrypt_file_warning_file_is_already_encrypted": "Файл уже зашифрован!",
    "dialog_encrypt_file_rewrite_existing_title": "Перезаписать существующий файл",
    "dialog_encrypt_file_rewrite_existing_text": "Перезаписать существующий файл \"{file_path}\"?",

    "dialog_decrypt_file_title": "Расшифровать файл",
    "dialog_decrypt_file_text": "Расшифровать файл \"{file_name}\"?",
    "decrypt_file_warning_file_is_not_encrypted": "Файл не зашифрован!",
    "dialog_decrypt_file_rewrite_existing_title": "Перезаписать существующий файл",
    "dialog_decrypt_file_rewrite_existing_text": "Перезаписать существующий файл \"{file_path}\"?",

    "dialog_encrypt_new_password_title": "Новый пароль",
    "dialog_encrypt_new_password_label": "Пароль:",
    "dialog_encrypt_new_password_input_placeholder_text": "Введите новый пароль",
    "dialog_encrypt_new_password_hint_label": "Подсказка:",
    "dialog_encrypt_new_password_hint_label_description":
        "Подсказка не зашифрована и может быть прочитана из файла!"
        "\nНе используйте очевидные подсказки, которые можно легко угадать,"
        "\nнапример, дату рождения и т.д. Попробуйте использовать отсылку.",
    "dialog_encrypt_new_password_hint_input_placeholder_text": "Введите подсказку (необязательно)",
    "dialog_encrypt_new_password_button_ok": "ОК",
    "dialog_encrypt_new_password_button_cancel": "Отмена",
    "dialog_encrypt_new_password_warning_empty_title": "Предупреждение",
    "dialog_encrypt_new_password_warning_empty_text": "Поле пароля не может быть пустым!",
    "dialog_encrypt_new_password_warning_too_long_title": "Предупреждение",
    "dialog_encrypt_new_password_warning_too_long_text": "Поле подсказки слишком длинное, максимум {symbols} символов!",

    "dialog_encrypt_password_title": "Введите пароль",
    "dialog_encrypt_password_label": "Пароль:",
    "dialog_encrypt_password_input_placeholder_text": "Введите пароль",
    "dialog_encrypt_password_hint_label": "Подсказка:",
    "dialog_encrypt_password_button_ok": "ОК",
    "dialog_encrypt_password_button_cancel": "Отмена",

    "dialog_encrypt_password_reset_title": "Сброс пароля шифрования",
    "dialog_encrypt_password_reset_text": "Вы уверены, что хотите сбросить текущий пароль шифрования?",
    "dialog_encrypt_password_reset_button_cancel": "Отмена",
    "dialog_encrypt_password_reset_button_yes": "Да",

    "dialog_open_link_title": "Ссылка",
    "dialog_open_link_text": "Открыть ссылку \"{url}\" в браузере?",

    "dialog_reset_settings_title": "Сбросить настройки?",
    "dialog_reset_settings_text":
        "Все сохранённые данные в настройках будут очищены, и приложение будет перезапущено для применения изменений.",

    "dialog_exit_unsaved_title": "Подтвердить Выход",
    "dialog_exit_unsaved_text": "Открытый файл '{file_name}' не может быть сохранен. Продолжить выход?",

    "message_app_config_file_access": "Доступ запрещен при обращении к файлу настроек приложения в {file_path}. "
                                      "Установите корректные разрешения для обеспечения правильной работы.",

    "field_dir_path_dialog_caption": "Выбрать каталог",
    "field_file_path_dialog_caption": "Выбрать файл",

    "load_file_encryption_password_mismatch": "Несоответствие пароля шифрования!",
    "load_file_encryption_password_incorrect": "Неверный пароль шифрования!",
    "load_file_none_content_error": "Невозможно загрузить файл.",

    "action_new_file_error_occurred": "Не удается создать файл; произошла ошибка.\nПроверьте разрешения файловой системы.",
    "save_active_file_error_occurred": "Не удается сохранить файл; произошла ошибка.",

    "expandable_block_default_title": "Больше информации...",
    "expandable_block_open_close_tags_mismatch_warning": "Несоответствие открывающих/закрывающих тегов блока <details>",

    "dialog_color_picker_color_copied_to_the_clipboard": "Форматированный текст был скопирован в буфер обмена",

    "popup_about_title": "Информация о приложении",
    "popup_about_app_name_description": "Python Markdown Редактор",

    "popup_about_version": "Версия",
    "popup_about_license": "Лицензия",
    "popup_about_website": "Веб-сайт",
    "popup_about_repository": "GitHub",
    "popup_about_pypi": "PyPi",
    "popup_about_date": "Дата",

    "update_helper_new_version_is_available": "Доступна новая версия {latest_version} приложения",
    "update_helper_latest_version_installed": "Установлена последняя версия приложения",

    "network_connection_error_empty": "Не удаётся получить информацию о ответе",
    "network_connection_error_connection_or_dns":
        "Хост не найден. Возможно, проблемы с интернет-соединением или DNS.",
    "network_connection_error_connection_refused":
        "Соединение отклонено. Возможно, сервер не работает или есть проблемы с сетью.",
    "network_connection_error_connection_timed_out": "Время ожидания соединения истекло. Возможно, есть проблемы с сетью.",
    "network_connection_error_connection_404_error":
        "Ошибка соединения 404. Запрошенная страница или ресурс не найдены.",
    "network_connection_error_generic_with_status_code": "Запрос не выполнен, код состояния: {status_code}",
}
