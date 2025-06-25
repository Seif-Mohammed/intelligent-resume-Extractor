
from typing import Dict, List

from PyQt6.QtCore import QThread, pyqtSignal
from  Resume_Processor import ResumeProcessor

class ProcessingThread(QThread):
    """Thread for processing resumes without blocking UI"""
    progress_updated = pyqtSignal(int)
    resume_processed = pyqtSignal(object)  # CandidateProfile
    processing_finished = pyqtSignal()
    
    def __init__(self, file_paths: List[str], criteria: Dict):
        super().__init__()
        self.file_paths = file_paths
        self.criteria = criteria
        self.processor = ResumeProcessor()
    
    def run(self):
        for i, file_path in enumerate(self.file_paths):
            profile = self.processor.process_resume(file_path, self.criteria)
            self.resume_processed.emit(profile)
            
            progress = int((i + 1) / len(self.file_paths) * 100)
            self.progress_updated.emit(progress)
        
        self.processing_finished.emit()