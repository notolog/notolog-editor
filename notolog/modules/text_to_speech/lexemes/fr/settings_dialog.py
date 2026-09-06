# French lexemes settings_dialog.py
lexemes = {
    "module_text_to_speech_config_enabled_label": "Activer la synthèse vocale",
    "module_text_to_speech_config_setup_label": "Configuration de la voix",
    "module_text_to_speech_config_runtime_label": "Moteur vocal",
    "module_text_to_speech_config_model_directory_label": "Dossier des modèles",
    "module_text_to_speech_config_tokenizer_directory_label": "Tokeniseurs",
    "module_text_to_speech_config_details_label": "Détails",
    "module_text_to_speech_config_model_license_label": "Licence du modèle",
    "module_text_to_speech_config_download_models_button": "Télécharger les modèles",
    "module_text_to_speech_config_verify_models_button": "Vérifier les modèles",
    "module_text_to_speech_config_cancel_button": "Annuler",
    "module_text_to_speech_config_stop_button": "Arrêter",
    "module_text_to_speech_config_custom_models_label": "Fichiers de modèle personnalisés",
    "module_text_to_speech_config_reading_label": "Lecture",
    "module_text_to_speech_config_language_label": "Langue",
    "module_text_to_speech_config_voice_label": "Voix",
    "module_text_to_speech_config_speed_label": "Vitesse",
    "module_text_to_speech_config_announce_headings_label": "Annoncer les titres",
    "module_text_to_speech_config_skip_inline_code_label": "Ignorer le code en ligne",
    "module_text_to_speech_config_skip_multiline_code_label": "Ignorer le code multiligne",
    "module_text_to_speech_config_test_voice_button": "Tester la voix",
    "module_text_to_speech_config_runtime_input_placeholder_text": "Sélectionner l’exécutable…",
    "module_text_to_speech_config_model_input_placeholder_text": "Automatique",
    "module_text_to_speech_config_get_runtime_link": "Obtenir le moteur {version}",
    "module_text_to_speech_config_about_label": "À propos de {title}",
    "module_text_to_speech_config_choose_path_label": "Choisir {title}",
    "module_text_to_speech_config_status_checking_runtime": "Vérification du moteur vocal…",
    "module_text_to_speech_config_status_checking_models": (
        "Vérification des fichiers en cache et téléchargement des modèles manquants…"
    ),
    "module_text_to_speech_config_status_models_verified": "Modèles existants vérifiés. Prêt à lire.",
    "module_text_to_speech_config_status_models_downloaded": "Modèles téléchargés et vérifiés. Prêt à lire.",
    "module_text_to_speech_config_status_models_found": "Modèles trouvés. Vérifiez-les ou testez la voix.",
    "module_text_to_speech_config_status_models_missing": "Modèles manquants. Téléchargez la voix pour commencer.",
    "module_text_to_speech_config_status_runtime_missing": (
        "Moteur requis. Sélectionnez un exécutable ou obtenez le moteur."
    ),
    "module_text_to_speech_config_status_download_cancelled": (
        "Annulé. Les téléchargements terminés sont conservés ; réessayez pour continuer."
    ),
    "module_text_to_speech_config_error_permission_denied": (
        "Accès refusé. Choisissez un dossier de modèles accessible en écriture et vérifiez les droits."
    ),
    "module_text_to_speech_config_error_file_access": "Échec d’accès au fichier : {error}. Voir Détails.",
    "module_text_to_speech_config_progress_elapsed": "{time} écoulé",
    "module_text_to_speech_config_progress_files_complete": "{count}/3 fichiers terminés",
    "module_text_to_speech_config_progress_downloading": "Fichier {number}/3 · Téléchargement de {role} · {size} MiB…",
    "module_text_to_speech_config_progress_cached": "{count}/3 fichiers de modèle vérifiés en cache…",
    "module_text_to_speech_config_progress_verifying": "Fichier {number}/3 · Vérification du téléchargement…",
    "module_text_to_speech_config_download_role_voice": "modèle vocal",
    "module_text_to_speech_config_download_role_codec": "décodeur audio",
    "module_text_to_speech_config_download_role_tokenizers": "tokeniseurs",
    "module_text_to_speech_config_download_role_model": "modèle",
    "module_text_to_speech_config_runtime_required": "Sélectionnez d’abord un moteur vocal.",
    "module_text_to_speech_config_models_required": "Téléchargez d’abord les modèles.",
    "module_text_to_speech_config_enable_required": "Activez d’abord la synthèse vocale.",
    "module_text_to_speech_config_status_testing_voice": "Chargement des modèles et préparation de la voix de test…",
    "module_text_to_speech_config_details_accessible_description": "Afficher ou masquer le journal",
    "module_text_to_speech_config_setup_accessible_description": (
        "Sélectionnez NeMo-Speech.cpp puis téléchargez MagpieTTS, NanoCodec et les tokeniseurs. Les "
        "modèles ont leur propre licence."
    ),
    "module_text_to_speech_config_runtime_input_accessible_description": (
        "Nécessite NeMo-Speech.cpp 0.1.0. Extrayez l’archive et sélectionnez bin/nemo-speech "
        "(bin/nemo-speech.exe sous Windows)."
    ),
    "module_text_to_speech_config_model_directory_input_accessible_description": (
        "Les modèles sont téléchargés ici. Les fichiers existants sont vérifiés et réutilisés. Nécessite"
        " curl et environ 550 Mo."
    ),
    "module_text_to_speech_config_custom_models_accessible_description": (
        "Remplacez les chemins des modèles ou videz les champs pour utiliser le dossier des modèles."
    ),
    "module_text_to_speech_config_reading_accessible_description": (
        "Choisissez la voix, la langue et la vitesse. Le code peut être remplacé par une courte annonce."
    ),
    "module_text_to_speech_config_language_input_accessible_description": (
        "Choisissez la langue du document ; aucune détection automatique. Anglais par défaut. Le "
        "mandarin et le japonais nécessitent un moteur compatible."
    ),
    "module_text_to_speech_config_voice_input_accessible_description": (
        "Voix MagpieTTS : John, Sofia, Aria, Jason et Leo."
    ),
    "module_text_to_speech_config_speed_input_accessible_description": (
        "La vitesse de lecture modifie aussi la hauteur de la voix."
    ),
    "module_text_to_speech_config_announce_headings_accessible_description": (
        "Annonce Chapter, Section, Subsection et Sub-subsection pour les titres Markdown et HTML de "
        "niveaux 1–4, puis Heading level 5–6."
    ),
    "module_text_to_speech_config_skip_inline_code_accessible_description": (
        "Coché : dit « Inline code block ». Décoché : lit le code en ligne. Le code délimité ou indenté "
        "utilise l’option multiligne."
    ),
    "module_text_to_speech_config_skip_multiline_code_accessible_description": (
        "Coché : dit « Multiline code block ». Décoché : lit le code délimité ou indenté."
    ),
    "module_text_to_speech_config_verify_models_accessible_description": (
        "Vérifier les fichiers existants et télécharger ceux qui manquent ou sont endommagés."
    ),
    "module_text_to_speech_config_editor_required": "Ouvrez ces paramètres depuis l’éditeur pour tester la voix.",
    "module_text_to_speech_config_context_length_label": "Longueur du contexte",
    "module_text_to_speech_config_context_whole_document": "Document entier",
    "module_text_to_speech_config_context_characters": "{count} caractères",
    "module_text_to_speech_config_context_length_accessible_description": (
        "Nombre maximal de caractères par requête vocale. À droite : document entier, avec pauses aux "
        "titres. Un contexte plus long augmente le délai initial et la mémoire utilisée. Les limites du "
        "moteur restent applicables."
    ),
    "module_text_to_speech_config_cancel_download_title": "Annuler le téléchargement ?",
    "module_text_to_speech_config_cancel_download_confirmation": (
        "Fermer les paramètres annule le téléchargement. Les fichiers terminés sont conservés. Fermer "
        "les paramètres ?"
    ),
    "module_text_to_speech_config_status_custom_models": (
        "Des fichiers de modèle personnalisés sont sélectionnés. Les téléchargements utilisent le "
        "dossier des modèles."
    ),
}
