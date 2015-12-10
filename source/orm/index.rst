Document ORM
============
The Document ORM component is a PHP7 ORM for document databases such as Redis. The purpose of such an ORM is to
provide not only an ORM layer for NoSQL databases but introduce relationship management to the mix.

The end result is an ORM similar to more traditional ORM's like Doctrine. However the rational behind using a document
database to begin with should not be forgotten as the more complex your relationships the less your advantage of using
a document database is.

:doc:`pros-cons`

The Bravo3 Document ORM achieves index and relationship management by using simple keys to store index values. This in
turn creates a software layer that does what most traditional SQL database servers would do internally.

General Usage
-------------

..  toctree::
    :maxdepth: 1

    quick-start
    indexing
    relationships
    queries
    mappers
    drivers
    key-schemes
    serialisers
    events

Advanced Concepts
-----------------

..  toctree::
    :maxdepth: 1

    race_conditions
    refs
    bundles/symfony
