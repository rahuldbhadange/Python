def is_palindrome(word):
    for i in word:
        j = len(word) - 1
        if word[i] == word[j]:
            return True
            # j = j+1
        else:
            return False


print(is_palindrome('Deleveled'))
