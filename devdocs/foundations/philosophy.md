# ExtractHero - Project Philosophy

## Core Philosophy

ExtractHero embodies the principle of **"Accurate Extraction with Almost Zero Compromise"** - a commitment to preserving data integrity while intelligently filtering noise from real-world content.

## Fundamental Beliefs

### 1. **Schema-First, Not Prompt-First**
We believe extraction should be **declarative and explicit**. Rather than hoping an LLM understands vague instructions, we define exactly what we want through structured specifications. Every field has a name, description, validation rules, and examples. This isn't just about better results - it's about **predictable, reproducible extraction**.

### 2. **Divide and Conquer**
Complex problems require **staged solutions**. By separating reduction, filtering, and parsing into distinct phases, each stage can be optimized independently. This isn't over-engineering - it's recognition that a monolithic approach fails when dealing with real-world complexity.

### 3. **Favor Recall Over Precision (When Filtering)**
In the filtering phase, we believe it's **better to include too much than too little**. Missing critical data is unforgivable; including extra context is manageable. The parsing phase can handle refinement, but it cannot resurrect discarded information.

### 4. **Context Is Sacred**
Data without context is dangerous. We preserve **semantic relationships** - if a value appears in a table, we keep the table structure. If a specification is part of a list, we maintain the full list. Context isn't overhead; it's essential for accurate understanding.

### 5. **Transparency Through Metrics**
Every operation should be **measurable and accountable**. Token counts, reduction percentages, processing times, and costs aren't just metrics - they're commitments to transparency. Users deserve to know exactly what happened to their data at every stage.

### 6. **Graceful Degradation**
Perfect extraction is impossible, but **failure should be informative**. When extraction fails, we provide clear error messages, partial results where possible, and enough information to understand what went wrong. A failed extraction should still provide value.

### 7. **Production-First Design**
This isn't a research project - it's a **production tool**. Every feature must handle edge cases, scale efficiently, and fail gracefully. We optimize for reliability over cleverness, consistency over perfection.

## Design Principles

### **No Magic, Only Clarity**
Every transformation is explicit. Users can see exactly what happened at each stage, inspect intermediate results, and understand the decision logic. Black boxes have no place in data extraction.

### **Flexibility Without Complexity**
Multiple strategies, output formats, and processing options - but with **sensible defaults**. Advanced users can fine-tune everything; beginners can start with one line of code.

### **Respect the Source**
We don't normalize, interpret, or "improve" data unless explicitly asked. The source material is truth; our job is to extract it faithfully, not to editorialze it.

### **Cost-Conscious Processing**
LLM tokens are expensive. Every stage tracks usage, every reduction is measured, and every operation is optimized for efficiency. We treat computational resources as precious because they are.

## What We Stand Against

### **Brittle Extraction**
We reject hardcoded selectors, fragile XPath queries, and regex-only solutions. The web is dynamic; our extraction must be adaptive.

### **All-or-Nothing Approaches**
We don't believe in monolithic prompts that try to do everything at once. Complex tasks deserve sophisticated pipelines.

### **Opaque Operations**
Hidden processing, unclear transformations, and mysterious failures are unacceptable. Every operation should be inspectable and understandable.

### **One-Size-Fits-All**
Different content requires different strategies. We embrace this complexity rather than forcing everything through the same pipeline.

## The ExtractHero Promise

When you use ExtractHero, you're not just running an extraction - you're deploying a **philosophy of careful, measured, transparent data processing**. Every decision in our codebase reflects these beliefs:

- **Your data matters** - We'll preserve it faithfully
- **Your costs matter** - We'll minimize token usage
- **Your time matters** - We'll provide clear, actionable results
- **Your understanding matters** - We'll show you exactly what we did

This isn't just about extracting data. It's about **extracting data the right way** - with respect for the source, transparency in the process, and accountability for the results.