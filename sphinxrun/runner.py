import multiprocessing
import os
import pickle as pkl
import socket
import subprocess
import sys
from tempfile import NamedTemporaryFile

import docutils

_outputs = []


def show(node: docutils.nodes.Node):
    """Insert a node in the document."""
    _outputs.append(node)


def dump():
    """Called by the runner process to export shown nodes."""
    with open(os.environ["SPHINXRUN_OUTPUT"], "wb") as f:
        pkl.dump(_outputs, f)


def run(setupcode, code, static_path) -> list[docutils.nodes.Node]:
    """Execute the code and return generated docutils nodes."""
    with NamedTemporaryFile("w+") as script, NamedTemporaryFile("rb") as dumpfile:
        # Write code to a temporary script file
        script.write(setupcode + "\n")
        script.write(code + "\n")
        script.write("\n".join(["import sphinxrun.runner", "sphinxrun.runner.dump()"]))
        script.flush()

        # Run the code in a separate python process
        env = os.environ.copy()
        env["SPHINXRUN_OUTPUT"] = dumpfile.name
        p = subprocess.run(
            [sys.executable, script.name], capture_output=True, text=True, env=env
        )

        # Reload dumped nodes
        dumpfile.flush()
        explicit_nodes = pkl.load(dumpfile)

    return explicit_nodes, p.stdout
