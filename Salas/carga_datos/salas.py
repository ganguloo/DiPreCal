def capacidad_salas(peticion):
    archivo = open("Salas/datos/salas.csv")
    info = archivo.readlines()[1:]
    archivo.close()
    if peticion == "capacidad":
        return list(map(lambda x: int(x.split("\n")[0].split(",")[2]), info))
    else:
        return list(map(lambda x: x.split("\n")[0].split(",")[1], info))
