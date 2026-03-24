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
    ROUTE_COLORS = {
        'Bus1':   '#1E40AF',
        'Bus2':   '#2563EB',
        'Bus3':   '#3B82F6',
        'Bus4':   '#60A5FA',
        'Bus5':   '#93C5FD',
        'Bus6':   '#1D4ED8',
        'Bus7':   '#1E3A8A',
        'Bus8':   '#172554',
        'Metro1': '#14532D',
        'Metro2': '#166534',
        'Metro3': '#15803D',
        'Metro4': '#16A34A',
        'Metro5': '#22C55E',
        'Auto1':  '#78350F',
        'Auto2':  '#92400E',
        'Auto3':  '#B45309',
        'Auto4':  '#D97706',
        'Auto5':  '#F59E0B',
        'Auto6':  '#FBBF24',
        'Auto7':  '#7C2D12',
        'Auto8':  '#9A3412',
        'Auto9':  '#C2410C',
        'Auto10': '#EA580C',
        'Auto11': '#F97316',
        'Auto12': '#FB923C',
    }

    RAD_SEQUENCE = [0.0, 0.18, 0.35, -0.18, -0.35]

    pos = {s: ((s % 5) * 2.6, -(s // 5) * 2.6) for s in range(25)}

    G = nx.DiGraph()
    G.add_nodes_from(range(25))

    fig, ax = plt.subplots(figsize=(16, 13))
    fig.patch.set_facecolor('#F9FAFB')
    ax.set_facecolor('#F9FAFB')

    # --- STEP 1: Draw nodes ---
    node_colors = []
    for s in range(25):
        if s == source:        node_colors.append('#15803D')
        elif s == destination: node_colors.append('#DC2626')
        elif s in HUB_STOPS:   node_colors.append('#7C3AED')
        else:                  node_colors.append('#6B7280')

    nx.draw_networkx_nodes(G, pos, ax=ax,
                           nodelist=list(range(25)),
                           node_color=node_colors,
                           node_size=800,
                           edgecolors='white',
                           linewidths=1.5)
    nx.draw_networkx_labels(G, pos, ax=ax,
                            labels={s: f'S{s}' for s in range(25)},
                            font_color='white',
                            font_size=8,
                            font_weight='bold')

    # --- STEP 2 & 3: Draw route edges with FancyArrowPatch + labels ---
    # Track how many routes have been drawn on each directed edge pair
    edge_count = defaultdict(int)

    for rname, rinfo in ROUTES.items():
        stops = rinfo['stops']
        color = ROUTE_COLORS.get(rname, '#6B7280')

        for i in range(len(stops) - 1):
            u, v = stops[i], stops[i + 1]
            # Normalise the edge pair so (u,v) and (v,u) share the
            # same counter — prevents overlapping in opposite directions
            pair = (min(u, v), max(u, v))
            idx = edge_count[pair]
            edge_count[pair] += 1

            rad = RAD_SEQUENCE[idx % len(RAD_SEQUENCE)]

            p_u = pos[u]
            p_v = pos[v]

            arrow = mpatches.FancyArrowPatch(
                posA=p_u, posB=p_v,
                arrowstyle='->', mutation_scale=12,
                connectionstyle=f'arc3,rad={rad}',
                color=color, lw=1.2, zorder=2,
            )
            ax.add_patch(arrow)

            # Label at midpoint, offset perpendicular for curved arcs
            mx = (p_u[0] + p_v[0]) / 2
            my = (p_u[1] + p_v[1]) / 2

            # Perpendicular offset based on rad value
            dx = p_v[0] - p_u[0]
            dy = p_v[1] - p_u[1]
            length = np.sqrt(dx * dx + dy * dy)
            if length > 0:
                # Perpendicular unit vector (rotated 90°)
                px = -dy / length
                py = dx / length
                offset = rad * length * 0.35
                mx += px * offset
                my += py * offset

            ax.text(mx, my, rname, fontsize=6, color=color,
                    ha='center', va='center', zorder=3,
                    fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.1',
                              facecolor='#F9FAFB', edgecolor='none',
                              alpha=0.8))

    # --- STEP 4: Draw optimal path overlay ---
    if best_path_stops and len(best_path_stops) > 1:
        for i in range(len(best_path_stops) - 1):
            u = best_path_stops[i]
            v = best_path_stops[i + 1]
            p_u = pos[u]
            p_v = pos[v]
            arrow = mpatches.FancyArrowPatch(
                posA=p_u, posB=p_v,
                arrowstyle='->', mutation_scale=18,
                connectionstyle='arc3,rad=0.0',
                color='#EF4444', lw=3.5, zorder=5,
            )
            ax.add_patch(arrow)

    # --- STEP 5: Legend ---
    legend_handles = [
        mpatches.Patch(color='#2563EB', label='Bus routes'),
        mpatches.Patch(color='#16A34A', label='Metro routes'),
        mpatches.Patch(color='#D97706', label='Auto routes'),
        mpatches.Patch(color='#7C3AED', label='Transfer hub'),
        mpatches.Patch(color='#15803D', label=f'Source (S{source})'),
        mpatches.Patch(color='#DC2626', label=f'Destination (S{destination})'),
        mpatches.Patch(color='#EF4444', label='Optimal path'),
    ]
    ax.legend(handles=legend_handles, loc='lower right',
              fontsize=8, framealpha=0.9)

    ax.set_title('Public Transport Network — 25 Stops | 25 Routes',
                 fontsize=13, pad=14)
    ax.axis('off')
    plt.tight_layout()
    return fig


def plot_qtable(Q):
    """
    Scatter plot showing every single Q-table entry as one dot.
    x-axis  = stop number (0 to 24)
    y-axis  = Q-value (can be positive or negative)
    colour  = green (#16A34A) if Q-value >= 0
              red   (#DC2626) if Q-value <  0

    This replaces the old max-per-stop bar chart which hid
    negative values because defaultdict(float) defaulted
    unvisited stops to 0.0, masking all negative Q-values.
    Every entry in the Q-table is now plotted individually
    so the full distribution is visible.
    """
    xs = []
    ys = []
    cs = []

    for (state, _), val in Q.items():
        xs.append(state[0])
        ys.append(round(val, 2))
        cs.append('#16A34A' if val >= 0 else '#DC2626')

    fig, ax = plt.subplots(figsize=(14, 5))
    fig.patch.set_facecolor('#F9FAFB')
    ax.set_facecolor('#F9FAFB')

    ax.scatter(xs, ys, c=cs, alpha=0.5, s=18, linewidths=0)

    ax.axhline(0, color='#9CA3AF', linewidth=0.8, linestyle='--')

    ax.set_xlabel('Stop number', fontsize=11)
    ax.set_ylabel('Q-value', fontsize=11)
    ax.set_title(
        'All Q-values — every Q-table entry plotted as one dot',
        fontsize=13, pad=12
    )

    ax.set_xticks(range(25))
    ax.set_xticklabels(
        [f'S{s}' for s in range(25)],
        rotation=45, fontsize=8
    )

    ax.grid(True, alpha=0.3)

    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w',
               markerfacecolor='#16A34A', markersize=7,
               label='Positive Q-value (good action)'),
        Line2D([0], [0], marker='o', color='w',
               markerfacecolor='#DC2626', markersize=7,
               label='Negative Q-value (bad / costly action)'),
    ]
    ax.legend(handles=legend_elements, fontsize=9,
              loc='lower right')

    plt.tight_layout()
    return fig
