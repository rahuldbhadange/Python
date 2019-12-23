#   Step 2: Application Setup Code:

# Now that the schema is in place, you can create the application module, flaskr.py.
# This file should be placed inside of the flaskr/flaskr folder.
# The first several lines of code in the application module are the needed import statements.
# After that there will be a few lines of configuration code. For small applications like flaskr,
# it is possible to drop the configuration directly into the module.
# However, a cleaner solution is to create a separate .ini or .py file, load that,
# and import the values from there.

# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash


# The next couple lines will create the actual application instance
# and initialize it with the config from the same file in flaskr.py:


app = Flask(__name__)   # create the application instance :)
app.config.from_object(__name__)    # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# The Config object works similarly to a dictionary, so it can be updated with new values.


# Database Path:
# Operating systems know the concept of a current working directory for each process.
# Unfortunately, you cannot depend on this in web applications
# because you might have more than one application in the same process.

# For this reason the app.root_path attribute can be used to get the path to the application.
# Together with the os.path module, files can then easily be found. In this example,
# we place the database right next to it.

# For a real-world application, it’s recommended to use Instance Folders instead.


# Usually, it is a good idea to load a separate, environment-specific configuration file.
# Flask allows you to import multiple configurations and it will use the setting defined in the last import.
# This enables robust configuration setups. from_envvar() can help achieve this.

#   app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# Simply define the environment variable FLASKR_SETTINGS that points to a config file to be loaded.
# The silent switch just tells Flask to not complain if no such environment key is set.

# In addition to that, you can use the from_object() method on the config object
# and provide it with an import name of a module. Flask will then initialize the variable from that module.
# Note that in all cases, only variable names that are uppercase are considered.

# The SECRET_KEY is needed to keep the client-side sessions secure.
# Choose that key wisely and as hard to guess and complex as possible.

# Lastly, you will add a method that allows for easy connections to the specified database.
# This can be used to open a connection on request and also from the interactive Python shell or a script.
# This will come in handy later. You can create a simple database connection through SQLite
# and then tell it to use the sqlite3.Row object to represent rows.
# This allows the rows to be treated as if they were dictionaries instead of tuples.

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


#   Step 4: Database Connections


# You currently have a function for establishing a database connection with connect_db,
# but by itself, it is not particularly useful.
# Creating and closing database connections all the time is very inefficient,
# so you will need to keep it around for longer. Because database connections encapsulate a transaction,
# you will need to make sure that only one request at a time uses the connection.
# An elegant way to do this is by utilizing the application context.

# Flask provides two contexts: the application context and the request context.
# For the time being, all you have to know is that there are special variables that use these.
# For instance, the request variable is the request object associated with the current request,
# whereas g is a general purpose variable associated with the current application context.
# The tutorial will cover some more details of this later on.

# For the time being, all you have to know is that you can store information safely on the g object.

# So when do you put it on there? To do that you can make a helper function.
# The first time the function is called, it will create a database connection for the current context,
# and successive calls will return the already established connection:


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

# Now you know how to connect, but how can you properly disconnect? For that,
# Flask provides us with the teardown_appcontext() decorator.
# It’s executed every time the application context tears down:


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
# Functions marked with teardown_appcontext() are called every time the app context tears down.
# What does this mean? Essentially, the app context is created before the request comes in
# and is destroyed (torn down) whenever the request finishes.
# A teardown can happen because of two reasons: either everything went well (the error parameter will be None)
# or an exception happened, in which case the error is passed to the teardown function


#   Step 5: Creating The Database


# As outlined earlier, Flaskr is a database powered application,
# and more precisely, it is an application powered by a relational database system.
# Such systems need a schema that tells them how to store that information.
# Before starting the server for the first time, it’s important to create that schema.

# Such a schema can be created by piping the schema.sql file into the sqlite3 command as follows:

# sqlite3 /tmp/flaskr.db < schema.sql
# The downside of this is that it requires the sqlite3 command to be installed,
# which is not necessarily the case on every system.
# This also requires that you provide the path to the database, which can introduce errors.
# It’s a good idea to add a function that initializes the database for you, to the application.

# To do this, you can create a function and hook it into a flask command that initializes the database.
# For now just take a look at the code segment below.
# A good place to add this function, and command, is just below the connect_db function in flaskr.py:

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

# The app.cli.command() decorator registers a new command with the flask script.
# When the command executes, Flask will automatically create an application context
# which is bound to the right application.
# Within the function, you can then access flask.g and other things as you might expect.
# When the script ends, the application context tears down and the database connection is released.

# You will want to keep an actual function around that initializes the database,
# though, so that we can easily create databases in unit tests later on.
# (For more information see Testing Flask Applications.)

# The open_resource() method of the application object is a convenient helper function
    # that will open a resource that the application provides.
    # This function opens a file from the resource location (the flaskr/flaskr folder) and allows you to read from it.
    # It is used in this example to execute a script on the database connection.

# The connection object provided by SQLite can give you a cursor object.
    # On that cursor, there is a method to execute a complete script.
    # Finally, you only have to commit the changes.
    # SQLite3 and other transactional databases will not commit unless you explicitly tell it to.

# Now, it is possible to create a database with the flask script:

# flask initdb
# Initialized the database.
