"""
Data structures for manipulating Chip's Challenge (CC) data
Created for the class Programming for Game Designers
"""
BYTE_ORDER = "little"


class CCField:
    """The base field class
    Member vars:
        type_val (int): the type identifier of this class (set to 3)
        byte_val (bytes): the byte data of the field
    """

    def __init__(self, type_val, byte_val):
        self.type_val = type_val
        self.byte_val = byte_val

    @property
    def byte_data(self):
        return self.byte_val

    def __str__(self):
        return_str = "    Generic Field (type="+self.type_val+")\n"
        return_str += "      data = "+str(self.byte_val)
        return return_str


class CCMapTitleField(CCField):
    """A class defining the map title field
    Member vars:
        title (string): the title, max length 63 characters
    """

    def __init__(self, title):
        if __debug__:
            if len(title) >= 64: raise AssertionError("Map Title must be 63 characters or fewer. Current title is '"+title+"'("+str(len(title))+")")
        self.title = title
        self.type_val = 3 #The internal field identifier--used for the DAT file

    def __str__(self):
        return_str = "    Map Title Field (type=3)\n"
        return_str += "      title = '"+str(self.title)+"'"
        return return_str

    @property
    def byte_data(self):
        title_bytes = b""
        title_bytes += self.title.encode("ascii")
        title_bytes += b'\x00'
        return title_bytes


class CCCoordinate:
    """A class defining a single coordinate
    Member vars:
        x (int): x position, a value from 0 to 31
        y (int): y position, a value from 0 to 31
    """

    def __init__(self, x, y):
        if __debug__:
            if (x<0 or x>31) or (y<0 or y>31):
                raise AssertionError("Coordinates: ("+str(x)+", "+str(y)+") out of range. Coordinates must be from 0 to 31")
        self.x = x
        self.y = y

    def __str__(self):
        return "("+str(self.x)+", "+str(self.y)+")"


class CCTrapControl:
    """A class defining a single trap control
    Member vars:
        button_coord (CCCoordinate): the location of the brown button
        trap_coord (CCCoordinate): the location of the trap
    """

    def __init__(self, bx, by, tx, ty):
        """Traps are defined by a pairs of coordinates (bx, by, tx, ty)
        Note that all coordinates must be from 0 to 31
        Args:
            bx, by (int, int): the position of the button
            tx, ty (int, int): the position of the trap
        """
        self.button_coord = CCCoordinate(bx, by)
        self.trap_coord = CCCoordinate(tx, ty)

    def __str__(self):
        return "button"+str(self.button_coord)+", trap"+str(self.trap_coord)


class CCTrapControlsField(CCField):
    """A class defining the trap controls field
    Member vars:
        traps (list of CCTrapControl): a list of traps for the map
    """

    def __init__(self, traps):
        """A Trap Control Field is defined by a list of traps
        Note that there is a max of 25 traps per level
        Args:
            traps (list of CCTrapControl): the traps
        """
        if __debug__:
            if len(traps) > 25:
                raise AssertionError("Max trap count exceeded. Max trap count is 25. Number of traps passed = "+str(len(traps)))
        self.traps = traps
        self.type_val = 4  # The internal field identifier--used for the DAT file

    def __str__(self):
        return_str = "    Trap Controls Field (type=4)\n"
        for trap in self.traps:
            return_str += "      trap = "+str(trap)
            if trap != self.traps[-1]:
                return_str += "\n"
        return return_str

    @property
    def byte_data(self):
        byte_value = b""
        for trap in self.traps:
            byte_value += trap.button_coord.x.to_bytes(2, BYTE_ORDER)
            byte_value += trap.button_coord.y.to_bytes(2, BYTE_ORDER)
            byte_value += trap.trap_coord.x.to_bytes(2, BYTE_ORDER)
            byte_value += trap.trap_coord.y.to_bytes(2, BYTE_ORDER)
            byte_value += b'\x00\x00' #DAT format says to append 0 to the end of the coordinates
        return byte_value


class CCCloningMachineControl:
    """A class defining a single cloning machine control
    Member vars:
        button_coord (CCCoordinate): the location of the red button
        machine_coord (CCCoordinate): the location of the cloning machine
    """

    def __init__(self, bx, by, tx, ty):
        """Cloning Machines are defined by a pairs of coordinates (bx, by, tx, ty)
        Note that all coordinates must be from 0 to 31
        Args:
            bx, by (int, int): the position of the button
            tx, ty (int, int): the position of the machine
        """
        self.button_coord = CCCoordinate(bx, by)
        self.machine_coord = CCCoordinate(tx, ty)

    def __str__(self):
        return "button"+str(self.button_coord)+", machine"+str(self.machine_coord)


class CCCloningMachineControlsField(CCField):
    """A class defining the cloning machine controls field
    Member vars:
        machine (list of CCCloningMachineControl): a list of cloning machines for the map
    """

    def __init__(self, machines):
        """A cloning machine control field is defined by a list of machines
        Note that there is a max of 31 machines per level
        Args:
            machines (list of CCCloningMachineControl): the machines
        """
        if __debug__:
            if len(machines) > 31:
                raise AssertionError("Max cloning machine count of 31 exceeded. Number of cloning machines passed = "+str(len(machines)))
        self.machines = machines
        self.type_val = 5  # The internal field identifier--used for the DAT file

    def __str__(self):
        return_str = "    Cloning Machine Controls Field (type=5)\n"
        for machine in self.machines:
            return_str += "      machine = "+str(machine)
            if machine != self.machines[-1]:
                return_str += "\n"
        return return_str

    @property
    def byte_data(self):
        byte_value = b""
        for machine in self.machines:
            byte_value += machine.button_coord.x.to_bytes(2, BYTE_ORDER)
            byte_value += machine.button_coord.y.to_bytes(2, BYTE_ORDER)
            byte_value += machine.machine_coord.x.to_bytes(2, BYTE_ORDER)
            byte_value += machine.machine_coord.y.to_bytes(2, BYTE_ORDER)
        return byte_value


class CCEncodedPasswordField(CCField):
    """A class defining an encoded password
    Member vars:
        password (list of ints): a password encoded as a list of ints from 4 to 9 ints in length
    """

    def __init__(self, password):
        """Initializes an encoded password
        Args:
            password (list of ints) : the integer values of an encoded password
        """
        if __debug__:
            if len(password) > 9 or len(password) < 4:
                raise AssertionError("Encoded password must be from 4 to 9 characters in length. Password passed is '"+str(password)+"'")
        self.password = password
        self.type_val = 6  # The internal field identifier--used for the DAT file

    def __str__(self):
        return_str = "    Encoded Password Field (type=6)\n"
        return_str += "      password = "+str(self.password)
        return return_str

    @property
    def byte_data(self):
        password_bytes = b""
        for i in self.password:
            password_bytes += i.to_bytes(1, BYTE_ORDER)
        password_bytes += b'\x00'
        return password_bytes


class CCMapHintField(CCField):
    """A class defining a hint
    Member vars:
        hint (string): the hint for the level max length 127 characters
    """

    def __init__(self, hint):
        if __debug__:
            if len(hint) > 127 or len(hint) < 0:
                raise AssertionError("Hint must be from 0 to 127 characters in length. Hint passed is '"+hint+"'")
        self.hint = hint
        self.type_val = 7  # The internal field identifier--used for the DAT file

    def __str__(self):
        return_str = "    Map Hint Field (type=7)\n"
        return_str += "      hint = '"+str(self.hint)+"'"
        return return_str

    @property
    def byte_data(self):
        hint_bytes = b""
        hint_bytes += self.hint.encode("ascii")
        hint_bytes += b'\x00'
        return hint_bytes


##HERE FOR REFERENCE, BUT NOT SUPPORTED
##MAKE SURE YOU USE CCEncodedPasswordField for PASSWORDS
class CCPasswordField(CCField):
    """A class defining an unencoded password
    Member vars:
        password (string): the password string, length from 4 to 9 characters
    """
    password = ""

    def __init__(self, password):
        if __debug__:
            if len(password) > 9 or len(password) < 4:
                raise AssertionError("Password must be from 4 to 9 characters in length. Password passed is '"+password+"'")
        self.password = password
        self.type_val = 8  # The internal field identifier--used for the DAT file

    def __str__(self):
        return_str = "    Password Field (type=8)\n"
        return_str += "      password = '"+str(self.password)+"'"
        return return_str

    @property
    def byte_data(self):
        password_bytes = b""
        password_bytes += self.password.encode("ascii")
        password_bytes + b'\x00'
        return password_bytes


class CCMonsterMovementField(CCField):
    """A class defining the monsters that move in a given level
    Member vars:
        monsters (list of CCCoordinate): the coordinates of each monster
    """

    def __init__(self, monsters):
        if __debug__:
            if len(monsters) > 128:
                raise AssertionError("Max monster count of 128 exceeded. Number of monsters passed = "+str(len(monsters)))
        self.monsters = monsters
        self.type_val = 10  # The internal field identifier--used for the DAT file

    def __str__(self):
        return_str = "    Monster Movement Field (type=10)\n"
        for monster in self.monsters:
            return_str += "      monster = "+str(monster)
            if monster != self.monsters[-1]:
                return_str += "\n"
        return return_str

    @property
    def byte_data(self):
        byte_value = b""
        for monster in self.monsters:
            byte_value += monster.x.to_bytes(1, BYTE_ORDER)
            byte_value += monster.y.to_bytes(1, BYTE_ORDER)
        return byte_value


class CCLevel:
    """A class defining the data of a single level
    Member vars:
        level_number (int): the sequence number for this level. it corresponds to it's order in the list of levels
        time (int): the time limit in seconds for the level. 0 means no time limit
        num_chips (int): the number of computer chips to be collected in the level
            Layers: Chip's Challenge maps are 32x32 grids in 2 layers: upper and lower
            A single map layer is stored as an array of 1024 ints
        upper_layer (int list): the layer data for the upper (main) layer
        lower_layer (int list): the lower layer data. this allows for objects to be placed under other objects
        optional_fields (list of CCField types): the fields that augment the data of this level. all levels have a title and a password
    """
    def __init__(self):
        self.level_number = -1
        self.time = -1
        self.num_chips = -1
        self.upper_layer = []
        self.lower_layer = []
        self.optional_fields = []

    def __str__(self):
        return_str = ""
        return_str += "  Level #"+str(self.level_number)+"\n"
        return_str += "    Time Limit = "+str(self.time)+"\n"
        return_str += "    Chip Count = "+str(self.num_chips)+"\n"
        for field in self.optional_fields:
            return_str += str(field) + "\n"
        return_str += "    Upper Layer:\n"
        for r in range(32):
            return_str += "    "
            row = self.upper_layer[(r*32):(r*32+32)]
            for v in row:
                return_str += " {0:3d}".format(v)
            return_str += "\n"
        return_str += "    Lower Layer:\n"
        for r in range(32):
            return_str += "    "
            row = self.lower_layer[(r*32):(r*32+32)]
            for v in row:
                return_str += " {0:3d}".format(v)
            return_str += "\n"
        return return_str

    def add_field(self, field):
        self.optional_fields.append(field)


class CCLevelPack:
    """A class defining the data of a pack of cc levels
    Member vars:
        levels (list of CCLevels): the levels of this level pack
    """

    def __init__(self):
        self.levels = []

    def __str__(self):
        return_str = ""
        return_str += "Level Pack:\n"
        for level in self.levels:
            return_str += str(level)

        return return_str

    @property
    def level_count(self):
        return len(self.levels)

    def add_level(self, level):
        self.levels.append(level)

