import random
from network import ROUTES, HEADWAY

def reset_episode(time_band_setting='random', closure_prob=0.10):
    if time_band_setting == 'peak':
        time_band = 'peak'
    elif time_band_setting == 'off_peak':
        time_band = 'off_peak'
    else:
        time_band = random.choice(['peak', 'off_peak'])

    env = {}
    for rname, rinfo in ROUTES.items():
        env[rname] = {
            'available': random.random() > closure_prob,
            'wait':      HEADWAY[time_band][rinfo['mode']],
            'edges':     {}
        }
        for edge in rinfo['edges']:
            env[rname]['edges'][edge] = {
                'congestion': round(random.uniform(1.0, 4.0), 2)
            }
    return env, time_band


def make_fixed_env():
    """
    Returns a fixed environment with NO congestion and all routes available.
    Used exclusively by get_best_path() to produce stable, reproducible results.
    congestion=1.0 means actual_speed = base_speed / 1.0 = base_speed (no slowdown).
    """
    env = {}
    for rname, rinfo in ROUTES.items():
        env[rname] = {
            'available': True,
            'wait':      HEADWAY['peak'][rinfo['mode']],
            'edges':     {}
        }
        for edge in rinfo['edges']:
            env[rname]['edges'][edge] = {'congestion': 1.0}
    return env


def get_travel_time(route_name, from_stop, to_stop, env):
    """
    Calculate actual travel time in minutes using:
        actual_speed = base_speed / congestion_factor
        actual_time  = (length_km / actual_speed) * 60

    Example:
        length_km=3.4, base_speed=18, congestion=2.5
        actual_speed = 18 / 2.5 = 7.2 km/h
        actual_time  = (3.4 / 7.2) * 60 = 28.3 minutes
    """
    edge         = (from_stop, to_stop)
    length_km    = ROUTES[route_name]['edges'][edge]['length_km']
    base_speed   = ROUTES[route_name]['edges'][edge]['base_speed']
    congestion   = env[route_name]['edges'][edge]['congestion']
    actual_speed = base_speed / congestion
    actual_time  = (length_km / actual_speed) * 60
    return round(actual_time, 2)
