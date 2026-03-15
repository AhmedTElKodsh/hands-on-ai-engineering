# Week 16: Specialization Tracks — Layer 1 Final

**Purpose:** Deep-dive into one specialized area based on career goals
**Duration:** 5 days (20 hours)
**Deliverable:** Working mini-project + blog post

---

## 🎯 TRACK SELECTION GUIDE

Choose ONE track based on your target role:

| Track | Best For | Prerequisites | Difficulty |
|-------|----------|---------------|------------|
| **A: NL2SQL Agent** | Backend-focused AI roles, enterprise data teams | Week 1-15 complete, SQL basics | ⭐⭐⭐ |
| **B: Document Intelligence** | AI startup roles, document processing companies | Week 1-15 complete | ⭐⭐⭐ |
| **C: Fine-Tuning Sprint** | ML platform roles, custom model teams | Week 1-15 complete, GPU access helpful | ⭐⭐⭐⭐ |

**Not sure?** Pick Track A or B. Fine-tuning is specialized and often overrated for entry-level AI engineer roles.

---

## 📅 WEEK STRUCTURE

| Day | Activity | Time |
|-----|----------|------|
| **Days 1-3** | Build core functionality | 12 hours |
| **Day 4** | Testing + documentation | 4 hours |
| **Day 5** | Polish + blog post | 4 hours |

---

# 🗄️ TRACK A: NL2SQL AGENT

## Overview

Build an agent that converts natural language questions to SQL queries, executes them safely, and explains results.

**Example:**
```
User: "Show me the top 5 customers by revenue in Q4"
Agent: SELECT customer_id, SUM(revenue) FROM orders 
       WHERE quarter = 'Q4' GROUP BY customer_id ORDER BY 2 DESC LIMIT 5
Result: [table + explanation]
```

---

## Day 1: Schema + Safe Query Design

**Learning (80 min):**
- SQL generation patterns (prompt engineering)
- Query validation (allowlist approach)
- Read-only user setup

**Build (120 min):**

### Step 1: Define Your Schema

```python
# schemas/database.py
DATABASE_SCHEMA = """
Tables:
- customers(id, name, email, created_at)
- orders(id, customer_id, total, status, created_at)
- products(id, name, price, category)
- order_items(id, order_id, product_id, quantity, price)
"""
```

### Step 2: Build Query Validator

```python
# app/validators/sql.py
class SQLValidator:
    ALLOWED_OPERATIONS = ['SELECT']
    FORBIDDEN_OPERATIONS = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER']
    
    def validate(self, query: str) -> tuple[bool, str]:
        query_upper = query.upper().strip()
        
        # Must start with SELECT
        if not query_upper.startswith('SELECT'):
            return False, "Only SELECT queries allowed"
        
        # Check for forbidden operations
        for forbidden in self.FORBIDDEN_OPERATIONS:
            if forbidden in query_upper:
                return False, f"{forbidden} operations not allowed"
        
        # Limit results
        if 'LIMIT' not in query_upper:
            query += " LIMIT 100"
        
        return True, query
```

**Checkpoint:**
- [ ] Schema documented
- [ ] Validator rejects dangerous queries
- [ ] Validator adds LIMIT if missing

---

## Day 2: NL2SQL Generation

**Learning (80 min):**
- Prompt engineering for SQL generation
- Few-shot examples
- Schema injection patterns

**Build (120 min):**

### Step 1: Build the Prompt

```python
# app/prompts/nl2sql.py
NL2SQL_PROMPT = """
You are a SQL expert. Convert natural language questions to SQL queries.

Database Schema:
{schema}

Rules:
1. Only SELECT queries (read-only)
2. Always include LIMIT (default 100)
3. Use table aliases for clarity
4. Add comments for complex logic

Examples:

Question: "Show me all customers"
SQL: SELECT * FROM customers LIMIT 100

Question: "Top 5 products by sales"
SQL: 
SELECT p.name, SUM(oi.quantity * oi.price) as total_sales
FROM products p
JOIN order_items oi ON p.id = oi.product_id
GROUP BY p.id
ORDER BY total_sales DESC
LIMIT 5

Question: {question}
SQL:
"""
```

### Step 2: Generate + Validate

```python
# app/services/nl2sql.py
async def generate_sql(question: str) -> str:
    # Generate with LLM
    prompt = NL2SQL_PROMPT.format(schema=DATABASE_SCHEMA, question=question)
    response = await llm.generate(prompt)
    sql = extract_sql_from_response(response)
    
    # Validate
    validator = SQLValidator()
    is_valid, result = validator.validate(sql)
    
    if not is_valid:
        raise ValueError(f"Invalid SQL: {result}")
    
    return result
```

**Checkpoint:**
- [ ] Prompt includes schema + examples
- [ ] LLM generates valid SQL
- [ ] Validator catches bad queries

---

## Day 3: Execution + Explanation

**Learning (80 min):**
- Safe SQL execution (parameterized queries)
- Result formatting
- Natural language explanation

**Build (120 min):**

### Step 1: Execute Safely

```python
# app/services/database.py
class DatabaseService:
    def __init__(self, read_only_connection):
        # Use read-only database user
        self.conn = read_only_connection
    
    async def execute_query(self, query: str) -> list[dict]:
        try:
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query)  # Already validated
            results = cursor.fetchall()
            return [dict(row) for row in results]
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Query failed: {str(e)}")
```

### Step 2: Generate Explanation

```python
# app/services/explainer.py
EXPLAIN_PROMPT = """
Explain this SQL query and its results in plain English.

Query: {query}

Results: {results}

Explain:
1. What the query does
2. Key findings from the results
3. Any notable patterns
"""

async def explain_query(query: str, results: list[dict]) -> str:
    # Summarize results if too many
    if len(results) > 10:
        results_summary = f"Showing first 10 of {len(results)} results"
    else:
        results_summary = json.dumps(results, indent=2)
    
    prompt = EXPLAIN_PROMPT.format(query=query, results=results_summary)
    explanation = await llm.generate(prompt)
    return explanation
```

### Step 3: Build API Endpoint

```python
# app/routes/nl2sql.py
@router.post("/ask")
async def ask_question(question: str):
    # Generate SQL
    sql = await generate_sql(question)
    
    # Execute
    results = await db.execute_query(sql)
    
    # Explain
    explanation = await explain_query(sql, results)
    
    return {
        "question": question,
        "sql": sql,
        "results": results,
        "explanation": explanation
    }
```

**Checkpoint:**
- [ ] API endpoint works
- [ ] Results returned as JSON
- [ ] Explanation is clear

---

## Day 4: Testing + Security

**Testing (120 min):**

```python
# tests/test_nl2sql.py
def test_simple_question():
    response = client.post("/ask?question=Show me all customers")
    assert response.status_code == 200
    assert "SELECT" in response.json()["sql"]
    assert "customers" in response.json()["sql"]

def test_dangerous_question_rejected():
    response = client.post("/ask?question=Delete all customers")
    assert response.status_code == 400
    assert "DELETE" in str(response.json()["detail"])

def test_complex_join():
    response = client.post("/ask?question=Top 5 products by revenue")
    assert response.status_code == 200
    assert "JOIN" in response.json()["sql"]
    assert "LIMIT" in response.json()["sql"]

def test_sql_injection_attempt():
    response = client.post("/ask?question=Show customers; DROP TABLE customers;--")
    # Should be rejected or sanitized
    assert response.status_code in [200, 400]
```

**Security Audit (40 min):**

```markdown
# Security Review — NL2SQL Agent

## Threats Mitigated
- [x] SQL injection (read-only user, validation)
- [x] Dangerous operations (allowlist)
- [x] Resource exhaustion (LIMIT enforced)
- [x] Prompt injection (input sanitization)

## Remaining Risks
- Complex queries could be slow (add query timeout)
- Large result sets (already limited to 100)
- Schema exposure (only show necessary tables)

## Testing Done
- [x] SQL injection attempts
- [x] Forbidden operation attempts
- [x] Edge cases (empty results, complex queries)
```

---

## Day 5: Polish + Blog Post

**Polish (80 min):**
- [ ] README with architecture diagram
- [ ] Demo video (2 min)
- [ ] Deploy to Streamlit Cloud or similar

**Blog Post (120 min):**

Write: "Building a Safe NL2SQL Agent: Lessons from Production"

**Outline:**
```markdown
# Building a Safe NL2SQL Agent: Lessons from Production

## The Challenge
Natural language to SQL sounds simple until you realize users will ask for 
anything, including things that could destroy your database.

## Architecture Overview
[Diagram: User → LLM → Validator → Database → Explainer → User]

## Key Safety Mechanisms
1. Read-only database user
2. SQL allowlist (SELECT only)
3. Automatic LIMIT enforcement
4. Prompt injection defense

## What Broke During Development
- [Failure from FAILURE-LOG.md]
- How you fixed it

## When to Use This Pattern
- Internal tools for non-technical users
- Customer-facing analytics
- Quick data exploration

## When NOT to Use This
- Write operations (obviously)
- Complex analytical queries (use BI tools)
- High-stakes decisions without human review

## Code Examples
[Key snippets from your implementation]

## Next Steps
- Query caching for repeated questions
- Query optimization suggestions
- Natural language follow-ups ("show me more")
```

---

## Track A Deliverables

| Item | Complete | Link |
|------|----------|------|
| Working NL2SQL API | ⬜ | |
| Security audit document | ⬜ | |
| Test suite (5+ tests) | ⬜ | |
| README with architecture | ⬜ | |
| Demo video | ⬜ | |
| Blog post | ⬜ | |

---

# 📄 TRACK B: DOCUMENT INTELLIGENCE

## Overview

Build a multi-modal document processing system that extracts structured data from documents containing text, tables, and images.

**Example:**
```
Input: Invoice PDF with logo, line items table, totals
Output: {
  "vendor": "Acme Corp",
  "invoice_number": "INV-2026-001",
  "line_items": [...],
  "total": 1250.00,
  "currency": "USD"
}
```

---

## Day 1: Document Loading + OCR

**Learning (80 min):**
- PDF parsing (PyMuPDF, pdfplumber)
- OCR for scanned documents (Tesseract, EasyOCR)
- Image extraction from PDFs

**Build (120 min):**

### Step 1: Universal Document Loader

```python
# app/loaders/document.py
class DocumentLoader:
    def load(self, file_path: str) -> Document:
        ext = Path(file_path).suffix.lower()
        
        if ext == '.pdf':
            return self._load_pdf(file_path)
        elif ext in ['.png', '.jpg', '.jpeg']:
            return self._load_image(file_path)
        elif ext == '.tiff':
            return self._load_tiff(file_path)
        else:
            raise ValueError(f"Unsupported format: {ext}")
    
    def _load_pdf(self, file_path: str) -> Document:
        # Check if PDF is text-based or scanned
        if self._is_scanned(file_path):
            return self._load_pdf_ocr(file_path)
        else:
            return self._load_pdf_text(file_path)
    
    def _is_scanned(self, file_path: str) -> bool:
        # Use pdfplumber to check for text
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                if page.extract_text():
                    return False
        return True
```

### Step 2: OCR for Scanned Documents

```python
# app/loaders/ocr.py
import easyocr

class OCRService:
    def __init__(self):
        self.reader = easyocr.Reader(['en'], gpu=False)
    
    def extract_text(self, image_path: str) -> str:
        results = self.reader.readtext(image_path)
        text = "\n".join([r[1] for r in results])
        return text
    
    def extract_with_boxes(self, image_path: str) -> list[dict]:
        """Extract text with bounding boxes for layout analysis"""
        results = self.reader.readtext(image_path)
        return [
            {
                "text": r[1],
                "confidence": r[2],
                "bbox": r[0]  # [[x1,y1], [x2,y1], [x2,y2], [x1,y2]]
            }
            for r in results
        ]
```

**Checkpoint:**
- [ ] PDFs load (text or OCR)
- [ ] Images load
- [ ] Text extracted with layout info

---

## Day 2: Table Extraction

**Learning (80 min):**
- Table detection in PDFs
- Structured table parsing
- Handling merged cells

**Build (120 min):**

### Step 1: Detect + Extract Tables

```python
# app/extractors/tables.py
import pdfplumber
import camelot

class TableExtractor:
    def extract_tables(self, file_path: str) -> list[dict]:
        ext = Path(file_path).suffix.lower()
        
        if ext == '.pdf':
            return self._extract_pdf_tables(file_path)
        else:
            raise ValueError("Table extraction only supports PDFs")
    
    def _extract_pdf_tables(self, file_path: str) -> list[dict]:
        tables = []
        
        # Method 1: pdfplumber (better for simple tables)
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                page_tables = page.extract_tables()
                for table_idx, table in enumerate(page_tables):
                    tables.append({
                        "page": page_num + 1,
                        "table_idx": table_idx,
                        "data": self._clean_table(table),
                        "method": "pdfplumber"
                    })
        
        # Method 2: Camelot (better for complex tables)
        try:
            camelot_tables = camelot.read_pdf(file_path, pages='all')
            for table in camelot_tables:
                tables.append({
                    "page": table.page,
                    "table_idx": len(tables),
                    "data": table.df.values.tolist(),
                    "method": "camelot",
                    "accuracy": table.parsing_report.get('accuracy', 0)
                })
        except Exception:
            pass  # Fall back to pdfplumber results
        
        return tables
    
    def _clean_table(self, table: list) -> list:
        # Remove None values, strip whitespace
        return [
            [cell.strip() if cell else "" for cell in row]
            for row in table
        ]
```

### Step 2: LLM Table Understanding

```python
# app/services/table_analyzer.py
TABLE_ANALYSIS_PROMPT = """
Analyze this table and extract structured information.

Table from page {page} of document:
{table}

Tasks:
1. Identify what type of table this is (invoice, receipt, report, etc.)
2. Extract key-value pairs (e.g., "Invoice Number: INV-001")
3. Identify line items if present
4. Calculate totals if applicable

Output as JSON.
"""

async def analyze_table(table_data: dict) -> dict:
    prompt = TABLE_ANALYSIS_PROMPT.format(
        page=table_data["page"],
        table=json.dumps(table_data["data"])
    )
    response = await llm.generate(prompt)
    return json.loads(response)
```

**Checkpoint:**
- [ ] Tables extracted from PDFs
- [ ] Multiple methods tried (pdfplumber, Camelot)
- [ ] LLM analyzes table structure

---

## Day 3: Multi-Modal Extraction

**Learning (80 min):**
- Vision LLMs for document understanding
- Combining text + table + image extraction
- Layout analysis

**Build (120 min):**

### Step 1: Vision LLM Integration

```python
# app/services/vision_llm.py
class VisionDocumentAnalyzer:
    def __init__(self):
        self.model = "gpt-4o"  # or Claude-3.5-Sonnet
    
    async def analyze_page(self, image_path: str, text: str = None) -> dict:
        """Analyze a document page using vision + text"""
        
        # Prepare prompt
        prompt = """
Analyze this document page and extract:
1. Document type (invoice, contract, report, etc.)
2. Key entities (dates, amounts, names, etc.)
3. Structure (headers, sections, tables)
4. Confidence score (0-1)

Be specific and accurate.
"""
        
        # Call vision model
        response = await vision_llm.generate(
            prompt=prompt,
            image_path=image_path
        )
        
        # Combine with text extraction if available
        if text:
            response["ocr_text"] = text[:1000]  # Truncate for context
        
        return response
```

### Step 2: Fusion Pipeline

```python
# app/pipelines/multi_modal.py
class MultiModalPipeline:
    def __init__(self):
        self.loader = DocumentLoader()
        self.table_extractor = TableExtractor()
        self.vision_analyzer = VisionDocumentAnalyzer()
    
    async def process(self, file_path: str) -> dict:
        # Load document
        doc = self.loader.load(file_path)
        
        # Extract tables
        tables = self.table_extractor.extract_tables(file_path)
        table_analyses = []
        for table in tables:
            analysis = await analyze_table(table)
            table_analyses.append(analysis)
        
        # Vision analysis (first page or key pages)
        vision_analysis = await self.vision_analyzer.analyze_page(
            doc.image_path,
            doc.text
        )
        
        # Fuse results
        return {
            "document_type": vision_analysis.get("document_type"),
            "text": doc.text,
            "tables": table_analyses,
            "entities": vision_analysis.get("entities"),
            "confidence": vision_analysis.get("confidence"),
            "metadata": {
                "pages": doc.page_count,
                "has_images": doc.has_images,
                "extraction_methods": ["ocr", "pdfplumber", "vision"]
            }
        }
```

**Checkpoint:**
- [ ] Vision model analyzes document images
- [ ] Results fused with text extraction
- [ ] Pipeline processes full document

---

## Day 4: Testing + Evaluation

**Testing (120 min):**

```python
# tests/test_document_intelligence.py
def test_pdf_text_extraction():
    doc = loader.load("tests/fixtures/invoice_text.pdf")
    assert doc.text is not None
    assert "Invoice" in doc.text

def test_pdf_ocr_extraction():
    doc = loader.load("tests/fixtures/scanned_invoice.pdf")
    assert doc.text is not None
    assert len(doc.text) > 50  # Should extract some text

def test_table_extraction():
    tables = extractor.extract_tables("tests/fixtures/invoice.pdf")
    assert len(tables) > 0
    assert any("total" in str(t["data"]).lower() for t in tables)

def test_end_to_end_invoice():
    result = await pipeline.process("tests/fixtures/invoice.pdf")
    assert result["document_type"] == "invoice"
    assert "total" in str(result["tables"]).lower()
    assert result["confidence"] > 0.7

def test_multi_format_support():
    formats = ["invoice.pdf", "receipt.png", "report.tiff"]
    for fmt in formats:
        result = await pipeline.process(f"tests/fixtures/{fmt}")
        assert result is not None
```

**Evaluation (40 min):**

```python
# evaluation/accuracy.py
def evaluate_extraction_accuracy(test_set: list[dict]) -> dict:
    """
    Test set format:
    [{"file": "invoice1.pdf", "expected": {"vendor": "Acme", "total": 100}}, ...]
    """
    results = []
    for test_case in test_set:
        result = await pipeline.process(test_case["file"])
        
        # Compare with expected
        matches = 0
        total = len(test_case["expected"])
        
        for key, expected_value in test_case["expected"].items():
            extracted = extract_value(result, key)
            if extracted and str(extracted).lower() == str(expected_value).lower():
                matches += 1
        
        results.append(matches / total)
    
    return {
        "accuracy": sum(results) / len(results),
        "by_document": results
    }
```

---

## Day 5: Polish + Blog Post

**Polish (80 min):**
- [ ] README with architecture diagram
- [ ] Demo: upload document → see extracted data
- [ ] Deploy to Streamlit Cloud

**Blog Post (120 min):**

Write: "Multi-Modal Document Intelligence: Beyond Simple OCR"

**Outline:**
```markdown
# Multi-Modal Document Intelligence: Beyond Simple OCR

## The Problem
Documents aren't just text. They're layouts, tables, images, and structure.
Traditional OCR misses the forest for the trees.

## Architecture Overview
[Diagram: Document → Loader → OCR + Tables + Vision → Fusion → Structured Output]

## Why Three Extraction Methods?
1. OCR: Raw text extraction
2. Table parsers: Structured data (pdfplumber, Camelot)
3. Vision LLMs: Layout understanding, document classification

Each method has blind spots. Together, they cover each other.

## What Broke During Development
- [Failure from FAILURE-LOG.md: e.g., scanned PDFs failing]
- How you fixed it: [e.g., added OCR fallback]

## Accuracy Results
- Test set: 20 documents
- Overall accuracy: X%
- Best performing: [method]
- Worst performing: [method]

## When to Use This Pattern
- Invoice processing
- Contract analysis
- Research paper parsing
- Form processing

## When NOT to Use This
- Handwritten documents (OCR struggles)
- Highly specialized formats (medical records, legal docs)
- Real-time requirements (vision models are slow)

## Cost Analysis
- OCR: Free (Tesseract) or $X/1000 pages (Cloud Vision)
- Vision LLM: $Y/1000 pages
- Total cost per document: $Z
```

---

## Track B Deliverables

| Item | Complete | Link |
|------|----------|------|
| Multi-modal pipeline | ⬜ | |
| Test suite (5+ tests) | ⬜ | |
| Evaluation results | ⬜ | |
| README with architecture | ⬜ | |
| Demo (upload → extract) | ⬜ | |
| Blog post | ⬜ | |

---

# 🎯 TRACK C: FINE-TUNING SPRINT

## Overview

Learn when to fine-tune vs. RAG vs. prompting, and implement QLoRA fine-tuning of a 7B model on a custom instruction dataset.

**Decision Framework:**
```
┌─────────────────────────────────────┐
│  Do you need model to know facts?   │
├─────────────────────────────────────┤
│  YES → Use RAG                      │
│  NO → Continue                      │
└─────────────────────────────────────┘
         ↓
┌─────────────────────────────────────┐
│  Do you need specific format/style? │
├─────────────────────────────────────┤
│  YES → Fine-tuning may help         │
│  NO → Prompt engineering first      │
└─────────────────────────────────────┘
```

---

## Day 1: Decision Framework + Dataset Prep

**Learning (80 min):**
- When to fine-tune (and when not to)
- QLoRA basics (quantization + LoRA adapters)
- Dataset formats for instruction tuning

**Build (120 min):**

### Step 1: Define Your Use Case

```python
# Choose ONE:
USE_CASE = "customer_support_classifier"  # Classify support tickets
USE_CASE = "medical_qa_style"  # Match medical response style
USE_CASE = "code_reviewer"  # Learn your code review style
USE_CASE = "legal_document_summarizer"  # Specific format for legal summaries
```

### Step 2: Create Dataset

```python
# datasets/{use_case}/raw_data.py
DATASET = [
    {
        "instruction": "Classify this support ticket",
        "input": "My account is locked and I can't login",
        "output": "Category: Account Access | Priority: High | Action: Reset required"
    },
    {
        "instruction": "Classify this support ticket",
        "input": "How do I export my data?",
        "output": "Category: Feature Question | Priority: Low | Action: Documentation link"
    },
    # Add 50-100 examples minimum
]

# Save in Alpaca format
import json
with open("datasets/support/train.json", "w") as f:
    json.dump(DATASET, f, indent=2)
```

### Step 3: Split + Validate

```python
# datasets/prepare.py
from sklearn.model_selection import train_test_split

def prepare_dataset(data: list) -> dict:
    train, test = train_test_split(data, test_size=0.2, random_state=42)
    
    print(f"Train: {len(train)} examples")
    print(f"Test: {len(test)} examples")
    
    # Validate format
    for item in train:
        assert "instruction" in item
        assert "input" in item
        assert "output" in item
    
    return {"train": train, "test": test}

dataset = prepare_dataset(DATASET)
```

**Checkpoint:**
- [ ] Use case defined
- [ ] 50-100 training examples created
- [ ] Train/test split done

---

## Day 2: Model Selection + Environment

**Learning (80 min):**
- Model options (Mistral-7B, Llama-2-7B, etc.)
- QLoRA: Quantized Low-Rank Adaptation
- VRAM requirements

**Build (120 min):**

### Step 1: Setup Environment

```bash
# requirements.txt
torch>=2.0.0
transformers>=4.35.0
peft>=0.6.0
bitsandbytes>=0.41.0
datasets>=2.14.0
accelerate>=0.24.0
```

```bash
pip install -r requirements.txt
```

### Step 2: Load Base Model

```python
# fine_tuning/load_model.py
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch

def load_model(model_name: str = "mistralai/Mistral-7B-Instruct-v0.1"):
    # Quantization config (4-bit)
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
    )
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token
    
    # Load model with quantization
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True
    )
    
    return model, tokenizer

model, tokenizer = load_model()
print(f"Model loaded: {model.config.model_type}")
```

**Checkpoint:**
- [ ] Environment set up
- [ ] Model loads without errors
- [ ] GPU available (or CPU fallback)

---

## Day 3: QLoRA Configuration + Training

**Learning (80 min):**
- LoRA adapters (rank, alpha, dropout)
- Training parameters (epochs, batch size, learning rate)
- Memory optimization

**Build (120 min):**

### Step 1: Configure LoRA

```python
# fine_tuning/lora_config.py
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

def configure_lora(model):
    # Prepare model for k-bit training
    model = prepare_model_for_kbit_training(model)
    
    # LoRA configuration
    lora_config = LoraConfig(
        r=16,  # Rank: 16 is good balance
        lora_alpha=32,  # Alpha: 2x rank is common
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],  # Attention layers
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )
    
    # Apply LoRA
    peft_model = get_peft_model(model, lora_config)
    peft_model.print_trainable_parameters()
    # Output: trainable params: 4,194,304 || all params: 7,241,731,072 || trainable%: 0.0579
    
    return peft_model
```

### Step 2: Training Arguments

```python
# fine_tuning/train.py
from transformers import TrainingArguments
from trl import SFTTrainer

def train(peft_model, tokenizer, train_dataset, eval_dataset):
    training_args = TrainingArguments(
        output_dir="./results",
        num_train_epochs=3,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        weight_decay=0.01,
        logging_steps=10,
        evaluation_strategy="steps",
        eval_steps=50,
        save_steps=100,
        warmup_steps=10,
        max_steps=200,  # For demo; use num_train_epochs for full training
        fp16=True,
    )
    
    trainer = SFTTrainer(
        model=peft_model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        tokenizer=tokenizer,
        dataset_text_field="text",  # Format your data as instruction + input + output
    )
    
    # Train
    trainer.train()
    
    # Save adapter
    peft_model.save_pretrained("./fine_tuned_adapter")
    
    return trainer
```

**Checkpoint:**
- [ ] LoRA configured
- [ ] Training starts without errors
- [ ] Loss decreases (monitor logs)

---

## Day 4: Evaluation + Comparison

**Learning (80 min):**
- Fine-tuning evaluation metrics
- Comparing base vs. fine-tuned models
- When fine-tuning fails

**Build (120 min):**

### Step 1: Load Fine-Tuned Model

```python
# evaluation/load_finetuned.py
from peft import PeftModel

def load_finetuned(base_model, adapter_path):
    finetuned_model = PeftModel.from_pretrained(base_model, adapter_path)
    return finetuned_model
```

### Step 2: Compare Base vs. Fine-Tuned

```python
# evaluation/compare.py
def compare_models(base_model, finetuned_model, tokenizer, test_set: list):
    results = []
    
    for example in test_set:
        prompt = f"Instruction: {example['instruction']}\nInput: {example['input']}\nOutput:"
        
        # Base model
        base_output = generate(base_model, tokenizer, prompt)
        
        # Fine-tuned model
        ft_output = generate(finetuned_model, tokenizer, prompt)
        
        # Compare with expected
        expected = example['output']
        
        results.append({
            "prompt": prompt,
            "expected": expected,
            "base_output": base_output,
            "finetuned_output": ft_output,
            "base_match": base_output.strip() == expected.strip(),
            "ft_match": ft_output.strip() == expected.strip(),
        })
    
    # Summary
    base_accuracy = sum(1 for r in results if r["base_match"]) / len(results)
    ft_accuracy = sum(1 for r in results if r["ft_match"]) / len(results)
    
    print(f"Base model accuracy: {base_accuracy:.2%}")
    print(f"Fine-tuned accuracy: {ft_accuracy:.2%}")
    print(f"Improvement: {(ft_accuracy - base_accuracy):.2%}")
    
    return results
```

### Step 3: Qualitative Analysis

```python
# evaluation/analysis.py
def analyze_results(results: list):
    print("\n=== EXAMPLES WHERE FINE-TUNING HELPED ===\n")
    for r in results:
        if not r["base_match"] and r["ft_match"]:
            print(f"Prompt: {r['prompt'][:100]}...")
            print(f"Expected: {r['expected']}")
            print(f"Base: {r['base_output']}")
            print(f"Fine-tuned: {r['finetuned_output']}")
            print()
    
    print("\n=== EXAMPLES WHERE FINE-TUNING DIDN'T HELP ===\n")
    for r in results:
        if not r["ft_match"]:
            print(f"Prompt: {r['prompt'][:100]}...")
            print(f"Expected: {r['expected']}")
            print(f"Fine-tuned: {r['finetuned_output']}")
            print()
```

**Checkpoint:**
- [ ] Fine-tuned model loads
- [ ] Comparison runs
- [ ] Accuracy improvement measured

---

## Day 5: Decision Framework + Blog Post

**Decision Framework Document (80 min):**

```markdown
# When to Fine-Tune vs. RAG vs. Prompt Engineering

## Decision Tree

### Question 1: Does the model need access to specific facts?
- **YES** → Use RAG
  - Fine-tuning doesn't add factual knowledge reliably
  - RAG lets you update knowledge without retraining
  - Example: "What's our Q3 revenue?" → RAG over financial docs

- **NO** → Continue to Question 2

### Question 2: Do you need a specific format or style?
- **YES** → Fine-tuning may help
  - Consistent output format (JSON, specific structure)
  - Matching a tone/style (medical, legal, brand voice)
  - Example: Always output `{diagnosis, confidence, next_steps}`

- **NO** → Use prompt engineering
  - Zero-shot or few-shot prompting
  - Cheapest, fastest option
  - Example: "Summarize this in 3 bullet points"

### Question 3: Is your task classification or simple transformation?
- **YES** → Fine-tuning is strong choice
  - Classification tasks benefit from fine-tuning
  - Simple transformations (rewrite, reformat)
  - Example: Classify support tickets, extract entities

- **NO** → Reconsider RAG or prompt engineering

## Cost Comparison

| Approach | Setup Time | Inference Cost | Maintenance |
|----------|------------|----------------|-------------|
| Prompt Engineering | Minutes | $ | None |
| RAG | Days-Weeks | $$ | Update docs |
| Fine-Tuning | Days-Weeks | $$ (or $$$ if hosting) | Retrain periodically |

## My Decision for This Project

**Use Case:** [Your use case]

**Decision:** [Fine-tuning / RAG / Prompt Engineering]

**Why:**
1. [Reason 1]
2. [Reason 2]
3. [Reason 3]

**Alternatives Considered:**
- [Alternative 1]: Why not chosen
- [Alternative 2]: Why not chosen
```

**Blog Post (120 min):**

Write: "Fine-Tuning LLMs: What I Learned (And When I Wouldn't Do It)"

**Outline:**
```markdown
# Fine-Tuning LLMs: What I Learned (And When I Wouldn't Do It)

## The Hype vs. Reality
Everyone talks about fine-tuning. Few talk about when NOT to do it.

## My Use Case
[What you tried to accomplish]

## The Decision Framework
[Your decision tree from above]

## Technical Approach: QLoRA
- Why QLoRA (memory efficiency)
- Model choice (Mistral-7B, etc.)
- Dataset size: [X] examples

## Results
- Base model accuracy: X%
- Fine-tuned accuracy: Y%
- Improvement: Z%

## What Surprised Me
- [Surprise 1: e.g., "Small dataset worked better than expected"]
- [Surprise 2: e.g., "Some examples got worse"]

## When I Would Fine-Tune Again
- [Scenario 1]
- [Scenario 2]

## When I Would NOT Fine-Tune
- [Scenario 1: e.g., "Factual Q&A — use RAG"]
- [Scenario 2: e.g., "One-off tasks — prompts are fine"]

## Cost Analysis
- Training: $X (GPU hours)
- Inference: $Y/1000 requests
- vs. API costs: $Z/1000 requests

## Code + Resources
[Links to your code]
```

---

## Track C Deliverables

| Item | Complete | Link |
|------|----------|------|
| Dataset (50-100 examples) | ⬜ | |
| QLoRA fine-tuned model | ⬜ | |
| Evaluation comparison | ⬜ | |
| Decision framework doc | ⬜ | |
| Blog post | ⬜ | |

**Note:** If GPU access is limited, focus on the decision framework and blog post. Run training on Colab Pro or similar.

---

## 📊 TRACK COMPARISON

| Criteria | Track A (NL2SQL) | Track B (Doc Intelligence) | Track C (Fine-Tuning) |
|----------|------------------|---------------------------|----------------------|
| **Job Market Fit** | Enterprise roles | AI startups | ML platform roles |
| **Difficulty** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **GPU Required** | No | No (optional for vision) | Yes (or Colab) |
| **Portfolio Impact** | High (demos well) | High (visual + practical) | Medium (harder to demo) |
| **Time to Complete** | 4-5 days | 4-5 days | 5-6 days |
| **Best For** | Backend-focused AI engineers | Full-stack AI engineers | Specialized ML roles |

---

## ✅ WEEK 16 CHECKLIST

**All Tracks:**
- [ ] Core functionality working
- [ ] Tests written and passing
- [ ] README with architecture diagram
- [ ] Demo recorded (2 min)
- [ ] Blog post published
- [ ] FAILURE-LOG.md updated
- [ ] COST-LOG.md updated

**Checkpoint Questions (Answer before Week 17):**
1. Why did you choose this track?
2. What was the hardest technical challenge?
3. How would you productionize this?
4. When would you NOT use this approach?
5. What would you do differently with more time?

---

**Remember:** Specialization is about depth, not breadth. One deep project beats three shallow ones.

**Choose wisely. Build deeply. Ship confidently.** 🚀

**Last Updated:** March 8, 2026
