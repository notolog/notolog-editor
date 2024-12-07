# Georgian lexemes settings_dialog.py
lexemes = {
    "tab_ondevice_llm_config": "მოწყობილობაზე LLM",

    "module_ondevice_llm_config_label": "მოწყობილობაზე LLM მოდელი",
    "module_ondevice_llm_config_path_label": "ONNX მოდელის მდებარეობა",
    "module_ondevice_llm_config_path_input_placeholder_text": "მოდელის დირექტორიის გზა",
    "module_ondevice_llm_config_path_input_accessible_description":
        "შეყვანის ველი სელექტორით მოდელის დირექტორიის გზის მითითებისთვის, სადაც ONNX ფაილები მდებარეობენ.\n"
        "მხარდაჭერილი მოდელები არის ONNX ფორმატში, რაც აღნიშნავს ოფლიანური ნეირონული ქსელის გაცვლის ღია სტანდარტს\n"
        "მანქანური სწავლის მოდელების ფორმატისთვის.",

    "module_ondevice_llm_config_response_temperature_label": "ტემპერატურა: {temperature}",
    "module_ondevice_llm_config_response_temperature_input_accessible_description":
        "რეგულირებს მოდელის პასუხების შემთხვევითობას. მაღალი მნიშვნელობები ქმნიან უფრო ვარიაციულ გამოსავალებს,\n"
        "დაბალი მნიშვნელობები გამოიღებენ უფრო წინასწარ განსაზღვრავ პასუხებს.",

    "module_ondevice_llm_config_response_max_tokens_label": "პასუხში მაქსიმუმ ტოკენების რაოდენობა",
    "module_ondevice_llm_config_response_max_tokens_input_accessible_description":
        "შეზღუდავს მოდელის პასუხებში ტოკენების რაოდენობას აქტუალური კონტექსტის ფანჯრის ლიმიტამდე.\n"
        "ნულოვანი მნიშვნელობა გამოიყენებს კონტექსტის ფანჯრის ჩათვლითი ტევადობას.",

    "module_ondevice_llm_config_prompt_history_size_label": "პრომპტის ისტორიის ზომა",
    "module_ondevice_llm_config_prompt_history_size_input_accessible_description":
        "კონტროლირებს პრომპტების ისტორიაში ჩანაწერების რაოდენობას, რომელიც სისტემამ სარეფერენციოდ ინახავს.\n"
        "ნულოვანი მნიშვნელობა აძლევს ულიმიტო შეტანებას."
}
