#!/usr/bin/env python
"""
Smoke test to demonstrate how _prepare_numbered_content works.
This test shows the transformation of text into numbered lines for LLM processing.
"""

import sys
import os
import json

# Add parent directory to path to import extracthero
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extracthero import FilterHero

def test_prepare_numbered_content():
    """Test the _prepare_numbered_content method with different input types"""
    
    filter_hero = FilterHero()
    
    print("=" * 80)
    print("SMOKE TEST: _prepare_numbered_content Method")
    print("=" * 80)
    
    # Test 1: Real sample file (gt_for_filter_output.txt)
    print("\n1. TESTING WITH REAL SAMPLE FILE")
    print("-" * 40)
    
    # Load the real sample file
    sample_file_path = "extracthero/real_life_samples/1/gt_for_filter_output.txt"
    with open(sample_file_path, 'r', encoding='utf-8') as f:
        sample_text = f.read()
    
    # Process it through _prepare_numbered_content
    numbered_content, original_lines = filter_hero._prepare_numbered_content(sample_text)
    
    print(f"📄 Original file: {len(sample_text)} characters, {len(original_lines)} lines")
    print(f"\n🔢 First 10 numbered lines:")
    print("-" * 40)
    
    # Show first 10 lines of numbered content
    numbered_lines_list = numbered_content.split('\n')
    for line in numbered_lines_list[:10]:
        print(line)
    
    # Save the full numbered content to file
    output_file = "smoke_tests/output_numbered_content.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(numbered_content)
    print(f"\n💾 Full numbered content saved to: {output_file}")
    
    # Test 2: HTML content
    print("\n\n2. TESTING WITH HTML CONTENT")
    print("-" * 40)
    
    html_content = """<div class="product">
    <h1>Diode Specifications</h1>
    <table>
        <tr>
            <th>Reverse Voltage</th>
            <td>VR ≤ 100 V</td>
        </tr>
        <tr>
            <th>Forward Voltage</th>
            <td>VF = 1000 mV @ IF=50mA</td>
        </tr>
    </table>
</div>"""
    
    numbered_html, html_lines = filter_hero._prepare_numbered_content(html_content)
    
    print(f"📄 HTML input: {len(html_lines)} lines")
    print(f"\n🔢 Numbered HTML:")
    print("-" * 40)
    print(numbered_html)
    
    # Test 3: Dictionary/JSON content
    print("\n\n3. TESTING WITH DICTIONARY INPUT")
    print("-" * 40)
    
    dict_content = {
        "product": "Diode",
        "specifications": {
            "reverse_voltage": "VR ≤ 100 V",
            "forward_voltage": "VF = 1000 mV @ IF=50mA",
            "max_current": "200mA"
        },
        "price": "$0.50"
    }
    
    numbered_dict, dict_lines = filter_hero._prepare_numbered_content(dict_content)
    
    print(f"📄 Dictionary input converts to: {len(dict_lines)} lines of JSON")
    print(f"\n🔢 Numbered JSON:")
    print("-" * 40)
    print(numbered_dict)
    
    # Test 4: Long line truncation
    print("\n\n4. TESTING LONG LINE TRUNCATION")
    print("-" * 40)
    
    long_line_text = "Short line\n" + "x" * 300 + "\nAnother short line"
    
    numbered_long, long_lines = filter_hero._prepare_numbered_content(long_line_text)
    
    print(f"📄 Text with 300-character line")
    print(f"\n🔢 Numbered output (note truncation):")
    print("-" * 40)
    print(numbered_long)
    
    # Save original lines for reference
    original_lines_file = "smoke_tests/output_original_lines.json"
    with open(original_lines_file, 'w', encoding='utf-8') as f:
        json.dump({
            "line_count": len(original_lines),
            "first_10_lines": original_lines[:10],
            "last_10_lines": original_lines[-10:] if len(original_lines) > 10 else original_lines
        }, f, indent=2)
    print(f"\n💾 Original lines info saved to: {original_lines_file}")
    
    # Demonstrate the relationship
    print("\n\n5. UNDERSTANDING THE RELATIONSHIP")
    print("-" * 40)
    print("The method returns TWO things:")
    print("1. numbered_content: For LLM to read and identify what to delete")
    print("2. original_lines: The actual lines array for applying deletions")
    print(f"\nExample: If LLM says 'delete lines 3-5', we remove:")
    print(f"  original_lines[2:5] (0-indexed in Python)")
    print(f"  Which corresponds to lines labeled 'Line 3' through 'Line 5' in numbered_content")
    
    # Show example deletion
    print("\n\n6. EXAMPLE DELETION SIMULATION")
    print("-" * 40)
    print("Simulating: Delete lines 2-4 from the HTML example")
    
    # Simulate deletion
    lines_to_delete = set(range(2, 5))  # Lines 2, 3, 4 (1-indexed becomes 0-indexed)
    filtered_lines = []
    for i, line in enumerate(html_lines, 1):
        if i not in lines_to_delete:
            filtered_lines.append(line)
    
    filtered_text = '\n'.join(filtered_lines)
    
    print("\n🔴 Lines marked for deletion:")
    for i in range(2, 5):
        print(f"  Line {i}: {html_lines[i-1]}")
    
    print("\n✅ Result after deletion:")
    print("-" * 40)
    print(filtered_text)
    
    print("\n" + "=" * 80)
    print("SMOKE TEST COMPLETE")
    print("=" * 80)
    print(f"\n📁 Check smoke_tests/ directory for output files:")
    print(f"  - output_numbered_content.txt: Full numbered version of sample file")
    print(f"  - output_original_lines.json: Info about original lines array")

if __name__ == "__main__":
    test_prepare_numbered_content()