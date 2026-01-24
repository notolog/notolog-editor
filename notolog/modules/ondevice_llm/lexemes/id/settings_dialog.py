# Indonesian lexemes settings_dialog.py
lexemes = {
    "tab_ondevice_llm_config": "LLM Perangkat Lokal",

    "module_ondevice_llm_config_label": "Model LLM Perangkat Lokal",
    "module_ondevice_llm_config_path_label": "Lokasi Model ONNX",
    "module_ondevice_llm_config_path_input_placeholder_text": "Jalur ke Direktori Model",
    "module_ondevice_llm_config_path_input_accessible_description":
        "Kolom input dengan pemilih untuk menentukan jalur ke direktori model tempat berkas ONNX berada.\n"
        "Model yang didukung dalam format ONNX, yang merupakan singkatan dari Open Neural Network Exchange, standar terbuka\n"
        "format untuk model pembelajaran mesin.",

    "module_ondevice_llm_config_response_temperature_label": "Suhu: {temperature}",
    "module_ondevice_llm_config_response_temperature_input_accessible_description":
        "Menyesuaikan keacakan respons model. Nilai yang lebih tinggi menghasilkan output yang lebih bervariasi,\n"
        "sementara nilai yang lebih rendah membuat respons lebih dapat diprediksi.",

    "module_ondevice_llm_config_response_max_tokens_label": "Token Respons Maksimum",
    "module_ondevice_llm_config_response_max_tokens_input_accessible_description":
        "Mengatur jumlah maksimum token yang akan diterima dalam respons, seperti kata dan tanda baca,\n"
        "mengontrol panjang output.",

    "module_ondevice_llm_config_execution_provider_label": "Akselerasi Perangkat Keras",
    "module_ondevice_llm_config_execution_provider_placeholder": "Pilih penyedia",
    "module_ondevice_llm_config_execution_provider_accessible_description":
        "Pilih penyedia akselerasi perangkat keras untuk inferensi model. Opsi meliputi:\n"
        "CPU (bawaan), CUDA (GPU NVIDIA), DirectML (Windows), TensorRT, OpenVINO (Intel), QNN (Qualcomm), CoreML (Apple).\n"
        "Catatan: Penyedia non-CPU memerlukan paket ONNX Runtime khusus (mis., onnxruntime-genai-cuda).",

    "module_ondevice_llm_config_prompt_history_size_label": "Ukuran Riwayat Perintah",
    "module_ondevice_llm_config_prompt_history_size_input_accessible_description":
        "Mengontrol jumlah entri dalam riwayat perintah yang disimpan sistem untuk referensi.\n"
        "Nilai nol memungkinkan entri tak terbatas."
}
