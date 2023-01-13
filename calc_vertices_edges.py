import math
#creating class for using global variables all over
class Vertex_Edge():
    v = []
    points_index = {}
    street_dict = {}
    lines = []
    intersections = []
    line_intersections = {}
    edges_list = []
    vertices = set()
    def __init__(self,streets):
        self.street_dict = streets

    def get_vertices_edges(self):
        self.intersections = []
        self.lines = []
        self.line_intersections = {}
        self.points_index = {}
        self.edges_list = []
        self.vertices.clear()
        self.convert_to_float()
        self.set_line_segments()
        for i in range(len(self.lines)):
            for j in range(i + 1, len(self.lines)):
                self.validate_intersection(self.lines[i], self.lines[j])
        for k, v in self.line_intersections.items():
            if (k[0], v[0]) not in self.edges_list and (v[0], k[0]) not in self.edges_list and (v[0] != k[0]):
                self.edges_list.append((k[0], v[0]))
            for i in range(0, len(v) - 1):
                if ((v[i], v[i + 1]) not in self.edges_list and (v[i + 1], v[i]) not in self.edges_list and (
                        v[i] != v[i + 1])):
                    self.edges_list.append((v[i], v[i + 1]))
            if ((k[1], v[len(v) - 1]) not in self.edges_list and (v[len(v) - 1], k[1]) not in self.edges_list and (
                    v[len(v) - 1] != k[1])):
                self.edges_list.append((k[1], v[len(v) - 1]))

        print("V = {")
        k = 1
        for vertex in self.vertices:
            print("{0} : ({1},{2})".format(k, float(vertex[0]), float(vertex[1])))
            k += 1
            self.points_index[k] = vertex
        print("}")
        #key_list = list(self.points_index.keys())
        val_list = list(self.points_index.values())
        print("E = {")
        for i in self.edges_list:
            print("<{0},{1}>".format(val_list.index(i[0]) + 1, val_list.index(i[1]) + 1))
        print("}")

    def set_line_segments(self):
        for k, v in self.street_dict.items():
            for i in range(len(v) - 1):
                self.lines.append([(v[i][0], v[i][1]), (v[i + 1][0], v[i + 1][1])])

    def convert_to_float(self):
        for k, v in self.street_dict.items():
            length = len(v)
            for i in range(length):
                if isinstance(v[0], tuple):
                    break
                coord = v[0].split(',')
                x_coord = float(coord[0][1:])
                y_coord = float(coord[1][:len(coord[1]) - 1])

                self.street_dict[k].remove(v[0])
                self.street_dict[k].append((x_coord, y_coord))

    def validate_intersection(self, line1, line2):
        if not self.if_parallel(line1, line2):
            intersection_point = self.find_line_intersection(line1, line2)
            x_coord = intersection_point[0]
            y_coord = intersection_point[1]
            x_range = [max(min(line1[0][0], line1[1][0]), min(line2[0][0], line2[1][0])),
                       min(max(line1[0][0], line1[1][0]), max(line2[0][0], line2[1][0]))]
            if min(x_range) <= x_coord <= max(x_range):
                dist = self.get_distance(line1[0][0], line1[0][1], line1[1][0], line1[1][1])
                dist1 = self.get_distance(line1[0][0], line1[0][1], x_coord, y_coord)
                dist2 = self.get_distance(x_coord, y_coord, line1[1][0], line1[1][1])
                if dist1 > dist or dist2 > dist:
                    pass
                else:
                    if (intersection_point not in line1 and intersection_point not in line2):
                        if intersection_point not in self.intersections:
                            self.intersections.append(intersection_point)
                            self.vertices.add(intersection_point)
                        self.vertices.add(line1[0])
                        self.vertices.add(line1[1])
                        self.vertices.add(line2[0])
                        self.vertices.add(line2[1])
                        if tuple(line1) not in self.line_intersections:
                            self.line_intersections[tuple(line1)] = [intersection_point]
                        else:
                            if intersection_point not in self.line_intersections[tuple(line1)]:
                                self.line_intersections[tuple(line1)].append(intersection_point)
                        if tuple(line2) not in self.line_intersections:
                            self.line_intersections[tuple(line2)] = [intersection_point]
                        else:
                            if intersection_point not in self.line_intersections[tuple(line2)]:
                                self.line_intersections[tuple(line2)].append(intersection_point)
                return True
            else:
                return False
        else:
            try:
                slope1 = (line1[1][1] - line1[0][1]) / (line1[1][0] - line1[0][0])
                slope2 = (line2[1][1] - line2[0][1]) / (line2[1][0] - line2[0][0])
                y_int1 = line1[0][1] - (slope1 * line1[0][0])
                y_int2 = line2[0][1] - (slope2 * line2[0][0])
            except:
                slope1 = 0
                slope2 = 0
                y_int1 = line1[0][0] - (slope1 * line1[0][0])
                y_int2 = line2[0][0] - (slope2 * line2[0][0])
            if (slope1 == slope2) and (y_int1 == y_int2):
                p = line1[0]
                if (self.in_range(p, line2)):
                    self.add_intersection_point_to_vertices(p, line2)
                p = line1[1]
                if (self.in_range(p, line2)):
                    self.add_intersection_point_to_vertices(p, line2)
                p = line2[0]
                if (self.in_range(p, line1)):
                    self.add_intersection_point_to_vertices(p, line1)
                p = line2[1]
                if (self.in_range(p, line1)):
                    self.add_intersection_point_to_vertices(p, line1)
                return True
            return False

    def if_parallel(self, line1, line2):
        if self.get_slope(line1) != self.get_slope(line2):
            return False
        return True

    def find_line_intersection(self, line1, line2):
        if not self.if_parallel(line1, line2):
            if self.get_slope(line1) is not None and self.get_slope(line2) is not None:
                x_coord = ((line2[0][1] - (self.get_slope(line2) * line2[0][0])) - (line1[0][1] - (self.get_slope(line1) * line1[0][0]))) / (self.get_slope(line1) - self.get_slope(line2))
                y_coord = (self.get_slope(line1) * x_coord) + (line1[0][1] - (self.get_slope(line1) * line1[0][0]))
            else:
                if self.get_slope(line1) is None:
                    x_coord = line1[0][0]
                    y_coord = (self.get_slope(line2) * x_coord) + (line2[0][1] - (self.get_slope(line2) * line2[0][0]))
                elif self.get_slope(line2) is None:
                    x_coord = line2[0][0]
                    y_coord = (self.get_slope(line1) * x_coord) + (line1[0][1] - (self.get_slope(line1) * line1[0][0]))
            x_coord = float("{0:.2f}".format(x_coord))
            y_coord = float("{0:.2f}".format(y_coord))
            return (x_coord, y_coord)
        else:
            return False

#    def get_intersect(self, line):
#        return line[0][1] - (self.get_slope(line) * line[0][0])

    def get_slope(self, l):
        m = None
        if l[0][0] != l[1][0]:
            m = (l[0][1] - l[1][1])/(l[0][0] - l[1][0])
            return m

    def get_distance(self, x1, y1, x2, y2):
        dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return dist


    def add_intersection_point_to_vertices(self, intersection_point, line1):
        self.vertices.add(line1[0])
        self.vertices.add(line1[1])
        if intersection_point not in self.intersections:
            self.intersections.append(intersection_point)
        if tuple(line1) not in self.line_intersections:
            self.line_intersections[tuple(line1)] = [intersection_point]
        else:
            if intersection_point not in self.line_intersections[tuple(line1)]:
                self.line_intersections[tuple(line1)].append(intersection_point)

    def in_range(self, point, line):
        if (point[0] == line[0][0] and point[0] == line[1][0]):

            if (point[1] >= line[0][1] and point[1] <= line[1][1]):
                return True
            elif (point[1] >= line[1][1] and point[1] <= line[0][1]):
                return True
            return False

        if (point[0] >= line[0][0] and point[0] <= line[1][0]):
            return True
        elif (point[0] >= line[1][0] and point[0] <= line[0][0]):
            return True
        return False