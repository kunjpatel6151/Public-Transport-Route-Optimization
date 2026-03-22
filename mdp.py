from network import ROUTES, STOP_ROUTES, HUB_STOPS, TRANSFER_COST
from environment import get_travel_time

def get_state(stop, route):
    return (stop, route)

def get_valid_actions(stop, route):
    actions = []
    route_stops = ROUTES[route]['stops']
    if stop in route_stops:
        idx = route_stops.index(stop)
        if idx + 1 < len(route_stops):
            nxt = route_stops[idx + 1]
            actions.append(('travel', nxt, route))
    if stop in HUB_STOPS:
        for other in STOP_ROUTES.get(stop, []):
            if other != route:
                actions.append(('transfer', stop, other))
    return actions

def get_reward(action_type, current_route, next_route,
               from_stop, to_stop, env, reached_destination):
    if not env[next_route]['available']:
        return -1000
    travel = 0
    if action_type == 'travel':
        travel = get_travel_time(next_route, from_stop, to_stop, env)
    wait = env[next_route]['wait']
    transfer = 0
    if action_type == 'transfer':
        fm = ROUTES[current_route]['mode']
        tm = ROUTES[next_route]['mode']
        transfer = TRANSFER_COST[(fm, tm)]
    reward = -(travel + wait + transfer)
    if reached_destination:
        reward += 200
    return round(reward, 2)
