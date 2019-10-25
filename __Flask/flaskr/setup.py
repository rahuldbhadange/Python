from setuptools import setup

setup(
    name='flaskr',
    packages=['flaskr'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)

# When using setuptools,
# it is also necessary to specify any special files that should be included in your package (in the MANIFEST.in).
# In this case, the static and templates directories need to be included, as well as the schema.
# Create the MANIFEST.in and add the following lines:
# graft flaskr/templates
# graft flaskr/static
# include flaskr/schema.sql
