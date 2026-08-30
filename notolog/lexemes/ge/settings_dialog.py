# Georgian lexemes settings_dialog.py
lexemes = {
    # პარამეტრების დიალოგი
    "window_title": "პარამეტრები",

    "button_close": "დახურვა",

    "tab_general": "ძირითადი",
    "tab_workspace": "სამუშაო სივრცე",
    "tab_ai_config": "AI კონფიგურაცია",

    "general_app_config_label": "აპლიკაციის კონფიგურაცია",
    "general_app_language_label": "ენა",
    "general_app_language_combo_placeholder_text": "აირჩიეთ ენა",
    "general_app_language_combo_accessible_description": "აპლიკაციის ინტერფეისის ენა",
    "general_app_theme_label": "თემა",
    "general_app_theme_combo_placeholder_text": "აირჩიეთ თემა",
    "general_app_theme_combo_accessible_description": "აპლიკაციის ინტერფეისის თემა",
    "general_app_default_path_label": "ჩანაწერების ნაგულისხმევი ფოლდერი",
    "general_app_default_path_input_accessible_description": "მიუთითეთ ნაგულისხმევი ფოლდერი, სადაც შენახული იქნება ჩანაწერები",
    "general_app_default_path_input_placeholder_text": "აირჩიეთ ან შეიყვანეთ ფოლდერის გზა",
    "general_app_elements_visibility_label": "ელემენტების ხილვადობის მართვა",
    "general_app_main_menu_label": "მთავარი მენიუ",
    "general_app_main_menu_checkbox": "მთავარი მენიუს ჩვენება",
    "general_app_main_menu_checkbox_accessible_description": "აჩვენეთ აპლიკაციის მთავარი ჩამოშლილი მენიუ",
    "general_app_font_size_label": "შრიფტის ზომა: {size}pt",
    "general_app_font_size_slider_accessible_description": "შრიფტის გლობალური ზომის რეგულირება",

    "general_file_deletion_label": "ფაილების წაშლა",
    "general_reversible_file_deletion_checkbox": "ფაილების აღდგენადად წაშლა",
    "general_reversible_file_deletion_checkbox_accessible_description":
        "წაშლილი ფაილების Notolog-ის კალათაში გადატანა .del გაფართოების დამატებით",

    "workspace_bottom_bar_show_global_cursor_position_checkbox": "მსოფლიო კურსორის პოზიციის ჩვენება",
    "workspace_bottom_bar_show_global_cursor_position_checkbox_accessible_description":
        "აჩვენეთ კურსორის მსოფლიო პოზიცია სტატუსის ზოლში",
    "workspace_bottom_bar_show_navigation_arrows_checkbox": "ნავიგაციის ისრების ჩვენება",
    "workspace_bottom_bar_show_navigation_arrows_checkbox_accessible_description": "ნავიგაციის ისრების გამოჩენა სტატუსბარში",

    "workspace_editor_mode_label": "რედაქტირების რეჟიმი",
    "workspace_editor_mode_show_line_numbers_checkbox": "ხაზების ნომრების ჩვენება",
    "workspace_editor_mode_show_line_numbers_checkbox_accessible_description": "ხაზების ნომრების ჩვენება რედაქტორში",

    "workspace_view_mode_label": "ნახვის რეჟიმი",
    "workspace_view_mode_process_emojis_checkbox": "ტექსტური ემოჯის გრაფიკულად გარდაქმნა",
    "workspace_view_mode_process_emojis_checkbox_accessible_description": "ტექსტური ემოჯების გრაფიკული წარმოჩენა",
    "workspace_view_mode_highlight_todos_checkbox": "TODO-ების გამოყოფა",
    "workspace_view_mode_highlight_todos_checkbox_accessible_description": "TODO ტეგების გამოყოფა ტექსტში",
    "workspace_view_mode_open_link_confirmation_checkbox": "ბმულების გახსნის დასტური",
    "workspace_view_mode_open_link_confirmation_checkbox_accessible_description":
        "ბმულების გახსნისას დასტურის მოთხოვნა",
    "workspace_view_mode_save_resources_checkbox": "გარე სურათების ავტომატური შენახვა დისკზე",
    "workspace_view_mode_save_resources_checkbox_accessible_description":
        "გარე სურათების ასლების ავტომატურად შენახვა დისკზე ოფლაინ წვდომისთვის.",

    "ai_config_inference_module_label": "ინფერენციის მოდული",
    "ai_config_inference_module_names_combo_label": "აქტიური ინფერენციის მოდული",
    "ai_config_inference_module_names_combo_placeholder_text": "აირჩიეთ მოდული",
    "ai_config_inference_module_names_combo_accessible_description":
        "აირჩიეთ AI ასისტენტთან მუშაობადი არსებული AI ინფერენციის მოდულებიდან.\n"
        "ოფციები მოიცავს ლოკალური დიდი ენის მოდელებს (LLM) რეალური დროის დამუშავებით,\n"
        "ან API-ზე დაყრდნობითი ფუნქციონალობით.",

    "ai_config_base_label": "ძირითადი პარამეტრები",
    "ai_config_multi_turn_dialogue_checkbox": "მრავალშრიანი დიალოგი საუბრის მეხსიერებით",
    "ai_config_multi_turn_dialogue_checkbox_accessible_description":
        "ჩართეთ მრავალშრიანი დიალოგი, რომელიც ინახავს წინა მოთხოვნას საუბრის მეხსიერებისთვის.\n"
        "გამორთვის შემთხვევაში, მხოლოდ ახალი შეტყობინება და სისტემის პრომპტი ახდენენ გავლენას პასუხზე.",
    "ai_config_convert_to_md_checkbox": "შედეგის Markdown-ში კონვერტაცია",
    "ai_config_convert_to_md_checkbox_accessible_description":
        "გადაიყვანეთ გამოსახული შეტყობინება Markdown ფორმატში.",
    "workspace_bottom_bar_label": "ქვედა ზოლი",
    "workspace_bottom_bar_show_system_load_graphs_checkbox": "CPU-სა და მეხსიერების გრაფიკების ჩვენება",
    "workspace_bottom_bar_show_system_load_graphs_checkbox_accessible_description":
        "ქვედა ზოლში CPU-სა და მეხსიერების გამოყენების გრაფიკებისა და გამყოფის ჩვენება",
    "workspace_bottom_bar_system_load_interval_ms_label": "გრაფიკების განახლების ინტერვალი",
    "workspace_bottom_bar_system_load_interval_ms_accessible_description":
        "CPU-სა და მეხსიერების გამოყენების წაკითხვის ინტერვალი მილიწამებში",
}
