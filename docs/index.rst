
Graaf - static sites generator
==============================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   config
   api/graaf


Why Graaf?
----------

This project is named after
`Van de Graaf <https://en.wikipedia.org/wiki/Van_de_Graaff_generator>`_.

Why did you build it?
---------------------

Recently I've built a number of sites backed by AWS API Gateway, and needed a
way to build their static pages, but remain consistent with the templates and
styles of the rest of the site.


How it works
------------

1. Put your source content in a directory. By default this is called `pages`.

2. You create a target directory to generate the content in. By default this is
called `assets`.

3. Write templates for your content. By default these go in a directory called
`templates`.

4. You run `graaf`

It will find every file in your sirce directory, and check if any of its
configured Generators will work on it.  If so, they will be invoked, and
(typically) generate an output file.

5. PROFIT!

Configuration
-------------

The main configuration file is called ``graaf.yml`` and contains two main
sections:

paths
`````

Here you can override any of three directories

.. code-block:: yaml

   paths:
     srcdir:
     destdir:
     templates:


generators
``````````

This is a list of generator classes to use, in order.

Each item in the list is a map with at least the import name of a Generator
class.  It may also include arguments to pass to the Generator for
configuration.

.. code-block:: yaml

   generators:
     - name: 'graaf.simple_md.SimpleMarkdown'
     - name: 'graaf.scss.SassGenerator'


