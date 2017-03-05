from __future__ import absolute_import

import os

from scss import Compiler

from .base import Generator


class SassGenerator(Generator):
    extensions = ['.scss', '.sass']

    def process(self, root, dest_dir, filename, processor):
        basename, ext = os.path.splitext(filename)

        compiler = Compiler(search_path=[processor.srcdir])

        with open(os.path.join(root, filename)) as fin:
            with open(os.path.join(dest_dir, filename), 'w') as fout:
                fout.write(compiler.compile_string(fin.read()))

        return True
