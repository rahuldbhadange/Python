# importing module
import logging

# Create and configure logger
logging.basicConfig(filename="new_file22.log", level=logging.DEBUG, filemode='w')

# , format='%(asctime)s %(levelname)s [%(name)s] {%(threadName)s} %(message)s'
# Creating an object
# log = logging.getLogger()


# Setting the threshold of logger to DEBUG
# logger.setLevel(logging.DEBUG)


log = logging.getLogger(__name__)

DEBUG_ENABLED = log.isEnabledFor(logging.DEBUG)


# Test messages
log.debug(" logger.debug : This will log a message with all level, .debug, .info, .warning, .error and .critical !!!")
log.info(" logger.info : This will log a message with level, .info, .warning, .error and .critical ! "
         "But omits .debug !!!")
log.warning(" logger.warning : This will log a message with level, .warning, .error and .critical ! "
            "But omits .debug and .info !!!")
log.error(" logger.error : This will log a message with level, .error and .critical ! "
          "But omits .debug, .info and .warning !!!")
log.critical(" logger.critical : This will log a message with level only .critical ! "
             "And omits all other, .debug, .info, .warning and .error !!!")


# log = logging.getLogger(__name__)
#
# DEBUG_ENABLED = log.isEnabledFor(logging.DEBUG)












""""1000021": {
"hash": "99624e7feb2fd7264f1bb7fff5060580"
},
"1000015": {
"hash": "5757917dcedfd414a43cac6aa111a97f"
},
"1000020": {
"hash": "99624e7feb2fd7264f1bb7fff5060580"
}
"""