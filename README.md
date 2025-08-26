# Sphinxrun

SphinxRun registers a new `.. run::` directive to execute python commands dynamically while building a sphinx documentation.
It can be used to generate documentation artifacts such as figures or to insert dynamic content.

## Example:

```py
import textwrap


class Wrapper:
    """Wrapper class.

    .. run::

        from example import Wrapper

        d = Wrapper()

        with open("docs/source/lorem.txt") as f:
            text = f.read()
    """

    def wrap70(self, text):
        """Wrap text to 70 columns.

        .. run::

            output = d.wrap70(text)

            sphinxrun.show(output)
        """
        return textwrap.fill(text)
```

renders as:

![rendered doc screenshot](example.jpg)

## Installation

Install the package:

```sh
pip install sphinxrun
# or
uv add --dev sphinxrun
```

Then add the extension to the sphinx configuration:

```py
   extensions = [
      ...
      "sphinxrun"
   ]
```

## Documentation

The documentation is hosted at: https://sphinxrun.readthedocs.io/en/latest/