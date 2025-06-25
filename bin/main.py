import sys
from PyQt6.QtWidgets import QApplication
import GUI

def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Intelligent Resume Classifier")
    app.setApplicationVersion("1.0.0")
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = GUI.ResumeClassifierGUI()
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()