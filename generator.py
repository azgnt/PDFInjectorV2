import sys
import os
import pyfiglet
from termcolor import colored
import fitz  # PyMuPDF
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QFileDialog, QWidget, QComboBox, QMessageBox, QProgressBar, QInputDialog
)
from PySide6.QtCore import Qt

# Mock AI Payload Generator (replace with actual AI logic)
def generate_payload(payload_type):
    # Placeholder for AI-generated payload logic
    return f"Generated {payload_type} payload"

# Display the banner
def display_banner():
    ascii_art = pyfiglet.figlet_format("PDFInjector v2", font="slant")
    ascii_art_author = pyfiglet.figlet_format("By Kdairatchi", font="digital")
    print(colored(ascii_art, 'cyan'))
    print(colored(ascii_art_author, 'magenta'))

class PDFInjectorV2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Injector v2")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()
        self.create_widgets()

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def create_widgets(self):
        self.add_label("Input PDF:")
        self.input_pdf_lineedit = self.add_line_edit()
        self.add_button("Browse", self.browse_input_pdf)

        self.add_label("Output PDF:")
        self.output_pdf_lineedit = self.add_line_edit()
        self.add_button("Browse", self.browse_output_pdf)

        self.add_label("Payload Type:")
        self.payload_type_combobox = QComboBox()
        self.payload_type_combobox.addItems(["Backdoor", "Password Stealer", "Cookie Stealer", "Geo Location", "Mic/Cam Access"])
        self.layout.addWidget(self.payload_type_combobox)

        self.add_button("Generate Payload", self.generate_payload)

        self.add_label("Communication Method:")
        self.communication_combobox = QComboBox()
        self.communication_combobox.addItems(["Telegram", "Discord"])
        self.layout.addWidget(self.communication_combobox)

        self.add_button("Inject Payload", self.inject_payload)

        self.progress_bar = QProgressBar(self)
        self.layout.addWidget(self.progress_bar)

    def add_label(self, text):
        label = QLabel(text)
        self.layout.addWidget(label)

    def add_line_edit(self):
        line_edit = QLineEdit()
        self.layout.addWidget(line_edit)
        return line_edit

    def add_button(self, text, slot):
        button = QPushButton(text)
        button.clicked.connect(slot)
        self.layout.addWidget(button)

    def browse_input_pdf(self):
        self.browse_file("Select Input PDF", self.input_pdf_lineedit)

    def browse_output_pdf(self):
        self.browse_file("Select Output PDF", self.output_pdf_lineedit, save=True)

    def browse_file(self, dialog_title, line_edit, save=False):
        file_name, _ = (QFileDialog.getSaveFileName if save else QFileDialog.getOpenFileName)(
            self, dialog_title, "", "PDF Files (*.pdf);;All Files (*)"
        )
        if file_name:
            line_edit.setText(file_name)

    def generate_payload(self):
        payload_type = self.payload_type_combobox.currentText()
        payload = generate_payload(payload_type)
        QMessageBox.information(self, "Payload Generated", f"{payload_type} payload generated:\n{payload}")

    def inject_payload(self):
        input_pdf = self.input_pdf_lineedit.text()
        output_pdf = self.output_pdf_lineedit.text()
        communication_method = self.communication_combobox.currentText()
        self.progress_bar.setValue(0)

        if not self.validate_inputs([input_pdf, output_pdf]):
            return

        try:
            doc = fitz.open(input_pdf)
            # Example: Injecting payload as text
            for page in doc:
                page.insert_text((72, 72), "Injected Payload", fontsize=12)

            doc.save(output_pdf)
            doc.close()

            QMessageBox.information(self, "Success", f"Payload injected successfully! Using {communication_method} for notifications.")
        except Exception as e:
            self.show_error_message("An error occurred while injecting the payload.", e)

    def validate_inputs(self, inputs):
        if any(not input_field for input_field in inputs):
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            return False
        return True

    def show_error_message(self, message, exception):
        QMessageBox.critical(self, "Error", f"{message}\nDetails: {exception}")

if __name__ == "__main__":
    display_banner()
    app = QApplication(sys.argv)
    window = PDFInjectorV2()
    window.show()
    sys.exit(app.exec())
