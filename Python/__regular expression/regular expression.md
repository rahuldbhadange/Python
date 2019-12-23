#### Regular Expression

    A RegEx, or Regular Expression, is a sequence of characters that forms a "search pattern"
    
    RegEx can be used to check if a "string" contains the specified search pattern.

.

##### RegEx Functions

The re module offers a set of functions that allows us to search a string for a match:

            Function	                    Description
            
            findall	       :        Returns a list containing all matches
            search	       :        Returns a Match object if there is a match anywhere in the string
            split	       :        Returns a list where the string has been split at each match
            sub	           :        Replaces one or many matches with a string
            

####### The findall() Function :
    
    The findall() function returns a list containing all matches.
    The list contains the matches in the order they are found.
    
    If no matches are found, an empty list is returned:

            
####### The search() Function :
    
    The search() function searches the string for a match, and returns a Match object if there is a match.
    If there is more than one match, only the first occurrence of the match will be returned:
    
    If no matches are found, the value None is returned:


####### The split() Function
    
    The split() function returns a list where the string has been split at each match:
    
    You can control the number of occurrences by specifying the maxsplit parameter:
    
    
#######  The sub() Function
    
    The sub() function replaces the matches with the text of your choice:
    
    You can control the number of replacements by specifying the count parameter
    
#######    Match Object

    A Match Object is an object containing information about the search and the result.
    
    Note: If there is no match, the value None will be returned, instead of the Match Object.
    
    The Match object has properties and methods used to retrieve information about the search, and the result:
    
    .span() returns a tuple containing the start-, and end positions of the match.
    .string returns the string passed into the function
    .group() returns the part of the string where there was a match
    
    Note: If there is no match, the value None will be returned, instead of the Match Object.




##### Metacharacters
    
Metacharacters are characters with a special meaning:
    
            []	        A set of characters	"[a-m]"	
            \	        Signals a special sequence (can also be used to escape special characters)	"\d"	
            .	        Any character (except newline character)	"he..o"	
            ^	        Starts with	"^hello"	
            $	        Ends with	"world$"	
            *	        Zero or more occurrences	"aix*"	
            +	        One or more occurrences	"aix+"	
            {}	        Exactly the specified number of occurrences	"al{2}"	
            |	        Either or	"falls|stays"	
            ()	        Capture and group