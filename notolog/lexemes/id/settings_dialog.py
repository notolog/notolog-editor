# Indonesian lexemes settings_dialog.py
lexemes = {
    # Settings dialog
    "window_title": "Pengaturan",

    "button_close": "Tutup",

    "tab_general": "Umum",
    "tab_workspace": "Ruang kerja",
    "tab_ai_config": "Konfigurasi AI",

    "general_app_config_label": "Konfigurasi aplikasi",
    "general_app_language_label": "Bahasa",
    "general_app_language_combo_placeholder_text": "Pilih bahasa",
    "general_app_language_combo_accessible_description": "Bahasa antarmuka aplikasi",
    "general_app_theme_label": "Tema",
    "general_app_theme_combo_placeholder_text": "Pilih tema",
    "general_app_theme_combo_accessible_description": "Tema antarmuka aplikasi",
    "general_app_default_path_label": "Folder bawaan untuk catatan",
    "general_app_default_path_input_accessible_description": "Tentukan folder bawaan tempat catatan akan disimpan",
    "general_app_default_path_input_placeholder_text": "Pilih atau masukkan jalur folder",
    "general_app_elements_visibility_label": "Kelola visibilitas elemen",
    "general_app_main_menu_label": "Menu Utama",
    "general_app_main_menu_checkbox": "Tampilkan Menu Utama",
    "general_app_main_menu_checkbox_accessible_description": "Tampilkan menu dropdown utama aplikasi",
    "general_app_font_size_label": "Ukuran Font: {size}pt",
    "general_app_font_size_slider_accessible_description": "Sesuaikan ukuran font global aplikasi",

    "general_file_deletion_label": "Penghapusan berkas",
    "general_reversible_file_deletion_checkbox": "Hapus berkas secara reversibel",
    "general_reversible_file_deletion_checkbox_accessible_description":
        "Pindahkan berkas yang dihapus ke tempat sampah Notolog dengan menambahkan ekstensi .del",

    "workspace_bottom_bar_show_global_cursor_position_checkbox": "Tampilkan Posisi Kursor Global",
    "workspace_bottom_bar_show_global_cursor_position_checkbox_accessible_description":
        "Tampilkan posisi kursor global di bilah status",
    "workspace_bottom_bar_show_navigation_arrows_checkbox": "Tampilkan Panah Navigasi",
    "workspace_bottom_bar_show_navigation_arrows_checkbox_accessible_description":
        "Tampilkan panah navigasi di bilah status.",

    "workspace_editor_mode_label": "Mode editor",
    "workspace_editor_mode_show_line_numbers_checkbox": "Tampilkan Nomor Baris",
    "workspace_editor_mode_show_line_numbers_checkbox_accessible_description": "Tampilkan nomor baris di editor",

    "workspace_view_mode_label": "Mode tampilan",
    "workspace_view_mode_process_emojis_checkbox": "Konversi Emoji Teks ke Grafis",
    "workspace_view_mode_process_emojis_checkbox_accessible_description": "Konversi emoji teks ke representasi grafis",
    "workspace_view_mode_highlight_todos_checkbox": "Sorot TODO",
    "workspace_view_mode_highlight_todos_checkbox_accessible_description": "Tekankan tag TODO dalam teks",
    "workspace_view_mode_open_link_confirmation_checkbox": "Memerlukan Konfirmasi untuk Membuka Tautan",
    "workspace_view_mode_open_link_confirmation_checkbox_accessible_description":
        "Minta konfirmasi sebelum membuka tautan",
    "workspace_view_mode_save_resources_checkbox": "Simpan otomatis gambar eksternal ke disk",
    "workspace_view_mode_save_resources_checkbox_accessible_description":
        "Menyimpan salinan gambar eksternal ke disk secara otomatis untuk akses offline.",

    "ai_config_inference_module_label": "Modul Inferensi",
    "ai_config_inference_module_names_combo_label": "Modul Inferensi Aktif",
    "ai_config_inference_module_names_combo_placeholder_text": "Pilih Modul",
    "ai_config_inference_module_names_combo_accessible_description":
        "Pilih dari modul inferensi AI yang tersedia untuk beroperasi dengan Asisten AI.\n"
        "Opsi termasuk Model Bahasa Besar (LLM) lokal dengan pemrosesan waktu nyata, atau fungsionalitas berbasis API.",

    "ai_config_base_label": "Parameter Dasar",
    "ai_config_multi_turn_dialogue_checkbox": "Dialog multi-giliran dengan memori percakapan",
    "ai_config_multi_turn_dialogue_checkbox_accessible_description":
        "Aktifkan dialog multi-giliran yang mempertahankan perintah sebelumnya untuk memori percakapan.\n"
        "Ketika dimatikan, hanya pesan baru dan perintah sistem yang memengaruhi respons.",
    "ai_config_convert_to_md_checkbox": "Konversi hasil ke Markdown",
    "ai_config_convert_to_md_checkbox_accessible_description": "Konversi pesan keluaran ke format Markdown.",
    "workspace_bottom_bar_label": "Bilah bawah",
    "workspace_bottom_bar_show_system_load_graphs_checkbox": "Tampilkan grafik CPU dan memori",
    "workspace_bottom_bar_show_system_load_graphs_checkbox_accessible_description":
        "Tampilkan grafik penggunaan CPU dan memori beserta pemisahnya di bilah bawah",
    "workspace_bottom_bar_system_load_interval_ms_label": "Interval penyegaran grafik",
    "workspace_bottom_bar_system_load_interval_ms_accessible_description":
        "Atur seberapa sering penggunaan CPU dan memori dibaca, dalam milidetik",
}
