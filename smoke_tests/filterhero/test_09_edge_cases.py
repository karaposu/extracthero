#!/usr/bin/env python
"""
Test 05: FilterHero Edge Cases and Error Handling
Tests edge cases, error conditions, and boundary scenarios.

Run: python smoke_tests/filterhero/test_05_edge_cases.py

Critical because: Production systems encounter unexpected inputs. FilterHero must
handle edge cases gracefully without crashes or data corruption.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from extracthero import FilterHero, WhatToRetain
import time

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

# Test 1: Empty and Minimal Content
def test_empty_content():
    """Test handling of empty or minimal content"""
    print_test_header("1. Empty and Minimal Content")
    
    filter_hero = FilterHero()
    specs = [WhatToRetain(name="anything", desc="any content")]
    
    passed = True
    
    try:
        # Test empty string
        result_empty = filter_hero.run(
            text="",
            extraction_spec=specs,
            filter_strategy="relaxed",
            filter_mode="extractive"
        )
        
        passed &= print_result(
            result_empty.success or result_empty.content == "",
            "Empty string handled without crash"
        )
        
        # Test single character
        result_char = filter_hero.run(
            text="x",
            extraction_spec=specs,
            filter_strategy="relaxed",
            filter_mode="subtractive"
        )
        
        passed &= print_result(
            result_char.success,
            "Single character handled"
        )
        
        # Test only whitespace
        result_space = filter_hero.run(
            text="   \n\n  \t  ",
            extraction_spec=specs,
            filter_strategy="contextual",
            filter_mode="extractive"
        )
        
        passed &= print_result(
            result_space.success or result_space.content == "",
            "Whitespace-only content handled"
        )
        
        # Test single line
        result_line = filter_hero.run(
            text="Single line of content",
            extraction_spec=specs,
            filter_strategy="relaxed",
            filter_mode="subtractive"
        )
        
        if result_line.success:
            passed &= print_result(
                result_line.original_line_count == 1,
                f"Single line counted correctly: {result_line.original_line_count} line"
            )
        
    except Exception as e:
        print_result(False, f"Exception with edge content: {e}")
        passed = False
    
    return passed

# Test 2: Very Large Content
def test_large_content():
    """Test handling of very large documents"""
    print_test_header("2. Very Large Content")
    
    # Create a large document (1000+ lines)
    large_lines = []
    for i in range(1000):
        if i == 500:
            large_lines.append("IMPORTANT: Target content we need to find")
        else:
            large_lines.append(f"Filler line number {i} with some random content")
    
    large_content = "\n".join(large_lines)
    
    filter_hero = FilterHero()
    specs = [WhatToRetain(name="target", desc="important target content")]
    
    passed = True
    
    try:
        # Test subtractive mode with large content
        start = time.time()
        result = filter_hero.run(
            text=large_content,
            extraction_spec=specs,
            filter_strategy="contextual",
            filter_mode="subtractive",
            max_line_length_for_indexing=100  # Truncate for efficiency
        )
        elapsed = time.time() - start
        
        passed &= print_result(
            result.success,
            f"Processed {len(large_lines)} lines in {elapsed:.2f}s"
        )
        
        if result.success:
            passed &= print_result(
                "IMPORTANT" in result.content or "Target" in result.content,
                "Found target in large document"
            )
            
            if result.lines_removed:
                removal_rate = result.lines_removed / len(large_lines)
                passed &= print_result(
                    removal_rate > 0.9,
                    f"Efficiently removed {removal_rate:.1%} of large document"
                )
        
    except Exception as e:
        print_result(False, f"Exception with large content: {e}")
        passed = False
    
    return passed

# Test 3: Malformed and Invalid Inputs
def test_malformed_inputs():
    """Test handling of malformed or invalid inputs"""
    print_test_header("3. Malformed and Invalid Inputs")
    
    filter_hero = FilterHero()
    specs = [WhatToRetain(name="content", desc="any valid content")]
    
    passed = True
    
    try:
        # Malformed HTML
        malformed_html = "<div><p>Unclosed tags<div><span>Mixed up</p>"
        result_html = filter_hero.run(
            text=malformed_html,
            extraction_spec=specs,
            filter_strategy="relaxed",
            filter_mode="extractive"
        )
        
        passed &= print_result(
            result_html.success or result_html.error,
            "Malformed HTML processed without crash"
        )
        
        # Invalid JSON string (not dict)
        invalid_json = '{"broken": "json", "missing": }'
        result_json = filter_hero.run(
            text=invalid_json,  # Will be treated as string
            extraction_spec=specs,
            filter_strategy="relaxed",
            filter_mode="subtractive"
        )
        
        passed &= print_result(
            result_json.success or result_json.error,
            "Invalid JSON string handled"
        )
        
        # Binary-like content
        binary_like = "\x00\x01\x02\x03\x04\x05"
        result_binary = filter_hero.run(
            text=binary_like,
            extraction_spec=specs,
            filter_strategy="contextual",
            filter_mode="extractive"
        )
        
        passed &= print_result(
            result_binary.success or result_binary.error,
            "Binary-like content handled"
        )
        
    except Exception as e:
        print_result(False, f"Exception with malformed input: {e}")
        passed = False
    
    return passed

# Test 4: Multiple WhatToRetain Specs
def test_multiple_specs():
    """Test handling of multiple extraction specifications"""
    print_test_header("4. Multiple WhatToRetain Specifications")
    
    content = """
    Product A: Laptop - $1000 - In stock
    Product B: Mouse - $20 - Out of stock
    Product C: Keyboard - $80 - In stock
    Contact: support@example.com
    """
    
    filter_hero = FilterHero()
    
    # Multiple specs
    multi_specs = [
        WhatToRetain(name="prices", desc="all price information"),
        WhatToRetain(name="availability", desc="stock status"),
        WhatToRetain(name="products", desc="product names")
    ]
    
    passed = True
    
    try:
        result = filter_hero.run(
            text=content,
            extraction_spec=multi_specs,
            filter_strategy="relaxed",
            filter_mode="extractive"
        )
        
        passed &= print_result(
            result.success,
            f"Processed {len(multi_specs)} specifications"
        )
        
        if result.success and result.content:
            # Should get prices, stock, and names
            has_prices = "$1000" in result.content or "$20" in result.content
            has_stock = "stock" in result.content.lower()
            has_products = "Laptop" in result.content or "Mouse" in result.content
            
            passed &= print_result(
                has_prices and has_stock and has_products,
                "Multiple specs all extracted relevant content"
            )
        
        # Test with empty spec list (edge case)
        empty_specs = []
        result_empty = filter_hero.run(
            text=content,
            extraction_spec=empty_specs,
            filter_strategy="relaxed",
            filter_mode="extractive"
        )
        
        # Should handle gracefully even with no specs
        passed &= print_result(
            result_empty.success or result_empty.error,
            "Empty spec list handled gracefully"
        )
        
    except Exception as e:
        print_result(False, f"Exception with multiple specs: {e}")
        passed = False
    
    return passed

# Test 5: Async Operations and Special Cases
def test_special_cases():
    """Test special cases and boundary conditions"""
    print_test_header("5. Special Cases and Boundaries")
    
    filter_hero = FilterHero()
    
    passed = True
    
    try:
        # Test with very long single line (no newlines)
        long_line = "Product " * 1000  # Very long single line
        specs = [WhatToRetain(name="product", desc="product information")]
        
        result_long = filter_hero.run(
            text=long_line,
            extraction_spec=specs,
            filter_strategy="relaxed",
            filter_mode="subtractive",
            max_line_length_for_indexing=200  # Should truncate
        )
        
        passed &= print_result(
            result_long.success,
            "Very long single line processed"
        )
        
        if result_long.success:
            passed &= print_result(
                result_long.original_line_count == 1,
                "Long content still counted as 1 line"
            )
        
        # Test with many empty lines
        many_empty = "\n" * 100 + "Content" + "\n" * 100
        result_empty = filter_hero.run(
            text=many_empty,
            extraction_spec=specs,
            filter_strategy="contextual",
            filter_mode="subtractive"
        )
        
        if result_empty.success:
            passed &= print_result(
                result_empty.original_line_count == 201,
                f"Empty lines counted: {result_empty.original_line_count} total lines"
            )
        
        # Test with None as text (should handle gracefully)
        try:
            result_none = filter_hero.run(
                text=None,
                extraction_spec=specs,
                filter_strategy="relaxed",
                filter_mode="extractive"
            )
            # Should fail gracefully
            passed &= print_result(
                not result_none.success or result_none.error,
                "None input handled with error"
            )
        except TypeError:
            # Expected - None is not valid
            passed &= print_result(True, "None input raised appropriate error")
        
        # Test conflicting text_rules in WhatToRetain
        conflict_spec = WhatToRetain(
            name="impossible",
            desc="content that contains both A and B",
            text_rules=["must contain 'alpha'", "must not contain 'a'"]  # Impossible
        )
        
        result_conflict = filter_hero.run(
            text="alpha beta gamma",
            extraction_spec=[conflict_spec],
            filter_strategy="relaxed",
            filter_mode="extractive"
        )
        
        # Should still process without crash
        passed &= print_result(
            result_conflict.success or result_conflict.error is not None,
            "Conflicting rules handled gracefully"
        )
        
    except Exception as e:
        print_result(False, f"Exception in special cases: {e}")
        passed = False
    
    return passed

def main():
    print("\n" + "="*80)
    print("FILTERHERO SMOKE TEST 05: EDGE CASES")
    print("="*80)
    print("\nTesting edge cases and error handling...")
    
    results = []
    
    # Run all tests
    results.append(("Empty Content", test_empty_content()))
    results.append(("Large Content", test_large_content()))
    results.append(("Malformed Inputs", test_malformed_inputs()))
    results.append(("Multiple Specs", test_multiple_specs()))
    results.append(("Special Cases", test_special_cases()))
    
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
        print("\n🎉 ALL EDGE CASE TESTS PASSED!")
    else:
        print(f"\n⚠️  {total_count - passed_count} test(s) failed")
    
    return passed_count == total_count

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)