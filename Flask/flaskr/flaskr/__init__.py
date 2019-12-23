# To simplify locating the application, add the following import statement into this file, flaskr/__init__.py:
from .flaskr import app

# This import statement brings the application instance into the top-level of the application package.
# When it is time to run the application, the Flask development server needs the location of the app instance.
# This import statement simplifies the location process.
# Without it the export statement a few steps below would need to be export FLASK_APP=flaskr.flaskr.


# At this point you should be able to install the application.
# As usual, it is recommended to install your Flask application within a virtualenv.
# With that said, go ahead and install the application with:
#
# pip install --editable .
# The above installation command assumes that it is run within the projects root directory,
# flaskr/. The editable flag allows editing source code
# without having to reinstall the Flask app each time you make changes.
# The flaskr app is now installed in your virtualenv (see output of pip freeze).
#
# With that out of the way, you should be able to start up the application.
# Do this with the following commands:
#
# export FLASK_APP=flaskr
# export FLASK_DEBUG=true
# flask run
# (In case you are on Windows you need to use set instead of export).
# The FLASK_DEBUG flag enables or disables the interactive debugger.
# Never leave debug mode activated in a production system,
# because it will allow users to execute code on the server!
#
# You will see a message telling you that server has started along with the address at which you can access it.
#
# When you head over to the server in your browser,
# you will get a 404 error because we don’t have any views yet.
# That will be addressed a little later, but first, you should get the database working.
