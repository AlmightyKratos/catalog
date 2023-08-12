import heapq


class Graph:
    def __init__(self) -> None:
        # {'L': {'mL': 1000}, 'mL': {'L': 1000, 'fl oz': 29.57}, 'fl oz': {'mL': 29.57}, 'kg': {'g': 1000, 'lb': 2.204}, 'g': {'kg': 1000, 'mg': 1000, 'tsp': 5}, 'mg': {'g': 1000}, 'tsp': {'g': 5}, 'lb': {'kg': 2.204}}
        self.graph: dict[str, dict[str, float]] = {}

    def get_neighbors(self, city):
        if city in self.graph:
            return self.graph[city]
        return {}

    def add_edge(self, city1: str, city2: str, cost: float) -> None:
        # Add the edge in both directions (graph is undirected)
        self._add_edge(city1, city2, cost)
        self._add_edge(city2, city1, cost)

    def _add_edge(self, city1: str, city2: str, cost: float) -> None:
        if city1 not in self.graph:
            self.graph[city1] = {}
        self.graph[city1][city2] = cost

    def dijkstra(self, start_city: str, end_city: str) -> float | None:
        # Initialize distance dictionary with infinity for all cities except the start city
        distance = {city: float("inf") for city in self.graph}
        distance[start_city] = 1

        # Priority queue to keep track of cities and their costs
        priority_queue: list[tuple[float, str]] = [(1, start_city)]

        while priority_queue:
            current_cost, current_city = heapq.heappop(priority_queue)

            # If the current city is the destination city, return its cost
            if current_city == end_city:
                return distance[end_city]

            # Explore neighbors of the current city
            for neighbor, edge_cost in self.graph[current_city].items():
                new_cost = current_cost * edge_cost
                if new_cost < distance[neighbor]:
                    distance[neighbor] = new_cost
                    heapq.heappush(priority_queue, (new_cost, neighbor))

        # If the destination city is not reachable from the start city, return None
        return None


# Create a new graph
graph = Graph()

# Add cities and their connections with associated costs
graph.add_edge("L", "mL", 1000)
graph.add_edge("fl oz", "mL", 29.57)
graph.add_edge("kg", "g", 1000)
graph.add_edge("g", "mg", 1000)
graph.add_edge("tsp", "g", 5)
graph.add_edge("kg", "lb", 2.204)
breakpoint()
graph.add_edge("lb", "oz", 16)

# Find the cost to go from one city to another using the least cost path
start_city = "mL"
end_city = "fl oz"
cost_factor = graph.dijkstra(start_city, end_city)
input_amount = 4


if cost_factor is not None:
    cost = cost_factor * input_amount
    print(f"{input_amount} {start_city} is equivalent to {cost} {end_city}.")
else:
    print(f"There is no path from {start_city} to {end_city}.")

# print(graph.get_neighbors("mL"))
