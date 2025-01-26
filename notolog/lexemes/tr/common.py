# Turkish lexemes common.py
lexemes = {
    "app_title": "Notolog Editörü",
    "app_title_with_sub": "{app_title} - {sub_title}",

    "tree_filter_accessible_desc": "Dosya filtre alanı",

    "menu_action_copy_file_path": "Dosya yolunu kopyala",
    "menu_action_rename": "Yeniden Adlandır",
    "menu_action_delete": "Sil",
    "menu_action_delete_completely": "Tamamen Sil",
    "menu_action_restore": "Geri Yükle",
    "menu_action_create_new_dir": "Yeni dizin oluştur",

    "dialog_file_rename_title": "Dosyayı Yeniden Adlandır",
    "dialog_file_rename_field_label": "Yeni dosya adını girin",
    "dialog_file_rename_button_ok": "Yeniden Adlandır",
    "dialog_file_rename_warning_exists": "Aynı isimde dosya zaten var",

    "dialog_file_delete_title": "Dosyayı Sil",
    "dialog_file_delete_text": "\"{file_name}\" dosyasını sil?",
    "dialog_file_delete_completely_title": "Dosyayı Tamamen Sil",
    "dialog_file_delete_completely_text": "\"{file_name}\" dosyasını tamamen sil?",
    "dialog_file_delete_error": "Dosya silinemedi, hata oluştu",
    "dialog_file_delete_error_not_found": "Dosya bulunamadı",

    "dialog_file_restore_title": "Dosyayı Geri Yükle",
    "dialog_file_restore_text": "\"{file_name}\" dosyasını geri yükle?",
    "dialog_file_restore_error": "Dosya geri yüklenemedi, hata oluştu",
    "dialog_file_restore_warning_exists": "Aynı isimde dosya zaten var",

    "dialog_create_new_dir_title": "Yeni dizin oluştur",
    "dialog_create_new_dir_label": "Yeni dizin adı",
    "dialog_create_new_dir_input_placeholder_text": "Dizin adını girin",
    "dialog_create_new_dir_button_ok": "Oluştur",
    "dialog_create_new_dir_button_cancel": "İptal",
    "dialog_create_new_dir_warning_empty_title": "Yeni dizin adı hatası",
    "dialog_create_new_dir_warning_empty_text": "Dizin adı boş olamaz",
    "dialog_create_new_dir_warning_too_long_title": "Yeni dizin adı hatası",
    "dialog_create_new_dir_warning_too_long_text": "Dizin adı çok uzun; en fazla {symbols} karakter izin verilir!",
    "dialog_create_new_dir_error_existed": "Dizin zaten var",
    "dialog_create_new_dir_error": "Dizin oluşturulamıyor. Hedef dizinin {base_dir} yazılabilir olduğundan emin olun",

    "dialog_message_box_title": "Mesaj",
    "dialog_message_box_button_ok": "Kapat",

    "action_new_file_first_line_template_text": "Yeni belge",
    "action_open_file_dialog_caption": "Dosya Aç",
    "action_save_as_file_dialog_caption": "Dosyayı Farklı Kaydet",

    "dialog_save_empty_file_title": "Boş Dosyayı Kaydet",
    "dialog_save_empty_file_text": "Boş içerikli dosyayı kaydetmeye izin ver?",

    "dialog_encrypt_file_title": "Dosyayı Şifrele",
    "dialog_encrypt_file_text": "\"{file_name}\" dosyasını şifrele?",
    "encrypt_file_warning_file_is_already_encrypted": "Dosya zaten şifrelenmiş!",
    "dialog_encrypt_file_rewrite_existing_title": "Mevcut dosyayı yeniden yaz",
    "dialog_encrypt_file_rewrite_existing_text": "\"{file_path}\" mevcut dosyayı yeniden yaz?",

    "dialog_decrypt_file_title": "Dosyanın Şifresini Çöz",
    "dialog_decrypt_file_text": "\"{file_name}\" dosyasının şifresini çöz?",
    "decrypt_file_warning_file_is_not_encrypted": "Dosya şifreli değil!",
    "dialog_decrypt_file_rewrite_existing_title": "Mevcut dosyayı yeniden yaz",
    "dialog_decrypt_file_rewrite_existing_text": "\"{file_path}\" mevcut dosyayı yeniden yaz?",

    "dialog_encrypt_new_password_title": "Yeni Şifre",
    "dialog_encrypt_new_password_label": "Şifre:",
    "dialog_encrypt_new_password_input_placeholder_text": "Yeni Şifre Girin",
    "dialog_encrypt_new_password_hint_label": "İpucu:",
    "dialog_encrypt_new_password_hint_label_description":
        "İpucu şifrelenmez ve dosyadan okunabilir!"
        "\nKolay tahmin edilebilecek açık ipuçları kullanmayın, örneğin doğum tarihleri gibi."
        "\nKolayca ilişkilendirilemeyecek bir referans kullanın.",
    "dialog_encrypt_new_password_hint_input_placeholder_text": "İpucu Girin (İsteğe Bağlı)",
    "dialog_encrypt_new_password_button_ok": "Tamam",
    "dialog_encrypt_new_password_button_cancel": "İptal",
    "dialog_encrypt_new_password_warning_empty_title": "Uyarı",
    "dialog_encrypt_new_password_warning_empty_text": "Şifre alanı boş olamaz!",
    "dialog_encrypt_new_password_warning_too_long_title": "Uyarı",
    "dialog_encrypt_new_password_warning_too_long_text": "İpucu alanı çok uzun, maksimum {symbols} karakter!",

    "dialog_encrypt_password_title": "Şifre Girin",
    "dialog_encrypt_password_label": "Şifre:",
    "dialog_encrypt_password_input_placeholder_text": "Şifre Girin",
    "dialog_encrypt_password_hint_label": "İpucu:",
    "dialog_encrypt_password_button_ok": "Tamam",
    "dialog_encrypt_password_button_cancel": "İptal",

    "dialog_encrypt_password_reset_title": "Şifreleme Şifresini Sıfırla",
    "dialog_encrypt_password_reset_text": "Mevcut şifreleme şifresini sıfırlamak istediğinizden emin misiniz?",
    "dialog_encrypt_password_reset_button_cancel": "İptal",
    "dialog_encrypt_password_reset_button_yes": "Evet",

    "dialog_open_link_title": "Bağlantı",
    "dialog_open_link_text": "\"{url}\" bağlantısını tarayıcıda aç?",

    "dialog_reset_settings_title": "Ayarları sıfırla?",
    "dialog_reset_settings_text":
        "Ayarlar içinde saklanan tüm veriler silinecek ve uygulama değişiklikleri uygulamak için yeniden başlatılacak.",

    "dialog_exit_unsaved_title": "Çıkışı Onayla",
    "dialog_exit_unsaved_text": "Açık olan dosya '{file_name}' kaydedilemiyor. Çıkışa devam edilsin mi?",

    "message_app_config_file_access": "{file_path} konumundaki uygulama yapılandırma dosyasına erişilirken izin reddedildi. "
                                      "Uygun işleyişi sağlamak için doğru izinleri ayarlayın.",

    "field_dir_path_dialog_caption": "Dizin Seç",
    "field_file_path_dialog_caption": "Dosya Seç",

    "dialog_select_default_dir_title": "Varsayılan Klasörü Seç",
    "dialog_select_default_dir_label": "Notlar için varsayılan klasörü seçin",
    "dialog_select_default_dir_input_placeholder_text": "Varsayılan Notlar Klasörü",
    "dialog_select_default_dir_button_ok": "Seç",
    "dialog_select_default_dir_button_cancel": "İptal",

    "load_file_encryption_password_mismatch": "Şifreleme şifresi eşleşmiyor!",
    "load_file_encryption_password_incorrect": "Hatalı şifreleme şifresi!",
    "load_file_none_content_error": "Dosya yüklenemiyor.",

    "open_dir_permission_error": "Dizine erişim izni reddedildi.",
    "open_file_permission_error": "Dosyaya erişim izni reddedildi.",
    "rename_file_permission_error": "Dosya adı değiştirme izni reddedildi.",

    "action_new_file_error_occurred": "Dosya oluşturulamıyor; bir hata oluştu.\nDosya sistemi izinlerini kontrol edin.",
    "save_active_file_error_occurred": "Dosya kaydedilemiyor; bir hata oluştu.",

    "expandable_block_default_title": "Daha fazla bilgi...",
    "expandable_block_open_close_tags_mismatch_warning": "<details> blok açma/kapama etiketleri uyuşmazlığı",

    "dialog_color_picker_color_copied_to_the_clipboard": "Biçimlendirilmiş metin panoya kopyalandı",

    "popup_about_title": "Uygulama Bilgisi",
    "popup_about_app_name_description": "Python Markdown Editörü",

    "popup_about_version": "Versiyon",
    "popup_about_license": "Lisans",
    "popup_about_website": "Web Sitesi",
    "popup_about_repository": "GitHub",
    "popup_about_pypi": "PyPi",
    "popup_about_date": "Tarih",

    "update_helper_new_version_is_available": "Uygulamanın yeni versiyonu {latest_version} mevcut",
    "update_helper_latest_version_installed": "Uygulamanın en güncel versiyonu yüklü",

    "network_connection_error_empty": "Yanıt bilgisi alınamıyor",
    "network_connection_error_connection_or_dns":
        "Sunucu bulunamadı. İnternet bağlantısında veya DNS'de bir sorun olabilir.",
    "network_connection_error_connection_refused":
        "Bağlantı reddedildi. Sunucu çökmüş olabilir veya ağ sorunları olabilir.",
    "network_connection_error_connection_timed_out": "Bağlantı zaman aşımına uğradı. Ağ sorunları olabilir.",
    "network_connection_error_connection_404_error":
        "404 bağlantı hatası. İstenen sayfa veya kaynak bulunamadı.",
    "network_connection_error_generic_with_status_code": "İstek, {status_code} durum kodu ile başarısız oldu.",
}
