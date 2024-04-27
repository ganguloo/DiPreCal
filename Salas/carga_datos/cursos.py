def curso(criterio, dia):
    archivo = open("Salas/datos/output.csv")
    info = archivo.readlines()[1:]
    archivo.close()
    info2 = []
    info = [x.strip("\n").split(";") for x in info]
    for linea in info:
        if linea[3] == dia:
            info2.append(linea)
    if criterio == "vacantes":
        pedido = list(map(lambda x: int(x[-1]), info2))
    elif criterio == "nombres":
        pedido = list(map(lambda x: x[0], info2))
    elif criterio == "num":
        pedido = list(map(lambda x: x[2], info2))
    elif criterio == "particion":
        pedido = list(map(lambda x: 2*int(len(x[1].split(','))), info2))

    return pedido
