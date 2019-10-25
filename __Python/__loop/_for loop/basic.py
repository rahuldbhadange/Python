# Loops
# Loops are a way to repeatedly execute some code. Here's an example:
Galaxy = "Milky Way"
planets = ["Sun - रवि/सूर्य", 'Mercury - बुध', 'Venus - शुक्र', 'Earth - पृथ्वी',
           'Mars - मंगल/मंगळ', 'Jupiter - गुरू/बृहस्पति', 'Saturn - शनि', 'Uranus - अरुण',
           'Neptune - वरुण', "Pluto - यम", "Moon - चंद्र/सोम",
           "Rahu (north node of the Moon) - राहु", "Ketu (south node of the Moon) - केतू"]

for planet in planets:
    # print(planet, end=' ')  # print all on same line
    print(planet)     # print all one after in column

# Mercury Venus Earth Mars Jupiter Saturn Uranus Neptune
# The for loop specifies

# the variable name to use (in this case, planet)
# the set of values to loop over (in this case, planets)
# You use the word "in" to link them together.
#
# The object to the right of the "in" can be any object that supports iteration.
# Basically, if it can be thought of as a group of things, you can probably loop over it.
# In addition to lists, we can iterate over the elements of a tuple:


multiplicands = (2, 2, 2, 3, 3, 5)
product = 1
for multi in multiplicands:
    product = product * multi

print("\n\n", product)

data = """
monday =  moon
tuesday = mars
wednesday = Mercury
thursday = jupiter
friday = Venus
saturday = saturn 
"""
print(data)

