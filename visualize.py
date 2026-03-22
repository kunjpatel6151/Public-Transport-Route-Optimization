import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import numpy as np
from collections import defaultdict
from network import ROUTES, HUB_STOPS

def plot_learning_curve(rewards):
    fig, ax = plt.subplots(figsize=(10, 4))
    fig.patch.set_facecolor('#F9FAFB')
    ax.set_facecolor('#F9FAFB')

    window = min(50, max(1, len(rewards) // 10))
    smooth = np.convolve(rewards, np.ones(window) / window, mode='valid')

    ax.plot(rewards, alpha=0.2, color='#2563EB', linewidth=0.8,
            label='Raw reward per episode')
    ax.plot(range(window - 1, len(rewards)), smooth,
            color='#2563EB', linewidth=2.2,
            label=f'{window}-episode moving average')

    if len(smooth) > 0:
        best_val = float(np.max(smooth))
        best_idx = int(np.argmax(smooth))
        ax.axhline(best_val, color='#16A34A', linestyle='--',
                   linewidth=1.2,
                   label=f'Best avg: {best_val:.1f} (ep {best_idx + window})')
        ax.scatter([best_idx + window], [best_val],
                   color='#16A34A', zorder=5, s=60)

    ax.set_xlabel('Episode', fontsize=11)
    ax.set_ylabel('Total Reward', fontsize=11)
    ax.set_title('Q-Learning: Reward Convergence Over Training', fontsize=13, pad=12)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig


def plot_network(best_path_stops=None, source=0, destination=24):
    G   = nx.DiGraph()
    pos = {s: ((s % 5) * 2.4, -(s // 5) * 2.4) for s in range(25)}
    G.add_nodes_from(range(25))

    edge_colors = {}
    for rname, rinfo in ROUTES.items():
        stops = rinfo['stops']
        color = ('#2563EB' if rinfo['mode'] == 'bus'
                 else '#16A34A' if rinfo['mode'] == 'metro'
                 else '#D97706')
        for i in range(len(stops) - 1):
            G.add_edge(stops[i], stops[i + 1])
            edge_colors[(stops[i], stops[i + 1])] = color

    node_colors = []
    for s in range(25):
        if s == source:        node_colors.append('#15803D')
        elif s == destination: node_colors.append('#DC2626')
        elif s in HUB_STOPS:   node_colors.append('#7C3AED')
        else:                  node_colors.append('#6B7280')

    ec = [edge_colors.get((u, v), '#D1D5DB') for u, v in G.edges()]

    fig, ax = plt.subplots(figsize=(11, 9))
    fig.patch.set_facecolor('#F9FAFB')
    ax.set_facecolor('#F9FAFB')

    nx.draw(G, pos, ax=ax,
            with_labels=True,
            labels={s: f'S{s}' for s in range(25)},
            node_color=node_colors,
            edge_color=ec,
            node_size=750,
            font_color='white',
            font_size=8,
            font_weight='bold',
            arrows=True,
            arrowsize=10,
            connectionstyle='arc3,rad=0.05')

    if best_path_stops and len(best_path_stops) > 1:
        path_edges = [(best_path_stops[i], best_path_stops[i + 1])
                      for i in range(len(best_path_stops) - 1)]
        nx.draw_networkx_edges(G, pos, ax=ax,
                               edgelist=path_edges,
                               edge_color='#EF4444',
                               width=4.5,
                               arrows=True,
                               arrowsize=18,
                               connectionstyle='arc3,rad=0.05')

    legend_handles = [
        mpatches.Patch(color='#2563EB', label='Bus route'),
        mpatches.Patch(color='#16A34A', label='Metro route'),
        mpatches.Patch(color='#D97706', label='Auto route'),
        mpatches.Patch(color='#7C3AED', label='Transfer hub'),
        mpatches.Patch(color='#15803D', label=f'Source (S{source})'),
        mpatches.Patch(color='#DC2626', label=f'Destination (S{destination})'),
        mpatches.Patch(color='#EF4444', label='Optimal path'),
    ]
    ax.legend(handles=legend_handles, loc='lower right',
              fontsize=8, framealpha=0.9)
    ax.set_title('Public Transport Network — 25 Stops | 25 Routes',
                 fontsize=13, pad=12)
    plt.tight_layout()
    return fig


def plot_qtable(Q):
    stop_val = defaultdict(float)
    for (state, _), val in Q.items():
        s = state[0]
        if val > stop_val[s]:
            stop_val[s] = val

    stops  = list(range(25))
    values = [stop_val.get(s, 0.0) for s in stops]
    colors = ['#16A34A' if v > 0 else '#DC2626' for v in values]

    fig, ax = plt.subplots(figsize=(13, 4))
    fig.patch.set_facecolor('#F9FAFB')
    ax.set_facecolor('#F9FAFB')

    bars = ax.bar([f'S{s}' for s in stops], values,
                  color=colors, edgecolor='white', linewidth=0.5)
    ax.axhline(0, color='#9CA3AF', linewidth=0.8)

    for bar, val in zip(bars, values):
        if val != 0:
            ax.text(bar.get_x() + bar.get_width() / 2,
                    val + (0.5 if val > 0 else -1.5),
                    f'{val:.1f}', ha='center', va='bottom',
                    fontsize=6, color='#374151')

    ax.set_xlabel('Stop', fontsize=11)
    ax.set_ylabel('Max Q-value', fontsize=11)
    ax.set_title('Max Q-value Learned per Stop', fontsize=13, pad=12)
    ax.grid(True, axis='y', alpha=0.3)
    plt.xticks(rotation=45, fontsize=8)
    plt.tight_layout()
    return fig
