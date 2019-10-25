def is_palindrome(word):
    q = len(word) - 1
    # print(word)
    for p in word:
        # print("p:", p)
        # print("q:", word[q])
        if p == word[q]:
            # print(p, word[q])
            q = q - 1
            # print("Yes !!!")
        else:
            # print("No !!!", p, word[q])
            return "No !!!", p, word[q]     # ***important
            break
    # return "Yes !!!"


ans, p, q = is_palindrome('delevelid')


if ans == None:
    print("Yes !!!")
else:
    print(ans, p, q)
