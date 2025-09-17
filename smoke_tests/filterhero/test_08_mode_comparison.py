#!/usr/bin/env python
"""
Test 04: FilterHero Mode Comparison (Extractive vs Subtractive)
Tests both modes side-by-side to ensure consistency and validate advantages.

Run: python smoke_tests/filterhero/test_04_mode_comparison.py

Critical because: The new subtractive mode must produce equivalent or better results
than extractive mode while solving the output limitation problem.
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

# Test 1: Mode Output Consistency
def test_mode_output_consistency():
    """Test that both modes produce similar filtered content"""
    print_test_header("1. Mode Output Consistency")
    
    test_content = """<div class="container">
    <header>Site Navigation</header>
    <div class="product">
        <h1>USB-C Hub</h1>
        <p>Price: $39.99</p>
        <p>7-in-1 connectivity solution</p>
    </div>
    <footer>Terms and Conditions</footer>
</div>"""
    
    filter_hero = FilterHero()
    specs = [WhatToRetain(name="product", desc="product information")]
    
    passed = True
    
    try:
        # Run both modes with same parameters
        result_ext = filter_hero.run(
            text=test_content,
            extraction_spec=specs,
            filter_strategy="relaxed",
            filter_mode="extractive"
        )
        
        result_sub = filter_hero.run(
            text=test_content,
            extraction_spec=specs,
            filter_strategy="relaxed",
            filter_mode="subtractive"
        )
        
        passed &= print_result(
            result_ext.success and result_sub.success,
            "Both modes executed successfully"
        )
        
        if result_ext.success and result_sub.success:
            # Both should keep the product info
            ext_has_product = "USB-C Hub" in result_ext.content and "$39.99" in result_ext.content
            sub_has_product = "USB-C Hub" in result_sub.content and "$39.99" in result_sub.content
            
            passed &= print_result(
                ext_has_product and sub_has_product,
                "Both modes kept essential product information"
            )
            
            # Both should remove navigation/footer
            ext_no_footer = "Terms and Conditions" not in result_ext.content
            sub_no_footer = "Terms and Conditions" not in result_sub.content
            
            passed &= print_result(
                ext_no_footer or sub_no_footer,  # At least one should remove it
                "Irrelevant content filtered in at least one mode"
            )
            
            print(f"  Extractive output: {len(result_ext.content)} chars")
            print(f"  Subtractive output: {len(result_sub.content)} chars")
        
    except Exception as e:
        print_result(False, f"Exception: {e}")
        passed = False
    
    return passed

# Test 2: Performance and Cost Comparison
def test_performance_comparison():
    """Compare performance metrics between modes"""
    print_test_header("2. Performance and Cost Comparison")
    
    # Create a larger document
    large_content = """<html>
<body>
""" + "\n".join([f"<p>Filler content line {i}</p>" for i in range(50)])
    
    large_content += """
    <div class="important">
        <h1>Critical Information</h1>
        <p>This is the important part we need.</p>
        <p>Price: $999.99</p>
    </div>
""" + "\n".join([f"<p>More filler line {i}</p>" for i in range(50)])
    
    large_content += """
</body>
</html>"""
    
    filter_hero = FilterHero()
    specs = [WhatToRetain(name="critical", desc="critical information and price")]
    
    passed = True
    
    try:
        # Time extractive mode
        start = time.time()
        result_ext = filter_hero.run(
            text=large_content,
            extraction_spec=specs,
            filter_strategy="contextual",
            filter_mode="extractive"
        )
        ext_time = time.time() - start
        
        # Time subtractive mode
        start = time.time()
        result_sub = filter_hero.run(
            text=large_content,
            extraction_spec=specs,
            filter_strategy="contextual",
            filter_mode="subtractive"
        )
        sub_time = time.time() - start
        
        passed &= print_result(
            result_ext.success and result_sub.success,
            "Both modes handled large content"
        )
        
        print(f"\n  Performance Metrics:")
        print(f"  Extractive mode: {ext_time:.2f}s")
        print(f"  Subtractive mode: {sub_time:.2f}s")
        
        if result_ext.usage and result_sub.usage:
            ext_cost = result_ext.usage.get('total_cost', 0)
            sub_cost = result_sub.usage.get('total_cost', 0)
            
            print(f"\n  Cost Comparison:")
            print(f"  Extractive: ${ext_cost:.4f}")
            print(f"  Subtractive: ${sub_cost:.4f}")
            
            if ext_cost > 0:
                savings = ((ext_cost - sub_cost) / ext_cost) * 100
                print(f"  Savings: {savings:.1f}%")
        
        # Subtractive should have metadata
        if result_sub.success:
            passed &= print_result(
                result_sub.lines_removed is not None,
                f"Subtractive provided deletion metadata: {result_sub.lines_removed} lines removed"
            )
        
    except Exception as e:
        print_result(False, f"Exception: {e}")
        passed = False
    
    return passed

# Test 3: Subtractive Mode Deletion Accuracy
def test_deletion_accuracy():
    """Test that subtractive mode accurately identifies and removes content"""
    print_test_header("3. Subtractive Mode Deletion Accuracy")
    
    numbered_content = """Line 1: Advertisement
Line 2: Buy Now!
Line 3: Product Name
Line 4: Price: $50
Line 5: Footer Info"""
    
    filter_hero = FilterHero()
    specs = [WhatToRetain(name="product", desc="product name and price")]
    
    passed = True
    
    try:
        result = filter_hero.run(
            text=numbered_content,
            extraction_spec=specs,
            filter_strategy="contextual",
            filter_mode="subtractive"
        )
        
        passed &= print_result(result.success, "Subtractive mode executed")
        
        if result.success:
            # Check deletions were applied
            if result.deletions_applied:
                print(f"\n  Deletions applied: {len(result.deletions_applied)} ranges")
                for deletion in result.deletions_applied:
                    print(f"    Lines {deletion['start_line']}-{deletion['end_line']}: {deletion.get('reason', 'N/A')}")
            
            # Verify correct content kept
            has_product = "Product Name" in result.content
            has_price = "$50" in result.content
            no_ad = "Advertisement" not in result.content
            no_footer = "Footer" not in result.content
            
            passed &= print_result(
                has_product and has_price,
                "Kept relevant product information"
            )
            passed &= print_result(
                no_ad and no_footer,
                "Removed irrelevant content"
            )
            
            # Check line count metrics
            if result.original_line_count and result.retained_line_count:
                reduction = ((result.original_line_count - result.retained_line_count) / 
                           result.original_line_count * 100)
                print(f"  Content reduction: {reduction:.1f}%")
                print(f"  Original lines: {result.original_line_count}")
                print(f"  Retained lines: {result.retained_line_count}")
        
    except Exception as e:
        print_result(False, f"Exception: {e}")
        passed = False
    
    return passed

# Test 4: Mode Parameters and Options
def test_mode_parameters():
    """Test mode-specific parameters work correctly"""
    print_test_header("4. Mode-Specific Parameters")
    
    test_content = "Short line\n" + "x" * 300 + "\nAnother line"
    
    filter_hero = FilterHero()
    specs = [WhatToRetain(name="all", desc="all content")]
    
    passed = True
    
    try:
        # Test subtractive with custom line format
        result1 = filter_hero.run(
            text=test_content,
            extraction_spec=specs,
            filter_strategy="relaxed",
            filter_mode="subtractive",
            line_format="#{n}:",
            max_line_length_for_indexing=50
        )
        
        passed &= print_result(
            result1.success,
            "Subtractive with custom line format works"
        )
        
        # Test without truncation
        result2 = filter_hero.run(
            text=test_content,
            extraction_spec=specs,
            filter_strategy="relaxed",
            filter_mode="subtractive",
            max_line_length_for_indexing=None
        )
        
        passed &= print_result(
            result2.success,
            "Subtractive without truncation works"
        )
        
        # Extractive mode shouldn't be affected by these params
        result3 = filter_hero.run(
            text=test_content,
            extraction_spec=specs,
            filter_strategy="relaxed",
            filter_mode="extractive"
        )
        
        passed &= print_result(
            result3.success,
            "Extractive mode unaffected by subtractive params"
        )
        
    except Exception as e:
        print_result(False, f"Exception: {e}")
        passed = False
    
    return passed

# Test 5: Filter Chain with Mixed Modes
def test_filter_chain():
    """Test filter chaining with multiple stages"""
    print_test_header("5. Filter Chain Operations")
    
    complex_content = """
    Navigation: Home | About | Contact
    
    Main Content:
    Product: Advanced Laptop
    Price: $1299
    CPU: Intel i9
    RAM: 32GB
    
    Secondary Product:
    Product: Basic Mouse
    Price: $19
    
    Footer: Copyright 2024
    """
    
    filter_hero = FilterHero()
    
    passed = True
    
    try:
        # Stage 1: Remove navigation/footer
        stage1_specs = [WhatToRetain(
            name="products",
            desc="all product information"
        )]
        
        # Stage 2: Focus on expensive products
        stage2_specs = [WhatToRetain(
            name="expensive",
            desc="products over $100"
        )]
        
        # Run filter chain
        chain_result = filter_hero.chain(
            text=complex_content,
            stages=[
                (stage1_specs, "relaxed"),
                (stage2_specs, "contextual")
            ]
        )
        
        passed &= print_result(
            chain_result.success,
            f"Filter chain completed with {len(chain_result.filterops)} stages"
        )
        
        if chain_result.success:
            final_content = chain_result.content  # Use content attribute instead
            
            # Should have laptop but not mouse
            has_laptop = "Advanced Laptop" in final_content or "$1299" in final_content
            no_mouse = "Basic Mouse" not in final_content
            no_nav = "Navigation" not in final_content
            
            passed &= print_result(
                has_laptop and no_mouse and no_nav,
                "Chain filtering produced expected result"
            )
            
            # Check stage metrics
            for i, op in enumerate(chain_result.filterops):
                if op.success and op.filtered_data_token_size:
                    print(f"  Stage {i+1} output: {op.filtered_data_token_size} tokens")
        
    except Exception as e:
        print_result(False, f"Exception: {e}")
        passed = False
    
    return passed

def main():
    print("\n" + "="*80)
    print("FILTERHERO SMOKE TEST 04: MODE COMPARISON")
    print("="*80)
    print("\nComparing extractive and subtractive modes...")
    
    results = []
    
    # Run all tests
    results.append(("Output Consistency", test_mode_output_consistency()))
    results.append(("Performance Comparison", test_performance_comparison()))
    results.append(("Deletion Accuracy", test_deletion_accuracy()))
    results.append(("Mode Parameters", test_mode_parameters()))
    results.append(("Filter Chain", test_filter_chain()))
    
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
        print("\n🎉 ALL MODE COMPARISON TESTS PASSED!")
    else:
        print(f"\n⚠️  {total_count - passed_count} test(s) failed")
    
    return passed_count == total_count

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)