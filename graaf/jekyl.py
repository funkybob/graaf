import os

import yaml
import markdown

from .base import Generator


md = markdown.Markdown()


class JekylGenerator(Generator):
    '''
    Generator to support Jekyl files.


    These files begin with a YAML document, followed by Markown content.
    '''
    extensions = ['.md', '.markdown']

    def process(self, root, dest_dir, filename, processor):
        basename, ext = os.path.splitext(filename)

        config = []

        with open(os.path.join(root, filename)) as fin:
            lines = iter(fin)

            line = next(lines)
            if line.rsplit() == '---':
                line = next(lines)

            try:
                while line.rsplit() != '---':
                    config.append(line)
                    line = next(lines)
            except StopIteration:
                return False

            config = yaml.load(''.join(config))
            content = ''.join(lines)

        config['content'] = markdown.reset().convert(content)
        with open(os.path.join(dest_dir, basename + '.html'), 'w') as fout:
            fout.write(processor.render('jekyl/%s.html' % config['layout'], config))

        return True
