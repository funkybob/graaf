import os
import shutil

from .base import Generator


class VerbatimGenerator(Generator):
    '''
    Copy _any_ file verbatim to the destination.

    Useful for static content like images and fonts.
    '''
    def can_process(self, filename):
        return True

    def process(self, root, dest_dir, filename, processor):
        shutil.copy(
            os.path.join(root, filename),
            os.path.join(dest_dir, filename)
        )

        return True
