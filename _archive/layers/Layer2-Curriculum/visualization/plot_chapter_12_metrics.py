#!/usr/bin/env python3
"""
Visualization for Chapter 12: Error Handling & Retries

Creates plots for:
1. Circuit Breaker State Timeline
2. Rate Limiter Token Bucket Behavior
3. Resilience Dashboard Health Metrics
"""

import matplotlib.pyplot as plt
import numpy as np

def plot_circuit_breaker_timeline():
    """Plot circuit breaker state transitions over time"""
    # Simulate circuit breaker states over time
    time_points = np.arange(0, 100, 1)
    states = []
    state_map = {'CLOSED': 0, 'OPEN': 1, 'HALF_OPEN': 0.5}

    # Simulate state transitions
    for t in time_points:
        if t < 20:
            states.append(state_map['CLOSED'])
        elif t < 30:
            states.append(state_map['OPEN'])  # Failures triggered circuit
        elif t < 35:
            states.append(state_map['HALF_OPEN'])  # Testing recovery
        elif t < 60:
            states.append(state_map['CLOSED'])  # Recovered
        elif t < 70:
            states.append(state_map['OPEN'])  # Another failure
        elif t < 75:
            states.append(state_map['HALF_OPEN'])
        else:
            states.append(state_map['CLOSED'])

    plt.figure(figsize=(14, 6))
    plt.fill_between(time_points, states, step='post', alpha=0.3, color='blue')
    plt.step(time_points, states, where='post', linewidth=2, color='blue', label='Circuit State')

    # Add state labels
    plt.axhline(y=0, color='green', linestyle='--', alpha=0.5, linewidth=1)
    plt.axhline(y=0.5, color='orange', linestyle='--', alpha=0.5, linewidth=1)
    plt.axhline(y=1, color='red', linestyle='--', alpha=0.5, linewidth=1)

    plt.yticks([0, 0.5, 1], ['CLOSED\n(Healthy)', 'HALF_OPEN\n(Testing)', 'OPEN\n(Failing)'])
    plt.title('Circuit Breaker State Timeline', fontsize=14, fontweight='bold')
    plt.xlabel('Time (seconds)', fontsize=12)
    plt.ylabel('Circuit State', fontsize=12)
    plt.grid(axis='x', alpha=0.3)
    plt.legend()
    plt.tight_layout()
    return plt.gcf()

def plot_rate_limiter_tokens():
    """Plot rate limiter token bucket behavior"""
    time_points = np.linspace(0, 10, 100)
    burst_size = 5
    refill_rate = 2  # tokens per second

    # Simulate token availability
    tokens = []
    current_tokens = burst_size
    last_time = 0

    for t in time_points:
        # Refill tokens
        elapsed = t - last_time
        current_tokens = min(burst_size, current_tokens + refill_rate * elapsed)

        # Simulate requests at certain intervals
        if int(t * 2) % 3 == 0:  # Request every 1.5 seconds
            current_tokens = max(0, current_tokens - 1)

        tokens.append(current_tokens)
        last_time = t

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    # Token availability over time
    ax1.plot(time_points, tokens, linewidth=2, color='blue', label='Available Tokens')
    ax1.fill_between(time_points, tokens, alpha=0.3, color='blue')
    ax1.axhline(y=burst_size, color='red', linestyle='--', label=f'Burst Limit ({burst_size})', linewidth=2)
    ax1.axhline(y=1, color='orange', linestyle='--', label='Warning (1 token)', linewidth=1)

    ax1.set_title('Rate Limiter: Token Bucket Behavior', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Time (seconds)', fontsize=12)
    ax1.set_ylabel('Available Tokens', fontsize=12)
    ax1.legend()
    ax1.grid(alpha=0.3)

    # Request handling visualization
    request_times = np.array([0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0])
    allowed = np.array([1, 1, 1, 1, 1, 0, 1, 1, 0, 1])  # 1=allowed, 0=rate limited

    colors = ['green' if a == 1 else 'red' for a in allowed]
    ax2.scatter(request_times, allowed, c=colors, s=200, alpha=0.7, edgecolors='black', linewidths=2)

    ax2.set_title('Request Handling: Allowed vs Rate Limited', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Time (seconds)', fontsize=12)
    ax2.set_ylabel('Request Status', fontsize=12)
    ax2.set_yticks([0, 1])
    ax2.set_yticklabels(['Rate Limited', 'Allowed'])
    ax2.set_ylim(-0.5, 1.5)
    ax2.grid(axis='x', alpha=0.3)

    plt.tight_layout()
    return fig

def plot_resilience_dashboard():
    """Plot resilience dashboard health metrics"""
    endpoints = ['OpenAI\nAPI', 'Anthropic\nAPI', 'Groq\nAPI', 'Local\nModel']
    success_rates = [95, 92, 88, 99]
    avg_latency = [120, 150, 80, 50]  # milliseconds
    circuit_states = ['CLOSED', 'CLOSED', 'OPEN', 'CLOSED']

    fig = plt.figure(figsize=(15, 10))
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

    # Success rates
    ax1 = fig.add_subplot(gs[0, 0])
    colors = ['green' if sr >= 95 else 'orange' if sr >= 90 else 'red' for sr in success_rates]
    bars1 = ax1.bar(endpoints, success_rates, color=colors, alpha=0.7, edgecolor='black')

    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}%',
                ha='center', va='bottom', fontweight='bold')

    ax1.axhline(y=95, color='green', linestyle='--', alpha=0.5, label='Excellent (95%)')
    ax1.axhline(y=90, color='orange', linestyle='--', alpha=0.5, label='Good (90%)')
    ax1.set_title('Success Rates by Endpoint', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Success Rate (%)', fontsize=10)
    ax1.set_ylim(0, 105)
    ax1.legend(fontsize=8)
    ax1.grid(axis='y', alpha=0.3)

    # Average latency
    ax2 = fig.add_subplot(gs[0, 1])
    colors2 = ['green' if lat < 100 else 'orange' if lat < 150 else 'red' for lat in avg_latency]
    bars2 = ax2.bar(endpoints, avg_latency, color=colors2, alpha=0.7, edgecolor='black')

    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}ms',
                ha='center', va='bottom', fontweight='bold')

    ax2.set_title('Average Latency by Endpoint', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Latency (ms)', fontsize=10)
    ax2.grid(axis='y', alpha=0.3)

    # Circuit breaker states
    ax3 = fig.add_subplot(gs[1, 0])
    state_colors = ['green' if s == 'CLOSED' else 'red' for s in circuit_states]
    state_values = [1 if s == 'CLOSED' else 0 for s in circuit_states]
    bars3 = ax3.bar(endpoints, state_values, color=state_colors, alpha=0.7, edgecolor='black')

    for i, (bar, state) in enumerate(zip(bars3, circuit_states)):
        ax3.text(bar.get_x() + bar.get_width()/2., 0.5,
                state,
                ha='center', va='center', fontweight='bold', fontsize=10, color='white')

    ax3.set_title('Circuit Breaker States', fontsize=12, fontweight='bold')
    ax3.set_ylabel('State', fontsize=10)
    ax3.set_yticks([])
    ax3.set_ylim(0, 1)

    # Overall health summary
    ax4 = fig.add_subplot(gs[1, 1])
    health_scores = [success_rates[i] * (1 - avg_latency[i]/500) * (1 if circuit_states[i] == 'CLOSED' else 0.5)
                    for i in range(len(endpoints))]
    health_colors = ['green' if hs > 70 else 'orange' if hs > 50 else 'red' for hs in health_scores]

    bars4 = ax4.barh(endpoints, health_scores, color=health_colors, alpha=0.7, edgecolor='black')

    for bar in bars4:
        width = bar.get_width()
        ax4.text(width, bar.get_y() + bar.get_height()/2.,
                f'{int(width)}',
                ha='left', va='center', fontweight='bold', fontsize=10)

    ax4.set_title('Overall Health Score', fontsize=12, fontweight='bold')
    ax4.set_xlabel('Health Score (0-100)', fontsize=10)
    ax4.grid(axis='x', alpha=0.3)

    plt.suptitle('Resilience Dashboard: Multi-Endpoint Health Metrics',
                fontsize=16, fontweight='bold', y=0.98)
    return fig

def main():
    print("Generating Chapter 12 Visualizations...")

    fig1 = plot_circuit_breaker_timeline()
    plt.savefig('ch12_circuit_breaker_timeline.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: ch12_circuit_breaker_timeline.png")

    fig2 = plot_rate_limiter_tokens()
    plt.savefig('ch12_rate_limiter_behavior.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: ch12_rate_limiter_behavior.png")

    fig3 = plot_resilience_dashboard()
    plt.savefig('ch12_resilience_dashboard.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: ch12_resilience_dashboard.png")

    print("\n📊 All Chapter 12 plots generated successfully!")
    plt.show()

if __name__ == "__main__":
    main()
