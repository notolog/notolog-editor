# Japanese lexemes settings_dialog.py
lexemes = {
    "tab_openai_api_config": "OpenAI API",

    "module_openai_api_label": "OpenAI API",
    "module_openai_api_url_label": "APIのURL",
    "module_openai_api_url_input_placeholder_text": "APIのURL",
    "module_openai_api_url_input_accessible_description":
        "OpenAI APIのURLはAPIエンドポイントのアドレスであり、サービスやバージョンによって異なる場合があります。\n"
        "AIアシスタントは、会話型チャット機能またはテキスト補完用のエンドポイントを使用します。\n"
        "最新のURLを取得するには、OpenAI APIの公式ドキュメントを参照してください。",
    "module_openai_api_key_label": "APIキー",
    "module_openai_api_key_input_placeholder_text": "APIキー",
    "module_openai_api_key_input_accessible_description":
        "OpenAI APIキーは、APIエンドポイントへのリクエストを認証するために使用される秘密のトークンです。",
    "module_openai_api_supported_models_label": "対応モデル",
    "module_openai_api_model_names_combo_placeholder_text": "モデルを選択",
    "module_openai_api_model_names_combo_accessible_description":
        "チャット会話用に対応するモデルから選択します。",

    "module_openai_api_base_system_prompt_label": "システムプロンプト",
    "module_openai_api_base_system_prompt_edit_placeholder_text": "各リクエストに先立つ基本システムプロンプト",
    "module_openai_api_base_system_prompt_edit_accessible_description":
        "各リクエストに先立つ基本システムプロンプト。\n"
        "通常、指示や役割の特性を含むプレーンテキストです。",

    "module_openai_api_base_response_temperature_label": "温度: {temperature}",
    "module_openai_api_base_response_temperature_input_accessible_description":
        "モデルの応答のランダム性を調整します。高い値はより多様な出力を生成し、\n"
        "低い値は応答をより予測可能にします。",

    "module_openai_api_base_response_max_tokens_label": "最大応答トークン数",
    "module_openai_api_base_response_max_tokens_input_accessible_description":
        "応答で受け取るトークンの最大数を設定します。これには単語や句読点が含まれ、\n"
        "出力の長さを制御します。",

    "module_openai_api_config_prompt_history_size_label": "プロンプト履歴のサイズ",
    "module_openai_api_config_prompt_history_size_input_accessible_description":
        "システムが参照用に保持するプロンプト履歴のエントリ数を制御します。\n"
        "0の値は無制限のエントリを許可します。"
}
