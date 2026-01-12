# Markdown Validator for English Learning Resources

A Python utility for validating and analyzing Markdown files used in English learning materials. This tool is designed to work with educational content including phrasal verbs, vocabulary lists, and YouTube transcriptions.

## Features

The `MarkdownValidator` class provides the following analysis capabilities:

- **Phrasal Verb Detection**: Automatically count phrasal verbs (e.g., "turn on", "look up")
- **Vocabulary Extraction**: Extract words marked with bold, code formatting, or bullet points
- **Example Counting**: Count example sentences using various markers (Example:, e.g., numbered lists, emojis)
- **Header Analysis**: Analyze document structure with H1-H6 header counts
- **URL Detection**: Find all HTTP, HTTPS, and www URLs in documents
- **Structure Validation**: Check for common issues (missing titles, excessive blank lines, overly long lines)
- **Word Count**: Calculate total word count excluding markdown formatting
- **Chinese Translation Detection**: Count lines containing Chinese characters for bilingual materials
- **Directory Analysis**: Recursively analyze all markdown files in a directory

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Command Line

Analyze a single file:
```bash
python markdown_validator.py file.md
```

Analyze all markdown files in a directory:
```bash
python markdown_validator.py /path/to/directory
```

### Python API

```python
from markdown_validator import MarkdownValidator, validate_directory

# Analyze a single file
validator = MarkdownValidator("phrasal_verbs.md")
result = validator.analyze()
print(f"Word count: {result['word_count']}")
print(f"Phrasal verbs found: {result['phrasal_verb_count']}")
print(f"Document valid: {result['is_valid']}")

# Analyze a directory
results = validate_directory("/path/to/learning/materials")
for file_path, analysis in results.items():
    print(f"{file_path}: {analysis['word_count']} words")
```

## Testing

The project includes a comprehensive test suite with 53 tests covering all functionality.

Run tests:
```bash
pytest test_markdown_validator.py -v
```

### Test Coverage

The test suite includes:

- **Initialization Tests**: Validator setup with different path types
- **File Loading Tests**: Success/failure cases, empty files, Unicode handling
- **Phrasal Verb Tests**: Basic detection, duplicates, various prepositions
- **Vocabulary Extraction Tests**: Bold, code, bullet points, mixed formatting
- **Example Counting Tests**: Keywords, numbered lists, emojis, abbreviations
- **Header Tests**: All H1-H6 levels, multiple headers, missing headers
- **URL Tests**: HTTP, HTTPS, www, markdown links
- **Structure Validation Tests**: Empty files, missing titles, formatting issues
- **Word Count Tests**: Simple text, markdown formatting, multiline content
- **Chinese Detection Tests**: Mixed bilingual content
- **Analysis Tests**: Complete document analysis
- **Directory Tests**: Recursive scanning, pattern matching
- **Edge Cases**: Whitespace-only files, special characters, large files, mixed line endings

All 53 tests pass successfully.

## API Reference

### MarkdownValidator

#### Methods

- `load_file() -> bool`: Load markdown file content
- `count_phrasal_verbs() -> int`: Count unique phrasal verbs
- `extract_vocabulary() -> List[str]`: Extract vocabulary words
- `count_examples() -> int`: Count example sentences
- `check_headers() -> Dict[str, int]`: Analyze header structure
- `find_urls() -> List[str]`: Extract all URLs
- `validate_structure() -> Tuple[bool, List[str]]`: Validate document structure
- `get_word_count() -> int`: Calculate total word count
- `find_chinese_translations() -> int`: Count lines with Chinese characters
- `analyze() -> Dict[str, any]`: Perform complete analysis

### validate_directory

```python
validate_directory(directory: str, pattern: str = "*.md") -> Dict[str, Dict]
```

Recursively validate all matching files in a directory.

## Example Output

```python
{
    'file_path': '/path/to/phrasal_verbs.md',
    'is_valid': True,
    'issues': [],
    'word_count': 342,
    'phrasal_verb_count': 15,
    'vocabulary_items': 28,
    'example_count': 12,
    'headers': {'h1': 1, 'h2': 3, 'h3': 0, 'h4': 0, 'h5': 0, 'h6': 0},
    'url_count': 2,
    'chinese_lines': 8,
    'line_count': 45
}
```

## License

This project is open source and available for educational purposes.
