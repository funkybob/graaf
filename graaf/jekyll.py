import io
import os

import yaml
import markdown
from stencil import Template

from .base import Generator


md = markdown.Markdown()


class JekylGenerator(Generator):
    '''
    Generator to support Jekyl files.

    These files begin with a YAML document (called `Front Matter` in Jekyll
    documentation), followed by Markown content.

    The MD content is processed as a Template first, allowing variables, etc.

    If a `layout` is specified in the `Front Matter`, the template
    `jekyll/{layout}.html` will be used.
    Otherwise a `template` value must be specified in the `Front Matter`.
    '''
    extensions = ['.md', '.markdown']

    def process(self, root, dest_dir, filename, processor):
        basename, ext = os.path.splitext(filename)

        config = []

        with io.open(os.path.join(root, filename), encoding='utf-8') as fin:
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

        content = md.reset().convert(content)
        processor.context['content'] = Template(content).render(processor.context)

        if 'layout' in config:
            template_name = 'jekyll/%s.html' % (config['layout'],)
        else:
            template_name = config['template']
        self.write_file(dest_dir, basename + '.html', processor.render(template_name, config))

        return True
