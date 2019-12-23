open(): open function is a pre-defined function used to open a file
At the time of openening a file,we need to specify the mode of the file.
mode indicates for what pupose you are opening the file.
The various modes are
        Mode               Description
    1.  'r'------------> opens a file for reading data(default)
    2.  'w'------------> opens a file to write data into file.
                         It creates a new file if the file
                         doesnot exist.
                         if file already exists then it
                         truncates(removes)
    3.  'a'------------> opens a file to append data at the
                         end of the file.
                         if file doesnt exist it creates a new file.
    4.  't'------------> opens a file in text mode.
    5.  'b'------------>opens a file in binary mode.
    6.  'w+'------------>opens a file to write and read data of a file.
                         The previous data in the file will be deleted.
    7.  'r+'------------>opens a file to read and write data into a file.
                         The previous data in the file will not be deleted.
                         The File pointer will be at the beginning of file.
    8.  'a+'------------>opens a file to append and read data of a file.
                         The file pointer will be at the end of the file
                         
