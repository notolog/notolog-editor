# Japanese lexemes settings_dialog.py
lexemes = {
    # 設定
    "window_title": "設定",

    "button_close": "閉じる",

    "tab_general": "一般",
    "tab_editor_config": "エディター",
    "tab_viewer_config": "ビューア",
    "tab_ai_config": "AI 設定",

    "general_app_config_label": "アプリ設定",
    "general_app_language_label": "言語",
    "general_app_language_combo_placeholder_text": "言語を選択",
    "general_app_language_combo_accessible_description": "アプリのインターフェース言語",
    "general_app_theme_label": "テーマ",
    "general_app_theme_combo_placeholder_text": "テーマを選択",
    "general_app_theme_combo_accessible_description": "アプリのインターフェーステーマ",
    "general_app_main_menu_label": "メインメニュー",
    "general_app_main_menu_checkbox": "メインメニューを表示",
    "general_app_main_menu_checkbox_accessible_description": "アプリのメインドロップダウンメニューを表示",
    "general_app_font_size_label": "フォントサイズ：{size}pt",
    "general_app_font_size_slider_accessible_description": "アプリの全体的なフォントサイズを調整する",

    "general_statusbar_label": "ステータスバー",
    "general_statusbar_show_global_cursor_position_checkbox": "グローバルカーソル位置を表示",
    "general_statusbar_show_global_cursor_position_checkbox_accessible_description":
        "ステータスバーにグローバルカーソル位置を表示する",

    "editor_config_label": "エディタ設定",
    "editor_config_show_line_numbers_checkbox": "行番号を表示",
    "editor_config_show_line_numbers_checkbox_accessible_description": "エディタ内で行番号を表示する",

    "viewer_config_label": "ビューワ設定",
    "viewer_config_process_emojis_checkbox": "テキスト絵文字をグラフィックに変換",
    "viewer_config_process_emojis_checkbox_accessible_description": "テキスト絵文字をグラフィカルな表現に変換する",
    "viewer_config_highlight_todos_checkbox": "TODOをハイライト",
    "viewer_config_highlight_todos_checkbox_accessible_description": "テキスト内のTODOタグを強調表示する",
    "viewer_config_open_link_confirmation_checkbox": "リンク開く前に確認が必要",
    "viewer_config_open_link_confirmation_checkbox_accessible_description": "リンクを開く前に確認を求める",
    "viewer_config_save_resources_checkbox": "外部画像をディスクに自動保存",
    "viewer_config_save_resources_checkbox_accessible_description":
        "オフラインアクセスのために外部画像のコピーをディスクに自動保存します。",

    "ai_config_openai_api_label": "OpenAI API",
    "ai_config_openai_api_url_input_placeholder_text": "API URL",
    "ai_config_openai_api_url_input_accessible_description": "OpenAI APIのURL",
    "ai_config_openai_api_key_input_placeholder_text": "API キー",
    "ai_config_openai_api_key_input_accessible_description": "OpenAI APIのキー",
    "ai_config_openai_api_supported_models_label": "サポートされているモデル",
    "ai_config_ai_model_names_combo_placeholder_text": "モデルを選択",
    "ai_config_ai_model_names_combo_accessible_description": "選択可能なサポートされているモデル",

    "ai_config_base_label": "基本パラメータ",
    "ai_config_base_system_prompt_label": "システムプロンプト",
    "ai_config_base_system_prompt_edit_placeholder_text": "各リクエストに先立つ基本システムプロンプト",
    "ai_config_base_system_prompt_edit_accessible_description":
        "各リクエストに先立つ基本システムプロンプト。プレーンテキスト。",
    "ai_config_base_response_max_tokens_label": "応答の最大トークン数",
    "ai_config_base_response_max_tokens_input_accessible_description": "応答で受け取る最大トークン数",
}