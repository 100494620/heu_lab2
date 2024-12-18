from constraint import *
import os
import sys
from collections import Counter

class Plane:
    def __init__(self, id, tipo, restr, t1, t2):
        self.id = id
        self.tipo = tipo
        self.restr = restr
        self.t1 = t1
        self.t2 = t2

    def __lt__(self, other):
        return self.id < other.id

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]

def read_data():
    if len(sys.argv) != 2:
        print("Incorrect amount of arguments")
        sys.exit(1)

    file_path = sys.argv[1]

    if not os.path.isfile(file_path):
        print(f"File '{file_path}' not found.")
        sys.exit(1)

    data = read_input_file(file_path)
    #print(data)
    return data

def parse_string(data, i):
    pos_string = data[i].split(":")[1].strip()
    positions = []
    for pos in pos_string.split():
        positions.append(tuple(map(int, pos.strip("()").split(","))))
    return positions

def parse_data(data):
    franjas = int(data[0].split(":")[1].strip())

    matrix_size = tuple(map(int, data[1].split("x")))

    std_positions = parse_string(data, 2)
    spc_positions = parse_string(data, 3)
    prk_positions =parse_string(data, 4)

    planes = []
    for plane_info in data[5:]:
        info = plane_info.strip().split("-")
        planes.append(Plane(info[0], info[1], info[2], info[3], info[4]))
    #print(prk_positions)
    return franjas, matrix_size, std_positions, spc_positions, prk_positions, planes


def franja_capacity(*args):
    # problem.addConstraint(jmb_adjacent, variables_to_time[i])
    # 0: (plane_0,0), (plane_1,0), (plane_2,0)
    #   (pos_plane0_0), (pos_plane1_0), (pos_plane2_0)
    # each taller can assist no more than 2 planes in one time slot
    if any(count > 2 for count in Counter(args).values()):
        return False
    return True

def taller_capacity(*args):
    # there is no JUMBO planes in the same time slot at the same taller
    if any(count > 1 for count in Counter(args).values()):
        return False
    return True

def main():
    problem = Problem()
    franjas, matrix_size, std_positions, spc_positions, prk_positions, planes = parse_data(read_data())

    variables = [] # [(plane: Plane, time_slot: int)]
    # problem.constraints: [((plane: Plane, time_slot: int), [pos, pos])]

    positions = std_positions + spc_positions + prk_positions

    # set values
    for plane in planes:
        for franja in range(0, franjas):
            variables.append((plane, franja))

    variables_to_time = {}
    jumbo_to_time = {}
    #0: (plane_0,0), (plane_1,0), (plane_2,0)
    #1: (plane_0,1), (plane_1,1), (plane_2,1)
    # ....

    for var in variables:
        if var[1] not in variables_to_time:
            variables_to_time[var[1]] = []
        variables_to_time[var[1]].append(var)

        if var[0].tipo == "JMB" and var[1] not in jumbo_to_time:
            jumbo_to_time[var[1]] = []
        jumbo_to_time[var[1]].append(var)

    # assures that all planes will be assigned to the unique taller/parking in each time slot
    for var in variables:
        problem.addVariable(var, positions)

    # variable - (plane, time-slot)
    # map <int time slot, planes>
    for i in range(0, franjas):
        problem.addConstraint(franja_capacity, variables_to_time[i])
        problem.addConstraint(taller_capacity, jumbo_to_time[i])

    #print(variables)
    #print(domain)
    solutions = problem.getSolutions()
    #print(solutions)
    print(len(solutions))

if __name__ == "__main__":
    main()