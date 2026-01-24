# Indonesian lexemes settings_dialog.py
lexemes = {
    "tab_openai_api_config": "OpenAI API",

    "module_openai_api_label": "OpenAI API",
    "module_openai_api_url_label": "URL API",
    "module_openai_api_url_input_placeholder_text": "URL API",
    "module_openai_api_url_input_accessible_description":
        "URL OpenAI API adalah alamat ke endpoint API, yang mungkin bervariasi tergantung pada layanan dan versi.\n"
        "Asisten AI menggunakan yang untuk fungsionalitas obrolan percakapan atau penyelesaian teks.\n"
        "Lihat dokumentasi resmi OpenAI API untuk mendapatkan URL terkini.",
    "module_openai_api_key_label": "Kunci API",
    "module_openai_api_key_input_placeholder_text": "Kunci API",
    "module_openai_api_key_input_accessible_description":
        "Kunci OpenAI API adalah token rahasia yang digunakan untuk mengautentikasi permintaan ke endpoint API.",
    "module_openai_api_supported_models_label": "Model yang Didukung",
    "module_openai_api_model_names_combo_placeholder_text": "Pilih Model",
    "module_openai_api_model_names_combo_accessible_description":
        "Pilih dari model yang didukung untuk percakapan obrolan.",

    "module_openai_api_base_system_prompt_label": "Perintah Sistem",
    "module_openai_api_base_system_prompt_edit_placeholder_text": "Perintah sistem dasar yang mendahului setiap permintaan",
    "module_openai_api_base_system_prompt_edit_accessible_description":
        "Perintah sistem dasar yang mendahului setiap permintaan.\n"
        "Biasanya berupa teks biasa dengan instruksi atau karakteristik peran.",

    "module_openai_api_base_response_temperature_label": "Suhu: {temperature}",
    "module_openai_api_base_response_temperature_input_accessible_description":
        "Menyesuaikan keacakan respons model. Nilai yang lebih tinggi menghasilkan output yang lebih bervariasi, "
        "sementara nilai yang lebih rendah membuat respons lebih dapat diprediksi.",

    "module_openai_api_base_response_max_tokens_label": "Token Respons Maksimum",
    "module_openai_api_base_response_max_tokens_input_accessible_description":
        "Jumlah maksimum token yang diterima dalam respons, seperti kata dan tanda baca, "
        "mengontrol panjang output.",

    "module_openai_api_config_prompt_history_size_label": "Ukuran Riwayat Perintah",
    "module_openai_api_config_prompt_history_size_input_accessible_description":
        "Mengontrol jumlah entri dalam riwayat perintah yang disimpan sistem untuk referensi.\n"
        "Nilai nol memungkinkan entri tak terbatas."
}
