=============
Configuration
=============
Configuration of the ORM is handled through a :code:`Configuration` class passed to the :code:`EntityManager`. All
sub-services of the entity manager will read the configuration from here. The only exception to this is the debug and
maintenance state of the entity manager itself. These are toggle options that can be changed at any time to alter the
state of an application during run-time.

Configuration Options
=====================

Cache Directory
---------------
The cache directory is required for the proxy manager to store class files for proxied entities. If omitted, your
system cache directory will be used. It is strongly recommend you set this cache directory to your applications cache
directory so that flushing cache will also include flushing proxy cache.

Force Unique Key Restraints
---------------------------
Forcing unique key restraints prevents an entity from overwriting the unique key of another entity. This will give your
application similar behaviour to an SQL style unique key restraint. If you disable this option, persisting an entity
with the same key will simply overwrite the previous key, taking ownership of that key.

..  note::

    If you disable the uniqueness restraint then the :code:`UniqueIndexManager` will check for a contested index before
    deleting it to prevent it deleting an index pointing to a different entity with the same value.

Run-time Toggles
================

Maintenance Mode
----------------
Maintenance mode is designed to correct anomalies or integrity violations in the database, specifically around
relationships or indices. If an entity schema has modified a relationship, you may want to rebuild your tables to
add new conditions, for example.

Maintenance mode forces the entity manager to ignore deltas and checks for modifications - this creates reduces the
efficiency of the entity manager, but will force all indices to be completely rebuilt.

Debug Mode
----------
Debug mode adds additional logging at the driver level. This is a very low-level form of logging, and is helpful for
the design of new drivers. The driver is aware of the debug state and may send log commands to the server or write to
its own logging interface.
