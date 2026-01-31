# Georgian lexemes settings_dialog.py
lexemes = {
    "tab_module_llama_cpp_config": "მოდული llama.cpp",

    "module_llama_cpp_config_label": "მოდული llama.cpp",
    "module_llama_cpp_config_path_label": "მოდელის მდებარეობა",
    "module_llama_cpp_config_path_input_placeholder_text": "აირჩიეთ ან შეიყვანეთ მოდელის გზა",
    "module_llama_cpp_config_path_input_accessible_description":
        "შეყვანის ველი სელექტორით ადგილზე მოდელის გზის მითითებისთვის. მხარდაჭერს GGUF ფორმატის მოდელებს,\n"
        "ბინარული ფაილის ფორმატი, ოპტიმიზირებული GGML-ით და GGML-ზე მუშაობადი ეგზეკუტორებისთვის.",
    "module_llama_cpp_config_path_input_filter_text": "GGUF ფაილები",

    "module_llama_cpp_config_context_window_label": "კონტექსტის ფანჯრის ზომა",
    "module_llama_cpp_config_context_window_input_accessible_description":
        "აყენებს ტოკენების რაოდენობას, რომელსაც მოდელი გამოიყენებს პასუხების გენერირებისთვის. კონტროლირებს წინა კონტექსტის\n"
        "გამოყენების რაოდენობას.",

    "module_llama_cpp_config_chat_formats_label": "ჩეთის ფორმატები",
    "module_llama_cpp_config_chat_formats_combo_placeholder_text": "აირჩიეთ ჩეთის ფორმატი",
    "module_llama_cpp_config_chat_formats_combo_accessible_description":
        "ჩამოშლილი მენიუ მოდელის საუბარების ფორმატის არჩევისთვის.",

    "module_llama_cpp_config_gpu_layers_label": "GPU ფენები",
    "module_llama_cpp_config_gpu_layers_input_accessible_description":
        "მოდელის ფენების რაოდენობა GPU-ზე გადასატანად.\n"
        "Auto: ავტომატური განსაზღვრა (GPU Apple Silicon-ზე, CPU სხვაგან).\n"
        "-1: ყველა ფენის გადატანა GPU-ზე.\n"
        "0: მხოლოდ CPU რეჟიმი (რეკომენდებულია Intel Mac-ისთვის).\n"
        "1-999: ნაწილობრივი GPU გადატანა (მოწინავე).",

    "module_llama_cpp_config_system_prompt_label": "სისტემის პრომპტი",
    "module_llama_cpp_config_system_prompt_edit_placeholder_text": "შეიყვანეთ სისტემის პრომპტის ტექსტი",
    "module_llama_cpp_config_system_prompt_edit_accessible_description":
        "ტექსტის ველი, რომელიც განაცხადი პრომპტების შეყვანას რეგულირებს, რომლებიც იძლევა\n"
        "მოდელის პასუხების გამართვას.",

    "module_llama_cpp_config_response_temperature_label": "პასუხის ტემპერატურა: {temperature}",
    "module_llama_cpp_config_response_temperature_input_accessible_description":
        "რეგულირებს მოდელის პასუხების შემთხვევითობას. მაღალი მნიშვნელობები ქმნიან უფრო ვარიაციულ გამოსავალებს,\n"
        "დაბალი მნიშვნელობები გამოიღებენ უფრო წინასწარ განსაზღვრავ პასუხებს.",

    "module_llama_cpp_config_response_max_tokens_label": "პასუხში მაქსიმუმ ტოკენების რაოდენობა",
    "module_llama_cpp_config_response_max_tokens_input_accessible_description":
        "შეზღუდავს მოდელის პასუხებში ტოკენების რაოდენობას აქტუალური კონტექსტის ფანჯრის ლიმიტამდე.\n"
        "ნულოვანი მნიშვნელობა გამოიყენებს კონტექსტის ფანჯრის ჩათვლითი ტევადობას.",

    "module_llama_cpp_config_prompt_history_size_label": "პრომპტის ისტორიის ზომა",
    "module_llama_cpp_config_prompt_history_size_input_accessible_description":
        "კონტროლირებს პრომპტების ისტორიაში ჩანაწერების რაოდენობას, რომელიც სისტემამ სარეფერენციოდ ინახავს.\n"
        "ნულოვანი მნიშვნელობა აძლევს ულიმიტო შეტანებას."
}
