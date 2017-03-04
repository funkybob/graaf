from distutils.core import setup


setup(
    name='graaf',
    version='0.0.1',
    description='Simple static site generator',
    author='Curtis Maloney',
    author_email='curtis@tinbrain.net',
    url='https://github.com/funkybob/graaf',
    packages=['graaf',],
    install_requires=[
        'stencil-template',
        'Markdown',
        'pyyaml',
    ],
)
