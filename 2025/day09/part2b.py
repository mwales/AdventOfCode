#!/usr/bin/env python3

'''
With the points so spread out, storing the entire grid in a 2D array becomes
problematic.  Even if we use a dictionry and just store the points, we later
want to fill the inside, which creates the same problem.  This solution
simplifies that data set by condensing the points into a much tighter collection
for the purposes of filling in the area inside. So for each point we keep
the condesed x-y coordinates (for filling / determining which squares are valid)
and the real x-y coordinates for measuring the area.
'''

import sys


def debug(msg):
    if True:
        sys.stderr.write(f"{msg}\n")

class Point:
    def __init__(self, x, y, real_x, real_y):
        self.x = x
        self.y = y
        self.real_x = real_x
        self.real_y = real_y

    def add(self, otherPoint):
        self.x += otherPoint.x
        self.y += otherPoint.y
        self.real_x += otherPoint.real_x
        self.real_y += otherPoint.real_y

    def area(self, otherPoint):
        area = abs(self.real_x - otherPoint.real_x) + 1
        area *= abs(self.real_y - otherPoint.real_y) + 1
        #debug(area)
        return area

    def __repr__(self):
        return f"({self.x},{self.y}  but really {self.real_x},{self.real_y})"


class Grid:
    def __init__(self, point_list):
        self.min_x = point_list[0].x
        self.max_x = self.min_x
        self.min_y = point_list[1].y
        self.max_y = self.min_y

        for p in point_list:
            self.min_x = min(self.min_x, p.x)
            self.max_x = max(self.max_x, p.x)
            self.min_y = min(self.min_y, p.y)
            self.max_y = max(self.max_y, p.y)

        self.width = self.max_x - self.min_x
        self.height = self.max_y - self.min_y

        debug(f"Grid X min = {self.min_x} to {self.max_x} with width of {self.width}")
        debug(f"Grid Y min = {self.min_y} to {self.max_y} with height of {self.height}")
        self.fill_grid = dict()

        for i in range(0, len(point_list)):
            prev_point = point_list[i-1]
            cur_point = point_list[i]

            # is horizontal?
            if prev_point.x == cur_point.x:
                # vertical line
                start_y = min(prev_point.y, cur_point.y)
                end_y = max(prev_point.y, cur_point.y)
                for y in range(start_y, end_y + 1):
                    self.fill_grid[ (cur_point.x, y) ] = 'X'
            elif prev_point.y == cur_point.y:
                # horizontal line
                start_x = min(prev_point.x, cur_point.x)
                end_x = max(prev_point.x, cur_point.x)
                for x in range(start_x, end_x + 1):
                    self.fill_grid[ (x, cur_point.y) ] = 'X'
            else:
                # diagnol!!!!
                print("Encountered unexpected diagnol line!")
                print("Prev point {prev_point} and current point {cur_point}")


        self.point_list = point_list

    def getVal(self, pt):
        if pt.x < 0 or pt.x >= self.width:
            return None

        if pt.y < 0 or pt.y >= self.height:
            return None

        return self.grid[ (pt.x, pt.y) ]

    def setVal(self, pt, val):
        if pt.x < 0 or pt.x >= self.width:
            return

        if pt.y < 0 or pt.y >= self.height:
            return

        self.grid[ (pt.x, pt.y) ] = val

    def drawGrid(self):
        for y in range(self.min_y, self.max_y + 1):
            cur_row = ""
            for x in range(self.min_x, self.max_x + 1):
                cur_char = self.fill_grid.get( (x,y), ' ')  
                cur_row += cur_char
            print(cur_row)

    def fillGrid(self):
        # Find the topmost horizontal segment, and fill in 1 pixel below the halfway point
        for i in range(len(self.point_list)):
            cur_point = self.point_list[i]
            prev_point = self.point_list[i-1]
            if cur_point.y == 0 and prev_point.y == 0:
                fill_x = (cur_point.x + prev_point.x) // 2
                fill_point = (fill_x, 1) 

        self.fillGridFromPoint(fill_point)

    def fillGridFromPoint(self, p):
        #debug(f"fillGridFromPoint( {p} )")
        points_to_try = [ p ]

        while len(points_to_try) > 0:
            next_point = points_to_try.pop()
            #debug(f"Filling at {next_point}")
           
            next_x, next_y = next_point
            if next_x < self.min_x or next_x > self.max_x:
                continue
            if next_y < self.min_y or next_y > self.max_y:
                continue

            # Has this point already been filled in?
            if self.fill_grid.get(next_point, ' ') == 'X':
                continue

            # Fill me in and add the neighbors
            self.fill_grid[next_point] = 'X'

            # Add the neighbors
            points_to_try.append( (next_x - 1, next_y) )
            points_to_try.append( (next_x + 1, next_y) )
            points_to_try.append( (next_x, next_y - 1) )
            points_to_try.append( (next_x, next_y + 1) )

            #self.drawGrid()

    def isAreaFilled(self, p1, p2):
        start_x = min(p1.x, p2.x)
        stop_x = max(p1.x, p2.x)
        start_y = min(p1.y, p2.y)
        stop_y = max(p1.y, p2.y)
        for y in range(start_y, stop_y + 1):
            for x in range(start_x, stop_x + 1):
                if self.fill_grid.get( (x,y), ' ' ) != 'X':
                    return False
        return True

def get_sim_value(real_value, full_list):
    return full_list.find(real_value)


def main(argv):

    if (len(argv) < 2):
        print("Usage: {} inputfile".format(sys.argv[0]))
        return

    f = open(argv[1])
    data = f.read().strip().split("\n")
    f.close()

    pointList = []
    for singleLine in data:
        p = tuple([ int(x) for x in singleLine.split(",") ])
        pointList.append(p)

    debug(pointList)

    # Resolution of coordinated are way to spread out, makes the it difficult to fill
    # Reduce resolution by converting a list of 100, 300, 450, 900 to basically 0, 1, 2, 3 
    x_set = set()
    y_set = set()

    for p in pointList:
        x_set.add(p[0])
        y_set.add(p[1])

    # Lets create the grid object which can do the fill
    x_list = list(x_set)
    y_list = list(y_set)

    x_list.sort()
    y_list.sort()

    point_list_2 = []

    for p in pointList:
        sim_x = x_list.index(p[0]) * 1 
        sim_y = y_list.index(p[1]) * 1 
        p_obj = Point(sim_x, sim_y, p[0], p[1])
        point_list_2.append(p_obj)

    debug(f"Grid points that are scaled: {point_list_2}")

    g = Grid(point_list_2)
    #g.drawGrid()

    g.fillGrid()

    g.drawGrid()

    area_list = []
    for i in range(len(pointList)):
        for j in range(len(pointList)):
            if i == j:
                continue
            p1 = point_list_2[i]
            p2 = point_list_2[j]
            area = p1.area(p2)

            area_list.append( (area, i, j) )

    area_list.sort()
    area_list.reverse()
    #print(area_list)

    for area_data in area_list:
        area, p1_index, p2_index = area_data
        p1 = point_list_2[p1_index]
        p2 = point_list_2[p2_index]
        if g.isAreaFilled(p1,p2):
            print(f"Solution {area}")
            break

if __name__ == "__main__":
    main(sys.argv)
