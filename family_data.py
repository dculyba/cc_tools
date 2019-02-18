#This is the Kid class.
#Note that the initializer takes 2 arguments:
#  name
#  age
class Kid:
    def __init__(self, name="Unknown", age=0):
        self.name = name
        self.age = age

#This is the Family class.
#It is defined by a 2 pieces of data:
# an array of parents
# an array of kids
class Family:
    def __init__(self):
        self.parents = []
        self.kids = []

    def add_kid(self, kid):
        self.kids.append(kid)

    def __str__(self):
        return_str = "Analyzing family data:\n"
        parent_count = 0
        for parent_name in self.parents:
            return_str += " Parent "+str(parent_count)+" = "+parent_name +"\n";
            parent_count += 1
        kid_count = 0
        for kid in self.kids:
            return_str += "  Kid "+str(kid_count) + "\n"
            return_str += "    Name = "+kid.name + "\n"
            return_str += "    Age  = "+str(kid.age) + "\n"
            kid_count += 1
        return return_str