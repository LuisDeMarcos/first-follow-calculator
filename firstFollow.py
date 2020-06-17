import string

noTerminal_dict = {}
directores_set = set()
directores_cache = {}
loop_savior = {}

def inicial(producciones, produccion, noTerminal): # Calcula el inicial de una produccion
    if(isinstance(produccion, str)): # Si la produccion no es una lista

        if(noTerminal+produccion in loop_savior): # Comprobar si estamos en bucle
            if(loop_savior.get(noTerminal+produccion) > 1):
                return
            else:
                loop_savior.update({noTerminal+produccion : 2})
        else:
            loop_savior.update({noTerminal+produccion : 1})

        if produccion[0] in string.ascii_lowercase: # Comprobar si el inicial es un terminal
            if(noTerminal+produccion in directores_cache):
                directores_set.add(directores_cache.get(noTerminal+produccion))
                return
            directores_cache.update({noTerminal+produccion : produccion[0]})
            directores_set.add(produccion[0])
            return
        elif produccion[0] == "*": # Comprobar si el inicial es epsilon, redirigiendo al seguidor del No Terminal de la produccion
            seguidor(producciones, noTerminal)
        else: # Si el inicial es un No Terminal
            tieneProduccionVacia = "*" in producciones[noTerminal_dict.get(produccion[0])] # Comprueba si el No Terminal tiene la produccion vacia
            if(tieneProduccionVacia): # Si tiene produccion vacia, se añade al resultado el inicial del seguidor de dicho No Terminal en esa produccion o, en caso de no haber, se añade el seguidor del No Terminal de la produccion
                if(len(produccion[1:]) > 0):
                    inicial(producciones, produccion[1:], noTerminal)
                else:
                    seguidor(producciones, noTerminal)
                inicial(producciones, producciones[noTerminal_dict.get(produccion[0])][1:-1], produccion[0])
            else: # Si no tiene producciones vacias, se calcula el inicial de ese No Terminal
                inicial(producciones, producciones[noTerminal_dict.get(produccion[0])][1:], produccion[0])

    else:
        for i in produccion: # Se calcula el inicial de cada produccion en caso de ser una lista
            inicial(producciones, i, noTerminal)

def seguidor(producciones, noTerminal): # Calcula el seguidor de un No Terminal
    if(noTerminal ==  producciones[0][0]):
        directores_set.add("$")
    else:
        for produccion in producciones:
            for i in produccion[1:]:
                if(noTerminal in i):
                    if(i.index(noTerminal) == len(i)-1 and noTerminal != produccion[0]):
                        seguidor(producciones, produccion[0])
                    elif(i.index(noTerminal) != len(i)-1):
                        inicial(producciones, i[i.index(noTerminal)+1:], produccion[0])

def leerProducciones(): # Obtiene la gramática por parte del usuario
    prod = ""
    producciones = []
    while(prod != "0"):
        prod = input()
        producciones.append(prod)
    return producciones[:len(producciones)-1]

def procesarProducciones(producciones): # Procesará la gramática para que el programa la entienda
    try:
        for i in range(len(producciones)):
            noTerminal_dict.update({producciones[i][0] : i})
            producciones[i] = producciones[i].replace(":","|")
            producciones[i] = producciones[i].split("|")
        return producciones
    except:
        print("Invalid Input!")
        exit()

def calcularDirectores(producciones): # Realizará el cálculo de cada director
    for i in range(len(producciones)):
        for j in range(1,len(producciones[i])):
            directores_set.clear()
            loop_savior.clear()
            print(f"Director de {producciones[i][0]} -> {producciones[i][j]}", end=" = ")
            inicial(producciones, producciones[i][j], producciones[i][0])
            print(directores_set)

def main():
    print("Grammar format:\n  S:Aa|b|* (* as epsilon, must be in the last position)\n  A:c\n  0 (to end grammar)\nIntroduce your grammar: ")
    test = leerProducciones()
    print(test)
    producciones = procesarProducciones(test)
    calcularDirectores(producciones)

if __name__ == '__main__':
    main()
