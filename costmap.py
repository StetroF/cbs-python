import random
import pygame
from baseClass import Point
from robot import Robot

LETHAL_OBSTACLE = 255  # 定义致命障碍的代价值

class CostMap:
    def __init__(self, size, cell_size, obstacle_count):
        self.size = size
        self.cell_size = cell_size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]  # 初始化空网格
        self.obstacle_count = obstacle_count
        self.robots: list[Robot] = []  # 跟踪机器人列表
        self.plan_path: list[Point] = []  # 路径点列表
        self.generate_grid_map()

    def generate_grid_map(self):
        """
        生成网格地图并随机添加障碍物。
        """
        height = 2  # 指定障碍物生成的行
        num_of_obstacle = min(self.size, 7)  # 障碍数量不超过网格宽度
        obstacle_list = set()

        while len(obstacle_list) < num_of_obstacle:
            x = random.randint(0, self.size - 1)
            if x not in obstacle_list:
                obstacle_list.add(x)
                self.grid[self.size - height - 1][x] = LETHAL_OBSTACLE  # 从下往上索引

    def is_valid_point(self, point: Point):
        """
        检查一个点是否在地图范围内且不是障碍物。
        """
        return (
            0 <= point.x < self.size
            and 0 <= point.y < self.size
            and self.grid[point.y][point.x] != LETHAL_OBSTACLE
        )

    def add_robot(self, robot: Robot):
        """
        添加机器人到代价地图中。
        - 如果机器人的位置在地图范围外或为障碍物，返回失败信息。
        """
        point = robot.position
        if not (0 <= point.x < self.size and 0 <= point.y < self.size):
            print(f"Invalid point: {point} is out of bounds!")
            return False
        if self.grid[point.y][point.x] == LETHAL_OBSTACLE:
            print(f"Invalid point: {point} is an obstacle!")
            return False

        self.robots.append(robot)
        return True

    def set_path(self, path: list[Point]):
        """
        设置规划路径。
        """
        self.plan_path = path

    def draw(self, screen):
        """
        绘制地图，包括网格、障碍物、机器人、目标点和路径。
        """
        # 绘制网格和障碍物
        for x in range(self.size):
            for y in range(self.size):
                rect = pygame.Rect(
                    x * self.cell_size,
                    (self.size - y - 1) * self.cell_size,  # 调整 y 坐标方向
                    self.cell_size,
                    self.cell_size,
                )
                if self.grid[y][x] == LETHAL_OBSTACLE:  # 障碍物
                    pygame.draw.rect(screen, (0, 0, 0), rect)
                else:  # 空闲空间
                    pygame.draw.rect(screen, (255, 255, 255), rect)
                pygame.draw.rect(screen, (200, 200, 200), rect, 1)  # 绘制网格边框

        # 绘制规划路径
        if self.plan_path:
            for i in range(len(self.plan_path) - 1):
                start = self.plan_path[i]
                end = self.plan_path[i + 1]
                start_pixel = (
                    start.x * self.cell_size + self.cell_size // 2,
                    (self.size - start.y - 1) * self.cell_size + self.cell_size // 2,
                )
                end_pixel = (
                    end.x * self.cell_size + self.cell_size // 2,
                    (self.size - end.y - 1) * self.cell_size + self.cell_size // 2,
                )
                pygame.draw.line(screen, (0, 255, 0), start_pixel, end_pixel, 3)  # 绘制路径线段

        # 绘制机器人及其目标点
        for robot in self.robots:
            position = robot.position
            if not self.is_valid_point(position):
                print(f"Skipping invalid robot position: {position}")
                continue  # 跳过无效位置的机器人

            # 绘制机器人
            robot_rect = pygame.Rect(
                position.x * self.cell_size,
                (self.size - position.y - 1) * self.cell_size,  # 调整 y 坐标方向
                self.cell_size,
                self.cell_size,
            )
            pygame.draw.ellipse(screen, (0, 0, 255), robot_rect)  # 用椭圆表示机器人

            # 绘制目标点
            robot_goal = robot.get_goal()
            if self.is_valid_point(robot_goal):
                robot_goal_rect = pygame.Rect(
                    robot_goal.x * self.cell_size,
                    (self.size - robot_goal.y - 1) * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(screen, (255, 0, 0), robot_goal_rect, 3)  # 红框表示目标点
            else:
                print(f"Skipping invalid robot goal: {robot_goal}")
