#!/usr/bin/env python3
"""
Markdown Validator for English Learning Resources

This module provides utilities to validate and analyze Markdown files
used in English learning materials, including phrasal verbs, vocabulary,
and YouTube transcriptions.
"""

import re
from typing import List, Dict, Tuple, Optional
from pathlib import Path


class MarkdownValidator:
    """Validates and analyzes English learning Markdown files."""

    def __init__(self, file_path: str):
        """
        Initialize the validator with a file path.

        Args:
            file_path: Path to the Markdown file to validate
        """
        self.file_path = Path(file_path)
        self.content = ""
        self.lines = []

    def load_file(self) -> bool:
        """
        Load the Markdown file content.

        Returns:
            True if file loaded successfully, False otherwise
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.content = f.read()
                self.lines = self.content.split('\n')
            return True
        except FileNotFoundError:
            return False
        except Exception:
            return False

    def count_phrasal_verbs(self) -> int:
        """
        Count the number of phrasal verbs in the document.

        Phrasal verbs are identified by patterns like:
        - "verb + preposition" (e.g., "look up", "turn on")
        - Typically found in learning materials with examples

        Returns:
            Count of unique phrasal verbs found
        """
        # Pattern to match common phrasal verb structures
        pattern = r'\b[a-z]+\s+(up|down|on|off|in|out|away|back|over|through|about|after|for|into|with)\b'
        matches = re.findall(pattern, self.content.lower())
        return len(set(matches))

    def extract_vocabulary(self) -> List[str]:
        """
        Extract vocabulary words marked with special formatting.

        Looks for words marked with:
        - Bold: **word**
        - Code: `word`
        - Bullet points at the start of lines

        Returns:
            List of vocabulary words found
        """
        vocabulary = []

        # Extract words in bold
        bold_words = re.findall(r'\*\*([^*]+)\*\*', self.content)
        vocabulary.extend(bold_words)

        # Extract words in code blocks
        code_words = re.findall(r'`([^`]+)`', self.content)
        vocabulary.extend(code_words)

        # Extract bullet point items (common in vocab lists)
        for line in self.lines:
            if line.strip().startswith(('- ', '* ', '+ ')):
                word = line.strip()[2:].split(':')[0].split('-')[0].strip()
                if word and len(word) < 50:  # Reasonable word length
                    vocabulary.append(word)

        return vocabulary

    def count_examples(self) -> int:
        """
        Count the number of example sentences.

        Examples are identified by:
        - Lines containing "Example:", "e.g.", "Ex:"
        - Numbered examples (1., 2., etc.)
        - Emoji markers like 📝

        Returns:
            Count of example sentences found
        """
        count = 0
        example_patterns = [
            r'(?i)example:',
            r'(?i)e\.g\.',
            r'(?i)ex:',
            r'^\s*\d+\.',
            r'📝',
            r'(?i)example \d+',
        ]

        for line in self.lines:
            for pattern in example_patterns:
                if re.search(pattern, line):
                    count += 1
                    break

        return count

    def check_headers(self) -> Dict[str, int]:
        """
        Analyze header structure in the document.

        Returns:
            Dictionary with header levels (h1-h6) as keys and counts as values
        """
        headers = {'h1': 0, 'h2': 0, 'h3': 0, 'h4': 0, 'h5': 0, 'h6': 0}

        for line in self.lines:
            if line.strip().startswith('#'):
                level = len(re.match(r'^#+', line.strip()).group())
                if 1 <= level <= 6:
                    headers[f'h{level}'] += 1

        return headers

    def find_urls(self) -> List[str]:
        """
        Extract all URLs from the document.

        Returns:
            List of URLs found
        """
        # Pattern to match URLs (http, https, www)
        url_pattern = r'https?://[^\s\)]+|www\.[^\s\)]+'
        urls = re.findall(url_pattern, self.content)
        return urls

    def validate_structure(self) -> Tuple[bool, List[str]]:
        """
        Validate the document structure and return issues found.

        Checks for:
        - Empty file
        - Missing title (h1 header)
        - Consecutive blank lines (more than 2)
        - Lines that are too long (>200 chars)

        Returns:
            Tuple of (is_valid, list of issues)
        """
        issues = []

        if not self.content.strip():
            issues.append("File is empty")
            return False, issues

        # Check for title
        has_h1 = any(line.strip().startswith('# ') for line in self.lines)
        if not has_h1:
            issues.append("Missing main title (H1 header)")

        # Check for consecutive blank lines
        blank_count = 0
        for i, line in enumerate(self.lines):
            if not line.strip():
                blank_count += 1
                if blank_count > 2:
                    issues.append(f"More than 2 consecutive blank lines at line {i+1}")
                    blank_count = 0  # Reset to avoid duplicate reports
            else:
                blank_count = 0

        # Check for overly long lines
        for i, line in enumerate(self.lines):
            if len(line) > 200:
                issues.append(f"Line {i+1} exceeds 200 characters ({len(line)} chars)")

        is_valid = len(issues) == 0
        return is_valid, issues

    def get_word_count(self) -> int:
        """
        Count total words in the document.

        Returns:
            Total word count
        """
        # Remove markdown formatting and count words
        text = re.sub(r'[#*`\[\]()]', ' ', self.content)
        words = text.split()
        return len(words)

    def find_chinese_translations(self) -> int:
        """
        Count lines containing Chinese characters.

        Useful for bilingual learning materials.

        Returns:
            Count of lines with Chinese characters
        """
        chinese_pattern = r'[\u4e00-\u9fff]+'
        count = 0
        for line in self.lines:
            if re.search(chinese_pattern, line):
                count += 1
        return count

    def analyze(self) -> Dict[str, any]:
        """
        Perform complete analysis of the document.

        Returns:
            Dictionary containing all analysis results
        """
        if not self.load_file():
            return {'error': 'Failed to load file'}

        is_valid, issues = self.validate_structure()

        return {
            'file_path': str(self.file_path),
            'is_valid': is_valid,
            'issues': issues,
            'word_count': self.get_word_count(),
            'phrasal_verb_count': self.count_phrasal_verbs(),
            'vocabulary_items': len(self.extract_vocabulary()),
            'example_count': self.count_examples(),
            'headers': self.check_headers(),
            'url_count': len(self.find_urls()),
            'chinese_lines': self.find_chinese_translations(),
            'line_count': len(self.lines),
        }


def validate_directory(directory: str, pattern: str = "*.md") -> Dict[str, Dict]:
    """
    Validate all Markdown files in a directory.

    Args:
        directory: Path to directory to scan
        pattern: File pattern to match (default: "*.md")

    Returns:
        Dictionary mapping file paths to analysis results
    """
    dir_path = Path(directory)
    results = {}

    if not dir_path.exists():
        return {'error': 'Directory not found'}

    for file_path in dir_path.rglob(pattern):
        validator = MarkdownValidator(str(file_path))
        results[str(file_path)] = validator.analyze()

    return results


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python markdown_validator.py <file_or_directory>")
        sys.exit(1)

    path = sys.argv[1]
    path_obj = Path(path)

    if path_obj.is_file():
        validator = MarkdownValidator(path)
        result = validator.analyze()
        print(f"\nAnalysis of {path}:")
        for key, value in result.items():
            print(f"  {key}: {value}")
    elif path_obj.is_dir():
        results = validate_directory(path)
        print(f"\nAnalyzed {len(results)} files in {path}")
        for file_path, result in results.items():
            print(f"\n{file_path}:")
            if 'error' in result:
                print(f"  Error: {result['error']}")
            else:
                print(f"  Valid: {result['is_valid']}")
                print(f"  Word count: {result['word_count']}")
    else:
        print(f"Error: {path} is not a valid file or directory")
        sys.exit(1)
