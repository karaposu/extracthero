# FilterHero Enhancement: Configurable Subtractive Filtering Approaches

## Overview

FilterHero's subtractive mode currently uses a single approach for identifying content to delete. This document proposes enhancing the subtractive mode to support multiple deletion strategies, allowing users to choose the most appropriate approach for their specific document type and extraction requirements.

## Proposed Enhancement

Add a new parameter `subtractive_approach` to FilterHero's `run()` method that allows selection between different deletion identification strategies.

### Parameter Definition

```python
def run(
    self,
    text: str | Dict[str, Any],
    extraction_spec: WhatToRetain | List[WhatToRetain],
    filter_strategy: str = "contextual",
    filter_mode: str = "extractive",
    subtractive_approach: str = "ssm",  # New parameter
    max_line_length_for_indexing: Optional[int] = 200,
    line_format: str = "[{n}]",
    model_name: Optional[str] = None
) -> FilterOp:
    """
    Parameters
    ----------
    subtractive_approach : str
        Strategy for identifying deletions in subtractive mode:
        - "ssm" (default): Semantic Section Mapping - categorizes document sections semantically
        - "rll": Relevant Line List - directly identifies relevant/irrelevant lines
    """
```

## Approach Definitions

### 1. Semantic Section Mapping (SSM) - Default

**Description**: Analyzes the document structure to create a semantic map of all sections, categorizing each by its purpose (navigation, content, metadata, code, footer, header). Deletions are determined based on semantic categories.

**How it works**:
1. Document is analyzed to identify semantic sections
2. Each section is categorized and marked as relevant/irrelevant
3. Entire sections marked as irrelevant are deleted
4. Preserves semantic coherence within sections

**Advantages**:
- Better understanding of document structure
- Preserves context within semantic blocks
- More consistent results across runs
- Easier to debug and understand decisions

**Best for**:
- Well-structured documents (API docs, technical documentation)
- Documents with clear semantic sections
- When preserving context within blocks is important
- Large documents where understanding structure helps filtering

**LLM Output Example**:
```json
{
  "sections": [
    {
      "name": "Navigation Menu",
      "category": "navigation",
      "start_line": 1,
      "end_line": 65,
      "is_content": false,
      "is_navigation": true
    },
    {
      "name": "API Authentication Guide",
      "category": "content",
      "start_line": 66,
      "end_line": 250,
      "is_content": true,
      "is_navigation": false
    }
  ]
}
```

### 2. Relevant Line List (RLL)

**Description**: Directly analyzes each line or group of lines to determine relevance. Returns specific line ranges to delete without considering broader document structure.

**How it works**:
1. Document lines are evaluated for relevance to extraction spec
2. Continuous ranges of irrelevant lines are identified
3. Returns list of line ranges to delete
4. More granular, line-by-line decisions

**Advantages**:
- More granular control
- Can remove individual irrelevant lines within sections
- Simpler prompt structure
- Lower token usage for deletion instructions

**Best for**:
- Unstructured or semi-structured documents
- Mixed content where relevant/irrelevant content is interleaved
- When maximum content reduction is priority
- Smaller documents where structure is less important

**LLM Output Example**:
```json
{
  "deletions": [
    {
      "start_line": 1,
      "end_line": 15,
      "reason": "navigation_menu"
    },
    {
      "start_line": 78,
      "end_line": 79,
      "reason": "advertisement"
    },
    {
      "start_line": 250,
      "end_line": 300,
      "reason": "footer_content"
    }
  ]
}
```

## Implementation Strategy

### Phase 1: Core Architecture
```python
class FilterHero:
    def _run_subtractive(self, text, extraction_spec, filter_strategy, 
                        max_line_length_for_indexing, line_format, 
                        model_name, subtractive_approach):
        
        if subtractive_approach == "ssm":
            return self._run_subtractive_ssm(
                text, extraction_spec, filter_strategy, 
                max_line_length_for_indexing, line_format, model_name
            )
        elif subtractive_approach == "rll":
            return self._run_subtractive_rll(
                text, extraction_spec, filter_strategy,
                max_line_length_for_indexing, line_format, model_name
            )
        else:
            raise ValueError(f"Unknown subtractive_approach: {subtractive_approach}")
    
    def _run_subtractive_ssm(self, ...):
        """Semantic Section Mapping approach"""
        # 1. Get semantic sections from LLM
        # 2. Filter sections based on relevance
        # 3. Convert to line deletions
        # 4. Apply deletions
        
    def _run_subtractive_rll(self, ...):
        """Relevant Line List approach"""
        # 1. Get line deletions directly from LLM
        # 2. Validate line ranges
        # 3. Apply deletions
```

### Phase 2: Prompt Templates

Create specialized prompts for each approach:

```python
# prompts.py

SUBTRACTIVE_SSM_PROMPT = """
Analyze this numbered document and identify all semantic sections.

For each section, determine:
1. Its semantic category (navigation, content, metadata, code, footer, header)
2. Whether it contains relevant content for: {thing_to_extract}
3. The line range it spans

Document:
{numbered_corpus}

Output a structured list of all document sections...
"""

SUBTRACTIVE_RLL_PROMPT = """
Identify all line ranges that should be DELETED from this document.
We want to keep only content relevant to: {thing_to_extract}

Document:
{numbered_corpus}

Output specific line ranges to delete...
"""
```

### Phase 3: Enhanced Metadata

Update FilterOp to include approach-specific metadata:

```python
@dataclass
class FilterOp:
    # Existing fields...
    
    # New fields for enhanced subtractive mode
    subtractive_approach: Optional[str] = None
    semantic_sections: Optional[List[Dict]] = None  # For SSM
    deletion_decisions: Optional[List[Dict]] = None  # For RLL
    approach_metadata: Optional[Dict] = None
```

## Usage Examples

### Example 1: API Documentation (SSM Recommended)
```python
filter_hero = FilterHero()
specs = [WhatToRetain(
    name="api_endpoints",
    desc="API endpoint definitions, parameters, and examples"
)]

result = filter_hero.run(
    text=api_documentation,
    extraction_spec=specs,
    filter_mode="subtractive",
    subtractive_approach="ssm"  # Use semantic mapping for structured docs
)
```

### Example 2: News Article (RLL Recommended)
```python
filter_hero = FilterHero()
specs = [WhatToRetain(
    name="main_story",
    desc="Main news story content, excluding ads and navigation"
)]

result = filter_hero.run(
    text=news_article,
    extraction_spec=specs,
    filter_mode="subtractive", 
    subtractive_approach="rll"  # Use line-by-line for mixed content
)
```

### Example 3: Automatic Selection
```python
def auto_select_approach(text: str) -> str:
    """Automatically select best subtractive approach based on document characteristics"""
    
    # Check for structured markers
    has_headers = "##" in text or "###" in text
    has_code_blocks = "```" in text
    has_navigation_patterns = bool(re.search(r'\[.*?\]\(.*?\)', text))
    
    # Calculate structure score
    structure_score = sum([has_headers, has_code_blocks, has_navigation_patterns])
    
    # Check document length
    line_count = len(text.split('\n'))
    
    if structure_score >= 2 or line_count > 500:
        return "ssm"  # Structured or large documents
    else:
        return "rll"  # Unstructured or small documents
```

## Performance Considerations

### Token Usage Comparison

| Approach | Input Tokens | Output Tokens | Best Case | Worst Case |
|----------|-------------|---------------|-----------|------------|
| SSM | ~50,000 | ~2,000-3,000 | Structured docs | Random text |
| RLL | ~50,000 | ~500-1,500 | Simple patterns | Complex interleaving |

### Accuracy Characteristics

| Aspect | SSM | RLL |
|--------|-----|-----|
| Context preservation | Excellent | Moderate |
| Granularity | Section-level | Line-level |
| Consistency | High | Moderate |
| Structural understanding | Excellent | Limited |
| Processing speed | Moderate | Fast |

## Migration Path

1. **Phase 1**: Implement dual approach support with SSM as default
2. **Phase 2**: Add approach auto-selection based on document analysis
3. **Phase 3**: Create hybrid approach that combines both strategies
4. **Phase 4**: Add confidence scoring and fallback mechanisms

## Testing Strategy

### Test Cases for Each Approach

1. **SSM Tests**:
   - Well-structured API documentation
   - Technical specifications with clear sections
   - Multi-level nested documentation
   - Documents with mixed semantic categories

2. **RLL Tests**:
   - News articles with inline ads
   - Blog posts with scattered relevant content
   - Forum threads with mixed discussions
   - Small documents with simple patterns

3. **Comparison Tests**:
   - Same document with both approaches
   - Accuracy metrics comparison
   - Token usage comparison
   - Consistency across multiple runs

## Future Enhancements

### 1. Hybrid Approach
Combine SSM and RLL for optimal results:
- Use SSM for initial structure understanding
- Apply RLL for fine-grained filtering within relevant sections

### 2. Confidence-Based Selection
```python
def select_approach_with_confidence(text, extraction_spec):
    ssm_confidence = analyze_structure_confidence(text)
    rll_confidence = analyze_pattern_confidence(text)
    
    if ssm_confidence > rll_confidence + 0.2:
        return "ssm"
    elif rll_confidence > ssm_confidence + 0.2:
        return "rll"
    else:
        return "hybrid"
```

### 3. Learning from Feedback
Track success rates and automatically adjust approach selection based on:
- Document domain
- Extraction spec patterns
- Historical performance data

## Conclusion

By supporting multiple subtractive approaches, FilterHero becomes more flexible and can optimize for different document types and extraction requirements. The SSM approach excels at structured documents while RLL provides better granularity for unstructured content. This enhancement maintains backward compatibility while significantly expanding FilterHero's capabilities.