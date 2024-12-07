# Georgian lexemes settings_dialog.py
lexemes = {
    "tab_openai_api_config": "OpenAI API",

    "module_openai_api_label": "OpenAI API",
    "module_openai_api_url_label": "API-ს URL",
    "module_openai_api_url_input_placeholder_text": "API-ს URL",
    "module_openai_api_url_input_accessible_description":
        "OpenAI API-ს URL არის API-ის საბოლოო წერტილის მისამართი, რომელიც შეიძლება შეიცვალოს სერვისის და ვერსიის მიხედვით.\n"
        "AI ასისტენტი იყენებს მას საუბრის ჩატისთვის ან ტექსტის შევსებისთვის.\n"
        "მიმდინარე URL-ის მისაღებად მიმართეთ OpenAI API-ის ოფიციალურ დოკუმენტაციას.",
    "module_openai_api_key_label": "API გასაღები",
    "module_openai_api_key_input_placeholder_text": "API გასაღები",
    "module_openai_api_key_input_accessible_description":
        "OpenAI API გასაღები არის საიდუმლო ნიშანი, რომელიც გამოიყენება API-ის საბოლოო წერტილზე\n"
        "მოთხოვნების აუთენტიფიკაციისთვის.",
    "module_openai_api_supported_models_label": "მხარდაჭერილი მოდელები",
    "module_openai_api_model_names_combo_placeholder_text": "აირჩიეთ მოდელი",
    "module_openai_api_model_names_combo_accessible_description":
        "აირჩიეთ ჩატის საუბარებისთვის მხარდაჭერილი მოდელებიდან.",

    "module_openai_api_base_system_prompt_label": "სისტემის პრომპტი",
    "module_openai_api_base_system_prompt_edit_placeholder_text":
        "ბაზისის სისტემური პრომპტი, რომელიც წინასწარმოიდგინება თითოეულ მოთხოვნას",
    "module_openai_api_base_system_prompt_edit_accessible_description":
        "ბაზისის სისტემური პრომპტი, რომელიც წინასწარმოიდგინება თითოეულ მოთხოვნას.\n"
        "ჩვეულებრივ წერტილიანი ტექსტია, რომელშიც არის ინსტრუქციები ან როლის თვისებები.",

    "module_openai_api_base_response_temperature_label": "ტემპერატურა: {temperature}",
    "module_openai_api_base_response_temperature_input_accessible_description":
        "რეგულირებს მოდელის პასუხების შემთხვევითობას. მაღალი მნიშვნელობები წარმოქმნიან უფრო რაზმიკებულ შედეგებს, "
        "ხოლო დაბალი მნიშვნელობები ხდის პასუხებს უფრო წინასწარ განსაზღვრად.",

    "module_openai_api_base_response_max_tokens_label": "პასუხის მაქსიმუმი ტოკენების რაოდენობა",
    "module_openai_api_base_response_max_tokens_input_accessible_description":
        "მაქსიმალური ტოკენების რაოდენობას ანიჭებს, რომელიც პასუხში მიიღება, როგორიცაა სიტყვები და პუნქტუაცია, "
        "რეგულირებს შედეგის სიგრძეს.",

    "module_openai_api_config_prompt_history_size_label": "პრომპტის ისტორიის ზომა",
    "module_openai_api_config_prompt_history_size_input_accessible_description":
        "კონტროლებს სისტემაში შენახული პრომპტის ისტორიის შენახვის შენახულ ჩანაწერების რაოდენობას.\n"
        "ნულოვანი მნიშვნელობა გამოიყენება შეუზღუდავ ჩანაწერებისთვის."
}
