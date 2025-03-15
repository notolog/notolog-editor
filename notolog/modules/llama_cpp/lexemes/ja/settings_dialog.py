# Japanese lexemes settings_dialog.py
lexemes = {
    "tab_module_llama_cpp_config": "モジュール llama.cpp",

    "module_llama_cpp_config_label": "モジュール llama.cpp",
    "module_llama_cpp_config_path_label": "モデルの位置",
    "module_llama_cpp_config_path_input_placeholder_text": "モデルパスを選択または入力してください",
    "module_llama_cpp_config_path_input_accessible_description":
        "ローカルモデルのパスを指定するためのセレクター付き入力フィールドです。GGUF形式のモデルをサポートし、\n"
        "GGMLおよびGGMLベースのエクゼキューターで使用されるモデルを格納するために最適化されたバイナリファイル形式です。",
    "module_llama_cpp_config_path_input_filter_text": "GGUFファイル",

    "module_llama_cpp_config_context_window_label": "コンテキストウィンドウのサイズ",
    "module_llama_cpp_config_context_window_input_accessible_description":
        "モデルがレスポンスを生成するために考慮するトークンの数を設定します。どれだけの前のコンテキストが使用されるかを制御します。",

    "module_llama_cpp_config_chat_formats_label": "チャット形式",
    "module_llama_cpp_config_chat_formats_combo_placeholder_text": "チャット形式を選択してください",
    "module_llama_cpp_config_chat_formats_combo_accessible_description":
        "モデル会話に使用される形式を選択するためのドロップダウンメニューです。",

    "module_llama_cpp_config_system_prompt_label": "システムプロンプト",
    "module_llama_cpp_config_system_prompt_edit_placeholder_text": "システムプロンプトのテキストを入力してください",
    "module_llama_cpp_config_system_prompt_edit_accessible_description":
        "モデルの応答を導くシステムプロンプトを入力するためのテキストフィールドです。",

    "module_llama_cpp_config_response_temperature_label": "応答の温度: {temperature}",
    "module_llama_cpp_config_response_temperature_input_accessible_description":
        "モデルの応答のランダム性を調整します。高い値はより多様な出力を生成し、\n"
        "低い値はより予測可能な応答をもたらします。",

    "module_llama_cpp_config_response_max_tokens_label": "応答あたりの最大トークン数",
    "module_llama_cpp_config_response_max_tokens_input_accessible_description":
        "実際のコンテキストウィンドウの制限までモデルの応答中のトークン数を制限します。\n"
        "ゼロ値はコンテキストウィンドウの容量を想定します。",

    "module_llama_cpp_config_prompt_history_size_label": "プロンプト履歴のサイズ",
    "module_llama_cpp_config_prompt_history_size_input_accessible_description":
        "システムによって参照のために保持されるプロンプト履歴のエントリの数を制御します。\n"
        "ゼロ値は無制限のエントリを可能にします。"
}
