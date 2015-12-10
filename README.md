Bravo3 Documention
==================
Bravo3 component documentation. 

Installing
----------
    
    # Required packages
    apt-get install python python-pip node npm make ruby ruby-dev
    npm install -g bower
    pip install -r requirements.txt
    gem install sass
    
    # Third-party assets
    bower install

Compiling Documentation
-----------------------
To create HTML documentation, simply run make:

    make dirhtml

Docs will be compiled into the `build/` directory. If you've modified the CSS/JS files, you might want to run
`make clean` before recompiling to ensure the SCSS compiler picks up `@import` changes:

    make clean dirhtml

Platform.sh
-----------
These documents will be compiled automatically by Platform.sh.
