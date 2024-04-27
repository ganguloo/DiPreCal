import plotly.graph_objects as go

from parametros.parametros import IDENTIFICADORES_FMAT


def grafico_vacantes_fmat_ing(fechas_validas, fechas_actualizado, mapeo_fechas, vacantes,
                              path, title="Vacantes_FMAT_ING"):
    vacantes_fechas_ing = {n: 0 for n in mapeo_fechas.values()}
    vacantes_fechas_mat = {n: 0 for n in mapeo_fechas.values()}
    cursos_fechas_nombres = {n: 0 for n in mapeo_fechas.values()}

    for fecha in fechas_validas:
        lista_cursos = list()
        mapeo = mapeo_fechas[fecha]
        cant_vacantes_ing = 0
        cant_vacantes_mat = 0
        for curso in fechas_actualizado:
            if curso[1] == mapeo:
                lista_cursos.append(curso[0])
                curso_fmat_bool = any(i in curso[0]
                                      for i in IDENTIFICADORES_FMAT)

                if curso_fmat_bool:
                    cant_vacantes_mat += vacantes.get(curso[0], 0)
                else:
                    cant_vacantes_ing += vacantes.get(curso[0], 0)
                    # print(curso)
            vacantes_fechas_mat[mapeo] = cant_vacantes_mat
            vacantes_fechas_ing[mapeo] = cant_vacantes_ing
        print(f"La cantidad de vacantes necesarias para {fecha} es {cant_vacantes_ing + cant_vacantes_mat}")

        cursos_fechas_nombres[mapeo] = lista_cursos

    x = list(mapeo_fechas.values())
    vacantes_ing = list(vacantes_fechas_ing.values())
    vacantes_fmat = list(vacantes_fechas_mat.values())

    fig = go.Figure(go.Bar(x=x, y=vacantes_ing, name="Vacantes Ingeniería"))
    fig.add_trace(go.Bar(x=x, y=vacantes_fmat, name="Vacantes FMAT"))

    fig.update_layout(barmode='stack')
    # path=os.path.join()
    fig.write_html(path)

