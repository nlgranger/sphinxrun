import importlib.metadata
import multiprocessing
from multiprocessing.shared_memory import ShareableList

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective
from sphinx.util.typing import ExtensionMetadata

from .runner import Runner

runners = {}


class RunDirective(SphinxDirective):
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        "group": directives.unchanged,
    }

    def run(self) -> list[nodes.Node]:
        source = self.env.current_document.docname
        source = str(self.env.doc2path(source))
        group = self.options.get("group", "DEFAULT")

        if source not in runners:
            runners[source] = {}

        if group not in runners[source]:
            runners[source] = {group: Runner()}

        runner = runners[source][group]

        code = "\n".join(self.content.data)

        output = runner.submit(code)

        output_nodes = self.parse_text_to_nodes(output)

        return output_nodes


def doctree_read_handler(app: Sphinx, doctree: nodes.document):
    """Cleanup hook to stop runners when a document is parsed."""
    source = doctree.attributes["source"]
    if source in runners:
        for r in runners[source].values():
            r.stop()


def setup(app: Sphinx) -> ExtensionMetadata:
    """Register hook for the `.. run::` directives in sphinx."""
    app.add_directive("run", RunDirective)

    app.connect("doctree-read", doctree_read_handler)

    return {
        "version": importlib.metadata.version("sphinxrun"),
        "parallel_read_safe": False,
        "parallel_write_safe": True,
    }
