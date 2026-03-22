import heapq
from network import ROUTES, STOP_ROUTES, SOURCE, DESTINATION

def dijkstra_static(source=SOURCE, destination=DESTINATION):
    dist = {s: float('inf') for s in range(25)}
    dist[source] = 0
    prev = {}
    pq   = [(0.0, source, None)]

    while pq:
        cost, stop, route = heapq.heappop(pq)
        if cost > dist[stop]:
            continue
        for rname in STOP_ROUTES.get(stop, []):
            stops = ROUTES[rname]['stops']
            if stop not in stops:
                continue
            idx = stops.index(stop)
            if idx + 1 < len(stops):
                nxt        = stops[idx + 1]
                edge       = (stop, nxt)
                length_km  = ROUTES[rname]['edges'][edge]['length_km']
                base_speed = ROUTES[rname]['edges'][edge]['base_speed']
                seg_time   = (length_km / base_speed) * 60
                new_cost   = cost + seg_time
                if new_cost < dist[nxt]:
                    dist[nxt] = new_cost
                    prev[nxt] = (stop, rname)
                    heapq.heappush(pq, (new_cost, nxt, rname))

    path, node = [], destination
    while node in prev:
        p_stop, r = prev[node]
        path.append({'stop': node, 'route': r})
        node = p_stop
    path.append({'stop': source, 'route': 'Start'})
    return list(reversed(path)), round(dist[destination], 1)
