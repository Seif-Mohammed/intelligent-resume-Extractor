# 🎯 Intelligent Resume Classifier

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.4+-green.svg)](https://pypi.org/project/PyQt6/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/yourusername/resume-classifier.svg)](https://github.com/yourusername/resume-classifier/stargazers)

An AI-powered resume processing and candidate filtering system with an intuitive GUI interface. This tool helps HR professionals and recruiters efficiently process, analyze, and filter resumes based on specific criteria.

## ✨ Features

### 🤖 Smart Resume Processing
- **Multi-format Support**: Process PDF, DOCX, and TXT resume files
- **AI-Powered Extraction**: Uses spaCy NLP for intelligent information extraction
- **Comprehensive Data Mining**: Extracts name, age, education, role, location, nationality, contact info

### 🎯 Advanced Filtering
- **Multi-criteria Filtering**: Filter by age range, location, role, education, nationality
- **Match Scoring**: Intelligent scoring system to rank candidates
- **Real-time Results**: Instant filtering and sorting capabilities

### 💼 Professional Export
- **Template-based Export**: Export filtered candidates using professional CV templates
- **Multiple Formats**: Export to DOCX and PDF formats
- **Batch Processing**: Process and export multiple candidates simultaneously

### 🖥️ User-Friendly Interface
- **Modern GUI**: Clean, intuitive PyQt6 interface
- **Progress Tracking**: Real-time processing progress indicators
- **Detailed Preview**: Comprehensive candidate information display
- **Responsive Design**: Resizable panels and adaptive layouts

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/resume-classifier.git
   cd resume-classifier
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download spaCy language model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. **Run the application**
   ```bash
   python bin/main.py
   ```

```

## 📖 Usage Guide

### 1. **Select Resume Files**
   - Click "Select Resume Files" to choose your resume collection
   - Supports PDF, DOCX, and TXT formats
   - Multiple file selection enabled

### 2. **Set Filtering Criteria**
   - **Age Range**: Set minimum and maximum age limits
   - **Location**: Filter by preferred location/city
   - **Role**: Specify desired job roles or positions
   - **Education**: Filter by educational background
   - **Nationality**: Set nationality preferences

### 3. **Process Resumes**
   - Click "Process Resumes" to start analysis
   - Monitor progress with the built-in progress bar
   - View real-time results as they're processed

### 4. **Review Results**
   - Sort candidates by match score, name, age, or nationality
   - Click on any candidate to view detailed information
   - Color-coded match scores for quick assessment

### 5. **Export Candidates**
   - Choose export format (DOCX or PDF)
   - Select output directory
   - Professional CV templates applied automatically

## 🏗️ Architecture

```
resume-classifier/
├── bin/
│   ├── Resume_Processor.py    # Core processing engine
│   ├── GUI.py                 # Main application interface
│   ├── Candidate_profile.py   # Data model for candidates
│   ├── Processing_Thread.py   # Multi-threading support
│   ├── resume_config.py       # Configuration and patterns
│   └── main.py               # Application entry point
├── templates/
│   └── temp.docx             # CV export template
├── tests/                    # Unit tests
├── docs/                     # Documentation
└── examples/                 # Sample files
```

## 🛠️ Core Components

### Resume Processor
- **Text Extraction**: Multi-format document parsing
- **NLP Analysis**: Advanced named entity recognition
- **Pattern Matching**: Robust regex-based information extraction
- **Validation**: Comprehensive data validation and cleaning

### GUI Application
- **Responsive Interface**: Modern PyQt6 design
- **Multi-threading**: Non-blocking processing
- **Real-time Updates**: Live progress and results
- **Export Integration**: Seamless document generation

### Filtering Engine
- **Multi-criteria Matching**: Complex filtering logic
- **Scoring Algorithm**: Intelligent candidate ranking
- **Flexible Criteria**: Customizable filter parameters


## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/
```

Run specific tests:
```bash
python -m pytest tests/test_processor.py -v
```


### CandidateProfile Class

```python
from src.Candidate_profile import CandidateProfile

profile = CandidateProfile(
    name="John Doe",
    age=30,
    education="Computer Science",
    current_role="Software Engineer"
)
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Install development dependencies (`pip install -r requirements-dev.txt`)
4. Make your changes
5. Run tests (`python -m pytest`)
6. Commit changes (`git commit -m 'Add amazing feature'`)
7. Push to branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📋 Roadmap

- [ ] **v1.1**: Add support for more file formats (ODT, RTF)
- [ ] **v1.2**: Implement machine learning-based matching
- [ ] **v1.3**: Add REST API for integration
- [ ] **v1.4**: Include skills extraction and matching
- [ ] **v1.5**: Add database support for candidate storage
- [ ] **v2.0**: Web-based interface option

## 🐛 Known Issues

- Large PDF files (>10MB) may take longer to process
- Some corrupted DOCX files might not parse correctly
- Non-English resumes require additional language models

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Seif Mohamed** - *Initial work* - [GitHub]([https://github.com/yourusername](https://github.com/Seif-Mohammed/))

## 🙏 Acknowledgments

- [spaCy](https://spacy.io/) for NLP capabilities
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) for the GUI framework
- [pdfplumber](https://github.com/jsvine/pdfplumber) for PDF processing
- [python-docx](https://python-docx.readthedocs.io/) for DOCX handling

## 📞 Support

- 📧 Email: seifmohamed606@gmail.com
- 🐛 Bug Reports: [GitHub Issues](https://github.com/Seif-Mohammed/intelligent-resume-Extractor/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/Seif-Mohammed/intelligent-resume-Extractor/discussions)
- 📖 Documentation: [Project Wiki](https://github.com/Seif-Mohammed/intelligent-resume-Extractor/wiki)

---

<div align="center">

**⭐ Star this project if you find it helpful!**

[Report Bug](https://github.com/Seif-Mohammed/intelligent-resume-Extractor/issues) •
[Request Feature](https://github.com/Seif-Mohammed/intelligent-resume-Extractor/issues) •
[Documentation](https://github.com/Seif-Mohammed/intelligent-resume-Extractor/wiki)

</div>
