def func(obj): 
	obj.capital() 
	obj.language() 
	obj.type()


	def capital():
		print("Delhi")


def India():
	print("India")


def USA():
	print("USA")

obj_ind = India()

obj_usa = USA() 


func(obj_ind) 
func(obj_usa) 
