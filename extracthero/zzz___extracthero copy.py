# extracthero/extracthero.py
# run with: python -m extracthero.extracthero

from __future__ import annotations

from time import time
from typing import List, Union, Optional, Tuple
import json

from extracthero.myllmservice import MyLLMService
from extracthero.schemes import (
    ExtractConfig,
    ExtractOp,
    FilterOp,
    FilterChainOp,
    ParseOp,
    WhatToRetain,
)
from extracthero.filterhero import FilterHero
from extracthero.parsehero import ParseHero
from extracthero.utils import load_html
from domreducer import HtmlReducer


class ExtractHero:
    """High-level orchestrator with 3 phases: HTML Reduction → Filter → Parse."""

    def __init__(self, config: ExtractConfig | None = None, llm: MyLLMService | None = None):
        self.config = config or ExtractConfig()
        self.llm = llm or MyLLMService()
        self.filter_hero = FilterHero(self.config, self.llm)
        self.parse_hero = ParseHero(self.config, self.llm)

    def extract(
        self,
        text: str | dict,
        extraction_spec: WhatToRetain | List[WhatToRetain],
        filter_strategy: str = "contextual",
        reduce_html: bool = True,
        model_name: Optional[str] = None,
    ) -> ExtractOp:
        """
        Three-phase extraction pipeline: HTML Reduction → Filter → Parse.

        Parameters
        ----------
        text : str | dict
            The source content to extract data from
        extraction_spec : WhatToRetain | List[WhatToRetain]
            Defines what data to extract and how
        filter_strategy : str
            Strategy for filtering ("contextual", "liberal", "inclusive", etc.)
        reduce_html : bool, default True
            Apply HTML reduction before filtering (only for HTML content)
        model_name : Optional[str]
            Specific model to use for LLM operations
            
        Returns
        -------
        ExtractOp
            Rich result object with content, timing, usage, and error details
        """
        extraction_start_time = time()
        
        # Initialize tracking variables
        reduced_html = None
        html_reduce_op = None
        corpus_to_filter = text
        
        # Phase 0: Optional HTML Reduction
        if reduce_html and isinstance(text, str) and "<" in text and ">" in text:
            try:
                html_reduce_op = HtmlReducer(str(text)).reduce()
                if html_reduce_op.success:
                    reduced_html = html_reduce_op.reduced_data
                    corpus_to_filter = html_reduce_op.reduced_data
                else:
                    corpus_to_filter = text
            except Exception as e:
                corpus_to_filter = text
        
        # Phase 1: Filtering
        filter_op: FilterOp = self.filter_hero.run(
            corpus_to_filter,
            extraction_spec,
            filter_strategy=filter_strategy
        )

        # Check if filter phase failed
        if not filter_op.success:
            parse_op = ParseOp.from_result(
                config=self.config,
                content=None,
                usage=None,
                start_time=time(),
                success=False,
                error="Filter phase failed - parse not attempted",
                generation_result=None
            )
            
            return ExtractOp.from_operations(
                filter_op=filter_op,
                parse_op=parse_op,
                start_time=extraction_start_time,
                content=None,
                reduced_html=reduced_html,
                html_reduce_op=html_reduce_op
            )

        # Phase 2: Parsing
        parse_op = self.parse_hero.run(
            filter_op.content, 
            extraction_spec,
            model_name=model_name
        )
        
        # Create ExtractOp with all metrics
        result = ExtractOp.from_operations(
            filter_op=filter_op,
            parse_op=parse_op,
            start_time=extraction_start_time,
            content=parse_op.content if parse_op.success else None,
            reduced_html=reduced_html,
            html_reduce_op=html_reduce_op
        )
        
        return result

    def extract_with_chain(
        self,
        text: str | dict,
        extraction_spec: WhatToRetain | List[WhatToRetain],
        filter_stages: List[Tuple[List[WhatToRetain], str]],
        reduce_html: bool = True,
        model_name: Optional[str] = None,
    ) -> ExtractOp:
        """
        Three-phase extraction with filter chaining.

        Parameters
        ----------
        text : str | dict
            The source content to extract data from
        extraction_spec : WhatToRetain | List[WhatToRetain]
            Final specifications for parsing
        filter_stages : List[Tuple[List[WhatToRetain], str]]
            List of (extraction_spec, filter_strategy) tuples for chaining
        reduce_html : bool, default True
            Apply HTML reduction before filtering
        model_name : Optional[str]
            Specific model to use
            
        Returns
        -------
        ExtractOp
            Rich result object with filter chain details
        """
        extraction_start_time = time()
        
        # Initialize tracking variables
        reduced_html = None
        html_reduce_op = None
        corpus_to_filter = text
        
        # Phase 0: Optional HTML Reduction
        if reduce_html and isinstance(text, str) and "<" in text and ">" in text:
            try:
                html_reduce_op = HtmlReducer(str(text)).reduce()
                if html_reduce_op.success:
                    reduced_html = html_reduce_op.reduced_data
                    corpus_to_filter = html_reduce_op.reduced_data
                else:
                    corpus_to_filter = text
            except Exception as e:
                corpus_to_filter = text
        
        # Phase 1: Filter Chain
        filter_chain_op: FilterChainOp = self.filter_hero.chain(
            corpus_to_filter,
            filter_stages
        )

        # Check if filter chain failed
        if not filter_chain_op.success:
            parse_op = ParseOp.from_result(
                config=self.config,
                content=None,
                usage=None,
                start_time=time(),
                success=False,
                error="Filter chain failed - parse not attempted",
                generation_result=None
            )
            
            return ExtractOp.from_operations(
                filter_chain_op=filter_chain_op,
                parse_op=parse_op,
                start_time=extraction_start_time,
                content=None,
                reduced_html=reduced_html,
                html_reduce_op=html_reduce_op
            )

        # Phase 2: Parsing
        parse_op = self.parse_hero.run(
            filter_chain_op.content, 
            extraction_spec,
            model_name=model_name
        )
        
        # Create ExtractOp with chain results
        result = ExtractOp.from_operations(
            filter_chain_op=filter_chain_op,
            parse_op=parse_op,
            start_time=extraction_start_time,
            content=parse_op.content if parse_op.success else None,
            reduced_html=reduced_html,
            html_reduce_op=html_reduce_op
        )
        
        return result

    async def extract_async(
        self,
        text: str | dict,
        extraction_spec: WhatToRetain | List[WhatToRetain],
        filter_strategy: str = "contextual",
        reduce_html: bool = True,
        model_name: Optional[str] = None,
    ) -> ExtractOp:
        """
        Async three-phase extraction pipeline.
        
        Parameters
        ----------
        text : str | dict
            The source content to extract data from
        extraction_spec : WhatToRetain | List[WhatToRetain]
            Defines what data to extract and how
        filter_strategy : str
            Strategy for filtering ("contextual", "liberal", "inclusive", etc.)
        reduce_html : bool, default True
            Apply HTML reduction before filtering (only for HTML content)
        model_name : Optional[str]
            Specific model to use for LLM operations
            
        Returns
        -------
        ExtractOp
            Rich result object with content, timing, usage, and error details
        """
        extraction_start_time = time()
        
        # Initialize tracking variables
        reduced_html = None
        html_reduce_op = None
        corpus_to_filter = text
        
        # Phase 0: Optional HTML Reduction
        if reduce_html and isinstance(text, str) and "<" in text and ">" in text:
            try:
                html_reduce_op = HtmlReducer(str(text)).reduce()
                if html_reduce_op.success:
                    reduced_html = html_reduce_op.reduced_data
                    corpus_to_filter = html_reduce_op.reduced_data
                else:
                    corpus_to_filter = text
            except Exception as e:
                corpus_to_filter = text
        
        # Phase 1: Async Filtering
        filter_op: FilterOp = await self.filter_hero.run_async(
            corpus_to_filter,
            extraction_spec,
            filter_strategy=filter_strategy
        )

        if not filter_op.success:
            parse_op = ParseOp.from_result(
                config=self.config,
                content=None,
                usage=None,
                start_time=time(),
                success=False,
                error="Filter phase failed - parse not attempted",
                generation_result=None
            )
            
            return ExtractOp.from_operations(
                filter_op=filter_op,
                parse_op=parse_op,
                start_time=extraction_start_time,
                content=None,
                reduced_html=reduced_html,
                html_reduce_op=html_reduce_op
            )

        # Phase 2: Async Parsing
        parse_op = await self.parse_hero.run_async(
            filter_op.content, 
            extraction_spec,
            model_name=model_name
        )
        
        result = ExtractOp.from_operations(
            filter_op=filter_op,
            parse_op=parse_op,
            start_time=extraction_start_time,
            content=parse_op.content if parse_op.success else None,
            reduced_html=reduced_html,
            html_reduce_op=html_reduce_op
        )
        
        return result

    async def extract_with_chain_async(
        self,
        text: str | dict,
        extraction_spec: WhatToRetain | List[WhatToRetain],
        filter_stages: List[Tuple[List[WhatToRetain], str]],
        reduce_html: bool = True,
        model_name: Optional[str] = None,
    ) -> ExtractOp:
        """
        Async three-phase extraction with filter chaining.
        
        Parameters
        ----------
        text : str | dict
            The source content to extract data from
        extraction_spec : WhatToRetain | List[WhatToRetain]
            Final specifications for parsing
        filter_stages : List[Tuple[List[WhatToRetain], str]]
            List of (extraction_spec, filter_strategy) tuples for chaining
        reduce_html : bool, default True
            Apply HTML reduction before filtering
        model_name : Optional[str]
            Specific model to use
            
        Returns
        -------
        ExtractOp
            Rich result object with filter chain details
        """
        extraction_start_time = time()
        
        # Initialize tracking variables
        reduced_html = None
        html_reduce_op = None
        corpus_to_filter = text
        
        # Phase 0: Optional HTML Reduction
        if reduce_html and isinstance(text, str) and "<" in text and ">" in text:
            try:
                html_reduce_op = HtmlReducer(str(text)).reduce()
                if html_reduce_op.success:
                    reduced_html = html_reduce_op.reduced_data
                    corpus_to_filter = html_reduce_op.reduced_data
                else:
                    corpus_to_filter = text
            except Exception as e:
                corpus_to_filter = text
        
        # Phase 1: Async Filter Chain
        filter_chain_op: FilterChainOp = await self.filter_hero.chain_async(
            corpus_to_filter,
            filter_stages
        )

        if not filter_chain_op.success:
            parse_op = ParseOp.from_result(
                config=self.config,
                content=None,
                usage=None,
                start_time=time(),
                success=False,
                error="Filter chain failed - parse not attempted",
                generation_result=None
            )
            
            return ExtractOp.from_operations(
                filter_chain_op=filter_chain_op,
                parse_op=parse_op,
                start_time=extraction_start_time,
                content=None,
                reduced_html=reduced_html,
                html_reduce_op=html_reduce_op
            )

        # Phase 2: Async Parsing
        parse_op = await self.parse_hero.run_async(
            filter_chain_op.content, 
            extraction_spec,
            model_name=model_name
        )
        
        result = ExtractOp.from_operations(
            filter_chain_op=filter_chain_op,
            parse_op=parse_op,
            start_time=extraction_start_time,
            content=parse_op.content if parse_op.success else None,
            reduced_html=reduced_html,
            html_reduce_op=html_reduce_op
        )
        
        return result


# ─────────────────────────── Demo ───────────────────────────
def main() -> None:
    """Demo showing different extraction methods."""
    extractor = ExtractHero()
    
    # # Define what to extract
    # specs = [
    #     WhatToRetain(
    #         name="title",
    #         desc="Product title",
    #         example="Wireless Keyboard"
    #     ),
    #     WhatToRetain(
    #         name="price",
    #         desc="Product price with currency symbol",
    #         example="€49.99"
    #     ),
    # ]
    
    # sample_html = """
    # <html><body>
    #   <div class="product">
    #     <h2 class="title">Wireless Keyboard</h2>
    #     <span class="price">€49.99</span>
    #     <p class="description">Premium wireless keyboard with backlight</p>
    #   </div>
    #   <div class="product">
    #     <h2 class="title">USB-C Hub</h2>
    #     <span class="price">€29.50</span>
    #     <p class="description">7-in-1 USB-C hub</p>
    #   </div>
    # </body></html>
    # """
    
    # print("🚀 ExtractHero Demo - Three Phase Extraction")
    # print("=" * 60)
    
    # # Example 1: Simple extraction
    # print("\n📋 Example 1: Simple extraction with HTML reduction")
    # op = extractor.extract(
    #     sample_html, 
    #     items, 
    #     filter_strategy="contextual",
    #     reduce_html=True
    # )
    
    # if op.success:
    #     print(f"✅ Success! Extracted: {op.content}")
    #     print(f"   Total time: {op.elapsed_time:.3f}s")
    #     if op.usage:
    #         print(f"   Total cost: ${op.usage.get('total_cost', 0):.4f}")
    # else:
    #     print(f"❌ Failed: {op.error}")
    
    # # Example 2: Filter chain extraction
    # print("\n📋 Example 2: Extraction with filter chain")
    # filter_stages = [
    #     ([WhatToRetain(name="products", desc="all product information")], "liberal"),
    #     ([WhatToRetain(name="main_product", desc="main product only")], "contextual"),
    # ]
    
    # op = extractor.extract_with_chain(
    #     sample_html,
    #     items,  # Final parsing spec
    #     filter_stages=filter_stages,
    #     reduce_html=True
    # )
    
    # if op.success:
    #     print(f"✅ Success! Extracted: {op.content}")
    #     print(f"   Filter stages: {len(op.filter_chain_op.stages_config)}")
    #     print(f"   Total time: {op.elapsed_time:.3f}s")
    #     if op.usage:
    #         print(f"   Total cost: ${op.usage.get('total_cost', 0):.4f}")
    # else:
    #     print(f"❌ Failed: {op.error}")



    specs = [
        # WhatToRetain(
        #     name="voltage",
        #     desc="all information regarding voltage attribute",
           
        # ),
        WhatToRetain(
            name="reverse_voltage_value",
            desc="reverse voltage value in units of V",
        
        ),
    ]
    
    # Example 3: Load real HTML file
    print("\n📋 Example 3: Real HTML file extraction")
    try:

        html_doc = load_html("extracthero/real_life_samples/1/nexperia-aa4afebbd10348ec91358f07facf06f1.html")
        extract_op = extractor.extract(html_doc, specs, reduce_html=True)
        
        if extract_op.success:
            print(f"✅ Success! Extracted: {extract_op.content}")
            print(f"   Filtered corpus length: {len(extract_op.filter_content)} chars")
            if extract_op.usage:
                print(f"   Total cost: ${extract_op.usage.get('total_cost', 0):.4f}")
        else:
            print(f"❌ Failed: {extract_op.error}")
    except Exception as e:
        print(f"Could not load HTML file: {e}")


if __name__ == "__main__":
    main()