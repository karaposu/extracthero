#!/usr/bin/env python
"""
Test 03: FilterHero Subtractive Filtering
Tests subtractive filtering mode specifically without specifying filter strategy.

Run: python smoke_tests/filterhero/test_03_subtractive_filtering.py

Critical because: Subtractive filtering is the new solution to LLM output limitations
and must work reliably with default settings.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from extracthero import FilterHero, WhatToRetain

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

# Test 1: Basic Subtractive Filtering
def test_basic_subtractive():
    """Test basic subtractive filtering with line deletions"""
    print_test_header("1. Basic Subtractive Filtering")
    
    content = """Line 1: Advertisement - Buy now!
Line 2: Navigation menu
Line 3: Product Name: Laptop Pro
Line 4: Price: $999
Line 5: Specifications: 16GB RAM, 512GB SSD
Line 6: Footer information
Line 7: Copyright notice"""
    
    filter_hero = FilterHero()
    specs = [WhatToRetain(name="product", desc="product information including name, price, and specs")]
    
    passed = True
    
    try:
        result = filter_hero.run(
            text=content,
            extraction_spec=specs,
            filter_mode="subtractive"
            # No filter_strategy - using default
        )
        
        passed &= print_result(
            result.success,
            "Subtractive filtering executed"
        )
        
        if result.success:
            # Check metadata
            passed &= print_result(
                result.lines_removed is not None,
                f"Lines removed: {result.lines_removed}"
            )
            passed &= print_result(
                result.original_line_count == 7,
                f"Original line count: {result.original_line_count}"
            )
            passed &= print_result(
                result.filtered_line_count is not None,
                f"Filtered line count: {result.filtered_line_count}"
            )
            
            # Check content
            if result.content:
                has_product = "Laptop Pro" in result.content
                has_price = "$999" in result.content or "999" in result.content
                has_specs = "16GB" in result.content or "512GB" in result.content
                no_footer = "Footer" not in result.content and "Copyright" not in result.content
                
                passed &= print_result(
                    has_product and has_price,
                    "Kept product information"
                )
                passed &= print_result(
                    no_footer,
                    "Removed irrelevant footer content"
                )
            
            # Check deletion details
            if result.deletions_applied:
                print(f"\n  Deletion details:")
                for deletion in result.deletions_applied:
                    print(f"    Lines {deletion['start_line']}-{deletion['end_line']}: {deletion.get('reason', 'N/A')}")
            
    except Exception as e:
        print_result(False, f"Exception: {e}")
        passed = False
    
    return passed

# Test 2: Line Numbering and Truncation
def test_line_processing():
    """Test line numbering formats and truncation in subtractive mode"""
    print_test_header("2. Line Numbering and Truncation")
    
    # Content with varied line lengths
    content = """Short line
This is a very long line that contains lots of information about the product including detailed specifications and features that might need to be truncated
Product details here
Another short line"""
    
    filter_hero = FilterHero()
    specs = [WhatToRetain(name="product", desc="product details")]
    
    passed = True
    
    try:
        # Test with default line format and truncation
        result1 = filter_hero.run(
            text=content,
            extraction_spec=specs,
            filter_mode="subtractive",
            max_line_length_for_indexing=50  # Truncate long lines
        )
        
        passed &= print_result(
            result1.success,
            "Subtractive with truncation succeeded"
        )
        
        # Test with custom line format
        result2 = filter_hero.run(
            text=content,
            extraction_spec=specs,
            filter_mode="subtractive",
            line_format="Line {n}: "
        )
        
        passed &= print_result(
            result2.success,
            "Subtractive with custom line format succeeded"
        )
        
        # Test without truncation
        result3 = filter_hero.run(
            text=content,
            extraction_spec=specs,
            filter_mode="subtractive",
            max_line_length_for_indexing=None  # No truncation
        )
        
        passed &= print_result(
            result3.success,
            "Subtractive without truncation succeeded"
        )
        
        # All should produce similar filtering results
        if result1.success and result2.success and result3.success:
            # Line formatting shouldn't affect final output
            if result1.content and result2.content:
                passed &= print_result(
                    result1.filtered_line_count == result2.filtered_line_count,
                    "Line format doesn't affect filtering outcome"
                )
        
    except Exception as e:
        print_result(False, f"Exception: {e}")
        passed = False
    
    return passed

# Test 3: Large Document Efficiency
def test_large_document():
    """Test subtractive filtering efficiency with large documents"""
    print_test_header("3. Large Document Efficiency")
    
    # Create a large document
    large_lines = []
    for i in range(500):
        if i == 250:
            large_lines.append("IMPORTANT: Product specification - Model X500")
        elif i == 251:
            large_lines.append("Price: $2999")
        elif i == 252:
            large_lines.append("Features: Advanced AI, 5G connectivity")
        else:
            large_lines.append(f"Filler content line {i} with random information")
    
    large_content = "\n".join(large_lines)
    
    filter_hero = FilterHero()
    specs = [WhatToRetain(name="product", desc="product model, price, and features")]
    
    passed = True
    
    try:
        result = filter_hero.run(
            text=large_content,
            extraction_spec=specs,
            filter_mode="subtractive",
            max_line_length_for_indexing=100  # Truncate for efficiency
        )
        
        passed &= print_result(
            result.success,
            f"Processed {len(large_lines)} lines"
        )
        
        if result.success:
            # Should remove most lines
            removal_rate = result.lines_removed / len(large_lines) if result.lines_removed else 0
            passed &= print_result(
                removal_rate > 0.9,
                f"Efficiently removed {removal_rate:.1%} of content"
            )
            
            # Should keep the important lines
            if result.content:
                has_product = "Model X500" in result.content
                has_price = "$2999" in result.content or "2999" in result.content
                
                passed &= print_result(
                    has_product and has_price,
                    "Found and kept relevant content in large document"
                )
            
            # Check performance metrics
            if result.usage:
                print(f"\n  Token usage:")
                print(f"    Input tokens: {result.usage.get('input_tokens', 'N/A')}")
                print(f"    Output tokens: {result.usage.get('output_tokens', 'N/A')}")
                print(f"    Total cost: ${result.usage.get('total_cost', 0):.4f}")
        
    except Exception as e:
        print_result(False, f"Exception: {e}")
        passed = False
    
    return passed

# Test 4: Multiple Deletion Ranges
def test_multiple_deletions():
    """Test handling multiple deletion ranges"""
    print_test_header("4. Multiple Deletion Ranges")
    
    content = """Header: Welcome to our site
Navigation: Home | Products | About
Ad: Special offer!

Product Section Start
Name: Premium Widget
Price: $149.99
Description: High-quality widget with advanced features

Customer Reviews:
- Great product! 5 stars
- Excellent value
- Fast shipping

Related Products:
- Widget Pro
- Widget Lite

Footer: Contact us
Copyright 2024"""
    
    filter_hero = FilterHero()
    specs = [WhatToRetain(
        name="product_core",
        desc="only the core product information - name, price, and description"
    )]
    
    passed = True
    
    try:
        result = filter_hero.run(
            text=content,
            extraction_spec=specs,
            filter_mode="subtractive"
        )
        
        passed &= print_result(
            result.success,
            "Multiple deletion ranges processed"
        )
        
        if result.success:
            if result.deletions_applied:
                num_ranges = len(result.deletions_applied)
                passed &= print_result(
                    num_ranges >= 2,
                    f"Applied {num_ranges} deletion ranges"
                )
                
                # Should have deleted header, reviews, related, footer
                print("\n  Deletions applied:")
                for deletion in result.deletions_applied:
                    print(f"    Lines {deletion['start_line']}-{deletion['end_line']}: {deletion.get('reason', 'N/A')}")
            
            if result.content:
                has_product = "Premium Widget" in result.content
                has_price = "$149" in result.content
                no_reviews = "5 stars" not in result.content
                no_footer = "Copyright" not in result.content
                
                passed &= print_result(
                    has_product and has_price,
                    "Kept core product information"
                )
                passed &= print_result(
                    no_footer,
                    "Removed footer content"
                )
                # Reviews might be kept or removed depending on LLM interpretation
                if no_reviews:
                    print("  ✓ Also removed customer reviews")
        
    except Exception as e:
        print_result(False, f"Exception: {e}")
        passed = False
    
    return passed

# Test 5: Edge Cases in Subtractive Mode
def test_subtractive_edge_cases():
    """Test edge cases specific to subtractive filtering"""
    print_test_header("5. Subtractive Mode Edge Cases")
    
    filter_hero = FilterHero()
    passed = True
    
    try:
        # Test 1: Empty content
        specs = [WhatToRetain(name="anything", desc="any content")]
        result_empty = filter_hero.run(
            text="",
            extraction_spec=specs,
            filter_mode="subtractive"
        )
        
        passed &= print_result(
            result_empty.success or result_empty.content == "",
            "Empty content handled"
        )
        
        # Test 2: Single line
        result_single = filter_hero.run(
            text="Single line with product info",
            extraction_spec=specs,
            filter_mode="subtractive"
        )
        
        passed &= print_result(
            result_single.success,
            "Single line handled"
        )
        
        if result_single.success:
            passed &= print_result(
                result_single.original_line_count == 1,
                "Single line counted correctly"
            )
        
        # Test 3: All lines relevant (nothing to delete)
        all_relevant = """Product: Widget
Price: $99
Features: Durable, Efficient
Warranty: 2 years"""
        
        result_all = filter_hero.run(
            text=all_relevant,
            extraction_spec=[WhatToRetain(name="product", desc="all product information")],
            filter_mode="subtractive"
        )
        
        if result_all.success:
            passed &= print_result(
                result_all.lines_removed == 0 or result_all.lines_removed <= 1,
                f"Minimal deletions when all content relevant ({result_all.lines_removed} lines removed)"
            )
        
        # Test 4: All lines irrelevant (delete everything)
        all_irrelevant = """Advertisement
Cookie notice
Navigation menu
Footer content"""
        
        result_none = filter_hero.run(
            text=all_irrelevant,
            extraction_spec=[WhatToRetain(name="product", desc="product specifications")],
            filter_mode="subtractive"
        )
        
        if result_none.success:
            passed &= print_result(
                result_none.lines_removed >= 3,
                f"Deleted most/all irrelevant content ({result_none.lines_removed} lines removed)"
            )
        
        # Test 5: Content with special characters
        special_content = """Price: €50.00
Features: λ = 450nm
Math: x² + y²"""
        
        result_special = filter_hero.run(
            text=special_content,
            extraction_spec=[WhatToRetain(name="specs", desc="technical specifications")],
            filter_mode="subtractive"
        )
        
        passed &= print_result(
            result_special.success,
            "Special characters handled in subtractive mode"
        )
        
    except Exception as e:
        print_result(False, f"Exception: {e}")
        passed = False
    
    return passed

def main():
    print("\n" + "="*80)
    print("FILTERHERO SMOKE TEST 03: SUBTRACTIVE FILTERING")
    print("="*80)
    print("\nTesting subtractive filtering mode with default settings...")
    
    results = []
    
    # Run all tests
    results.append(("Basic Subtractive", test_basic_subtractive()))
    results.append(("Line Processing", test_line_processing()))
    results.append(("Large Document", test_large_document()))
    results.append(("Multiple Deletions", test_multiple_deletions()))
    results.append(("Edge Cases", test_subtractive_edge_cases()))
    
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
        print("\n🎉 ALL SUBTRACTIVE FILTERING TESTS PASSED!")
    else:
        print(f"\n⚠️  {total_count - passed_count} test(s) failed")
    
    return passed_count == total_count

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)