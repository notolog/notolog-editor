# Chinese lexemes settings_dialog.py
lexemes = {
    # 设置
    "window_title": "设置",

    "button_close": "关闭",

    "tab_general": "通用",
    "tab_editor_config": "编辑器",
    "tab_viewer_config": "查看器",
    "tab_ai_config": "AI 配置",

    "general_app_config_label": "应用配置",
    "general_app_language_label": "语言",
    "general_app_language_combo_placeholder_text": "选择语言",
    "general_app_language_combo_accessible_description": "应用界面语言",
    "general_app_theme_label": "主题",
    "general_app_theme_combo_placeholder_text": "选择主题",
    "general_app_theme_combo_accessible_description": "应用界面主题",
    "general_app_default_path_label": "默认笔记文件夹",
    "general_app_default_path_input_accessible_description": "指定存储笔记的默认文件夹",
    "general_app_default_path_input_placeholder_text": "选择或输入文件夹路径",
    "general_app_elements_visibility_label": "管理元素可见性",
    "general_app_main_menu_label": "主菜单",
    "general_app_main_menu_checkbox": "显示主菜单",
    "general_app_main_menu_checkbox_accessible_description": "显示应用的主下拉菜单",
    "general_app_font_size_label": "字体大小：{size}pt",
    "general_app_font_size_slider_accessible_description": "调整应用程序的全局字体大小",

    "general_statusbar_label": "状态栏",
    "general_statusbar_show_global_cursor_position_checkbox": "显示全局光标位置",
    "general_statusbar_show_global_cursor_position_checkbox_accessible_description":
        "在状态栏显示全局光标位置",
    "general_statusbar_show_navigation_arrows_checkbox": "显示导航箭头",
    "general_statusbar_show_navigation_arrows_checkbox_accessible_description": "在状态栏中显示导航箭头",

    "editor_config_label": "编辑器配置",
    "editor_config_show_line_numbers_checkbox": "显示行号",
    "editor_config_show_line_numbers_checkbox_accessible_description": "在编辑器中显示行号",

    "viewer_config_label": "查看器配置",
    "viewer_config_process_emojis_checkbox": "将文本表情转换为图形",
    "viewer_config_process_emojis_checkbox_accessible_description": "将文本表情转换为图形表示",
    "viewer_config_highlight_todos_checkbox": "突出显示待办事项",
    "viewer_config_highlight_todos_checkbox_accessible_description": "在文本中突出显示待办事项标签",
    "viewer_config_open_link_confirmation_checkbox": "打开链接前需确认",
    "viewer_config_open_link_confirmation_checkbox_accessible_description":
        "打开链接前询问确认",
    "viewer_config_save_resources_checkbox": "自动保存外部图片到硬盘",
    "viewer_config_save_resources_checkbox_accessible_description": "自动将外部图片的副本保存到硬盘以供离线访问。",

    "ai_config_inference_module_label": "推理模块",
    "ai_config_inference_module_names_combo_label": "活跃推理模块",
    "ai_config_inference_module_names_combo_placeholder_text": "选择模块",
    "ai_config_inference_module_names_combo_accessible_description":
        "从可用的AI推理模块中选择，以配合AI助手使用。\n"
        "选项包括具有实时处理功能的本地大型语言模型（LLM）或基于API的功能。",

    "ai_config_base_label": "基础参数",
    "ai_config_multi_turn_dialogue_checkbox": "带有会话记忆的多轮对话",
    "ai_config_multi_turn_dialogue_checkbox_accessible_description":
        "启用多轮对话，可保留上一次提示以进行会话记忆。\n"
        "关闭时，仅新消息和系统提示会影响回复。",
    "ai_config_convert_to_md_checkbox": "将结果转换为Markdown",
    "ai_config_convert_to_md_checkbox_accessible_description":
        "将输出消息转换为Markdown格式。",
}
