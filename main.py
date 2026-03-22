import matplotlib.pyplot as plt
from agent import train, get_best_path, export_qtable_csv
from visualize import plot_learning_curve, plot_network, plot_qtable
from comparison import dijkstra_static
import csv

if __name__ == '__main__':
    print('=' * 60)
    print('  Public Transport Route Optimizer — Q-Learning')
    print('  25 Stops | 8 Bus | 5 Metro | 12 Auto')
    print('  Travel time: length_km / (base_speed / congestion) × 60')
    print('=' * 60)

    print('\n[1] Training for 2000 episodes...')
    Q, rewards = train(episodes=2000)
    avg = sum(rewards[-100:]) / 100
    print(f'    Done. Final 100-ep avg reward: {avg:.2f}')

    print('\n[2] Extracting best path (fixed env, no congestion)...')
    path, total_time, total_dist = get_best_path(Q)
    print(f'    Total journey time : {total_time} min')
    print(f'    Total distance     : {total_dist} km')
    for i, step in enumerate(path):
        print(f"    Step {i:2d}: S{step['stop']:2d}  "
              f"{step['action']:8s}  {step['route']:<10}  "
              f"+{step['time']} min  "
              f"{step['distance_km']} km @ {step['speed_kmh']} km/h")

    print('\n[3] Dijkstra static baseline...')
    d_path, d_cost = dijkstra_static()
    print(f'    Dijkstra cost: {d_cost} min  (base speed, no congestion, no wait)')

    print('\n[4] Exporting Q-table to qtable_export.csv...')
    rows = export_qtable_csv(Q)
    with open('qtable_export.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f'    Exported {len(rows)} Q-table entries.')

    print('\n[5] Generating plots...')
    path_stops = [p['stop'] for p in path]
    fig1 = plot_learning_curve(rewards)
    fig2 = plot_network(path_stops)
    fig3 = plot_qtable(Q)
    plt.show()
    print('Done.')
