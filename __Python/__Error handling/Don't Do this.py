# Don't Do this
# If you're using this form of exception handling:

try:
    something
except:     # don't just do a bare except!
    pass
# Then you won't be able to interrupt your something block with Ctrl-C.
# Your program will overlook every possible Exception inside the try code block.

# Here's another example that will have the same undesirable behavior:

# except BaseException as e: # don't do this either - same as bare!
#     logging.info(e)
# Instead, try to only catch the specific exception you know you're looking for.
# For example, if you know you might get a value-error on a conversion:


try:
    foo = operation_that_includes_int(foo)
except ValueError as e:
    if fatal_condition(): # You can raise the exception if it's bad,
        logging.info(e)   # but if it's fatal every time,
        raise             # you probably should just not catch it.
    else:                 # Only catch exceptions you are prepared to handle.
        foo = 0           # Here we simply assign foo to 0 and continue.

# Further Explanation with another example
# You might be doing it because you've been web-scraping and been getting say,
# a UnicodeError, but because you've used the broadest Exception catching, your code,
# which may have other fundamental flaws, will attempt to run to completion, wasting bandwidth,
# processing time, wear and tear on your equipment, running out of memory, collecting garbage data, etc.

# If other people are asking you to complete so that they can rely on your code,
# I understand feeling compelled to just handle everything.
# But if you're willing to fail noisily as you develop, you will have the opportunity
# to correct problems that might only pop up intermittently, but that would be long term costly bugs.

# With more precise error handling, you code can be more robust
