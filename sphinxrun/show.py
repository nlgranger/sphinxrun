import os
from typing import Text


def show(content: Text):
    """Insert content at the position of the calling :rst:`.. run::` directive."""
    with open(os.environ["SPHINXRUN_OUTPUT"], "a") as f:
        f.write(content + "\n\n")
        f.flush()
