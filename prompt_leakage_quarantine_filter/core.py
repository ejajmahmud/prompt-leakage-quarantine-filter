"""Core Prompt Leakage Quarantine Filter implementation."""
from typing import Dict, Any, List, Set

class FilterResult:
    def __init__(self, leaked: bool, sanitized_text: str, detected_rules: List[str]):
        self.leaked = leaked
        self.sanitized_text = sanitized_text
        self.detected_rules = detected_rules

class PromptLeakageFilter:
    def __init__(self, confidential_rules: Optional[List[str]] = None):
        self.rules = confidential_rules or []
        self._rule_fingerprints: List[Set[str]] = [self._tokenize(r) for r in self.rules]

    @staticmethod
    def _tokenize(text: str) -> Set[str]:
        words = text.lower().split()
        return set(words)

    def add_confidential_rule(self, rule_text: str):
        self.rules.append(rule_text)
        self._rule_fingerprints.append(self._tokenize(rule_text))

    def filter_output(self, output_text: str, overlap_threshold: float = 0.6) -> FilterResult:
        out_tokens = self._tokenize(output_text)
        if not out_tokens:
            return FilterResult(False, output_text, [])

        leaked_rules = []
        sanitized = output_text

        for idx, rule_set in enumerate(self._rule_fingerprints):
            if not rule_set:
                continue
            common = out_tokens.intersection(rule_set)
            overlap = len(common) / len(rule_set)
            if overlap >= overlap_threshold:
                leaked_rules.append(self.rules[idx])
                sanitized = "[CONFIDENTIAL SYSTEM INSTRUCTION REDACTED]"

        return FilterResult(len(leaked_rules) > 0, sanitized, leaked_rules)
