"""Includes dependency-graph classes."""
import re
from os import walk
from pathlib import Path
from typing import Iterable, Optional, Set, Union


path_types = Optional[Union[str, Iterable[str]]]


class DependencyGraph(object):
    """Build the dependency graph object.

    Constructor examines ``self.filename`` Python script's dependencies in
    order to build the dependency digraph.

    :param filename: path to Python script to analyze.
    :type filename: str
    :param search_paths: optional search paths.
    :type search_paths: path_types
    :raises: FileNotFoundError
    :ivar root: initial value: filename.
    :type root: str
    """

    """Dependency graph object.

    Class/Structure containing relevant information for building the
    dependency digraph of the Python project.

    'filename' is the path to the Python source file or Python package
    directory.

    'search_paths' includes the directory or list of directories where package
    dependencies will be searched in addition to 'filename' directory.
    """

    def __init__(self, filename: str, search_paths: path_types = None):
        if filename.startswith("external:"):
            self.root: str = filename.split(":", 1)[-1]
            self.root_filename: str = self.root
            self._is_package: bool = True
            self.search_paths: Set[str] = set()
            self.module_names: Set[str] = set()
            self.module_paths: Set[str] = set()
            self.module_deps: Set[DependencyGraph] = set()

            pass
        else:
            cwd = Path(filename)
            self.root_filename: Path = cwd.absolute()

            if cwd.is_file():
                root = "/".join(cwd.as_posix().split("/")[:-1])
                self.root: Path = Path(root).absolute()
                self._is_package: bool = False
                del root
            elif self.is_package(filename):
                self.root: Path = Path(filename).absolute()
                self._is_package: bool = True
                pass
            else:
                msg = "Error, file is nor package nor file: {}"
                print(msg.format(filename))
                raise FileNotFoundError()
                pass

            if search_paths is None:
                self.search_paths = (self.root,)
            elif type(search_paths) is str:
                self.search_paths = (self.root, search_paths)
            else:
                self.search_paths = (self.root, *search_paths)
                pass

            self.module_names = self.inspect_module_names()
            self.module_paths = self.get_module_paths()
            self.module_deps = self.get_module_deps()
            del cwd
            pass
        pass

    def inspect_module_names(self) -> Set[str]:
        """Get imported modules.

        Examines ``self.filename`` in search of imported packages and returns
        a set of found module names.

        :return: Set of imported module names.
        :rtype: Set[str]
        """
        modules = []
        pattern_1 = r"import\s+(?P<module>\w+)"
        pattern_2 = r"from\s+(?P<module>\w+)"
        if not self._is_package:
            with open(str(self.root_filename), "r") as file:
                for line in file.readlines():
                    m = re.match(pattern_1, line)
                    if m:
                        module = m.group("module")
                        modules.append(module)
                        pass
                    m = re.match(pattern_2, line)
                    if m:
                        module = m.group("module")
                        modules.append(module)
                        pass
                    pass
                pass
            pass
        else:
            # pattern = r"import\s+(?P<module>\w+)"
            for path, _, filenames in walk(str(self.root)):
                dir_path = self.root.joinpath(path)
                for filename in filenames:
                    abs_path = dir_path.joinpath(filename)

                    if not str(abs_path).endswith(".py"):
                        continue
                        pass
                    modules.append(filename)
                pass
            pass
        return set(modules)

    def get_module_paths(self) -> Set[str]:
        """Get imported modules' paths.

        Examines the found module names from 'inspect_module_names' and
        returns a set of paths where those modules are defined.

        :returns: set of file/package paths where imported modules are defined.
        :rtype: Set[str]
        """
        paths = []
        for module in self.module_names:
            module_found = False
            for search_path in self.search_paths:
                path = Path(search_path).absolute().joinpath(module)
                is_package = self.is_package(path)
                is_file = path.is_file()
                if (is_package or is_file) and not module_found:
                    paths.append(str(path))
                    module_found = True
                    pass
                pass
            if not module_found:
                paths.append("external:{}".format(module))
            pass
        return set(paths)

    def get_module_deps(self) -> Set["DependencyGraph"]:
        """Get imported modules' dependancy graph objects.

        Generates a set of DependencyGraph objects of the found modules'
        paths from 'get_module_paths'.

        :returns: Set of dependencies as DependencyGraph objects.
        :rtype: Set["DependencyGraph"]
        """
        deps = []
        for path in self.module_paths:
            if path.startswith("external:"):
                dep = DependencyGraph(path, self.search_paths)
                deps.append(dep)
                pass
            else:
                dep = DependencyGraph(path, self.search_paths)
                deps.append(dep)
                pass
        return set(deps)

    @staticmethod
    def is_package(abs_path: str) -> bool:
        """Get True if 'abs_path' is package directory, else False.

        :param abs_path: path to the potential package directory.
        :type abs_path: str
        :return: True if ``abs_path`` is package dir.
        :rtype: bool
        """
        ans = False
        path = Path(abs_path)
        if path.is_dir():
            init = path.joinpath("__init__.py")
            if init.is_file():
                ans = True
                pass
            pass
        return ans

    def __str__(self) -> str:
        """Get string representation of the dependency graph.

        :return: String representation of the dependency graph.
        """
        text = "Root Filename: {}\n".format(self.root_filename)
        for dep in self.module_deps:
            text += "\t" + str(dep)
            pass
        return text

    pass
