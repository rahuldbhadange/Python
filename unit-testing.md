#### unit-testing-> integration-testing-> system-testing-> Acceptance-testing


unit-testing:

    - A unit is the smallest testable part of any software
    - The purpose is to validate that each unit of the software performs as designed.
    - In procedural programming, a unit may be an individual program, function, procedure, etc.
    - In object-oriented programming, the smallest unit is a method, 
      which may belong to a base/ super class, abstract class or derived/ child class.
      
      
      
import pytest

TEST_DATABASE = 'test'

@pytest.fixture()
def data_access():
    """Returns a DataAccess instance pointing to a local MongoDB installation.
    """
    access = DataAccess('mongodb://localhost:27017', TEST_DATABASE)
    access.open()
    access.client.drop_database(TEST_DATABASE)
    yield access
    access.client.drop_database(TEST_DATABASE)
    access.close()


    The main advantages of unit testing are:
    
    executing unit tests doesn’t require the application to be running. 
    And it can be done even before the whole application is built,
    unit testing leads to less bugs in the software,
    developers feel more confident in deploying code that is covered by unit tests,
    programmers following the Test-Driven Development (TDD) process claim that unit testing helps them achieve their goals faster, 
    solving problems with less code and better code architecture,
    with unit tests you can also improve parallel work, 
    you don’t need to wait for the whole project to be done to test just a piece of that.