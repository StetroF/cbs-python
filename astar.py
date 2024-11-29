from baseClass import Point,neighbour_list
from robot import Robot
from costmap import LETHAL_OBSTACLE,CostMap
import time
import heapq

class AstarPlanner:
    def __init__(self,costMap):
        self.costMap:CostMap = costMap
        

    def plan(self, robot: Robot):
        """
        基于A*算法的路径规划。
        """
        start = Point(robot.position.x, robot.position.y)
        goal = robot.get_goal()

        # 优先队列存储 (f_cost, g_cost, 当前节点, 父节点)
        open_list = []
        heapq.heappush(open_list, (0, 0, start, None))

        # 记录已访问的节点和路径信息
        came_from = {}  # 用于记录每个节点的父节点
        g_costs = {start: 0}  # 起点到各节点的实际代价
        closed_set = set()  # 已经处理过的节点

        while open_list:
            # 取出 f_cost 最小的节点
            _, curr_g_cost, curr, parent = heapq.heappop(open_list)

            if curr in closed_set:
                continue
            closed_set.add(curr)
            came_from[curr] = parent

            print(f"当前节点: {curr.x}, {curr.y}")

            # 如果到达目标点，则重构路径
            if curr == goal:
                print("Goal reached!")
                path = self.reconstruct_path(came_from, goal)
                print(f"路径列表: {[{'x': p.x, 'y': p.y} for p in path]}")
                return path

            # 遍历邻居节点
            for neighbour in self.get_neighbour(curr):
                if neighbour in closed_set:
                    continue

                tentative_g_cost = curr_g_cost + 1  # 当前节点到邻居的代价（假设网格每步代价为1）
                if neighbour not in g_costs or tentative_g_cost < g_costs[neighbour]:
                    g_costs[neighbour] = tentative_g_cost
                    h_cost = self.get_h_cost(neighbour, goal)
                    f_cost = tentative_g_cost + h_cost

                    # 将邻居加入优先队列
                    heapq.heappush(open_list, (f_cost, tentative_g_cost, neighbour, curr))

        print("未找到路径")
        return []  # 如果没有找到路径，返回空列表
    def get_h_cost(self,input_point:Point,goal_point:Point):
        return abs(input_point.x-goal_point.x) + abs(input_point.y-goal_point.y)
    
    def get_neighbour(self,current_point:Point)->list[Point]:
        neighbours = []
        
        
        ###向周围4个方向拓展
        for candinate in neighbour_list:
            candinate_point = Point(current_point.x+candinate[0],current_point.y+candinate[1])
            if self.costMap.is_valid_point(candinate_point):
                neighbours.append(candinate_point)
            
        return neighbours
    