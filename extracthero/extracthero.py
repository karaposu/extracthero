#extracthero.py

import re
from typing import Any, Dict
from time import time

from myllmservice import MyLLMService
from extracthero.schemes import ExtractConfig
from extracthero.schemes import FilterOp, ParseOp, ExtractOp
from domreducer import HTMLReducer
import json
from json import JSONDecodeError
# from string2Dict

from string2dict import String2Dict



class Extractor:
    def __init__(self, config: ExtractConfig = None, myllmservice=None):
        self.config = config or ExtractConfig()
        self.myllmservice = myllmservice or MyLLMService()

    def filter_with_llm(
        self, text: str, thing_to_extract: str, text_type: str = None
    ) -> FilterOp:
        start_time = time()
        reduced_html = None
        
        # 1. HTML reduction if needed
        if text_type == "html":
            reducer = HTMLReducer()
            reduce_op = reducer.reduce(text)
            if reduce_op.success:
                corpus = reduce_op.reduced_data
                reduced_html = reduce_op.reduced_data
            else:
                corpus = text
        else:
            corpus = text

        
        
        if text_type == "json":

            s2d=String2Dict()
            parsed_dict= s2d.run(text)
            if parsed_dict is None:
                return FilterOp.from_result(
                    config=self.config,
                    content=None,
                    usage=None,
                    reduced_html=None,
                    start_time=start_time,
                    success=False,
                    error="text_type=json but json is invalid"
                )
            if isinstance(thing_to_extract, list):
                content = {key: parsed_dict.get(key) for key in thing_to_extract}
            else:
                content = parsed_dict.get(thing_to_extract)
            return FilterOp.from_result(
                config=self.config,
                content=content,
                usage=None,
                reduced_html=None,
                start_time=start_time,
                success=True
            )
        
        # 
        # 2. LLM-based filtering
        generation_result = self.myllmservice.filter_via_llm(corpus, thing_to_extract)
        
        # 3. Wrap in FilterOp
        return FilterOp.from_result(
            config=self.config,
            content=generation_result.content if generation_result.success else None,
            usage=generation_result.usage,
            reduced_html=reduced_html,
            start_time=start_time,
            success=generation_result.success
        )

    def parser(self, corpus: str, thing_to_extract: str) -> ParseOp:
        start_time = time()
        result = self.myllmservice.parse_via_llm(corpus, thing_to_extract)
        return ParseOp.from_result(
            config=self.config,
            content=result.content if result.success else None,
            usage=result.usage,
            start_time=start_time,
            success=result.success
        )

    def extract(
        self, text: str, thing_to_extract: str, text_type: str = None
    ) -> ExtractOp:
        # Filter phase
        filter_op = self.filter_with_llm(text, thing_to_extract, text_type)
        if not filter_op.success:
            # short-circuit parse on filter failure
            parse_start = time()
            parse_op = ParseOp.from_result(
                config=self.config,
                content=None,
                usage=None,
                start_time=parse_start,
                success=False
            )
            return ExtractOp(filter_op=filter_op, parse_op=parse_op)

        # Parse phase
        parse_op = self.parser(filter_op.content, thing_to_extract)
        return ExtractOp(filter_op=filter_op, parse_op=parse_op)

    def check_if_contains_mandatory_keywords(self, text: str) -> bool:
        if not self.config.must_exist_keywords:
            return True
        flags = 0 if self.config.keyword_case_sensitive else re.IGNORECASE
        for kw in self.config.must_exist_keywords:
            pattern = (
                rf"\b{re.escape(kw)}\b"
                if self.config.keyword_whole_word
                else re.escape(kw)
            )
            if not re.search(pattern, text, flags):
                return False
        return True

    def confirm_that_content_theme_is_relevant_to_our_search(self, text: str) -> bool:
        if not self.config.semantics_exist_validation:
            return True
        result = self.myllmservice.confirm_that_content_theme_is_relevant_to_our_search(
            text, self.config.semantics_exist_validation
        )
        return bool(result.content)

    def isolate_relevant_chunk_only(self, text: str) -> str:
        result = self.myllmservice.isolate_relevant_chunk_only(
            text, self.config.semantic_chunk_isolation
        )
        return result.content

    def output_format_check_with_regex(self, results: Dict[str, Any]) -> bool:
        if not self.config.regex_validation:
            return True
        for field, pattern in self.config.regex_validation.items():
            value = results.get(field)
            if value is None or not re.fullmatch(pattern, str(value)):
                return False
        return True


def main():
    extractor = Extractor()
    # example usage...
    sample_html = "<html>...</html>"
    op = extractor.extract(sample_html, "Extract product names", text_type="html")
    print(op)


if __name__ == "__main__":
    main()
