
from typing import List
from dataclasses import dataclass

@dataclass
class CandidateProfile:
    """Data class to store extracted candidate information"""
    name: str = ""
    age: int = 0
    current_residence: str = ""
    education: str = ""
    current_role: str = ""
    email: str = ""
    phone: str = ""
    nationality: str = ""
    languages: List[str] = None
    certifications: List[str] = None
    raw_text: str = ""
    file_path: str = ""
    match_score: float = 0.0
    
    def __post_init__(self):
        if self.languages is None:
            self.languages = []
        if self.certifications is None:
            self.certifications = []
