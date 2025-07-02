# extracthero/parsehero.py
# run with: python -m extracthero.parsehero


"""
ParseHero — the “parse” phase of ExtractHero.
  • Converts a filtered corpus into structured data keyed by WhatToRetain specs.
  • Skips the LLM when the corpus is already a dict, unless you force it.
  • Performs per-field regex validation after parsing.
  • Returns a ParseOp.
"""

from __future__ import annotations

import json as _json
from time import time
from typing import Any, Dict, List, Optional, Tuple, Union

from llmservice.generation_engine import GenerationResult
from extracthero.myllmservice import MyLLMService
from extracthero.schemes import ExtractConfig, ParseOp, WhatToRetain

import warnings
warnings.filterwarnings(
    "ignore",
    category=RuntimeWarning,
    message=r".*extracthero\.parsehero.*"
)


class ParseHero:
    # ───────────────────────── init ─────────────────────────
    def __init__(
        self,
        config: Optional[ExtractConfig] = None,
        llm: Optional[MyLLMService] = None,
    ):
        self.config = config or ExtractConfig()
        self.llm = llm or MyLLMService()

    # ───────────────────────── public ───────────────────────
    def run(
        self,
        corpus: str | Dict[str, Any],
        items: WhatToRetain | List[WhatToRetain],
        enforce_llm_based_parse: bool = False,
    ) -> ParseOp:
        """
        Same semantics as `run`, but non-blocking.
        Requires your `MyLLMService` to expose `parse_via_llm_async`.
        """
        start_ts = time()


        if isinstance(corpus, dict):

            if enforce_llm_based_parse:

                pass


            else:
                parsed_values_dict = self.make_new_dict_by_parsing_keys_with_their_values(corpus, items)
                return ParseOp.from_result(
                                        config=self.config,
                                        content=parsed_values_dict ,
                                        usage=None,
                                        start_time=start_ts,
                                        success=True,    
            )
        elif isinstance(corpus, str):
            try:
                corpus_dict = _json.loads(corpus)
                parsed_values_dict = self.make_new_dict_by_parsing_keys_with_their_values(corpus_dict, items)
                return ParseOp.from_result(
                                        config=self.config,
                                        content=parsed_values_dict ,
                                        usage=None,
                                        start_time=start_ts,
                                        success=True,    
                 )
                
            except Exception:
               
                pass # dont do anything, bc it is true string and we will use LLM to parse

        

        # if code reaches here it means corpus is string and not json or dict
   
        # creating prompt

        if isinstance(items, WhatToRetain):
            prompt = (items.compile_parser())
        else:
            prompt="\n\n".join(it.compile_parser() for it in items)

        

        # 4. call async LLM
        model= "gpt-4o"
        # model= "gpt-4o-mini"
        gen = self.llm.parse_via_llm(corpus, prompt, model=model)


        
        if not gen.success:
            return ParseOp.from_result(
                config=self.config,
                content=None,
                usage=gen.usage,
                start_time=start_ts,
                success=False,
                error="LLM parse failed",
              
            )

        # 5. decode JSON
        parsed_dict=gen.content
        

        return ParseOp.from_result(
            config=self.config,
            content=parsed_dict,
            usage=gen.usage,
            start_time=start_ts,
            success=True,
            error=None,
            generation_result=gen
        )


    # ───────────────────── helper utilities ─────────────────────
    @staticmethod
    def make_new_dict_by_parsing_keys_with_their_values(
        data: Dict[str, Any],
        items: WhatToRetain | List[WhatToRetain],
    ) -> Dict[str, Any]:
        keys = [items.name] if isinstance(items, WhatToRetain) else [it.name for it in items]
        return {k: data.get(k) for k in keys}

    # @staticmethod
    # def _regex_validate(
    #     data: Dict[str, Any],
    #     items: WhatToRetain | List[WhatToRetain],
    # ) -> Tuple[bool, Optional[str]]:
    #     item_list = [items] if isinstance(items, WhatToRetain) else items
    #     import re

    #     for it in item_list:
    #         if it.regex_validator and it.name in data:
    #             if data[it.name] is None or not re.fullmatch(it.regex_validator, str(data[it.name])):
    #                 return False, f"Field '{it.name}' failed regex validation"
    #     return True, None
    

        # ───────────────────────── public (async) ───────────────────────
    
    async def run_async(
        self,
        corpus: str | Dict[str, Any],
        items: WhatToRetain | List[WhatToRetain],
        enforce_llm_based_parse: bool = False,
    ) -> ParseOp:
        """
        Same semantics as `run`, but non-blocking.
        Requires your `MyLLMService` to expose `parse_via_llm_async`.
        """
        start_ts = time()


        if isinstance(corpus, dict):

            if enforce_llm_based_parse:

                pass


            else:
                parsed_values_dict = self.make_new_dict_by_parsing_keys_with_their_values(corpus, items)
                return ParseOp.from_result(
                                        config=self.config,
                                        content=parsed_values_dict ,
                                        usage=None,
                                        start_time=start_ts,
                                        success=True,    
            )
        elif isinstance(corpus, str):
            try:
                corpus_dict = _json.loads(corpus)
                parsed_values_dict = self.make_new_dict_by_parsing_keys_with_their_values(corpus_dict, items)
                return ParseOp.from_result(
                                        config=self.config,
                                        content=parsed_values_dict ,
                                        usage=None,
                                        start_time=start_ts,
                                        success=True,    
                 )
                
            except Exception:
               
                pass # dont do anything, bc it is true string and we will use LLM to parse

        

        # if code reaches here it means corpus is string and not json or dict
   
        # creating prompt

        if isinstance(items, WhatToRetain):
            prompt = (items.compile())
        else:
            "\n\n".join(it.compile() for it in items)

      
        
        # 4. call async LLM
        gen: GenerationResult = await self.llm.parse_via_llm_async(corpus, prompt)
        
        if not gen.success:
            return ParseOp.from_result(
                config=self.config,
                content=None,
                usage=gen.usage,
                start_time=start_ts,
                success=False,
                error="LLM parse failed",
            )

        # 5. decode JSON
        parsed_dict=gen.content
        

        return ParseOp.from_result(
            config=self.config,
            content=parsed_dict,
            usage=gen.usage,
            start_time=start_ts,
            success=True,
            error=None,
            generation_result=gen
        )


# ────────────────────────── demo ───────────────────────────
def main() -> None:
    cfg = ExtractConfig()
    hero = ParseHero(cfg)

    # items = [
    #     WhatToRetain(name="title", desc="Product title"),
    #     WhatToRetain(name="price", desc="Product price"),
    # ]


    # result dict should have a field called product 
    items = [
       #WhatToRetain(name="product", desc="Product info in plain text format, not json, DO NOT JSONIFY THIS PART!"),
       
        #  WhatToRetain(name="product", desc="Product title"),

         WhatToRetain(name="product_title", desc="Product title"),
         WhatToRetain(name="product_rating", desc="Product rating"),
        #  WhatToRetain(name="product_title"),
        # WhatToRetain(name="product", desc="Product info in SEO friendly format"),

        #   WhatToRetain(name="product", desc="Product info" , text_rules=["SEO friendly format plain text"]),
        #  WhatToRetain(name="SEO_mistakes", desc="Product price"),
    ]
    
    # 'product': title is Wireless Keyboard Pro and  price: €49.99,  list-price: €59.99,  rating: 4.5 ★  the availability: In Stock

    


    # filtered_text = """
    #     title: Wireless Keyboard Pro and  price: €49.99
    #     list-price: €59.99
    #     rating: 4.5 ★  the availability: In Stock
    #     delivery: Free next-day
    #     ---
    #     title: USB-C Hub (6-in-1)
    #     price: €29.50
    #     availability: Only 3 left!
    #     rating: 4.1 ★
    #     ---
    #     title: Gaming Mouse XT-8 and list_price: $42.00
    #     price: $35.00
    #     availability: Out of Stock
    #     warranty: 2-year limited
    #     ---
    #     title: Luggage Big 65 L
    #     availability: Pre-order (ships in 3 weeks)
    #     rating: 4.8 ★
    #     """
    
    filtered_text = """
        title: Wireless Keyboard Pro and  price: €49.99
        list-price: €59.99
        rating: 4.5 ★  the availability: In Stock
        delivery: Free next-day


        title: Fridge New
        
        """
    
    
    p_op = hero.run(filtered_text, items, enforce_llm_based_parse=True)
    print("Success:", p_op.success)

    #print(p_op.content)
    print(" " )
    parsed_dict=p_op.content
    if isinstance(parsed_dict, list):
        print("List elements:" )
        for e in parsed_dict:
            print(e)
    else:
        print("Parsed dict:", parsed_dict)
  
    print(" ")
    print(" ")
    print("debug formatted_prompt=:",  p_op.generation_result.generation_request.formatted_prompt)
   


if __name__ == "__main__":
    main()
