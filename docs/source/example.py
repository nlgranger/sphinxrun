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
