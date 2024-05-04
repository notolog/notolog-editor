from PySide6.QtWidgets import QApplication


class ClipboardHelper:
    @staticmethod
    def set_text(text):
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
