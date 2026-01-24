# Georgian lexemes common.py
lexemes = {
    "app_title": "Notolog რედაქტორი",
    "app_title_with_sub": "{app_title} - {sub_title}",

    "tree_filter_input_placeholder_text": "სწრაფი ფილტრი",
    "tree_filter_input_accessible_desc": "გაფილტვრა ფაილებისა და დირექტორიების სახელის მიხედვით",
    "tree_filter_clear_button_tooltip": "ფილტრის გასუფთავება",
    "tree_filter_clear_button_accessible_name": "ფილტრის ველის გასუფთავება",

    "menu_action_copy_file_path": "ფაილის გზის კოპირება",
    "menu_action_rename": "გადარქმევა",
    "menu_action_delete": "წაშლა",
    "menu_action_delete_completely": "სრული წაშლა",
    "menu_action_restore": "აღდგენა",
    "menu_action_create_new_dir": "ახალი დირექტორიის შექმნა",

    "dialog_file_rename_title": "ფაილის გადარქმევა",
    "dialog_file_rename_field_label": "შეიყვანეთ ახალი ფაილის სახელი",
    "dialog_file_rename_button_ok": "გადარქმევა",
    "dialog_file_rename_warning_exists": "ამ სახელით ფაილი უკვე არსებობს",

    "dialog_file_delete_title": "ფაილის წაშლა",
    "dialog_file_delete_text": "წაშლა ფაილი \"{file_name}\"?",
    "dialog_file_delete_completely_title": "ფაილის სრული წაშლა",
    "dialog_file_delete_completely_text": "წაშალეთ ფაილი \"{file_name}\" სრულად?",
    "dialog_file_delete_error": "ფაილის წაშლა ვერ ხერხდება, წარმოიშვა შეცდომა",
    "dialog_file_delete_error_not_found": "ფაილი ვერ მოიძებნა",

    "dialog_file_restore_title": "ფაილის აღდგენა",
    "dialog_file_restore_text": "აღადგინოთ ფაილი \"{file_name}\"?",
    "dialog_file_restore_error": "ფაილის აღდგენა ვერ ხერხდება, წარმოიშვა შეცდომა",
    "dialog_file_restore_warning_exists": "ამ სახელით ფაილი უკვე არსებობს",

    "dialog_create_new_dir_title": "ახალი დირექტორიის შექმნა",
    "dialog_create_new_dir_label": "ახალი დირექტორიის სახელი",
    "dialog_create_new_dir_input_placeholder_text": "შეიყვანეთ დირექტორიის სახელი",
    "dialog_create_new_dir_button_ok": "შექმნა",
    "dialog_create_new_dir_button_cancel": "გაუქმება",
    "dialog_create_new_dir_warning_empty_title": "ახალი დირექტორიის სახელის შეცდომა",
    "dialog_create_new_dir_warning_empty_text": "დირექტორიის სახელი არ შეიძლება იყოს ცარიელი",
    "dialog_create_new_dir_warning_too_long_title": "ახალი დირექტორიის სახელის შეცდომა",
    "dialog_create_new_dir_warning_too_long_text": "დირექტორიის სახელი ძალიან გრძელია; მაქსიმუმ "
                                                   "{symbols} სიმბოლოებია ნებადართული!",
    "dialog_create_new_dir_error_existed": "დირექტორია უკვე არსებობს",
    "dialog_create_new_dir_error": "ვერ შევქმენით დირექტორია. დარწმუნდით, რომ სამიზნე დირექტორია "
                                   "{base_dir} ჩაწერის შესაძლებლობით არის",

    "dialog_message_box_title": "შეტყობინება",
    "dialog_message_box_button_ok": "დახურვა",

    "action_new_file_first_line_template_text": "ახალი დოკუმენტი",
    "action_open_file_dialog_caption": "ფაილის გახსნა",
    "action_save_as_file_dialog_caption": "ფაილის შენახვა",

    "dialog_save_empty_file_title": "ცარიელი ფაილის შენახვა",
    "dialog_save_empty_file_text": "დაშვებულია ფაილის შენახვა ცარიელი შინაარსით?",

    "dialog_encrypt_file_title": "ფაილის დაშიფვრა",
    "dialog_encrypt_file_text": "დაშიფრეთ ფაილი \"{file_name}\"?",
    "encrypt_file_warning_file_is_already_encrypted": "ფაილი უკვე დაშიფრულია!",
    "dialog_encrypt_file_rewrite_existing_title": "არსებული ფაილის გადაწერა",
    "dialog_encrypt_file_rewrite_existing_text": "გადაწერეთ არსებული ფაილი \"{file_path}\"?",

    "dialog_decrypt_file_title": "ფაილის დეშიფვრა",
    "dialog_decrypt_file_text": "დეშიფრეთ ფაილი \"{file_name}\"?",
    "decrypt_file_warning_file_is_not_encrypted": "ფაილი არ არის დაშიფრული!",
    "dialog_decrypt_file_rewrite_existing_title": "არსებული ფაილის გადაწერა",
    "dialog_decrypt_file_rewrite_existing_text": "გადაწერეთ არსებული ფაილი \"{file_path}\"?",

    "dialog_encrypt_new_password_title": "ახალი პაროლი",
    "dialog_encrypt_new_password_label": "პაროლი:",
    "dialog_encrypt_new_password_input_placeholder_text": "შეიყვანეთ ახალი პაროლი",
    "dialog_encrypt_new_password_hint_label": "მინიშნება:",
    "dialog_encrypt_new_password_hint_label_description":
        "მინიშნება არ არის დაშიფრული და ფაილიდან იკითხება!"
        "\nარ გამოიყენოთ მინიშნები, რომლებიც ადვილად შეიმჩნევა, როგორიცაა"
        "\nდაბადების თარიღი."
        "\nსცადეთ გამოიყენოთ რეფერენცია, რომელიც ადვილად არ არის თქვენთან გაიგიანებელი.",
    "dialog_encrypt_new_password_hint_input_placeholder_text": "შეიყვანეთ მინიშნება (არასავალდებულო)",
    "dialog_encrypt_new_password_button_ok": "კარგი",
    "dialog_encrypt_new_password_button_cancel": "გაუქმება",
    "dialog_encrypt_new_password_warning_empty_title": "გაფრთხილება",
    "dialog_encrypt_new_password_warning_empty_text": "პაროლის ველი ცარიელი ვერ დარჩება!",
    "dialog_encrypt_new_password_warning_too_long_title": "გაფრთხილება",
    "dialog_encrypt_new_password_warning_too_long_text": "მინიშნების ველი ძალიან გრძელია, მაქსიმუმი {symbols} სიმბოლო!",

    "dialog_encrypt_password_title": "პაროლის შეტანა",
    "dialog_encrypt_password_label": "პაროლი:",
    "dialog_encrypt_password_input_placeholder_text": "შეიყვანეთ პაროლი",
    "dialog_encrypt_password_hint_label": "მინიშნება:",
    "dialog_encrypt_password_button_ok": "კარგი",
    "dialog_encrypt_password_button_cancel": "გაუქმება",

    "dialog_encrypt_password_reset_title": "დაშიფრვის პაროლის განულება",
    "dialog_encrypt_password_reset_text": "დარწმუნებული ხართ, რომ გსურთ მიმდინარე დაშიფრვის პაროლის განულება?",
    "dialog_encrypt_password_reset_button_cancel": "გაუქმება",
    "dialog_encrypt_password_reset_button_yes": "დიახ",

    "dialog_open_link_title": "ბმული",
    "dialog_open_link_text": "გახსნა ბმული \"{url}\" ბრაუზერში?",

    "dialog_reset_settings_title": "პარამეტრების აღდგენა?",
    "dialog_reset_settings_text":
        "ყველა შენახული მონაცემი პარამეტრებში წაიშლება, და აპლიკაცია გადაიტვირთება ცვლილებების გამო.",

    "dialog_exit_unsaved_title": "გასვლის დადასტურება",
    "dialog_exit_unsaved_text": "გახსნილი ფაილი '{file_name}' ვერ ინახება. გავაგრძელოთ გასვლა?",

    "message_app_config_file_access": "დაშვების უფლებები უარყოფილია {file_path} აპლიკაციის კონფიგურაციული ფაილის წვდომისას. "
                                      "დააყენეთ სწორი უფლებები სწორი ოპერაციის გარანტირებლად.",

    "field_dir_path_dialog_caption": "აირჩიეთ დირექტორია",
    "field_file_path_dialog_caption": "აირჩიეთ ფაილი",

    "dialog_select_default_dir_title": "აირჩიეთ ნაგულისხმევი ფოლდერი",
    "dialog_select_default_dir_label": "აირჩიეთ ნოტებისთვის ნაგულისხმევი ფოლდერი",
    "dialog_select_default_dir_input_placeholder_text": "ნაგულისხმევი ნოტების ფოლდერი",
    "dialog_select_default_dir_button_ok": "არჩევა",
    "dialog_select_default_dir_button_cancel": "გაუქმება",

    "load_file_encryption_password_mismatch": "შიფრირების პაროლი არ ემთხვევა!",
    "load_file_encryption_password_incorrect": "შესაშიფრი პაროლი არასწორია!",
    "load_file_none_content_error": "ფაილის ჩატვირთვა შეუძლებელია.",

    "open_dir_permission_error": "ფოლდერის წვდომა უარყოფილია.",
    "open_file_permission_error": "ფაილზე წვდომა უარყოფილია.",
    "rename_file_permission_error": "ფაილის გადარქმევის ნებართვა უარყოფილია.",

    "action_new_file_error_occurred": "ფაილის შექმნა ვერ ხერხდება; მოხდა შეცდომა.\nგადამოწმეთ ფაილის სისტემის ნებართვები.",
    "save_active_file_error_occurred": "ფაილის შენახვა ვერ ხერხდება; მოხდა შეცდომა.",

    "expandable_block_default_title": "მეტი ინფორმაცია...",
    "expandable_block_open_close_tags_mismatch_warning": "<details> ბლოკის გახსნის/დახურვის თეგების არასწორი მოთხოვნები",

    "dialog_color_picker_color_copied_to_the_clipboard": "ფორმატირებული ტექსტი ბუფერში ასლი გადაიტანეს",

    "popup_about_title": "აპლიკაციის ინფორმაცია",
    "popup_about_app_name_description": "Python-ის Markdown რედაქტორი",

    "popup_about_version": "ვერსია",
    "popup_about_license": "ლიცენზია",
    "popup_about_website": "ვებგვერდი",
    "popup_about_repository": "GitHub",
    "popup_about_pypi": "PyPi",
    "popup_about_date": "თარიღი",

    "update_helper_new_version_is_available": "აპლიკაციის ახალი ვერსია {latest_version} მისაწვდომია",
    "update_helper_latest_version_installed": "აპლიკაციის უახლესი ვერსია დაყენებულია",

    "network_connection_error_empty": "პასუხის ინფორმაციის მიღება ვერ ხერხდება",
    "network_connection_error_connection_or_dns":
        "ჰოსტი ვერ მოიძებნა. შესაძლოა ინტერნეტის კავშირში ან DNS-ში იყოს პრობლემა.",
    "network_connection_error_connection_refused":
        "კავშირი უარყოფილია. სერვერი შესაძლოა გამორთული იყოს ან ქსელში იყოს პრობლემები.",
    "network_connection_error_connection_timed_out": "კავშირი დავადებით დამთავრდა. შესაძლოა ქსელში იყოს პრობლემები.",
    "network_connection_error_connection_404_error":
        "404 კავშირის შეცდომა. მოთხოვნილი გვერდი ან რესურსი ვერ მოიძებნა.",
    "network_connection_error_generic_with_status_code": "მოთხოვნა ვერ შესრულდა, სტატუსის კოდი: {status_code}",
}
