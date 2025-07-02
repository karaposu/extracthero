# extracthero/filterhero.py
# run with:  python -m extracthero.filterhero
"""
FilterHero — the “filter” phase of ExtractHero.
• Normalises raw input (HTML / JSON / dict / plain-text).
• Optionally reduces HTML to visible text.
• Uses a JSON fast-path when possible; otherwise builds LLM prompts.
"""

from __future__ import annotations

import json as _json
from dataclasses import dataclass
from time import time
from typing import Any, Dict, List, Optional, Tuple, Union

from llmservice import GenerationResult
from extracthero.myllmservice import MyLLMService
from extracthero.schemes import (
    ExtractConfig,
    FilterOp,
    CorpusPayload,   
    WhatToRetain, 
    ProcessResult
)

from domreducer import HtmlReducer
from string2dict import String2Dict
from extracthero.utils import load_html


import warnings
warnings.filterwarnings(
    "ignore",
    category=RuntimeWarning,
    message=".*extracthero.filterhero.*"
)



# ─────────────────────────────────────────────────────────────────────────────
class FilterHero:
    def __init__(
        self,
        config: Optional[ExtractConfig] = None,
        llm: Optional[MyLLMService] = None,
    ):
        self.config = config or ExtractConfig()
        self.llm = llm or MyLLMService()

        self.html_reducer_op=None

    # ──────────────────────── public orchestrator ────────────────────────
    def run(
        self,
        text: str | Dict[str, Any],
        extraction_spec: WhatToRetain | List[WhatToRetain],
        text_type: Optional[str] = None,
        filter_separately: bool = False,
        reduce_html: bool = True,
        enforce_llm_based_filter: bool = False,
    ) -> FilterOp:
        """
        End-to-end filter phase.
        """
        ts = time()
       
        # 1) Pre-process (HTML reduction / JSON parsing / pass-through)
        payload = self._prepare_corpus(text, text_type, reduce_html)
        if payload.error:
            return FilterOp.from_result(
                config=self.config,
                content=None,
                usage=None,
                reduced_html=payload.reduced_html,
                start_time=ts,
                success=False,
             
                error=payload.error,
            )

        # 2) Handle JSON fast-path or stringify payload for LLM
        proc = self.process_corpus_payload(
            payload, extraction_spec, enforce_llm_based_filter, ts
        )
        if proc.fast_op is not None:                     # shortcut hit
            return proc.fast_op

        # 3) Dispatch LLM calls
        gen_results = self._dispatch(proc.corpus, extraction_spec, filter_separately)

        # 4) Success flag
        ok = (
            gen_results[0].success
            if isinstance(extraction_spec, WhatToRetain) or not filter_separately
            else all(r.success for r in gen_results)
        )

        # 5) Aggregate content + usage
        content, usage = self._aggregate(gen_results, extraction_spec, filter_separately)

        # 6) Wrap & return
        return FilterOp.from_result(
            config=self.config,
            content=content,
            usage=usage,
            reduced_html=proc.reduced,
            html_reduce_op=self.html_reducer_op,
            start_time=ts,
            success=ok,

            error=None if ok else "LLM filter failed",
        )

    # ─────────────────────── helper: preprocessing ───────────────────────
    def _prepare_corpus(
        self,
        text: str | Dict[str, Any],
        text_type: Optional[str],
        reduce_html: bool,
    ) -> CorpusPayload:
        """Return CorpusPayload(corpus, corpus_type, reduced_html, error)"""

        # HTML branch
        if text_type == "html":
            if reduce_html:
                op = HtmlReducer(str(text)).reduce()
                
                self.html_reducer_op=op
                return CorpusPayload(
                    corpus=op.reduced_data if op.success else str(text),
                    corpus_type="html",
                    reduced_html=op.reduced_data if op.success else None,
                
                )
            return CorpusPayload(corpus=str(text), corpus_type="html", reduced_html=None)

        # JSON branch
        if text_type == "json":
            parsed = String2Dict().run(str(text))
            if parsed is None:
                return CorpusPayload(
                    corpus=None,
                    corpus_type="json",
                    reduced_html=None,

                    error="Invalid JSON input",
                )
            return CorpusPayload(corpus=parsed, corpus_type="json", reduced_html=None)

        # dict branch
        if text_type == "dict":
            if not isinstance(text, dict):
                return CorpusPayload(
                    corpus=None,
                    corpus_type="json",
                    reduced_html=None,
                    error="dict type mismatch",
                )
            return CorpusPayload(corpus=text, corpus_type="json", reduced_html=None)

        # plain text branch
        return CorpusPayload(corpus=str(text), corpus_type="text", reduced_html=None)

    # ───────────── helper: JSON shortcut or corpus stringification ─────────────
    def process_corpus_payload(
        self,
        payload: CorpusPayload,
        items: WhatToRetain | List[WhatToRetain],
        enforce_llm: bool,
        ts: float,
    ) -> ProcessResult:
        """
        • If JSON and not forced → return FilterOp shortcut.  
        • Else → make sure corpus is a *string* for LLM.
        """
        # JSON / dict
        if payload.corpus_type == "json":
            data: Dict[str, Any] = payload.corpus  # already dict

            if not enforce_llm:
                keys = (
                    [items.name]
                    if isinstance(items, WhatToRetain)
                    else [it.name for it in items]
                )
                subset = {k: data.get(k) for k in keys}
                fast = FilterOp.from_result(
                    config=self.config,
                    content=subset,
                    usage=None,
                    reduced_html=None,
                    start_time=ts,
                    success=True,
                  
                    error=None,
                )
                return ProcessResult(fast, None, None)

            # fallback: stringify dict for LLM
            return ProcessResult(None, self._stringify_json(data), None)

        # HTML / text
        return ProcessResult(None, str(payload.corpus), payload.reduced_html)

    # ───────────── helper: dispatch to LLM ─────────────
    def _dispatch(
        self,
        corpus_str: str,
        items: WhatToRetain | List[WhatToRetain],
        separate: bool,
    ) -> List[GenerationResult]:
        it_list = [items] if isinstance(items, WhatToRetain) else items
        if len(it_list) == 1 or not separate:
            prompt = "\n\n".join(it.compile() for it in it_list)
            return [self.llm.filter_via_llm(corpus_str, prompt)]

        return [
            self.llm.filter_via_llm(corpus_str, it.compile()) for it in it_list
        ]

    # ───────────── helper: aggregate results ─────────────
    def _aggregate(
        self,
        gen_results: List[GenerationResult],
        items: WhatToRetain | List[WhatToRetain],
        separate: bool,
    ) -> Tuple[Any, Optional[Dict[str, int]]]:

        if isinstance(items, WhatToRetain) or not separate:
            first = gen_results[0]
            return first.content, first.usage

        names = [it.name for it in items]
        content_map = {n: r.content for n, r in zip(names, gen_results)}

        usage_tot: Dict[str, int] = {}
        for r in gen_results:
            if r.usage:
                for k, v in r.usage.items():
                    usage_tot[k] = usage_tot.get(k, 0) + v
        return content_map, usage_tot or None

    # ───────────── helper: JSON→string ─────────────
    @staticmethod
    def _stringify_json(data: Dict[str, Any]) -> str:
        return _json.dumps(data, ensure_ascii=False, indent=2)
    



wrt_to_source_filter_desc="""
### Task
Return **every content chunk** that is relevant to the main product
described in the page’s hero section.

### How to decide relevance
1. **Keep** a chunk if its title, brand, or descriptive text
   • matches the hero product **or**
   • is ambiguous / generic enough that it _could_ be the hero product.
2. **Discard** a chunk **only when** there is a **strong, explicit** signal
   that it belongs to a _different_ item (e.g. totally different brand,
   unrelated product type, “customers also bought” label).
3. When in doubt, **keep** the chunk (favor recall).

### Output
Return the retained chunks exactly as HTML snippets.
""".strip()


# ─────────────────────────────── demo ───────────────────────────────
if __name__ == "__main__":
    cfg = ExtractConfig()
    filter_hero = FilterHero(cfg)
    
    specs = [
        WhatToRetain(
            name="products",
            # desc="product  including title and price",
            wrt_to_source_filter_desc=wrt_to_source_filter_desc,
            include_context_chunk=False,
            # text_rules=[
            #     "productlar cok buyuk olmasin "
            # ]
        )
    ]

    # HowToParse

    # html_doc = """
    # <html><body>
    #   <div class="product"><h2 class="title">Wireless Keyboard</h2><span class="price">€49.99</span></div>
    #   <div class="product"><h2 class="title">USB-C Hub</h2><span class="price">€29.50</span></div>
    # </body></html>
    # """

   
    html_doc = load_html("extracthero/simple_html_sample_2.html")

  
    filter_op = filter_hero.run(html_doc, specs, text_type="html")
    # filter_op = filter_hero.run(html_doc, specs, text_type="html", reduce_html=False)

 
    
    print("Reduced_html")
    print(" ")
    print(filter_op.reduced_html)

    print(" ")
    print("reducement_details: ")
    print(filter_op.html_reduce_op.reducement_details)
    print(" ")
    
    print(" ")
    print("token_reducement_percentage: ")
    print(filter_op.html_reduce_op.token_reducement_percentage)
    print(" ")
    
    
    

    print("Filtered corpus: ⬇")
    print(" ")
    print(filter_op.content)

    

    # print(" ")
    # print("Success:", filter_op.success)



# Entity