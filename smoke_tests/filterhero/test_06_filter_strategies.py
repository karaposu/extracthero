#!/usr/bin/env python
"""
Test 02: FilterHero Filter Strategies
Tests all filter strategies (liberal, contextual, inclusive, recall, base) in both modes.

Run: python smoke_tests/filterhero/test_02_filter_strategies.py

Critical because: Different strategies produce vastly different results. We need to ensure
each strategy behaves correctly and filters content according to its intended behavior.
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

# Sample content for testing
SAMPLE_HTML = """<html>
<head><title>Product Page</title></head>
<body>
    <nav>Home | Products | About | Contact</nav>
    <div class="ads">Special Offer! Buy Now!</div>
    
    <div class="product">
        <h1>Wireless Keyboard</h1>
        <p class="price">Price: $49.99</p>
        <p class="description">High-quality wireless keyboard with mechanical switches.</p>
        <div class="specs">
            <h3>Specifications</h3>
            <ul>
                <li>Connection: Bluetooth 5.0</li>
                <li>Battery: 6 months</li>
                <li>Switch Type: Mechanical Blue</li>
            </ul>
        </div>
    </div>
    
    <footer>© 2024 TechStore. Privacy | Terms</footer>
</body>
</html>"""

# Test 1: Relaxed Strategy (Both Modes)
def test_relaxed_strategy():
    """Test relaxed strategy - should keep more content when in doubt"""
    print_test_header("1. Relaxed Strategy")
    
    filter_hero = FilterHero()
    specs = [WhatToRetain(
        name="product_info",
        desc="product name, price, and specifications"
    )]
    
    passed = True
    
    try:
        # Extractive mode
        result_ext = filter_hero.run(
            text=SAMPLE_HTML,
            extraction_spec=specs,
            filter_strategy="relaxed",
            filter_mode="extractive"
        )
        
        passed &= print_result(
            result_ext.success,
            f"Extractive mode succeeded"
        )
        
        if result_ext.success and result_ext.content:
            has_price = "$49.99" in result_ext.content or "49.99" in result_ext.content
            has_name = "Wireless Keyboard" in result_ext.content or "wireless keyboard" in result_ext.content.lower()
            passed &= print_result(
                has_price and has_name,
                f"Extractive: Found price and name (liberal keeps more)"
            )
            print(f"  Content length: {len(result_ext.content)} chars")
        
        # Subtractive mode
        result_sub = filter_hero.run(
            text=SAMPLE_HTML,
            extraction_spec=specs,
            filter_strategy="relaxed",
            filter_mode="subtractive"
        )
        
        passed &= print_result(
            result_sub.success,
            f"Subtractive mode succeeded"
        )
        
        if result_sub.success:
            passed &= print_result(
                result_sub.lines_removed is not None and result_sub.lines_removed > 0,
                f"Subtractive: Removed {result_sub.lines_removed} lines (liberal removes less)"
            )
            
            # Liberal should preserve more content
            if result_sub.original_line_count and result_sub.retained_line_count:
                retention_rate = result_sub.retained_line_count / result_sub.original_line_count
                passed &= print_result(
                    retention_rate > 0.5,
                    f"Liberal retention rate: {retention_rate:.1%} (should be high)"
                )
        
    except Exception as e:
        print_result(False, f"Exception: {e}")
        passed = False
    
    return passed

# Test 2: Contextual Strategy (Both Modes)
def test_contextual_strategy():
    """Test contextual strategy - preserves semantic context"""
    print_test_header("2. Contextual Strategy")
    
    filter_hero = FilterHero()
    specs = [WhatToRetain(
        name="specifications",
        desc="technical specifications of the product"
    )]
    
    passed = True
    
    try:
        # Extractive mode
        result_ext = filter_hero.run(
            text=SAMPLE_HTML,
            extraction_spec=specs,
            filter_strategy="contextual",
            filter_mode="extractive"
        )
        
        passed &= print_result(
            result_ext.success,
            "Extractive mode succeeded"
        )
        
        if result_ext.success and result_ext.content:
            has_specs = "Bluetooth" in result_ext.content or "Battery" in result_ext.content
            passed &= print_result(
                has_specs,
                "Extractive: Found specifications with context"
            )
            print(f"  Content length: {len(result_ext.content)} chars")
        
        # Subtractive mode
        result_sub = filter_hero.run(
            text=SAMPLE_HTML,
            extraction_spec=specs,
            filter_strategy="contextual",
            filter_mode="subtractive"
        )
        
        passed &= print_result(
            result_sub.success,
            "Subtractive mode succeeded"
        )
        
        if result_sub.success and result_sub.content:
            # Check that context is preserved (e.g., full specs section)
            has_spec_header = "Specifications" in result_sub.content
            has_spec_items = "Bluetooth" in result_sub.content
            passed &= print_result(
                has_spec_header and has_spec_items,
                "Subtractive: Preserved complete specification context"
            )
        
    except Exception as e:
        print_result(False, f"Exception: {e}")
        passed = False
    
    return passed

# Test 3: Focused Strategy
def test_focused_strategy():
    """Test focused strategy - includes anything potentially related"""
    print_test_header("3. Focused Strategy")
    
    filter_hero = FilterHero()
    specs = [WhatToRetain(
        name="price_info",
        desc="any information about price or cost"
    )]
    
    passed = True
    
    try:
        result = filter_hero.run(
            text=SAMPLE_HTML,
            extraction_spec=specs,
            filter_strategy="focused",
            filter_mode="extractive"
        )
        
        passed &= print_result(
            result.success,
            "Inclusive strategy executed"
        )
        
        if result.success and result.content:
            has_price = "$49.99" in result.content
            # Inclusive might also include "Special Offer" as price-related
            has_offer = "offer" in result.content.lower() or "buy" in result.content.lower()
            passed &= print_result(
                has_price,
                f"Found direct price information"
            )
            print(f"  Also included related content: {has_offer}")
        
    except Exception as e:
        print_result(False, f"Exception: {e}")
        passed = False
    
    return passed

# Test 4: Preserve Strategy
def test_preserve_strategy():
    """Test preserve strategy - prioritizes not missing anything"""
    print_test_header("4. Preserve Strategy")
    
    filter_hero = FilterHero()
    specs = [WhatToRetain(
        name="product",
        desc="product information"
    )]
    
    passed = True
    
    try:
        result = filter_hero.run(
            text=SAMPLE_HTML,
            extraction_spec=specs,
            filter_strategy="preserve",
            filter_mode="subtractive"
        )
        
        passed &= print_result(
            result.success,
            "Recall strategy executed"
        )
        
        if result.success:
            # Recall should have very high retention
            if result.original_line_count and result.retained_line_count:
                retention_rate = result.retained_line_count / result.original_line_count
                passed &= print_result(
                    retention_rate > 0.6,
                    f"Recall retention rate: {retention_rate:.1%} (should be very high)"
                )
            
            # Should definitely keep all product content
            if result.content:
                has_all_product = (
                    "Wireless Keyboard" in result.content and
                    "$49.99" in result.content and
                    "Bluetooth" in result.content
                )
                passed &= print_result(
                    has_all_product,
                    "Recall kept all product-related content"
                )
        
    except Exception as e:
        print_result(False, f"Exception: {e}")
        passed = False
    
    return passed

# Test 5: Strict Strategy and Strategy Comparison
def test_strict_and_compare_strategies():
    """Test strict strategy and compare all strategies"""
    print_test_header("5. Strict Strategy & Comparison")
    
    filter_hero = FilterHero()
    specs = [WhatToRetain(
        name="product",
        desc="product name and price"
    )]
    
    passed = True
    strategies_retention = {}
    
    try:
        # Test each strategy in subtractive mode to compare retention
        for strategy in ["strict", "relaxed", "contextual", "focused", "preserve"]:
            result = filter_hero.run(
                text=SAMPLE_HTML,
                extraction_spec=specs,
                filter_strategy=strategy,
                filter_mode="subtractive"
            )
            
            if result.success and result.original_line_count and result.retained_line_count:
                retention = result.retained_line_count / result.original_line_count
                strategies_retention[strategy] = retention
                print(f"  {strategy:12s}: {retention:.1%} retention, {result.lines_removed} lines removed")
        
        # Verify expected retention order (generally)
        # recall >= liberal >= inclusive >= contextual >= base
        if len(strategies_retention) == 5:
            passed &= print_result(
                strategies_retention.get("preserve", 0) >= strategies_retention.get("relaxed", 0) * 0.9,
                "Recall has highest or near-highest retention"
            )
            passed &= print_result(
                strategies_retention.get("strict", 1) <= strategies_retention.get("relaxed", 0) * 1.1,
                "Base has lower or similar retention to liberal"
            )
        
        # Test that all strategies produce valid output
        passed &= print_result(
            len(strategies_retention) == 5,
            f"All {len(strategies_retention)} strategies produced results"
        )
        
    except Exception as e:
        print_result(False, f"Exception: {e}")
        passed = False
    
    return passed

def main():
    print("\n" + "="*80)
    print("FILTERHERO SMOKE TEST 02: FILTER STRATEGIES")
    print("="*80)
    print("\nTesting all filter strategies with real content...")
    
    results = []
    
    # Run all tests
    results.append(("Relaxed Strategy", test_relaxed_strategy()))
    results.append(("Contextual Strategy", test_contextual_strategy()))
    results.append(("Focused Strategy", test_focused_strategy()))
    results.append(("Preserve Strategy", test_preserve_strategy()))
    results.append(("Base & Comparison", test_strict_and_compare_strategies()))
    
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
        print("\n🎉 ALL STRATEGY TESTS PASSED!")
    else:
        print(f"\n⚠️  {total_count - passed_count} test(s) failed")
    
    return passed_count == total_count

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)