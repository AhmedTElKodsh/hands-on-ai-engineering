#!/usr/bin/env python3
"""
Visualization for Chapter 9: Prompt Engineering Basics

Creates plots for:
1. Prompt Validator Score Distribution
2. A/B Test Cost Comparison
3. Few-Shot Performance by Example Count
"""

import matplotlib.pyplot as plt
import numpy as np

# Sample data (students would replace with their actual results)
def plot_prompt_validator_scores():
    """Plot prompt quality score distribution"""
    prompts = ['Vague\nPrompt', 'Missing\nFormat', 'Ambiguous\nTerms', 'Good\nPrompt 1', 'Good\nPrompt 2']
    scores = [40, 55, 75, 95, 100]
    colors = ['red' if s < 70 else 'orange' if s < 85 else 'green' for s in scores]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(prompts, scores, color=colors, alpha=0.7, edgecolor='black')

    # Add threshold lines
    plt.axhline(y=70, color='red', linestyle='--', alpha=0.5, label='Fail threshold (70)')
    plt.axhline(y=85, color='orange', linestyle='--', alpha=0.5, label='Good threshold (85)')

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontweight='bold')

    plt.title('Prompt Quality Score Distribution', fontsize=14, fontweight='bold')
    plt.xlabel('Prompt Type', fontsize=12)
    plt.ylabel('Quality Score (0-100)', fontsize=12)
    plt.ylim(0, 105)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    return plt.gcf()

def plot_ab_test_costs():
    """Plot A/B test cost comparison"""
    prompt_types = ['Simple\nInstruction', 'Few-Shot\n(3 examples)', 'Constrained\nwith Rules']
    costs = [0.0002, 0.0005, 0.0003]  # Dollars
    tokens = [100, 250, 180]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Cost comparison
    bars1 = ax1.bar(prompt_types, costs, color=['green', 'orange', 'blue'], alpha=0.7, edgecolor='black')
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'${height:.4f}',
                ha='center', va='bottom', fontweight='bold')

    ax1.set_title('A/B Test: Cost per API Call', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Cost (USD)', fontsize=12)
    ax1.grid(axis='y', alpha=0.3)

    # Token usage
    bars2 = ax2.bar(prompt_types, tokens, color=['green', 'orange', 'blue'], alpha=0.7, edgecolor='black')
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom', fontweight='bold')

    ax2.set_title('Token Usage Comparison', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Tokens Used', fontsize=12)
    ax2.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    return fig

def plot_few_shot_performance():
    """Plot few-shot performance by example count"""
    example_counts = [0, 1, 2, 3, 5]
    accuracy = [45, 65, 78, 92, 94]  # Sample accuracy percentages

    plt.figure(figsize=(10, 6))
    plt.plot(example_counts, accuracy, marker='o', linewidth=2, markersize=10,
            color='blue', label='Classification Accuracy')

    # Fill area under curve
    plt.fill_between(example_counts, accuracy, alpha=0.3, color='blue')

    # Add value labels
    for x, y in zip(example_counts, accuracy):
        plt.text(x, y + 2, f'{y}%', ha='center', fontweight='bold')

    plt.title('Few-Shot Learning: Performance vs Example Count', fontsize=14, fontweight='bold')
    plt.xlabel('Number of Examples', fontsize=12)
    plt.ylabel('Accuracy (%)', fontsize=12)
    plt.ylim(0, 100)
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    return plt.gcf()

def main():
    print("Generating Chapter 9 Visualizations...")

    # Create plots
    fig1 = plot_prompt_validator_scores()
    plt.savefig('ch09_prompt_validator_scores.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: ch09_prompt_validator_scores.png")

    fig2 = plot_ab_test_costs()
    plt.savefig('ch09_ab_test_comparison.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: ch09_ab_test_comparison.png")

    fig3 = plot_few_shot_performance()
    plt.savefig('ch09_few_shot_performance.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: ch09_few_shot_performance.png")

    print("\n📊 All Chapter 9 plots generated successfully!")
    print("   Use these plots to visualize your prompt engineering results.")

    # Show all plots
    plt.show()

if __name__ == "__main__":
    main()
