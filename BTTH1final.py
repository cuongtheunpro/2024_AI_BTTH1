import heapq

class Node:
    def __init__(self, state, parent=None, cost=0, heuristic=0):
        self.state = state  # Lưu trữ trạng thái của nút (ví dụ: 'A', 'B')
        self.parent = parent  # Lưu trữ nút cha của nút này trong đường đi
        self.cost = cost      # Chi phí từ nút bắt đầu đến nút này (g trong A*)
        self.heuristic = heuristic # Ước lượng chi phí từ nút này đến đích (h trong A*)
        self.f_score = cost + heuristic # Tổng chi phí ước tính (f = g + h)

    def __lt__(self, other): # Định nghĩa cách so sánh hai nút dựa trên f_score
        return self.f_score < other.f_score

def heuristic_func(state, goal):
    """
    Khai báo hàm heuristic  .
    """
    return abs(ord(goal) - ord(state)) # Trả về giá trị tuyệt đối của hiệu mã ASCII

def a_star_dfs_combined(graph, start, goal, split_ratio=0.5):
    """
    Kết hợp thuật toán A* và DFS để tìm đường đi.

    Args:
        graph: Đồ thị dưới dạng từ điển (danh sách kề).
        start: Nút bắt đầu.
        goal: Nút đích.
        split_ratio: Tỉ lệ số nút được duyệt bằng A*.

    Returns:
        Tuple chứa (đường đi, chi phí, số nút A* đã duyệt, số nút DFS đã duyệt), hoặc (None, None, 0, 0) nếu không tìm thấy đường đi.
    """
    total_nodes = len(graph) # Tổng số nút trong đồ thị
    a_star_nodes_limit = int(total_nodes * split_ratio) # Số nút tối đa được duyệt bằng A*
    a_star_nodes_explored = 0 # Biến đếm số nút đã duyệt bằng A*
    dfs_nodes_explored = 0 # Biến đếm số nút đã duyệt bằng DFS
    open_set = [] # Tập hợp các nút cần được xét (hàng đợi ưu tiên cho A*)
    stack = [] # Ngăn xếp cho DFS
    visited = set() # Tập hợp các nút đã được xét
    heapq.heappush(open_set, Node(start, None, 0, heuristic_func(start, goal))) # Thêm nút bắt đầu vào open_set

    # Giai đoạn 1: Tìm kiếm A*
    for _ in range(a_star_nodes_limit): # Lặp tối đa a_star_nodes_limit lần
        if not open_set: # Nếu open_set rỗng, kết thúc vòng lặp
            break
        current_node = heapq.heappop(open_set) # Lấy nút có f_score nhỏ nhất từ open_set
        if current_node.state in visited: # Nếu nút này đã được xét, bỏ qua
            continue
        visited.add(current_node.state) # Đánh dấu nút này là đã xét
        a_star_nodes_explored += 1
        if current_node.state == goal: # Nếu nút hiện tại là đích, trả về đường đi
            path = reconstruct_path(current_node)
            return path, current_node.cost, a_star_nodes_explored, dfs_nodes_explored

        for neighbor, cost in graph.get(current_node.state, []): # Duyệt các nút kề
            if neighbor not in visited: # Nếu nút kề chưa được xét
                heapq.heappush(open_set, Node(neighbor, current_node, current_node.cost + cost, heuristic_func(neighbor, goal)))

    # Giai đoạn 2: Tìm kiếm DFS
    stack.extend(open_set) # Chuyển các nút còn lại trong open_set sang stack
    while stack: # Lặp cho đến khi stack rỗng
        current_node = stack.pop() # Lấy nút từ đỉnh stack
        if current_node.state in visited: # Nếu nút này đã được xét, bỏ qua
            continue
        visited.add(current_node.state) # Đánh dấu nút này là đã xét
        dfs_nodes_explored += 1
        if current_node.state == goal: # Nếu nút hiện tại là đích, trả về đường đi
            path = reconstruct_path(current_node)
            return path, current_node.cost, a_star_nodes_explored, dfs_nodes_explored

        for neighbor, cost in graph.get(current_node.state, []): # Duyệt các nút kề
            if neighbor not in visited: # Nếu nút kề chưa được xét
                stack.append(Node(neighbor, current_node, current_node.cost + cost))

    return None, None, a_star_nodes_explored, dfs_nodes_explored # Trả về None nếu không tìm thấy đường đi

def reconstruct_path(node):
    """
    Tái tạo đường đi từ nút đích về nút bắt đầu.
    """
    path = []
    while node: # Lặp cho đến khi nút là None (đã đến nút bắt đầu)
        path.append(node.state) # Thêm trạng thái của nút vào đường đi
        node = node.parent # Di chuyển lên nút cha
    return path[::-1] # Đảo ngược đường đi để có thứ tự từ bắt đầu đến đích

# 5 cấu hình khác nhau
configurations = [
    {"graph": { # Cấu hình 1 (Đồ thị đơn giản)
        'A': [('B', 1), ('C', 2)],
        'B': [('D', 1)],
        'C': [('D', 3)],
        'D': []
    }, "start": 'A', "goal": 'D', "split_ratio": 0.5},
    {"graph": { # Cấu hình 2 (Đồ thị phức tạp hơn)
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
    }, "start": 'A', "goal": 'G', "split_ratio": 0.3},
    {"graph": { # Cấu hình 3 (Đồ thị phức tạp hơn, đích là nút cụt)
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
    }, "start": 'A', "goal": 'K', "split_ratio": 0.7},
    {"graph": { # Cấu hình 4 (Đồ thị đơn giản hơn)
        'A': [('B', 1), ('C', 3)],
        'B': [('D', 2)],
        'C': [],
        'D': []
    }, "start": 'A', "goal": 'D', "split_ratio": 0.5},
        {"graph": { # Cấu hình 5 (Đồ thị phức tạp hơn, thay đổi điểm bắt đầu)
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
    }, "start": 'B', "goal": 'G', "split_ratio": 0.5},
]

# Chạy demo với 5 cấu hình
for i, config in enumerate(configurations):
    print(f"\n--- Cấu hình {i+1} ---")
    print(f"Đồ thị: {config['graph']}")
    print(f"Bắt đầu: {config['start']}")
