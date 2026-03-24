#!/usr/bin/env python3
"""
Visualization for Chapter 10: Streaming Responses

Creates plots for:
1. Streaming Throughput (tokens/second)
2. Buffer Efficiency Comparison
3. Response Time Distribution
"""

import matplotlib.pyplot as plt
import numpy as np

def plot_streaming_throughput():
    """Plot streaming throughput over time"""
    time_seconds = np.linspace(0, 10, 100)
    # Simulate streaming throughput with some variance
    throughput = 25 + 5 * np.sin(time_seconds / 2) + np.random.normal(0, 1, 100)

    plt.figure(figsize=(12, 6))
    plt.plot(time_seconds, throughput, linewidth=2, color='blue', alpha=0.7)
    plt.fill_between(time_seconds, throughput, alpha=0.3, color='blue')

    # Add average line
    avg_throughput = np.mean(throughput)
    plt.axhline(y=avg_throughput, color='red', linestyle='--',
               label=f'Average: {avg_throughput:.1f} tok/s', linewidth=2)

    plt.title('Streaming Throughput Over Time', fontsize=14, fontweight='bold')
    plt.xlabel('Time (seconds)', fontsize=12)
    plt.ylabel('Tokens per Second', fontsize=12)
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    return plt.gcf()

def plot_buffer_comparison():
    """Compare buffered vs unbuffered streaming"""
    categories = ['Unbuffered\nStreaming', 'Smart Buffer\n(Sentences)', 'Fixed Buffer\n(10 tokens)']
    readability = [60, 95, 75]  # Subjective readability score
    latency_ms = [0, 150, 100]  # Average latency in milliseconds

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Readability comparison
    bars1 = ax1.bar(categories, readability, color=['red', 'green', 'orange'],
                   alpha=0.7, edgecolor='black')
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontweight='bold')

    ax1.set_title('Readability Score (Higher = Better)', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Readability Score', fontsize=12)
    ax1.set_ylim(0, 100)
    ax1.grid(axis='y', alpha=0.3)

    # Latency comparison
    bars2 = ax2.bar(categories, latency_ms, color=['green', 'red', 'orange'],
                   alpha=0.7, edgecolor='black')
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}ms',
                ha='center', va='bottom', fontweight='bold')

    ax2.set_title('Average Latency (Lower = Better)', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Latency (ms)', fontsize=12)
    ax2.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    return fig

def plot_response_time_distribution():
    """Plot response time distribution for different chunk sizes"""
    # Simulate response time data
    np.random.seed(42)
    small_chunks = np.random.normal(50, 10, 100)  # Mean 50ms, std 10ms
    medium_chunks = np.random.normal(100, 20, 100)
    large_chunks = np.random.normal(200, 40, 100)

    plt.figure(figsize=(12, 6))

    # Create histogram
    bins = np.linspace(0, 300, 30)
    plt.hist(small_chunks, bins=bins, alpha=0.5, label='Small chunks (1-5 tokens)',
            color='green', edgecolor='black')
    plt.hist(medium_chunks, bins=bins, alpha=0.5, label='Medium chunks (5-10 tokens)',
            color='orange', edgecolor='black')
    plt.hist(large_chunks, bins=bins, alpha=0.5, label='Large chunks (10+ tokens)',
            color='red', edgecolor='black')

    plt.title('Response Time Distribution by Chunk Size', fontsize=14, fontweight='bold')
    plt.xlabel('Response Time (ms)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    return plt.gcf()

def main():
    print("Generating Chapter 10 Visualizations...")

    fig1 = plot_streaming_throughput()
    plt.savefig('ch10_streaming_throughput.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: ch10_streaming_throughput.png")

    fig2 = plot_buffer_comparison()
    plt.savefig('ch10_buffer_comparison.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: ch10_buffer_comparison.png")

    fig3 = plot_response_time_distribution()
    plt.savefig('ch10_response_time_distribution.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: ch10_response_time_distribution.png")

    print("\n📊 All Chapter 10 plots generated successfully!")
    plt.show()

if __name__ == "__main__":
    main()
