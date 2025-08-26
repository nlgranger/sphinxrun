import multiprocessing
import os
import pickle as pkl
import socket
import subprocess
import sys
import textwrap
import weakref
from multiprocessing.connection import Connection
from tempfile import NamedTemporaryFile


class Runner:
    def __init__(self):
        self.pipe, child_pipe = multiprocessing.Pipe()
        self.proc = multiprocessing.Process(
            target=Runner.loop, args=[self.pipe, child_pipe]
        )
        self.proc.start()
        child_pipe.close()

    @staticmethod
    def loop(parent_pipe: Connection, pipe: Connection):
        parent_pipe.close()

        globals = {}
        locals = {}

        exec("import sphinxrun", globals, locals)

        while True:
            try:
                todo = pipe.recv()
            except EOFError:
                break

            with NamedTemporaryFile("r") as f:
                os.environ["SPHINXRUN_OUTPUT"] = f.name

                exec(todo, globals, locals)

                pipe.send(f.read())

    def __del__(self):
        self.stop()

    def stop(self):
        if self.proc.is_alive():
            self.proc.terminate()

        self.proc.join()

    def submit(self, code):
        self.pipe.send(code)
        out = self.pipe.recv()

        return out
