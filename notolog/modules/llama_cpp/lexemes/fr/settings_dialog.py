# French lexemes settings_dialog.py
lexemes = {
    "tab_module_llama_cpp_config": "Module llama.cpp",

    "module_llama_cpp_config_label": "Module llama.cpp",
    "module_llama_cpp_config_path_label": "Emplacement du modèle",
    "module_llama_cpp_config_path_input_placeholder_text": "Sélectionnez ou entrez le chemin du modèle",
    "module_llama_cpp_config_path_input_accessible_description":
        "Un champ de saisie avec un sélecteur pour spécifier le chemin du modèle local.\n"
        "Prend en charge les modèles au format GGUF, un format de fichier binaire optimisé\n"
        "pour stocker des modèles utilisés avec GGML et des exécuteurs basés sur GGML.",
    "module_llama_cpp_config_path_input_filter_text": "Fichiers GGUF",

    "module_llama_cpp_config_context_window_label": "Taille de la fenêtre de contexte",
    "module_llama_cpp_config_context_window_input_accessible_description":
        "Définit le nombre de jetons que le modèle considère pour générer des réponses.\n"
        "Contrôle la quantité de contexte préalable utilisée.",

    "module_llama_cpp_chat_formats_label": "Formats de chat",
    "module_llama_cpp_chat_formats_combo_placeholder_text": "Sélectionnez un format de chat",
    "module_llama_cpp_chat_formats_combo_accessible_description":
        "Menu déroulant pour sélectionner le format utilisé pour les conversations modèles.",

    "module_llama_cpp_config_system_prompt_label": "Invite de système",
    "module_llama_cpp_config_system_prompt_edit_placeholder_text": "Entrez le texte de l'invite système",
    "module_llama_cpp_config_system_prompt_edit_accessible_description":
        "Champ de texte pour entrer les invites de système qui guident les réponses du modèle.",

    "module_llama_cpp_config_response_temperature_label": "Température de réponse : {temperature}",
    "module_llama_cpp_config_response_temperature_input_accessible_description":
        "Ajuste l'aléatoire des réponses du modèle. Des valeurs plus élevées produisent des sorties plus variées,\n"
        "tandis que des valeurs plus basses résultent en des réponses plus prévisibles.",

    "module_llama_cpp_config_response_max_tokens_label": "Nombre maximal de jetons par réponse",
    "module_llama_cpp_config_response_max_tokens_input_accessible_description":
        "Limite le nombre de jetons dans les réponses du modèle jusqu'à la limite réelle de la fenêtre de contexte.\n"
        "Une valeur nulle suppose la capacité de la fenêtre de contexte.",

    "module_llama_cpp_config_prompt_history_size_label": "Taille de l'historique des invites",
    "module_llama_cpp_config_prompt_history_size_input_accessible_description":
        "Contrôle le nombre d'entrées dans l'historique des invites conservé par le système pour référence.\n"
        "Une valeur nulle permet un nombre illimité d'entrées."
}
