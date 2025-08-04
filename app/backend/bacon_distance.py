from app.backend.modules.bacon_distance_modules.bfs_search import find_bacon_distance

Kevin_Bacon_Name = "Kevin Bacon"

def get_bacon_distance(actor_name, graph, actor_name_to_id):
    actor_name = actor_name.strip().title()

    if not actor_name:
        return "No actor name provided"


    try:
        distance = find_bacon_distance(graph, actor_name_to_id, actor_name)

        return distance
    except ValueError as e:
        return str(e)
