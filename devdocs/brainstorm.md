# Brainstorm: Alternative Filtering Approaches

## Current Approaches Recap

1. **Extractive Filtering** - LLM outputs the filtered content directly
2. **Subtractive Filtering** - LLM outputs deletion instructions
   - With SSM (Semantic Section Mapping) - categorizes sections before deletion

## New Approach Ideas

### 1. Index-Based Filtering (IBF)
**Concept**: Output only line numbers or indices to keep, not deletion instructions.

```python
# Instead of outputting content or deletions, output:
{
  "keep_lines": [3, 4, 5, 10, 11, 12, 15, 20, 21, 22, 23, 24, 25],
  "keep_ranges": [[3, 5], [10, 12], [15, 15], [20, 25]]
}
```

**Advantages**:
- Even smaller output than subtractive (just numbers)
- Can use structured output for guaranteed valid format
- Easy to validate (all numbers must be within document range)

**Challenges**:
- LLMs might struggle with accurate line counting
- No semantic grouping information

### 2. Hierarchical Filtering (HF)
**Concept**: Build a document tree, then specify paths to keep/remove.

```python
{
  "document_tree": {
    "header": {"keep": false},
    "sections": {
      "introduction": {"keep": true},
      "api": {
        "endpoints": {"keep": true},
        "examples": {"keep": true},
        "deprecated": {"keep": false}
      },
      "footer": {"keep": false}
    }
  }
}
```

**Advantages**:
- Preserves document structure
- Can make decisions at different granularity levels
- Natural for hierarchical documents (XML, HTML, Markdown)

### 3. Query-Based Filtering (QBF)
**Concept**: Output a query/selector that identifies content to keep.

```python
{
  "keep_queries": [
    "section:contains('API')",
    "code_block:all",
    "heading:level(2):contains('endpoint')",
    "paragraph:after(heading:contains('authentication'))"
  ]
}
```

**Advantages**:
- Very compact output
- Reusable queries across similar documents
- Can leverage existing selector syntaxes (CSS, XPath)

### 4. Mask-Based Filtering (MBF)
**Concept**: Output a binary mask or run-length encoding.

```python
# Binary mask (1=keep, 0=delete)
"mask": "0011111100111000011111111100"

# Run-length encoding
"rle": [(0, 2), (1, 6), (0, 2), (1, 3), (0, 4), (1, 8), (0, 2)]
# Means: skip 2, keep 6, skip 2, keep 3, etc.
```

**Advantages**:
- Extremely compact for documents with large contiguous sections
- No ambiguity about what to keep
- Easy to apply programmatically

### 5. Anchor-Based Filtering (ABF)
**Concept**: Identify key anchor points and radius of context to keep.

```python
{
  "anchors": [
    {"pattern": "GET /api/", "before_lines": 2, "after_lines": 10},
    {"pattern": "authentication", "before_lines": 5, "after_lines": 15},
    {"pattern": "```python", "before_lines": 1, "after_lines": "until_pattern", "until": "```"}
  ]
}
```

**Advantages**:
- Natural for extracting context around specific topics
- Flexible context windows
- Good for sparse relevant content

### 6. Differential Filtering (DF)
**Concept**: Output edit operations like a diff/patch.

```python
{
  "operations": [
    {"op": "delete", "from": 1, "to": 50},
    {"op": "keep", "from": 51, "to": 100},
    {"op": "delete", "from": 101, "to": 150},
    {"op": "summarize", "from": 151, "to": 200, "summary": "Configuration details"},
    {"op": "keep", "from": 201, "to": 300}
  ]
}
```

**Advantages**:
- Can include transformation operations (not just keep/delete)
- Similar to how developers think about changes
- Can include "summarize" for less important sections

### 7. Priority-Based Filtering (PBF)
**Concept**: Assign priorities to sections, keep top N priority content.

```python
{
  "sections": [
    {"lines": [1, 10], "priority": 0.2, "reason": "header"},
    {"lines": [11, 50], "priority": 0.95, "reason": "core API docs"},
    {"lines": [51, 70], "priority": 0.7, "reason": "examples"},
    {"lines": [71, 100], "priority": 0.1, "reason": "footer"}
  ],
  "keep_threshold": 0.5  # Keep all sections with priority >= 0.5
}
```

**Advantages**:
- Adaptive to size constraints
- Can adjust threshold based on desired output size
- Provides importance scores for dynamic filtering

### 8. Template-Based Filtering (TBF)
**Concept**: Match document against known templates, extract by template slots.

```python
{
  "template": "api_documentation",
  "extract_slots": [
    "endpoint_definitions",
    "authentication",
    "request_examples",
    "response_schemas"
  ],
  "ignore_slots": [
    "navigation",
    "marketing_content",
    "legal_notices"
  ]
}
```

**Advantages**:
- Very efficient for standardized documents
- Can pre-train on document types
- Reusable across similar documents

### 9. Attention-Based Filtering (AttBF)
**Concept**: Use attention weights to identify important content.

```python
{
  "attention_scores": {
    "lines_1_10": 0.15,
    "lines_11_20": 0.85,
    "lines_21_30": 0.92,
    "lines_31_40": 0.23
  },
  "keep_above": 0.5
}
```

**Advantages**:
- Leverages LLM's internal attention mechanisms
- Continuous importance scores
- Can visualize importance heatmap

### 10. Collaborative Filtering (CF)
**Concept**: Multiple passes with different strategies, then merge.

```python
{
  "pass1": {"method": "keyword", "found": [1, 5, 10, 15]},
  "pass2": {"method": "semantic", "found": [3, 5, 11, 16]},
  "pass3": {"method": "structure", "found": [1, 2, 3, 10, 11, 12]},
  "merge_strategy": "union",  # or "intersection", "majority"
  "final_keep": [1, 2, 3, 5, 10, 11, 12, 15, 16]
}
```

**Advantages**:
- Reduces individual method biases
- More robust results
- Can catch edge cases

### 11. Checkpoint-Based Filtering (CBF)
**Concept**: Process document in chunks with checkpoints.

```python
{
  "checkpoints": [
    {"line": 100, "decision": "keep_all_above"},
    {"line": 200, "decision": "delete_all_above"},
    {"line": 300, "decision": "keep_selective", "keywords": ["api", "endpoint"]},
    {"line": 400, "decision": "delete_all_below"}
  ]
}
```

**Advantages**:
- Memory efficient for huge documents
- Can process documents larger than context window
- Progressive decision making

### 12. Regex-Based Filtering (RBF)
**Concept**: Output regex patterns for content to keep/delete.

```python
{
  "keep_patterns": [
    r"^#{1,3}\s+.*API.*$",  # Headers containing API
    r"^```[\s\S]*?```$",     # Code blocks
    r"^\s*GET|POST|PUT|DELETE\s+/.*$"  # HTTP endpoints
  ],
  "delete_patterns": [
    r"^\[.*\]\(.*\)$",  # Markdown links
    r"^Copyright.*$",    # Copyright lines
  ]
}
```

**Advantages**:
- Very compact output
- Deterministic application
- Can be validated/tested separately

### 13. Graph-Based Filtering (GBF)
**Concept**: Build knowledge graph, traverse to keep connected components.

```python
{
  "nodes": [
    {"id": 1, "type": "concept", "name": "authentication"},
    {"id": 2, "type": "endpoint", "name": "GET /api/users"},
    {"id": 3, "type": "example", "name": "auth_example"}
  ],
  "edges": [
    {"from": 1, "to": 2, "relation": "required_for"},
    {"from": 1, "to": 3, "relation": "demonstrated_by"}
  ],
  "keep_strategy": "connected_to_targets",
  "target_nodes": [2]
}
```

**Advantages**:
- Captures relationships between content
- Can follow dependency chains
- Good for complex technical documentation

### 14. Compression-Based Filtering (CompBF)
**Concept**: Use information theory - keep high-entropy (informative) sections.

```python
{
  "sections": [
    {"lines": [1, 10], "entropy": 2.3, "compressed_size": 450},
    {"lines": [11, 20], "entropy": 4.8, "compressed_size": 890},
    {"lines": [21, 30], "entropy": 1.2, "compressed_size": 200}
  ],
  "keep_strategy": "high_entropy",
  "threshold": 3.0
}
```

**Advantages**:
- Objective measure of information content
- Language agnostic
- No semantic understanding needed

### 15. Interactive Filtering (IF)
**Concept**: Multi-turn interaction to refine filtering.

```python
# Turn 1
{
  "initial_filter": {"keep": [1, 100], "uncertain": [101, 200], "delete": [201, 300]},
  "questions": [
    "Should we keep the deprecation warnings?",
    "Include code examples for GET endpoints?"
  ]
}
# Turn 2 (after user response)
{
  "refined_filter": {"keep": [1, 100, 150, 175], "delete": [101, 149, 151, 174, 176, 300]}
}
```

**Advantages**:
- Higher precision through clarification
- Handles ambiguous requirements
- Can learn user preferences

### 16. Sliding Window Filtering (SWF)
**Concept**: Process document in overlapping windows, merge decisions.

```python
{
  "windows": [
    {"start": 1, "end": 100, "keep": [10, 20, 30, 40]},
    {"start": 50, "end": 150, "keep": [60, 70, 120, 130]},
    {"start": 100, "end": 200, "keep": [120, 130, 140, 180]}
  ],
  "merge": "voting",  # Lines kept if appear in majority of overlapping windows
}
```

**Advantages**:
- Better context awareness
- Handles long documents beyond context limit
- Reduces edge effects

### 17. Metadata-Based Filtering (MetaBF)
**Concept**: Use document metadata to guide filtering.

```python
{
  "metadata_rules": [
    {"author": "api-team", "action": "keep_all"},
    {"last_modified": "> 2024-01-01", "action": "keep"},
    {"tag": "deprecated", "action": "delete"},
    {"section_type": "example", "importance": "high", "action": "keep"}
  ]
}
```

**Advantages**:
- Leverages existing document structure
- Fast rule-based filtering
- Combines with content-based approaches

### 18. Embedding-Based Filtering (EBF)
**Concept**: Compare section embeddings to target embedding.

```python
{
  "target_embedding": [0.23, 0.45, 0.67, ...],  # What we want
  "section_similarities": [
    {"lines": [1, 10], "similarity": 0.23},
    {"lines": [11, 20], "similarity": 0.89},
    {"lines": [21, 30], "similarity": 0.91}
  ],
  "keep_threshold": 0.7
}
```

**Advantages**:
- Semantic similarity matching
- Can work with pre-computed embeddings
- Good for finding related content

## Hybrid Approaches

### 19. Cascade Filtering
Combine multiple approaches in sequence:
1. Template-based for structure
2. SSM for categorization  
3. Priority-based for fine-tuning

### 20. Ensemble Filtering
Run multiple approaches in parallel, combine results:
- Extractive for quality check
- Subtractive for efficiency
- Index-based for precision
- Vote on final output

## Evaluation Criteria for New Approaches

1. **Output Size** - How compact is the instruction set?
2. **Accuracy** - How precisely can we specify what to keep?
3. **Robustness** - How well does it handle edge cases?
4. **LLM Compatibility** - Can current LLMs execute this reliably?
5. **Determinism** - Is the application of instructions deterministic?
6. **Interpretability** - Can humans understand the decisions?
7. **Speed** - How fast to generate and apply?
8. **Memory** - RAM requirements for processing?
9. **Reversibility** - Can we reconstruct the original?
10. **Flexibility** - Can it handle different document types?

## Most Promising Candidates

Based on the criteria above, the most promising approaches are:

1. **Index-Based Filtering** - Minimal output, high precision
2. **Hierarchical Filtering** - Natural for structured documents
3. **Priority-Based Filtering** - Adaptive to constraints
4. **Run-Length Encoding** - Extremely efficient for contiguous sections
5. **Checkpoint-Based** - Handles massive documents

## Implementation Roadmap

### Phase 1: Research & Prototype
- Implement Index-Based Filtering
- Test on benchmark documents
- Compare with existing approaches

### Phase 2: Advanced Methods
- Hierarchical Filtering for structured docs
- Priority-Based for dynamic sizing
- Hybrid approaches

### Phase 3: Optimization
- Combine best approaches
- Create adaptive selector
- Build approach recommender

## Key Insights

1. **Output minimization is key** - Smaller outputs = lower costs
2. **Structure awareness helps** - Documents have patterns to exploit
3. **Multiple passes can improve quality** - But increase cost
4. **Deterministic application is crucial** - No ambiguity in implementation
5. **Different documents need different approaches** - No one-size-fits-all