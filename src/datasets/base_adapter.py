from abc import ABC, abstractmethod
from typing import Iterable, Dict, Any, List

class DatasetAdapter(ABC):
    """Standardizes any dataset to JSONL rows with keys: input, reference, meta."""
    @abstractmethod
    def load_records(self, raw_path: str) -> List[Dict[str, Any]]:
        ...

    @abstractmethod
    def to_examples(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Return list of {"input": str, "reference": str, "meta": {...}}"""
        ...
