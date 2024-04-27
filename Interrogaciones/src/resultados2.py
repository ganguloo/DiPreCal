from modelo_optimizacion.cargar_datos.cargar_vacantes import cargar_vacantes
from datos.generacion_calendario import generacion_calendario
from datos.interrogaciones import organizacion_datos_interrogaciones



from bokeh.io import show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure
from bokeh.palettes import Viridis256, Turbo256, d3

fechas_validas, mapeo_fechas, fechas = generacion_calendario()
vacantes = cargar_vacantes()

fechas_actualizado = organizacion_datos_interrogaciones(mapeo_fechas, "resultados_rest_vacantes.txt")


def interrogaciones_mes(mes, fechas_interrogaciones, fechas):
    interrogaciones_del_mes = []
    for curso in fechas_interrogaciones:
        if mes in curso[1]:
            date = fechas[curso[1]].date()
            texto = f"I{curso[2]} : {curso[0]}"
            interrogaciones_del_mes.append((date, texto))

    return interrogaciones_del_mes


abril = interrogaciones_mes("Apr", fechas_actualizado, fechas)
mayo = interrogaciones_mes("May", fechas_actualizado, fechas)
junio = interrogaciones_mes("Jun", fechas_actualizado, fechas)

dict_fechas = {4: abril, 5: mayo, 6: junio}

# print("VACANTES", vacantes["IMI3100-1"])


vacantes_fechas = {n: 0 for n in mapeo_fechas.values()}
cursos_fechas = {n: 0 for n in mapeo_fechas.values()}

cursos_fechas_nombres = {n: 0 for n in mapeo_fechas.values()}

for fecha in fechas_validas:
    mapeo = mapeo_fechas[fecha]
    cantidad_cursos = 0
    cantidad_vacantes = 0
    lista_cursos = []
    for curso in fechas_actualizado:
        if curso[1] == mapeo:
            cantidad_cursos += 1
            cantidad_vacantes += vacantes.get(curso[0], 0)
            lista_cursos.append(curso[0])

    vacantes_fechas[mapeo] = cantidad_vacantes
    cursos_fechas[mapeo] = cantidad_cursos
    cursos_fechas_nombres[mapeo] = lista_cursos

x_values = list(cursos_fechas.keys())
y_values = list(cursos_fechas.values())

for key, value in cursos_fechas_nombres.items():
    if value == 0:
        cursos_fechas_nombres[key] = []

# Ordenar este código

mapped_info_x = list(map(cursos_fechas_nombres.get, x_values))
source = ColumnDataSource(data=dict(x_values=x_values, y_values=y_values, color=Turbo256,
                          info_x=mapped_info_x, vacantes=list(vacantes_fechas.values())))
p = figure(x_range=x_values, plot_width=1700, plot_height=900,
           x_axis_label="Fechas", y_axis_label="Cantidad de cursos")
p.xaxis.major_label_orientation = 1
p.vbar(x="x_values", top="y_values", width=0.9, source=source, color="color")
hover = HoverTool(tooltips=[('Fecha', '@x_values'),
                  ('Cursos asignados', '@info_x'), ('Cantidad de cursos', '@y_values'),
                  ("Vacantes necesarias", "@vacantes")])
p.add_tools(hover)

p.xaxis.axis_label_text_font_size = '8pt'
p.yaxis.axis_label_text_font_size = '14pt'
p.xaxis.major_label_text_font_size = '10pt'
p.yaxis.major_label_text_font_size = '12pt'

show(p)

