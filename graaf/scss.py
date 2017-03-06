from __future__ import absolute_import

import os

from scss import Compiler

from .base import Generator


class SassGenerator(Generator):
    extensions = ['.scss', '.sass']

    def __init__(self, include_paths=None, include_source=True, output_style='nested'):
        self.include_paths = include_paths or []
        self.include_source = include_source
        self.output_style = output_style

    def can_process(self, filename):
        return super(SassGenerator, self).can_process(filename) and not filename.startswith('_')

    def process(self, root, dest_dir, filename, processor):
        basename, ext = os.path.splitext(filename)

        search_path = self.include_paths
        if self.include_source:
            search_path.append(processor.srcdir)
        compiler = Compiler(search_path=search_path, output_style=self.output_style)

        with open(os.path.join(root, filename)) as fin:
            with open(os.path.join(dest_dir, basename + '.css'), 'w') as fout:
                fout.write(compiler.compile_string(fin.read()))

        return True
