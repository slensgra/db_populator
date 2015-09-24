Database Populator
==================

At a glance
-----------

To run the command: `python manage.py populate_db`

___You have to run the command on a completely empty database with migrations applied, else it will crash.___

Description
-----------

Applys a simple, guided DFS technique to traverse a schema, and create a concrete / compact database.
The meat of the code base runs using a modified version of [django dynamic fixture](https://github.com/paulocheque/django-dynamic-fixture) by Paulo Cheque.

The populate\_db management command iterates through all models recognized by the ORM,
attempting to save each instance to the database. If the instance has a non-empty
chain of dependencies, the code fills out the dependencies before
saving the instance. Our code differs from ddf in that it stores
all previously created objects. When dependencies are filled out,
previously created objects are used to fill the chain unless otherwise specified.

The following three lists of classes are used to alter the behavior of the command. They should be set in your app's settings.py.
Note that all classes must be given in their fully qualified class name (with all modules and submodules).

#### IGNORE

The IGNORE list specifies
classes that will not be used in the top level constructor function. Most of the classes
currently in the IGNORE list are ones which require special fixture data to be saved.
The app works okay without them or auto-generates these, usually.

#### ALLOW\_MULTIPLE

The allow multiple specifies classes that will be created as though
they are not already in the list of created instances.
I.e. a profile may be dependent on a user, but it may
be nonsensical for all profiles to be associated to
a single user

_currently anything that is on the receiving end of a one\_to\_one will need to be in ALLOW\_MULTIPLE for proper behavior_.

#### REQUIREMENTS

Sometimes a web app may require a subgraph with specific properties. The requirements
list allows you to specify a subgraph in a json-like format. Requirements
are stored as a list of (possibly) nested dictionaries, keyed by the
field name (edge of the graph) that connects nodes with specific properties.

A useful example imported from our configuration:

```python

REQUIREMENTS = [
  # Examples of chained dependencies. This foo.bar.Baz selects a 'foo.Quux' with 'daedalus'
  # in the 'foo.Quux' field named 'name'
  # through its field with name 'qux'
  {'foo.bar.Baz': {'qux': {'foo.Quux': {'name': 'daedalus'}}}},
  {'foo.bar.Baz': {'qux': {'foo.Quux': {'name': 'tiresias'}}}},
  {'corge.Waldo': {'qux': {'foo.Quux': {'name': 'daedalus'}}, 'is_prophet': False}},
  {'corge.Waldo': {'qux': {'foo.Quux': {'name': 'tiresias'}}, 'is_prophet': True}},

  # Objects with specific properties may be declared without necessarily chaining
  {'django.contrib.auth.User': {'email': EMAIL_1}},
  {'django.contrib.auth.User': {'email': EMAIL_2}}
]

```
