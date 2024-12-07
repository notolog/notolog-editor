# French lexemes common.py
lexemes = {
    "app_title": "Éditeur Notolog",
    "app_title_with_sub": "{app_title} - {sub_title}",

    "tree_filter_accessible_desc": "Champ de filtre de fichier",

    "menu_action_copy_file_path": "Copier le chemin du fichier",
    "menu_action_rename": "Renommer",
    "menu_action_delete": "Supprimer",
    "menu_action_delete_completely": "Supprimer définitivement",
    "menu_action_restore": "Restaurer",
    "menu_action_create_new_dir": "Créer un nouveau répertoire",

    "dialog_file_rename_title": "Renommer le fichier",
    "dialog_file_rename_field_label": "Entrer le nouveau nom du fichier",
    "dialog_file_rename_button_ok": "Renommer",
    "dialog_file_rename_warning_exists": "Un fichier portant le même nom existe déjà",

    "dialog_file_delete_title": "Supprimer le fichier",
    "dialog_file_delete_text": "Supprimer le fichier \"{file_name}\" ?",
    "dialog_file_delete_completely_title": "Supprimer définitivement le fichier",
    "dialog_file_delete_completely_text": "Supprimer définitivement le fichier \"{file_name}\" ?",
    "dialog_file_delete_error": "Impossible de supprimer le fichier, une erreur s'est produite",
    "dialog_file_delete_error_not_found": "Fichier non trouvé",

    "dialog_file_restore_title": "Restaurer le fichier",
    "dialog_file_restore_text": "Restaurer le fichier \"{file_name}\" ?",
    "dialog_file_restore_error": "Impossible de restaurer le fichier, une erreur s'est produite",
    "dialog_file_restore_warning_exists": "Un fichier portant le nom {file_name} existe déjà",

    "dialog_create_new_dir_title": "Créer un nouveau répertoire",
    "dialog_create_new_dir_label": "Nom du nouveau répertoire",
    "dialog_create_new_dir_input_placeholder_text": "Entrez le nom du répertoire",
    "dialog_create_new_dir_button_ok": "Créer",
    "dialog_create_new_dir_button_cancel": "Annuler",
    "dialog_create_new_dir_warning_empty_title": "Erreur de nom du nouveau répertoire",
    "dialog_create_new_dir_warning_empty_text": "Le nom du répertoire ne peut pas être vide",
    "dialog_create_new_dir_warning_too_long_title": "Erreur de nom du nouveau répertoire",
    "dialog_create_new_dir_warning_too_long_text": "Le nom du répertoire est trop long; maximum "
                                                   "{symbols} caractères autorisés !",
    "dialog_create_new_dir_error_existed": "Le répertoire existe déjà",
    "dialog_create_new_dir_error": "Impossible de créer le répertoire. Assurez-vous que le répertoire de destination "
                                   "{base_dir} est accessible en écriture",

    "dialog_message_box_title": "Message",
    "dialog_message_box_button_ok": "Fermer",

    "action_new_file_first_line_template_text": "Nouveau document",
    "action_open_file_dialog_caption": "Ouvrir un fichier",
    "action_save_as_file_dialog_caption": "Enregistrer un fichier",

    "dialog_save_empty_file_title": "Enregistrer un fichier vide",
    "dialog_save_empty_file_text": "Autoriser l'enregistrement du fichier sans contenu ?",

    "dialog_encrypt_file_title": "Chiffrer le fichier",
    "dialog_encrypt_file_text": "Chiffrer le fichier \"{file_name}\" ?",
    "encrypt_file_warning_file_is_already_encrypted": "Le fichier est déjà chiffré !",
    "dialog_encrypt_file_rewrite_existing_title": "Réécrire sur le fichier existant",
    "dialog_encrypt_file_rewrite_existing_text": "Réécrire sur le fichier existant \"{file_path}\" ?",

    "dialog_decrypt_file_title": "Déchiffrer le fichier",
    "dialog_decrypt_file_text": "Déchiffrer le fichier \"{file_name}\" ?",
    "decrypt_file_warning_file_is_not_encrypted": "Le fichier n'est pas chiffré !",
    "dialog_decrypt_file_rewrite_existing_title": "Réécrire sur le fichier existant",
    "dialog_decrypt_file_rewrite_existing_text": "Réécrire sur le fichier existant \"{file_path}\" ?",

    "dialog_encrypt_new_password_title": "Nouveau mot de passe",
    "dialog_encrypt_new_password_label": "Mot de passe :",
    "dialog_encrypt_new_password_input_placeholder_text": "Entrez un nouveau mot de passe",
    "dialog_encrypt_new_password_hint_label": "Indice :",
    "dialog_encrypt_new_password_hint_label_description":
        "L'indice n'est pas crypté et peut être lu dans le fichier ! "
        "\nÉvitez des indices évidents faciles à deviner, comme la date de naissance. "
        "\nEssayez d'utiliser une référence qui n'est pas facilement associable à vous.",
    "dialog_encrypt_new_password_hint_input_placeholder_text": "Entrez un indice (facultatif)",
    "dialog_encrypt_new_password_button_ok": "OK",
    "dialog_encrypt_new_password_button_cancel": "Annuler",
    "dialog_encrypt_new_password_warning_empty_title": "Avertissement",
    "dialog_encrypt_new_password_warning_empty_text": "Le champ du mot de passe ne peut pas être vide !",
    "dialog_encrypt_new_password_warning_too_long_title": "Avertissement",
    "dialog_encrypt_new_password_warning_too_long_text":
        "Le champ d'indice est trop long, {symbols} caractères maximum !",

    "dialog_encrypt_password_title": "Entrez le mot de passe",
    "dialog_encrypt_password_label": "Mot de passe :",
    "dialog_encrypt_password_input_placeholder_text": "Entrez le mot de passe",
    "dialog_encrypt_password_hint_label": "Indice :",
    "dialog_encrypt_password_button_ok": "OK",
    "dialog_encrypt_password_button_cancel": "Annuler",

    "dialog_encrypt_password_reset_title": "Réinitialiser le mot de passe de chiffrement",
    "dialog_encrypt_password_reset_text":
        "Êtes-vous sûr de vouloir réinitialiser le mot de passe de chiffrement actuel ?",
    "dialog_encrypt_password_reset_button_cancel": "Annuler",
    "dialog_encrypt_password_reset_button_yes": "Oui",

    "dialog_open_link_title": "Lien",
    "dialog_open_link_text": "Ouvrir le lien \"{url}\" dans un navigateur ?",

    "dialog_reset_settings_title": "Réinitialiser les paramètres ?",
    "dialog_reset_settings_text":
        "Toutes les données enregistrées dans les paramètres seront effacées, et l'application redémarrera pour "
        "appliquer les modifications.",

    "dialog_exit_unsaved_title": "Confirmer la Sortie",
    "dialog_exit_unsaved_text": "Le fichier ouvert '{file_name}' ne peut pas être enregistré. Continuer à quitter?",

    "message_app_config_file_access": "Accès refusé lors de l'accès au fichier de configuration de l'application à "
                                      "{file_path}. Définissez les autorisations correctes pour assurer un fonctionnement "
                                      "approprié.",

    "field_dir_path_dialog_caption": "Sélectionner un Répertoire",
    "field_file_path_dialog_caption": "Sélectionner un Fichier",

    "load_file_encryption_password_mismatch": "Non-concordance du mot de passe de chiffrement !",
    "load_file_encryption_password_incorrect": "Mot de passe de chiffrement incorrect !",
    "load_file_none_content_error": "Impossible de charger le fichier.",

    "action_new_file_error_occurred": "Impossible de créer le fichier ; une erreur est survenue."
                                      "\nVérifiez les autorisations du système de fichiers.",
    "save_active_file_error_occurred": "Impossible de sauvegarder le fichier ; une erreur est survenue.",

    "expandable_block_default_title": "Plus d'infos...",
    "expandable_block_open_close_tags_mismatch_warning": "Balises d'ouverture/fermeture du bloc <details> incompatibles",

    "dialog_color_picker_color_copied_to_the_clipboard": "Le texte formaté a été copié dans le presse-papiers",

    "popup_about_title": "Infos de l'Application",
    "popup_about_app_name_description": "Éditeur Markdown Python",

    "popup_about_version": "Version",
    "popup_about_license": "Licence",
    "popup_about_website": "Site Web",
    "popup_about_repository": "GitHub",
    "popup_about_pypi": "PyPi",
    "popup_about_date": "Date",

    "update_helper_new_version_is_available": "Une nouvelle version {latest_version} de l'application est disponible",
    "update_helper_latest_version_installed": "La dernière version de l'application est installée",

    "network_connection_error_empty": "Impossible d'obtenir des informations de réponse",
    "network_connection_error_connection_or_dns":
        "Hôte introuvable. Il pourrait y avoir un problème avec la connexion Internet ou le DNS.",
    "network_connection_error_connection_refused":
        "Connexion refusée. Le serveur pourrait être hors service ou il pourrait y avoir des problèmes de réseau.",
    "network_connection_error_connection_timed_out":
        "La connexion a expiré. Il pourrait y avoir des problèmes de réseau.",
    "network_connection_error_connection_404_error":
        "Erreur 404 de connexion. La page ou la ressource demandée n'est pas trouvée.",
    "network_connection_error_generic_with_status_code": "Échec de la requête avec le code d'état : {status_code}",
}
