# Turkish lexemes settings_dialog.py
lexemes = {
    "tab_ondevice_llm_config": "Cihazda LLM",

    "module_ondevice_llm_config_label": "Cihazda LLM Modeli",
    "module_ondevice_llm_config_path_label": "ONNX Model Konumu",
    "module_ondevice_llm_config_path_input_placeholder_text": "Model dizinine yol",
    "module_ondevice_llm_config_path_input_accessible_description":
        "ONNX dosyalarının bulunduğu model dizinine yol belirtmek için bir seçiciye sahip giriş alanı.\n"
        "Desteklenen modeller ONNX formatındadır, bu da Açık Sinir Ağı Değişimini temsil eder, açık standart\n"
        "makine öğrenimi modelleri formatıdır.",

    "module_ondevice_llm_config_response_temperature_label": "Sıcaklık: {temperature}",
    "module_ondevice_llm_config_response_temperature_input_accessible_description":
        "Modelin yanıtlarının rastgeleliğini ayarlar. Daha yüksek değerler daha çeşitli çıktılar üretir,\n"
        "daha düşük değerler ise yanıtları daha tahmin edilebilir kılar.",

    "module_ondevice_llm_config_response_max_tokens_label": "Maksimum Yanıt Token'ları",
    "module_ondevice_llm_config_response_max_tokens_input_accessible_description":
        "Bir yanıtta alınabilecek maksimum token sayısını belirler, bu da kelimeler ve noktalama işaretlerini içerir,\n"
        "çıktının uzunluğunu kontrol eder.",

    "module_ondevice_llm_config_execution_provider_label": "Donanım Hızlandırma",
    "module_ondevice_llm_config_execution_provider_placeholder": "Sağlayıcı seçin",
    "module_ondevice_llm_config_execution_provider_accessible_description":
        "Model çıkarımı için donanım hızlandırma sağlayıcısını seçin. Seçenekler:\n"
        "CPU (varsayılan), CUDA (NVIDIA GPU), DirectML (Windows), TensorRT, OpenVINO (Intel), "
        "QNN (Qualcomm), CoreML (Apple).\n"
        "Not: CPU dışı sağlayıcılar özel ONNX Runtime paketleri gerektirir "
        "(örn: onnxruntime-genai-cuda).",

    "module_ondevice_llm_config_prompt_history_size_label": "Komut Geçmişi Boyutu",
    "module_ondevice_llm_config_prompt_history_size_input_accessible_description":
        "Sistem tarafından referans için tutulan komut geçmişindeki giriş sayısını kontrol eder.\n"
        "Sıfır değer sınırsız girişe izin verir."
}
