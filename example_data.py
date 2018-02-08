#This is the Kid class.
#Note that the initializer takes 2 arguments:
#  name
#  age
class Kid:
    def __init__(self, name="Unknown", age=0):
        self.name = name
        self.age = age

#This is the Family class.
#It is defined by a 3 pieces of data:
# parent1
# parent2
# an array of kids
#Note that parent1 and parent2 are passed into the initializer
class Family:
    def __init__(self, parent1=None, parent2=None):
        self.parent1 = parent1
        self.parent2 = parent2
        self.kids = []

    def add_kid(self, kid):
        self.kids.append(kid)

    def __str__(self):
        return_str = "Analyzing family data:\n"
        return_str += " Parent1 = "+str(self.parent1) + "\n"
        return_str += " Parent2 = "+str(self.parent2) + "\n"
        kid_count = 0
        for kid in self.kids:
            return_str += "  Kid "+str(kid_count) + "\n"
            return_str += "    Name = "+kid.name + "\n"
            return_str += "    Age  = "+str(kid.age) + "\n"
            kid_count += 1
        return return_str