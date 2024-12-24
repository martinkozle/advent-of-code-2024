import re
from typing import Literal

import networkx as nx  # type: ignore[import-untyped]

from src.prep import run_with_prep
from src.timing import timing

type Operation = Literal["OR", "AND", "XOR"]
type Wire = str
type Gate = tuple[Wire, Operation, Wire]


# modified from: https://stackoverflow.com/a/59598265
def draw_graph3(
    networkx_graph: nx.DiGraph,
    notebook: bool = True,
    output_filename: str = "graph.html",
    show_buttons: bool = False,
    only_physics_buttons: bool = False,
) -> None:
    """
    This function accepts a networkx graph object,
    converts it to a pyvis network object preserving its node and edge attributes,
    and both returns and saves a dynamic network visualization.

    Valid node attributes include:
        "size", "value", "title", "x", "y", "label", "color".

        (For more info: https://pyvis.readthedocs.io/en/latest/documentation.html#pyvis.network.Network.add_node)

    Valid edge attributes include:
        "arrowStrikethrough", "hidden", "physics", "title", "value", "width"

        (For more info: https://pyvis.readthedocs.io/en/latest/documentation.html#pyvis.network.Network.add_edge)


    Args:
        networkx_graph: The graph to convert and display
        notebook: Display in Jupyter?
        output_filename: Where to save the converted network
        show_buttons: Show buttons in saved version of network?
        only_physics_buttons: Show only buttons controlling physics of network?
    """

    # import
    from pyvis import network as net  # type: ignore[import-untyped]

    # make a pyvis network
    pyvis_graph = net.Network(notebook=notebook, directed=True)
    pyvis_graph.width = "1000px"
    # for each node and its attributes in the networkx graph
    for node, node_attrs in networkx_graph.nodes(data=True):
        pyvis_graph.add_node(node, **node_attrs)

    # for each edge and its attributes in the networkx graph
    for source, target, edge_attrs in networkx_graph.edges(data=True):
        # if value/width not specified directly, and weight is specified
        # set 'value' to 'weight'
        if (
            "value" not in edge_attrs
            and "width" not in edge_attrs
            and "weight" in edge_attrs
        ):
            # place at key 'value' the weight of the edge
            edge_attrs["value"] = edge_attrs["weight"]
        # add the edge
        pyvis_graph.add_edge(source, target, **edge_attrs)

    # turn buttons on
    if show_buttons:
        if only_physics_buttons:
            pyvis_graph.show_buttons(filter_=["physics"])
        else:
            pyvis_graph.show_buttons()

    # save
    pyvis_graph.show(output_filename, notebook=notebook)


@timing
def main(inp: str) -> None:
    start_values_str, gates_str = inp.split("\n\n")
    start_values = {
        row[0:3]: row[5] == "1" for row in start_values_str.strip().split("\n")
    }
    gates: dict[Wire, Gate] = {
        w3: (w1, op, w2)
        for w1, op, w2, w3 in re.findall(
            r"(.+) (\w+) (.+) -> (.+)",
            gates_str,
        )
    }
    graph = nx.DiGraph()
    for wire in start_values:
        if wire[0] == "x":
            graph.add_node(wire, color="#0055ff")
        if wire[0] == "y":
            graph.add_node(wire, color="#882255")
    for out_wire in gates:
        if out_wire[0] == "z":
            graph.add_node(out_wire, color="#00ff00")
    for out_wire, (wire1, op, wire2) in gates.items():
        graph.add_edges_from(((wire1, out_wire), (wire2, out_wire)), label=op)
    draw_graph3(graph, notebook=False, output_filename="day_24_part2_graph.html")
    # check manually...

    print("fvw,grf,mdb,nwq,wpq,z18,z22,z36")


if __name__ == "__main__":
    run_with_prep(main)
