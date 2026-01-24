# Indonesian lexemes settings_dialog.py
lexemes = {
    "tab_module_llama_cpp_config": "Modul llama.cpp",

    "module_llama_cpp_config_label": "Modul llama.cpp",
    "module_llama_cpp_config_path_label": "Lokasi Model",
    "module_llama_cpp_config_path_input_placeholder_text": "Pilih atau masukkan jalur model",
    "module_llama_cpp_config_path_input_accessible_description":
        "Kolom input dengan pemilih untuk menentukan jalur model lokal. Mendukung model dalam format GGUF,\n"
        "format file biner yang dioptimalkan untuk menyimpan model yang digunakan dengan GGML dan eksekutor berbasis GGML.",
    "module_llama_cpp_config_path_input_filter_text": "Berkas GGUF",

    "module_llama_cpp_config_context_window_label": "Ukuran Jendela Konteks",
    "module_llama_cpp_config_context_window_input_accessible_description":
        "Mengatur jumlah token yang dipertimbangkan model untuk menghasilkan respons. "
        "Mengontrol seberapa banyak konteks sebelumnya yang digunakan.",

    "module_llama_cpp_config_chat_formats_label": "Format Obrolan",
    "module_llama_cpp_config_chat_formats_combo_placeholder_text": "Pilih format obrolan",
    "module_llama_cpp_config_chat_formats_combo_accessible_description":
        "Menu dropdown untuk memilih format yang digunakan untuk percakapan model.",

    "module_llama_cpp_config_system_prompt_label": "Perintah Sistem",
    "module_llama_cpp_config_system_prompt_edit_placeholder_text": "Masukkan teks perintah sistem",
    "module_llama_cpp_config_system_prompt_edit_accessible_description":
        "Kolom teks untuk memasukkan perintah sistem yang memandu respons model.",

    "module_llama_cpp_config_response_temperature_label": "Suhu Respons: {temperature}",
    "module_llama_cpp_config_response_temperature_input_accessible_description":
        "Menyesuaikan keacakan respons model. Nilai yang lebih tinggi menghasilkan output yang lebih bervariasi,\n"
        "sementara nilai yang lebih rendah menghasilkan respons yang lebih dapat diprediksi.",

    "module_llama_cpp_config_response_max_tokens_label": "Token Maksimum per Respons",
    "module_llama_cpp_config_response_max_tokens_input_accessible_description":
        "Membatasi jumlah token dalam respons model hingga batas jendela konteks aktual.\n"
        "Nilai nol mengasumsikan kapasitas jendela konteks.",

    "module_llama_cpp_config_prompt_history_size_label": "Ukuran Riwayat Perintah",
    "module_llama_cpp_config_prompt_history_size_input_accessible_description":
        "Mengontrol jumlah entri dalam riwayat perintah yang disimpan sistem untuk referensi.\n"
        "Nilai nol memungkinkan entri tak terbatas."
}
