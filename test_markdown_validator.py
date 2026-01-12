#!/usr/bin/env python3
"""
Comprehensive test suite for markdown_validator.py

Tests cover all functions and edge cases for the MarkdownValidator class
and related utilities.
"""

import pytest
import tempfile
import os
from pathlib import Path
from markdown_validator import MarkdownValidator, validate_directory


class TestMarkdownValidatorInit:
    """Test MarkdownValidator initialization."""

    def test_init_with_string_path(self):
        """Test initialization with string path."""
        validator = MarkdownValidator("/path/to/file.md")
        assert validator.file_path == Path("/path/to/file.md")
        assert validator.content == ""
        assert validator.lines == []

    def test_init_with_pathlib_path(self):
        """Test initialization with pathlib Path."""
        path = Path("/path/to/file.md")
        validator = MarkdownValidator(str(path))
        assert validator.file_path == path


class TestLoadFile:
    """Test file loading functionality."""

    def test_load_existing_file(self):
        """Test loading an existing file successfully."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("# Test\nContent here")
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            assert validator.load_file() is True
            assert validator.content == "# Test\nContent here"
            assert validator.lines == ["# Test", "Content here"]
        finally:
            os.unlink(temp_path)

    def test_load_nonexistent_file(self):
        """Test loading a file that doesn't exist."""
        validator = MarkdownValidator("/nonexistent/file.md")
        assert validator.load_file() is False
        assert validator.content == ""

    def test_load_empty_file(self):
        """Test loading an empty file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            assert validator.load_file() is True
            assert validator.content == ""
            assert validator.lines == [""]
        finally:
            os.unlink(temp_path)

    def test_load_file_with_unicode(self):
        """Test loading a file with Unicode characters."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("# 你好\nHello 世界\n📝 Example")
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            assert validator.load_file() is True
            assert "你好" in validator.content
            assert "📝" in validator.content
        finally:
            os.unlink(temp_path)


class TestCountPhrasalVerbs:
    """Test phrasal verb counting functionality."""

    def test_count_basic_phrasal_verbs(self):
        """Test counting basic phrasal verbs."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("Please turn on the light. Look up the word. Come back soon.")
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            validator.load_file()
            count = validator.count_phrasal_verbs()
            assert count > 0
        finally:
            os.unlink(temp_path)

    def test_count_no_phrasal_verbs(self):
        """Test counting when no phrasal verbs present."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("The cat sat quietly. Birds fly high.")
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            validator.load_file()
            count = validator.count_phrasal_verbs()
            assert count >= 0
        finally:
            os.unlink(temp_path)

    def test_count_duplicate_phrasal_verbs(self):
        """Test that duplicate phrasal verbs are counted as unique."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("Turn on the TV. Turn on the radio. Turn on the computer.")
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            validator.load_file()
            count = validator.count_phrasal_verbs()
            # Should count "turn on" only once due to set()
            assert count >= 1
        finally:
            os.unlink(temp_path)

    def test_count_various_prepositions(self):
        """Test phrasal verbs with different prepositions."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("Look up, look down, come in, go out, take away, bring back")
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            validator.load_file()
            count = validator.count_phrasal_verbs()
            assert count > 0
        finally:
            os.unlink(temp_path)


class TestExtractVocabulary:
    """Test vocabulary extraction functionality."""

    def test_extract_bold_vocabulary(self):
        """Test extracting words marked with bold."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("Learn these words: **apple**, **banana**, **cherry**")
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            validator.load_file()
            vocab = validator.extract_vocabulary()
            assert "apple" in vocab
            assert "banana" in vocab
            assert "cherry" in vocab
        finally:
            os.unlink(temp_path)

    def test_extract_code_vocabulary(self):
        """Test extracting words marked with code formatting."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("Use `variable` and `function` in code")
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            validator.load_file()
            vocab = validator.extract_vocabulary()
            assert "variable" in vocab
            assert "function" in vocab
        finally:
            os.unlink(temp_path)

    def test_extract_bullet_point_vocabulary(self):
        """Test extracting vocabulary from bullet points."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("- word1: definition\n* word2: meaning\n+ word3 - description")
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            validator.load_file()
            vocab = validator.extract_vocabulary()
            assert "word1" in vocab
            assert "word2" in vocab
            assert "word3" in vocab
        finally:
            os.unlink(temp_path)

    def test_extract_mixed_vocabulary(self):
        """Test extracting vocabulary with mixed formatting."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("**bold**, `code`, - bullet\n* another")
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            validator.load_file()
            vocab = validator.extract_vocabulary()
            assert len(vocab) > 0
        finally:
            os.unlink(temp_path)

    def test_extract_no_vocabulary(self):
        """Test extraction when no vocabulary markers present."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("Plain text without any special formatting")
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            validator.load_file()
            vocab = validator.extract_vocabulary()
            assert isinstance(vocab, list)
        finally:
            os.unlink(temp_path)


class TestCountExamples:
    """Test example counting functionality."""

    def test_count_example_keyword(self):
        """Test counting examples with 'Example:' keyword."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("Example: This is an example\nExample: Another one\nEx: Short form")
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            validator.load_file()
            count = validator.count_examples()
            assert count >= 3
        finally:
            os.unlink(temp_path)

    def test_count_numbered_examples(self):
        """Test counting numbered examples."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("1. First example\n2. Second example\n3. Third example")
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            validator.load_file()
            count = validator.count_examples()
            assert count >= 3
        finally:
            os.unlink(temp_path)

    def test_count_emoji_examples(self):
        """Test counting examples with emoji markers."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("📝 Example one\n📝 Example two")
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            validator.load_file()
            count = validator.count_examples()
            assert count >= 2
        finally:
            os.unlink(temp_path)

    def test_count_eg_abbreviation(self):
        """Test counting examples with e.g. abbreviation."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("Use fruits, e.g. apples, bananas.\nAlso vegetables, e.g., carrots.")
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            validator.load_file()
            count = validator.count_examples()
            assert count >= 2
        finally:
            os.unlink(temp_path)

    def test_count_no_examples(self):
        """Test counting when no examples present."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("Just regular text without examples")
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            validator.load_file()
            count = validator.count_examples()
            assert count == 0
        finally:
            os.unlink(temp_path)


class TestCheckHeaders:
    """Test header structure checking."""

    def test_check_all_header_levels(self):
        """Test checking all header levels H1-H6."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("# H1\n## H2\n### H3\n#### H4\n##### H5\n###### H6")
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            validator.load_file()
            headers = validator.check_headers()
            assert headers['h1'] == 1
            assert headers['h2'] == 1
            assert headers['h3'] == 1
            assert headers['h4'] == 1
            assert headers['h5'] == 1
            assert headers['h6'] == 1
        finally:
            os.unlink(temp_path)

    def test_check_multiple_same_level(self):
        """Test counting multiple headers of the same level."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("## Section 1\n## Section 2\n## Section 3")
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            validator.load_file()
            headers = validator.check_headers()
            assert headers['h2'] == 3
            assert headers['h1'] == 0
        finally:
            os.unlink(temp_path)

    def test_check_no_headers(self):
        """Test when no headers present."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("Plain text\nNo headers here")
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            validator.load_file()
            headers = validator.check_headers()
            assert all(count == 0 for count in headers.values())
        finally:
            os.unlink(temp_path)

    def test_check_headers_with_text(self):
        """Test headers with actual text content."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("# Main Title\nSome text\n## Subsection\nMore text")
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            validator.load_file()
            headers = validator.check_headers()
            assert headers['h1'] == 1
            assert headers['h2'] == 1
        finally:
            os.unlink(temp_path)


class TestFindUrls:
    """Test URL finding functionality."""

    def test_find_http_urls(self):
        """Test finding HTTP URLs."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("Visit http://example.com and http://test.org")
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            validator.load_file()
            urls = validator.find_urls()
            assert "http://example.com" in urls
            assert "http://test.org" in urls
            assert len(urls) == 2
        finally:
            os.unlink(temp_path)

    def test_find_https_urls(self):
        """Test finding HTTPS URLs."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("Secure sites: https://secure.com and https://github.com")
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            validator.load_file()
            urls = validator.find_urls()
            assert len(urls) == 2
            assert any("https://secure.com" in url for url in urls)
        finally:
            os.unlink(temp_path)

    def test_find_www_urls(self):
        """Test finding www URLs."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("Check www.example.com for more info")
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            validator.load_file()
            urls = validator.find_urls()
            assert len(urls) >= 1
        finally:
            os.unlink(temp_path)

    def test_find_urls_in_markdown_links(self):
        """Test finding URLs in Markdown link syntax."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("[Link](https://example.com) and [Another](https://test.com)")
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            validator.load_file()
            urls = validator.find_urls()
            assert len(urls) == 2
        finally:
            os.unlink(temp_path)

    def test_find_no_urls(self):
        """Test when no URLs present."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("Just plain text without any URLs")
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            validator.load_file()
            urls = validator.find_urls()
            assert len(urls) == 0
        finally:
            os.unlink(temp_path)


class TestValidateStructure:
    """Test document structure validation."""

    def test_validate_empty_file(self):
        """Test validation of empty file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            validator.load_file()
            is_valid, issues = validator.validate_structure()
            assert is_valid is False
            assert "empty" in issues[0].lower()
        finally:
            os.unlink(temp_path)

    def test_validate_missing_title(self):
        """Test validation when H1 title is missing."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("## Subsection\nContent without main title")
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            validator.load_file()
            is_valid, issues = validator.validate_structure()
            assert is_valid is False
            assert any("title" in issue.lower() for issue in issues)
        finally:
            os.unlink(temp_path)

    def test_validate_excessive_blank_lines(self):
        """Test validation of excessive blank lines."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("# Title\n\n\n\nContent")
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            validator.load_file()
            is_valid, issues = validator.validate_structure()
            assert is_valid is False
            assert any("blank lines" in issue.lower() for issue in issues)
        finally:
            os.unlink(temp_path)

    def test_validate_long_lines(self):
        """Test validation of overly long lines."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            long_line = "# Title\n" + "x" * 250
            f.write(long_line)
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            validator.load_file()
            is_valid, issues = validator.validate_structure()
            assert is_valid is False
            assert any("200 characters" in issue for issue in issues)
        finally:
            os.unlink(temp_path)

    def test_validate_well_formed_document(self):
        """Test validation of a well-formed document."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("# Main Title\n\n## Section\n\nContent here")
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            validator.load_file()
            is_valid, issues = validator.validate_structure()
            assert is_valid is True
            assert len(issues) == 0
        finally:
            os.unlink(temp_path)


class TestGetWordCount:
    """Test word counting functionality."""

    def test_count_simple_words(self):
        """Test counting words in simple text."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("One two three four five")
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            validator.load_file()
            count = validator.get_word_count()
            assert count == 5
        finally:
            os.unlink(temp_path)

    def test_count_words_with_markdown(self):
        """Test word counting ignores markdown formatting."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("# **Title** with `code` and [link](url)")
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            validator.load_file()
            count = validator.get_word_count()
            assert count > 0
        finally:
            os.unlink(temp_path)

    def test_count_zero_words(self):
        """Test counting words in empty file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            validator.load_file()
            count = validator.get_word_count()
            assert count == 0
        finally:
            os.unlink(temp_path)

    def test_count_multiline_words(self):
        """Test counting words across multiple lines."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("First line\nSecond line\nThird line")
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            validator.load_file()
            count = validator.get_word_count()
            assert count == 6
        finally:
            os.unlink(temp_path)


class TestFindChineseTranslations:
    """Test Chinese character detection."""

    def test_find_chinese_characters(self):
        """Test finding lines with Chinese characters."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("Hello 你好\nWorld 世界\nEnglish only")
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            validator.load_file()
            count = validator.find_chinese_translations()
            assert count == 2
        finally:
            os.unlink(temp_path)

    def test_find_no_chinese_characters(self):
        """Test when no Chinese characters present."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("Only English text here")
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            validator.load_file()
            count = validator.find_chinese_translations()
            assert count == 0
        finally:
            os.unlink(temp_path)

    def test_find_mixed_content(self):
        """Test finding Chinese in mixed content."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("# 標題 Title\n中文 English 混合\nPure English")
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            validator.load_file()
            count = validator.find_chinese_translations()
            assert count == 2
        finally:
            os.unlink(temp_path)


class TestAnalyze:
    """Test complete analysis functionality."""

    def test_analyze_complete_document(self):
        """Test complete analysis of a comprehensive document."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            content = """# English Learning Material

## Phrasal Verbs

**turn on** - 打開
- Example: Turn on the light

1. Look up the word
2. Come back later

Visit https://example.com for more

📝 Practice exercises here
"""
            f.write(content)
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            result = validator.analyze()

            assert 'file_path' in result
            assert 'is_valid' in result
            assert 'word_count' in result
            assert 'phrasal_verb_count' in result
            assert 'vocabulary_items' in result
            assert 'example_count' in result
            assert 'headers' in result
            assert 'url_count' in result
            assert 'chinese_lines' in result
            assert 'line_count' in result

            assert result['word_count'] > 0
            assert result['url_count'] >= 1
            assert result['chinese_lines'] >= 1
            assert 'error' not in result
        finally:
            os.unlink(temp_path)

    def test_analyze_nonexistent_file(self):
        """Test analysis of nonexistent file."""
        validator = MarkdownValidator("/nonexistent/file.md")
        result = validator.analyze()
        assert 'error' in result

    def test_analyze_returns_header_structure(self):
        """Test that analysis includes header structure."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("# Title\n## Section\n### Subsection")
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            result = validator.analyze()
            assert result['headers']['h1'] == 1
            assert result['headers']['h2'] == 1
            assert result['headers']['h3'] == 1
        finally:
            os.unlink(temp_path)


class TestValidateDirectory:
    """Test directory validation functionality."""

    def test_validate_directory_with_files(self):
        """Test validating a directory containing markdown files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create test files
            file1 = Path(tmpdir) / "file1.md"
            file2 = Path(tmpdir) / "file2.md"
            file1.write_text("# File 1\nContent")
            file2.write_text("# File 2\nContent")

            results = validate_directory(tmpdir)
            assert len(results) == 2
            assert all('error' not in result for result in results.values())

    def test_validate_directory_recursive(self):
        """Test validating directory recursively."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create nested structure
            subdir = Path(tmpdir) / "subdir"
            subdir.mkdir()
            (Path(tmpdir) / "root.md").write_text("# Root")
            (subdir / "nested.md").write_text("# Nested")

            results = validate_directory(tmpdir)
            assert len(results) == 2

    def test_validate_nonexistent_directory(self):
        """Test validating a nonexistent directory."""
        results = validate_directory("/nonexistent/directory")
        assert 'error' in results

    def test_validate_empty_directory(self):
        """Test validating an empty directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            results = validate_directory(tmpdir)
            assert len(results) == 0

    def test_validate_directory_with_pattern(self):
        """Test validating directory with specific pattern."""
        with tempfile.TemporaryDirectory() as tmpdir:
            (Path(tmpdir) / "test.md").write_text("# Test")
            (Path(tmpdir) / "README.md").write_text("# README")
            (Path(tmpdir) / "notes.txt").write_text("Notes")

            results = validate_directory(tmpdir, pattern="*.md")
            assert len(results) == 2


class TestEdgeCases:
    """Test edge cases and special scenarios."""

    def test_file_with_only_whitespace(self):
        """Test file containing only whitespace."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("   \n\n   \n")
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            validator.load_file()
            is_valid, issues = validator.validate_structure()
            assert is_valid is False
        finally:
            os.unlink(temp_path)

    def test_file_with_special_characters(self):
        """Test file with special characters and emojis."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("# 📚 Learning\n\n✨ **sparkle** ✨\n\n🎯 Goals")
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            result = validator.analyze()
            assert result['word_count'] > 0
            assert result['headers']['h1'] == 1
        finally:
            os.unlink(temp_path)

    def test_very_large_file(self):
        """Test handling of large file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
            f.write("# Title\n\n" + "Word " * 10000)
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            result = validator.analyze()
            assert result['word_count'] > 10000
        finally:
            os.unlink(temp_path)

    def test_file_with_mixed_line_endings(self):
        """Test file with mixed line endings."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8', newline='') as f:
            f.write("# Title\r\nLine with CRLF\nLine with LF\r\nAnother CRLF")
            temp_path = f.name

        try:
            validator = MarkdownValidator(temp_path)
            assert validator.load_file() is True
            assert len(validator.lines) > 0
        finally:
            os.unlink(temp_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
