# The decorator to make it bold
def make_bold(fn):
    # The new function the decorator returns
    def wrapper():
        # Insertion of some code before and after
        return '<b>' + fn() + '</b>'
    return wrapper


# The decorator to make it italic
def make_italic(fn):
    # The new function the decorator returns
    def wrapper():
        # Insertion of some code before and after
        return '<i>' + fn() + '</i>'
    return wrapper


@make_bold
@make_italic
def say():
    return 'hello'


print(say())
# outputs: <b><i>hello</i></b>


# This is the exact equivalent to
def say():
    return 'hello'


say = make_bold(make_italic(say))


print(say())
# outputs: <b><i>hello</i></b>
