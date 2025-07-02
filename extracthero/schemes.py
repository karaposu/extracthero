#schemes.py

import re
from typing import List, Union, Dict, Any, Optional
from dataclasses import dataclass
from typing import Any, Optional
import time


from dataclasses import dataclass, field
from typing import List, Optional

# 

@dataclass
class CorpusPayload:
    corpus:       str                # Text input or original JSON string
    corpus_type:  str                # "html", "json" or "text"
    reduced_html: Optional[str]      # Only when HTML is reduced
    error:        Optional[str] = None    # ← give a default

@dataclass
class CorpusPayload:
    corpus:        Any                     # str or dict
    corpus_type:   str                     # "html" | "json" | "text"
    reduced_html:  Optional[str] = None
    # reduce_op:     Optional[Any] = None   # holds the full ReduceOperation object
    error:         Optional[str] = None

from dataclasses import dataclass, field
from typing import List, Optional




@dataclass
class WhatToRetain:
    """
    Specification for FilterHero’s “guidable selective semantic context chunking”.

    Parameters
    ----------
    name : str
         A short identifier (e.g., "product name", "person profile").
    desc : Optional[str]
       An LLM-readable, definitive description of the item to filter.  
        For example, for a product name you might write:  
        “Title of the product as it is listed.”
    include_context_chunk : bool
        If True (default), instructs the LLM to retain the entire semantic
        content relevant to this item.
    custom_context_chunk_desc : Optional[str]
        Extra guidance that refines what “context chunk” means.  
        Example: “Only non-technical sales information—exclude technical
        attributes.”
    wrt_to_source_filter_desc : Optional[str]
        Free-text relevance hint that narrows the selection with respect to the
        page’s main subject.  
        Examples: “Primary product only”;  
        “Should not include side products like recommendations.”
    
    context_contradiction_check : bool
        If True, instructs the LLM to discard chunks that clearly contradict
        `target_context`, while retaining any ambiguous or matching ones.
    text_rules : Optional[List[str]]
        Additional bullet-point rules to refine inclusion/exclusion logic.
    """
    
    # ───────── core fields ─────────
    name: str
    desc: Optional[str] = None
    include_context_chunk: bool = True
    custom_context_chunk_desc: Optional[str] = None
    wrt_to_source_filter_desc: Optional[str] = None
    
    # ───────── context targeting ────
    identifier_context_contradiction_check: bool = False
    
    # ───────── extra rules ──────────
    text_rules: Optional[List[str]] = None

    regex_validator: Optional[str] = None      # format guard

    # example
    example: Optional[str] = None

    # ─────── prompt builder ────────
    def compile(self) -> str:
        parts: List[str] = [f"Chunk name: {self.name}"]

        if self.desc:
            parts.append(f"Description: {self.desc}")

        if self.example:
            parts.append(f"Example: {self.example}")


        if self.include_context_chunk:
            ctx = (
                self.custom_context_chunk_desc
                or "Include the entire semantic block that represents this item."
            )
            parts.append(f"Context guidance: {ctx}")

        if self.wrt_to_source_filter_desc:
            parts.append(
                f"Relevance hint w.r.t. page source: {self.wrt_to_source_filter_desc}"
            )

        

        if self.identifier_context_contradiction_check:
            parts.append(
                "Contradiction rule: Discard chunks that clearly contradict the "
                "target context above, but retain any that might still be relevant."
            )

        if self.text_rules:
            parts.append("Additional rules: " + "; ".join(self.text_rules))

        return "\n".join(parts)
    


    # ─────── prompt builder ────────
    def compile_parser(self) -> str:
        parts: List[str] = [f"keyword: {self.name}"]

        if self.desc:
            parts.append(f"keyword description: {self.desc}")

        # if self.include_context_chunk:
        #     ctx = (
        #         self.custom_context_chunk_desc
        #         or "Include the entire semantic block that represents this item."
        #     )
        #     parts.append(f"Context guidance: {ctx}")

     
        if self.text_rules:
            parts.append("Additional rules: " + "; ".join(self.text_rules))

        return "\n".join(parts)
    







@dataclass
class ItemToExtract:
    name: str                                  # e.g. "price"
    desc: Optional[str] = None                 # human-readable description
    regex_validator: Optional[str] = None      # format guard
    text_rules: List[str] = field(default_factory=list)
    example: Optional[str] = None

    # ───────────── context options ─────────
    include_context_chunk: bool = False        # keep the entire semantic chunk?
    custom_context_chunk_desc: Optional[str] = None
    # if set, guides the LLM on how to pick the surrounding context chunk;
    # if None, the LLM decides boundaries automatically

    def compile(self) -> str:
        sections: List[str] = [f"Field name: {self.name}"]

        if self.desc:
            sections.append(f"Field description: {self.desc}")

        if self.text_rules:
            sections.append("Text rules: " + "; ".join(self.text_rules))

        if self.example:
            sections.append(f"Example: {self.example}")

        if self.include_context_chunk:
            guidance = (
                self.custom_context_chunk_desc
                or "Include the full semantic context block that belongs "
                   "to this field (e.g., the <div class='product'> element)."
            )
            sections.append(f"Context guidance: {guidance}")

        return "\n".join(sections)
    




    







class ExtractConfig:
    def __init__(
        self,
        must_exist_keywords: Union[str, List[str]] = None,
        keyword_case_sensitive: bool = False,
        keyword_whole_word: bool = True,
        semantics_exist_validation: Union[str, List[str]] = None,
        semantics_model: str = "gpt-4o-mini",
        regex_validation: Dict[str, str] = None,
        semantic_chunk_isolation: Union[str, List[str]] = None,
    ):
      
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
        self.regex_validation = regex_validation or {}
        self.semantic_chunk_isolation = (
            [semantic_chunk_isolation]
            if isinstance(semantic_chunk_isolation, str)
            else semantic_chunk_isolation
        )




@dataclass
class FilterOp:
    success: bool                   # Whether filtering succeeded
    content: Any                    # The filtered corpus (text) for parsing
    usage: Optional[Dict[str, Any]] # LLM usage stats (tokens, cost, etc.)
    elapsed_time: float             # Time in seconds that the filter step took
    config: ExtractConfig           # The ExtractConfig used for this filter run
    reduced_html: Optional[str]     # Reduced HTML (if HTMLReducer was applied)
    html_reduce_op:     Optional[Any] = None   # holds the full Domreducer ReduceOperation object
  
    error: Optional[str] = None   

    @classmethod
    def from_result(
        cls,
        config: ExtractConfig,
        content: Any,
        usage: Optional[Dict[str, Any]],
        reduced_html: Optional[str],
        start_time: float,
        html_reduce_op: Optional[Any] = None ,
        success: bool = True,
        error: Optional[str] = None
    ) -> "FilterOp":
        elapsed = time.time() - start_time
        return cls(
            success=success,
            content=content,
            usage=usage,
            elapsed_time=elapsed,
            config=config,
            reduced_html=reduced_html,
            html_reduce_op=html_reduce_op,         # ← pass it here
            error=error
        )
    


@dataclass
class ProcessResult:
    fast_op:   Optional[FilterOp]   # ready-to-return FilterOp (JSON path)
    corpus:    Optional[str]        # always a string if we need the LLM
    reduced:   Optional[str]        # reduced HTML snippet (may be None)
    


@dataclass
class ParseOp:
    success: bool                                  # Whether parsing succeeded
    content: Any                                   # The parsed result (e.g. dict, list, etc.)
    usage: Optional[Dict[str, Any]]                # LLM usage stats for parsing step
    elapsed_time: float                            # Time in seconds that the parse step took
    config: ExtractConfig                          # The ExtractConfig used for this parse run
    error: Optional[str] = None                    # Optional error message if success=False
    generation_result: Optional[Any] =None
    
    @classmethod
    def from_result(
        cls,
        config: ExtractConfig,
        content: Any,
        usage: Optional[Dict[str, Any]],
        start_time: float,
        success: bool = True,
        error: Optional[str] = None,
        generation_result=generation_result
    ) -> "ParseOp":
        elapsed = time.time() - start_time
        return cls(
            success=success,
            content=content,
            usage=usage,
            elapsed_time=elapsed,
            config=config,
            error=error, 
            generation_result=generation_result
        )

    


@dataclass
class ExtractOp:
    filter_op: FilterOp
    parse_op: ParseOp
    content: Optional[Any] = None       


    @property
    def success(self) -> bool:
        return self.filter_op.success and self.parse_op.success

