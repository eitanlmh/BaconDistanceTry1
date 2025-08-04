from collections import deque

def find_bacon_distance(graph, actor_name_to_id, actor_name, bacon_id="nm0000102"):

    print("searching bacon distance...")
    if actor_name not in actor_name_to_id:
        raise ValueError("actor name {} not in actor_name_to_id".format(actor_name))

    target_ids = actor_name_to_id[actor_name]

    if bacon_id in target_ids:
        return 0

    visited = {bacon_id}
    queue = deque([(bacon_id, 0)])
    while queue:
        current_actor, dist = queue.popleft()

        if current_actor in target_ids:
            return dist

        try:

            for neighbor in graph[current_actor]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
        except KeyError:
            continue

    return float("inf")

