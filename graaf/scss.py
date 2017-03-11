from __future__ import absolute_import

import os

from scss.compiler import Compiler
from stencil import Template

from .base import Generator


class SassGenerator(Generator):
    '''
    Process .scss and .sass files as SCSS/SASS.

    Content will be passed through templating before processing, so it can
    contain variables and other template operations.

    Filenames beginning with '_' will be ignored.

    Arguments:

    - include_paths:
        A list of paths for the SCSS processor to search for @include statements.
    - include_source:
        Automatically add the pages source directory to the `include_paths` list.
    - minify:
        Minify the output if True, output nested if False.
    '''
    extensions = ['.scss', '.sass']

    def __init__(self, include_paths=None, include_source=True, minify=True):
        self.include_paths = include_paths or []
        self.include_source = include_source
        self.minify = minify

    def can_process(self, filename):
        return (
            super(SassGenerator, self).can_process(filename) and
            not filename.startswith('_')
        )

    def process(self, src_dir, dest_dir, filename, processor):
        basename, ext = os.path.splitext(filename)

        include_paths = self.include_paths
        if self.include_source:
            include_paths.append(processor.srcdir)

        scss_source = self.read_file(src_dir, filename)
        scss_source = Template(scss_source).render(processor.context)
        compiler = Compiler(search_path=include_paths)
        content = compiler.compile_string(scss_source, output_style='compressed' if self.minify else 'nested')
        self.write_file(dest_dir, basename + '.css', content)

        return True
