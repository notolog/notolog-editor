# Japanese lexemes settings_dialog.py
lexemes = {
    # 設定
    "window_title": "設定",

    "button_close": "閉じる",

    "tab_general": "一般",
    "tab_workspace": "ワークスペース",
    "tab_ai_config": "AI 設定",

    "general_app_config_label": "アプリ設定",
    "general_app_language_label": "言語",
    "general_app_language_combo_placeholder_text": "言語を選択",
    "general_app_language_combo_accessible_description": "アプリのインターフェース言語",
    "general_app_theme_label": "テーマ",
    "general_app_theme_combo_placeholder_text": "テーマを選択",
    "general_app_theme_combo_accessible_description": "アプリのインターフェーステーマ",
    "general_app_default_path_label": "ノートのデフォルトフォルダー",
    "general_app_default_path_input_accessible_description": "ノートを保存するデフォルトフォルダーを指定してください",
    "general_app_default_path_input_placeholder_text": "フォルダーパスを選択または入力",
    "general_app_elements_visibility_label": "要素の可視性を管理",
    "general_app_main_menu_label": "メインメニュー",
    "general_app_main_menu_checkbox": "メインメニューを表示",
    "general_app_main_menu_checkbox_accessible_description": "アプリのメインドロップダウンメニューを表示",
    "general_app_font_size_label": "フォントサイズ：{size}pt",
    "general_app_font_size_slider_accessible_description": "アプリの全体的なフォントサイズを調整する",

    "general_file_deletion_label": "ファイルの削除",
    "general_reversible_file_deletion_checkbox": "ファイルを復元可能な方法で削除",
    "general_reversible_file_deletion_checkbox_accessible_description":
        ".del 拡張子を追加して、削除したファイルを Notolog のごみ箱に移動します",

    "workspace_bottom_bar_show_global_cursor_position_checkbox": "グローバルカーソル位置を表示",
    "workspace_bottom_bar_show_global_cursor_position_checkbox_accessible_description":
        "ステータスバーにグローバルカーソル位置を表示する",
    "workspace_bottom_bar_show_navigation_arrows_checkbox": "ナビゲーション矢印を表示",
    "workspace_bottom_bar_show_navigation_arrows_checkbox_accessible_description": "ステータスバーにナビゲーション矢印を表示",

    "workspace_editor_mode_label": "編集モード",
    "workspace_editor_mode_show_line_numbers_checkbox": "行番号を表示",
    "workspace_editor_mode_show_line_numbers_checkbox_accessible_description": "エディタ内で行番号を表示する",

    "workspace_view_mode_label": "表示モード",
    "workspace_view_mode_process_emojis_checkbox": "テキスト絵文字をグラフィックに変換",
    "workspace_view_mode_process_emojis_checkbox_accessible_description": "テキスト絵文字をグラフィカルな表現に変換する",
    "workspace_view_mode_highlight_todos_checkbox": "TODOをハイライト",
    "workspace_view_mode_highlight_todos_checkbox_accessible_description": "テキスト内のTODOタグを強調表示する",
    "workspace_view_mode_open_link_confirmation_checkbox": "リンク開く前に確認が必要",
    "workspace_view_mode_open_link_confirmation_checkbox_accessible_description": "リンクを開く前に確認を求める",
    "workspace_view_mode_save_resources_checkbox": "外部画像をディスクに自動保存",
    "workspace_view_mode_save_resources_checkbox_accessible_description":
        "オフラインアクセスのために外部画像のコピーをディスクに自動保存します。",

    "ai_config_inference_module_label": "推論モジュール",
    "ai_config_inference_module_names_combo_label": "アクティブ推論モジュール",
    "ai_config_inference_module_names_combo_placeholder_text": "モジュールを選択",
    "ai_config_inference_module_names_combo_accessible_description":
        "AIアシスタントと連携して動作する利用可能なAI推論モジュールから選択してください。\n"
        "オプションには、リアルタイム処理を備えたローカルの大規模言語モデル（LLM）またはAPIベースの機能が含まれます。",

    "ai_config_base_label": "基本パラメーター",
    "ai_config_multi_turn_dialogue_checkbox": "会話メモリを伴うマルチターンダイアログ",
    "ai_config_multi_turn_dialogue_checkbox_accessible_description":
        "以前のプロンプトを保持する会話メモリ付きのマルチターンダイアログを有効にします。\n"
        "オフの場合、新しいメッセージとシステムプロンプトのみが応答に影響します。",
    "ai_config_convert_to_md_checkbox": "結果をMarkdownに変換",
    "ai_config_convert_to_md_checkbox_accessible_description":
        "出力メッセージをMarkdown形式に変換します。",
    "workspace_bottom_bar_label": "下部バー",
    "workspace_bottom_bar_show_system_load_graphs_checkbox": "CPUとメモリのグラフを表示",
    "workspace_bottom_bar_show_system_load_graphs_checkbox_accessible_description":
        "下部バーにCPUとメモリの使用率グラフおよび区切り線を表示します",
    "workspace_bottom_bar_system_load_interval_ms_label": "グラフの更新間隔",
    "workspace_bottom_bar_system_load_interval_ms_accessible_description":
        "CPUとメモリの使用率を読み取る間隔をミリ秒単位で設定します",
}
