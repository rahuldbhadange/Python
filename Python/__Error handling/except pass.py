Don’t catch any error. Always specify which exceptions you are prepared to recover from and only catch those.
Try to avoid passing in except blocks. Unless explicitly desired, this is usually not a good sign.
But let’s go into detail:

Don’t catch any error
When using a try block, you usually do this because you know that there is a chance of an exception being thrown. As such, you also already have an approximate idea of what can break and what exception can be thrown. In such cases, you catch an exception because you can positively recover from it. That means that you are prepared for the exception and have some alternative plan which you will follow in case of that exception.

For example, when you ask for the user to input a number, you can convert the input using int() which might raise a ValueError. You can easily recover that by simply asking the user to try it again, so catching the ValueError and prompting the user again would be an appropriate plan. A different example would be if you want to read some configuration from a file, and that file happens to not exist. Because it is a configuration file, you might have some default configuration as a fallback, so the file is not exactly necessary. So catching a FileNotFoundError and simply applying the default configuration would be a good plan here. Now in both these cases, we have a very specific exception we expect and have an equally specific plan to recover from it. As such, in each case, we explicitly only except that certain exception.

However, if we were to catch everything, then—in addition to those exceptions we are prepared to recover from—there is also a chance that we get exceptions that we didn’t expect, and which we indeed cannot recover from; or shouldn’t recover from.

Let’s take the configuration file example from above. In case of a missing file, we just applied our default configuration, and might decided at a later point to automatically save the configuration (so next time, the file exists). Now imagine we get a IsADirectoryError, or a PermissionError instead. In such cases, we probably do not want to continue; we could still apply our default configuration, but we later won’t be able to save the file. And it’s likely that the user meant to have a custom configuration too, so using the default values is likely not desired. So we would want to tell the user about it immediately, and probably abort the program execution too. But that’s not something we want to do somewhere deep within some small code part; this is something of application-level importance, so it should be handled at the top—so let the exception bubble up.

Another simple example is also mentioned in the Python 2 idioms document. Here, a simple typo exists in the code which causes it to break. Because we are catching every exception, we also catch NameErrors and SyntaxErrors. Both are mistakes that happen to us all while programming; and both are mistakes we absolutely don’t want to include when shipping the code. But because we also caught those, we won’t even know that they occurred there and lose any help to debug it correctly.

But there are also more dangerous exceptions which we are unlikely prepared for. For example SystemError is usually something that happens rarely and which we cannot really plan for; it means there is something more complicated going on, something that likely prevents us from continuing the current task.

In any case, it’s very unlikely that you are prepared for everything in a small scale part of the code, so that’s really where you should only catch those exceptions you are prepared for. Some people suggest to at least catch Exception as it won’t include things like SystemExit and KeyboardInterrupt which by design are to terminate your application, but I would argue that this is still far too unspecific. There is only one place where I personally accept catching Exception or just any exception, and that is in a single global application-level exception handler which has the single purpose to log any exception we were not prepared for. That way, we can still retain as much information about unexpected exceptions, which we then can use to extend our code to handle those explicitly (if we can recover from them) or—in case of a bug—to create test cases to make sure it won’t happen again. But of course, that only works if we only ever caught those exceptions we were already expecting, so the ones we didn’t expect will naturally bubble up.

Try to avoid passing in except blocks
When explicitly catching a small selection of specific exceptions, there are many situations in which we will be fine by simply doing nothing. In such cases, just having except SomeSpecificException: pass is just fine. Most of the time though, this is not the case as we likely need some code related to the recovery process (as mentioned above). This can be for example something that retries the action again, or to set up a default value instead.

If that’s not the case though, for example because our code is already structured to repeat until it succeeds, then just passing is good enough. Taking our example from above, we might want to ask the user to enter a number. Because we know that users like to not do what we ask them for, we might just put it into a loop in the first place, so it could look like this:

def askForNumber ():
    while True:
        try:
            return int(input('Please enter a number: '))
        except ValueError:
            pass
Because we keep trying until no exception is thrown, we don’t need to do anything special in the except block, so this is fine. But of course, one might argue that we at least want to show the user some error message to tell him why he has to repeat the input.

In many other cases though, just passing in an except is a sign that we weren’t really prepared for the exception we are catching. Unless those exceptions are simple (like ValueError or TypeError), and the reason why we can pass is obvious, try to avoid just passing. If there’s really nothing to do (and you are absolutely sure about it), then consider adding a comment why that’s the case; otherwise, expand the except block to actually include some recovery code.

except: pass
The worst offender though is the combination of both. This means that we are willingly catching any error although we are absolutely not prepared for it and we also don’t do anything about it. You at least want to log the error and also likely reraise it to still terminate the application (it’s unlikely you can continue like normal after a MemoryError). Just passing though will not only keep the application somewhat alive (depending where you catch of course), but also throw away all the information, making it impossible to discover the error—which is especially true if you are not the one discovering it.

So the bottom line is: Catch only exceptions you really expect and are prepared to recover from; all others are likely either mistakes you should fix, or something you are not prepared for anyway. Passing specific exceptions is fine if you really don’t need to do something about them. In all other cases, it’s just a sign of presumption and being lazy. And you definitely want to fix that.