from datetime import date
import re
from pathlib import Path
from typing import Dict
from datetime import datetime
import pdfplumber
import docx
import spacy
from Candidate_profile import CandidateProfile
from resume_config import *

class ResumeProcessor:
 
    def __init__(self):
        self.setup_ai_models()
        
    def setup_ai_models(self):
        """Initialize AI models for text processing"""
        # Load spaCy model for NER
        self.nlp = spacy.load("en_core_web_sm")
    
    def extract_text_from_file(self, file_path: str) -> str:
        """Extract text from PDF, DOCX files"""
        file_path = Path(file_path)
        text = ""
        
        try:
            if file_path.suffix.lower() == '.pdf':
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
            
            elif file_path.suffix.lower() == '.docx':
                doc = docx.Document(file_path)
                for paragraph in doc.paragraphs:
                    text += paragraph.text + "\n"
            
        except Exception as e:
            print(f"Error extracting text from {file_path}: {e}")
            
        return text.strip()
    # NAME EXTRACTION AND VALIDATION
    def extract_name(self, text: str) -> str:
        """Extract name from resume text using multiple methods"""
        
        # Method 1: Use regex patterns
        for pattern in NAME_PATTERNS:
            matches = pattern.findall(text)
            if matches:
                potential_name = matches[0].strip()
                potential_name = re.sub(r'^\d+\s+de\s+\d+\s*', '', potential_name)
                potential_name = potential_name.strip()
                
                if potential_name and self.validate_name(potential_name):
                    return potential_name
        
        name = ""
        lines = text.strip().split('\n')
        
        # Method 2: Try table-specific extraction first (bilingual CVs)
        match = re.search(BILINGUAL_PATTERNS, text, re.MULTILINE | re.DOTALL)
        if match:
            potential_name = match.group(1).strip()
            potential_name = re.sub(r'\s+[A-Z]$', '', potential_name)  # Remove single trailing capital
            if self.validate_name(potential_name):
                return potential_name
        
        # Method 3: Try table patterns
        for pattern_tuple in TABLE_PATTERNS:
            pattern = pattern_tuple[0]  # Get pattern string from tuple
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE | re.DOTALL)
            if matches:
                for match in matches:
                    potential_name = match.strip()
                    if self.validate_name(potential_name):
                        return potential_name

        # Method 4: Check the very first line
        if lines:
            first_line = lines[0].strip()
            first_line = re.sub(r'^\d+\s+de\s+\d+\s*', '', first_line)
            first_line = re.sub(r'^Page\s+\d+.*', '', first_line, flags=re.IGNORECASE)
            first_line = first_line.strip()
            
            if first_line:
                if first_line.isupper() and len(first_line.split()) >= 2:
                    words = first_line.split()
                    if all(self.is_likely_name_word(word) for word in words):
                        name = first_line.title()
                        if self.validate_name(name):
                            return name
                
                elif first_line and not first_line.isupper():
                    words = first_line.split()
                    if (2 <= len(words) <= 6 and 
                        all(self.is_valid_name_word(word) for word in words)):
                        if not any(indicator in first_line.lower() for indicator in 
                                ['address', 'phone', 'email', 'mobile', '@', 'street', 'city', 'location']):
                            if self.validate_name(first_line):
                                return first_line
        

        # Method 5: spaCy extraction
        if self.nlp:
            clean_text = re.sub(r'^\d+\s+de\s+\d+\s*', '', text)
            doc = self.nlp(clean_text[:800])
            
            for ent in doc.ents:
                if ent.label_ == "PERSON" and ent.start_char < 300:
                    potential_name = ent.text.strip()
                    if self.validate_name(potential_name):
                        return potential_name

        return ""

    def validate_name(self, name: str) -> bool:
        """Validate extracted name"""
        if not name or len(name) < 3:
            return False
        
        words = name.split()
        
        # Check word count (reasonable range)
        if not (2 <= len(words) <= 6):
            return False
        
        # Each word should be a valid name component
        for word in words:
            if not self.is_valid_name_word(word):
                return False
        
        # Explicit blacklist of common false positives
        if name.lower() in FALSE_POSITIVE_NAMES:
            return False
        
        # If any word in the name is a non-name word, reject it
        name_words_lower = [word.lower().rstrip('.,;:-') for word in words]
        if any(word in NON_NAME_VALIDATION_WORDS for word in name_words_lower):
            return False
        
        # Additional check: names shouldn't contain common CV section headers
        if any(section in name.lower() for section in CV_SECTIONS):
            return False
        
        
        return True

    def is_valid_name_word(self, word: str) -> bool:
        """Enhanced name word validation"""
        clean_word = word.rstrip('.,;:-')
                
        # Must be alphabetic (allowing hyphens and apostrophes)
        if not (clean_word.replace('-', '').replace("'", "").isalpha() or 
                any(ord(c) > 127 for c in clean_word)):
            return False
        
        # Enhanced blacklist
        return clean_word.lower() not in NON_NAME_WORDS
    
    def is_likely_name_word(self, word: str) -> bool:
        """Check if word is likely part of a name (for all-caps detection)"""
        clean_word = word.replace('-', '').replace("'", "")
        return (clean_word.isalpha() and 
                len(clean_word) >= 2 and 
                len(clean_word) <= 25 and
                word.lower() not in ['page', 'date', 'phone', 'email'])
    # EDUCATION EXTRACTION AND VALIDATION
    def extract_education(self, text: str) -> str:
        """Extract education information from resume text"""
        text_lower = text.lower()

        for pattern in EDUCATION_PATTERNS:
            matches = re.findall(pattern, text_lower, re.IGNORECASE | re.MULTILINE | re.DOTALL)
            for match in matches:
                # If match is a tuple, get the first non-empty group
                if isinstance(match, tuple):
                    education = ', '.join(m.strip() for m in match if m and len(m.strip()) > 2)
                else:
                    education = match
                
                education = education.strip()
                
                # Handle special case for professional titles with institutions
                if '(' in education and ('university' in education.lower() or 'college' in education.lower() or 'institute' in education.lower()):
                    parts = education.split(',')
                    if len(parts) >= 2:
                        title = parts[0].strip()
                        institution_part = parts[-1].strip()
                        if '(' in institution_part:
                            institution = institution_part.split('(')[0].strip()
                            education = f"{title}, {institution}"
                
                # If the pattern starts with 'degree', prepend 'Degree' to the result
                elif pattern.startswith(r'degree\s+([A-Za-z]'):
                    education = f"Degree {education}"
                
                # Clean up the match
                education = re.sub(r'\s+', ' ', education)
                education = education.strip('.,;:-')
                
                if self.validate_education(education):
                    return education.title()

        return ""

    def validate_education(self, education: str) -> bool:
        """Validate extracted education entry"""
        if not education or len(education.strip()) < 3:
            return False
        
        education_lower = education.lower().strip()
        
        # Length check - reasonable education description
        if len(education) > 250:
            return False
        
        # Exclude obvious non-education content
        exclusion_words = [
            'phone', 'email', 'address', 'contact', 'mobile', 'tel', 'fax',
            'years of experience', 'work experience', 'employment', 'salary',
            'date of birth', 'nationality', 'marital status', 'gender',
            'responsibilities', 'duties', 'skills', 'languages', 'hobbies',
            'references', 'objective', 'summary', 'profile', 'career',
            'designation', 'position', 'title', 'role', 'company', 'organization',
            'years of', 'date of', 'joining', 'intertek'
        ]
        
        if any(word in education_lower for word in exclusion_words):
            return False
        
        # Must contain at least one education-related keyword
        education_keywords = [
            'degree', 'bachelor', 'master', 'phd', 'diploma', 'certificate',
            'administration', 'engineering', 'science', 'arts', 'business',
            'management', 'technology', 'studies', 'medicine', 'law',
            'university', 'college', 'institute', 'school', 'education',
            'qualification', 'academic', 'graduation', 'mba', 'bba',
            'translator', 'secretary', 'analyst', 'specialist', 'consultant',
            'coordinator', 'administrator', 'manager', 'assistant', 'technician',
            'literary', 'scientific', 'public'
        ]
        
        has_education_keyword = any(keyword in education_lower for keyword in education_keywords)
        is_exact_education_keyword = any(education_lower == keyword for keyword in education_keywords)        
        
        if not has_education_keyword and len(education.strip()) < 10:
            return False
        
        if is_exact_education_keyword:
            return False
        
        # Should not start with numbers (likely years or dates)
        if re.match(r'^\d', education.strip()):
            return False
        
        # Should contain at least one alphabetic character
        if not re.search(r'[A-Za-z]', education):
            return False
        
        # Special validation for specific cases
        if 'public' in education_lower and 'administration' in education_lower:
            return True
        
        return has_education_keyword
    # CURRENT ROLE EXTRACTION AND VALIDATION
    def extract_current_role(self, text: str) -> str:
        """Extract current job role using pattern matching"""
        for pattern in ROLE_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            if matches:
                first_match = matches[0]
                if isinstance(first_match, tuple):
                    role = " ".join([m for m in first_match if m]).strip()
                else:
                    role = first_match.strip()
                if self.validate_current_role(role):
                    return role
        
        return ""

    def validate_current_role(self, role: str) -> bool:
        """Validate extracted current role"""
        if not role or len(role.strip()) < 2:
            return False
        
        role = role.strip()
        role_lower = role.lower()
        
        # Length check
        if len(role) > 100:
            return False
        
        # Should contain alphabetic characters
        if not re.search(r'[A-Za-z]', role):
            return False
        
        # Exclude obvious non-role content
        exclusion_words = [
            'phone', 'email', 'address', 'contact', 'mobile', 'tel', 'fax',
            'date of birth', 'nationality', 'marital status', 'gender',
            'years of experience', 'salary', 'references', 'hobbies'
        ]
        
        if any(word in role_lower for word in exclusion_words):
            return False
        
        # Should not be just numbers or dates
        if re.match(r'^\d+[\d\s/.-]*$', role.strip()):
            return False
        
        return True
    # LOCATION EXTRACTION AND VALIDATION
    def extract_current_address(self, text: str) -> str:
        """Extract current address/location from resume text"""
        if not text or len(text.strip()) < 10:
            return ""
        
        lines = text.strip().split('\n')
        
        # Method 1: Try labeled patterns first
        for pattern in LOCATION_LABEL_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            if matches:
                for match in matches:
                    location = match.strip().rstrip('.,;:-|')
                    if self.validate_location(location):
                        return location
        
        # Method 2: Check the first few lines for header format
        for line in lines[:8]:  # Check first 8 lines
            line = line.strip()
            
            # Skip lines that are clearly not locations
            if any(word in line.lower() for word in NON_LOCATION_WORDS):
                continue
            
            # Pattern: Single word that could be a city
            if re.match(r'^[A-Z][a-zA-Z]{3,15}$', line):
                if self.validate_location(line):
                    return line
            
            # Pattern: City, Country format or City - Country format
            if re.match(r'^[A-Z][a-zA-Z\s]+[,-]\s*[A-Z][a-zA-Z\s]+$', line):
                if self.validate_location(line):
                    return line
        
        # Method 3: Use NLP for geographic entities
        if self.nlp:
            doc = self.nlp(text)
            locations = [ent.text for ent in doc.ents if ent.label_ in ["GPE", "LOC"]]
            if locations:
                filtered_locations = [loc for loc in locations if len(loc.split()) <= 3]
                if filtered_locations and self.validate_location(filtered_locations[0]):
                    return filtered_locations[0]
        
        return ""

    def validate_location(self, location: str) -> bool:
        """Validate extracted location"""
        if not location or len(location.strip()) < 2:
            return False
        
        location = location.strip()
        location_lower = location.lower()
        words = location.split()
        
        # Basic validation
        if len(location) > 50 or any(word.lower() in NON_LOCATION_WORDS for word in words):
            return False
        
        # Technical terms check
        technical_indicators = [
            'experience', 'years', 'engineer', 'developer', 'manager',
            'phone', 'email', 'mobile', 'address', 'qualification',
            'education', 'university', 'college', 'degree', 'skills'
        ]
        
        if any(indicator in location_lower for indicator in technical_indicators):
            return False
        
        # Single word locations
        if len(words) == 1:
            return (location.replace('-', '').replace("'", "").isalpha() and
                   2 <= len(location) <= 25)
        
        # Multi-word locations - check for country names
        for country in COUNTRIES:
            if country.lower() in location_lower:
                return True
        
        # Check city-country patterns
        if ',' in location or '-' in location:
            parts = re.split(r'[,-]', location)
            if len(parts) == 2:
                potential_country = parts[1].strip()
                if potential_country.lower() in [c.lower() for c in COUNTRIES]:
                    return True
        
        # Multi-word validation without country
        return all(word.strip('.,;:-').replace('-', '').replace("'", "").isalpha() 
                  for word in words)
    # NATIONALITY EXTRACTION AND VALIDATION
    def extract_nationality(self, text: str) -> str:
        """Extract nationality from resume text"""
        # Common character replacements for corrupted text
        replacements = {
            'Ɵ': 't', 'ƫ': 't', 'ť': 't', 'ţ': 't', 'ṭ': 't', '†': 't',
            'ı': 'i', 'í': 'i', 'ì': 'i', '1': 'l', '0': 'o',
            'ö': 'o', 'ó': 'o', 'ò': 'o', 'ø': 'o',
        }
        
        # Apply replacements to the text    
        for corrupted, correct in replacements.items():
            text = text.replace(corrupted, correct)
        
        # Try nationality patterns first
        for pattern in NATIONALITY_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
            if matches:
                for match in matches:
                    nationality = match.strip()
                    if self.validate_nationality(nationality):
                        return nationality
        
        # If no nationality found, use current residence as fallback
        current_residence = self.extract_current_address(text)
        if current_residence:
            # Extract country name from residence if it contains one
            for country in COUNTRIES:
                if country.lower() in current_residence.lower():
                    return country
            # If no country found in residence, return the residence itself
            return current_residence
        
        return ""

    def validate_nationality(self, nationality: str) -> bool:
        """Validate extracted nationality"""
        if not nationality or len(nationality.strip()) < 3:
            return False
        
        nationality = nationality.strip()
        nationality_lower = nationality.lower()
        
        # Check if it ends with common nationality suffixes
        nationality_suffixes = ['ian', 'an', 'ese', 'ish', 'i', 'e']
        if any(nationality_lower.endswith(suffix) for suffix in nationality_suffixes):
            return True       
        
        # Check against countries list
        return any(country.lower() == nationality_lower for country in COUNTRIES)
    # AGE EXTRACTION AND VALIDATION
    def extract_age(self, text: str) -> int:
        """Extract age from resume text"""
        # Method 1: Extract age from explicit age mentions
        age_matches = AGE_PATTERN.findall(text)
        if age_matches:
            age = int(age_matches[0])
            if self.validate_age(age):
                return age
        
        # Method 2: Extract birth date and calculate age
        for pattern in BIRTH_DATE_PATTERNS:
            match = pattern.search(text)
            if match:
                try:
                    groups = match.groups()
                    
                    if len(groups) == 1:  # Year only
                        birth_str = groups[0]
                    elif len(groups) == 2:  # MM/YYYY format
                        birth_str = f"01/{groups[0]}/{groups[1]}"  # Assume 1st day of month
                    elif len(groups) == 3:  # DD/MM/YYYY format
                        birth_str = f"{groups[0]}/{groups[1]}/{groups[2]}"
                    
                    calculated_age = self.calculate_age_from_birth_date(birth_str)
                    if self.validate_age(calculated_age):
                        return calculated_age
                        
                except Exception as e:
                    print(f"Birth date parsing failed: {e}")
                    continue
        
        return 0

    def validate_age(self, age: int) -> bool:
        """Validate extracted age"""
        return 0 <= age <= 100

    def calculate_age_from_birth_date(self, birth_date_str: str) -> int:
        """Calculate age from birth date string"""
        try:
            current_date = date.today()
            birth_date_str = birth_date_str.strip()
            month_map = MONTH_MAP
            
            # check if month is written in letters
            if '/' in birth_date_str and len(birth_date_str.split('/')) >= 2:
                month = birth_date_str.split('/')[1].lower()
                if month in month_map:
                    month = str(month_map[month])
                    birth_date_str = f"{birth_date_str.split('/')[0]}/{month}/{birth_date_str.split('/')[2]}"
            
            date_formats = DATE_FORMATS
            birth_date = None
            
            for fmt in date_formats:
                try:
                    if fmt == '%Y':
                        birth_date = datetime.strptime(birth_date_str, fmt).date()
                        birth_date = birth_date.replace(month=1, day=1)
                    elif fmt in ('%m/%y', '%m/%Y', '%m-%y', '%m-%Y'):
                        temp_date = datetime.strptime(birth_date_str, fmt).date()
                        birth_date = temp_date.replace(day=1)
                    else:
                        birth_date = datetime.strptime(birth_date_str, fmt).date()
                        
                    if birth_date.year < 100:
                        if birth_date.year > 50:
                            birth_date = birth_date.replace(year=birth_date.year + 1900)
                        else:
                            birth_date = birth_date.replace(year=birth_date.year + 2000)
                            
                    break
                except ValueError:
                    continue
            
            if birth_date:
                age = current_date.year - birth_date.year
                if current_date.month < birth_date.month or \
                (current_date.month == birth_date.month and current_date.day < birth_date.day):
                    age -= 1
                return age if 0 <= age <= 100 else 0
                
        except Exception as e:
            print(f"Error calculating age from birth date '{birth_date_str}': {e}")
        
        return 0
    # EMAIL EXTRACTION AND VALIDATION
    def extract_email(self, text: str) -> str:
        """Extract email from resume text"""
        email_matches = EMAIL_PATTERN.findall(text)
        if email_matches:
            email = email_matches[0]
            if self.validate_email(email):
                return email
        return ""

    def validate_email(self, email: str) -> bool:
        """Validate extracted email"""
        if not email:
            return False
        
        # Basic email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_pattern, email))
    # PHONE EXTRACTION AND VALIDATION
    def extract_phone(self, text: str) -> str:
        """Extract phone number from resume text"""
        phone_matches = PHONE_PATTERN.findall(text)
        if phone_matches:
            phone = phone_matches[0]
            if self.validate_phone(phone):
                return phone
        return ""

    def validate_phone(self, phone: str) -> bool:
        """Validate extracted phone number"""
        if not phone:
            return False
        
        # Remove common phone number separators
        clean_phone = re.sub(r'[^\d+]', '', phone)
        
        # Should have reasonable length (6-15 digits)
        if len(clean_phone) < 6 or len(clean_phone) > 15:
            return False
        
        # Should contain mostly digits
        return bool(re.match(r'^[\d+\s\-()\.]{6,20}$', phone))
    # MAIN PROCESSING METHODS
    def extract_personal_info(self, text: str) -> Dict:
        """Extract all personal information using individual extraction methods"""
        info = {}
        
        info['name'] = self.extract_name(text)
        info['email'] = self.extract_email(text)
        info['phone'] = self.extract_phone(text)
        info['age'] = self.extract_age(text)
        info['current_residence'] = self.extract_current_address(text)
        info['nationality'] = self.extract_nationality(text)
        
        return info
   
    def calculate_match_score(self, profile: CandidateProfile, criteria: Dict) -> float:
        """Calculate match score based on filtering criteria"""
        score = 0.0
        total_criteria = 0
        
        # Age matching
        if criteria.get('min_age', 0) > 0 or criteria.get('max_age', 100) < 100:
            total_criteria += 1
            min_age = criteria.get('min_age', 0)
            max_age = criteria.get('max_age', 100)
            if min_age <= profile.age <= max_age:
                score += 1.0
        
        # Location matching
        if criteria.get('location', ''):
            total_criteria += 1
            if criteria['location'].lower() in profile.current_residence.lower():
                score += 1.0
        
        # Role matching
        if criteria.get('role', ''):
            total_criteria += 1
            if criteria['role'].lower() in profile.current_role.lower():
                score += 1.0
         
        # Education matching
        if criteria.get('education', ''):
            total_criteria += 1
            if criteria['education'].lower() in profile.education.lower():
                score += 1.0
                
        return score / total_criteria if total_criteria > 0 else 0.0 
        
    def process_resume(self, file_path: str, criteria: Dict = None) -> CandidateProfile:
        """Process a single resume and extract all information"""
        text = self.extract_text_from_file(file_path)
        
        if not text:
            return CandidateProfile(file_path=file_path)
        
        # Extract personal information
        personal_info = self.extract_personal_info(text)
        
        # Create candidate profile
        profile = CandidateProfile(
            name=personal_info.get('name', ''),
            age=personal_info.get('age', 0),
            current_residence=personal_info.get('current_residence', ''),
            nationality=personal_info.get('nationality', ''),
            education=self.extract_education(text),
            current_role=self.extract_current_role(text),
            email=personal_info.get('email', ''),
            phone=personal_info.get('phone', ''),
            raw_text=text[:500] + "..." if len(text) > 500 else text,
            file_path=file_path
        )
        
        # Calculate match score if criteria provided
        if criteria:
            profile.match_score = self.calculate_match_score(profile, criteria)
        
        return profile