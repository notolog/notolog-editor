# Japanese lexemes settings_dialog.py
lexemes = {
    "tab_ondevice_llm_config": "デバイス上のLLM",

    "module_ondevice_llm_config_label": "デバイス上のLLMモデル",
    "module_ondevice_llm_config_path_label": "ONNXモデルの位置",
    "module_ondevice_llm_config_path_input_placeholder_text": "モデルディレクトリへのパス",
    "module_ondevice_llm_config_path_input_accessible_description":
        "ONNXファイルが位置するモデルディレクトリへのパスを指定するセレクター付き入力フィールド。\n"
        "サポートされるモデルはONNX形式で、これはオープンニューラルネットワークエクスチェンジの略で、\n"
        "機械学習モデルのためのオープンスタンダードフォーマットです。",

    "module_ondevice_llm_config_response_temperature_label": "温度: {temperature}",
    "module_ondevice_llm_config_response_temperature_input_accessible_description":
        "モデルの応答のランダム性を調整します。高い値はより多様な出力を生み出し、\n"
        "低い値はより予測可能な応答をもたらします。",

    "module_ondevice_llm_config_response_max_tokens_label": "最大応答トークン数",
    "module_ondevice_llm_config_response_max_tokens_input_accessible_description":
        "応答で受け取るトークンの最大数を設定します。これには単語や句読点が含まれ、\n"
        "出力の長さを制御します。",

    "module_ondevice_llm_config_prompt_history_size_label": "プロンプト履歴のサイズ",
    "module_ondevice_llm_config_prompt_history_size_input_accessible_description":
        "システムが参照用に保持するプロンプト履歴のエントリ数を制御します。\n"
        "ゼロの値は無制限のエントリを許可します。"
}
