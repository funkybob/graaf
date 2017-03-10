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
            if line.rstrip() == '---':
                line = next(lines)

            try:
                while line.rstrip() != '---':
                    config.append(line)
                    line = next(lines)
            except StopIteration:
                print "Failed to find end of document: %r" % line
                return False

            config = yaml.load(''.join(config))
            content = ''.join(lines)

        config['content'] = md.reset().convert(content)

        if 'layout' in config:
            template_name = 'jekyl/%s.html' % (config['layout'],)
        else:
            template_name = config['template']
        with open(os.path.join(dest_dir, basename + '.html'), 'w') as fout:
            fout.write(processor.render(template_name, config))

        return True
