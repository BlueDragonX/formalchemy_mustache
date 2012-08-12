
Mustache for FormAlchemy
========================

Implements a Mustache template engine for FormAlchemy.


Installation
------------

Get the source code and install the package:

  git clone git://github.com/BlueDragonX/formalchemy_mustache.git
  cd formalchemy_mustache
  python setup.py install


Usage
-----

To use with FormAlchemy:

  from formalchemy_mustache import configure
  dirs = ['/path_to_templates']
  configure(directories=dirs)

To use with Pyramid and pyramid_mustache, execute in main:

  config.include('formalchemy_mustache.pyramid.configure')


Authors
-------

The formalchemy_mustache project is the product of work by the following
people:

- Ryan Bourgeois <bluedragonx@gmail.com>


License
-------

The formalchemy_mustache project is licensed under the BSD-derived license and
is copyright (c) 2012 Ryan Bourgeois. A copy of the license is included in the
LICENSE file. If it is missing a copy can be found on the [project page][1].

[1]: https://github.com/BlueDragonX/formalchemy_mustache/blob/master/LICENSE	"License"

