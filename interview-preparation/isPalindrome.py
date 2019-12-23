def isPalindrome(string):
    left, right = 0, len(string) - 1

    while right>=left:
        if not string[left]==string[right]:
            return False
        left += 1; right -= 1
        return True
isPalindrome('redrum murder')


def isPalindrome(string, left, right):
    print(string, left, right)
    if left == right:
        return True
    if not string[left]==string[right]:
        return False
    if left < right:
        isPalindrome(string, left + 1, right - 1)
    return True
    

string = 'redrum m1rder'
isPalindrome(string,  0, len(string) - 1)