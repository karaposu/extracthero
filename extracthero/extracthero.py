import re
from typing import List, Union, Dict, Any
# from bs4 import BeautifulSoup
from myllmservice import MyLLMService
from extracthero.schemes import ExtractConfig, ExtractOp
from domreducer import HTMLReducer
from time import time



class Extractor:
    def __init__(self, config: ExtractConfig = None, myllmservice=None):
        self.config = config or ExtractConfig()
        self.myllmservice = myllmservice or MyLLMService()
       
    def filter_with_llm(self, text: str, thing_to_extract: str, text_type: str = None) -> ExtractOp:
        # 1. If HTML, reduce to visible text/layout context
        reduced_html = None
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

        # 2. LLM-based filtering
        generation_result = self.myllmservice.filter_via_llm(corpus, thing_to_extract)
        # wrap in ExtractOp

        return generation_result
        return ExtractOp.from_config_and_result(
            config=self.config,
            raw_content=generation_result.content if generation_result.success else None,
            usage=generation_result.usage,
            reduced_html=reduced_html,
            start_time=time.time() - 0,  # assume ExtractOp will compute elapsed internally
            success=generation_result.success
        )


    def filter_with_llm(self, text: str, thing_to_extract: str, text_type: str = None) -> Any:
      
        # 1. If HTML, reduce to visible text/layout context
        if text_type == "html":
            reducer = HTMLReducer()
            reduce_op = reducer.reduce(text)
            if reduce_op.success:
                corpus = reduce_op.reduced_data
            else:
                corpus = text
        else:
            corpus = text
        
        generation_result= self.myllmservice.filter_via_llm(corpus, thing_to_extract )
      
        return generation_result
    
    def parser(self, corpus, thing_to_extract):
        
        generation_result= self.myllmservice.parse_via_llm(corpus, thing_to_extract )
        return generation_result
    
    
    def extract(self, text, thing_to_extract, text_type=None) -> Any:
        if text_type == "html":
            filter_generation_result=self.filter_with_llm(text,thing_to_extract, text_type )
            if filter_generation_result.success:
                 new_corpus= filter_generation_result.content
            else:
                return False
        else:
            new_corpus= text

         
        parse_generation_result = self.parser(new_corpus, thing_to_extract)
        json_data= parse_generation_result.content

        return json_data



    
    
    def check_if_contains_mandatory_keywords(self, text: str) -> bool:
        if not self.config.must_exist_keywords:
            return True
        flags = 0 if self.config.keyword_case_sensitive else re.IGNORECASE
        for kw in self.config.must_exist_keywords:
            pattern = rf"\b{re.escape(kw)}\b" if self.config.keyword_whole_word else re.escape(kw)
            if not re.search(pattern, text, flags):
                return False
        return True

    def confirm_that_content_theme_is_relevant_to_our_search(self, text: str):
        if not self.config.semantics_exist_validation:
            return 
        generation_result= self.myllmservice.confirm_that_content_theme_is_relevant_to_our_search(text, self.config.semantics_exist_validation) 
        is_relevant = generation_result.content
        return is_relevant

    def isolate_relevant_chunk_only(self, text: str) -> str:
        # stub: uses LLM to isolate relevant chunk based on concepts
        
        generation_result= self.myllmservice.isolate_relevant_chunk_only(text, self.config._isolate_relevant_chunk_onlys) 
        isolated_chunk= generation_result.content
        return isolated_chunk

    def output_format_check_with_regex(self, results: Dict[str, Any]) -> bool:
        if not self.config.regex_validation:
            return True
        for field, pattern in self.config.regex_validation.items():
            value = results.get(field)
            if value is None or not re.fullmatch(pattern, str(value)):
                return False
        return True
    


def main():

     extractor=Extractor()



if __name__ == '__main__':
    main()
