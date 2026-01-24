# Indonesian lexemes common.py
lexemes = {
    "app_title": "Notolog Editor",
    "app_title_with_sub": "{app_title} - {sub_title}",

    "tree_filter_input_placeholder_text": "Filter cepat",
    "tree_filter_input_accessible_desc": "Filter berkas dan direktori berdasarkan nama",
    "tree_filter_clear_button_tooltip": "Hapus filter",
    "tree_filter_clear_button_accessible_name": "Hapus kolom input filter",

    "menu_action_copy_file_path": "Salin jalur berkas",
    "menu_action_rename": "Ubah nama",
    "menu_action_delete": "Hapus",
    "menu_action_delete_completely": "Hapus sepenuhnya",
    "menu_action_restore": "Pulihkan",
    "menu_action_create_new_dir": "Buat direktori baru",

    "dialog_file_rename_title": "Ubah nama berkas",
    "dialog_file_rename_field_label": "Masukkan nama berkas baru",
    "dialog_file_rename_button_ok": "Ubah nama",
    "dialog_file_rename_warning_exists": "Berkas dengan nama yang sama sudah ada",

    "dialog_file_delete_title": "Hapus berkas",
    "dialog_file_delete_text": "Hapus berkas \"{file_name}\"?",
    "dialog_file_delete_completely_title": "Hapus berkas sepenuhnya",
    "dialog_file_delete_completely_text": "Hapus berkas \"{file_name}\" sepenuhnya?",
    "dialog_file_delete_error": "Tidak dapat menghapus berkas, terjadi kesalahan",
    "dialog_file_delete_error_not_found": "Berkas tidak ditemukan",

    "dialog_file_restore_title": "Pulihkan berkas",
    "dialog_file_restore_text": "Pulihkan berkas \"{file_name}\"?",
    "dialog_file_restore_error": "Tidak dapat memulihkan berkas, terjadi kesalahan",
    "dialog_file_restore_warning_exists": "Berkas dengan nama {file_name} sudah ada",

    "dialog_create_new_dir_title": "Buat direktori baru",
    "dialog_create_new_dir_label": "Nama direktori baru",
    "dialog_create_new_dir_input_placeholder_text": "Masukkan nama direktori",
    "dialog_create_new_dir_button_ok": "Buat",
    "dialog_create_new_dir_button_cancel": "Batal",
    "dialog_create_new_dir_warning_empty_title": "Kesalahan nama direktori baru",
    "dialog_create_new_dir_warning_empty_text": "Nama direktori tidak boleh kosong",
    "dialog_create_new_dir_warning_too_long_title": "Kesalahan nama direktori baru",
    "dialog_create_new_dir_warning_too_long_text": "Nama direktori terlalu panjang; maksimal {symbols} karakter diizinkan!",
    "dialog_create_new_dir_error_existed": "Direktori sudah ada",
    "dialog_create_new_dir_error": "Tidak dapat membuat direktori. Pastikan direktori tujuan {base_dir} dapat ditulis",

    "dialog_message_box_title": "Pesan",
    "dialog_message_box_button_ok": "Tutup",

    "action_new_file_first_line_template_text": "Dokumen baru",
    "action_open_file_dialog_caption": "Buka Berkas",
    "action_save_as_file_dialog_caption": "Simpan Berkas",

    "dialog_save_empty_file_title": "Simpan berkas kosong",
    "dialog_save_empty_file_text": "Izinkan menyimpan berkas dengan konten kosong?",

    "dialog_encrypt_file_title": "Enkripsi berkas",
    "dialog_encrypt_file_text": "Enkripsi berkas \"{file_name}\"?",
    "encrypt_file_warning_file_is_already_encrypted": "Berkas sudah dienkripsi!",
    "dialog_encrypt_file_rewrite_existing_title": "Timpa berkas yang ada",
    "dialog_encrypt_file_rewrite_existing_text": "Timpa berkas yang ada \"{file_path}\"?",

    "dialog_decrypt_file_title": "Dekripsi berkas",
    "dialog_decrypt_file_text": "Dekripsi berkas \"{file_name}\"?",
    "decrypt_file_warning_file_is_not_encrypted": "Berkas tidak dienkripsi!",
    "dialog_decrypt_file_rewrite_existing_title": "Timpa berkas yang ada",
    "dialog_decrypt_file_rewrite_existing_text": "Timpa berkas yang ada \"{file_path}\"?",

    "dialog_encrypt_new_password_title": "Kata Sandi Baru",
    "dialog_encrypt_new_password_label": "Kata sandi:",
    "dialog_encrypt_new_password_input_placeholder_text": "Masukkan Kata Sandi Baru",
    "dialog_encrypt_new_password_hint_label": "Petunjuk:",
    "dialog_encrypt_new_password_hint_label_description": "Petunjuk tidak dienkripsi dan dapat dibaca dari berkas!"
                                                          "\nHindari petunjuk yang mudah ditebak, seperti tanggal lahir."
                                                          "\nCobalah menggunakan referensi yang tidak mudah dikaitkan "
                                                          "dengan Anda.",
    "dialog_encrypt_new_password_hint_input_placeholder_text": "Masukkan Petunjuk (Opsional)",
    "dialog_encrypt_new_password_button_ok": "OK",
    "dialog_encrypt_new_password_button_cancel": "Batal",
    "dialog_encrypt_new_password_warning_empty_title": "Peringatan",
    "dialog_encrypt_new_password_warning_empty_text": "Kolom kata sandi tidak boleh kosong!",
    "dialog_encrypt_new_password_warning_too_long_title": "Peringatan",
    "dialog_encrypt_new_password_warning_too_long_text": "Kolom petunjuk terlalu panjang, maksimal {symbols} karakter!",

    "dialog_encrypt_password_title": "Masukkan Kata Sandi",
    "dialog_encrypt_password_label": "Kata sandi:",
    "dialog_encrypt_password_input_placeholder_text": "Masukkan Kata Sandi",
    "dialog_encrypt_password_hint_label": "Petunjuk:",
    "dialog_encrypt_password_button_ok": "OK",
    "dialog_encrypt_password_button_cancel": "Batal",

    "dialog_encrypt_password_reset_title": "Atur Ulang Kata Sandi Enkripsi",
    "dialog_encrypt_password_reset_text": "Apakah Anda yakin ingin mengatur ulang kata sandi enkripsi saat ini?",
    "dialog_encrypt_password_reset_button_cancel": "Batal",
    "dialog_encrypt_password_reset_button_yes": "Ya",

    "dialog_open_link_title": "Tautan",
    "dialog_open_link_text": "Buka tautan \"{url}\" di peramban?",

    "dialog_reset_settings_title": "Atur ulang pengaturan?",
    "dialog_reset_settings_text":
        "Semua data tersimpan dalam pengaturan akan dihapus, dan aplikasi akan dimulai ulang untuk menerapkan perubahan.",

    "dialog_exit_unsaved_title": "Konfirmasi Keluar",
    "dialog_exit_unsaved_text": "Berkas yang dibuka '{file_name}' tidak dapat disimpan. Lanjutkan keluar?",

    "message_app_config_file_access": "Akses ditolak saat mengakses berkas konfigurasi aplikasi di {file_path}. "
        "Atur izin yang benar untuk memastikan operasi yang tepat.",

    "field_dir_path_dialog_caption": "Pilih Direktori",
    "field_file_path_dialog_caption": "Pilih Berkas",

    "dialog_select_default_dir_title": "Pilih Folder Bawaan",
    "dialog_select_default_dir_label": "Pilih folder bawaan untuk catatan",
    "dialog_select_default_dir_input_placeholder_text": "Folder Catatan Bawaan",
    "dialog_select_default_dir_button_ok": "Pilih",
    "dialog_select_default_dir_button_cancel": "Batal",

    "load_file_encryption_password_mismatch": "Kata sandi enkripsi tidak cocok!",
    "load_file_encryption_password_incorrect": "Kata sandi enkripsi salah!",
    "load_file_none_content_error": "Berkas tidak dapat dimuat.",

    "open_dir_permission_error": "Akses ditolak saat mengakses direktori.",
    "open_file_permission_error": "Akses ditolak saat mengakses berkas.",
    "rename_file_permission_error": "Akses ditolak saat mengubah nama berkas.",

    "action_new_file_error_occurred": "Tidak dapat membuat berkas; terjadi kesalahan.\nPeriksa izin sistem berkas.",
    "save_active_file_error_occurred": "Tidak dapat menyimpan berkas; terjadi kesalahan.",

    "expandable_block_default_title": "Info lebih lanjut...",
    "expandable_block_open_close_tags_mismatch_warning": "Ketidakcocokan tag buka/tutup blok <details>",

    "dialog_color_picker_color_copied_to_the_clipboard": "Teks terformat telah disalin ke papan klip",

    "popup_about_title": "Info Aplikasi",
    "popup_about_app_name_description": "Editor Markdown Python",

    "popup_about_version": "Versi",
    "popup_about_license": "Lisensi",
    "popup_about_website": "Situs Web",
    "popup_about_repository": "GitHub",
    "popup_about_pypi": "PyPi",
    "popup_about_date": "Tanggal",

    "update_helper_new_version_is_available": "Versi baru {latest_version} aplikasi tersedia",
    "update_helper_latest_version_installed": "Versi terbaru aplikasi sudah terpasang",

    "network_connection_error_empty": "Tidak dapat memperoleh informasi respons",
    "network_connection_error_connection_or_dns":
        "Host tidak ditemukan. Mungkin ada masalah dengan koneksi internet atau DNS.",
    "network_connection_error_connection_refused":
        "Koneksi ditolak. Server mungkin tidak aktif, atau mungkin ada masalah jaringan.",
    "network_connection_error_connection_timed_out": "Koneksi habis waktu. Mungkin ada masalah jaringan.",
    "network_connection_error_connection_404_error":
        "Kesalahan koneksi 404. Halaman atau sumber daya yang diminta tidak ditemukan.",
    "network_connection_error_generic_with_status_code": "Permintaan gagal dengan kode status: {status_code}",
}
