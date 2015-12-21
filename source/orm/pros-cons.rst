==============================================
The Pros and Cons of a Relational Document ORM
==============================================
A document database is a very simple key/value database. There are no relationships, no queries.

..  admonition:: pro

    PRO: Retrieving a record is super fast.


..  admonition:: con

    CON: You can't do a query on relationships.


There are a variety of ways to escape the lack of relationships. You can create a serialised list of IDs on your
object, use sets in your document database, etc. When you attempt to clean this up in a nice, tidy object orientated
manner in your application, however, things can get very messy, very quickly, as your application starts to grow in
complexity.

Relational Document ORM to the Rescue
=====================================
The theory behind a relational document ORM is to abstract the method you use to counter the lack of relationships.
If you're using Redis, the Redis driver will use sets and sorted sets to create relational ORM style functions. If you
use the filesystem driver - the most pure of key/value databases - then the filesystem will use serialised lists in
individual files (documents) to maintain relationship metadata.

The Downside
============
The pretense of a document database is speed and simplicity. You pull a document from the most efficient indexing
engine possible (a filesystem hashtable, for example) and there is no overhead that an SQL engine requires.

But now you've started adding the complications of relationship and index management, except this is not done on the
database server but rather on the application layer itself! Not so bad, except now the communication between the
application and the database is increased dramatically, and network latency starts to play a very big role.

..  tip::

    Consider a read-only slave on your application server (or web server) to reduce the latency between the application
    and database server.

Conclusion
==========
You can't avoid this, you will now start to seriously increase the number of requests between your application and
database as you make many more smaller requests for little bits and pieces of information. What is now the application
developers responsibility to make sure they're only using the complicated factors of inter-document relationships
when absolutely required. Keep your application design as simple as possible to take advantage of document engines.
