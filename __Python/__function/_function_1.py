'''
def is_alive(self):
    """Helper function to show if send & recv Threads are running"""
    if self.__send_ready.is_set() and self.__recv_ready.is_set():
        if self.__send_thread is not None and self.__recv_thread is not None:
            return self.__send_thread.is_alive() and self.__recv_thread.is_alive()
    return False
'''


rahul = None
kuldip = False
r = 5
k = None


def is_alive():
    """Helper function to show if send & recv Threads are running"""
    if rahul and kuldip:
        print("in")
        if r is not None and k is not None:
            return rahul() and kuldip()
        else:
            return 'inner false'
    else:
        return 'outer false'


def kuldip():
    print("kuldip function")
    # yield "kuldip"


def rahul():
    print("rahul function")
    # yield "rahul"


print(is_alive(), hex(id(is_alive())))
