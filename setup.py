from distutils.core import setup

from graaf import get_version

setup(
    name='graaf',
    version=get_version(),
    description='Simple static site generator',
    author='Curtis Maloney',
    author_email='curtis@tinbrain.net',
    url='https://github.com/funkybob/graaf',
    packages=['graaf'],
    install_requires=[
        'stencil-template',
        'Markdown',
        'pyyaml',
        'pyScss',
    ],
    scripts=['scripts/graaf'],
)
