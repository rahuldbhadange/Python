A MIME type is a label used to identify a type of data. It is used so software can know how to handle the data. It serves the same purpose on the Internet that file extensions do on Microsoft Windows.

So if a server says "This is text/html" the client can go "Ah, this is an HTML document, I can render that internally", while if the server says "This is application/pdf" the client can go "Ah, I need to launch the FoxIt PDF Reader plugin that the user has installed and that has registered itself as the application/pdf handler."

You'll most commonly find them in the headers of HTTP messages (to describe the content that an HTTP server is responding with or the formatting of the data that is being POSTed in a request) and in email headers (to describe the message format and attachments).






MIME stands for Multi-purpose Internet Mail Extensions. MIME types form a standard way of classifying file types on the Internet. Internet programs such as Web servers and browsers all have a list of MIME types, so that they can transfer files of the same type in the same way, no matter what operating system they are working in.

A MIME type has two parts: a type and a subtype. They are separated by a slash (/). For example, the MIME type for Microsoft Word files is application and the subtype is msword. Together, the complete MIME type is application/msword.

Although there is a complete list of MIME types, it does not list the extensions associated with the files, nor a description of the file type. This means that if you want to find the MIME type for a certain kind of file, it can be difficult. Sometimes you have to look through the list and make a guess as to the MIME type of the file you are concerned with.