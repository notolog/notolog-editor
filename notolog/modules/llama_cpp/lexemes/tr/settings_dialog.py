# Turkish lexemes settings_dialog.py
lexemes = {
    "tab_module_llama_cpp_config": "Modül llama.cpp",

    "module_llama_cpp_config_label": "Modül llama.cpp",
    "module_llama_cpp_config_path_label": "Model Yerleşimi",
    "module_llama_cpp_config_path_input_placeholder_text": "Model yolu seçin veya girin",
    "module_llama_cpp_config_path_input_accessible_description":
        "Yerel modelin yolunu belirtmek için bir seçiciye sahip giriş alanı. GGUF formatındaki modelleri destekler,\n"
        "GGML ile kullanılan ve GGML tabanlı yürütücüler için optimize edilmiş bir ikili dosya formatıdır.",
    "module_llama_cpp_config_path_input_filter_text": "GGUF Dosyaları",

    "module_llama_cpp_config_context_window_label": "Bağlam Penceresi Boyutu",
    "module_llama_cpp_config_context_window_input_accessible_description":
        "Modelin yanıtları üretmek için dikkate aldığı token sayısını belirler.\n"
        "Ne kadar önceki bağlamın kullanıldığını kontrol eder.",

    "module_llama_cpp_config_chat_formats_label": "Sohbet Formatları",
    "module_llama_cpp_config_chat_formats_combo_placeholder_text": "Bir sohbet formatı seçin",
    "module_llama_cpp_config_chat_formats_combo_accessible_description":
        "Model konuşmaları için kullanılan formatı seçmek için açılır menü.",

    "module_llama_cpp_config_gpu_layers_label": "GPU Katmanları",
    "module_llama_cpp_config_gpu_layers_input_accessible_description":
        "GPU'ya aktarılacak model katmanı sayısı.\n"
        "Auto: Otomatik algılama (Apple Silicon'da GPU, diğerlerinde CPU).\n"
        "-1: Tüm katmanları GPU'ya aktar.\n"
        "0: Yalnızca CPU modu (Intel Mac'ler için önerilir).\n"
        "1-999: Kısmi GPU aktarımı (gelişmiş).",

    "module_llama_cpp_config_system_prompt_label": "Sistem İstem",
    "module_llama_cpp_config_system_prompt_edit_placeholder_text": "Sistem istem metnini girin",
    "module_llama_cpp_config_system_prompt_edit_accessible_description":
        "Model yanıtlarını yönlendiren sistem istemlerini girmek için metin alanı.",

    "module_llama_cpp_config_response_temperature_label": "Yanıt Sıcaklığı: {temperature}",
    "module_llama_cpp_config_response_temperature_input_accessible_description":
        "Modelin yanıtlarının rastgeleliğini ayarlar. Daha yüksek değerler daha çeşitli çıktılar üretir,\n"
        "daha düşük değerler ise daha öngörülebilir yanıtlar verir.",

    "module_llama_cpp_config_response_max_tokens_label": "Yanıt Başına Maksimum Token",
    "module_llama_cpp_config_response_max_tokens_input_accessible_description":
        "Modelin yanıtlarındaki token sayısını gerçek bağlam penceresi limitine kadar sınırlar.\n"
        "Sıfır değer, bağlam penceresinin kapasitesini varsayar.",

    "module_llama_cpp_config_prompt_history_size_label": "İstem Geçmişi Boyutu",
    "module_llama_cpp_config_prompt_history_size_input_accessible_description":
        "Sistem tarafından referans için tutulan istem geçmişindeki giriş sayısını kontrol eder.\n"
        "Sıfır değer sınırsız girişe izin verir."
}
