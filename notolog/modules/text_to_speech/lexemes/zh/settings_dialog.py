# Chinese lexemes settings_dialog.py
lexemes = {
    "module_text_to_speech_config_enabled_label": "启用文本朗读",
    "module_text_to_speech_config_setup_label": "语音设置",
    "module_text_to_speech_config_runtime_label": "语音运行程序",
    "module_text_to_speech_config_model_directory_label": "模型文件夹",
    "module_text_to_speech_config_tokenizer_directory_label": "分词器",
    "module_text_to_speech_config_details_label": "详情",
    "module_text_to_speech_config_model_license_label": "模型许可证",
    "module_text_to_speech_config_download_models_button": "下载模型",
    "module_text_to_speech_config_verify_models_button": "验证模型",
    "module_text_to_speech_config_cancel_button": "取消",
    "module_text_to_speech_config_stop_button": "停止",
    "module_text_to_speech_config_custom_models_label": "自定义模型文件",
    "module_text_to_speech_config_reading_label": "朗读",
    "module_text_to_speech_config_language_label": "语言",
    "module_text_to_speech_config_voice_label": "声音",
    "module_text_to_speech_config_speed_label": "速度",
    "module_text_to_speech_config_announce_headings_label": "播报标题级别",
    "module_text_to_speech_config_skip_inline_code_label": "跳过行内代码",
    "module_text_to_speech_config_skip_multiline_code_label": "跳过多行代码",
    "module_text_to_speech_config_test_voice_button": "测试声音",
    "module_text_to_speech_config_runtime_input_placeholder_text": "选择可执行文件…",
    "module_text_to_speech_config_model_input_placeholder_text": "自动",
    "module_text_to_speech_config_get_runtime_link": "获取运行程序 {version}",
    "module_text_to_speech_config_about_label": "关于{title}",
    "module_text_to_speech_config_choose_path_label": "选择{title}",
    "module_text_to_speech_config_status_checking_runtime": "正在检查语音运行程序…",
    "module_text_to_speech_config_status_checking_models": "正在检查缓存并下载缺失的模型…",
    "module_text_to_speech_config_status_models_verified": "现有模型已验证，可以开始朗读。",
    "module_text_to_speech_config_status_models_downloaded": "模型已下载并验证，可以开始朗读。",
    "module_text_to_speech_config_status_models_found": "已找到模型文件，请验证模型或测试声音。",
    "module_text_to_speech_config_status_models_missing": "需要模型，请先下载声音。",
    "module_text_to_speech_config_status_runtime_missing": "需要运行程序，请选择可执行文件或获取运行程序。",
    "module_text_to_speech_config_status_download_cancelled": "已取消。已完成的下载会保留，请重试以继续。",
    "module_text_to_speech_config_error_permission_denied": "权限不足，请选择可写入的模型文件夹并检查文件访问权限。",
    "module_text_to_speech_config_error_file_access": "文件访问失败：{error}。请查看详情。",
    "module_text_to_speech_config_progress_elapsed": "已用时 {time}",
    "module_text_to_speech_config_progress_files_complete": "已完成 {count}/3 个文件",
    "module_text_to_speech_config_progress_downloading": "文件 {number}/3 · 正在下载{role} · {size} MiB…",
    "module_text_to_speech_config_progress_cached": "已验证缓存中的 {count}/3 个模型文件…",
    "module_text_to_speech_config_progress_verifying": "文件 {number}/3 · 正在验证下载文件…",
    "module_text_to_speech_config_download_role_voice": "语音模型",
    "module_text_to_speech_config_download_role_codec": "音频解码器",
    "module_text_to_speech_config_download_role_tokenizers": "分词器",
    "module_text_to_speech_config_download_role_model": "模型",
    "module_text_to_speech_config_runtime_required": "请先选择语音运行程序。",
    "module_text_to_speech_config_models_required": "请先下载模型。",
    "module_text_to_speech_config_enable_required": "请先启用文本朗读。",
    "module_text_to_speech_config_status_testing_voice": "正在加载模型并准备测试声音…",
    "module_text_to_speech_config_details_accessible_description": "显示或隐藏操作日志",
    "module_text_to_speech_config_setup_accessible_description": (
        "选择 NeMo-Speech.cpp 运行程序，然后下载 MagpieTTS、NanoCodec 和分词器。模型使用单独的许可证。"
    ),
    "module_text_to_speech_config_runtime_input_accessible_description": (
        "需要 NeMo-Speech.cpp 0.1.0。解压归档后选择 bin/nemo-speech（Windows 上为 bin/nemo-speech.exe）。"
    ),
    "module_text_to_speech_config_model_directory_input_accessible_description": (
        "模型将下载到此处。现有文件会被验证并重复使用。需要 curl 和约 550 MB 空间。"
    ),
    "module_text_to_speech_config_custom_models_accessible_description": "指定自定义模型路径，或清空这些字段以使用模型文件夹。",
    "module_text_to_speech_config_reading_accessible_description": "选择声音、语言和播放速度。可以用简短的语音提示代替代码内容。",
    "module_text_to_speech_config_language_input_accessible_description": (
        "选择文档语言，不会自动检测。默认为英语。普通话和日语需要编译时启用相应语言支持的运行程序。"
    ),
    "module_text_to_speech_config_voice_input_accessible_description": "MagpieTTS 声音：John、Sofia、Aria、Jason 和 Leo。",
    "module_text_to_speech_config_speed_input_accessible_description": "播放速度也会改变音高。",
    "module_text_to_speech_config_announce_headings_accessible_description": (
        "Markdown 和 HTML 的 1–4 级标题分别播报 Chapter、Section、Subsection 和 Sub-subsection，5–6 级播报 Heading level"
        " 5–6。"
    ),
    "module_text_to_speech_config_skip_inline_code_accessible_description": (
        "勾选时播报“Inline code block”，未勾选时朗读行内代码。围栏代码和缩进代码使用多行代码设置。"
    ),
    "module_text_to_speech_config_skip_multiline_code_accessible_description": (
        "勾选时播报“Multiline code block”，未勾选时朗读围栏代码和缩进代码。"
    ),
    "module_text_to_speech_config_verify_models_accessible_description": "验证现有文件并下载缺失或损坏的文件。",
    "module_text_to_speech_config_editor_required": "请从编辑器打开这些设置以测试声音。",
    "module_text_to_speech_config_context_length_label": "上下文长度",
    "module_text_to_speech_config_context_whole_document": "整个文档",
    "module_text_to_speech_config_context_characters": "{count} 个字符",
    "module_text_to_speech_config_context_length_accessible_description": (
        "每次语音请求的最大字符数。最右端：整个文档，保留标题停顿。较大的上下文会增加启动时间和内存占用。运行程序的限制仍然适用。"
    ),
    "module_text_to_speech_config_cancel_download_title": "取消下载？",
    "module_text_to_speech_config_cancel_download_confirmation": "关闭设置将取消下载。已完成的文件会保留。关闭设置？",
    "module_text_to_speech_config_status_custom_models": "已选择自定义模型文件。下载使用模型文件夹。",
}
