# Hindi lexemes common.py
lexemes = {
    "app_title": "नोटोलॉग एडिटर",
    "app_title_with_sub": "{app_title} - {sub_title}",

    "tree_filter_input_placeholder_text": "त्वरित फ़िल्टर",
    "tree_filter_input_accessible_desc": "फ़ाइलों और निर्देशिकाओं को नाम से फ़िल्टर करें",

    "menu_action_copy_file_path": "फ़ाइल पथ की प्रतिलिपि बनाएँ",
    "menu_action_rename": "नाम बदलें",
    "menu_action_delete": "हटाएं",
    "menu_action_delete_completely": "पूरी तरह से हटाएं",
    "menu_action_restore": "पुनर्स्थापित करें",
    "menu_action_create_new_dir": "नई निर्देशिका बनाएँ",

    "dialog_file_rename_title": "फ़ाइल का नाम बदलें",
    "dialog_file_rename_field_label": "नया फ़ाइल नाम दर्ज करें",
    "dialog_file_rename_button_ok": "नाम बदलें",
    "dialog_file_rename_warning_exists": "इसी नाम की फ़ाइल पहले से मौजूद है",

    "dialog_file_delete_title": "फ़ाइल हटाएं",
    "dialog_file_delete_text": "क्या आप वाकई फ़ाइल \"{file_name}\" को हटाना चाहते हैं?",
    "dialog_file_delete_completely_title": "फ़ाइल को पूरी तरह से हटाएं",
    "dialog_file_delete_completely_text": "क्या आप वाकई फ़ाइल \"{file_name}\" को पूरी तरह से हटाना चाहते हैं?",
    "dialog_file_delete_error": "फ़ाइल हटाने में असमर्थ, त्रुटि हुई है",
    "dialog_file_delete_error_not_found": "फ़ाइल नहीं मिली",

    "dialog_file_restore_title": "फ़ाइल पुनर्स्थापित करें",
    "dialog_file_restore_text": "क्या आप वाकई फ़ाइल \"{file_name}\" को पुनर्स्थापित करना चाहते हैं?",
    "dialog_file_restore_error": "फ़ाइल को पुनर्स्थापित करने में असमर्थ, त्रुटि हुई है",
    "dialog_file_restore_warning_exists": "इस नाम की फ़ाइल पहले से मौजूद है",

    "dialog_create_new_dir_title": "नई निर्देशिका बनाएँ",
    "dialog_create_new_dir_label": "नई निर्देशिका का नाम",
    "dialog_create_new_dir_input_placeholder_text": "निर्देशिका नाम दर्ज करें",
    "dialog_create_new_dir_button_ok": "बनाएँ",
    "dialog_create_new_dir_button_cancel": "रद्द करें",
    "dialog_create_new_dir_warning_empty_title": "नई निर्देशिका नाम त्रुटि",
    "dialog_create_new_dir_warning_empty_text": "निर्देशिका नाम खाली नहीं हो सकता",
    "dialog_create_new_dir_warning_too_long_title": "नई निर्देशिका नाम त्रुटि",
    "dialog_create_new_dir_warning_too_long_text": "निर्देशिका का नाम बहुत लंबा है; अधिकतम "
                                                   "{symbols} वर्णों की अनुमति है!",
    "dialog_create_new_dir_error_existed": "निर्देशिका पहले से मौजूद है",
    "dialog_create_new_dir_error": "निर्देशिका नहीं बनाई जा सकती। सुनिश्चित करें कि गंतव्य निर्देशिका "
                                   "{base_dir} लिखने योग्य है",

    "dialog_message_box_title": "संदेश",
    "dialog_message_box_button_ok": "बंद करें",

    "action_new_file_first_line_template_text": "नया दस्तावेज़",
    "action_open_file_dialog_caption": "फ़ाइल खोलें",
    "action_save_as_file_dialog_caption": "फ़ाइल सहेजें",

    "dialog_save_empty_file_title": "खाली फ़ाइल सहेजें",
    "dialog_save_empty_file_text": "क्या खाली सामग्री के साथ फ़ाइल को सहेजने की अनुमति दें?",

    "dialog_encrypt_file_title": "फ़ाइल एन्क्रिप्ट करें",
    "dialog_encrypt_file_text": "क्या आप वाकई फ़ाइल \"{file_name}\" को एन्क्रिप्ट करना चाहते हैं?",
    "encrypt_file_warning_file_is_already_encrypted": "फ़ाइल पहले से ही एन्क्रिप्टेड है!",
    "dialog_encrypt_file_rewrite_existing_title": "मौजूदा फ़ाइल को पुनः लिखें",
    "dialog_encrypt_file_rewrite_existing_text": "क्या आप वाकई मौजूदा फ़ाइल \"{file_path}\" को पुनः लिखना चाहते हैं?",

    "dialog_decrypt_file_title": "फ़ाइल डिक्रिप्ट करें",
    "dialog_decrypt_file_text": "क्या आप वाकई फ़ाइल \"{file_name}\" को डिक्रिप्ट करना चाहते हैं?",
    "decrypt_file_warning_file_is_not_encrypted": "फ़ाइल एन्क्रिप्टेड नहीं है!",
    "dialog_decrypt_file_rewrite_existing_title": "मौजूदा फ़ाइल को पुनः लिखें",
    "dialog_decrypt_file_rewrite_existing_text": "क्या आप वाकई मौजूदा फ़ाइल \"{file_path}\" को पुनः लिखना चाहते हैं?",

    "dialog_encrypt_new_password_title": "नया पासवर्ड",
    "dialog_encrypt_new_password_label": "पासवर्ड:",
    "dialog_encrypt_new_password_input_placeholder_text": "नया पासवर्ड दर्ज करें",
    "dialog_encrypt_new_password_hint_label": "संकेत:",
    "dialog_encrypt_new_password_hint_label_description": "संकेत एन्क्रिप्टेड नहीं होता है और फ़ाइल से पढ़ा जा सकता है!"
                                                          "\nजन्म तिथियों जैसे आसानी से अनुमान लगाए जा सकने वाले "
                                                          "स्पष्ट संकेतों से बचें।\nआपके साथ आसानी से जुड़े नहीं जा "
                                                          "सकने वाले संदर्भ का प्रयोग करने का प्रयास करें।",
    "dialog_encrypt_new_password_hint_input_placeholder_text": "संकेत दर्ज करें (वैकल्पिक)",
    "dialog_encrypt_new_password_button_ok": "ठीक है",
    "dialog_encrypt_new_password_button_cancel": "रद्द करें",
    "dialog_encrypt_new_password_warning_empty_title": "चेतावनी",
    "dialog_encrypt_new_password_warning_empty_text": "पासवर्ड फ़ील्ड खाली नहीं हो सकती!",
    "dialog_encrypt_new_password_warning_too_long_title": "चेतावनी",
    "dialog_encrypt_new_password_warning_too_long_text": "संकेत फ़ील्ड बहुत लंबी है, अधिकतम {symbols} अक्षर!",

    "dialog_encrypt_password_title": "पासवर्ड दर्ज करें",
    "dialog_encrypt_password_label": "पासवर्ड:",
    "dialog_encrypt_password_input_placeholder_text": "पासवर्ड दर्ज करें",
    "dialog_encrypt_password_hint_label": "संकेत:",
    "dialog_encrypt_password_button_ok": "ठीक है",
    "dialog_encrypt_password_button_cancel": "रद्द करें",

    "dialog_encrypt_password_reset_title": "एन्क्रिप्शन पासवर्ड रीसेट करें",
    "dialog_encrypt_password_reset_text": "क्या आप वाकई मौजूदा एन्क्रिप्शन पासवर्ड को रीसेट करना चाहते हैं?",
    "dialog_encrypt_password_reset_button_cancel": "रद्द करें",
    "dialog_encrypt_password_reset_button_yes": "हाँ",

    "dialog_open_link_title": "लिंक",
    "dialog_open_link_text": "लिंक \"{url}\" को ब्राउज़र में खोलें?",

    "dialog_reset_settings_title": "सेटिंग्स रीसेट करें?",
    "dialog_reset_settings_text":
        "सेटिंग्स में संग्रहीत सभी डेटा मिटाया जाएगा, और एप्लिकेशन परिवर्तन लागू करने के लिए पुनः आरंभ होगा।",

    "dialog_exit_unsaved_title": "बाहर जाने की पुष्टि करें",
    "dialog_exit_unsaved_text": "खुली हुई फ़ाइल '{file_name}' को सहेजा नहीं जा सकता। क्या बाहर जाना जारी रखें?",

    "message_app_config_file_access": "{file_path} पर ऐप कॉन्फ़िगरेशन फ़ाइल तक पहुँचते समय अनुमति अस्वीकृत। सही "
                                      "ऑपरेशन सुनिश्चित करने के लिए सही अनुमतियाँ सेट करें।",

    "field_dir_path_dialog_caption": "डायरेक्टरी चुनें",
    "field_file_path_dialog_caption": "फ़ाइल चुनें",

    "dialog_select_default_dir_title": "डिफ़ॉल्ट फ़ोल्डर चुनें",
    "dialog_select_default_dir_label": "नोट्स के लिए डिफ़ॉल्ट फ़ोल्डर चुनें",
    "dialog_select_default_dir_input_placeholder_text": "डिफ़ॉल्ट नोट्स फ़ोल्डर",
    "dialog_select_default_dir_button_ok": "चुनें",
    "dialog_select_default_dir_button_cancel": "रद्द करें",

    "load_file_encryption_password_mismatch": "एन्क्रिप्शन पासवर्ड मेल नहीं खा रहा!",
    "load_file_encryption_password_incorrect": "गलत एन्क्रिप्शन पासवर्ड!",
    "load_file_none_content_error": "फ़ाइल लोड नहीं की जा सकती।",

    "open_dir_permission_error": "डायरेक्टरी तक पहुंच की अनुमति अस्वीकृत।",
    "open_file_permission_error": "फ़ाइल तक पहुंचने की अनुमति अस्वीकृत।",
    "rename_file_permission_error": "फ़ाइल का नाम बदलने की अनुमति अस्वीकृत।",

    "action_new_file_error_occurred": "फ़ाइल नहीं बनाई जा सकती; एक त्रुटि हुई।\nफ़ाइल सिस्टम अनुमतियों की जाँच करें।",
    "save_active_file_error_occurred": "फ़ाइल सहेज नहीं सकते; एक त्रुटि हुई।",

    "expandable_block_default_title": "अधिक जानकारी...",
    "expandable_block_open_close_tags_mismatch_warning": "<details> ब्लॉक ओपन/क्लोज टैग मेल नहीं खाते",

    "dialog_color_picker_color_copied_to_the_clipboard": "स्वरूपित पाठ क्लिपबोर्ड में कॉपी किया गया है",

    "popup_about_title": "एप्लिकेशन की जानकारी",
    "popup_about_app_name_description": "पायथन मार्कडाउन एडिटर",

    "popup_about_version": "संस्करण",
    "popup_about_license": "लाइसेंस",
    "popup_about_website": "वेबसाइट",
    "popup_about_repository": "गिटहब",
    "popup_about_pypi": "पाइपी",
    "popup_about_date": "तारीख",

    "update_helper_new_version_is_available": "ऐप का नया संस्करण {latest_version} उपलब्ध है",
    "update_helper_latest_version_installed": "ऐप का नवीनतम संस्करण स्थापित है",

    "network_connection_error_empty": "प्रतिक्रिया जानकारी प्राप्त करने में असमर्थ",
    "network_connection_error_connection_or_dns": "होस्ट नहीं मिला। इंटरनेट कनेक्शन या DNS में समस्या हो सकती है।",
    "network_connection_error_connection_refused":
        "कनेक्शन अस्वीकृत किया गया। सर्वर बंद हो सकता है, या नेटवर्क में समस्या हो सकती है।",
    "network_connection_error_connection_timed_out": "कनेक्शन का समय समाप्त हो गया। नेटवर्क में समस्या हो सकती है।",
    "network_connection_error_connection_404_error": "कनेक्शन 404 त्रुटि। अनुरोधित पृष्ठ या संसाधन नहीं मिला।",
    "network_connection_error_generic_with_status_code": "स्थिति कोड के साथ अनुरोध विफल: {status_code}"
}
