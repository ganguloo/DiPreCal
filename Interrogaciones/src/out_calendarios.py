import os
from datos.generacion_calendario import generacion_calendario
from datos.interrogaciones import organizacion_datos_interrogaciones, interrogaciones_mes

from modelo_optimizacion.cargar_datos.cargar_vacantes import cargar_vacantes

from resultados.test_calendar import make_calendar
from resultados.cupos_fmat_ing import grafico_vacantes_fmat_ing
from resultados.grafico_dias import graficar_dias, graficar_dias_plotly

from bokeh.document import Document
from bokeh.embed import file_html
from bokeh.layouts import gridplot

from bokeh.resources import INLINE
from bokeh.util.browser import view

import sys
from parametros.parametros import NUM_EXPERIMENTO

if __name__ == "__main__":
    fechas_validas, mapeo_fechas, fechas = generacion_calendario()
    fechas_actualizado = organizacion_datos_interrogaciones(mapeo_fechas,
                                                            "resultados_rest_vacantes.txt")

    # print(fechas_actualizado)
    # sys.exit()
    vacantes = cargar_vacantes()
    abril = interrogaciones_mes("Sep", fechas_actualizado, fechas)
    mayo = interrogaciones_mes("Oct", fechas_actualizado, fechas)
    junio = interrogaciones_mes("Nov", fechas_actualizado, fechas)

    dict_fechas = {9: abril, 10: mayo, 11: junio}
    months = [[make_calendar(dict_fechas[i], 2024, i) for i in range(9, 12)]]

    # print(months)
    # sys.exit()

    grid = gridplot(toolbar_location="above", children=months)

    doc = Document()
    doc.add_root(grid)
    doc.validate()
    filename = "calendars.html"
    carpeta = f"experimento_{NUM_EXPERIMENTO}"
    filename = os.path.join("output_resultados", carpeta, filename)

    with open(filename, "w") as f:
        f.write(file_html(doc, INLINE, "Interrogaciones 2023-1"))
    # print(f"Wrote {filename}")
    view(filename)

    graficar_dias_plotly(mapeo_fechas,
                         fechas_actualizado,
                         path=os.path.join("output_resultados", carpeta, "Comb_fechas.html"))
    grafico_vacantes_fmat_ing(fechas_validas, fechas_actualizado, mapeo_fechas, vacantes,
                              path=os.path.join("output_resultados", carpeta, "Vacantes_FMAT_ING.html"))
#
