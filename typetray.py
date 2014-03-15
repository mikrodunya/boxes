#!/usr/bin/python

from boxes import *

class BottomEdge(FingerJointEdge):
    def __init__(self, boxes, sections, slot=0):
        FingerJointEdge.__init__(self, boxes, None)
        self.sections = sections
        self.slot = slot

    def _slot(self):
        if self.slot:
            self.boxes.corner(90)
            self.boxes.edge(self.slot)
            self.boxes.corner(-90)
            self.boxes.edge(self.thickness)
            self.boxes.corner(-90)
            self.boxes.edge(self.slot)
            self.boxes.corner(90)
        else:
            self.boxes.edge(self.thickness)

    def __call__(self, l, **kw):
        for x in self.sections[:-1]:
            self.boxes.fingerJointEdge(x)
            self._slot()
        self.boxes.fingerJointEdge(self.sections[-1])

class TopEdge(BottomEdge):
    

    margin = Edge.margin
    width = Edge.width

    def __call__(self, l, **kw):
        for x in self.sections[:-1]:
            self.boxes.edge(x)
            self._slot()
        self.boxes.edge(self.sections[-1])

class TypeTray(Boxes):
    def __init__(self, x, y, h, hi=None, **kw):
        self.x, self.y, self.h = x, y, h
        self.hi = hi or h
        Boxes.__init__(self, width=sum(x)+sum(y)+70, height=sum(y)+8*h+50, **kw)

    def xSlots(self):
        posx = -0.5 * self.thickness
        for x in self.x[:-1]:
            posx += x + self.thickness
            posy = 0
            for y in self.y:
                self.fingerHolesAt(posx, posy, y)
                posy += y + self.thickness

    def ySlots(self):
        posy = -0.5 * self.thickness
        for y in self.y[:-1]:
            posy += y + self.thickness
            posx = 0
            for x in self.x:
                self.fingerHolesAt(posy, posx, x)
                posx += x + self.thickness

    def xHoles(self):
        posx = -0.5 * self.thickness
        for x in self.x[:-1]:
            posx += x + self.thickness
            self.fingerHolesAt(posx, 0, self.hi)

    def yHoles(self):
        posy = -0.5 * self.thickness
        for y in self.y[:-1]:
            posy += y + self.thickness
            self.fingerHolesAt(posy, 0, self.hi)

    def fingerHole(self):
        dx = 50
        dy = 30
        x = sum(self.x) + self.thickness * (len(self.x)-1)
        self.moveTo(0.5*(x-dx), 5)
        self.edge(dx)
        self.corner(180, 0.5*dy)
        self.edge(dx)
        self.corner(180, 0.5*dy)
        #self.hole(0.5*x-30, 15, 10)
        #self.hole(0.5*x+30, 15, 10)

    def render(self):
        x = sum(self.x) + self.thickness * (len(self.x)-1)
        y = sum(self.y) + self.thickness * (len(self.y)-1)
        h = self.h
        hi = self.hi
        t = self.thickness

        self.moveTo(t, t)
        # outer walls
        self.rectangularWall(x, h, "Ffef", callback=[
            self.xHoles, None, self.fingerHole],
                             move="right")
        self.rectangularWall(y, h, "FFeF",  callback=[self.yHoles,],
                             move="up")
        self.rectangularWall(y, h, "FFeF", callback=[self.yHoles,])
        self.rectangularWall(x, h, "Ffef", callback=[self.xHoles,],
                             move="left up")
        
        # floor
        self.rectangularWall(x, y, "ffff",
                             callback=[self.xSlots, self.ySlots],
                             move="right")
        # Inner walls
        for i in range(len(self.x)-1):
            e = [BottomEdge(self, self.y, 0.5*hi), "f", "e", "f"]
            self.rectangularWall(y, hi, e,
                                 move="up")
        for i in range(len(self.y)-1):
            e = [BottomEdge(self, self.x), "f",
                 TopEdge(self, self.x, 0.5*hi), "f"]
            self.rectangularWall(x, hi, e,
                                 move="up")

        self.ctx.stroke()
        self.surface.flush()
        self.surface.finish()

x = 260
nx = 3
y = 300
ny = 4
thickness=4.0

dx = (x-thickness)/nx-thickness
dy = (y-thickness)/ny-thickness
sx = [dx] * nx
#sy = [dy] * ny
sy = [120, 300-3*thickness-120]

b = TypeTray(sx, sy, 78-thickness, 40, thickness=thickness, burn=0.1)
b.edges["f"].settings.setValues(b.thickness, space=3, finger=3,
                                surroundingspaces=0.5)
b.render()