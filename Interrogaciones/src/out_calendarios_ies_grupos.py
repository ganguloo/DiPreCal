import os
from datos.generacion_calendario import generacion_calendario
from datos.interrogaciones import (organizacion_datos_interrogaciones, interrogaciones_mes, interrogaciones_mes_i1s,
                                   interrogaciones_mes_grupos, interrogaciones_mes_i2s)
from parametros.grupos_modelo import GRUPOS_M

from modelo_optimizacion.cargar_datos.cargar_vacantes import cargar_vacantes

from resultados.test_calendar import make_calendar
from resultados.cupos_fmat_ing import grafico_vacantes_fmat_ing
from resultados.grafico_dias import graficar_dias, graficar_dias_plotly

from bokeh.document import Document
from bokeh.embed import file_html
from bokeh.layouts import gridplot

from bokeh.resources import INLINE
from bokeh.util.browser import view


from parametros.parametros import NUM_EXPERIMENTO

if __name__ == "__main__":
    fechas_validas, mapeo_fechas, fechas = generacion_calendario()
    fechas_actualizado = organizacion_datos_interrogaciones(mapeo_fechas,
                                                            "resultados_rest_vacantes.txt")
    vacantes = cargar_vacantes()
    for i in range(3) :
        if i == 0 :
            abril = interrogaciones_mes_i1s("Apr", fechas_actualizado, fechas)
            mayo = interrogaciones_mes_i1s("May", fechas_actualizado, fechas)
            junio = interrogaciones_mes_i1s("Jun", fechas_actualizado, fechas)

        elif i == 1 :
            abril = interrogaciones_mes_i2s("Apr", fechas_actualizado, fechas)
            mayo = interrogaciones_mes_i2s("May", fechas_actualizado, fechas)
            junio = interrogaciones_mes_i2s("Jun", fechas_actualizado, fechas)
        
        else :
            abril = interrogaciones_mes_grupos("Apr", fechas_actualizado, fechas)
            mayo = interrogaciones_mes_grupos("May", fechas_actualizado, fechas)
            junio = interrogaciones_mes_grupos("Jun", fechas_actualizado, fechas)

        dict_fechas = {4: abril, 5: mayo, 6: junio}
        months = [[make_calendar(dict_fechas[i], 2023, i) for i in range(4, 7)]]

        grid = gridplot(toolbar_location="above", children=months)

        doc = Document()
        doc.add_root(grid)
        doc.validate()
        if i == 0:
            filename = "calendars_i1s.html"

        elif i == 1:
            filename = "calendars_i2s.html"

        else :
            filename = "calendars_grupos.html"
            
        carpeta = f"experimento_{NUM_EXPERIMENTO}"
        filename = os.path.join("output_resultados", carpeta, filename)

        with open(filename, "w") as f:
            f.write(file_html(doc, INLINE, "Interrogaciones 2023-1"))
        # print(f"Wrote {filename}")
        
        view(filename)

