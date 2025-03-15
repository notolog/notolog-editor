# Hindi lexemes settings_dialog.py
lexemes = {
    "tab_module_llama_cpp_config": "मॉड्यूल llama.cpp",

    "module_llama_cpp_config_label": "मॉड्यूल llama.cpp",
    "module_llama_cpp_config_path_label": "मॉडल स्थान",
    "module_llama_cpp_config_path_input_placeholder_text": "मॉडल पथ का चयन करें या दर्ज करें",
    "module_llama_cpp_config_path_input_accessible_description":
        "एक इनपुट फ़ील्ड जिसमें सेलेक्टर होता है ताकि स्थानीय मॉडल के पथ को निर्दिष्ट किया जा सके।\n"
        "GGUF प्रारूप में मॉडलों का समर्थन करता है, जो GGML और GGML आधारित एक्जीक्यूटर्स के साथ\n"
        "उपयोग किए जाने वाले मॉडलों को संग्रहीत करने के लिए अनुकूलित एक बाइनरी फ़ाइल प्रारूप है।",

    "module_llama_cpp_config_path_input_filter_text": "GGUF फ़ाइलें",

    "module_llama_cpp_config_context_window_label": "संदर्भ विंडो आकार",
    "module_llama_cpp_config_context_window_input_accessible_description":
        "वह संख्या निर्धारित करता है जिसे मॉडल प्रतिक्रियाएं उत्पन्न करने के लिए विचार में रखता है। यह\n"
        "नियंत्रित करता है कि कितना पूर्व संदर्भ प्रयुक्त होता है।",

    "module_llama_cpp_config_chat_formats_label": "चैट प्रारूप",
    "module_llama_cpp_config_chat_formats_combo_placeholder_text": "एक चैट प्रारूप का चयन करें",
    "module_llama_cpp_config_chat_formats_combo_accessible_description":
        "मॉडल वार्तालापों के लिए प्रयुक्त प्रारूप का चयन करने के लिए ड्रॉपडाउन मेनू।",

    "module_llama_cpp_config_system_prompt_label": "सिस्टम प्रॉम्प्ट",
    "module_llama_cpp_config_system_prompt_edit_placeholder_text": "सिस्टम प्रॉम्प्ट टेक्स्ट दर्ज करें",
    "module_llama_cpp_config_system_prompt_edit_accessible_description":
        "सिस्टम प्रॉम्प्ट दर्ज करने के लिए टेक्स्ट फील्ड जो मॉडल प्रतिक्रियाओं को निर्देशित करता है।",

    "module_llama_cpp_config_response_temperature_label": "प्रतिक्रिया तापमान: {temperature}",
    "module_llama_cpp_config_response_temperature_input_accessible_description":
        "मॉडल की प्रतिक्रियाओं की यादृच्छिकता को समायोजित करता है। उच्च मूल्य अधिक विविधतापूर्ण आउटपुट\n"
        "उत्पन्न करते हैं, जबकि निम्न मूल्य अधिक पूर्वानुमान योग्य प्रतिक्रियाएं देते हैं।",

    "module_llama_cpp_config_response_max_tokens_label": "प्रतिक्रिया प्रति अधिकतम टोकन",
    "module_llama_cpp_config_response_max_tokens_input_accessible_description":
        "मॉडल की प्रतिक्रियाओं में टोकन की संख्या को वास्तविक संदर्भ विंडो सीमा तक सीमित करता है।\n"
        "शून्य मूल्य संदर्भ विंडो की क्षमता को मान लेता है।",

    "module_llama_cpp_config_prompt_history_size_label": "प्रॉम्प्ट इतिहास का आकार",
    "module_llama_cpp_config_prompt_history_size_input_accessible_description":
        "सिस्टम द्वारा संदर्भ के लिए बनाए रखे गए प्रॉम्प्ट इतिहास की प्रविष्टियों की संख्या को नियंत्रित करता है।\n"
        "शून्य मूल्य असीमित प्रविष्टियों की अनुमति देता है।"
}
