# French lexemes settings_dialog.py
lexemes = {
    "tab_ondevice_llm_config": "LLM sur Appareil",

    "module_ondevice_llm_config_label": "Modèle LLM sur Appareil",
    "module_ondevice_llm_config_path_label": "Emplacement du modèle ONNX",
    "module_ondevice_llm_config_path_input_placeholder_text": "Chemin du répertoire du modèle",
    "module_ondevice_llm_config_path_input_accessible_description":
        "Un champ de saisie avec un sélecteur pour spécifier le chemin vers le répertoire du modèle où se trouvent\n"
        "les fichiers ONNX. Les modèles pris en charge sont au format ONNX, qui représente l'échange de réseaux\n"
        "neuronaux ouverts, un standard ouvert pour les formats de modèles d'apprentissage automatique.",

    "module_ondevice_llm_config_response_temperature_label": "Température : {temperature}",
    "module_ondevice_llm_config_response_temperature_input_accessible_description":
        "Ajuste l'aléatoire des réponses du modèle. Des valeurs plus élevées produisent des sorties plus variées,\n"
        "tandis que des valeurs plus basses rendent les réponses plus prévisibles.",

    "module_ondevice_llm_config_response_max_tokens_label": "Nombre maximum de tokens de réponse",
    "module_ondevice_llm_config_response_max_tokens_input_accessible_description":
        "Définit le nombre maximum de tokens à recevoir en réponse, tels que les mots et la ponctuation,\n"
        "contrôlant la longueur de la sortie.",

    "module_ondevice_llm_config_execution_provider_label": "Accélération Matérielle",
    "module_ondevice_llm_config_execution_provider_placeholder": "Sélectionner le fournisseur",
    "module_ondevice_llm_config_execution_provider_accessible_description":
        "Sélectionnez le fournisseur d'accélération matérielle pour l'inférence du modèle. "
        "Les options incluent :\n"
        "CPU (par défaut), CUDA (GPUs NVIDIA), DirectML (Windows), TensorRT, OpenVINO (Intel), "
        "QNN (Qualcomm), CoreML (Apple).\n"
        "Remarque : Les fournisseurs non-CPU nécessitent des packages ONNX Runtime spécifiques "
        "(ex: onnxruntime-genai-cuda).",

    "module_ondevice_llm_config_prompt_history_size_label": "Taille de l'historique des prompts",
    "module_ondevice_llm_config_prompt_history_size_input_accessible_description":
        "Contrôle le nombre d'entrées dans l'historique des prompts que le système conserve pour référence.\n"
        "Une valeur zéro permet un nombre illimité d'entrées."
}
