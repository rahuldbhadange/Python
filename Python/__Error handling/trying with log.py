# importing module
import logging

# Create and configure logger
logging.basicConfig(filename="newfile.log", format='%(asctime)s %(message)s', filemode='w')


# Creating an object
logger = logging.getLogger()


# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)

try:
    1555/"5"
except:
    logger.exception('Something happened')
