import re
import sys
from add_mod_rm import *
from cal_vertex_n_edges import *

class ParseException(Exception):
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return str(self._value)


def main():
    entry_n_exit(sys.stdin, sys.stdout, sys.stderr)


def entry_n_exit(inp, out, err):
    while True:

        s = inp.readline()
        s = s.replace('\n', '')

        if s == '':
            break
        elif s == "DONE":
            out.write('DONE')
            out.flush()
            break
        try:
            parse_line(s, inp, out, err)
        except ParseException as ex:
            err.write("Error: {0}\n".format(ex))
    sys.exit(0)

def parse_line(cmd, inp, out, err):
    if not cmd.startswith('add') and not cmd.startswith('mod') and not cmd.startswith('gg') and not cmd.startswith('rm'):
        raise ParseException("The string does not start with 'add' or 'mod' or 'rm' or 'gg'")
    else:
        cmd = cmd.replace("\n", '')
        data = cmd.split(" ", 1)
        if len(data[0]) == 1:
            func = data[0]
            if not cmd.startswith('gg'):
                if len(data) > 1:
                    separate = data[1].split('"(', 1)
                    if len(separate) > 1 and not cmd.startswith('rm') == 'True':
                        raise ParseException("Missing Space between street and coordinates")
                    street_temp = data[1].split('"', 2)
                    if len(street_temp) == 3:
                        street_name = street_temp[1].lower()
                        if not re.match(r'.[a-zA-Z\s]*$', street_name):
                            raise ParseException("No special character allowed in street name")
                        street = street_name.replace(' ', '_').replace('"', "")

                        street_temp[2] = street_temp[2].replace(" ", '')
                        street_temp[2] = street_temp[2].replace("\n", '')
                        raw = len(street_temp[2])
                        check_pair_coord = re.findall('\s*[-]*[0-9]+\.?[0-9]*\s*', street_temp[2])

                        if not len(check_pair_coord) % 2 == 0:
                            raise ParseException("Missing Pair X,Y of Coordinate values")

                        parsed_coord = re.findall(r'\(.*?\)', street_temp[2])
                        open_bracket = street_temp[2].count('(')
                        close_bracket = street_temp[2].count(')')

                        temp = 0
                        for i in range(0, len(parsed_coord)):
                            temp = temp + len(parsed_coord[i])

                        if not raw == temp or not open_bracket == close_bracket:
                            raise ParseException("Missing Open/Closing Brackets in coordinates")

                        street_detail = parsed_coord
                    elif len(street_temp) == 2:
                        if not street_temp[0] == '"' and not street_temp[-1] == '"':
                            raise ParseException("Please provide Street in Quotes")
                        street_name = street_temp[1].lower()
                        if not re.match(r'.[a-zA-Z\s]*$', street_name):
                            raise ParseException("No special character allowed in street name")
                        if street_name.startswith(" ") or street_name.endswith(" "):
                            raise ParseException("Street name cannot have leading or trailing whitespaces!")
                        street = street_name.replace(' ', '_').replace('"', "")
                        street = street.replace("\n", '')
                    else:
                        raise ParseException("Insufficient Data")

                    if street not in full_str_lst:
                        if func == 'add':
                            addStreet(full_str_lst, street, street_detail, city_map_dict)

                        if func == 'mod':
                            raise ParseException("'mod' specified for a street that does not exist")
                            pass
                        elif func == 'rm':
                            raise ParseException("'rm' specified for a street that does not exist")
                            pass
                    else:
                        if func == 'add':
                            raise ParseException("'a' specified for a street that already exists use 'c'")
                            pass
                        elif func == 'mod':
                            modifyStreet(full_str_lst, street, street_detail, city_map_dict)
                        elif func == 'rm':
                            removeStreet(city_map_dict, street, city_map, full_str_lst)
                else:
                    raise ParseException("Insufficient Data")
            else:
                intersection_coordinates, line_equation, intersection_coordinates_keys = calculateVertices(city_map_dict, full_str_lst, vertices,
                                                                               vdict)  # Calculate Vertices
                edges = calculatEdges(intersection_coordinates, vdict, vertices, line_equation)  # Calculate Edges
                len_v = len(vertices)
                out.write(format('V') + ' ' + format(len_v))
                out.flush()
                out.write("\nE {" + ",".join(edges) + "}\n")
                out.flush()
                vdict.clear()
                line_equation = []
                edges = []
                intersection_coordinates_keys = []
                intersection_coordinates.clear()
        else:
            raise ParseException("Please separate Function,Street and Coordinates with white spaces")


if __name__ == '__main__':
    # Declare Global Variables
    full_str_lst = []  # List to store all street names
    city_map = []  # List to store Names,Coordinates
    city_map_dict = {}
    lines = []
    vertices = {}
    vdict = {}
    edges = []
    intersection_coordinates = {}
    intersection_coordinates_keys = []
    line_equation = []
    V = ''
    main()
