#1
def canFinish(numCourses, prerequisites):
    # Create adjacency list to represent the graph
    graph = [[] for _ in range(numCourses)]
    # Track in-degree (number of prerequisites) for each course
    inDegree = [0] * numCourses
    
    # Build the graph and count prerequisites
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        inDegree[course] += 1
    
    # Initialize queue with all courses that have no prerequisites
    queue = []
    for course in range(numCourses):
        if inDegree[course] == 0:
            queue.append(course)
    
    # Count courses we can complete
    coursesCompleted = 0
    
    # Process courses in topological order
    while queue:
        current = queue.pop(0)
        coursesCompleted += 1
        
        # For each course that requires the current course
        for nextCourse in graph[current]:
            inDegree[nextCourse] -= 1
            # If we've satisfied all prerequisites for nextCourse
            if inDegree[nextCourse] == 0:
                queue.append(nextCourse)
    
    # If we can complete all courses, return True
    return coursesCompleted == numCourses
#2
def networkDelayTime(times, n, k):
    INF = float('inf')
    
    # Create adjacency matrix
    graph = [[INF] * (n + 1) for _ in range(n + 1)]
    
    # Initialize diagonal elements to 0
    for i in range(1, n + 1):
        graph[i][i] = 0
    
    # Fill graph with edge weights
    for u, v, w in times:
        graph[u][v] = w
    
    # Track visited nodes
    visited = [False] * (n + 1)
    
    # Distance array for storing shortest paths
    distances = [INF] * (n + 1)
    distances[k] = 0
    
    def get_min_unvisited():
        min_dist = INF
        min_node = -1
        for node in range(1, n + 1):
            if not visited[node] and distances[node] < min_dist:
                min_dist = distances[node]
                min_node = node
        return min_node
    
    # Run Dijkstra's algorithm
    for _ in range(n):
        # Get unvisited node with minimum distance
        curr = get_min_unvisited()
        
        # If no reachable unvisited nodes found
        if curr == -1:
            break
            
        visited[curr] = True
        
        # Update distances through current node
        for next_node in range(1, n + 1):
            if not visited[next_node] and graph[curr][next_node] != INF:
                new_dist = distances[curr] + graph[curr][next_node]
                if new_dist < distances[next_node]:
                    distances[next_node] = new_dist
    
    # Find maximum time to reach any node
    max_time = 0
    for i in range(1, n + 1):
        if distances[i] == INF:
            return -1
        max_time = max(max_time, distances[i])
    
    return max_time
#3
def minCostWater(n, wells, pipes):
    # Add a virtual node (node 0) to represent water source
    # Create edges from this node to each house with well cost
    edges = []
    for i in range(n):
        edges.append((0, i + 1, wells[i]))  # Edge from source to house
    
    # Add all pipe connections
    for house1, house2, cost in pipes:
        edges.append((house1, house2, cost))
    
    # Sort edges by cost
    edges.sort(key=lambda x: x[2])
    
    # Initialize disjoint set for union-find
    parent = list(range(n + 1))  # +1 for virtual node 0
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        parent[find(x)] = find(y)
    
    # Kruskal's algorithm
    total_cost = 0
    connections = 0
    
    for u, v, cost in edges:
        if find(u) != find(v):
            union(u, v)
            total_cost += cost
            connections += 1
            if connections == n:  # We need exactly n edges for n houses
                break
    
    return total_cost
