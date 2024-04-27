import os
import networkx as nx

from bokeh.io import show, save, output_file
from bokeh.models import Circle, ColumnDataSource, MultiLine, NodesAndLinkedEdges, LabelSet
from bokeh.plotting import figure
from bokeh.plotting import from_networkx
from bokeh.palettes import Blues8
from bokeh.transform import linear_cmap


def dibujar_grafo(title, grafo):
    """
    # TODO
    Documentación

    """

    node_highlight_color = 'white'
    edge_highlight_color = 'black'

    # Choose attributes from G network to size and color by —
    # setting manual size (e.g. 10) or color (e.g. 'skyblue') also allowed
    size_by_this_attribute = 'adjusted_node_size'
    color_by_this_attribute = 'adjusted_node_size'
    degrees = dict(nx.degree(grafo))
    nx.set_node_attributes(grafo, name='degree', values=degrees)
    # Pick a color palette — Blues8, Reds8, Purples8, Oranges8, Viridis8
    color_palette = Blues8
    number_to_adjust_by = 5
    adjusted_node_size = dict([(node, degree+number_to_adjust_by)
                              for node, degree in nx.degree(grafo)])
    nx.set_node_attributes(grafo, name='adjusted_node_size', values=adjusted_node_size)

    vecinos = dict()

    for node in grafo.nodes:
        neighbors = [n for n in grafo.neighbors(node)]
        vecinos[node] = ",".join(neighbors)
    # Choose a title!
    nx.set_node_attributes(grafo, name="vecinos", values=vecinos)
    # Establish which categories will appear when hovering over each node
    HOVER_TOOLTIPS = [
        ("Nombre", "@index"),
        ("Degree", "@degree"),
        ("Vecinos", "@vecinos")
    ]

    # Create a plot — set dimensions, toolbar, and title
    plot = figure(tooltips=HOVER_TOOLTIPS,
                  tools="pan,wheel_zoom,save,reset", active_scroll='wheel_zoom',
                  title=title, align="center")

    plot.width = 1900
    plot.height = 900
    network_graph = from_networkx(grafo, nx.nx_agraph.graphviz_layout(grafo), scale=10, center=(0, 0))

    # network_graph = from_networkx(grafo, nx.kamada_kawai_layout(grafo), scale=10, center=(0, 0))

    # Set node sizes and colors according to node degree (color as category from attribute)
    
    minimum_value_color = min(network_graph.node_renderer.data_source.data[color_by_this_attribute])
    maximum_value_color = max(network_graph.node_renderer.data_source.data[color_by_this_attribute])

    network_graph.node_renderer.glyph = Circle(size=size_by_this_attribute, fill_color=linear_cmap(
        color_by_this_attribute, color_palette, minimum_value_color, maximum_value_color))
    # Set node highlight colors
    network_graph.node_renderer.hover_glyph = Circle(
        size=size_by_this_attribute, fill_color=node_highlight_color, line_width=2)
    network_graph.node_renderer.selection_glyph = Circle(
        size=size_by_this_attribute, fill_color=node_highlight_color, line_width=2)
    # Set edge opacity and width
    network_graph.edge_renderer.glyph = MultiLine(line_alpha=0.5, line_width=1)
    # Set edge highlight colors
    network_graph.edge_renderer.selection_glyph = MultiLine(
        line_color=edge_highlight_color, line_width=2)
    network_graph.edge_renderer.hover_glyph = MultiLine(
        line_color=edge_highlight_color, line_width=2)

    # Highlight nodes and edges
    network_graph.selection_policy = NodesAndLinkedEdges()
    network_graph.inspection_policy = NodesAndLinkedEdges()

    plot.renderers.append(network_graph)

    x, y = zip(*network_graph.layout_provider.graph_layout.values())
    node_labels = list(grafo.nodes())
    source = ColumnDataSource(
        {'x': x, 'y': y, 'name': [node_labels[i] for i in range(len(x))]})
    labels = LabelSet(x='x', y='y', text='name', source=source,
                      background_fill_color='white',
                      text_font_size='10px', background_fill_alpha=.7)
    plot.renderers.append(labels)

    file = f"{title}.html"
    show(plot)
    output_file(filename=os.path.join("images", file))
    save(plot, filename=os.path.join("images", file))
