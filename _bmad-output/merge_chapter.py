#!/usr/bin/env python3
"""Merge chapter continuation into main enhanced file"""

# Read continuation
with open('_bmad-output/chapter-09-continuation.md', 'r', encoding='utf-8') as f:
    continuation = f.read()

# Append to main file
with open('curriculum/chapters/phase-1-llm-fundamentals/chapter-09-prompt-engineering-basics-ENHANCED.md', 'a', encoding='utf-8') as f:
    f.write('\n' + continuation)

print("✅ Chapter 9 continuation merged successfully!")
