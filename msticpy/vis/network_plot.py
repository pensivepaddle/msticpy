# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
"""Module for common display functions."""
from typing import List, Optional, Union

import networkx as nx
from bokeh.io import output_notebook
from bokeh.models import (
    BoxSelectTool,
    Circle,
    EdgesAndLinkedNodes,
    HoverTool,
    Label,
    MultiLine,
    NodesAndLinkedEdges,
    Renderer,
    TapTool,
)
from bokeh.palettes import Spectral4
from bokeh.plotting import figure, from_networkx, show

from .._version import VERSION

__version__ = VERSION
__author__ = "Ian Hellen"


# pylint: disable=too-many-arguments, too-many-locals
def plot_nx_graph(
    nx_graph: nx.Graph,
    title: str = "Data Graph",
    node_size: int = 25,
    font_size: Union[int, str] = 10,
    height: int = 800,
    width: int = 800,
    scale: int = 2,
    hide: bool = False,
    source_attrs: Optional[List[str]] = None,
    target_attrs: Optional[List[str]] = None,
    edge_attrs: Optional[List[str]] = None,
    **kwargs,
) -> figure:
    """
    Plot entity graph with Bokeh.

    Parameters
    ----------
    nx_graph : nx.Graph
        The entity graph as a networkX graph
    title : str
        Title for the plot, by default 'Data Graph'
    node_size : int, optional
        Size of the nodes in pixels, by default 25
    font_size : int, optional
        Font size for node labels, by default 10
        Can be an integer (point size) or a string (e.g. "10pt")
    width : int, optional
        Width in pixels, by default 800
    height : int, optional
        Image height (the default is 800)
    scale : int, optional
        Position scale (the default is 2)
    hide : bool, optional
        Don't show the plot, by default False. If True, just
        return the figure.
    source_attrs : Optional[List[str]], optional
        Optional list of source attributes to use as hover properties, by default None
    target_attrs : Optional[List[str]], optional
        Optional list of target attributes to use as hover properties, by default None
    edge_attrs : Optional[List[str]], optional
        Optional list of edge attributes to use as hover properties, by default None

    Other Parameters
    ----------------
    source_color : str, optional
        The color of the source nodes, by default 'light-blue'
    target_color : str, optional
        The color of the source nodes, by default 'light-green'
    edge_color : str, optional
        The color of the edges, by default 'black'

    Returns
    -------
    bokeh.plotting.figure
        The network plot.

    """
    output_notebook()
    font_pnt = f"{font_size}pt" if isinstance(font_size, int) else font_size
    node_attrs = {
        node: attrs.get(
            "color",
            kwargs.pop("source_color", "lightblue")
            if attrs.get("node_role", "source") == "source"
            else kwargs.pop("target_color", "lightgreen"),
        )
        for node, attrs in nx_graph.nodes(data=True)
    }
    nx.set_node_attributes(nx_graph, node_attrs, "node_color")

    plot = figure(
        title=title,
        x_range=(-3, 3),
        y_range=(-3, 3),
        width=width,
        height=height,
    )

    graph_renderer = from_networkx(
        nx_graph, nx.spring_layout, scale=scale, center=(0, 0)
    )
    _create_edge_renderer(graph_renderer, edge_color=kwargs.pop("edge_color", "black"))
    _create_node_renderer(graph_renderer, node_size, "node_color")

    graph_renderer.selection_policy = NodesAndLinkedEdges()
    graph_renderer.inspection_policy = EdgesAndLinkedNodes()
    plot.renderers.append(graph_renderer)

    hover_tools = [
        _create_node_hover(source_attrs, target_attrs, [graph_renderer.node_renderer])
    ]
    if edge_attrs:
        hover_tools.append(
            _create_edge_hover(edge_attrs, [graph_renderer.edge_renderer])
        )
    plot.add_tools(*hover_tools, TapTool(), BoxSelectTool())

    # Create labels
    for name, pos in graph_renderer.layout_provider.graph_layout.items():
        label = Label(
            x=pos[0],
            y=pos[1],
            x_offset=5,
            y_offset=5,
            text=name,
            text_font_size=font_pnt,
        )
        plot.add_layout(label)
    if not hide:
        show(plot)
    return plot


def _create_node_hover(
    source_attrs: Optional[List[str]],
    target_attrs: Optional[List[str]],
    renderers: List[Renderer],
) -> HoverTool:
    """Create a hover tool for nodes."""
    node_attr_cols = (source_attrs or []) + (target_attrs or [])
    node_tooltips = [
        ("node_type", "@node_type"),
        *[(col, f"@{{{col}}}") for col in node_attr_cols],
    ]
    return HoverTool(tooltips=node_tooltips, renderers=renderers)


def _create_edge_hover(edge_attrs: List[str], renderers: List[Renderer]) -> HoverTool:
    """Create a hover tool for nodes."""
    edge_attr_cols = edge_attrs or []
    edge_tooltips = [
        *[(col, f"@{{{col}}}") for col in edge_attr_cols],
    ]
    return HoverTool(tooltips=edge_tooltips, renderers=renderers)


def _create_node_renderer(graph_renderer: Renderer, node_size: int, fill_color: str):
    """Create graph render for nodes."""
    graph_renderer.node_renderer.glyph = Circle(size=node_size, fill_color=fill_color)
    graph_renderer.node_renderer.hover_glyph = Circle(
        size=node_size, fill_color=Spectral4[1]
    )
    graph_renderer.node_renderer.selection_glyph = Circle(
        size=node_size, fill_color=Spectral4[2]
    )


def _create_edge_renderer(graph_renderer: Renderer, edge_color: str):
    """Create graph render for edges."""
    graph_renderer.edge_renderer.hover_glyph = MultiLine(
        line_color=Spectral4[1], line_width=5
    )
    graph_renderer.edge_renderer.glyph = MultiLine(
        line_alpha=0.8, line_color=edge_color, line_width=1
    )
    graph_renderer.edge_renderer.selection_glyph = MultiLine(
        line_color=Spectral4[2], line_width=5
    )


def plot_entity_graph(
    entity_graph: nx.Graph,
    node_size: int = 25,
    font_size: Union[int, str] = 10,
    height: int = 800,
    width: int = 800,
    scale: int = 2,
    hide: bool = False,
) -> figure:
    """
    Plot entity graph with Bokeh.

    Parameters
    ----------
    entity_graph : nx.Graph
        The entity graph as a networkX graph
    node_size : int, optional
        Size of the nodes in pixels, by default 25
    font_size : int, optional
        Font size for node labels, by default 10
        Can be an integer (point size) or a string (e.g. "10pt")
    width : int, optional
        Width in pixels, by default 800
    height : int, optional
        Image height (the default is 800)
    scale : int, optional
        Position scale (the default is 2)
    hide : bool, optional
        Don't show the plot, by default False. If True, just
        return the figure.

    Returns
    -------
    bokeh.plotting.figure
        The network plot.

    """
    output_notebook()
    font_pnt = f"{font_size}pt" if isinstance(font_size, int) else font_size
    node_attrs = {
        node: attrs.get("color", "green")
        for node, attrs in entity_graph.nodes(data=True)
    }
    nx.set_node_attributes(entity_graph, node_attrs, "node_color")

    plot = figure(
        title="Alert Entity graph",
        x_range=(-3, 3),
        y_range=(-3, 3),
        width=width,
        height=height,
    )

    plot.add_tools(
        HoverTool(
            tooltips=[
                ("node_type", "@node_type"),
                ("name", "@name"),
                ("description", "@description"),
                ("entitytype", "@entitytype"),
            ]
        )
    )

    graph_renderer = from_networkx(
        entity_graph, nx.spring_layout, scale=scale, center=(0, 0)
    )
    graph_renderer.node_renderer.glyph = Circle(
        size=node_size, fill_color="node_color", fill_alpha=0.5
    )
    # pylint: disable=no-member
    plot.renderers.append(graph_renderer)

    # Create labels
    for name, pos in graph_renderer.layout_provider.graph_layout.items():
        label = Label(
            x=pos[0],
            y=pos[1],
            x_offset=5,
            y_offset=5,
            text=name,
            text_font_size=font_pnt,
        )
        plot.add_layout(label)
    # pylint: enable=no-member
    if not hide:
        show(plot)
    return plot