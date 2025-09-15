# FilterHero Solution: Line-Based Deletion Strategy

## Proposed Solution Overview

Instead of having the LLM output the filtered content (which hits output limits), the LLM identifies and outputs only the **line numbers of irrelevant content** to be removed. The actual deletion is performed deterministically in code using these line numbers.

## How It Works

### Traditional Approach (Current Problem)
```
Input: 50k tokens → LLM → Output: 40k tokens (TRUNCATED at 8k)
```

### Line-Based Approach (Proposed Solution)
```
Input: 50k tokens → LLM → Output: List of line ranges to delete (< 1k tokens)
                             ↓
                     Python removes lines → Final output: 40k tokens (COMPLETE)
```

## Solution Architecture

### Step 1: Convert Content to Numbered Lines
```python
def prepare_numbered_content(text):
    lines = text.split('\n')
    numbered_lines = []
    for i, line in enumerate(lines, 1):
        numbered_lines.append(f"Line {i}: {line}")
    return '\n'.join(numbered_lines), lines
```

Example:
```
Line 1: <html>
Line 2:   <head>
Line 3:     <title>Product Page</title>
Line 4:     <!-- Google Analytics -->
Line 5:     <script>tracking code...</script>
Line 6:   </head>
Line 7:   <body>
Line 8:     <div class="advertisement">
Line 9:       Buy now! Limited offer!
Line 10:    </div>
Line 11:    <div class="product-info">
Line 12:      <h1>Wireless Keyboard</h1>
Line 13:      <p>Price: $49.99</p>
```

### Step 2: LLM Identifies Irrelevant Line Ranges
```json
{
  "deletions": [
    {"start_line": 4, "end_line": 5, "reason": "tracking_code"},
    {"start_line": 8, "end_line": 10, "reason": "advertisement"},
    {"start_line": 45, "end_line": 67, "reason": "navigation_menu"},
    {"start_line": 120, "end_line": 125, "reason": "footer"}
  ]
}
```

### Step 3: Apply Line Deletions
```python
def apply_line_deletions(lines, deletions):
    # Create set of lines to delete for O(1) lookup
    lines_to_delete = set()
    for deletion in deletions:
        for line_num in range(deletion['start_line'], deletion['end_line'] + 1):
            lines_to_delete.add(line_num)
    
    # Keep only non-deleted lines
    filtered_lines = []
    for i, line in enumerate(lines, 1):
        if i not in lines_to_delete:
            filtered_lines.append(line)
    
    return '\n'.join(filtered_lines)
```

## Advantages

### 1. **Universal Format Support**
- Works with ANY text format (HTML, JSON, XML, Markdown, plain text)
- No format-specific parsing needed
- Line numbers are universal

### 2. **Bypasses Output Limitation**
- Output is just line numbers (typically < 1k tokens)
- Can handle documents of ANY size
- No truncation possible

### 3. **Cost Efficient**
- Minimal output tokens (just numbers)
- Example: 50k input → 200 token output (250x reduction)
- Scales with number of deletion ranges, not content size

### 4. **Simple and Unambiguous**
- Line numbers are clear and precise
- No confusion from duplicate text
- Easy for LLM to understand and output

### 5. **Preserves Structure**
- Original formatting intact within kept lines
- No LLM interpretation or reformatting
- Maintains exact content as written

## Implementation Format

### Recommended Output Format
```json
{
  "format": "line_deletion_v1",
  "total_lines": 500,
  "deletions": [
    {
      "start_line": 10,
      "end_line": 25,
      "content_type": "advertisement"
    },
    {
      "start_line": 100,
      "end_line": 100,  // Single line deletion
      "content_type": "tracking_pixel"
    }
  ],
  "summary": {
    "lines_to_delete": 45,
    "lines_to_keep": 455,
    "retention_rate": 0.91
  }
}
```

## Implementation Considerations

### Handling Edge Cases

#### Empty Lines
```python
# Preserve empty lines for structure
lines = text.split('\n')  # Keeps empty strings for blank lines
```

#### Very Long Lines
```python
# For lines exceeding reasonable length, truncate in display
def prepare_display_line(line, max_length=200):
    if len(line) > max_length:
        return f"{line[:max_length]}... [truncated]"
    return line
```

#### Large Line Counts
For documents with thousands of lines, process in chunks:
```python
def process_large_document(text, chunk_size=500):
    lines = text.split('\n')
    all_deletions = []
    
    for i in range(0, len(lines), chunk_size):
        chunk_lines = lines[i:i+chunk_size]
        numbered_chunk = prepare_numbered_chunk(chunk_lines, offset=i)
        
        # Get deletions for this chunk
        chunk_deletions = llm_identify_deletions(numbered_chunk)
        
        # Adjust line numbers for chunk offset
        for deletion in chunk_deletions:
            deletion['start_line'] += i
            deletion['end_line'] += i
            all_deletions.append(deletion)
    
    return all_deletions
```

## Cost Analysis

### Traditional Filtering
```
50k tokens input + 40k tokens output = 90k tokens total
Cost: ~$2.70 (GPT-4)
Result: 8k tokens (truncated, 80% data lost)
```

### Line-Based Deletion
```
50k tokens input + 0.2k tokens output = 50.2k tokens total
Cost: ~$0.51 (GPT-4)
Result: 40k tokens (complete, 100% relevant data preserved)
Savings: 81% cost reduction + complete content preservation
```

## Integration with FilterHero

### Modified Filter Pipeline
```python
class LineBasedFilterHero:
    def filter(self, text, extraction_spec, filter_strategy):
        # Step 1: Prepare numbered content
        numbered_content, original_lines = self.prepare_numbered_content(text)
        
        # Step 2: Get deletion ranges from LLM
        deletion_response = self.llm.identify_irrelevant_lines(
            numbered_content, 
            extraction_spec,
            filter_strategy=filter_strategy
        )
        
        # Step 3: Parse and validate line ranges
        deletions = self.parse_deletion_response(deletion_response)
        validated_deletions = self.validate_line_ranges(deletions, len(original_lines))
        
        # Step 4: Apply deletions
        filtered_text = self.apply_line_deletions(original_lines, validated_deletions)
        
        # Step 5: Return with metadata
        return FilterOp(
            content=filtered_text,
            deletions_applied=validated_deletions,
            lines_removed=sum(d['end_line'] - d['start_line'] + 1 for d in validated_deletions),
            total_lines=len(original_lines),
            retention_rate=len(filtered_text.split('\n')) / len(original_lines)
        )
    
    def validate_line_ranges(self, deletions, total_lines):
        """Ensure line numbers are valid"""
        valid_deletions = []
        for deletion in deletions:
            if (1 <= deletion['start_line'] <= total_lines and
                1 <= deletion['end_line'] <= total_lines and
                deletion['start_line'] <= deletion['end_line']):
                valid_deletions.append(deletion)
        return valid_deletions
```

### Prompt Template for LLM
```python
DELETION_PROMPT = """
You are reviewing the following numbered content to identify irrelevant sections:

{numbered_content}

Identify line ranges that contain {filter_description}.

Output ONLY a JSON with line ranges to DELETE:
{
  "deletions": [
    {"start_line": X, "end_line": Y, "content_type": "type_of_content"}
  ]
}

Keep your output minimal - just the line numbers to remove.
"""
```

## Why Line-Based is Superior

### Compared to Character Indices
- ✅ **Easier for LLM** to count lines vs characters
- ✅ **More robust** - no off-by-one errors from character counting
- ✅ **Human readable** - developers can verify line numbers easily

### Compared to Text Anchors
- ✅ **No ambiguity** - line 45 is always line 45
- ✅ **No duplicates** - each line has unique number
- ✅ **Format agnostic** - works with any text

### Compared to Structural Parsing
- ✅ **Universal** - doesn't require understanding HTML/JSON structure
- ✅ **Simple** - no complex parsing logic needed
- ✅ **Reliable** - works even with malformed content

## Conclusion

The line-based deletion strategy is the **optimal solution** for FilterHero because it:

1. **Completely bypasses** the output token limitation
2. **Reduces costs** by 80%+ while preserving 100% of relevant content
3. **Works universally** with any text format
4. **Maintains simplicity** that both LLMs and developers can work with
5. **Provides precision** without ambiguity

This approach transforms FilterHero from being constrained by LLM limitations to being a highly efficient, cost-effective filtering solution that scales to any document size while maintaining perfect fidelity to the source content.