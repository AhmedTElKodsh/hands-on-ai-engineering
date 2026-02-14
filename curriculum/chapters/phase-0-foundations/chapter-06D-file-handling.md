# Chapter 6D: File Handling & Path Management
**Reading Prompts, Saving Outputs, and Managing Document Collections**

**Chapter Type**: Foundation | **Difficulty**: ⭐ | **Time**: 1.5 hours
**Prerequisites**: Chapter 1 (Environment Setup), Chapter 6B (Error Handling)
**Builds Toward**: All LLM chapters (7+), Document Processing (RAG in Ch 17-22), Batch Operations

**What You'll Build**: A file operations utility for reading prompts, saving LLM outputs, and managing document collections.

**Why This Matters**: Every AI project reads prompts from files and saves outputs. Whether you're processing documents for RAG, loading prompts for LLM calls, or saving generated content, file handling is the foundation. By the end of this chapter, you'll confidently manage files for any AI application.

---

## 🎯 Learning Objectives

By the end of this chapter, you will:

- ✅ Read and write text files with Python's built-in functions
- ✅ Use pathlib for cross-platform path management
- ✅ Implement file context managers (the `with` statement)
- ✅ Handle CSV and JSON files for structured data
- ✅ Perform directory operations safely
- ✅ Handle file errors gracefully (FileNotFoundError, PermissionError)
- ✅ Load prompts from files for LLM calls
- ✅ Save and organize LLM outputs
- ✅ Iterate through large files efficiently

---

## Part 1: The Hook - Your First File Read (5 Minutes)

### The Goal

You'll read a file and print its contents in **3 lines of code**. No theory yet—just working code.

### Create Your First File

Let's create a simple prompt file for an AI assistant:

**Step 1**: Create a new file `my_prompt.txt` in your project directory with this content:

```text
You are a helpful AI assistant specialized in explaining technical concepts.
Be clear, concise, and use analogies when helpful.
```

**Step 2**: Read and print the file with these 3 lines:

```python
# read_file.py
with open('my_prompt.txt') as f:
    content = f.read()
print(content)
```

**Step 3**: Run it:

```bash
python read_file.py
```

**Output**:
```
You are a helpful AI assistant specialized in explaining technical concepts.
Be clear, concise, and use analogies when helpful.
```

**🎉 Success!** You just read a file. Those 3 lines did something important:
1. **Opened** the file safely
2. **Read** all its contents
3. **Automatically closed** the file (the `with` statement did this!)

---

### Why This Is Powerful for AI

Imagine you're building an LLM application. Instead of hardcoding prompts in your Python files, you can:

```python
# Before: Hardcoded (hard to maintain)
prompt = "You are a helpful AI assistant..."

# After: From a file (easy to update, version control, share)
with open('system_prompt.txt') as f:
    prompt = f.read()
```

Now you can update prompts without changing code, share prompts with your team, and version control them separately.

---

## Part 2: Understanding What Just Happened (Deep Dive)

Now that you've seen file reading work, let's understand **why** it works and **how** to do more.

### The `with` Statement: Your Safety Net

You might be wondering: **"What is `with`? Why not just `open()` and `close()`?"**

Great question! Let's see the difference:

**❌ Without `with` (Risky)**:
```python
f = open('my_prompt.txt')
content = f.read()
f.close()  # What if an error happens before this line?
```

**Problem**: If an error occurs between `open()` and `close()`, the file stays open. This wastes resources and can cause issues.

**✅ With `with` (Safe)**:
```python
with open('my_prompt.txt') as f:
    content = f.read()
    # File automatically closes here, even if there's an error!
```

**Key Insight**: The `with` statement is a **context manager**. It guarantees the file closes, no matter what. Even if an exception occurs, Python cleans up for you.

**Analogy**: Think of `with` like an automatic door. You walk through (open the file), do your business (read/write), and the door closes behind you automatically—even if you trip on the way out!

---

### File Modes: Choosing Your Action

When you call `open()`, you can specify a **mode** that tells Python what you want to do:

| Mode | Name | What It Does | Example Use Case |
|------|------|-------------|------------------|
| `'r'` | Read (default) | Read file contents | Loading prompts |
| `'w'` | Write | Create or overwrite file | Saving LLM outputs |
| `'a'` | Append | Add to end of file | Logging |
| `'r+'` | Read & Write | Read and modify | Editing configs |
| `'x'` | Exclusive Create | Create only if doesn't exist | Preventing overwrites |

**Examples**:

```python
# Read mode (default)
with open('prompts.txt', 'r') as f:
    content = f.read()

# Write mode (creates new or overwrites existing)
with open('output.txt', 'w') as f:
    f.write("Generated text from LLM")

# Append mode (adds to end, preserves existing content)
with open('log.txt', 'a') as f:
    f.write("New log entry\n")
```

**⚠️ Warning**: `'w'` mode **erases** existing content! If the file exists, it's completely overwritten. Use `'a'` to preserve existing data.

---

### Reading Files: Three Patterns

**Pattern 1: Read Entire File at Once** (Best for small files)

```python
with open('small_prompt.txt') as f:
    content = f.read()  # Returns entire file as a string
```

**Use when**: File is small (<1MB), you need all content at once.

---

**Pattern 2: Read Line by Line** (Best for large files)

```python
with open('large_document.txt') as f:
    for line in f:
        print(line.strip())  # Process each line individually
```

**Use when**: File is large, you process lines independently (like logs).

**Why This Works**: Python reads one line at a time into memory, not the entire file. Perfect for gigabyte-sized files!

---

**Pattern 3: Read All Lines into a List**

```python
with open('prompts.txt') as f:
    lines = f.readlines()  # Returns list of lines

# Each line includes '\n', so strip it:
clean_lines = [line.strip() for line in lines]
```

**Use when**: You need random access to lines (e.g., `lines[5]`).

---

### Writing Files: Creating AI Outputs

Let's say your LLM generated some text. Here's how to save it:

```python
# Generate some AI output (simplified)
llm_response = """
# Marketing Plan

## Executive Summary
Our AI-powered marketing strategy leverages...
"""

# Save to file
with open('generated_plan.md', 'w') as f:
    f.write(llm_response)

print("✅ Saved to generated_plan.md")
```

**What if the file already exists?** With `'w'` mode, it gets overwritten. To prevent this, use `'x'` mode:

```python
try:
    with open('generated_plan.md', 'x') as f:
        f.write(llm_response)
except FileExistsError:
    print("⚠️ File already exists. Choose a different name or use 'w' to overwrite.")
```

---

## Part 3: Working with Paths - The Right Way

### The Problem with String Paths

You might be tempted to build file paths like this:

```python
# ❌ Don't do this!
path = "outputs/" + username + "/" + filename + ".txt"
```

**Problems**:
1. **Slash direction**: `"/"` works on Mac/Linux, but Windows uses `"\"`
2. **Path separators**: Hardcoding slashes breaks cross-platform compatibility
3. **Path manipulation**: Want to get the file extension? Good luck parsing strings!

---

### The Solution: `pathlib`

Python's `pathlib` module provides a cross-platform way to work with file paths:

```python
from pathlib import Path

# Create paths (works on Windows, Mac, Linux!)
prompt_file = Path('prompts') / 'system_prompt.txt'
output_dir = Path('outputs') / 'user_123'

print(prompt_file)  # prompts/system_prompt.txt (or prompts\system_prompt.txt on Windows)
```

**Key Benefits**:
1. **Cross-platform**: `/` operator works everywhere
2. **Path manipulation**: Easy methods for common tasks
3. **Type safety**: Paths are `Path` objects, not strings
4. **Readable**: `Path('a') / 'b' / 'c'` vs `"a" + "/" + "b" + "/" + "c"`

---

### Common `pathlib` Operations

```python
from pathlib import Path

file = Path('outputs/generated_report.md')

# Check if file exists
if file.exists():
    print("File found!")

# Check if it's a file (not a directory)
if file.is_file():
    print("It's a file")

# Get file extension
print(file.suffix)  # '.md'

# Get file name without extension
print(file.stem)  # 'generated_report'

# Get parent directory
print(file.parent)  # outputs

# Get absolute path
print(file.absolute())  # /Users/you/project/outputs/generated_report.md

# Create parent directories if they don't exist
file.parent.mkdir(parents=True, exist_ok=True)
```

---

### Reading/Writing with `pathlib`

`Path` objects have convenient read/write methods:

```python
from pathlib import Path

# Read entire file
prompt_path = Path('prompts/system.txt')
content = prompt_path.read_text()

# Write to file
output_path = Path('outputs/response.txt')
output_path.write_text("LLM response here")

# Read lines
lines = prompt_path.read_text().splitlines()
```

**Convenience**: These methods handle opening, reading/writing, and closing automatically!

---

## Part 4: Working with Structured Data

### CSV Files: Tabular Data

CSV (Comma-Separated Values) is perfect for storing structured data like user inputs, evaluation results, or datasets.

**Example**: Store LLM evaluation results

```python
import csv
from pathlib import Path

# Data to save
results = [
    {'prompt': 'Explain AI', 'model': 'gpt-4', 'quality': 9.2, 'cost': 0.003},
    {'prompt': 'Write code', 'model': 'claude', 'quality': 9.5, 'cost': 0.002},
]

# Write CSV
csv_path = Path('outputs/eval_results.csv')
with open(csv_path, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['prompt', 'model', 'quality', 'cost'])
    writer.writeheader()
    writer.writerows(results)

print(f"✅ Saved {len(results)} results to CSV")
```

**Output** (`eval_results.csv`):
```
prompt,model,quality,cost
Explain AI,gpt-4,9.2,0.003
Write code,claude,9.5,0.002
```

---

**Reading CSV**:

```python
import csv

with open('outputs/eval_results.csv', newline='') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"{row['model']}: Quality {row['quality']}")
```

**Output**:
```
gpt-4: Quality 9.2
claude: Quality 9.5
```

---

### JSON Files: Nested Data

JSON is ideal for configuration files, API responses, and nested data structures.

**Example**: Save LLM configuration

```python
import json
from pathlib import Path

config = {
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 1000,
    "system_prompt": "You are a helpful assistant",
    "fallback_models": ["gpt-3.5-turbo", "claude-v1"]
}

# Write JSON (pretty-printed)
config_path = Path('config/llm_settings.json')
config_path.parent.mkdir(parents=True, exist_ok=True)

with open(config_path, 'w') as f:
    json.dump(config, f, indent=2)

print("✅ Config saved")
```

**Output** (`llm_settings.json`):
```json
{
  "model": "gpt-4",
  "temperature": 0.7,
  "max_tokens": 1000,
  "system_prompt": "You are a helpful assistant",
  "fallback_models": [
    "gpt-3.5-turbo",
    "claude-v1"
  ]
}
```

---

**Reading JSON**:

```python
import json

with open('config/llm_settings.json') as f:
    config = json.load(f)

print(f"Using model: {config['model']}")
print(f"Temperature: {config['temperature']}")
```

---

## Part 5: Error Handling for Files

Files can fail in many ways. Let's handle them gracefully.

### Common File Errors

**1. File Not Found**

```python
from pathlib import Path

def load_prompt(filename):
    prompt_path = Path('prompts') / filename

    try:
        return prompt_path.read_text()
    except FileNotFoundError:
        print(f"❌ Error: '{prompt_path}' not found")
        print("💡 Tip: Check spelling and that the 'prompts/' directory exists")
        return None

# Usage
prompt = load_prompt('system.txt')
if prompt:
    print("Loaded successfully!")
```

---

**2. Permission Denied**

```python
def save_output(content, filepath):
    try:
        Path(filepath).write_text(content)
    except PermissionError:
        print(f"❌ Permission denied: Cannot write to '{filepath}'")
        print("💡 Tip: Check file permissions or try a different directory")
    except OSError as e:
        print(f"❌ OS error: {e}")
```

---

**3. Comprehensive Error Handling**

```python
from pathlib import Path

def safe_read_file(filepath):
    """Safely read a file with comprehensive error handling"""
    path = Path(filepath)

    # Check if file exists
    if not path.exists():
        return None, f"File not found: {filepath}"

    # Check if it's actually a file (not a directory)
    if not path.is_file():
        return None, f"Not a file: {filepath}"

    # Try to read
    try:
        content = path.read_text(encoding='utf-8')
        return content, None
    except PermissionError:
        return None, f"Permission denied: {filepath}"
    except UnicodeDecodeError:
        return None, f"Cannot decode file (not UTF-8): {filepath}"
    except Exception as e:
        return None, f"Unexpected error: {e}"

# Usage
content, error = safe_read_file('prompts/system.txt')
if error:
    print(f"❌ {error}")
else:
    print(f"✅ Read {len(content)} characters")
```

---

## Part 6: Directory Operations

### Creating Directories

```python
from pathlib import Path

# Create a single directory
output_dir = Path('outputs')
output_dir.mkdir(exist_ok=True)  # Won't error if already exists

# Create nested directories
nested_path = Path('outputs/user_123/session_456')
nested_path.mkdir(parents=True, exist_ok=True)  # Creates all parent dirs
```

**Parameters**:
- `exist_ok=True`: Don't raise error if directory exists
- `parents=True`: Create parent directories if needed

---

### Listing Files in a Directory

```python
from pathlib import Path

# List all files in a directory
prompts_dir = Path('prompts')
for file in prompts_dir.iterdir():
    if file.is_file():
        print(f"Found: {file.name}")
```

---

**Filter by extension** (glob pattern):

```python
# Find all .txt files
txt_files = list(prompts_dir.glob('*.txt'))
print(f"Found {len(txt_files)} text files")

# Find all .json files recursively
json_files = list(prompts_dir.rglob('*.json'))  # Searches subdirectories too!
```

---

### Practical Example: Organizing LLM Outputs

```python
from pathlib import Path
from datetime import datetime

def save_llm_output(content, model_name):
    """Save LLM output with timestamp and model name"""
    # Create outputs directory
    output_dir = Path('outputs') / model_name
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"response_{timestamp}.txt"
    filepath = output_dir / filename

    # Save content
    filepath.write_text(content)

    print(f"✅ Saved to {filepath}")
    return filepath

# Usage
response = "This is the LLM's generated response..."
save_llm_output(response, model_name='gpt-4')
# Output: ✅ Saved to outputs/gpt-4/response_20260210_143022.txt
```

---

## Part 7: Putting It All Together - LLM Prompt Manager

Let's build a practical utility for managing prompts and outputs.

```python
# prompt_manager.py
from pathlib import Path
import json
from datetime import datetime

class PromptManager:
    """Manage LLM prompts and outputs"""

    def __init__(self, base_dir='ai_data'):
        self.base_dir = Path(base_dir)
        self.prompts_dir = self.base_dir / 'prompts'
        self.outputs_dir = self.base_dir / 'outputs'

        # Create directories
        self.prompts_dir.mkdir(parents=True, exist_ok=True)
        self.outputs_dir.mkdir(parents=True, exist_ok=True)

    def load_prompt(self, name):
        """Load a prompt by name"""
        prompt_path = self.prompts_dir / f"{name}.txt"

        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt not found: {name}")

        return prompt_path.read_text()

    def save_prompt(self, name, content):
        """Save a prompt"""
        prompt_path = self.prompts_dir / f"{name}.txt"
        prompt_path.write_text(content)
        print(f"✅ Saved prompt: {name}")

    def save_output(self, content, model='default', metadata=None):
        """Save LLM output with metadata"""
        # Create model directory
        model_dir = self.outputs_dir / model
        model_dir.mkdir(exist_ok=True)

        # Generate timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Save content
        content_path = model_dir / f"{timestamp}.txt"
        content_path.write_text(content)

        # Save metadata if provided
        if metadata:
            meta_path = model_dir / f"{timestamp}_meta.json"
            with open(meta_path, 'w') as f:
                json.dump(metadata, f, indent=2)

        print(f"✅ Saved output: {content_path}")
        return content_path

    def list_prompts(self):
        """List all available prompts"""
        prompts = [f.stem for f in self.prompts_dir.glob('*.txt')]
        return sorted(prompts)

    def list_outputs(self, model='default'):
        """List outputs for a specific model"""
        model_dir = self.outputs_dir / model
        if not model_dir.exists():
            return []

        outputs = [f.stem for f in model_dir.glob('*.txt')]
        return sorted(outputs)

# Usage example
if __name__ == '__main__':
    manager = PromptManager()

    # Save a prompt
    system_prompt = "You are a helpful AI assistant"
    manager.save_prompt('system', system_prompt)

    # Load and use
    prompt = manager.load_prompt('system')
    print(f"Loaded: {prompt}")

    # Save output with metadata
    llm_response = "Here's my generated response..."
    metadata = {
        'model': 'gpt-4',
        'temperature': 0.7,
        'tokens': 150
    }
    manager.save_output(llm_response, model='gpt-4', metadata=metadata)

    # List all prompts
    print(f"Available prompts: {manager.list_prompts()}")
```

**Output**:
```
✅ Saved prompt: system
Loaded: You are a helpful AI assistant
✅ Saved output: ai_data/outputs/gpt-4/20260210_143520.txt
Available prompts: ['system']
```

---

## 🧪 Try This! Exercises

### Exercise 1: Prompt Library

**Goal**: Create a library of different prompts and load them dynamically.

**Tasks**:
1. Create a `prompts/` directory
2. Save 3 different prompts as text files:
   - `creative.txt`: "You are a creative writer..."
   - `technical.txt`: "You are a technical expert..."
   - `summarizer.txt`: "You are a concise summarizer..."
3. Write a function that takes a prompt name and returns its content
4. Print each prompt to verify

**Starter Code**:
```python
from pathlib import Path

def get_prompt(name):
    # Your code here
    pass

# Test it
print(get_prompt('creative'))
print(get_prompt('technical'))
```

---

### Exercise 2: LLM Response Logger

**Goal**: Log all LLM responses with timestamps.

**Tasks**:
1. Create a function `log_response(model, prompt, response)` that:
   - Creates an `outputs/` directory
   - Saves the response to a file with timestamp
   - Appends a summary line to `log.txt` with timestamp, model, and prompt (first 50 chars)
2. Call it 3 times with different data
3. Read and print `log.txt`

**Expected Output** (log.txt):
```
2026-02-10 14:35:20 | gpt-4 | Explain quantum computing
2026-02-10 14:35:25 | claude | Write a poem about AI
2026-02-10 14:35:30 | gpt-3.5 | Summarize this article
```

---

## 📚 Summary: Key Takeaways

Let's recap what you've learned:

1. **✅ `with` statement is essential**: Always use `with open()` to ensure files close properly—even if errors occur.

2. **✅ File modes matter**: `'r'` reads, `'w'` overwrites, `'a'` appends, `'x'` creates only if new.

3. **✅ Read patterns for different scenarios**:
   - `read()` for small files (entire content at once)
   - Line iteration for large files (memory-efficient)
   - `readlines()` for random access to lines

4. **✅ pathlib is better than string paths**: Cross-platform, readable, and feature-rich.

5. **✅ Common pathlib operations**: `exists()`, `is_file()`, `mkdir(parents=True, exist_ok=True)`, `glob()`, `read_text()`, `write_text()`.

6. **✅ CSV for tabular data**: Use `csv.DictWriter` and `csv.DictReader` for structured data.

7. **✅ JSON for nested data**: Use `json.dump()` and `json.load()` for configs and complex structures.

8. **✅ Handle errors gracefully**: `FileNotFoundError`, `PermissionError`, `UnicodeDecodeError`—catch them and provide helpful messages.

9. **✅ Organize AI outputs**: Use directories, timestamps, and metadata for managing LLM responses.

10. **✅ Build utilities**: Encapsulate file operations in classes like `PromptManager` for reusability.

---

## 🔗 What's Next?

With file handling mastered, you're ready to:

- **Chapter 7-12**: Read prompts from files for LLM calls, save responses
- **Chapter 17-22**: Load documents for RAG (Retrieval-Augmented Generation)
- **Chapter 50-54**: Generate and save contracts, proposals, reports

**File handling is the foundation of every AI project**. You'll use these patterns hundreds of times in the coming chapters!

---

## ✅ Verification: Test Your Knowledge

Run this verification script to ensure everything works:

```python
# verify_chapter_6d.py
from pathlib import Path
import json
import csv

def test_basic_read_write():
    """Test basic file operations"""
    # Write
    test_file = Path('test_output.txt')
    test_file.write_text("Hello from file!")

    # Read
    content = test_file.read_text()
    assert content == "Hello from file!", "Content mismatch"

    # Cleanup
    test_file.unlink()
    print("✅ Basic read/write works")

def test_pathlib_operations():
    """Test pathlib operations"""
    # Create nested directory
    test_dir = Path('test_dir/nested/deep')
    test_dir.mkdir(parents=True, exist_ok=True)

    assert test_dir.exists(), "Directory not created"
    assert test_dir.is_dir(), "Not a directory"

    # Cleanup
    import shutil
    shutil.rmtree('test_dir')
    print("✅ pathlib operations work")

def test_json_operations():
    """Test JSON read/write"""
    data = {'model': 'gpt-4', 'temp': 0.7}
    json_path = Path('test.json')

    # Write
    with open(json_path, 'w') as f:
        json.dump(data, f)

    # Read
    with open(json_path) as f:
        loaded = json.load(f)

    assert loaded == data, "JSON data mismatch"

    # Cleanup
    json_path.unlink()
    print("✅ JSON operations work")

def test_csv_operations():
    """Test CSV read/write"""
    data = [{'name': 'Alice', 'score': 95}, {'name': 'Bob', 'score': 87}]
    csv_path = Path('test.csv')

    # Write
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'score'])
        writer.writeheader()
        writer.writerows(data)

    # Read
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        loaded = list(reader)

    assert len(loaded) == 2, "CSV row count mismatch"

    # Cleanup
    csv_path.unlink()
    print("✅ CSV operations work")

def test_error_handling():
    """Test error handling"""
    try:
        Path('nonexistent.txt').read_text()
        assert False, "Should have raised FileNotFoundError"
    except FileNotFoundError:
        print("✅ Error handling works")

if __name__ == '__main__':
    test_basic_read_write()
    test_pathlib_operations()
    test_json_operations()
    test_csv_operations()
    test_error_handling()
    print("\n🎉 All tests passed! You've mastered file handling!")
```

**Run it**:
```bash
python verify_chapter_6d.py
```

**Expected Output**:
```
✅ Basic read/write works
✅ pathlib operations work
✅ JSON operations work
✅ CSV operations work
✅ Error handling works

🎉 All tests passed! You've mastered file handling!
```

---

**You're ready for the next chapter!** File handling is now in your toolkit. Next up: **Chapter 7 - Your First LLM Call** 🚀
