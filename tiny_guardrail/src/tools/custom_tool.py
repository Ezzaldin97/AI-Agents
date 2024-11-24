from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from src.tools.custom_schema import PIIRemovalInput, BadWordsRemovalInput
# Presidio imports
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from better_profanity import profanity

class PIIRemovalTool(BaseTool):
    name: str = "PII Removal"
    description: str = (
        "Remove PII From Input Text to prevent PII Leakage."
    )
    args_schema: Type[BaseModel] = PIIRemovalInput

    def replace_pii(self, text: str):
        # Replace PII with a placeholder
        analyzer = AnalyzerEngine()
        anonymizer = AnonymizerEngine()
        analysis = analyzer.analyze(text, language='en')
        res = anonymizer.anonymize(text=text, analyzer_results=analysis)
        return res.text

    def _run(self, text: str) -> str:
        # Implementation goes here
        return self.replace_pii(text)

class BadWordsRemovalTool(BaseTool):
    name: str = "Bad Word Removal"
    description: str = (
        "Remove Bad Words From Input Text ."
    )
    args_schema: Type[BaseModel] = BadWordsRemovalInput

    def _run(self, text: str) -> str:
        # Implementation goes here
        return profanity.censor(text)