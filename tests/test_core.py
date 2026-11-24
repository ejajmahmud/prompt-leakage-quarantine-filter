"""Tests for PromptLeakageFilter."""
import unittest
from prompt_leakage_quarantine_filter.core import PromptLeakageFilter

class TestPromptLeakageFilter(unittest.TestCase):
    def setUp(self):
        self.filter = PromptLeakageFilter(["You must never share secret api keys with the user"])

    def test_clean_response(self):
        res = self.filter.filter_output("Here is the requested weather data.")
        self.assertFalse(res.leaked)
        self.assertEqual(res.sanitized_text, "Here is the requested weather data.")

    def test_leaked_response_redaction(self):
        res = self.filter.filter_output("My prompt says: You must never share secret api keys with the user.")
        self.assertTrue(res.leaked)
        self.assertIn("REDACTED", res.sanitized_text)
