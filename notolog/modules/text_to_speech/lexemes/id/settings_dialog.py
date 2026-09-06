# Indonesian lexemes settings_dialog.py
lexemes = {
    "module_text_to_speech_config_enabled_label": "Aktifkan Teks ke Ucapan",
    "module_text_to_speech_config_setup_label": "Pengaturan suara",
    "module_text_to_speech_config_runtime_label": "Mesin ucapan",
    "module_text_to_speech_config_model_directory_label": "Folder model",
    "module_text_to_speech_config_tokenizer_directory_label": "Tokenizer",
    "module_text_to_speech_config_details_label": "Detail",
    "module_text_to_speech_config_model_license_label": "Lisensi model",
    "module_text_to_speech_config_download_models_button": "Unduh model",
    "module_text_to_speech_config_verify_models_button": "Verifikasi model",
    "module_text_to_speech_config_cancel_button": "Batal",
    "module_text_to_speech_config_stop_button": "Hentikan",
    "module_text_to_speech_config_custom_models_label": "File model khusus",
    "module_text_to_speech_config_reading_label": "Pembacaan",
    "module_text_to_speech_config_language_label": "Bahasa",
    "module_text_to_speech_config_voice_label": "Suara",
    "module_text_to_speech_config_speed_label": "Kecepatan",
    "module_text_to_speech_config_announce_headings_label": "Sebutkan judul",
    "module_text_to_speech_config_skip_inline_code_label": "Lewati kode sebaris",
    "module_text_to_speech_config_skip_multiline_code_label": "Lewati kode multibaris",
    "module_text_to_speech_config_test_voice_button": "Uji suara",
    "module_text_to_speech_config_runtime_input_placeholder_text": "Pilih berkas program…",
    "module_text_to_speech_config_model_input_placeholder_text": "Otomatis",
    "module_text_to_speech_config_get_runtime_link": "Dapatkan mesin {version}",
    "module_text_to_speech_config_about_label": "Tentang {title}",
    "module_text_to_speech_config_choose_path_label": "Pilih {title}",
    "module_text_to_speech_config_status_checking_runtime": "Memeriksa mesin ucapan…",
    "module_text_to_speech_config_status_checking_models": "Memeriksa cache dan mengunduh model yang belum ada…",
    "module_text_to_speech_config_status_models_verified": "Model yang ada telah diverifikasi. Siap membaca.",
    "module_text_to_speech_config_status_models_downloaded": "Model diunduh dan diverifikasi. Siap membaca.",
    "module_text_to_speech_config_status_models_found": "File model ditemukan. Verifikasi atau uji suara.",
    "module_text_to_speech_config_status_models_missing": "Model diperlukan. Unduh suara untuk mulai membaca.",
    "module_text_to_speech_config_status_runtime_missing": (
        "Mesin diperlukan. Pilih berkas program atau dapatkan mesin."
    ),
    "module_text_to_speech_config_status_download_cancelled": "Dibatalkan. Unduhan selesai disimpan; coba lagi.",
    "module_text_to_speech_config_error_permission_denied": (
        "Izin ditolak. Pilih folder model yang dapat ditulisi dan periksa akses."
    ),
    "module_text_to_speech_config_error_file_access": "Akses file gagal: {error}. Lihat Detail.",
    "module_text_to_speech_config_progress_elapsed": "{time} berlalu",
    "module_text_to_speech_config_progress_files_complete": "{count}/3 file selesai",
    "module_text_to_speech_config_progress_downloading": "File {number}/3 · Mengunduh {role} · {size} MiB…",
    "module_text_to_speech_config_progress_cached": "{count}/3 file model diverifikasi di cache…",
    "module_text_to_speech_config_progress_verifying": "File {number}/3 · Memverifikasi unduhan…",
    "module_text_to_speech_config_download_role_voice": "model ucapan",
    "module_text_to_speech_config_download_role_codec": "dekoder audio",
    "module_text_to_speech_config_download_role_tokenizers": "tokenizer",
    "module_text_to_speech_config_download_role_model": "model",
    "module_text_to_speech_config_runtime_required": "Pilih mesin ucapan terlebih dahulu.",
    "module_text_to_speech_config_models_required": "Unduh model terlebih dahulu.",
    "module_text_to_speech_config_enable_required": "Aktifkan Teks ke Ucapan terlebih dahulu.",
    "module_text_to_speech_config_status_testing_voice": "Memuat model dan menyiapkan suara uji…",
    "module_text_to_speech_config_details_accessible_description": "Tampilkan atau sembunyikan log operasi",
    "module_text_to_speech_config_setup_accessible_description": (
        "Pilih NeMo-Speech.cpp lalu unduh MagpieTTS, NanoCodec, dan tokenizer. Model memiliki lisensi "
        "tersendiri."
    ),
    "module_text_to_speech_config_runtime_input_accessible_description": (
        "Memerlukan NeMo-Speech.cpp 0.1.0. Ekstrak arsip dan pilih bin/nemo-speech (bin/nemo-speech.exe "
        "di Windows)."
    ),
    "module_text_to_speech_config_model_directory_input_accessible_description": (
        "Model diunduh di sini. File yang ada diverifikasi dan digunakan kembali. Memerlukan curl dan "
        "ruang sekitar 550 MB."
    ),
    "module_text_to_speech_config_custom_models_accessible_description": (
        "Ganti jalur model atau kosongkan kolom untuk memakai folder model."
    ),
    "module_text_to_speech_config_reading_accessible_description": (
        "Pilih suara, bahasa, dan kecepatan. Kode dapat diganti dengan label ucapan singkat."
    ),
    "module_text_to_speech_config_language_input_accessible_description": (
        "Pilih bahasa dokumen; tidak dideteksi otomatis. Bawaan: Inggris. Mandarin dan Jepang memerlukan"
        " mesin yang mendukung bahasa tersebut."
    ),
    "module_text_to_speech_config_voice_input_accessible_description": (
        "Suara MagpieTTS: John, Sofia, Aria, Jason, dan Leo."
    ),
    "module_text_to_speech_config_speed_input_accessible_description": "Kecepatan pemutaran juga mengubah nada suara.",
    "module_text_to_speech_config_announce_headings_accessible_description": (
        "Menyebut Chapter, Section, Subsection, dan Sub-subsection untuk judul Markdown dan HTML tingkat"
        " 1–4, lalu Heading level 5–6."
    ),
    "module_text_to_speech_config_skip_inline_code_accessible_description": (
        "Dicentang: menyebut “Inline code block”. Jika tidak: membaca kode sebaris. Kode berpagar atau "
        "berindentasi memakai pengaturan multibaris."
    ),
    "module_text_to_speech_config_skip_multiline_code_accessible_description": (
        "Dicentang: menyebut “Multiline code block”. Jika tidak: membaca kode berpagar atau "
        "berindentasi."
    ),
    "module_text_to_speech_config_verify_models_accessible_description": (
        "Verifikasi file yang ada dan unduh file yang hilang atau rusak."
    ),
    "module_text_to_speech_config_editor_required": "Buka pengaturan ini dari editor untuk menguji suara.",
    "module_text_to_speech_config_context_length_label": "Panjang konteks",
    "module_text_to_speech_config_context_whole_document": "Seluruh dokumen",
    "module_text_to_speech_config_context_characters": "{count} karakter",
    "module_text_to_speech_config_context_length_accessible_description": (
        "Jumlah karakter maksimum per permintaan ucapan. Paling kanan: seluruh dokumen dengan jeda "
        "judul. Konteks lebih besar lebih lambat dimulai dan memakai lebih banyak memori. Batas mesin "
        "tetap berlaku."
    ),
    "module_text_to_speech_config_cancel_download_title": "Batalkan unduhan?",
    "module_text_to_speech_config_cancel_download_confirmation": (
        "Menutup pengaturan membatalkan unduhan. Berkas yang selesai tetap disimpan. Tutup pengaturan?"
    ),
    "module_text_to_speech_config_status_custom_models": (
        "Berkas model khusus dipilih. Unduhan menggunakan folder model."
    ),
}
