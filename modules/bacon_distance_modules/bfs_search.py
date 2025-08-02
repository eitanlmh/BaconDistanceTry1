from collections import deque

def find_bacon_distance(graph, name_to_ids, actor_name, bacon_id="nm0000102"):
    if actor_name not in name_to_ids:
        raise ValueError(f"actor '{actor_name} not found in dataset")

    target_ids = name_to_ids[actor_name]

    if bacon_id in target_ids:
        return 0

    visited = set()
    queue = deque()
    queue.append((bacon_id, 0))
    visited.add(bacon_id)

    while queue:
        current_actor, dist = queue.popleft()

        if current_actor in target_ids:
            return dist

        for neighbor in graph.get(current_actor, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor,dist+1))

    return float("inf")
