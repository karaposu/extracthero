# ExtractHero - Project Description

## What Are We Building?

ExtractHero is a Python library that provides **accurate, structured data extraction** from messy, real-world content sources. It acts as an intelligent extraction pipeline that can process various input formats (raw HTML, screenshots, PDFs, JSON blobs, plain text) and convert them into clean, structured data with minimal loss of important information.

The system employs a sophisticated three-phase pipeline:
1. **Reduction** - Removes noise and clutter from input data
2. **Filtering** - Isolates relevant content based on extraction requirements  
3. **Parsing** - Extracts specific structured fields from filtered content

## What Problem Are We Solving?

### The Core Challenge
Real-world data extraction faces several critical problems:

1. **DOM Pollution** - Web pages contain massive amounts of non-content elements (ads, navigation bars, JavaScript widgets, tracking pixels) that pollute extraction attempts and confuse traditional parsers

2. **Needle in Haystack** - Important data is often buried in large documents, causing LLMs to hallucinate or produce unstructured output when processing too much content at once

3. **Brittle Extraction Logic** - Simple prompts like "extract price" fail in production because real-world extraction requires complex, context-dependent logic

4. **Format Heterogeneity** - Data comes in various formats (HTML, JSON, PDFs, screenshots) each requiring different optimization strategies

5. **Post-hoc Validation Complexity** - Validating extracted data after the fact is messy and error-prone without built-in validation mechanisms

## Project Scopes

### 1. **Core Extraction Engine**
- Multi-phase pipeline orchestration
- LLM-based intelligent filtering and parsing
- Token optimization and reduction tracking
- Async/sync operation support

### 2. **Input Processing**
- HTML reduction and cleaning
- JSON fast-path extraction
- PDF text and visual extraction
- Screenshot analysis
- Plain text processing

### 3. **Extraction Control**
- Schema-first extraction with `WhatToRetain` specifications
- Multiple filtering strategies (liberal, contextual, inclusive, recall)
- Filter chaining for progressive refinement
- Validation rules and regex patterns

### 4. **Output Management**
- Multiple output formats (JSON, Markdown, plain text)
- Token usage metrics and cost tracking
- Detailed operation results with error handling
- Stage-by-stage performance analytics

### 5. **Developer Experience**
- Simple, declarative API
- Comprehensive error messages
- Detailed logging and debugging
- Both synchronous and asynchronous interfaces

## Who Are The Targeted Users?

### Primary Users

1. **Data Engineers**
   - Need reliable extraction from multiple sources
   - Require consistent, structured output
   - Value token efficiency and cost optimization
   - Need production-grade error handling

2. **Web Scraping Developers**
   - Deal with complex, dynamic websites
   - Need to handle JavaScript-rendered content
   - Require robust noise filtering
   - Want to avoid maintaining brittle CSS/XPath selectors

3. **AI/ML Engineers**
   - Need clean training data from web sources
   - Require structured data for model inputs
   - Want to minimize LLM costs through efficient filtering
   - Need reliable validation of extracted data

4. **Business Analysts**
   - Extract competitive intelligence from websites
   - Monitor product information across e-commerce sites
   - Gather structured data from PDF reports
   - Need accurate, validated data for analysis

5. **Research Teams**
   - Extract academic data from papers and websites
   - Need high accuracy with minimal data loss
   - Require preservation of data relationships
   - Want reproducible extraction results

### Secondary Users

1. **API Developers** - Building data extraction services
2. **Content Aggregators** - Collecting information from multiple sources
3. **Compliance Teams** - Extracting regulatory information from documents
4. **Product Managers** - Monitoring competitor features and pricing

## Use Case Examples

1. **E-commerce Price Monitoring** - Extract product prices, specifications, and availability from competitor websites
2. **Financial Document Processing** - Extract key figures from earnings reports and regulatory filings
3. **Real Estate Listings** - Gather property details from multiple listing sites
4. **Job Market Analysis** - Extract job posting details for market research
5. **Academic Research** - Extract citations, figures, and data from research papers
6. **Legal Document Analysis** - Extract clauses and terms from contracts and agreements