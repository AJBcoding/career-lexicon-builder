"""Tests for format_cv.py CLI argument parsing."""
import sys
import unittest
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path
import json


class TestDocumentTypeFlag(unittest.TestCase):
    """Test --document-type flag parsing and behavior."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_content = [
            {"text": "Test", "style": "Body Text", "type": "paragraph"}
        ]
        self.input_json = json.dumps(self.test_content)

    @patch('format_cv.StyleApplicator')
    @patch('builtins.open', new_callable=mock_open)
    def test_document_type_cv_accepted(self, mock_file, mock_applicator):
        """Test that --document-type cv is accepted and parsed correctly."""
        # Setup mocks
        mock_file.return_value.__enter__.return_value.read.return_value = self.input_json

        # Mock Path objects
        with patch('format_cv.Path') as mock_path_cls:
            # Mock input/output paths
            mock_input_path = MagicMock()
            mock_input_path.exists.return_value = True

            mock_output_path = MagicMock()

            # Mock template path
            mock_template_path = MagicMock()
            mock_template_path.exists.return_value = True

            mock_home = MagicMock()
            mock_home.__truediv__ = MagicMock(side_effect=lambda x: mock_template_path if '.claude' in x else MagicMock())
            mock_path_cls.home.return_value = mock_home

            # Make Path() constructor return appropriate mocks
            def path_constructor(arg):
                if 'input.json' in str(arg):
                    return mock_input_path
                elif 'output.docx' in str(arg):
                    return mock_output_path
                return MagicMock()

            mock_path_cls.side_effect = path_constructor

            mock_instance = MagicMock()
            mock_instance.apply_styles.return_value = True
            mock_applicator.return_value = mock_instance

            # Simulate CLI args
            test_args = ['format_cv.py', 'input.json', 'output.docx', '--document-type', 'cv']

            with patch.object(sys, 'argv', test_args):
                import format_cv
                result = format_cv.main()

            # Verify success
            self.assertEqual(result, 0)

            # Verify StyleApplicator was called with document_type
            mock_instance.apply_styles.assert_called_once()
            args, kwargs = mock_instance.apply_styles.call_args
            self.assertEqual(kwargs.get('document_type'), 'cv')

    @patch('format_cv.StyleApplicator')
    @patch('builtins.open', new_callable=mock_open)
    def test_document_type_cover_letter_accepted(self, mock_file, mock_applicator):
        """Test that --document-type cover-letter is accepted and parsed correctly."""
        # Setup mocks
        mock_file.return_value.__enter__.return_value.read.return_value = self.input_json

        # Mock Path objects
        with patch('format_cv.Path') as mock_path_cls:
            # Mock input/output paths
            mock_input_path = MagicMock()
            mock_input_path.exists.return_value = True

            mock_output_path = MagicMock()

            # Mock template path
            mock_template_path = MagicMock()
            mock_template_path.exists.return_value = True

            mock_home = MagicMock()
            mock_home.__truediv__ = MagicMock(side_effect=lambda x: mock_template_path if '.claude' in x else MagicMock())
            mock_path_cls.home.return_value = mock_home

            # Make Path() constructor return appropriate mocks
            def path_constructor(arg):
                if 'input.json' in str(arg):
                    return mock_input_path
                elif 'output.docx' in str(arg):
                    return mock_output_path
                return MagicMock()

            mock_path_cls.side_effect = path_constructor

            mock_instance = MagicMock()
            mock_instance.apply_styles.return_value = True
            mock_applicator.return_value = mock_instance

            # Simulate CLI args
            test_args = ['format_cv.py', 'input.json', 'output.docx', '--document-type', 'cover-letter']

            with patch.object(sys, 'argv', test_args):
                import format_cv
                result = format_cv.main()

            # Verify success
            self.assertEqual(result, 0)

            # Verify StyleApplicator was called with document_type
            mock_instance.apply_styles.assert_called_once()
            args, kwargs = mock_instance.apply_styles.call_args
            self.assertEqual(kwargs.get('document_type'), 'cover-letter')

    @patch('format_cv.StyleApplicator')
    @patch('builtins.open', new_callable=mock_open)
    def test_document_type_defaults_to_cv(self, mock_file, mock_applicator):
        """Test that document_type defaults to 'cv' when flag is omitted."""
        # Setup mocks
        mock_file.return_value.__enter__.return_value.read.return_value = self.input_json

        # Mock Path objects
        with patch('format_cv.Path') as mock_path_cls:
            # Mock input/output paths
            mock_input_path = MagicMock()
            mock_input_path.exists.return_value = True

            mock_output_path = MagicMock()

            # Mock template path
            mock_template_path = MagicMock()
            mock_template_path.exists.return_value = True

            mock_home = MagicMock()
            mock_home.__truediv__ = MagicMock(side_effect=lambda x: mock_template_path if '.claude' in x else MagicMock())
            mock_path_cls.home.return_value = mock_home

            # Make Path() constructor return appropriate mocks
            def path_constructor(arg):
                if 'input.json' in str(arg):
                    return mock_input_path
                elif 'output.docx' in str(arg):
                    return mock_output_path
                return MagicMock()

            mock_path_cls.side_effect = path_constructor

            mock_instance = MagicMock()
            mock_instance.apply_styles.return_value = True
            mock_applicator.return_value = mock_instance

            # Simulate CLI args WITHOUT --document-type
            test_args = ['format_cv.py', 'input.json', 'output.docx']

            with patch.object(sys, 'argv', test_args):
                import format_cv
                result = format_cv.main()

            # Verify success
            self.assertEqual(result, 0)

            # Verify StyleApplicator was called with default document_type
            mock_instance.apply_styles.assert_called_once()
            args, kwargs = mock_instance.apply_styles.call_args
            self.assertEqual(kwargs.get('document_type'), 'cv')

    def test_document_type_invalid_value_rejected(self):
        """Test that invalid --document-type values are rejected."""
        # Simulate CLI args with invalid document type
        test_args = ['format_cv.py', 'input.json', 'output.docx', '--document-type', 'invalid']

        with patch.object(sys, 'argv', test_args):
            import format_cv
            result = format_cv.main()

        # Should fail with error
        self.assertEqual(result, 1)


if __name__ == '__main__':
    unittest.main()
