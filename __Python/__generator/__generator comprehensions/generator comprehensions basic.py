# generator comprehensions
# They are also similar to list comprehensions.
# The only difference is that they don’t allocate memory for the whole list but generate one item at a time,
# thus more memory efficient.

multiples_gen = (i for i in range(30) if i % 3 == 0)
print(multiples_gen, type(multiples_gen))
# Output: <generator object <genexpr> at 0x7fdaa8e407d8>
for x in multiples_gen:
  print(x)
  # Outputs numbers
