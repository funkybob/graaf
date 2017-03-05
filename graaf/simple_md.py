import os

import markdown

from .base import Generator, get_yaml

md = markdown.Markdown()


class SimpleMarkdown(Generator):
    extensions = ['.md']

    def process(self, root, dest_dir, filename, processor):
        basename, ext = os.path.splitext(filename)

        processor.context.push(**get_yaml(os.path.join(root, basename + '.yml')))
        with open(os.path.join(root, filename)) as fin:
            processor.context['content'] = md.reset().convert(fin.read())
        tmpl = processor.templates[processor.context['template']]
        with open(os.path.join(dest_dir, basename + '.html'), 'w') as fout:
            fout.write(tmpl.render(processor.context))
        processor.context.pop()

        return True
