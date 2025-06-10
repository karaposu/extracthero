````markdown
# extracthero

Now you can extract information from any data with almost zero compromise. 


## Features

- **Multi-modal input**: ingest raw HTML strings, screenshot image files, or paired HTML+image inputs  
- **Spatial context preservation**: maintain element positions to extract data that depends on layout or visual proximity  
- **LLM-powered extraction**: plug in your favorite LLM (e.g. OpenAI, Anthropic Claude) for flexible schema-driven parsing  
- **Optional validation**: enable built-in rules or custom validators to enforce types, ranges and required fields  
- **Extensible pipeline**: hook into pre- and post-processing steps

## Installation

```bash
pip install extracthero
````


## Quickstart

```python
from extracthero import Extractor, ExtractConfig

# 1. Initialize with your LLM backend and schema
config = ExtractConfig(
    llm_backend="openai",
    prompt_template="Extract product titles and prices from the page",
    validation_enabled=True
)
extractor = Extractor(config)

# 2a. Extract from raw HTML
html = "<html>…</html>"
result_html = extractor.extract_from_html(html)
print(result_html)

# 2b. Extract from a screenshot
result_img = extractor.extract_from_screenshot("page.png")
print(result_img)

# 2c. Extract using both HTML + screenshot (preserve layout)
result_combo = extractor.extract_from_both(html, "page.png")
print(result_combo)
```

## Configuration

| Option               | Type    | Default       | Description                                                   |
| -------------------- | ------- | ------------- | ------------------------------------------------------------- |
| `llm_backend`        | `str`   | `"openai"`    | Which LLM to use (“openai”, “anthropic”, etc.)                |
| `prompt_template`    | `str`   | `None`        | Template guiding the LLM’s extraction instructions            |
| `validation_enabled` | `bool`  | `False`       | Turn on built-in schema and rule validation                   |
| `ocr_engine`         | `str`   | `"tesseract"` | OCR engine for screenshot text extraction                     |
| `spatial_threshold`  | `float` | `0.5`         | Minimum layout-overlap ratio to consider two elements related |

```python
from extracthero import ExtractConfig

config = ExtractConfig(
    llm_backend="anthropic",
    validation_enabled=False,
    spatial_threshold=0.7
)
```

## Validation Logic

When `validation_enabled=True`, extracted fields are checked against:

* **Type rules** (e.g. string, number, date)
* **Range checks** (e.g. price ≥ 0, date within the last year)
* **Presence** (required vs. optional fields)

Customize or extend:

```python
from extracthero.validation import Validator, FieldRule

# custom rule: price must be < 1 000 000
class PriceRule(FieldRule):
    def validate(self, value):
        return isinstance(value, (int, float)) and value < 1_000_000

config.custom_validators = {
    "price": PriceRule()
}
```

## CLI Interface

```bash
# Extract from HTML file
extracthero html input.html --schema product_schema.json --output out.json

# Extract from screenshot
extracthero image page.png --prompt "Get titles" --output out.json

# Combined mode
extracthero combo input.html page.png --output out.json
```

Use `extracthero --help` for full options and flags.

## Examples

1. **E-commerce product scraper**
2. **News article metadata extraction**
3. **Invoice data capture with layout**

See the [examples/](./examples) folder for ready-to-run demos.

## Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feat/my-feature`)
3. Implement & test
4. Submit a pull request

Please follow our [code style guide](./CONTRIBUTING.md) and write tests for new features.

