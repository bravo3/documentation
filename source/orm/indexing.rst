Indexing
========
..  warning::

    Index naming conventions will be overhauled in release 0.6.0 of the ORM.


Indices apply to two places within the ORM:

1.  **On the table**

    * Allows a unique key lookup or
    * the ability to sort and filter records in the table

2.  **On a relationship**

    * Allows you to filter a set of related entities or
    * sort the relationship

Unique Index
------------
..  note::

    In release :code:`< 0.6.0` a "unique index" is referred to simply as an "Index".

A unique index allows you to create an index that can be dereferenced from an ID or slug. A useful example of this is
getting a user from their email address instead of their ID, or retrieving an article from its URL slug.

If compared to a traditional SQL table, this would appear like a unique key constraint. A unique index can be comprised
of multiple columns or even methods (getters, that return the value of the index).

..  configuration-block::

    ..  code-block:: yaml

        MyApp\Entity\IndexedEntity:
            columns:
                alpha: { type: string }
                bravo: { type: int }
                charlie: { type: bool }
            indices:
                ab: { columns: [alpha, bravo] }
                bc: { columns: [bravo], methods: [getCharlie] }
                b: { columns: [bravo] }

    ..  code-block:: php-annotations

        /**
         * @Entity(indices={
         *      @Index(name="ab", columns={"alpha", "bravo"}),
         *      @Index(name="bc", columns={"bravo"}, methods={"getCharlie"}),
         *      @Index(name="b", columns={"bravo"})
         * })
         */
        class IndexedEntity
        {
            ..
        }

..  code-block:: php

    $bravo = 200;

    // Retrieve using index 'b' from the column 'bravo' (int):
    $entity = $em->retrieveByIndex(IndexedEntity::class, 'b', $bravo);
    echo $entity->getBravo();   // 200

When using multiple columns in an index, the index is always concatenated using a period:

..  code-block:: php

    $alpha = 'hello';
    $bravo = 200;

    // Retrieve using index 'ab', a combination of 'alpha' (string) and 'bravo' (int):
    $entity = $em->retrieveByIndex(IndexedEntity::class, 'ab', $alpha.'.'.$bravo);
    echo $entity->getAlpha();   // hello

Boolean index values are serialised an integer, 0 or 1:

..  code-block:: php

    // Retrieve using index 'bc', a combination of 'bravo' (int) and 'charlie' (bool):
    $entity = $em->retrieveByIndex(IndexedEntity::class, 'bc', '200.1');
    $entity->getCharlie();   // true

..  caution::

    Release :code:`0.5.x` will allow a new entity to overwrite another entities unique index. This will raise an
    exception in release :code:`0.6.0`.

Sorted Table Index
------------------
This gives you the ability to sort and filter all records in a table. It is also the most efficient way to retrieve
all records in a table.

..  note::

    It is impossible to have an unsorted table filter.

This example provides an entity that can be sorted by name (:code:`name_all`) or can retrieve all "active" users,
sorted by name:

..  configuration-block::

    ..  code-block:: yaml

        MyApp\Entity\SortedUser:
            table: sorted_user
            columns:
                id: { type: int, id: true }
                name: { type: string }
                active: { type: bool }
            sortable:
                name_active: { column: name, conditions: [{ value: true, column: active }] }
                name_all: { column: name }

    ..  code-block:: php-annotations

        /**
         * @Entity(sortable_by={
         *      @Sortable(name="name_active", column="name", conditions={
         *          @Condition(column="active", value=true)
         *      }),
         *      @Sortable(name="name_all", column="name")
         * })
         */
        class SortedUser
        {
            ..
        }

..  code-block:: php

    $query = $em->sortedQuery(new SortedTableQuery(SortedUser::class, 'name_all'));
    $query->count(); // all users

    $query = $em->sortedQuery(new SortedTableQuery(SortedUser::class, 'name_active'));
    $query->count(); // only active users

    foreach ($query as $user) {
        echo $user->getName()."\n";
    }

All sorted queries can also take a direction (ascending/descending), a start index and an end index:

..  code-block:: php

    $stq = new SortedTableQuery(SortedUser::class, 'name_active', Direction::ASC(), 2, 5);
    $query = $em->sortedQuery($stq);
    $query->count(); // 4

The final parameter of any sorted query allows your query to universally ignore cache when retrieving entities - this
will ensure you do not get a modified object of the same entity from another code block.

..  note::

    The query result is a special list class that will retrieve entities from the database *at the time they are
    accessed*, not at the time the query is executed (lazy-loading).

Sorted Relationship Index
-------------------------
A sorted relationship index is almost completely identical to a :code:`SortedTableQuery`, they are both instances of
the :code:`SortedQuery` class.

..  configuration-block::

    ..  code-block:: yaml

        MyApp\Entity\Category:
            table: category
            columns:
                id: { type: int, id: true }
                name: { type: string }
                articles:
                    association: otm
                    target: MyApp\Entity\Article
                    inversed_by: category
                    sortable:
                        last_modified:
                            column: last_modified
                            conditions:
                                - { value: true, column: published }
                                - { value: 50, column: id, comparison: '>' }
                        id:
                            column: id
                        last_modified_all:
                            column: last_modified
                            conditions:
                                - { value: true, column: published }

    ..  code-block:: php-annotations

        use Bravo3\Orm\Annotations as Orm;

        /**
         * @Orm\Entity()
         */
        class Category
        {
            /**
             * NB: The `sortable_by` clause may contain a string or a `@Sortable` object
             *
             * @var Article[]
             * @Orm\OneToMany(
             *      target="MyApp\Entity\Article",
             *      inversed_by="category",
             *      sortable_by={
             *          @Orm\Sortable(column="last_modified", conditions={
             *              @Orm\Condition(column="published", value=true),
             *              @Orm\Condition(column="id", value=50, comparison=">")
             *          }),
             *          "id",
             *          @Orm\Sortable(column="last_modified", conditions={
             *              @Orm\Condition(column="published", value=true),
             *          }, name="last_modified_all")
             *      })
             */
            protected $articles;

            ..
        }

..  code-block:: php

    // Retrieve an object with a *to-many* relationship on it:
    $category = $em->retrieve(Category::class, 123);

    // Execute a query in the same way we did for tables:
    $sq = new SortedQuery($category, 'articles', 'sort_date', Direction::ASC(), 2, 5);
    $results = $em->sortedQuery($sq);

Full Set Size
-------------
Sorted queries (table or relationship) have the ability to retrieve the full set size even if we've asked for a start
and end index. By default the entity manager will not attempt to check the full set size (to reduce overhead) so you
must explicitly ask the entity manager to check the full set size when executing the query:


..  code-block:: php

    $sq = new SortedQuery($category, 'articles', 'sort_date', Direction::ASC(), 2, 5);
    $results = $em->sortedQuery($sq, true);
    $results->getFullSize());

Some drivers might know the full set size naturally as a process of filtering the data, however you can not rely on the
fact that all drivers will behave this way.
