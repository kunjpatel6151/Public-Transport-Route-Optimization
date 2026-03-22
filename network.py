STOPS = list(range(25))
SOURCE = 0
DESTINATION = 24

# Every stop served by 2+ routes is a hub.
# S9  served by Bus2, Bus8, Auto4      → hub
# S4  served by Bus1, Bus8             → hub
# S14 served by Bus3, Bus8, Auto8      → hub
# S19 served by Bus4, Bus8             → hub
# S21 served by Metro1, Auto11         → hub
# S22 served by Bus5, Bus7             → hub
# S23 served by Bus5, Metro2, Auto12   → hub
HUB_STOPS = {1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14,
             15, 16, 17, 18, 19, 21, 22, 23}

ROUTES = {
    'Bus1': {
        'stops': [0, 1, 2, 3, 4], 'mode': 'bus',
        'edges': {
            (0,1): {'length_km': 2.1, 'base_speed': 24},
            (1,2): {'length_km': 3.4, 'base_speed': 18},
            (2,3): {'length_km': 2.8, 'base_speed': 22},
            (3,4): {'length_km': 1.9, 'base_speed': 28},
        }
    },
    'Bus2': {
        'stops': [5, 6, 7, 8, 9], 'mode': 'bus',
        'edges': {
            (5,6): {'length_km': 2.5, 'base_speed': 20},
            (6,7): {'length_km': 3.1, 'base_speed': 26},
            (7,8): {'length_km': 2.2, 'base_speed': 16},
            (8,9): {'length_km': 2.9, 'base_speed': 22},
        }
    },
    'Bus3': {
        'stops': [10, 11, 12, 13, 14], 'mode': 'bus',
        'edges': {
            (10,11): {'length_km': 2.3, 'base_speed': 21},
            (11,12): {'length_km': 4.1, 'base_speed': 15},
            (12,13): {'length_km': 2.0, 'base_speed': 25},
            (13,14): {'length_km': 3.2, 'base_speed': 19},
        }
    },
    'Bus4': {
        'stops': [15, 16, 17, 18, 19], 'mode': 'bus',
        'edges': {
            (15,16): {'length_km': 3.0, 'base_speed': 18},
            (16,17): {'length_km': 2.4, 'base_speed': 23},
            (17,18): {'length_km': 2.1, 'base_speed': 26},
            (18,19): {'length_km': 3.5, 'base_speed': 17},
        }
    },
    'Bus5': {
        'stops': [20, 21, 22, 23, 24], 'mode': 'bus',
        'edges': {
            (20,21): {'length_km': 1.8, 'base_speed': 27},
            (21,22): {'length_km': 2.6, 'base_speed': 21},
            (22,23): {'length_km': 2.3, 'base_speed': 24},
            (23,24): {'length_km': 3.1, 'base_speed': 19},
        }
    },
    'Bus6': {
        'stops': [0, 5, 10, 15, 20], 'mode': 'bus',
        'edges': {
            (0,5):   {'length_km': 3.8, 'base_speed': 20},
            (5,10):  {'length_km': 4.2, 'base_speed': 18},
            (10,15): {'length_km': 3.6, 'base_speed': 22},
            (15,20): {'length_km': 3.1, 'base_speed': 24},
        }
    },
    'Bus7': {
        'stops': [2, 7, 12, 17, 22], 'mode': 'bus',
        'edges': {
            (2,7):   {'length_km': 4.5, 'base_speed': 19},
            (7,12):  {'length_km': 3.8, 'base_speed': 21},
            (12,17): {'length_km': 4.0, 'base_speed': 20},
            (17,22): {'length_km': 3.3, 'base_speed': 23},
        }
    },
    'Bus8': {
        'stops': [4, 9, 14, 19, 24], 'mode': 'bus',
        'edges': {
            (4,9):   {'length_km': 3.5, 'base_speed': 22},
            (9,14):  {'length_km': 4.8, 'base_speed': 16},
            (14,19): {'length_km': 3.2, 'base_speed': 24},
            (19,24): {'length_km': 2.7, 'base_speed': 26},
        }
    },
    'Metro1': {
        'stops': [1, 6, 11, 16, 21], 'mode': 'metro',
        'edges': {
            (1,6):   {'length_km': 4.2, 'base_speed': 65},
            (6,11):  {'length_km': 5.1, 'base_speed': 58},
            (11,16): {'length_km': 4.4, 'base_speed': 65},
            (16,21): {'length_km': 3.8, 'base_speed': 72},
        }
    },
    'Metro2': {
        'stops': [3, 8, 13, 18, 23], 'mode': 'metro',
        'edges': {
            (3,8):   {'length_km': 4.6, 'base_speed': 65},
            (8,13):  {'length_km': 4.3, 'base_speed': 65},
            (13,18): {'length_km': 5.5, 'base_speed': 55},
            (18,23): {'length_km': 3.9, 'base_speed': 72},
        }
    },
    'Metro3': {
        'stops': [6, 7, 8], 'mode': 'metro',
        'edges': {
            (6,7): {'length_km': 3.2, 'base_speed': 70},
            (7,8): {'length_km': 3.5, 'base_speed': 68},
        }
    },
    'Metro4': {
        'stops': [11, 12, 13], 'mode': 'metro',
        'edges': {
            (11,12): {'length_km': 3.8, 'base_speed': 62},
            (12,13): {'length_km': 3.3, 'base_speed': 70},
        }
    },
    'Metro5': {
        'stops': [16, 17, 18], 'mode': 'metro',
        'edges': {
            (16,17): {'length_km': 3.1, 'base_speed': 70},
            (17,18): {'length_km': 3.6, 'base_speed': 65},
        }
    },
    'Auto1':  {'stops': [0,  6],  'mode': 'auto',
               'edges': {(0,6):   {'length_km': 1.8, 'base_speed': 16}}},
    'Auto2':  {'stops': [1,  7],  'mode': 'auto',
               'edges': {(1,7):   {'length_km': 1.5, 'base_speed': 18}}},
    'Auto3':  {'stops': [2,  8],  'mode': 'auto',
               'edges': {(2,8):   {'length_km': 2.1, 'base_speed': 14}}},
    'Auto4':  {'stops': [3,  9],  'mode': 'auto',
               'edges': {(3,9):   {'length_km': 1.6, 'base_speed': 20}}},
    'Auto5':  {'stops': [5,  11], 'mode': 'auto',
               'edges': {(5,11):  {'length_km': 2.4, 'base_speed': 13}}},
    'Auto6':  {'stops': [6,  12], 'mode': 'auto',
               'edges': {(6,12):  {'length_km': 1.9, 'base_speed': 17}}},
    'Auto7':  {'stops': [7,  13], 'mode': 'auto',
               'edges': {(7,13):  {'length_km': 2.0, 'base_speed': 15}}},
    'Auto8':  {'stops': [8,  14], 'mode': 'auto',
               'edges': {(8,14):  {'length_km': 1.7, 'base_speed': 19}}},
    'Auto9':  {'stops': [10, 16], 'mode': 'auto',
               'edges': {(10,16): {'length_km': 2.2, 'base_speed': 14}}},
    'Auto10': {'stops': [12, 18], 'mode': 'auto',
               'edges': {(12,18): {'length_km': 1.8, 'base_speed': 16}}},
    'Auto11': {'stops': [15, 21], 'mode': 'auto',
               'edges': {(15,21): {'length_km': 2.0, 'base_speed': 15}}},
    'Auto12': {'stops': [17, 23], 'mode': 'auto',
               'edges': {(17,23): {'length_km': 1.5, 'base_speed': 18}}},
}

STOP_ROUTES = {}
for rname, rinfo in ROUTES.items():
    for s in rinfo['stops']:
        STOP_ROUTES.setdefault(s, []).append(rname)

TRANSFER_COST = {
    ('bus',   'bus'):   2,
    ('bus',   'metro'): 8,
    ('bus',   'auto'):  3,
    ('metro', 'bus'):   8,
    ('metro', 'metro'): 2,
    ('metro', 'auto'):  5,
    ('auto',  'bus'):   3,
    ('auto',  'metro'): 5,
    ('auto',  'auto'):  2,
}

HEADWAY = {
    'peak':     {'bus': 3,  'metro': 4,  'auto': 1},
    'off_peak': {'bus': 12, 'metro': 15, 'auto': 4},
}
