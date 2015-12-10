Quick Start
===========

Installing
----------
The best way to get started with the ORM is to add it to your :code:`composer.json`:

..  code:: bash

    composer require bravo3/orm

..  tip::

    For those unfamiliar with Composer you can get more information on the
    `Composer website <https://getcomposer.org/>`_.

If you're planning to use Redis then you also need to install Predis, if you plan to use YAML for entity metadata, then
you also need the Symfony YAML component:

..  code:: bash

    composer require predis/predis symfony/yaml

Creating a Manager
------------------
Your entity manager is your master service to all things ORM. You must construct an entity manager with a driver
(connection to your database) and a mapper (a method of understanding your entities). An entity manager must be
constructed using the factory function:

..  code-block:: php

    use Bravo3\Orm\Drivers\Redis\RedisDriver;
    use Bravo3\Orm\Mappers\Annotation\AnnotationMapper;
    use Bravo3\Orm\Services\EntityManager;

    $driver = new RedisDriver(['host' => '127.0.0.1', 'port' => 6379, 'database' => 0]);
    $mapper = new AnnotationMapper();

    $manager = EntityManager::build($driver, $mapper);

The above example will require your entities contain annotations to explain their table names, columns, relationships,
etc. You don't need to use annotations however, you could also use the :code:`YamlMapper` or even a chained mapper
which will give you the ability to support multiple mapping types in a single manager.

..  code-block:: php

    use Bravo3\Orm\Drivers\Redis\RedisDriver;
    use Bravo3\Orm\Mappers\Annotation\AnnotationMapper;
    use Bravo3\Orm\Mappers\Chained\ChainedMapper;
    use Bravo3\Orm\Mappers\Yaml\YamlMapper;
    use Bravo3\Orm\Services\EntityManager;

    $driver = new RedisDriver(['host' => '127.0.0.1', 'port' => 6379, 'database' => 0]);
    $mapper = new ChainedMapper(
        [
            new AnnotationMapper(),
            new YamlMapper(['entities.yml'])
        ]
    );

    $manager = EntityManager::build($driver, $mapper);

This now gives you an entity manager with the ability to support annotations or YAML metadata. :code:`entities.yml`
is a file we'll use a little further down to store all our metadata.

Creating Entities
-----------------
Entities are value-holder classes, they should contain no special logic other than getter and setters. You may inherit
a base class and you can use traits in your entities, however.

Let's get started with a basic :code:`User` entity:

..  code-block:: php

    <?php
    namespace MyApp\Entity;

    class User
    {
        private $id;
        private $username;

        public function getId()
        {
            return $this->id;
        }

        public function setId($id)
        {
            $this->id = $id;
            return $this;
        }

        public function getUsername()
        {
            return $this->username;
        }

        public function setUsername($username)
        {
            $this->username = $username;
            return $this;
        }
    }

This is all your entity class needs, however you need some way of telling the entity manager what each field is. This
process is called mapping, which is why you've already created a chained mapper with annotation and YAML support.

.. configuration-block::

    .. code-block:: yaml

        # entities.yml
        MyApp\Entity\User:
            table: 'users'
            columns:
                id: { type: int, id: true }
                username: { type: string }

    .. code-block:: php-annotations

        <?php
        namespace MyApp\Entity;

        use Bravo3\Orm\Annotations as Orm;

        /**
         * @Orm\Entity(table="users")
         */
        class User
        {
            /**
             * @Orm\Column(type="int")
             * @Orm\Id()
             */
            private $id;

            /**
             * @Orm\Column(type="string")
             */
            private $username;

            public function getId()
            {
                return $this->id;
            }

            public function setId($id)
            {
                $this->id = $id;
                return $this;
            }

            public function getUsername()
            {
                return $this->username;
            }

            public function setUsername($username)
            {
                $this->username = $username;
                return $this;
            }
        }

You need either to create a YAML file (:code:`entities.yml`) or add annotations to your entity class, there is no need
to do both.

..  caution::

    Annotations have more overhead than most other mappers, and have some caveats in the deeper internal workings of
    the ORM. See :doc:`dangers-of-annotations`.

You're now ready to make your first database calls.

Persisting a Record
-------------------
When performing write operations to the database it's important to keep in mind that all operations are done in bulk
and not immediate at the time you call a write function on the entity manager.

To complete your transaction, you must run :code:`flush()` after your persist or delete operations.

..  code-block:: php

    use MyApp\Entity\User;

    $user = new User();
    $user->setId(1)->setUsername('bob');

    $manager->persist($user);
    // Nothing has happened at this point

    $manager->flush();
    // The user record has now been written

..  caution::

    After persisting a record you still have a "new" entity. Changes to that entity will not be tracked and subsequent
    operations will be treated as a new record.

    If you continue to work on the :code:`$user` entity, first run :code:`$manager->refresh($user);` to convert it to
    a managed entity.

Retrieving a Record
-------------------
Retrieving a record by its ID is the simplest and most efficient way to retrieve data:

..  code-block:: php

    use MyApp\Entity\User;

    $user = $manager->retrieve(User::class, 1);
    echo $user->getUsername()."\n";     // bob

Because objects are references, it is possible to modify an entity and ask the entity manager to retrieve it again. The
object returned will be the same (modified) object you've already got. If you need a fresh copy, you must ask the
entity manager to ignore the entity cache:

..  code-block:: php

    use MyApp\Entity\User;

    $user1 = $manager->retrieve(User::class, 1);
    $user1->getUsername();   // bob
    $user1->setUsername('barry');

    $user2 = $manager->retrieve(User::class, 1);
    $user2->getUsername();   // barry, $user2 is the same object as $user1

    $user3 = $manager->retrieve(User::class, 1, false);
    $user3->getUsername();   // bob, you have a fresh object

Deleting a Record
-----------------
A delete operation is similar to a persist operation, in that you need to explicitly flush the manager before the action
takes place:

..  code-block:: php

    $manager->delete($user);
    $manager->flush();
