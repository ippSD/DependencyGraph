"""Includes dependency-graph functions."""
from os import sep

from pydotplus import Dot, Edge, Node, Subgraph

from .classes import DependencyGraph as Dg


# from typing import List


def build(graph: Dg) -> Subgraph:
    """Generate the dependency digraph.

    Builds the dependency digraph recursively from the main node.

    :param graph: main node.
    :type graph: Dg
    :return: Dot type digraph.
    :rtype: Dot
    """
    digraph = Subgraph()
    main_node_name = str(graph.root_filename).split(sep)[-1]
    main_node = Node(main_node_name)
    digraph.add_node(main_node)
    for dep in graph.module_deps:
        node_name = str(dep.root_filename).split(sep)[-1]
        node = Node(node_name)
        edge = Edge(main_node_name, node_name)
        digraph.add_node(node)
        digraph.add_edge(edge)
        digraph.add_subgraph(build(dep))
        pass
    return digraph


def export(digraph: Subgraph, name: str = "a") -> None:
    """Generate the dependency digraph plot.

    Exports the generated digraph from 'build' to 'name'.png file.

    :param digraph: Dot digraph from 'build'.
    :type digraph: Dot
    :param name: export file's basename.
    :type name: str
    """
    graph = Dot()
    graph.add_subgraph(digraph)
    graph.write(name + ".dot")
    result = graph.create(format="png")
    if result is None:
        print("Error!")
        pass
    else:
        with open(name + ".png", "wb") as file:
            file.write(result)
            pass
        pass
    pass
