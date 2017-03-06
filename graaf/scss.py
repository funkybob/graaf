from __future__ import absolute_import

import os

import sass

from .base import Generator


class SassGenerator(Generator):
    extensions = ['.scss', '.sass']

    def __init__(self, include_paths=None, include_source=True, minify=True):
        self.include_paths = include_paths or []
        self.include_source = include_source
        self.minify = minify

    def can_process(self, filename):
        return super(SassGenerator, self).can_process(filename) and not filename.startswith('_')

    def process(self, root, dest_dir, filename, processor):
        basename, ext = os.path.splitext(filename)

        include_paths = self.include_paths
        if self.include_source:
            include_paths.append(processor.srcdir)

        with open(os.path.join(root, filename)) as fin:
            with open(os.path.join(dest_dir, basename + '.css'), 'w') as fout:
                fout.write(sass.compile_string(
                    fin.read(),
                    include_paths=include_paths[0],
                    output_style=sass.SASS_STYLE_COMPRESSED if self.minify else sass.SASS_STYLE_NESTED,
                ))

        return True
