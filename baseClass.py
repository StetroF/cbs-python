class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __eq__(self, obj):
        return isinstance(obj, Point) and self.x == obj.x and self.y == obj.y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __hash__(self):
        """
        使用 Python 内置的 hash 函数，确保 Point 对象可以被哈希。
        """
        return hash((self.x, self.y))
    def __lt__(self, other):
        # 自定义排序规则，比如优先比较 x，其次比较 y
        return (self.x, self.y) < (other.x, other.y)
####四个方向的相邻点
neighbour_list = [
    [-1,0],
    [1,0],
    [0,-1],
    [0,1]
]