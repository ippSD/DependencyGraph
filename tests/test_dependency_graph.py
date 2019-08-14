from dependency_graph import __version__
import dependency_graph as dg


def test_version():
    assert __version__ == '0.1.0'


def test_main_file():
    try:
        graph = dg.generate("./dependency_graph")
        assert True
        pass
    except Exception:
        assert False
    pass