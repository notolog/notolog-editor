# Turkish lexemes settings_dialog.py
lexemes = {
    "tab_openai_api_config": "OpenAI API",

    "module_openai_api_label": "OpenAI API",
    "module_openai_api_url_label": "API URL",
    "module_openai_api_url_input_placeholder_text": "API URL",
    "module_openai_api_url_input_accessible_description":
        "OpenAI API'sinin URL'si, API'nin uç noktasının adresidir ve hizmete veya sürüme bağlı olarak değişebilir.\n"
        "AI Asistanı, sohbet işlevselliği veya metin tamamlama için uç noktayı kullanır.\n"
        "Mevcut URL'yi almak için OpenAI API'nin resmi belgelerine başvurun.",
    "module_openai_api_key_label": "API Anahtarı",
    "module_openai_api_key_input_placeholder_text": "API Anahtarı",
    "module_openai_api_key_input_accessible_description":
        "OpenAI API Anahtarı, API uç noktasına yapılan istekleri doğrulamak için kullanılan gizli bir jetondur.",
    "module_openai_api_supported_models_label": "Desteklenen Modeller",
    "module_openai_api_model_names_combo_placeholder_text": "Bir Model Seçin",
    "module_openai_api_model_names_combo_accessible_description":
        "Sohbet konuşmaları için desteklenen modellerden seçim yapın.",

    "module_openai_api_base_system_prompt_label": "Sistem İstemleri",
    "module_openai_api_base_system_prompt_edit_placeholder_text": "Her istekten önce gelen temel sistem istemi",
    "module_openai_api_base_system_prompt_edit_accessible_description":
        "Her istekten önce gelen temel sistem istemi.\n"
        "Genellikle talimatlar veya rol özellikleri içeren düz metindir.",

    "module_openai_api_base_response_temperature_label": "Sıcaklık: {temperature}",
    "module_openai_api_base_response_temperature_input_accessible_description":
        "Modelin yanıtlarının rastgeleliğini ayarlar. Daha yüksek değerler daha çeşitli çıktılar üretir, "
        "daha düşük değerler ise yanıtları daha tahmin edilebilir yapar.",

    "module_openai_api_base_response_max_tokens_label": "Maksimum Yanıt Token'ları",
    "module_openai_api_base_response_max_tokens_input_accessible_description":
        "Yanıtta alınacak maksimum token sayısını belirler, bu da kelimeler ve noktalama işaretlerini içerir, "
        "çıktının uzunluğunu kontrol eder.",

    "module_openai_api_config_prompt_history_size_label": "İstem Geçmişi Boyutu",
    "module_openai_api_config_prompt_history_size_input_accessible_description":
        "Sistem tarafından referans için tutulan istem geçmişindeki giriş sayısını kontrol eder.\n"
        "Sıfır değer sınırsız girişe izin verir."
}
