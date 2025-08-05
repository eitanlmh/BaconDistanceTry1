import time
from collections import deque

def find_bacon_distance(graph, actor_name_to_id, actor_name):
    bacon_id=actor_name_to_id["Kevin Bacon"]
    print("searching bacon distance...")
    if actor_name not in actor_name_to_id:
        raise ValueError("actor name {} not in actor_name_to_id".format(actor_name))

    print("finding actor id by actor name...")
    start_time = time.time()
    target_id = actor_name_to_id[actor_name]
    end_time = time.time()
    print(f"found id: {target_id}, in {end_time - start_time} seconds")
    if bacon_id in target_id:
        return 0

    visited = {bacon_id}
    queue = deque([(bacon_id, 0)])
    print(f"searching the queue...")
    _start_time = time.time()
    while queue:
        current_actor, dist = queue.popleft()

        if current_actor in target_id:

            __end_time = time.time()
            print(f"returning dist inside while {dist} in {__end_time - _start_time} seconds")
            return dist

        try:

            for neighbor in graph[current_actor]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
        except KeyError:
            continue
    _end_time=time.time()
    print(f"finished scanning at end of while in {_end_time - _start_time} seconds")
    return float("inf")

