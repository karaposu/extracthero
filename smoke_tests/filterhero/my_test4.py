
# python -m my_test4

from extracthero.utils import prepare_numbered_content, read_md
from extracthero import FilterHero, WhatToRetain
from extracthero.myllmservice import MyLLMService, TocSection, TocOutput

filter_hero = FilterHero()


print()
sample_md_path = "samples/1.md"

print("sample_md_path:", sample_md_path)
sample_md=read_md(sample_md_path)

print("sample_md len:", len(sample_md))




# what_to_retain=" actionable technical API sections: all information regarding enpoints, data types, all usage examples, authentications,"

# TOC= """
# Analyze this document from line 1 to the last line.
# Create a comprehensive breakdown of ALL sections.

# Corpus:
#   {numbered_corpus}

# What counts as CONTENT for this analysis (determines is_content field):
#   {what_to_retain}

# Create a structured output with sections containing:
# - name: descriptive name for the section
# - category: type of content (navigation, content, metadata, code, footer, or header)
# - start_line and end_line: line numbers for this section
# - is_content: true if this matches what_to_retain criteria
# - is_navigation: true if primarily navigation links

# Rules:
#   1. Every line from 1 to {max_line} must be covered
#   2. No gaps between sections (end_line + 1 = next section's start_line)
#   3. Use exact integers for line numbers
#   4. Navigation links (format: [text](url)) should ALWAYS be category:"navigation"
#   5. Code blocks (``` markers) should ALWAYS be category:"code"  
#   6. A section ends when content type changes (e.g., navigation→content)
#   7. Minimum section size is 3 lines (don't create tiny sections)
#   8. If a line is blank, include it with the section above
#   9. Group consecutive navigation links together as one section
#   10. is_content=true for: code examples, API endpoints, authentication info, technical instructions
#   11. is_content=false for: navigation menus, headers, footers, metadata
# """



what_to_retain=" actionable technical API sections: all information regarding enpoints, data types, all usage examples, authentications,"

TOC= """
Analyze this document from line 1 to the last line.
Create a comprehensive breakdown of ALL of it.


Corpus:
  {numbered_corpus}


 What counts as CONTENT for this analysis (used for is_content section in output):
    {what_to_retain}

OUTPUT MUST BE VALID JSON in this EXACT format:
  {{
    "sections": [
      {{
        "name": "section name",
        "category": "navigation|content|metadata|code|footer|header",
        "start_line": 1,
        "end_line": 10,
        "is_content": true,
        "is_navigation": false,
      }}
    ]
  }}

  Rules:
  1. Every line from 1 to {max_line} must be covered
  2. No gaps between sections
  3. Use exact integers for line numbers
  4. Output ONLY valid JSON, no markdown formatting
  5. Navigation links (format: [text](url)) should ALWAYS be category:"navigation"
  6. Code blocks (``` markers) should ALWAYS be category:"code"  
  7. A section ends when content type changes (e.g., navigation→content)
  8. Minimum section size is 3 lines (don't create tiny sections)
  9. If a line is blank, include it with the section above
  10. Group consecutive navigation links together as one section
  """



 
original_lines = sample_md.split('\n')
numbered_content = prepare_numbered_content( original_lines )
 
user_prompt = TOC.format( 
    numbered_corpus=numbered_content,
    max_line=len(original_lines),
    what_to_retain=what_to_retain
)


my_llmservice= MyLLMService()


print("starting generation....")

gen_result= my_llmservice.get_deletions_via_llm_custom_with_schema(
    user_prompt,
    model="gpt-4.1-mini",
)

print("\n=== RAW RESPONSE ===")
print(gen_result.raw_content)

print("\n=== PARSED CONTENT ===")
if gen_result.success:
    if isinstance(gen_result.content, TocOutput):
        print("✅ Successfully parsed as TocOutput model")
        print(f"  - Total sections: {len(gen_result.content.sections)}")
        
        # Analyze sections
        content_sections = [s for s in gen_result.content.sections if s.is_content]
        nav_sections = [s for s in gen_result.content.sections if s.is_navigation]
        
        print(f"  - Content sections: {len(content_sections)}")
        print(f"  - Navigation sections: {len(nav_sections)}")
        
        # Show all sections
        print(f"\n📋 All {len(gen_result.content.sections)} sections:")
        for i, section in enumerate(gen_result.content.sections, 1):
            print(f"  {i}. {section.name}")
            print(f"     Lines {section.start_line}-{section.end_line}")
            print(f"     Category: {section.category}")
            print(f"     Is content: {section.is_content}")
            print(f"     Is navigation: {section.is_navigation}")
        
        # Validate coverage
        total_lines = len(original_lines)
        covered_lines = set()
        for section in gen_result.content.sections:
            for line in range(section.start_line, section.end_line + 1):
                covered_lines.add(line)
        
        print(f"\n✅ Coverage check:")
        print(f"  - Document lines: {total_lines}")
        print(f"  - Lines covered: {len(covered_lines)}")
        print(f"  - Coverage: {len(covered_lines)/total_lines*100:.1f}%")
        
        # Lines to keep (content sections)
        lines_to_keep = set()
        for section in content_sections:
            for line in range(section.start_line, section.end_line + 1):
                lines_to_keep.add(line)
        
        print(f"\n📊 Filtering result:")
        print(f"  - Lines to keep: {len(lines_to_keep)}")
        print(f"  - Lines to remove: {total_lines - len(lines_to_keep)}")
        print(f"  - Content retained: {len(lines_to_keep)/total_lines*100:.1f}%")
    else:
        print(f"❌ Content is not TocOutput: {type(gen_result.content)}")
else:
    print(f"❌ Generation failed: {gen_result.error_message}")