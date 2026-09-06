# Turkish lexemes settings_dialog.py
lexemes = {
    "module_text_to_speech_config_enabled_label": "Metin okumayı etkinleştir",
    "module_text_to_speech_config_setup_label": "Ses kurulumu",
    "module_text_to_speech_config_runtime_label": "Konuşma motoru",
    "module_text_to_speech_config_model_directory_label": "Model klasörü",
    "module_text_to_speech_config_tokenizer_directory_label": "Belirteçleyiciler",
    "module_text_to_speech_config_details_label": "Ayrıntılar",
    "module_text_to_speech_config_model_license_label": "Model lisansı",
    "module_text_to_speech_config_download_models_button": "Modelleri indir",
    "module_text_to_speech_config_verify_models_button": "Modelleri doğrula",
    "module_text_to_speech_config_cancel_button": "İptal",
    "module_text_to_speech_config_stop_button": "Durdur",
    "module_text_to_speech_config_custom_models_label": "Özel model dosyaları",
    "module_text_to_speech_config_reading_label": "Okuma",
    "module_text_to_speech_config_language_label": "Dil",
    "module_text_to_speech_config_voice_label": "Ses",
    "module_text_to_speech_config_speed_label": "Hız",
    "module_text_to_speech_config_announce_headings_label": "Başlıkları duyur",
    "module_text_to_speech_config_skip_inline_code_label": "Satır içi kodu atla",
    "module_text_to_speech_config_skip_multiline_code_label": "Çok satırlı kodu atla",
    "module_text_to_speech_config_test_voice_button": "Sesi dene",
    "module_text_to_speech_config_runtime_input_placeholder_text": "Yürütülebilir dosya seç…",
    "module_text_to_speech_config_model_input_placeholder_text": "Otomatik",
    "module_text_to_speech_config_get_runtime_link": "Motor {version} indir",
    "module_text_to_speech_config_about_label": "{title} hakkında",
    "module_text_to_speech_config_choose_path_label": "{title} seç",
    "module_text_to_speech_config_status_checking_runtime": "Konuşma motoru denetleniyor…",
    "module_text_to_speech_config_status_checking_models": "Önbellek denetleniyor ve eksik modeller indiriliyor…",
    "module_text_to_speech_config_status_models_verified": "Mevcut modeller doğrulandı. Okumaya hazır.",
    "module_text_to_speech_config_status_models_downloaded": "Modeller indirildi ve doğrulandı. Okumaya hazır.",
    "module_text_to_speech_config_status_models_found": "Model dosyaları bulundu. Doğrulayın veya sesi deneyin.",
    "module_text_to_speech_config_status_models_missing": "Model gerekli. Okumaya başlamak için sesi indirin.",
    "module_text_to_speech_config_status_runtime_missing": (
        "Motor gerekli. Bir yürütülebilir dosya seçin veya motoru indirin."
    ),
    "module_text_to_speech_config_status_download_cancelled": (
        "İptal edildi. Tamamlanan indirmeler korundu; yeniden deneyin."
    ),
    "module_text_to_speech_config_error_permission_denied": (
        "İzin reddedildi. Yazılabilir bir model klasörü seçip erişimi denetleyin."
    ),
    "module_text_to_speech_config_error_file_access": "Dosyaya erişilemedi: {error}. Ayrıntılara bakın.",
    "module_text_to_speech_config_progress_elapsed": "{time} geçti",
    "module_text_to_speech_config_progress_files_complete": "{count}/3 dosya tamamlandı",
    "module_text_to_speech_config_progress_downloading": "Dosya {number}/3 · {role} indiriliyor · {size} MiB…",
    "module_text_to_speech_config_progress_cached": "Önbellekte {count}/3 model dosyası doğrulandı…",
    "module_text_to_speech_config_progress_verifying": "Dosya {number}/3 · İndirme doğrulanıyor…",
    "module_text_to_speech_config_download_role_voice": "konuşma modeli",
    "module_text_to_speech_config_download_role_codec": "ses çözücü",
    "module_text_to_speech_config_download_role_tokenizers": "belirteçleyiciler",
    "module_text_to_speech_config_download_role_model": "model",
    "module_text_to_speech_config_runtime_required": "Önce bir konuşma motoru seçin.",
    "module_text_to_speech_config_models_required": "Önce modelleri indirin.",
    "module_text_to_speech_config_enable_required": "Önce metin okumayı etkinleştirin.",
    "module_text_to_speech_config_status_testing_voice": "Modeller yükleniyor ve deneme sesi hazırlanıyor…",
    "module_text_to_speech_config_details_accessible_description": "İşlem günlüğünü göster veya gizle",
    "module_text_to_speech_config_setup_accessible_description": (
        "NeMo-Speech.cpp seçin; MagpieTTS, NanoCodec ve belirteçleyicileri indirin. Modellerin ayrı "
        "lisansı vardır."
    ),
    "module_text_to_speech_config_runtime_input_accessible_description": (
        "NeMo-Speech.cpp 0.1.0 gereklidir. Arşivi açıp bin/nemo-speech (Windows: bin/nemo-speech.exe) "
        "seçin."
    ),
    "module_text_to_speech_config_model_directory_input_accessible_description": (
        "Modeller buraya indirilir. Mevcut dosyalar doğrulanıp yeniden kullanılır. curl ve yaklaşık 550 "
        "MB gerekir."
    ),
    "module_text_to_speech_config_custom_models_accessible_description": (
        "Model yollarını değiştirin veya model klasörünü kullanmak için alanları temizleyin."
    ),
    "module_text_to_speech_config_reading_accessible_description": (
        "Ses, dil ve hızı seçin. Kod yerine kısa bir sesli etiket okunabilir."
    ),
    "module_text_to_speech_config_language_input_accessible_description": (
        "Belgenin dilini seçin; otomatik algılanmaz. Varsayılan İngilizcedir. Mandarin ve Japonca için "
        "bu dilleri destekleyen motor gerekir."
    ),
    "module_text_to_speech_config_voice_input_accessible_description": (
        "MagpieTTS sesleri: John, Sofia, Aria, Jason ve Leo."
    ),
    "module_text_to_speech_config_speed_input_accessible_description": "Oynatma hızı sesin perdesini de değiştirir.",
    "module_text_to_speech_config_announce_headings_accessible_description": (
        "Markdown ve HTML başlıklarının 1–4 düzeyleri için Chapter, Section, Subsection ve "
        "Sub-subsection; ardından Heading level 5–6 söylenir."
    ),
    "module_text_to_speech_config_skip_inline_code_accessible_description": (
        "İşaretli: “Inline code block” der. Değilse satır içi kod okunur. Çevrili veya girintili kod çok"
        " satırlı ayarı kullanır."
    ),
    "module_text_to_speech_config_skip_multiline_code_accessible_description": (
        "İşaretli: “Multiline code block” der. Değilse çevrili ve girintili kod okunur."
    ),
    "module_text_to_speech_config_verify_models_accessible_description": (
        "Mevcut dosyaları doğrula, eksik veya bozuk olanları indir."
    ),
    "module_text_to_speech_config_editor_required": "Sesi denemek için bu ayarları düzenleyiciden açın.",
    "module_text_to_speech_config_context_length_label": "Bağlam uzunluğu",
    "module_text_to_speech_config_context_whole_document": "Tüm belge",
    "module_text_to_speech_config_context_characters": "{count} karakter",
    "module_text_to_speech_config_context_length_accessible_description": (
        "Konuşma isteği başına en fazla karakter. En sağ: başlık araları korunarak tüm belge. Büyük "
        "bağlamlar daha geç başlar ve daha fazla bellek kullanır. Motor sınırları geçerlidir."
    ),
    "module_text_to_speech_config_cancel_download_title": "İndirme iptal edilsin mi?",
    "module_text_to_speech_config_cancel_download_confirmation": (
        "Ayarları kapatmak indirmeyi iptal eder. Tamamlanan dosyalar korunur. Ayarlar kapatılsın mı?"
    ),
    "module_text_to_speech_config_status_custom_models": (
        "Özel model dosyaları seçili. İndirmeler model klasörünü kullanır."
    ),
}
