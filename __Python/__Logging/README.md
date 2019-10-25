Logging in Python

Logging is a means of tracking events that happen when some software runs. Logging is important for software developing, debugging and running. If you don�t have any logging record and your program crashes, there are very little chances that you detect the cause of the problem. And if you detect the cause, it will consume a lot of time. With logging, you can leave a trail of breadcrumbs so that if something goes wrong, we can determine the cause of the problem.
There are a number of situations like if you are expecting an integer, you have been given a float and you can a cloud API, the service is down for maintenance and much more. Such problems are out of control and are hard to determine.



Why Printing is not a good option?

Some developers use the concept of printing the statements to validate if the statements are executed correctly or some error has occurred. But printing is not a good idea. It may solve your issues for simple scripts but for complex scripts, printing approach will fail.

Python has a built-in module logging which allows writing status messages to a file or any other output streams. The file can contain the information on which part of the code is executed and what problems have been arisen.



Levels of Log Message

There are two built-in levels of the log message.

Debug : These are used to give Detailed information, typically of interest only when diagnosing problems.
Info : These are used to Confirm that things are working as expected
Warning : These are used an indication that something unexpected happened, or indicative of some problem in the near future
Error : This tells that due to a more serious problem, the software has not been able to perform some function
Critical : This tells serious error, indicating that the program itself may be unable to continue running
If required, developers have the option to create more levels but these are sufficient enough to handle every possible situation. Each built-in level has been assigned its numeric value.


Logging module is packed with several features. It has several constants, classes, and methods. The items with all caps are constant, the capitalize items are classes and the items which start with lowercase letters are methods.
There are several logger objects offered by the module itself.

Logger.info(msg) : This will log a message with level INFO on this logger.
Logger.warning(msg) : This will log a message with level WARNING on this logger.
Logger.error(msg) : This will log a message with level ERROR on this logger.
Logger.critical(msg) : This will log a message with level CRITICAL on this logger.
Logger.log(lvl,msg) : This will Logs a message with integer level lvl on this logger.
Logger.exception(msg) : This will log a message with level ERROR on this logger.
Logger.setLevel(lvl) : This function sets the threshold of this logger to lvl. This means that all the messages below this level will be ignored.
Logger.addFilter(filt) : This adds a specific filter filt to the to this logger.
Logger.removeFilter(filt) : This removes a specific filter filt to the to this logger.
Logger.filter(record) : This method applies the logger�s filter to the record provided and returns True if record is to be processed. Else, it will return False.
Logger.addHandler(hdlr) : This adds a specific handler hdlr to the to this logger.
Logger.removeHandler(hdlr) : This removes a specific handler hdlr to the to this logger.
Logger.hasHandlers() : This checks if the logger has any handler configured or not.