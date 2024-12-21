import heapq

class Node:
    def __init__(self, state, parent=None, cost=0, heuristic=0):
        self.state = state
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic
        self.f_score = cost + heuristic

    def __lt__(self, other):
        return self.f_score < other.f_score

def heuristic_func(state, goal):
    """
    Khai báo hàm heuristic  .
    """
    return abs(ord(goal) - ord(state))

def a_star_dfs_combined(graph, start, goal, split_ratio=0.5):
    """
    Kết hợp thuật toán A* và DFS để tìm đường đi.

    Args:
        graph: Đồ thị dưới dạng từ điển (danh sách kề).
        start: Nút bắt đầu.
        goal: Nút đích.
        split_ratio: Tỉ lệ số nút được duyệt bằng A*.

    Returns:
        Tuple chứa (đường đi, chi phí, số nút A* đã duyệt, số nút DFS đã duyệt), hoặc (None, None) nếu không tìm thấy đường đi.
    """
    total_nodes = len(graph)
    a_star_nodes_limit = int(total_nodes * split_ratio)
    a_star_nodes_explored = 0
    dfs_nodes_explored = 0
    open_set = []
    stack = []
    visited = set()
    heapq.heappush(open_set, Node(start, None, 0, heuristic_func(start, goal)))

    # Giai đoạn 1: Tìm kiếm A*
    for _ in range(a_star_nodes_limit):
        if not open_set:
            break
        current_node = heapq.heappop(open_set)
        if current_node.state in visited:
            continue
        visited.add(current_node.state)
        a_star_nodes_explored += 1
        if current_node.state == goal:
            path = reconstruct_path(current_node)
            return path, current_node.cost, a_star_nodes_explored, dfs_nodes_explored

        for neighbor, cost in graph.get(current_node.state, []):
            if neighbor not in visited:
                heapq.heappush(open_set, Node(neighbor, current_node, current_node.cost + cost, heuristic_func(neighbor, goal)))
    
    # Giai đoạn 2: Tìm kiếm DFS
    stack.extend(open_set)
    while stack:
        current_node = stack.pop()
        if current_node.state in visited:
            continue
        visited.add(current_node.state)
        dfs_nodes_explored += 1
        if current_node.state == goal:
            path = reconstruct_path(current_node)
            return path, current_node.cost, a_star_nodes_explored, dfs_nodes_explored

        for neighbor, cost in graph.get(current_node.state, []):
            if neighbor not in visited:
                stack.append(Node(neighbor, current_node, current_node.cost + cost))

    return None, None, a_star_nodes_explored, dfs_nodes_explored

def reconstruct_path(node):
    """
    Tái tạo đường đi từ nút đích về nút bắt đầu.
    """
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    return path[::-1]

# Ví dụ đồ thị
graph = {
    'A': [('B', 1), ('C', 2), ('H', 3)],
    'B': [('D', 4), ('E', 1)],
    'C': [('F', 2)],
    'H': [('I', 1)],
    'D': [('G', 1)],
    'E': [],
    'F': [('G', 3)],
    'I': [('K', 1)],
    'G': [],
    'K': [] 
}

start = 'A'
goal = 'G'
path, cost, a_star_explored, dfs_explored = a_star_dfs_combined(graph, start, goal)
if path:
    print(f"Đường đi từ {start} đến {goal}: {path}, Chi phí: {cost}, Số nút A* đã duyệt: {a_star_explored}, Số nút DFS đã duyệt: {dfs_explored}")
else:
    print(f"Không tìm thấy đường đi từ {start} đến {goal}, Số nút A* đã duyệt: {a_star_explored}, Số nút DFS đã duyệt: {dfs_explored}")

start = 'A'
goal = 'K'
path, cost, a_star_explored, dfs_explored = a_star_dfs_combined(graph, start, goal)
if path:
    print(f"Đường đi từ {start} đến {goal}: {path}, Chi phí: {cost}, Số nút A* đã duyệt: {a_star_explored}, Số nút DFS đã duyệt: {dfs_explored}")
else:
    print(f"Không tìm thấy đường đi từ {start} đến {goal}, Số nút A* đã duyệt: {a_star_explored}, Số nút DFS đã duyệt: {dfs_explored}")

start = 'A'
goal = 'E'
path, cost, a_star_explored, dfs_explored = a_star_dfs_combined(graph, start, goal)
if path:
    print(f"Đường đi từ {start} đến {goal}: {path}, Chi phí: {cost}, Số nút A* đã duyệt: {a_star_explored}, Số nút DFS đã duyệt: {dfs_explored}")
else:
    print(f"Không tìm thấy đường đi từ {start} đến {goal}, Số nút A* đã duyệt: {a_star_explored}, Số nút DFS đã duyệt: {dfs_explored}")