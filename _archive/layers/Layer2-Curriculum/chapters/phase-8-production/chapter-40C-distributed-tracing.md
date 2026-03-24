# Chapter 40C: Distributed Tracing & Cost Analytics — Following the Breadcrumbs

<!--
METADATA
Phase: Phase 8: Production
Time: 1.5 hours (30 minutes reading + 60 minutes hands-on)
Difficulty: ⭐⭐⭐⭐
Type: Implementation / Advanced
Prerequisites: Chapter 40B (Phoenix), Chapter 6B (Error Handling)
Builds Toward: Chapter 54 (Complete System)
Correctness Properties: P84 (Correlation ID propagation), P85 (Cost attribution accuracy)
-->

## ☕ Coffee Shop Intro: The Relay Race

Imagine a relay race. Runner A passes the baton to Runner B, then to Runner C.

If Runner C is slow, the whole team loses. But if you only clock the *team's* total time, you don't know who was slow. Was A tired? Did B trip? Did C stop for a snack?

In modern software, your AI is part of a relay team:
1.  **Frontend** (Runner A) receives user click.
2.  **Backend** (Runner B) processes auth.
3.  **AI Service** (Runner C) generates text.

**Distributed Tracing** is the baton. It carries a specific ID (`trace_id`) from A to B to C, so you can see exactly how long each leg took and where the baton was dropped.

---

## 🔍 The 3-Layer Dive

### Layer 1: Local Tracing (Phoenix)
Great for seeing inside *one* Python process. (What we did in Ch 40B).
*   **Limit**: If your Python app calls an external API, the trace stops at the border.

### Layer 2: Correlation IDs
Passing a unique ID (`X-Request-ID: 123`) in HTTP headers.
*   **Pros**: Links logs together.
*   **Cons**: You have to manually parse logs from 3 different servers to stitch the story.

### Layer 3: OpenTelemetry (OTel)
The industry standard for distributed tracing.
*   **How it works**: Auto-generates IDs, passes them in headers, and sends data to a central collector (like Jaeger, Honeycomb, or Phoenix).
*   **Result**: One timeline showing Frontend -> Backend -> AI -> Database -> AI -> Frontend.

---

## 🛠️ Implementation Guide: Passing the Baton

We'll use **OpenTelemetry** to instrument a function and simulate a distributed call.

### Step 1: Setup

```bash
pip install opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp
```

### Step 2: Setting up the Tracer

This boilerplate is required to tell Python "Start recording traces and print them to console".

```python
# trace_setup.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

def configure_tracer():
    # 1. Create a provider
    provider = TracerProvider()
    
    # 2. Tell it where to send data (Console for now)
    processor = SimpleSpanProcessor(ConsoleSpanExporter())
    provider.add_span_processor(processor)
    
    # 3. Set as global default
    trace.set_tracer_provider(provider)
    
    return trace.get_tracer(__name__)

tracer = configure_tracer()
```

### Step 3: Manual Instrumentation (The "With" Block)

You wrap code in `start_as_current_span`.

```python
import time

def process_user_request(user_id):
    with tracer.start_as_current_span("parent_request") as parent:
        parent.set_attribute("user.id", user_id)
        print("Received request...")
        
        # Simulate calling the AI service
        call_ai_service("Hello")

def call_ai_service(prompt):
    # This span is automatically a CHILD of "parent_request"
    with tracer.start_as_current_span("ai_generation") as child:
        child.set_attribute("prompt.length", len(prompt))
        print("Generating AI response...")
        time.sleep(0.5) # Simulate work

if __name__ == "__main__":
    process_user_request("user_123")
```

**Output**: You'll see structured JSON logs showing `parent_request` taking ~0.5s, containing `ai_generation`.

---

## 💰 Cost Analytics: The "Who Pays?" Question

In a startup, you need to know: "How much is User 123 costing us?"
With Tracing, you simply add cost as an **attribute** to the span.

```python
def calculate_cost(tokens):
    cost = tokens * 0.00002
    # Add to current active span
    current_span = trace.get_current_span()
    current_span.set_attribute("cost.usd", cost)
```

Now you can aggregate all spans where `user.id = 123` and sum `cost.usd`.

---

## 🧪 Correctness Properties (Testing The Baton)

| Property | Description |
|----------|-------------|
| **P84: Correlation ID Propagation** | If Service A calls Service B, B must receive A's Trace ID. |
| **P85: Cost Attribution** | Sum(User Costs) must equal Total Bill (within margin). |

### Hypothesis Test Example

```python
from hypothesis import given, strategies as st
# Conceptual test

def test_p84_propagation():
    """P84: Context must be preserved across calls."""
    trace_id_a = "abc-123"
    
    # Simulate HTTP call with headers
    headers = {"traceparent": f"00-{trace_id_a}-..."}
    
    # Simulate receiving in Service B
    trace_id_b = extract_trace_id(headers)
    
    assert trace_id_a == trace_id_b
```

---

## ✍️ Try This! (Hands-On Exercises)

### Exercise 1: The decorator
Writing `with tracer.start...` is tedious. Write a python decorator `@traced` that automatically creates a span with the function's name.

### Exercise 2: Budget Alert
Write a function that checks the current span's accumulated cost. If it exceeds $0.01, print a "BUDGET ALARM" warning.

---

## ✅ Verification Script

Create `verify_ch40c.py`.

```python
"""
Verification script for Chapter 40C: Distributed Tracing
"""
import sys
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

def verify_opentelemetry():
    print("1. Configuring OpenTelemetry...")
    try:
        provider = TracerProvider()
        # Use ConsoleExporter to verify we can actually output data
        exporter = ConsoleSpanExporter()
        processor = SimpleSpanProcessor(exporter)
        provider.add_span_processor(processor)
        trace.set_tracer_provider(provider)
        tracer = trace.get_tracer("verification_tracer")
    except Exception as e:
        print(f"❌ Configuration failed: {e}")
        sys.exit(1)

    print("2. Creating a Span...")
    try:
        with tracer.start_as_current_span("verification_span") as span:
            span.set_attribute("test.status", "passing")
            print("   Span active.")
            current = trace.get_current_span()
            if current != span:
                raise Exception("Context context not set correctly")
    except Exception as e:
        print(f"❌ Span creation failed: {e}")
        sys.exit(1)

    print("✅ OpenTelemetry functions correctly.")

if __name__ == "__main__":
    verify_opentelemetry()
```

---

## 📝 Summary & Key Takeaways

1.  **Distributed Tracing**: The only way to debug microservices or multi-stage AI pipelines.
2.  **OpenTelemetry (OTel)**: The universal standard. Learn it once, use it with Jaeger, Phoenix, Datadog, etc.
3.  **Spans**: Units of work. They have a start, end, and attributes.
4.  **Trace Context**: The "Baton" passed between functions or servers.
5.  **Cost Analytics**: Don't guess costs. Tag every span with `cost` and `user_id`.
6.  **Attributes**: Key-value pairs you attach to spans (e.g., `model="gpt-4"`, `tokens=50`).
7.  **Overhead**: OTel is lightweight, designed for production use.

**Key Insight**: You cannot optimize what you cannot measure. Distributed tracing gives you the granular measurement needed to turn AI from a "science project" into a "business".

---

## 🔜 What's Next?

We've mastered Observation. Now let's tackle Coordination. In **Chapter 43**, we'll start **Phase 9: Multi-Agent Systems**, where multiple AI agents work together to solve problems too big for one model.
