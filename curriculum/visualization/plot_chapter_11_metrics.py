#!/usr/bin/env python3
"""
Visualization for Chapter 11: Structured Output

Creates plots for:
1. Schema Validation Pass Rates
2. Extraction Accuracy by Complexity
3. Format Fallback Success Rates
"""

import matplotlib.pyplot as plt
import numpy as np

def plot_validation_pass_rates():
    """Plot validation pass rates for different data types"""
    data_types = ['Simple\nFields', 'Nested\nObjects', 'Lists/Arrays', 'Complex\nConstraints', 'Business\nRules']
    pass_rates = [98, 92, 87, 78, 65]
    colors = ['green', 'green', 'orange', 'orange', 'red']

    plt.figure(figsize=(10, 6))
    bars = plt.bar(data_types, pass_rates, color=colors, alpha=0.7, edgecolor='black')

    # Add threshold line
    plt.axhline(y=85, color='red', linestyle='--', alpha=0.5, label='Target: 85%')

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}%',
                ha='center', va='bottom', fontweight='bold')

    plt.title('Schema Validation Pass Rates by Complexity', fontsize=14, fontweight='bold')
    plt.ylabel('Pass Rate (%)', fontsize=12)
    plt.ylim(0, 105)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    return plt.gcf()

def plot_extraction_accuracy():
    """Plot extraction accuracy vs document complexity"""
    complexity_scores = np.array([1, 2, 3, 4, 5])
    json_accuracy = np.array([95, 92, 88, 82, 75])
    csv_accuracy = np.array([90, 85, 78, 70, 60])
    yaml_accuracy = np.array([88, 82, 75, 65, 55])

    plt.figure(figsize=(12, 6))

    plt.plot(complexity_scores, json_accuracy, marker='o', linewidth=2,
            markersize=8, label='JSON Format', color='green')
    plt.plot(complexity_scores, csv_accuracy, marker='s', linewidth=2,
            markersize=8, label='CSV Format', color='orange')
    plt.plot(complexity_scores, yaml_accuracy, marker='^', linewidth=2,
            markersize=8, label='YAML Format', color='blue')

    # Add shaded regions for complexity levels
    plt.axvspan(1, 2, alpha=0.1, color='green', label='Easy')
    plt.axvspan(2, 4, alpha=0.1, color='yellow')
    plt.axvspan(4, 5, alpha=0.1, color='red')

    plt.title('Extraction Accuracy vs Document Complexity', fontsize=14, fontweight='bold')
    plt.xlabel('Document Complexity (1=Simple, 5=Very Complex)', fontsize=12)
    plt.ylabel('Extraction Accuracy (%)', fontsize=12)
    plt.xticks(complexity_scores)
    plt.ylim(50, 100)
    plt.legend(loc='upper right')
    plt.grid(alpha=0.3)
    plt.tight_layout()
    return plt.gcf()

def plot_fallback_success():
    """Plot fallback strategy success rates"""
    scenarios = ['Primary\nSuccess', 'Fallback to\nSecondary', 'Fallback to\nTertiary', 'All\nFailed']
    percentages = [75, 18, 5, 2]
    colors = ['green', 'orange', 'red', 'darkred']
    explode = (0.1, 0, 0, 0)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Pie chart
    wedges, texts, autotexts = ax1.pie(percentages, labels=scenarios, autopct='%1.1f%%',
                                        colors=colors, explode=explode, startangle=90,
                                        textprops={'fontweight': 'bold'})
    ax1.set_title('Format Fallback Distribution', fontsize=14, fontweight='bold')

    # Bar chart for recovery metrics
    recovery_types = ['Immediate\nSuccess', 'Recovered\nvia Fallback', 'Failed\n(No Recovery)']
    success_rates = [75, 23, 2]
    bars = ax2.bar(recovery_types, success_rates,
                  color=['green', 'orange', 'red'], alpha=0.7, edgecolor='black')

    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}%',
                ha='center', va='bottom', fontweight='bold')

    ax2.set_title('Overall Recovery Success', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Success Rate (%)', fontsize=12)
    ax2.set_ylim(0, 85)
    ax2.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    return fig

def main():
    print("Generating Chapter 11 Visualizations...")

    fig1 = plot_validation_pass_rates()
    plt.savefig('ch11_validation_pass_rates.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: ch11_validation_pass_rates.png")

    fig2 = plot_extraction_accuracy()
    plt.savefig('ch11_extraction_accuracy.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: ch11_extraction_accuracy.png")

    fig3 = plot_fallback_success()
    plt.savefig('ch11_fallback_success.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: ch11_fallback_success.png")

    print("\n📊 All Chapter 11 plots generated successfully!")
    plt.show()

if __name__ == "__main__":
    main()
