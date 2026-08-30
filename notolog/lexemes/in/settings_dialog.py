# Hindi lexemes settings_dialog.py
lexemes = {
    # सेटिंग्स संवाद
    "window_title": "सेटिंग्स",

    "button_close": "बंद करें",

    "tab_general": "सामान्य",
    "tab_workspace": "कार्यक्षेत्र",
    "tab_ai_config": "एआई कॉन्फ़िग",

    "general_app_config_label": "एप्लिकेशन कॉन्फ़िग",
    "general_app_language_label": "भाषा",
    "general_app_language_combo_placeholder_text": "एक भाषा चुनें",
    "general_app_language_combo_accessible_description": "एप्लिकेशन की इंटरफ़ेस भाषा",
    "general_app_theme_label": "थीम",
    "general_app_theme_combo_placeholder_text": "एक थीम चुनें",
    "general_app_theme_combo_accessible_description": "एप्लिकेशन की इंटरफ़ेस थीम",
    "general_app_default_path_label": "नोट्स के लिए डिफ़ॉल्ट फ़ोल्डर",
    "general_app_default_path_input_accessible_description": "डिफ़ॉल्ट फ़ोल्डर निर्दिष्ट करें जहाँ नोट्स सहेजे जाएंगे",
    "general_app_default_path_input_placeholder_text": "फ़ोल्डर पथ चुनें या दर्ज करें",
    "general_app_elements_visibility_label": "तत्वों की दृश्यता प्रबंधित करें",
    "general_app_main_menu_label": "मुख्य मेनू",
    "general_app_main_menu_checkbox": "मुख्य मेनू दिखाएं",
    "general_app_main_menu_checkbox_accessible_description": "ऐप का मुख्य ड्रॉपडाउन मेनू दिखाएं",
    "general_app_font_size_label": "फ़ॉन्ट आकार: {size} पीटी",
    "general_app_font_size_slider_accessible_description": "ऐप का वैश्विक फ़ॉन्ट आकार समायोजित करें",

    "general_file_deletion_label": "फ़ाइल हटाना",
    "general_reversible_file_deletion_checkbox": "फ़ाइलों को पुनर्स्थापित करने योग्य तरीके से हटाएँ",
    "general_reversible_file_deletion_checkbox_accessible_description":
        ".del एक्सटेंशन जोड़कर हटाई गई फ़ाइलों को Notolog की टोकरी में ले जाएँ",

    "workspace_bottom_bar_show_global_cursor_position_checkbox": "ग्लोबल कर्सर स्थिति दिखाएं",
    "workspace_bottom_bar_show_global_cursor_position_checkbox_accessible_description":
        "स्थिति पट्टी में ग्लोबल कर्सर स्थिति दिखाएं",
    "workspace_bottom_bar_show_navigation_arrows_checkbox": "नेविगेशन तीर दिखाएं",
    "workspace_bottom_bar_show_navigation_arrows_checkbox_accessible_description": "स्टेटस बार में नेविगेशन तीर दिखाएं",

    "workspace_editor_mode_label": "संपादक मोड",
    "workspace_editor_mode_show_line_numbers_checkbox": "लाइन संख्याएँ दिखाएं",
    "workspace_editor_mode_show_line_numbers_checkbox_accessible_description": "संपादक में लाइन संख्याएँ दिखाएं",

    "workspace_view_mode_label": "दृश्य मोड",
    "workspace_view_mode_process_emojis_checkbox": "पाठ इमोजी को ग्राफिक में परिवर्तित करें",
    "workspace_view_mode_process_emojis_checkbox_accessible_description": "पाठ इमोजी को चित्रित प्रतिनिधि में परिवर्तित करें",
    "workspace_view_mode_highlight_todos_checkbox": "TODO को हाइलाइट करें",
    "workspace_view_mode_highlight_todos_checkbox_accessible_description": "पाठ में TODO टैग को महत्वपूर्ण बनाएं",
    "workspace_view_mode_open_link_confirmation_checkbox": "लिंक खोलने के लिए पुष्टि की आवश्यकता",
    "workspace_view_mode_open_link_confirmation_checkbox_accessible_description":
        "लिंक खोलने से पहले पुष्टि की आवश्यकता है",
    "workspace_view_mode_save_resources_checkbox": "बाहरी छवियों को डिस्क में स्वचालित रूप से सहेजें",
    "workspace_view_mode_save_resources_checkbox_accessible_description":
        "ऑफ़लाइन पहुंच के लिए बाहरी छवियों की स्वचालित प्रतिलिपियाँ डिस्क में सहेजें।",

    "ai_config_inference_module_label": "अनुमान मॉड्यूल",
    "ai_config_inference_module_names_combo_label": "सक्रिय अनुमान मॉड्यूल",
    "ai_config_inference_module_names_combo_placeholder_text": "मॉड्यूल चुनें",
    "ai_config_inference_module_names_combo_accessible_description":
        "AI सहायक के साथ संचालन के लिए उपलब्ध AI अनुमान मॉड्यूलों में से चुनें।\n"
        "विकल्पों में वास्तविक समय प्रसंस्करण के साथ बड़े भाषा मॉडल (LLM) या API-आधारित कार्यक्षमताएं शामिल हैं।",

    "ai_config_base_label": "मूल पैरामीटर",
    "ai_config_multi_turn_dialogue_checkbox": "संवादी स्मृति के साथ मल्टी-टर्न संवाद",
    "ai_config_multi_turn_dialogue_checkbox_accessible_description":
        "संवादी स्मृति के लिए अंतिम संकेत को बनाए रखने वाला मल्टी-टर्न संवाद सक्षम करें।\n"
        "बंद होने पर, केवल नया संदेश और सिस्टम प्रॉम्प्ट प्रतिक्रिया को प्रभावित करते हैं।",
    "ai_config_convert_to_md_checkbox": "परिणाम को Markdown में बदलें",
    "ai_config_convert_to_md_checkbox_accessible_description":
        "आउटपुट संदेश को Markdown प्रारूप में बदलें।",
    "workspace_bottom_bar_label": "निचली पट्टी",
    "workspace_bottom_bar_show_system_load_graphs_checkbox": "CPU और मेमोरी ग्राफ दिखाएं",
    "workspace_bottom_bar_show_system_load_graphs_checkbox_accessible_description":
        "निचली पट्टी में CPU और मेमोरी उपयोग ग्राफ और उनका विभाजक दिखाएं",
    "workspace_bottom_bar_system_load_interval_ms_label": "ग्राफ़ रीफ़्रेश अंतराल",
    "workspace_bottom_bar_system_load_interval_ms_accessible_description":
        "CPU और मेमोरी उपयोग पढ़ने का अंतराल मिलीसेकंड में सेट करें",
}
