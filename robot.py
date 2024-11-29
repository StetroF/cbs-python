from baseClass import Point

class Robot:
    def __init__(self, point:Point):
        self.position = Point(point.x, point.y)
        self.__goal:Point|None = None
    
    
    def set_goal(self,goal:Point):
        self.__goal = goal
    
    def get_goal(self):
        return self.__goal
    
    def move(self,dx,dy):
        self.position.x += dx
        self.position.y += dy
        #test