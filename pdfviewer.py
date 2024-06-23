from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
import subprocess
import sys, os

class ReportViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yearly Report Viewer")
        self.setGeometry(100, 100, 800, 600)
        self.reportViewer = QTextEdit()
        self.reportViewer.setReadOnly(True)
        self.printButton = QPushButton("Print Report")
        self.printButton.clicked.connect(self.print_report)
        global currentYear

        layout = QVBoxLayout()
        layout.addWidget(self.reportViewer)
        layout.addWidget(self.printButton)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.load_report_data()

    def load_report_data(self):
        # Placeholder for report data generation
        report_data = self.generate_report_data()
        self.reportViewer.setText(report_data)

    def generate_report_data(self):
        import sqlite3
        # Connect to the SQLite database
        conn = sqlite3.connect('db.db')
        cursor = conn.cursor()
        currentYear = 2024

        # SQL query to select yearly duty data, using parameterized queries for safety
        query = "SELECT * FROM dutychart WHERE dateYear = ?"
        
        try:
            # Execute the query with currentYear as a parameter
            cursor.execute(query, (currentYear,))
            # Fetch all results
            results = cursor.fetchall()
            # Process results (this is a placeholder, adjust as needed)
            report_data = "Yearly Report Data Here\n"
            for row in results:
                report_data += f"{row}\n"
        except sqlite3.Error as e:
            report_data = f"Error fetching data: {e}"
        finally:
            # Close the connection
            conn.close()
        
        return report_data
    
    def print_report(self):
        printer = QPrinter()
        printer.setOutputFormat(QPrinter.PdfFormat)
        
        # Set the resolution if needed, for example to 600 dpi
        # printer.setResolution(600)
        
        # Construct the path for the PDF file inside the 'reports' folder of the program root directory
        program_root = os.path.dirname(os.path.abspath(__file__))
        reports_folder = os.path.join(program_root, 'reports')
        pdf_path = os.path.join(reports_folder, 'report.pdf')
        
        # Ensure the 'reports' folder exists
        if not os.path.exists(reports_folder):
            os.makedirs(reports_folder)
        
        printer.setOutputFileName(pdf_path)
    
        # Directly print without showing the print dialog
        self.reportViewer.print_(printer)
        # After saving the PDF, open it in your own viewer
        self.print_pdf(pdf_path)

    def print_pdf(self, pdf_path):
        # Adjust the command according to the user's OS
        if sys.platform == "win32":
            # Example: Open with the default PDF viewer
            subprocess.run(["start", pdf_path], shell=True, check=True)
        # Add more platform-specific commands as needed

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = ReportViewer()
    viewer.show()
    sys.exit(app.exec())