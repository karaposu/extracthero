
import tiktoken
import time

# === WHAT lru_cache DOES ===

# @lru_cache(maxsize=1)
def get_tiktoken_encoding(model_name="gpt-4o-mini"):
    """Get tiktoken encoding with caching to avoid repeated initialization."""
    print(f"🔄 ACTUALLY LOADING tiktoken for {model_name}...")  # This will only print once!
    import tiktoken
    return tiktoken.encoding_for_model(model_name)

# === DEMONSTRATION ===

print("=== First call ===")
start = time.time()
encoding1 = get_tiktoken_encoding("gpt-4o-mini")
print(f"Time taken: {time.time() - start:.6f}s")
print(f"Encoding object: {type(encoding1)}")

print("\n=== Second call (same arguments) ===")
start = time.time()
encoding2 = get_tiktoken_encoding("gpt-4o-mini")  # Same arguments!
print(f"Time taken: {time.time() - start:.6f}s")  # Much faster!
print(f"Same object? {encoding1 is encoding2}")  # True - exact same object!

print("\n=== Third call (same arguments) ===")
start = time.time()
encoding3 = get_tiktoken_encoding("gpt-4o-mini")
print(f"Time taken: {time.time() - start:.6f}s")  # Still fast!

print("\n=== Different arguments ===")
start = time.time()
encoding4 = get_tiktoken_encoding("gpt-4o")  # Different model!
print(f"Time taken: {time.time() - start:.6f}s")  


