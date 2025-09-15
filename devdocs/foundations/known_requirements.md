# ExtractHero - Known Requirements

## Technical Requirements

### Core Processing Pipeline
- **Multi-phase architecture** with clear separation between reduction, filtering, and parsing stages
- **Synchronous and asynchronous** operation modes for all major operations
- **Token tracking** at every stage with detailed metrics on usage and reduction
- **LLM service abstraction** supporting multiple models (GPT-4, GPT-4-mini, custom models)
- **Stateless operation** - each extraction request must be independent and reproducible

### Input Format Support
- **HTML processing** with intelligent DOM reduction
- **JSON/Dictionary** fast-path extraction when structure is known
- **PDF extraction** including both text and visual content
- **Screenshot analysis** with OCR and visual understanding
- **Plain text** processing with context preservation
- **Jupyter notebook** (.ipynb) file reading with cell outputs

### Performance & Scalability
- **Configurable concurrency** limits for LLM requests (max_concurrent_requests)
- **Character-level trimming** support for large documents (trim_char_length parameter)
- **Token optimization** through progressive reduction
- **Caching mechanisms** for repeated operations (15-minute cache for web fetches)
- **Batch processing** capability for multiple extractions

### Error Handling & Reliability
- **Graceful degradation** when individual phases fail
- **Detailed error messages** with actionable information
- **Partial result preservation** when possible
- **Timeout controls** for long-running operations
- **Retry mechanisms** for transient failures

### Integration Requirements
- **Python 3.7+** compatibility
- **Dependency on external services**: llmservice, domreducer libraries
- **Environment variable** configuration support (.env files)
- **Async/await** compatibility for integration with async frameworks
- **Type hints** and dataclass usage for better IDE support

## Business Requirements

### Cost Management
- **Token usage tracking** with detailed breakdowns by stage
- **Cost calculation** for each extraction operation
- **Configurable model selection** to balance cost vs. quality
- **Efficient filtering** to minimize LLM token consumption
- **Usage reporting** for billing and optimization

### Quality Assurance
- **Validation mechanisms** including regex patterns and semantic checks
- **Success/failure tracking** for each extraction phase
- **Reproducible results** with consistent extraction given same inputs
- **Audit trail** through detailed operation logs
- **Metrics collection** for quality monitoring

### Flexibility & Customization
- **Multiple filter strategies** (liberal, contextual, inclusive, recall, base)
- **Filter chaining** for complex multi-stage extraction
- **Configurable output formats** (JSON, Markdown, plain text)
- **Custom validation rules** per extraction field
- **Extensible architecture** for adding new strategies

### Production Readiness
- **No hardcoded credentials** - use environment variables
- **Comprehensive logging** with configurable levels
- **Health check capabilities** for service monitoring
- **Version tracking** in package metadata
- **Documentation** for API and usage patterns

## User Requirements

### Developer Experience
- **Simple API** for basic use cases (single method calls)
- **Progressive complexity** - advanced features available but not required
- **Clear documentation** with practical examples
- **Intuitive schema definition** through WhatToRetain specifications
- **Helpful error messages** that suggest solutions

### Data Extraction Control
- **Field-level specifications** with name, description, and validation
- **Context preservation options** to maintain data relationships
- **Contradiction checking** to eliminate conflicting information
- **Custom extraction rules** through text_rules lists
- **Example-driven extraction** for better LLM understanding

### Visibility & Debugging
- **Intermediate result access** to inspect each pipeline stage
- **Token usage breakdown** showing reduction at each phase
- **Performance metrics** including timing for each operation
- **Failed extraction analysis** with clear failure points
- **Prompt inspection** for understanding LLM interactions

### Output Requirements
- **Structured data output** in specified format
- **Preserved relationships** between extracted fields
- **Original content reference** for validation
- **Confidence indicators** where applicable
- **Export capabilities** to files with configurable encoding

### Use Case Support
- **E-commerce extraction**: prices, specifications, availability
- **Document processing**: tables, lists, structured content
- **Web scraping**: handling dynamic content and JavaScript
- **Research tasks**: preserving citations and references
- **Monitoring applications**: consistent extraction over time

## Compliance & Security Requirements

### Data Handling
- **No persistent storage** of extracted content by default
- **Configurable data retention** policies
- **Secure credential management** through environment variables
- **No logging of sensitive data** in debug output
- **Optional data anonymization** capabilities

### API Standards
- **RESTful design principles** where applicable
- **Consistent error response** formats
- **Rate limiting respect** for external services
- **Timeout handling** for all network operations
- **Graceful service degradation** under load

## Future Considerations

### Planned Enhancements
- **Additional LLM providers** beyond OpenAI
- **Custom model training** for domain-specific extraction
- **Distributed processing** for large-scale extraction
- **Real-time extraction** capabilities
- **WebSocket support** for streaming extraction

### Extensibility Requirements
- **Plugin architecture** for custom filters
- **Custom validator** support beyond regex
- **External storage** integration for results
- **Webhook notifications** for async operations
- **Multi-language** content support