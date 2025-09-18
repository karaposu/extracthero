#!/usr/bin/env python3
"""
Direct Comparison: FilterHero vs LangExtract with SAME INPUT
Shows the fundamental difference in output even with identical input.
"""

from filterhero import FilterHero, WhatToRetain
import langextract as lx
from dotenv import load_dotenv
import time

load_dotenv()

# IDENTICAL INPUT DOCUMENT FOR BOTH TOOLS
SAME_INPUT = """
# Product Catalog

## Navigation
Home > Electronics > Headphones

## Sony WH-1000XM5 Headphones
Price: $399.99
SKU: SNY-WH1000XM5
Features:
- Industry-leading noise cancellation
- 30-hour battery life
- Multipoint connectivity
In Stock: Yes

## Customer Reviews
"Best headphones I've ever owned!" - John D.
"Amazing sound quality" - Sarah M.
Rating: 4.8/5 stars (2,341 reviews)

## Related Products
- Bose QuietComfort Ultra - $429
- Apple AirPods Max - $549
- Sennheiser Momentum 4 - $379

## Footer
Contact us | Privacy Policy | Terms of Service
© 2024 TechStore Inc. All rights reserved.
"""

def run_comparison():
    print("="*70)
    print("SAME INPUT, DIFFERENT OUTPUTS: FilterHero vs LangExtract")
    print("="*70)
    print("\n📄 INPUT DOCUMENT (same for both):")
    print("-"*50)
    print(SAME_INPUT[:200] + "...\n")
    
    # ========== FILTERHERO ==========
    print("="*70)
    print("1️⃣ FILTERHERO - Content Filtering")
    print("="*70)
    
    filter_hero = FilterHero()
    
    # Tell FilterHero what content to KEEP
    what_to_keep = WhatToRetain(
        name="main product information",
        desc="The primary product being sold, not related products or reviews",
        text_rules=[
            "Keep product name, price, and features",
            "Remove navigation, footer, reviews, and related products"
        ]
    )
    
    start = time.time()
    filter_result = filter_hero.run(
        text=SAME_INPUT,
        extraction_spec=what_to_keep,
        filter_strategy="contextual",
        filter_mode="subtractive",  # Using subtractive mode
        model_name="gpt-4o-mini"
    )
    filter_time = time.time() - start
    
    print("\n📤 FilterHero Output (Filtered Document):")
    print("-"*50)
    if filter_result.success:
        print(filter_result.content)
        print(f"\nStats: {filter_result.retained_line_count}/{filter_result.original_line_count} lines kept")
        print(f"Time: {filter_time:.2f}s")
        if filter_result.usage:
            print(f"Cost: ${filter_result.usage.get('total_cost', 0):.5f}")
    else:
        print(f"Error: {filter_result.error}")
    
    # ========== LANGEXTRACT ==========
    print("\n" + "="*70)
    print("2️⃣ LANGEXTRACT - Data Extraction")
    print("="*70)
    
    # Tell LangExtract what data to EXTRACT
    prompt = "Extract product information including name, price, SKU, and features"
    
    examples = [
        lx.data.ExampleData(
            text="Apple iPhone 15 - Price: $999, SKU: APL-IP15, Features: A17 chip, 48MP camera",
            extractions=[
                lx.data.Extraction(
                    extraction_class="product",
                    extraction_text="Apple iPhone 15",
                    attributes={
                        "name": "Apple iPhone 15",
                        "price": "$999",
                        "sku": "APL-IP15",
                        "features": ["A17 chip", "48MP camera"]
                    }
                )
            ]
        )
    ]
    
    start = time.time()
    extract_result = lx.extract(
        text_or_documents=SAME_INPUT,
        prompt_description=prompt,
        examples=examples,
        model_id="gpt-4o-mini"
    )
    extract_time = time.time() - start
    
    print("\n📤 LangExtract Output (Structured Data):")
    print("-"*50)
    for extraction in extract_result.extractions:
        if extraction.extraction_class == "product":
            attrs = extraction.attributes
            print(f"Name: {attrs.get('name')}")
            print(f"Price: {attrs.get('price')}")
            print(f"SKU: {attrs.get('sku')}")
            print(f"Features: {attrs.get('features')}")
    print(f"\nTime: {extract_time:.2f}s")
    
    # ========== COMPARISON ==========
    print("\n" + "="*70)
    print("📊 COMPARISON SUMMARY")
    print("="*70)
    
    print("\n🎯 SAME GOAL: Get product information")
    print("📥 SAME INPUT: Identical document with product catalog")
    print("\n📤 DIFFERENT OUTPUTS:")
    
    print("\nFilterHero Output Type: FILTERED TEXT DOCUMENT")
    print("  → Removes unwanted sections (nav, footer, reviews)")
    print("  → Keeps the original text format")
    print("  → Result: Clean document with just product info")
    
    print("\nLangExtract Output Type: STRUCTURED JSON DATA")
    print("  → Extracts specific data fields")
    print("  → Transforms into structured format")
    print("  → Result: JSON object with product attributes")
    
    print("\n💡 USE CASES:")
    print("\nFilterHero when you need:")
    print("  • Clean documents for reading")
    print("  • Reduced content for further processing")
    print("  • Preserved formatting and context")
    print("  • Input preparation for other tools")
    
    print("\nLangExtract when you need:")
    print("  • Database entries")
    print("  • API responses")
    print("  • Spreadsheet data")
    print("  • Structured analytics")
    
    print("\n🔄 BEST TOGETHER:")
    print("  1. FilterHero: Remove 90% irrelevant content")
    print("  2. LangExtract: Extract structured data from the clean 10%")
    print("  = Efficient and accurate data extraction pipeline")

if __name__ == "__main__":
    run_comparison()