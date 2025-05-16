class PlatformGraph:
    def __init__(self):
        self.nodes = {}  # node_id -> (x, y)
        self.edges = {}  # node_id -> list of neighbor ids

    def build_platform_graph(self, tmx_data):
        self.nodes.clear()
        self.edges.clear()

        node_id = 0
        tile_width = tmx_data.tilewidth

        # Tìm objectgroup "triggers"
        for obj_group in tmx_data.objectgroups:
            if obj_group.name == "triggers":
                for obj in obj_group:
                    if obj.name == "gnd":
                        x_start = int(obj.x)
                        x_end = int(obj.x + obj.width)
                        y = int(obj.y)

                        # Chia platform thành các node mỗi 32px
                        for x in range(x_start, x_end, 16):
                            cx = x + 16  # center x of node
                            cy = y - 16  # center y (trên mặt đất)
                            self.nodes[node_id] = (cx, cy)

                            if node_id - 1 in self.nodes:
                                # nối với node trước cùng platform
                                self.edges.setdefault(node_id - 1, []).append(node_id)
                                self.edges.setdefault(node_id, []).append(node_id - 1)

                            node_id += 1

    def get_closest_node(self, x, y):
        closest_id = None
        min_dist = float('inf')
        for node_id, (nx, ny) in self.nodes.items():
            dist = ((nx - x) ** 2 + (ny - y) ** 2) ** 0.5
            if dist < min_dist:
                min_dist = dist
                closest_id = node_id
        return closest_id
    
def find_nearest_node(x, y, nodes):
    closest_id = None
    min_dist = float('inf')
    for node_id, center in nodes.items():
        cx, cy = center
        dist = ((cx - x) ** 2 + (cy - y) ** 2) ** 0.5
        if dist < min_dist:
            min_dist = dist
            closest_id = node_id
    return closest_id
    