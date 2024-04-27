import datetime

from datos.generacion_calendario import generacion_calendario
from datos.interrogaciones import interrogaciones_mes, organizacion_datos_interrogaciones
from calendar import Calendar, day_abbr as day_abbrs, month_name as month_names

from bokeh.document import Document
from bokeh.embed import file_html
from bokeh.layouts import gridplot
from bokeh.models import (CategoricalAxis, CategoricalScale, ColumnDataSource,
                          FactorRange, HoverTool, Plot, Rect, Text)
from bokeh.resources import INLINE
from bokeh.util.browser import view


def make_calendar(pruebas: list[(datetime.date, str)],
                  year: int,
                  month: int,
                  firstweekday: str = "Mon") -> Plot:
    firstweekday = list(day_abbrs).index(firstweekday)
    calendar = Calendar(firstweekday=firstweekday)

    month_days = [None if not day else str(
        day) for day in calendar.itermonthdays(year, month)]
    month_weeks = len(month_days) // 7

    workday = "linen"
    weekend = "lightsteelblue"

    def weekday(date):
        return (date.weekday() - firstweekday) % 7

    def pick_weekdays(days):
        return [days[i % 7] for i in range(firstweekday, firstweekday+7)]

    day_names = pick_weekdays(day_abbrs)
    week_days = pick_weekdays([workday]*5 + [weekend]*2)

    source = ColumnDataSource(data=dict(
        days=list(day_names)*month_weeks,
        weeks=sum([[str(week)]*7 for week in range(month_weeks)], []),
        month_days=month_days,
        day_backgrounds=sum([week_days]*month_weeks, []),
    ))
    pruebas_source = ColumnDataSource(data=dict(
        holidays_days=[day_names[weekday(date)] for date, _ in pruebas],
        holidays_weeks=[str((weekday(date.replace(day=1)) + date.day) // 7)
                        for date, _ in pruebas],
        month_holidays=[summary for _, summary in pruebas],
    ))

    xdr = FactorRange(factors=list(day_names))
    ydr = FactorRange(factors=list(
        reversed([str(week) for week in range(month_weeks)])))
    x_scale, y_scale = CategoricalScale(), CategoricalScale()

    plot = Plot(x_range=xdr, y_range=ydr, x_scale=x_scale, y_scale=y_scale,
                width=600, height=600, outline_line_color=None)
    plot.title.text = month_names[month]
    plot.title.text_font_size = "16px"
    plot.title.text_color = "darkolivegreen"
    plot.title.offset = 25
    plot.min_border_left = 0
    plot.min_border_bottom = 5
    plot.min_border_top = 300

    rect = Rect(x="days", y="weeks", width=0.9, height=0.9,
                fill_color="day_backgrounds", line_color="silver")
    plot.add_glyph(source, rect)

    rect = Rect(x="holidays_days", y="holidays_weeks", width=0.67,
                height=0.8, fill_color="pink", line_color="indianred")
    rect_renderer = plot.add_glyph(pruebas_source, rect)

    text = Text(x="days", y="weeks", text="month_days",
                text_align="center", text_baseline="middle")
    plot.add_glyph(source, text)

    xaxis = CategoricalAxis()
    xaxis.major_label_text_font_size = "11px"
    xaxis.major_label_standoff = 0
    xaxis.major_tick_line_color = None
    xaxis.axis_line_color = None
    plot.add_layout(xaxis, 'above')

    hover_tool = HoverTool(renderers=[rect_renderer], tooltips=[
                           ("Prueba", "@month_holidays")])
    plot.tools.append(hover_tool)

    return plot


if __name__ == "__main__":
    fechas_validas, mapeo_fechas, fechas = generacion_calendario()
    fechas_actualizado = organizacion_datos_interrogaciones(mapeo_fechas, "resultados_rest_vacantes.txt")

    abril = interrogaciones_mes("Apr", fechas_actualizado, fechas)
    mayo = interrogaciones_mes("May", fechas_actualizado, fechas)
    junio = interrogaciones_mes("Jun", fechas_actualizado, fechas)
    dict_fechas = {4: abril, 5: mayo, 6: junio}
    # months = [[make_calendar(dict_fechas.get(i, []), 2023, i) for i in range(1, 12)]]
    months = [[make_calendar(2023, 3*i + j + 1)
               for j in range(3)] for i in range(4)]
    grid = gridplot(toolbar_location=None, children=months)

    doc = Document()
    doc.add_root(grid)
    doc.validate()
    filename = "calendars.html"
    with open(filename, "w") as f:
        f.write(file_html(doc, INLINE, "Interrogaciones 2023-1"))
    print(f"Wrote {filename}")
    view(filename)
