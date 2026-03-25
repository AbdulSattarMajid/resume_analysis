# Resume Analyzer

A comprehensive resume analysis tool that evaluates skills, provides grammar corrections, and recommends career paths.

## Features

- **PDF & DOCX Support**: Extract text from multiple resume formats
- **Skill Matching**: Identify skills and match them against a taxonomy
- **Grammar Checking**: Detect and suggest corrections for grammatical errors
- **Role Recommendations**: Suggest suitable job roles based on identified skills
- **No-AI Logic**: Uses spaCy and pattern matching (no external AI APIs required)

## Project Structure

```
Resume Analyzer/
├── .streamlit/              # Streamlit configuration
├── data/                    # Knowledge base (skill taxonomy)
├── engine/                  # Core analysis logic
├── assets/                  # Static assets (images, icons)
├── tests/                   # Test suite
├── requirements.txt         # Python dependencies
├── main.py                  # Entry point
└── README.md               # Documentation
```

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Download spaCy model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Running the Application

```bash
streamlit run main.py
```

The application will open in your browser at `http://localhost:8501`

## Test Cases

Run the test suite:
```bash
python tests/test_cases.py
```

Test cases TC-01 through TC-06 cover:
- PDF extraction
- DOCX extraction
- Skill matching
- Role recommendation
- Grammar checking
- End-to-end analysis

## Core Modules

- **parser.py**: Handles PDF and DOCX extraction
- **analyzer.py**: Performs skill analysis and matching
- **grammar.py**: Integrates LanguageTool for grammar checking

## Technologies Used

- Streamlit: Web UI framework
- spaCy: NLP processing
- LanguageTool: Grammar checking
- Python-DOCX: DOCX file handling
- PyPDF2: PDF file handling

## License

This project is part of the 8th Semester coursework.
