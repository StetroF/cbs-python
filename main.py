import pygame
import sys
from baseClass import Point
from costmap import CostMap  # 导入 CostMap 类
from robot import Robot  # 导入 Robot 类
from astar import AstarPlanner
import time
# 初始化 Pygame
pygame.init()

# 网格和窗口设置
GRID_SIZE = 10
CELL_SIZE = 50
WINDOW_SIZE = GRID_SIZE * CELL_SIZE

# 初始化 Pygame 窗口
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("动态网格地图与机器人")

# 主函数
def main():
    clock = pygame.time.Clock()
    costmap = CostMap(GRID_SIZE, CELL_SIZE, obstacle_count=15)  # 初始化 CostMap 类
    robot1 = Robot(Point(0, 0))  # 创建一个初始位置在 (0, 0) 的机器人
    robot1.set_goal(Point(3, 9))

    costmap.add_robot(robot1)  # 将机器人添加到 CostMap 中
    planner = AstarPlanner(costmap)  # 初始化 A* 规划器
    plan_path = planner.plan(robot1)  # 规划机器人的路径
    
    costmap.set_path(plan_path)  # 设置路径

    running = True
    looping = True
    time = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            dx = 0
            dy = 0

            ###让robot沿着plan_path移动
            # if looping:
            #     for path_point in plan_path:
            #         robot1.set_pose(path_point)
            #         costmap.add_robot(robot1)  # 更新机器人的位置
            # # 按 'd' 键让 robot1 向右移动
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                time+=1
                if time < len(plan_path):
                    robot1.set_pose(plan_path[time])
                    costmap.add_robot(robot1)  # 更新机器人的位置
                else:
                    pass
                # # 移动机器人
                # if robot1.position.x < GRID_SIZE - 1:
                #     dx = 1
                #     robot1.move(dx, dy)
                #     costmap.add_robot(robot1)  # 更新机器人的位置
                # else:
                #     print("机器人已经到了右边的边界!")

        # 绘制地图和路径
        costmap.draw(screen)  # 将路径传递给 draw 方法

        # 更新显示
        pygame.display.flip()

        # 控制刷新率
        clock.tick(30)

# 运行程序
if __name__ == "__main__":
    main()
