import sys
import re
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QTextEdit,
    QComboBox, QPushButton, QFormLayout, QMessageBox, QHBoxLayout
)
from PyQt5.QtCore import Qt

class FormValidator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Formulir Validasi")
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout()

        # Input Fields
        self.nama_input = QLineEdit()
        self.email_input = QLineEdit()
        self.umur_input = QLineEdit()

        # Nomor HP (dengan prefix +62)
        self.hp_input = QLineEdit()
        self.hp_input.textChanged.connect(self.format_hp_input)

        hp_layout = QHBoxLayout()
        hp_layout.addWidget(QLabel("+62"))
        hp_layout.addWidget(self.hp_input)

        self.alamat_input = QTextEdit()
        self.gender_input = QComboBox()
        self.gender_input.addItems(["", "Laki-laki", "Perempuan"])
        self.pendidikan_input = QComboBox()
        self.pendidikan_input.addItems(["", "SMA", "D3", "S1", "S2", "S3"])

        # Buttons
        self.save_button = QPushButton("Simpan")
        self.clear_button = QPushButton("Hapus")

        # Add Widgets
        layout.addRow("Nama", self.nama_input)
        layout.addRow("Email", self.email_input)
        layout.addRow("Umur", self.umur_input)
        layout.addRow("No. HP", hp_layout)
        layout.addRow("Alamat", self.alamat_input)
        layout.addRow("Jenis Kelamin", self.gender_input)
        layout.addRow("Pendidikan", self.pendidikan_input)
        layout.addRow(self.save_button, self.clear_button)

        # Footer
        self.footer = QLabel("Nama: Muhammad Ridho Fahru Rozy\nNIM: F1D022076")
        layout.addRow(self.footer)

        self.setLayout(layout)

        # Connect
        self.save_button.clicked.connect(self.validate_form)
        self.clear_button.clicked.connect(self.clear_form)

    def format_hp_input(self):
        current_text = self.hp_input.text()
        digits_only = re.sub(r"\D", "", current_text) 

        parts = []
        if len(digits_only) <= 3:
            parts = [digits_only]
        elif len(digits_only) <= 7:
            parts = [digits_only[:3], digits_only[3:]]
        else:
            parts = [digits_only[:3], digits_only[3:7], digits_only[7:11]]

        formatted = " ".join(parts)
        cursor_pos = self.hp_input.cursorPosition()

        # Hindari efek rekursif
        self.hp_input.blockSignals(True)
        self.hp_input.setText(formatted)
        self.hp_input.setCursorPosition(min(cursor_pos, len(formatted)))
        self.hp_input.blockSignals(False)

    def validate_form(self):
        nama = self.nama_input.text().strip()
        email = self.email_input.text().strip()
        umur = self.umur_input.text().strip()
        no_hp = self.hp_input.text().strip().replace(" ", "")  
        alamat = self.alamat_input.toPlainText().strip()
        gender = self.gender_input.currentText().strip()
        pendidikan = self.pendidikan_input.currentText().strip()

        if not all([nama, email, umur, no_hp, alamat, gender, pendidikan]):
            QMessageBox.warning(self, "Peringatan", "Semua field harus diisi!")
            return

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            QMessageBox.warning(self, "Peringatan", "Format email tidak valid!")
            return

        if not no_hp.isdigit() or len(no_hp) < 9:
            QMessageBox.warning(self, "Peringatan", "Nomor HP minimal 9 digit!")
            return

        if not umur.isdigit():
            QMessageBox.warning(self, "Peringatan", "Umur harus berupa angka!")
            return

        QMessageBox.information(self, "Sukses", "Data berhasil disimpan!")

    def clear_form(self):
        self.nama_input.clear()
        self.email_input.clear()
        self.umur_input.clear()
        self.hp_input.clear()
        self.alamat_input.clear()
        self.gender_input.setCurrentIndex(0)
        self.pendidikan_input.setCurrentIndex(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FormValidator()
    window.show()
    sys.exit(app.exec_())
