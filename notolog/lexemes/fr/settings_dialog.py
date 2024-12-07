# French lexemes settings_dialog.py
lexemes = {
    # Paramètres
    "window_title": "Paramètres",

    "button_close": "Fermer",

    "tab_general": "Général",
    "tab_editor_config": "Éditeur",
    "tab_viewer_config": "Visualiseur",
    "tab_ai_config": "Config IA",

    "general_app_config_label": "Configuration de l'application",
    "general_app_language_label": "Langue",
    "general_app_language_combo_placeholder_text": "Choisir une langue",
    "general_app_language_combo_accessible_description": "Langue de l'interface de l'application",
    "general_app_theme_label": "Thème",
    "general_app_theme_combo_placeholder_text": "Choisir un thème",
    "general_app_theme_combo_accessible_description": "Thème de l'interface de l'application",
    "general_app_main_menu_label": "Menu Principal",
    "general_app_main_menu_checkbox": "Afficher le menu principal",
    "general_app_main_menu_checkbox_accessible_description": "Afficher le menu déroulant principal de l'application",
    "general_app_font_size_label": "Taille de police : {size}pt",
    "general_app_font_size_slider_accessible_description": "Ajuster la taille de la police globale de l'application",

    "general_statusbar_label": "Barre de statut",
    "general_statusbar_show_global_cursor_position_checkbox": "Afficher la position globale du curseur",
    "general_statusbar_show_global_cursor_position_checkbox_accessible_description":
        "Afficher la position globale du curseur dans la barre de statut",

    "editor_config_label": "Configuration de l'éditeur",
    "editor_config_show_line_numbers_checkbox": "Afficher les numéros de ligne",
    "editor_config_show_line_numbers_checkbox_accessible_description": "Afficher les numéros de ligne dans l'éditeur",

    "viewer_config_label": "Configuration du visualiseur",
    "viewer_config_process_emojis_checkbox": "Convertir les emojis de texte en graphiques",
    "viewer_config_process_emojis_checkbox_accessible_description":
        "Convertir les emojis de texte en représentations graphiques",
    "viewer_config_highlight_todos_checkbox": "Mettre en évidence les TODO",
    "viewer_config_highlight_todos_checkbox_accessible_description": "Souligner les balises TODO dans le texte",
    "viewer_config_open_link_confirmation_checkbox": "Demander confirmation avant d'ouvrir les liens",
    "viewer_config_open_link_confirmation_checkbox_accessible_description":
        "Demander une confirmation avant d'ouvrir des liens",
    "viewer_config_save_resources_checkbox": "Enregistrer automatiquement les images externes sur le disque",
    "viewer_config_save_resources_checkbox_accessible_description":
        "Enregistre automatiquement des copies des images externes sur le disque pour un accès hors ligne.",

    "ai_config_inference_module_label": "Module d'inférence",
    "ai_config_inference_module_names_combo_label": "Module d'inférence actif",
    "ai_config_inference_module_names_combo_placeholder_text": "Choisir un module",
    "ai_config_inference_module_names_combo_accessible_description":
        "Sélectionnez parmi les modules d'inférence IA disponibles pour fonctionner avec l'Assistant AI.\n"
        "Les options incluent des modèles de langage de grande taille (LLM) avec traitement en temps réel,\n"
        "ou des fonctionnalités basées sur l'API.",

    "ai_config_base_label": "Paramètres de base",
    "ai_config_multi_turn_dialogue_checkbox": "Dialogue multi-tours avec mémoire conversationnelle",
    "ai_config_multi_turn_dialogue_checkbox_accessible_description":
        "Activez un dialogue multi-tours qui conserve la dernière invite pour une mémoire conversationnelle.\n"
        "Lorsqu'il est désactivé, seuls le nouveau message et l'invite système influencent la réponse.",
    "ai_config_convert_to_md_checkbox": "Convertir le résultat en Markdown",
    "ai_config_convert_to_md_checkbox_accessible_description":
        "Convertissez le message de sortie au format Markdown.",
}
