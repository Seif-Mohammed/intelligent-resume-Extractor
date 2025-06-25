# Configuration file for Resume Processor
# Contains all lists, patterns, and mappings used in resume processing
import re

EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
PHONE_PATTERN = re.compile(r'[\+]?[1-9]?[0-9]{7,14}')
AGE_PATTERN = re.compile(r'\b(?:age|years old|yr old)\s*:?\s*(\d{1,2})\b', re.IGNORECASE)
        
# Birth date regex patterns - consolidated from Resume_Processor.py
        # Consolidated birth date patterns
BIRTH_DATE_PATTERNS = [
    # e.g. "Date of Birth: 12/05/1985" (DD/MM/YYYY)
    re.compile(r'\b(?:born|birth|dob|date\s*of\s*birth)\s*:?\s*(\d{1,2})\s*[\/\-]\s*(\d{1,2})\s*[\/\-]\s*(\d{4})\b', re.IGNORECASE),
    re.compile(r'(?:date\s*of\s*birth|birth\s*date|dob|born):?\s*(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{4})', re.IGNORECASE),
    re.compile(r'(?:date\s*of\s*birth|birth\s*date|dob|born)\s*:?\s*(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{4})', re.IGNORECASE),
    re.compile(r'(?:date\s*of\s*birth|birth\s*date|dob|born)\s*:?\s*(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{4})', re.IGNORECASE),
    # e.g. "Date of Birth: 12.05.85" (DD.MM.YYYY)
    re.compile(r'\b(?:born|birth|dob|date\s*of\s*birth)\s*:?\s*(\d{1,2})\.(\d{1,2})\.(\d{4})\b', re.IGNORECASE),
    # e.g. "Date of Birth: 12/05/85" (DD/MM/YY)
    re.compile(r'\b(?:born|birth|dob|date\s*of\s*birth)\s*:?\s*(\d{1,2})\s*[\/\-]\s*(\d{1,2})\s*[\/\-]\s*(\d{2})\b', re.IGNORECASE),
    # e.g. "Date of Birth: 12-05-1985" (DD-MM-YYYY)
    re.compile(r'\b(?:born|birth|dob|date\s*of\s*birth)\s*:?\s*(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{4})\b', re.IGNORECASE),
    # e.g. "Date of Birth: 12-05-85" (DD-MM-YY)
    re.compile(r'\b(?:born|birth|dob|date\s*of\s*birth)\s*:?\s*(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{2})\b', re.IGNORECASE),
    # e.g. "Date of Birth: 1985-05-12" (YYYY-MM-DD)
    re.compile(r'\b(?:born|birth|dob|date\s*of\s*birth)\s*:?\s*(\d{4})-(\d{1,2})-(\d{1,2})\b', re.IGNORECASE),
    # e.g. "Date of Birth: 1985" (YYYY)
    re.compile(r'\b(?:born|birth|dob|date\s*of\s*birth)\s*:?\s*(\d{4})\b', re.IGNORECASE),
    # e.g. "Date of Birth: 12 May 1985" (DD Month YYYY)
    re.compile(r'\b(?:born|birth|dob|d\.\s*of\s*birth|date\s*of\s*birth)\s*:?\s*(\d{1,2})\s+([a-z]{3,9})\s+(\d{4})\b', re.IGNORECASE),
    # e.g. "Date of Birth: 12/1985" (MM/YYYY)
    re.compile(r'\b(?:born|birth|dob|date\s*of\s*birth)\s*:?\s*'r'(\d{1,2})\s*[\/\-]\s*(\d{2,4})\b', re.IGNORECASE),
    # e.g. "12/05/1985" (DD/MM/YYYY) without label
    re.compile(r'\b(\d{1,2})\s*[\/\-]\s*(\d{1,2})\s*[\/\-]\s*(\d{4})\b'),
    # e.g. "1985-05-12" (YYYY-MM-DD) without label
    re.compile(r'\b(\d{4})-(\d{1,2})-(\d{1,2})\b'),
    # e.g. "Date of Birth: 12/85" (MM/YY)
    re.compile(r'\b(?:born|birth|dob|date\s*of\s*birth)\s*:?\s*(\d{1,2})\s*[\/\-]\s*(\d{2})\b', re.IGNORECASE),
    # e.g. "12/85" (MM/YY) without label
    re.compile(r'\b(\d{1,2})[\/\-](\d{2})\b'),
]

# Consolidated name patterns - removed many redundant patterns
NAME_PATTERNS = [
    re.compile(r'Name\s+of\s+Person\s+([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)*?)(?=\s*\n)', re.IGNORECASE | re.MULTILINE),    re.compile(r'^\s*(?:FullName|Name\s+of\s+Person|full\s*name|Complete\s*Name|complete\s*name|name)[\s:-]*([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)*)\s*(?=[\n\.]|$)', re.IGNORECASE | re.MULTILINE),
    re.compile(r'(?:االســـــــــــم|Name)\s*\n.*?\n([A-ZÀ-ÿ][a-zà-ÿ]+(?:\s+[A-ZÀ-ÿ][a-zà-ÿ]+){1,4})', re.IGNORECASE | re.MULTILINE | re.DOTALL),
    re.compile(r'Name\s*\n.*?\n([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,4}(?:\s+[A-Z][a-z]+)?)', re.IGNORECASE | re.MULTILINE | re.DOTALL),
    # for names in beginning of the document
    re.compile(r'^([A-Z]+(?: [A-Z]+)+)\s*$', re.MULTILINE),

]

# Fallback patterns name in table
TABLE_PATTERNS = [
    # Look for "Name" followed by English name (skipping Arabic)
    (r'Name\s*[\r\n]+(?:[^\r\n]*[\u0600-\u06FF][^\r\n]*[\r\n]+)?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,4})', 'name_label'),
    # Standard colon pattern
    (r'(?:Name|Full\s+Name)\s*[:|]\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,4})', 'colon'),
    # Table cell pattern
    (r'\|\s*(?:Name|Full\s+Name)\s*\|\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,4})\s*\|', 'pipe'),
]

# This pattern looks for: Arabic name section -> "Name" -> Arabic name -> English name
BILINGUAL_PATTERNS = r'االســـ*م\s*[\r\n]+\s*Name\s*[\r\n]+\s*[^\r\n]*[\u0600-\u06FF][^\r\n]*[\r\n]+\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+(?:\s+[A-Z][a-z]+)*)'

EDUCATION_PATTERNS = [
    # General education section pattern in case education is written as it is or like this "E D U C A T I O N"
    r'\bE\s*D\s*U\s*C\s*A\s*T\s*I\s*O\s*N\b\s*[:\n]\s*([^\n]+(?:\n(?![A-Z][A-Z\s]*[A-Z])[^\n]+)*?)(?=\n\s*(?:experience|work|employment|skills|certifications|years\s+of|date\s+of|designation|$))',
    # Academic qualifications pattern
    r'academic\s+qualifications?\s*[:\n]\s*([A-Za-z][A-Za-z\s&]+(?:administration|engineering|science|arts|business|management|technology|studies|medicine|law|diploma|certificate|degree))',
    # Pattern for "BS in [Subject] ([Year]), [University]"
    r'BS\s+in\s+([^(]+)\s*\([^)]*(\d{4})[^)]*\)\s*,?\s*([^,\n]+)',
    # Pattern for "Bachelor/Master in [Subject], [University]"
    r'(?:Bachelor|Master|BS|MS|BA|MA|PhD)\s+(?:in|of)\s+([^,\n]+(?:Science|Technology|Engineering|Arts|Administration|Studies))[^,\n]*,?\s*([^,\n]+(?:University|College|Institute))',
    # Pattern for degree followed by university
    r'([A-Z][a-z]+\s+(?:in|of)\s+[^,\n]+(?:Science|Technology|Engineering|Arts|Studies))[^,\n]*,?\s*([^,\n]+(?:University|College|Institute))',
    # Pattern for university name with degree
    r'([^,\n]+(?:University|College|Institute))[^,\n]*(?:BS|MS|Bachelor|Master|Degree)\s+(?:in|of)\s+([^,\n]+)',
    # Pattern for tabular format: "Academic Qualifications" followed by degree info
    r'(?:Academic\s+Qualifications?|المؤهالت\s+العلمية)[^:]*:?\s*([^,\n]+(?:BS|MS|Bachelor|Master|Degree|Science|Technology|Engineering))[^,\n]*([^,\n]+(?:University|College|Institute))?',
    # General education section patterns
    r'(?i)education\s*[:\n]\s*(.*?(?:university|college|institute).*?(?:\d{4}).*?)(?=\n\s*(?:[A-Z][A-Z\s]*[A-Z]|$))',
    # Pattern for "تخصص" (specialization) which often follows degree info
    r'(BS|MS|Bachelor|Master|Degree)\s+(?:in|of)?\s*([^,\n]+(?:Science|Technology|Engineering|Arts))[^,\n]*(?:تخصص|specialization)',
    # General pattern for common degree abbreviations
    r'(BS|MS|BA|MA|PhD|Bachelor|Master)\s+(?:in|of)?\s*([^\n\.]{1,}?)(?=(?:\.\s|\n{2,}| {2,}|$))(?:\s*\([^)]*\d{4}[^)]*\))?\s*,?\s*([^,\n]*(?:University|College|Institute))?',
    # Professional title format with university (e.g., "English Literary and Scientific Translator, USAL (University)")
    r'([A-Za-z][A-Za-z\s&,]+(?:translator|teacher|analyst|specialist|consultant|coordinator|administrator|manager|secretary|assistant|technician|engineer|scientist|researcher|professor|instructor|designer|developer|programmer|architect|planner|advisor|auditor|inspector|supervisor|director|officer|representative|accountant|economist|lawyer|attorney|therapist|counselor|physician|doctor|nurse|pharmacist|veterinarian)(?:[,\s]+[A-Z][A-Za-z\s&,]*)?[,\s]+(?:[A-Z]{2,}|[A-Za-z\s]+)\s*\([Uu]niversity|[Cc]ollege|[Ii]nstitute|[Ss]chool\))',
    # Specific pattern for "Degree [Subject]" format
    r'degree\s+([A-Za-z][A-Za-z\s&]+(?:administration|engineering|science|arts|business|management|technology|studies|medicine|law))',
    # Pattern for "Degree: [Degree], Grade: [Grade], University: [University], Year: [Year]"
    r'(?:\n\s*){2,}(?:(degree\s*:?\s*([^\n:]+)[\n\r]*)|(grade\s*:?\s*([^\n:]+)[\n\r]*)|(university\s*:?\s*([^\n:]+)[\n\r]*)|(year\s*:?\s*([^\n:]+)[\n\r]*)){4,}',
    # Professional qualification with institution pattern
    r'([A-Za-z][A-Za-z\s&,]+(?:translator|secretary|analyst|specialist|consultant|coordinator|administrator|manager|assistant|technician|engineer|scientist|researcher|professor|instructor|designer|developer|programmer|architect|planner|advisor|auditor|inspector|supervisor|director|officer|representative|accountant|economist|lawyer|attorney|therapist|counselor|physician|doctor|nurse|pharmacist|veterinarian)(?:[,\s]+[A-Za-z\s&,]+)?(?:[,\s]+[A-Z][A-Za-z\s&]*)?)',
    # Degree with colon/dash
    r'degree\s*[:\-]\s*([A-Za-z][A-Za-z\s&]+(?:administration|engineering|science|arts|business|management|technology|studies|medicine|law))',
    # Standard degree patterns
    r'(?:bachelor|master|phd|diploma|certificate)s?\s+(?:of\s+|in\s+)?([A-Za-z][A-Za-z\s&]+(?:administration|engineering|science|arts|business|management|technology|studies|medicine|law))',
    # Abbreviated degree patterns
    r'(?:b\.?sc|m\.?sc|b\.?eng|m\.?eng|b\.?a|m\.?a|phd|dvm|d\.?v\.?m)\.?\s+(?:in\s+)?([A-Za-z][A-Za-z\s&]+(?:administration|engineering|science|arts|business|management|technology|studies|medicine|law))',
    # University/institution patterns
    r'(?:university|college|institute|faculty)\s+of\s+([A-Za-z][A-Za-z\s&]+(?:administration|engineering|science|arts|business|management|technology|studies|medicine|law))',
    # Qualification patterns
    r'qualifications?\s*[:\n]\s*([A-Za-z][A-Za-z\s&]+(?:administration|engineering|science|arts|business|management|technology|studies|medicine|law|diploma|certificate|degree))',
    # Year-based patterns
    r'([A-Za-z][A-Za-z\s&]+(?:administration|engineering|science|arts|business|management|technology|studies|medicine|law))\s+[-–]\s*\d{4}',
    # Degree with institution (e.g., "Bachelor of Science in Computer Science, XYZ University")
    r'(?i)(?:degree\s+(?:in\s+)?)?([A-Za-z]+\s+[A-Za-z]+(?:\s+(?:administration|engineering|science|arts|business|management|technology|studies|medicine|law))?)',
    # Generic degree patterns (fallback)
    r'([A-Za-z][A-Za-z\s&]+\s+degree)',
]
# Simplified role patterns - removed many redundant ones
ROLE_PATTERNS = [
    # Arabic current position pattern that handles both languages
    r'(?:الوظيفة الحالية|Current\s+Position)[\s\n]+((?:(?!في الفترة من|from\s+\d).)*?)(?:في الفترة من|from\s+\d).*?(?:حتى االن|until now|Present)',
    # SOLUTION 6: If you want to keep your original structure but fix it
    r'(?:الوظيفة الحالية|Current\s+Position)[\s\n]+(.*?)(?:في الفترة من|period from)\s*(?:(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+)?\d{1,2}?[\/\-]?\d{1,2}?[\/\-]?\d{4}\s*(?:to|until|حتى|-|–)\s*(?:Present|Now|Currently|until now|االن|الآن|current|ongoing)',
    # Arabic current position pattern
    r'(?:(?:\nCurrent\s*\nPosition)|(?:الوظيفة الحالية))[\s\n]*(.*?)(?:until now|حتى االن)',
    # Current role explicit keywords
    r'current\s+(?:position|role|job|title)\s*:?\s*([^\n\r]+)',
    r'(?:currently|presently)\s+(?:working\s+as|employed\s+as|serving\s+as)\s+(?:a\s+|an\s+)?([^\n\r]+)',
    # Company + role pattern
    r'(?:[\n\s:,]){2,}([^,\n:]+)[\s:,]+From[\s:,]+[^,\n:]+[\s:,]+to[\s:,]+(?:Present|Now|2024|2025)[\s:,]*\n[\s:,]*([A-Z][A-Za-z\s&:,]+)',
    # Roles after company names (with common company suffixes)
    r'(?:(?:[A-Z][a-zA-Z\s&]+(?:S\.A\.|Inc\.|Ltd\.|LLC|Corp)\.?)\s*\n)([A-Z][a-zA-Z\s/&-]+(?:Manager|Director|Coordinator|Specialist|Analyst|Assistant|Quality|Responsible|Lead)[^\n]*)',
    # Experience section patterns
    # Add this pattern to your ROLE_PATTERNS list:
    r'(?:WORK\s+EXPERIENCE|Experience|الخبرة)\s*\n\s*(?:[•\-\*]\s*)?([A-Z][A-Za-z\s&]+(?:Engineer|Developer|Manager|Analyst|Designer|Consultant|Director|Specialist|Coordinator|Administrator|Executive|Officer|Representative|Supervisor|Chief|Chemist|Quality|Auditor|Translator|Secretary|Technician))\s*\n[^(]*\(.*?(?:Present|Now|2024|2025|current|ongoing)',
    r'(?:Experience|Work\s+Experience|WORK\s+EXPERIENCE)\s*\n\s*(?:[•\-\*]\s*)?([A-Z][A-Za-z\s&]+(?:Engineer|Developer|Manager|Analyst|Designer|Consultant|Director|Specialist|Coordinator|Administrator|Executive|Officer|Representative|Supervisor|Chief|Chemist|Quality|Auditor|Translator|Secretary|Technician))',
    r'(?:EXPERIENCE\s*\n[^\n]*\n)(?:[•\-\*]\s*)?([A-Z][a-zA-Z\s/&-]+(?:Quality\s+Assurance|Responsible|Manager|Director|Coordinator)[^\n]*)'
    # Generic date-based pattern (original format)
    r'(?:\n\s*){2,}(.*?)From\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}\s+to\s+(?:Present|Now|Currently working here).*',
    # Job titles with standard endings (most comprehensive)
    r'([A-Z][A-Za-z\s&]+(?:Engineer|Developer|Manager|Analyst|Designer|Consultant|Director|Specialist|Coordinator|Administrator|Executive|Officer|Representative|Supervisor|Chief|Chemist|Quality|Auditor|Translator|Secretary)).*?(?:to\s+)?(?:Present|Now|2024|2025|current)',
    # Role with responsibility indicator
    r'([A-Z][A-Za-z\s&]+(?:Quality|Management|Coordinator|Auditor|Translator|Secretary))\s*\n\s*Responsibility',
    # Specific title patterns
    r'(?:designation|position|title)\s*:?\s*(general\s+manager|manager)',
    r'(general\s+manager|operations\s+manager|business\s+manager)',
    # Exclude academic roles
    r'^\s*([A-Z][A-Za-z\s&]+(?:Engineer|Developer|Manager|Analyst|Designer|Consultant|Director|Coordinator|Administrator|Executive|Officer|Representative|Supervisor|Chief|Chemist))\s*,(?![^,]*(?:University|College|Institute|School|Faculty))',
    r'([A-Z][a-z]+(?: [A-Z][a-z]+)*)(?!\s*,|\s*-|,|-)\s*,\s*[A-Z][^,\n]+(?:company|corporation|school|hospital)',
    r'-\s*([A-Za-z\s]{3,30})\s*,\s*[A-Za-z\s]+(?:School|Company|Corporation|Ltd|Inc|University|Institute)',
]

LOCATION_LABEL_PATTERNS = [
    
    r'(?:location|address|city|residence):\s*([^,\n]+(?:,\s*[^,\n]+){0,2})',
    r'(?:current\s+(?:location|address|residence)):\s*([^,\n]+(?:,\s*[^,\n]+){0,2})',
    r'(?:location|address|current\s+address|residence)\s*:?\s*([A-Za-z\s,]+(?:,\s*[A-Za-z\s]+)?)',
    r'(?:based\s+in|located\s+in)\s*:?\s*([A-Za-z\s,]+(?:,\s*[A-Za-z\s]+)?)',
    # More specific "from" pattern - only capture city/country format
    r'from\s+([A-Za-z\s]+(?:,\s*[A-Za-z\s]+)?)(?:\s*[,.]|\s*$)',
    r'(\b[A-Z][a-zA-Z]+\s*[-–]\s*[A-Z][a-zA-Z]+\b)(?:\s*\||\s*$)',  # City-Country pattern

]
# Exclusion words for address/location extraction
# Nationality extraction patterns
NATIONALITY_PATTERNS = [
    r'nationality[:\s]+([a-zA-Z\s]+)',
    r'citizen(?:ship)?[:\s]+([a-zA-Z\s]+)',
    r'national[:\s]+([a-zA-Z\s]+)',
    r'country of citizenship[:\s]+([a-zA-Z\s]+)',
    r'passport[:\s]+([a-zA-Z\s]+)',
        # Enhanced patterns with common OCR errors
    # Handle 't' -> 'Ɵ', 'ƫ', 'ť', 'ţ', 'ṭ', '†'
    r'na[Ɵƫťţṭ†t] ionali[Ɵƫťţṭ†t]y[:\s]+([a-zA-Z\s]+)',
    r'na[Ɵƫťţṭ†t]ional[:\s]+([a-zA-Z\s]+)',
    
    # Handle 'i' -> 'l', '1', 'ı', 'í', 'ì' and other variations
    r'nat[ıíìl1i]onal[ıíìl1i]ty[:\s]+([a-zA-Z\s]+)',
    
    # Handle 'o' -> '0', 'ö', 'ó', 'ò', 'ø'
    r'nati[0öóòøo]nality[:\s]+([a-zA-Z\s]+)',
    
    # More flexible pattern that allows for multiple character substitutions
    r'n[aá][\w]*[ıíìl1i][\w]*n[aá]l[\w]*[Ɵƫťţṭ†t]y[:\s]+([a-zA-Z\s]+)',
    
    # Case-insensitive versions
    r'(?i)na[Ɵƫťţṭ†t]ionali[Ɵƫťţṭ†t]y[:\s]+([a-zA-Z\s]+)',
    r'(?i)citizen(?:ship)?[:\s]+([a-zA-Z\s]+)',
    r'NaƟonality[:\s]+([a-zA-ZƟ]+(?: [a-zA-ZƟ]+)*)',
    r'(?i)naƟonaliƟy[:\s]+([a-zA-ZƟ\s]+)',
    
    # More flexible patterns using .* to handle various corruptions
    r'(?i)na.{0,2}ionalit.{0,2}[:\s]+([a-zA-Z\s]+)',
    r'(?i)nat.{0,2}onalit.{0,2}[:\s]+([a-zA-Z\s]+)',
    
    # Pattern that looks for the structure regardless of character corruption
    r'(?i)[Nn][a-zA-Z]{1,3}[Ɵt][a-zA-Z]{0,2}onal[a-zA-Z]{0,2}[Ɵt][a-zA-Z]{0,2}y[:\s]+([a-zA-Z\s]+)',
    
    # Even more permissive - look for N followed by characters ending in ty:
    r'(?i)N[a-zA-ZƟ]{8,12}y[:\s]+([a-zA-Z\s]+)',
]

ADDRESS_EXCLUSION_WORDS = [
    'address', 'phone', 'email', 'mobile', 'contact', 'number', 'fax', 'tel',
    'years of experience', 'work experience', 'employment', 'salary',
    'date of birth', 'nationality', 'marital status', 'gender',
    'responsibilities', 'duties', 'skills', 'languages', 'hobbies',
    'references', 'objective', 'summary', 'profile', 'career',
    'designation', 'position', 'title', 'role', 'company', 'organization',
    'years of', 'date of', 'joining', 'intertek'
]

# Education validation exclusion words
EDUCATION_EXCLUSION_WORDS = [
    'phone', 'email', 'address', 'contact', 'mobile', 'tel', 'fax',
    'years of experience', 'work experience', 'employment', 'salary',
    'date of birth', 'nationality', 'marital status', 'gender',
    'responsibilities', 'duties', 'skills', 'languages', 'hobbies',
    'references', 'objective', 'summary', 'profile', 'career',
    'designation', 'position', 'title', 'role', 'company', 'organization',
    'years of', 'date of', 'joining', 'intertek'
]

# Extended education keywords for validation
EXTENDED_EDUCATION_KEYWORDS = [
    'degree', 'bachelor', 'master', 'phd', 'diploma', 'certificate',
    'administration', 'engineering', 'science', 'arts', 'business',
    'management', 'technology', 'studies', 'medicine', 'law',
    'university', 'college', 'institute', 'school', 'education',
    'qualification', 'academic', 'graduation', 'mba', 'bba',
    'translator', 'secretary', 'analyst', 'specialist', 'consultant',
    'coordinator', 'administrator', 'manager', 'assistant', 'technician',
    'literary', 'scientific', 'public'
]

# Additional flags for validation (reusable constants)
MIN_NAME_LENGTH = 3
MAX_NAME_LENGTH = 200
MIN_EDUCATION_LENGTH = 10
MAX_AGE_LIMIT = 100
MIN_AGE_LIMIT = 0

# Month mappings for date parsing
MONTH_MAP = {
    'jan': 1, 'january': 1, 'feb': 2, 'february': 2, 'mar': 3, 'march': 3,
    'apr': 4, 'april': 4, 'may': 5, 'jun': 6, 'june': 6, 'jul': 7, 'july': 7,
    'aug': 8, 'august': 8, 'sep': 9, 'september': 9, 'oct': 10, 'october': 10,
    'nov': 11, 'november': 11, 'dec': 12, 'december': 12
}

# Date format patterns for parsing
DATE_FORMATS = [
    '%m/%y', '%m/%Y', '%m-%y', '%m-%Y', 
    '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y', '%m-%d-%Y',
    '%d/%m/%y', '%m/%d/%y', '%d-%m-%y', '%m-%d-%y',
    '%Y-%m-%d', '%Y'
]

# Non-name words blacklist
NON_NAME_WORDS = {
    'page', 'date', 'birth', 'phone', 'email', 'address', 'location', 
    'nationality', 'experience', 'qualification', 'education', 'mobile',
    'number', 'status', 'academic', 'graduation', 'project', 'estimate',
    'skills', 'technical', 'current', 'position', 'contact', 'information',
    'english', 'spanish', 'french', 'german', 'italian', 'portuguese',
    'arabic', 'saudi', 'egypt', 'giza'
}

# Common non-name words for validation
NON_NAME_VALIDATION_WORDS = {
    'number', 'mobile', 'phone', 'email', 'address', 'birth', 'date',
    'graduation', 'project', 'estimate', 'qualifications', 'academic',
    'experience', 'skills', 'technical', 'current', 'position', 'status'
}

# False positive name patterns
FALSE_POSITIVE_NAMES = {
    'mobile number', 'phone number', 'email address', 'date birth', 
    'social status', 'academic qualifications', 'graduation project',
    'graduation year', 'graduation estimate', 'work experience',
    'current position', 'technical skills', 'saudi arabia',
    'address line', 'contact information'
}

# CV section headers
CV_SECTIONS = ['qualification', 'education', 'experience', 'contact']

# Education/degree patterns
EDUCATION_KEYWORDS = {
    'degree', 'bachelor', 'master', 'phd', 'diploma', 'certificate', 'b.sc', 'b.eng', 'b.a', 'm.sc', 'm.eng', 'm.a', 'dvm', 'd.v.m',
    'qualification', 'education', 'faculty' , 'translator', 'translation', 'literary', 'scientific translator', 'language', 'linguistics'

}


# Name titles to exclude
NAME_TITLES = ['sir', 'mr', 'mrs', 'ms', 'dr', 'prof', 'ing', 'eng']

# Words that indicate non-location in address extraction
NON_LOCATION_WORDS = [
    'engineer', 'developer', 'manager', 'experience', 'years', 'switchboard', 
    'design', 'phone', 'email', 'mobile','rtl', 'coding', 'verilog', 'vhdl', 'synthesis', 'implementation', 'design', 
    'verification', 'testing', 'simulation', 'programming', 'development',
    'engineer', 'developer', 'manager', 'analyst', 'specialist', 'coordinator',
    'experience', 'years', 'skills', 'languages', 'tools', 'education',
    'project', 'diploma', 'training', 'course', 'workshop', 'internship',
    'system', 'processor', 'architecture', 'digital', 'embedded', 'software',
    'hardware', 'technical', 'objective', 'phone', 'email', 'github', 'linkedin'
]

# NLP entity labels for locations
LOCATION_ENTITY_LABELS = ["GPE", "LOC"]

# Common job role suffixes for pattern matching
JOB_ROLE_SUFFIXES = [
    'Engineer', 'Developer', 'Manager', 'Analyst', 'Designer', 'Consultant', 
    'Director', 'Specialist', 'Coordinator', 'Administrator', 'Executive', 
    'Officer', 'Representative', 'Supervisor', 'Chief', 'Chemist'
]

# Educational institution keywords
EDUCATIONAL_INSTITUTIONS = ['university', 'college', 'institute', 'school', 'faculty']

COUNTRIES = [
        # Major countries and common variations
        "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Argentina", 
        "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", 
        "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", 
        "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", 
        "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cambodia", "Cameroon", 
        "Canada", "Cape Verde", "Central African Republic", "Chad", "Chile", 
        "China", "Colombia", "Comoros", "Congo", "Costa Rica", "Croatia", 
        "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica", 
        "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", 
        "Eritrea", "Estonia", "Ethiopia", "Fiji", "Finland", "France", "Gabon", 
        "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", 
        "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", 
        "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", 
        "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", 
        "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", 
        "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", 
        "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", 
        "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", 
        "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", 
        "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", 
        "Nigeria", "North Korea", "North Macedonia", "Norway", "Oman", "Pakistan", 
        "Palau", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", 
        "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", 
        "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", 
        "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", 
        "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", 
        "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sudan", 
        "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", 
        "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", 
        "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", 
        "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", 
        "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", 
        "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe",
        
        # Common abbreviations and alternative names
        "USA", "US", "United States of America", "UK", "Britain", "Great Britain", "ENG", "EGY",
        "UAE", "KSA", "Russia", "USSR", "Soviet Union", "Czech Republic", "Czechia",
        "North Macedonia", "Macedonia", "Bosnia", "Herzegovina", "Trinidad", "Tobago" , "ARG" , "BRA"
    ]