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

Deploying
---------
These documents are hosted on S3, to deploy you must have S3 configuration details in your `~/.aws/credentials` file:

    [bravo3]
    aws_access_key_id=xxx
    aws_secret_access_key=xxx

Then you can use `make` to deploy:
 
    make deploy
    
The `deploy` recipe has `dirhtml` as a requisite and will sync the `build/dirhtml`/ directory with the S3 bucket, 
changes will come live with the CDN cache expires.
