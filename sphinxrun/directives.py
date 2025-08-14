import importlib.metadata
import multiprocessing
from multiprocessing.shared_memory import ShareableList

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective
from sphinx.util.typing import ExtensionMetadata

from .runner import run


class RunSetupDirective(SphinxDirective):
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        "group": directives.unchanged,
    }

    def run(self) -> list[nodes.Node]:
        group = self.options.get("group", "DEFAULT")

        code = "\n".join(self.content.data)

        if "RunSetupDirective.groups" not in self.env.current_document:
            self.env.current_document["RunSetupDirective.groups"] = {}

        self.env.current_document["RunSetupDirective.groups"][group] = code

        return []


class RunDirective(SphinxDirective):
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        "group": directives.unchanged,
    }

    @staticmethod
    def target(setupcode, code):
        output = []
        exec(setupcode)
        exec(code)
        return output

    def run(self) -> list[nodes.Node]:
        group = self.options.get("group", "DEFAULT")

        code = "\n".join(self.content.data)

        try:
            setupcode = self.env.current_document["RunSetupDirective.groups"][group]
        except KeyError:
            setupcode = ""

        explicit_nodes, stdout = run(setupcode, code, self.env.settings)

        stdout_nodes = self.parse_text_to_nodes(stdout)

        return explicit_nodes + stdout_nodes


def setup(app: Sphinx) -> ExtensionMetadata:
    """Register hook for the `..runsetup` and `..run` directives."""
    app.add_directive("runsetup", RunSetupDirective)
    app.add_directive("run", RunDirective)

    return {
        "version": importlib.metadata.version("sphinxrun"),
        "parallel_read_safe": False,
        "parallel_write_safe": True,
    }
