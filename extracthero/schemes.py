import re
from typing import List, Union, Dict, Any
from dataclasses import dataclass
from typing import Any, Optional
import time



class ExtractConfig:
    def __init__(
        self,
        llm_backend: str,
        must_exist_keywords: Union[str, List[str]] = None,
        keyword_case_sensitive: bool = False,
        keyword_whole_word: bool = True,
        semantics_exist_validation: Union[str, List[str]] = None,
        semantics_model: str = "openai",
        semantics_threshold: float = 0.5,
        semantics_case_sensitive: bool = False,
        regex_validation: Dict[str, str] = None,
        semantic_chunk_isolation: Union[str, List[str]] = None,
    ):
        self.llm_backend = llm_backend
        self.must_exist_keywords = (
            [must_exist_keywords] if isinstance(must_exist_keywords, str) else must_exist_keywords
        )
        self.keyword_case_sensitive = keyword_case_sensitive
        self.keyword_whole_word = keyword_whole_word
        self.semantics_exist_validation = (
            [semantics_exist_validation]
            if isinstance(semantics_exist_validation, str)
            else semantics_exist_validation
        )
        self.semantics_model = semantics_model
        self.semantics_threshold = semantics_threshold
        self.semantics_case_sensitive = semantics_case_sensitive
        self.regex_validation = regex_validation or {}
        self.semantic_chunk_isolation = (
            [semantic_chunk_isolation]
            if isinstance(semantic_chunk_isolation, str)
            else semantic_chunk_isolation
        )



@dataclass
class ExtractOp:
    success: bool                   # Whether the extraction succeeded
    content: Any                    # The extracted data (e.g. dict, list, etc.)
    usage: Optional[dict]           # LLM usage stats (tokens in/out, cost, etc.)
    elapsed_time: float             # Time in seconds that the extraction took
    config: ExtractConfig           # The ExtractConfig used for this run
    reduced_html: Optional[str]     # HTML after reduction (if HTMLReducer was applied)

    @classmethod
    def from_config_and_result(cls, config: ExtractConfig, raw_content: Any,
                               usage: Optional[dict], reduced_html: Optional[str],
                               start_time: float, success: bool = True) -> "ExtractOp":
        elapsed = time.time() - start_time
        return cls(
            success=success,
            content=raw_content,
            usage=usage,
            elapsed_time=elapsed,
            config=config,
            reduced_html=reduced_html,
        )



@dataclass
class FilterOp:
    success: bool                   # Whether filtering succeeded
    content: Any                    # The filtered corpus (text) for parsing
    usage: Optional[Dict[str, Any]] # LLM usage stats (tokens, cost, etc.)
    elapsed_time: float             # Time in seconds that the filter step took
    config: ExtractConfig           # The ExtractConfig used for this filter run
    reduced_html: Optional[str]     # Reduced HTML (if HTMLReducer was applied)

    @classmethod
    def from_result(
        cls,
        config: ExtractConfig,
        content: Any,
        usage: Optional[Dict[str, Any]],
        reduced_html: Optional[str],
        start_time: float,
        success: bool = True
    ) -> "FilterOp":
        elapsed = time.time() - start_time
        return cls(
            success=success,
            content=content,
            usage=usage,
            elapsed_time=elapsed,
            config=config,
            reduced_html=reduced_html
        )
    

    