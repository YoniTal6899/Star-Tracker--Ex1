
from Edge import Edge
from Point import Point

EPSILON = 0.01


class Triangle:
    def __init__(self, e1: Edge, e2: Edge, e3: Edge):
        self.e1 = e1
        self.e2 = e2
        self.e3 = e3
        self.p1=e1.p1
        self.p2=e2.p1
        self.p3= e3.p1
        self.data = {}
        self.fill_data()

    def fill_data(self):
        len_e1 = self.e1.p1.distanceTo(self.e1.p2)
        len_e2 = self.e2.p1.distanceTo(self.e2.p2)
        len_e3 = self.e3.p1.distanceTo(self.e3.p2)
        self.data.update({'e1': len_e1, 'e2': len_e2, 'e3': len_e3})

    def isSimilar(self, t) -> bool:
        t1 = [self.e1.length, self.e2.length, self.e3.length]
        t1 = sorted(t1, reverse=True)
        t2 = [t.e1.length, t.e2.length, t.e3.length]
        t2 = sorted(t2, reverse=True)
        p1 = t1[0] / t2[0]
        p2 = t1[1] / t2[1]
        p3 = t1[2] / t2[2]
        avg=(p1+p2+p3)/3
        if (abs(p1 - p2) < EPSILON and abs(p1 - p3) < EPSILON and abs(p3 - p2) < EPSILON): return [True,avg]
        return [False,0]

    def getEdges(self):
        edges = [self.e1, self.e2, self.e3]
        edges.sort(key=lambda edge: edge.length)
        return edges

    def get_common_point(self,e1:Edge,e2:Edge):
        if e2.contain_point(self.p1) and e1.contain_point(self.p1):
            return self.p1
        elif e2.contain_point(self.p2) and e1.contain_point(self.p2):
            return self.p2
        else:
            return self.p3
    def __str__(self):
        return self.data.__str__()

    def get_v(self):
        str=f"Point1: {self.p1.get_id()} \n Point2: {self.p2.get_id()} \n Point3: {self.p3.get_id()}"
        return str


if __name__ == '__main__':
    p1=Point(0,0,0)
    p2=Point(1,3,0)
    p3=Point(2,0,4)
    p4=Point(3,0,4)
    p5=Point(4,-3,0)
    p6=Point(5,-3,4)
    e1=Edge(p1,p2)
    e2=Edge(p2,p3)
    e3=Edge(p3,p1)
    e4=Edge(p4,p5)
    e5=Edge(p5,p6)
    e6=Edge(p6,p4)
    t1=Triangle(e1,e2,e3)
    t2=Triangle(e4,e5,e6)

    lst=[]
    for i in range(0,5):
        lst.append(i+1)
    print(lst.__str__())

