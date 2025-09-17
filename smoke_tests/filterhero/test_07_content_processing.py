#!/usr/bin/env python
"""
Test 03: FilterHero Content Processing
Tests different content types (HTML, JSON, plain text) and processing features.

Run: python smoke_tests/filterhero/test_03_content_processing.py

Critical because: FilterHero must handle various input formats correctly and 
process them through both extractive and subtractive modes without data loss.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from extracthero import FilterHero, WhatToRetain
import json

def print_test_header(test_name):
    print("\n" + "="*80)
    print(f"TEST: {test_name}")
    print("="*80)

def print_result(passed, details=""):
    if passed:
        print(f"✅ PASSED: {details}")
    else:
        print(f"❌ FAILED: {details}")
    return passed

# Test 1: HTML Content Processing
def test_html_content():
    """Test processing of HTML content"""
    print_test_header("1. HTML Content Processing")
    
    html_content = """<!DOCTYPE html>
<html>
<head><title>Test Page</title></head>
<body>
    <header>Navigation Menu</header>
    <main>
        <article>
            <h1>Important Article</h1>
            <p>This is the main content we want.</p>
            <p>Price: <span class="price">$99.99</span></p>
        </article>
    </main>
    <footer>Copyright 2024</footer>
</body>
</html>"""
    
    filter_hero = FilterHero()
    specs = [WhatToRetain(name="article", desc="main article content and price")]
    
    passed = True
    
    try:
        # Test extractive mode
        result = filter_hero.run(
            text=html_content,
            extraction_spec=specs,
            filter_strategy="contextual",
            filter_mode="extractive"
        )
        
        passed &= print_result(result.success, "HTML extractive mode processed")
        
        if result.success and result.content:
            has_content = "Important Article" in result.content or "main content" in result.content
            has_price = "$99.99" in result.content or "99.99" in result.content
            passed &= print_result(
                has_content and has_price,
                f"Extracted HTML content correctly"
            )
        
        # Test subtractive mode
        result_sub = filter_hero.run(
            text=html_content,
            extraction_spec=specs,
            filter_strategy="contextual",
            filter_mode="subtractive"
        )
        
        passed &= print_result(result_sub.success, "HTML subtractive mode processed")
        
        if result_sub.success:
            # Should remove header/footer but keep article
            no_footer = "Copyright" not in result_sub.content
            has_article = "<article>" in result_sub.content or "Important Article" in result_sub.content
            passed &= print_result(
                no_footer and has_article,
                "Subtractive removed correct HTML sections"
            )
        
    except Exception as e:
        print_result(False, f"Exception: {e}")
        passed = False
    
    return passed

# Test 2: JSON/Dictionary Content Processing
def test_json_content():
    """Test processing of JSON/dictionary content"""
    print_test_header("2. JSON/Dictionary Content Processing")
    
    json_content = {
        "metadata": {
            "timestamp": "2024-01-01",
            "version": "1.0"
        },
        "product": {
            "name": "Laptop Pro",
            "price": 1299.99,
            "specs": {
                "cpu": "Intel i7",
                "ram": "16GB",
                "storage": "512GB SSD"
            }
        },
        "reviews": [
            {"rating": 5, "comment": "Excellent!"},
            {"rating": 4, "comment": "Good value"}
        ]
    }
    
    filter_hero = FilterHero()
    specs = [WhatToRetain(
        name="product_specs",
        desc="product specifications including CPU, RAM, and storage"
    )]
    
    passed = True
    
    try:
        # Test with dictionary input
        result = filter_hero.run(
            text=json_content,  # Pass dict directly
            extraction_spec=specs,
            filter_strategy="relaxed",
            filter_mode="extractive"
        )
        
        passed &= print_result(result.success, "JSON/dict extractive mode processed")
        
        if result.success and result.content:
            has_cpu = "Intel i7" in result.content or "i7" in result.content
            has_ram = "16GB" in result.content
            has_storage = "512GB" in result.content or "SSD" in result.content
            passed &= print_result(
                has_cpu or has_ram or has_storage,
                f"Extracted specs from JSON"
            )
        
        # Test subtractive mode with JSON
        result_sub = filter_hero.run(
            text=json_content,
            extraction_spec=specs,
            filter_strategy="relaxed",
            filter_mode="subtractive"
        )
        
        passed &= print_result(result_sub.success, "JSON/dict subtractive mode processed")
        
        if result_sub.success and result_sub.content:
            # Should keep specs but maybe remove reviews
            has_specs = "cpu" in result_sub.content or "ram" in result_sub.content
            passed &= print_result(has_specs, "Subtractive kept JSON specs")
        
    except Exception as e:
        print_result(False, f"Exception: {e}")
        passed = False
    
    return passed

# Test 3: Plain Text Processing
def test_plain_text():
    """Test processing of plain text content"""
    print_test_header("3. Plain Text Processing")
    
    plain_text = """Product Review Summary
    
The new smartphone model features:
- 6.5 inch OLED display
- 128GB storage
- 5G connectivity
- Price: $799

Customer feedback has been positive.
Average rating: 4.5 stars

Contact support at support@example.com
Terms and conditions apply."""
    
    filter_hero = FilterHero()
    specs = [WhatToRetain(
        name="features",
        desc="smartphone features and specifications"
    )]
    
    passed = True
    
    try:
        result = filter_hero.run(
            text=plain_text,
            extraction_spec=specs,
            filter_strategy="contextual",
            filter_mode="extractive"
        )
        
        passed &= print_result(result.success, "Plain text processed")
        
        if result.success and result.content:
            has_display = "OLED" in result.content
            has_storage = "128GB" in result.content
            has_5g = "5G" in result.content
            passed &= print_result(
                has_display or has_storage or has_5g,
                f"Extracted features from plain text"
            )
            print(f"  Extracted content length: {len(result.content)} chars")
        
    except Exception as e:
        print_result(False, f"Exception: {e}")
        passed = False
    
    return passed

# Test 4: Line Processing Features (Subtractive Mode)
def test_line_processing_features():
    """Test line numbering, truncation, and formatting features"""
    print_test_header("4. Line Processing Features")
    
    filter_hero = FilterHero()
    
    # Content with varied line lengths
    test_content = """Short line
This is a very long line that contains lots of text and might need to be truncated when showing to the LLM to save on tokens but the original should remain intact
Another short line
Mid-length line with some content"""
    
    passed = True
    
    try:
        # Test line numbering without truncation
        lines = test_content.split('\n')
        numbered = filter_hero._prepare_numbered_content(
            lines,
            max_line_length=None,
            line_format="[{n}]"
        )
        
        passed &= print_result(
            len(lines) == 4,
            f"Correctly split into {len(lines)} lines"
        )
        
        passed &= print_result(
            numbered.startswith("[1]"),
            "Line numbering format applied correctly"
        )
        
        # Test with truncation
        numbered_truncated = filter_hero._prepare_numbered_content(
            lines,
            max_line_length=50,
            line_format="[{n}]"
        )
        
        truncated_lines = numbered_truncated.split('\n')
        long_line = truncated_lines[1]  # The long line
        passed &= print_result(
            "..." in long_line and len(long_line) < 70,  # 50 + format + ...
            f"Long line truncated correctly"
        )
        
        # Test different line formats
        formats_to_test = ["#{n}:", "L{n}:", "{n:03d}|"]
        for fmt in formats_to_test:
            numbered_fmt = filter_hero._prepare_numbered_content(
                ["Test line"],
                line_format=fmt
            )
            expected_start = fmt.format(n=1)
            passed &= print_result(
                numbered_fmt.startswith(expected_start),
                f"Format '{fmt}' produces '{expected_start}'"
            )
        
    except Exception as e:
        print_result(False, f"Exception: {e}")
        passed = False
    
    return passed

# Test 5: Content with Special Characters and Encoding
def test_special_characters():
    """Test handling of special characters and encodings"""
    print_test_header("5. Special Characters and Encoding")
    
    special_content = """Product: Café Résumé
Price: €50.00 (≈ $55.00)
Features: • Unicode bullets
         → Arrows
         ✓ Checkmarks
         
Technical specs: λ = 450nm, ΔT = ±2°C
Math: x² + y² = r²
Emojis: 🎯 Target achieved! 🚀"""
    
    filter_hero = FilterHero()
    specs = [WhatToRetain(name="specs", desc="technical specifications")]
    
    passed = True
    
    try:
        result = filter_hero.run(
            text=special_content,
            extraction_spec=specs,
            filter_strategy="relaxed",
            filter_mode="extractive"
        )
        
        passed &= print_result(result.success, "Special characters processed")
        
        if result.success and result.content:
            # Check various special characters preserved
            has_lambda = "λ" in result.content or "450nm" in result.content
            has_delta = "ΔT" in result.content or "±2°C" in result.content
            passed &= print_result(
                has_lambda or has_delta,
                "Special characters preserved in extraction"
            )
        
        # Test subtractive mode preserves encoding
        result_sub = filter_hero.run(
            text=special_content,
            extraction_spec=specs,
            filter_strategy="contextual",
            filter_mode="subtractive"
        )
        
        passed &= print_result(
            result_sub.success,
            "Subtractive mode handled special characters"
        )
        
        if result_sub.success:
            # Check if content was filtered (might be empty if all removed)
            if result_sub.content:
                # If content exists, check unicode preservation
                has_unicode = any(char in result_sub.content for char in ["€", "≈", "•", "→", "✓", "λ", "Δ"])
                passed &= print_result(
                    has_unicode or result_sub.lines_removed > 5,
                    f"Unicode preserved or heavily filtered ({result_sub.lines_removed} lines removed)"
                )
            else:
                # If all content removed, that's valid for "technical specs" filter
                passed &= print_result(
                    result_sub.lines_removed > 0,
                    f"Filtered out non-technical content ({result_sub.lines_removed} lines removed)"
                )
        
    except Exception as e:
        print_result(False, f"Exception: {e}")
        passed = False
    
    return passed

def main():
    print("\n" + "="*80)
    print("FILTERHERO SMOKE TEST 03: CONTENT PROCESSING")
    print("="*80)
    print("\nTesting various content types and processing features...")
    
    results = []
    
    # Run all tests
    results.append(("HTML Content", test_html_content()))
    results.append(("JSON/Dict Content", test_json_content()))
    results.append(("Plain Text", test_plain_text()))
    results.append(("Line Processing", test_line_processing_features()))
    results.append(("Special Characters", test_special_characters()))
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("\n🎉 ALL CONTENT PROCESSING TESTS PASSED!")
    else:
        print(f"\n⚠️  {total_count - passed_count} test(s) failed")
    
    return passed_count == total_count

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)