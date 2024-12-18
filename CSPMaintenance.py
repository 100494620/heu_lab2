from constraint import *
import os
import sys

class Plane:
    def __init__(self, id, tipo, restr, t1, t2):
        self.id = id
        self.tipo = tipo
        self.restr = restr
        self.t1 = t1
        self.t2 = t2

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

#def restrictions(franjas, matrix_size, std_positions, spc_positions, prk_positions, planes):

def jmb_adjacent(*args):
    positions = []
    plane_types = []

    """for plane in planes:
        plane_types.append(plane.tipo)

    for i in range(len(planes) - 1):
        for j in range(i + 1, len(positions)):
            if plane_types[i] == plane_types[j] == "JMB":
                if abs(positions[i][0] - positions[j][0]) + abs(positions[i][1] - positions[j][1]) == 1:
                    return False

    return True"""

def main():
    problem = Problem()
    franjas, matrix_size, std_positions, spc_positions, prk_positions, planes = parse_data(read_data())

    variables = []

    positions = std_positions + spc_positions + prk_positions

    for plane in planes:
        for franja in range(0, franjas):
            variables.append((plane, franja))
    # assures that all planes will be assigned to the unique taller/parking in each time slot
    for var in variables:
        problem.addVariable(var, positions)

    # variable - (plane, time-slot)
    # map <int time slot, planes>
    for i in range(0, franjas):
        problem.addConstraint(jmb_adjacent, (planes, i))

    #print(variables)
    #print(domain)
    solutions = problem.getSolutions()
    print(solutions)
    #print(len(solutions))

if __name__ == "__main__":
    main()

# A continuacion se anyaden las restricciones del problema mediante la funcion addConstraint proporcionada por la libreria
#
# Ejemplos:
# problem.addConstraint(lambda a, b: a > b, ('a', 'b'))		Crea una funcion lambda que recibe dos parametros que se corresponden
# con los valores de las variables 'a' y 'b', y comprueba que 'a' es mayor que 'b'. Tambien se podria haber creado una funcion para
# comprobar este hecho:
#
# def greater(a, b):
#    if a > b:
#	return True
#
# problem.addConstraint(greater, ('a', 'b'))
#
# En este caso vamos a modelar en primer lugar la restriccion de que Alfredo y Ruben no quieren trabajar juntos, es decir,
# RA,R = [(1,2),(1,3),(2,1),(2,3),(3,1),(3,2)]. Se puede hacer de varias formas. Una de ellas es definir una funcion, por ejemplo,
# notEqual, que compruebe que el valor de una variable es diferente de la de la otra:

"""def notEqual(a, b):
	if a != b:
		return True

problem.addConstraint(notEqual, ('A', 'R'))

# Tambien se puede crear una funcion lambda para hacer esta comprobacion:

problem.addConstraint(lambda a, b: a != b, ('A', 'R'))


# Por ultimo, la libreria ofrece la funcion AllDifferentConstraint que precisamente comprueba que el valor de una variable es diferente a las de las otras:

problem.addConstraint(AllDifferentConstraint(), ['A', 'R'])

# Lo anterior, son tres formas diferentes de modelar la misma restriccion RA,R = [(1,2),(1,3),(2,1),(2,3),(3,1),(3,2)]
# Ahora modelamos la restriccion de que Ruben y Felisa quieren trabajar en la misma parte RR,F={(1,1),(2,2),(3,3)}

problem.addConstraint(lambda a, b: a == b, ('R', 'F'))


# Por ultimo, modelamos la restriccion de que Yara hace una parte posterior a la que haga Ruben, RR,Y={(1,2),(1,3),(2,3)}

def consecutive(a, b):
	if b > a:
		return True

problem.addConstraint(consecutive, ('R', 'Y'))

# Una vez modelado el problema, podemos recuperar una de las soluciones:

print(problem.getSolution())

# o todas las soluciones:

print(problem.getSolutions())
print(len(problem.getSolutions()))"""