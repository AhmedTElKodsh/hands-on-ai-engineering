#!/usr/bin/env python3
"""
Verification Script for Chapter 10: Streaming Responses

Tests Generator logic and Response Reconstruction (P6).
Includes tests for Project 3 (Smart Buffer), Project 4 (Progress Bar), and Project 5 (Stream Recorder).
"""

import sys
import time
import json
import os
from typing import Generator

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_test(name, passed, details=""):
    status = f"{Colors.GREEN}✓ PASS{Colors.RESET}" if passed else f"{Colors.RED}✗ FAIL{Colors.RESET}"
    print(f"{status} - {name}")
    if details: print(f"  {details}")

# --- Test 1: Generator Logic ---
def test_generator_basics():
    """Verify yield behavior"""
    def simple_gen():
        yield "Part 1"
        yield "Part 2"
    
    try:
        gen = simple_gen()
        results = list(gen)
        assert results == ["Part 1", "Part 2"]
        print_test("Generator Basics", True, "Yields multiple values correctly")
        return True
    except Exception as e:
        print_test("Generator Basics", False, str(e))
        return False

# --- Test 2: Response Reconstruction (P6) ---
def test_response_reconstruction():
    """Verify that chunks can be joined back to original"""
    expected = "Hello from the LLM stream!"
    chunks = ["Hello ", "from ", "the ", "LLM ", "stream!"]

    try:
        reconstructed = "".join(chunks)
        assert reconstructed == expected
        print_test("Response Reconstruction (P6)", True, "Chunks reconstructed perfectly")
        return True
    except Exception as e:
        print_test("Response Reconstruction (P6)", False, str(e))
        return False

# --- Test 3: Smart Buffer (Project 3) ---
def test_smart_buffer():
    """Test Smart Buffer sentence detection logic"""
    try:
        class SmartBuffer:
            def __init__(self):
                self.buffer = ""
                self.completed_sentences = []

            def add_chunk(self, chunk: str) -> list:
                """Add chunk and return completed sentences"""
                self.buffer += chunk
                sentences = []

                # Check for sentence endings
                while any(self.buffer.find(end) != -1 for end in ['.', '!', '?']):
                    # Find first sentence ending
                    endings = [(self.buffer.find(c), c) for c in ['.', '!', '?'] if self.buffer.find(c) != -1]
                    if not endings:
                        break

                    pos, _ = min(endings)
                    # Extract sentence (including punctuation)
                    sentence = self.buffer[:pos+1].strip()
                    if sentence:
                        sentences.append(sentence)

                    # Keep remaining buffer
                    self.buffer = self.buffer[pos+1:].strip()

                return sentences

            def flush(self) -> str:
                """Get remaining buffered content"""
                result = self.buffer
                self.buffer = ""
                return result

        # Test with streaming chunks
        buffer = SmartBuffer()
        chunks = [
            "Hello", ", how are", " you today", "? I'm here",
            " to help", ". What can I", " do for", " you?"
        ]

        all_sentences = []
        for chunk in chunks:
            sentences = buffer.add_chunk(chunk)
            all_sentences.extend(sentences)

        # Check for remaining content
        remaining = buffer.flush()

        # Verify correct sentence detection
        assert len(all_sentences) >= 1, "Should detect at least 1 complete sentence"
        assert "Hello, how are you today?" in all_sentences[0], "First sentence should be complete"

        # Verify buffer logic
        assert any("help" in s for s in all_sentences), "Should detect sentence with 'help'"

        print_test("Smart Buffer (Project 3)", True,
                  f"Detected {len(all_sentences)} sentences, remaining: {len(remaining)} chars")
        return True
    except Exception as e:
        print_test("Smart Buffer (Project 3)", False, str(e))
        return False

# --- Test 4: Progress Bar (Project 4) ---
def test_progress_bar():
    """Test Progress Bar calculation logic"""
    try:
        class ProgressBar:
            def __init__(self, total_expected: int = 100):
                self.total_expected = total_expected
                self.current_tokens = 0
                self.start_time = time.time()
                self.updates = []

            def update(self, tokens: int):
                """Update progress"""
                self.current_tokens += tokens
                elapsed = time.time() - self.start_time

                percent = min(100, (self.current_tokens / self.total_expected) * 100)
                tokens_per_sec = self.current_tokens / elapsed if elapsed > 0 else 0

                self.updates.append({
                    "tokens": self.current_tokens,
                    "percent": percent,
                    "elapsed": elapsed,
                    "rate": tokens_per_sec
                })

            def get_final_stats(self) -> dict:
                """Get final statistics"""
                elapsed = time.time() - self.start_time
                return {
                    "total_tokens": self.current_tokens,
                    "duration": elapsed,
                    "rate": self.current_tokens / elapsed if elapsed > 0 else 0
                }

        # Test progress tracking
        progress = ProgressBar(total_expected=100)

        # Simulate streaming with different chunk sizes
        chunk_sizes = [10, 15, 20, 25, 30]
        for size in chunk_sizes:
            progress.update(size)
            time.sleep(0.01)  # Small delay

        stats = progress.get_final_stats()

        # Verify tracking
        assert progress.current_tokens == sum(chunk_sizes), "Should track all tokens"
        assert progress.current_tokens == 100, "Total should be 100"
        assert len(progress.updates) == 5, "Should have 5 updates"

        # Verify percentage calculation
        final_update = progress.updates[-1]
        assert final_update["percent"] == 100, "Should reach 100%"

        # Verify rate calculation
        assert stats["rate"] > 0, "Rate should be positive"

        print_test("Progress Bar (Project 4)", True,
                  f"Tracked {stats['total_tokens']} tokens in {stats['duration']:.2f}s ({stats['rate']:.0f} tok/s)")
        return True
    except Exception as e:
        print_test("Progress Bar (Project 4)", False, str(e))
        return False

# --- Test 5: Stream Recorder (Project 5) ---
def test_stream_recorder():
    """Test Stream Recorder capture and replay logic"""
    try:
        class StreamRecorder:
            def __init__(self):
                self.recording = []
                self.start_time = None

            def start_recording(self):
                """Initialize recording"""
                self.recording = []
                self.start_time = time.time()

            def record_chunk(self, chunk: str):
                """Record chunk with timestamp"""
                if self.start_time is None:
                    self.start_recording()

                timestamp = time.time() - self.start_time
                self.recording.append({
                    "chunk": chunk,
                    "timestamp": timestamp,
                    "length": len(chunk)
                })

            def save_to_file(self, filename: str):
                """Save recording to JSON"""
                metadata = {
                    "total_duration": self.recording[-1]["timestamp"] if self.recording else 0,
                    "total_chunks": len(self.recording),
                    "total_length": sum(r["length"] for r in self.recording)
                }

                data = {
                    "metadata": metadata,
                    "chunks": self.recording
                }

                with open(filename, "w") as f:
                    json.dump(data, f, indent=2)

            def replay(self, filename: str, speed: float = 1.0) -> Generator[str, None, None]:
                """Replay recorded stream"""
                with open(filename, "r") as f:
                    data = json.load(f)

                prev_timestamp = 0
                for event in data["chunks"]:
                    delay = (event["timestamp"] - prev_timestamp) / speed
                    time.sleep(delay)
                    prev_timestamp = event["timestamp"]
                    yield event["chunk"]

        # Test recorder
        recorder = StreamRecorder()
        recorder.start_recording()

        # Record some chunks
        test_chunks = ["Hello", " world", "!", " Testing", " recorder", "."]
        for chunk in test_chunks:
            recorder.record_chunk(chunk)
            time.sleep(0.01)  # Small delay between chunks

        # Save to temp file
        test_file = "test_recording.json"
        recorder.save_to_file(test_file)

        # Verify file exists and is valid JSON
        assert os.path.exists(test_file), "Recording file should exist"

        with open(test_file, "r") as f:
            data = json.load(f)

        # Verify structure
        assert "metadata" in data, "Should have metadata"
        assert "chunks" in data, "Should have chunks"
        assert data["metadata"]["total_chunks"] == len(test_chunks), "Should record all chunks"
        assert data["metadata"]["total_length"] == sum(len(c) for c in test_chunks)

        # Test replay
        replayed = []
        for chunk in recorder.replay(test_file, speed=10.0):  # Fast replay for testing
            replayed.append(chunk)

        # Verify replay
        assert replayed == test_chunks, "Replay should match original"

        # Cleanup
        os.remove(test_file)

        print_test("Stream Recorder (Project 5)", True,
                  f"Recorded {len(test_chunks)} chunks, replay successful")
        return True
    except Exception as e:
        # Cleanup on error
        if os.path.exists("test_recording.json"):
            os.remove("test_recording.json")
        print_test("Stream Recorder (Project 5)", False, str(e))
        return False

def main():
    print(f"\n{Colors.BOLD}Chapter 10 Verification{Colors.RESET}")
    print("="*60)

    tests = [
        test_generator_basics,
        test_response_reconstruction,
        test_smart_buffer,
        test_progress_bar,
        test_stream_recorder
    ]

    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"Test crashed: {e}")
            results.append(False)
        print()

    passed = sum(1 for r in results if r)
    total = len(results)

    print("="*60)
    print(f"Passed: {passed}/{total}")

    if passed == total:
        print(f"\n{Colors.GREEN}✅ All Chapter 10 tests passed!{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}⚠️ Some tests failed.{Colors.RESET}")

if __name__ == "__main__":
    main()
