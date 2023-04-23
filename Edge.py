import numpy as np


class Edge:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.v = np.array([[self.p1.x, self.p1.y], [self.p2.x, self.p2.y]])
        self.id=str(self.p1.id)+","+str(self.p2.id)
        self.length = self.p1.distanceTo(self.p2)


    def contain_point(self,p):
        if(p==self.p1 or p==self.p2):
            return True
        return False

