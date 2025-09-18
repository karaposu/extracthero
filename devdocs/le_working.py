#!/usr/bin/env python3
"""
LangExtract Working Example - Correct API Usage
Based on devdocs/external_assets/le.md

python le_working.py
"""

import langextract as lx
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def example_api_extraction():
    """
    Extract API endpoints from documentation using LangExtract
    """
    print("="*60)
    print("API ENDPOINT EXTRACTION WITH LANGEXTRACT")
    print("="*60)
    
    # Define the extraction task
    prompt = """Extract API endpoints with their HTTP methods, paths, and descriptions.
    Use exact text for extractions. Extract each endpoint as a separate entity."""
    
    # Provide examples using the correct API format
    examples = [
        lx.data.ExampleData(
            text="GET /users - Returns a list of all users in the system",
            extractions=[
                lx.data.Extraction(
                    extraction_class="endpoint",
                    extraction_text="GET /users",
                    attributes={
                        "method": "GET",
                        "path": "/users",
                        "description": "Returns a list of all users in the system"
                    }
                )
            ]
        )
    ]
    
    # Test document
    input_text = """
    API Documentation
    
    GET /products
    Description: Retrieve all products
    Response: JSON array of products
    
    POST /products
    Description: Create a new product
    Request Body: {"name": "string", "price": "number"}
    
    DELETE /products/{id}
    Description: Delete a product by ID
    Parameters: id (required) - Product ID
    """
    
    # Extract using OpenAI
    result = lx.extract(
        text_or_documents=input_text,
        prompt_description=prompt,
        examples=examples,
        model_id="gpt-4o-mini"  # Using OpenAI
    )
    
    # Display results
    print(f"\nExtracted {len(result.extractions)} endpoints:\n")
    for i, extraction in enumerate(result.extractions, 1):
        print(f"{i}. Class: {extraction.extraction_class}")
        print(f"   Text: '{extraction.extraction_text}'")
        if extraction.attributes:
            for key, value in extraction.attributes.items():
                print(f"   - {key}: {value}")
        print()
    
    return result

def example_filter_comparison():
    """
    Compare extraction vs filtering approach
    """
    print("="*60)
    print("LANGEXTRACT vs FILTERHERO COMPARISON")
    print("="*60)
    
    sample_doc = """
    # Product Page
    
    Navigation: Home > Products > Electronics
    
    ## Sony WH-1000XM5 Headphones
    Price: $399.99
    Features: Active noise canceling, 30-hour battery
    
    ## Related Products
    - Bose QuietComfort
    - Apple AirPods Max
    
    Footer: © 2024 Store Inc.
    """
    
    # LangExtract approach: Extract structured data
    prompt = "Extract product information including name, price, and features"
    
    examples = [
        lx.data.ExampleData(
            text="iPhone 15 Pro - Price: $999, Features: A17 chip, titanium design",
            extractions=[
                lx.data.Extraction(
                    extraction_class="product",
                    extraction_text="iPhone 15 Pro",
                    attributes={
                        "name": "iPhone 15 Pro",
                        "price": "$999",
                        "features": "A17 chip, titanium design"
                    }
                )
            ]
        )
    ]
    
    result = lx.extract(
        text_or_documents=sample_doc,
        prompt_description=prompt,
        examples=examples,
        model_id="gpt-4o-mini"
    )
    
    print("\n📊 LangExtract Output (Structured Data):")
    print("-" * 40)
    for extraction in result.extractions:
        if extraction.extraction_class == "product":
            attrs = extraction.attributes
            print(f"Product: {attrs.get('name', 'N/A')}")
            print(f"Price: {attrs.get('price', 'N/A')}")
            print(f"Features: {attrs.get('features', 'N/A')}")
    
    print("\n📄 FilterHero Output (Would be filtered text):")
    print("-" * 40)
    print("## Sony WH-1000XM5 Headphones")
    print("Price: $399.99")
    print("Features: Active noise canceling, 30-hour battery")
    
    print("\n💡 Key Difference:")
    print("- LangExtract: Returns structured JSON data")
    print("- FilterHero: Returns filtered document text")

def example_multi_class_extraction():
    """
    Extract multiple types of entities
    """
    print("\n" + "="*60)
    print("MULTI-CLASS EXTRACTION")
    print("="*60)
    
    # Define multiple extraction classes
    prompt = """Extract different types of information:
    - error_codes: HTTP error codes with their meanings
    - auth_info: Authentication methods and requirements
    - rate_limits: API rate limiting information"""
    
    examples = [
        lx.data.ExampleData(
            text="401 Unauthorized - Invalid API key. Rate limit: 100 requests per minute",
            extractions=[
                lx.data.Extraction(
                    extraction_class="error_code",
                    extraction_text="401 Unauthorized",
                    attributes={"code": "401", "meaning": "Invalid API key"}
                ),
                lx.data.Extraction(
                    extraction_class="rate_limit",
                    extraction_text="100 requests per minute",
                    attributes={"limit": "100", "period": "minute"}
                )
            ]
        )
    ]
    
    test_doc = """
    API Documentation
    
    Authentication: Use Bearer token in Authorization header
    
    Error Codes:
    - 400 Bad Request
    - 403 Forbidden
    - 429 Too Many Requests
    
    Rate Limits:
    - Free tier: 60 requests per hour
    - Pro tier: 1000 requests per hour
    """
    
    result = lx.extract(
        text_or_documents=test_doc,
        prompt_description=prompt,
        examples=examples,
        model_id="gpt-4o-mini"
    )
    
    # Group by extraction class
    by_class = {}
    for extraction in result.extractions:
        cls = extraction.extraction_class
        if cls not in by_class:
            by_class[cls] = []
        by_class[cls].append(extraction)
    
    for cls, items in by_class.items():
        print(f"\n{cls.upper()} ({len(items)} found):")
        for item in items:
            print(f"  • {item.extraction_text}")
            if item.attributes:
                for k, v in item.attributes.items():
                    print(f"    - {k}: {v}")

def main():
    print("\n" + "="*60)
    print("LANGEXTRACT WORKING EXAMPLES (CORRECT API)")
    print("="*60)
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not found in environment!")
        print("Please add it to your .env file")
        return 1
    
    print("✅ OPENAI_API_KEY found")
    print("✅ Using correct LangExtract API with ExampleData objects\n")
    
    try:
        # Run examples
        example_api_extraction()
        example_filter_comparison()
        example_multi_class_extraction()
        
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        print("\n✅ LangExtract successfully extracts structured data")
        print("✅ Returns data with source grounding (extraction_text)")
        print("✅ Supports multiple extraction classes")
        print("✅ Works with OpenAI models (gpt-4o-mini, gpt-4o, etc.)")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())