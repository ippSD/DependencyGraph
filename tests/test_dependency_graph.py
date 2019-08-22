from os import pardir
from pathlib import Path

import dependency_graph as dg
from dependency_graph import __version__


def test_version():
    assert __version__ == "0.1.0"


def test_main_file():
    try:
        graph = dg.DependencyGraph("./tests/test_simple.py")
        print(graph)
        assert True
        pass
    except Exception:
        assert False
    pass


def test_root_directory():
    try:
        root_path = Path().absolute()
        subfile = "tests/test_simple.py"
        subdir = "tests"
        graph = dg.DependencyGraph(subfile, search_paths=".")
        assert graph.root == root_path.joinpath(subdir)
        pass
    except Exception:
        assert False
    pass


def test_module_findings():
    try:
        graph = dg.DependencyGraph("./tests/test_simple.py", search_paths=".")
        assert "dependency_graph" in graph.module_names
        pass
    except Exception:
        assert False
    pass


def test_module_path_findings():
    try:
        graph = dg.DependencyGraph("./tests/test_simple.py", search_paths=".")
        path = pardir.join(str(Path().absolute()).split(pardir)[0:-2])
        path += "dependency_graph"
        path_abs = Path(path).absolute()
        found_paths = [Path(p).absolute() for p in graph.module_paths]
        print("Found Paths:\n{}".format(found_paths))
        print("Expected path:\t{}".format(path_abs))
        assert any([path_abs == p for p in found_paths])
        pass
    except Exception:
        assert False
    pass


def test_missing_file():
    try:
        src_file = "./dependency_graph/clases.py"
        dg.DependencyGraph(src_file, search_paths=".")
        assert False
    except FileNotFoundError:
        assert True
        pass
    pass


def test_module_deps():
    src_file = "./dependency_graph/classes.py"
    graph = dg.DependencyGraph(src_file, search_paths=".")
    assert len(graph.module_names) > 0
    assert "re" in graph.module_names
    assert len(graph.module_deps) > 0
    pass


def test_module_deps_iter():
    src_file = "./tests/test_simple.py"
    graph = dg.DependencyGraph(src_file, search_paths=".")
    digraph = dg.build(graph)
    dg.export(digraph, name="test")
    assert True
