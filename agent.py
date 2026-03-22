import random
from collections import defaultdict
from network import SOURCE, DESTINATION, STOP_ROUTES, ROUTES, TRANSFER_COST
from environment import reset_episode, make_fixed_env, get_travel_time
from mdp import get_state, get_valid_actions, get_reward

def train(episodes=2000, alpha=0.1, gamma=0.9, epsilon_start=1.0,
          time_band_setting='random', closure_prob=0.10,
          source=SOURCE, destination=DESTINATION,
          progress_callback=None):

    Q = defaultdict(float)
    rewards_per_episode = []
    epsilon = epsilon_start
    MAX_STEPS = 120
    start_route = STOP_ROUTES[source][0]

    for ep in range(episodes):
        env, _ = reset_episode(time_band_setting, closure_prob)
        stop   = source
        route  = start_route
        state  = get_state(stop, route)
        total_r = 0

        for _ in range(MAX_STEPS):
            actions = get_valid_actions(stop, route)
            if not actions:
                break
            if random.random() < epsilon:
                action = random.choice(actions)
            else:
                action = max(actions, key=lambda a: Q[(state, a)])

            atype, next_stop, next_route = action
            done   = (next_stop == destination)
            reward = get_reward(atype, route, next_route,
                                stop, next_stop, env, done)
            total_r += reward

            ns     = get_state(next_stop, next_route)
            na     = get_valid_actions(next_stop, next_route)
            max_nq = max((Q[(ns, a)] for a in na), default=0)

            Q[(state, action)] += alpha * (
                reward + gamma * max_nq - Q[(state, action)]
            )

            stop, route, state = next_stop, next_route, ns
            if done:
                break

        rewards_per_episode.append(total_r)
        epsilon = max(0.01, epsilon * 0.995)

        if progress_callback and (ep + 1) % 50 == 0:
            progress_callback(ep + 1, episodes, rewards_per_episode)

    return Q, rewards_per_episode


def get_best_path(Q, source=SOURCE, destination=DESTINATION):
    """
    Extract greedy path using a fixed environment (no congestion,
    all routes available). Uses visited_states to prevent infinite
    cycling when Q-values are equal or poorly learned.
    """
    env    = make_fixed_env()
    stop   = source
    route  = STOP_ROUTES[source][0]
    path   = [{'stop': stop, 'route': route, 'action': 'start',
                'time': 0, 'distance_km': 0.0, 'speed_kmh': 0}]
    total_time = 0.0
    total_dist = 0.0
    visited_states = set()

    for _ in range(120):
        state = get_state(stop, route)

        if state in visited_states:
            break
        visited_states.add(state)

        actions = get_valid_actions(stop, route)
        if not actions:
            break

        unvisited_actions = [
            a for a in actions
            if get_state(a[1], a[2]) not in visited_states
        ]
        candidates = unvisited_actions if unvisited_actions else actions
        action = max(candidates, key=lambda a: Q[(state, a)])

        atype, next_stop, next_route = action

        if atype == 'travel':
            edge       = (stop, next_stop)
            length_km  = ROUTES[next_route]['edges'][edge]['length_km']
            base_speed = ROUTES[next_route]['edges'][edge]['base_speed']
            travel_t   = round((length_km / base_speed) * 60, 1)
            wait_t     = env[next_route]['wait']
            step_time  = round(travel_t + wait_t, 1)
            d          = length_km
            s          = base_speed
        else:
            fm        = ROUTES[route]['mode']
            tm        = ROUTES[next_route]['mode']
            step_time = TRANSFER_COST[(fm, tm)] + env[next_route]['wait']
            d         = 0.0
            s         = 0

        total_time += step_time
        total_dist += d

        path.append({
            'stop':        next_stop,
            'route':       next_route,
            'action':      atype,
            'time':        step_time,
            'distance_km': round(d, 2),
            'speed_kmh':   s,
        })

        stop, route = next_stop, next_route
        if stop == destination:
            break

    return path, round(total_time, 1), round(total_dist, 2)


def export_qtable_csv(Q):
    rows = []
    for (state, action), q_val in Q.items():
        state_stop,  state_route  = state
        action_type, a_next_stop, a_next_route = action
        rows.append({
            'state_stop':       state_stop,
            'state_route':      state_route,
            'action_type':      action_type,
            'action_next_stop': a_next_stop,
            'action_next_route':a_next_route,
            'q_value':          round(q_val, 4),
        })
    rows.sort(key=lambda r: r['q_value'], reverse=True)
    return rows
