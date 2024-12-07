# French lexemes settings_dialog.py
lexemes = {
    "tab_openai_api_config": "API OpenAI",

    "module_openai_api_label": "API OpenAI",
    "module_openai_api_url_label": "URL de l'API",
    "module_openai_api_url_input_placeholder_text": "URL de l'API",
    "module_openai_api_url_input_accessible_description":
        "L'URL de l'API OpenAI est l'adresse du point de terminaison de l'API, qui peut varier en fonction du service\n"
        "et de la version. L'Assistant AI utilise celle dédiée à la fonctionnalité de chat conversationnel ou\n"
        "aux complétions de texte. Consultez la documentation officielle de l'API OpenAI pour obtenir l'URL actuelle.",
    "module_openai_api_key_label": "Clé API",
    "module_openai_api_key_input_placeholder_text": "Clé API",
    "module_openai_api_key_input_accessible_description":
        "La clé API OpenAI est un jeton secret utilisé pour authentifier les requêtes au point de terminaison de l'API.",
    "module_openai_api_supported_models_label": "Modèles pris en charge",
    "module_openai_api_model_names_combo_placeholder_text": "Choisir un modèle",
    "module_openai_api_model_names_combo_accessible_description":
        "Sélectionnez parmi les modèles pris en charge pour les conversations par chat.",

    "module_openai_api_base_system_prompt_label": "Prompt Système",
    "module_openai_api_base_system_prompt_edit_placeholder_text": "Prompt système de base qui précède chaque demande",
    "module_openai_api_base_system_prompt_edit_accessible_description":
        "Un prompt système de base qui précède chaque demande.\n"
        "Généralement, il s'agit de texte simple avec des instructions ou des caractéristiques de rôle.",

    "module_openai_api_base_response_temperature_label": "Température : {temperature}",
    "module_openai_api_base_response_temperature_input_accessible_description":
        "Ajuste l'aléatoire des réponses du modèle. Des valeurs plus élevées produisent des résultats plus variés, "
        "tandis que des valeurs plus faibles rendent les réponses plus prévisibles.",

    "module_openai_api_base_response_max_tokens_label": "Nombre maximum de tokens de réponse",
    "module_openai_api_base_response_max_tokens_input_accessible_description":
        "Le nombre maximum de tokens à recevoir en réponse, tels que des mots et de la ponctuation, "
        "contrôlant la longueur de la sortie.",

    "module_openai_api_config_prompt_history_size_label": "Taille de l'historique des prompts",
    "module_openai_api_config_prompt_history_size_input_accessible_description":
        "Contrôle le nombre d'entrées dans l'historique des prompts que le système conserve pour référence.\n"
        "Une valeur nulle permet un nombre illimité d'entrées."
}
