"""
Methods for encoding and decoding Chip's Challenge (CC) data to and from binary DAT files
Created for the class Programming for Game Designers
"""
import cc_data

CC_DAT_HEADER_CODE = b'\xAC\xAA\x02\x00'
RLE_CODE_INT = 255

READ_ADDRESS = 0

def do_read(reader, byte_count):
    """Utility read function to enable address tracking and other debugging when reading binary files
    Currently keeps track of the current byte address in the file in the global variable TEMP_ADDRESS
    Args:
        reader (BufferedReader) : reader to read from
        byte_count (int) : number of bytes to read
    """
    global READ_ADDRESS
    to_return = reader.read(byte_count)
    # print("x"+format(TEMP_ADDRESS, '02x')+": "+str(to_return)+" ("+str(int.from_bytes(to_return, cc_data.BYTE_ORDER))+")")
    READ_ADDRESS += byte_count
    return to_return


def get_string_from_bytes(byte_data, encoding="ascii"):
    """Decodes a string from DAT file byte data.
    Note that in byte form these strings are 0 terminated and this 0 is removed
    Args:
        byte_data (bytes) : the binary data to convert to a string
        encoding (string) : optional, the encoding type to use when converting
    """
    string_bytes = byte_data[0:(len(byte_data) - 1)]  # strip off the 0 at the end of the string
    string = string_bytes.decode(encoding)
    return string


def make_field_from_bytes(field_type, field_bytes):
    """Constructs and returns the appropriate cc field
    Args:
        field_type (int) : what type of field to construct
        field_bytes (bytes) : the binary data to be used to create the field
    """
    if field_type == cc_data.CCMapTitleField.TYPE:
        return cc_data.CCMapTitleField(get_string_from_bytes(field_bytes))
    elif field_type == cc_data.CCTrapControlsField.TYPE:
        trap_count = int(len(field_bytes) / 10)
        traps = []
        for t_index in range(trap_count):
            i = t_index * 10
            bx = int.from_bytes(field_bytes[i:(i + 2)], byteorder=cc_data.BYTE_ORDER)
            by = int.from_bytes(field_bytes[i + 2:(i + 4)], byteorder=cc_data.BYTE_ORDER)
            tx = int.from_bytes(field_bytes[i + 4:(i + 6)], byteorder=cc_data.BYTE_ORDER)
            ty = int.from_bytes(field_bytes[i + 6:(i + 8)], byteorder=cc_data.BYTE_ORDER)
            traps.append(cc_data.CCTrapControl(bx, by, tx, ty))
        return cc_data.CCTrapControlsField(traps)
    elif field_type == cc_data.CCCloningMachineControlsField.TYPE:
        machine_count = int(len(field_bytes) / 8)
        machines = []
        for m_index in range(machine_count):
            i = m_index * 8
            bx = int.from_bytes(field_bytes[i:(i + 2)], byteorder=cc_data.BYTE_ORDER)
            by = int.from_bytes(field_bytes[i + 2:(i + 4)], byteorder=cc_data.BYTE_ORDER)
            tx = int.from_bytes(field_bytes[i + 4:(i + 6)], byteorder=cc_data.BYTE_ORDER)
            ty = int.from_bytes(field_bytes[i + 6:(i + 8)], byteorder=cc_data.BYTE_ORDER)
            machines.append(cc_data.CCCloningMachineControl(bx, by, tx, ty))
        return cc_data.CCCloningMachineControlsField(machines)
    elif field_type == cc_data.CCEncodedPasswordField.TYPE:
        # passwords are encoded as a list of ints
        password = []
        # A bytes object behaves as a list of integers
        # password data is terminated with a zero, iterate to one short of the end of the array
        for b in field_bytes[0:(len(field_bytes)-1)]:
            password.append(b)
        return cc_data.CCEncodedPasswordField(password)
    elif field_type == cc_data.CCMapHintField.TYPE:
        return cc_data.CCMapHintField(get_string_from_bytes(field_bytes))
    elif field_type == cc_data.CCPasswordField.TYPE:
        return cc_data.CCPasswordField(get_string_from_bytes(field_bytes))
    elif field_type == cc_data.CCMonsterMovementField.TYPE:
        monster_count = int(len(field_bytes) / 2)
        monsters = []
        for m_index in range(monster_count):
            i = m_index * 2
            x = int.from_bytes(field_bytes[i:(i + 1)], byteorder=cc_data.BYTE_ORDER)
            y = int.from_bytes(field_bytes[i + 1:(i + 2)], byteorder=cc_data.BYTE_ORDER)
            monsters.append(cc_data.CCCoordinate(x, y))
        return cc_data.CCMonsterMovementField(monsters)
    else:
        if __debug__:
            raise AssertionError("Unsupported field type: " + str(field_type))
        return cc_data.CCField(field_type, field_bytes)


def make_optional_fields_from_dat(reader):
    """Reads all the optional fields in from the active reader
    Note that this assumes the reader is at the optional fields section in the file.
    This code does not error check for invalid data
    Args:
        reader (BufferedReader) : active reader reading a DAT file
    Returns:
        A list of all the constructed optional fields
    """
    fields = []
    total_optional_field_bytes = int.from_bytes(do_read(reader, 2), byteorder=cc_data.BYTE_ORDER)
    while total_optional_field_bytes > 0:
        field_type = int.from_bytes(do_read(reader, 1), byteorder=cc_data.BYTE_ORDER)
        byte_count = int.from_bytes(do_read(reader, 1), byteorder=cc_data.BYTE_ORDER)
        byte_vals = do_read(reader, byte_count)
        fields.append(make_field_from_bytes(field_type, byte_vals))
        total_optional_field_bytes -= (byte_count + 2)
    return fields


def make_layer_from_bytes(layer_bytes):
    """Constructs layer data (a 1024 list of ints) from the given layer_bytes data
    Note: DAT files employ Run Length Encoding which this function is designed to decode
    Args:
        layer_bytes (bytes) : The binary data of a layer read in from the DAT file
    Returns:
        A list of ints initialized with the layer data
    """
    layer_data = []
    index = 0
    while index < len(layer_bytes):
        val = layer_bytes[index]
        index += 1
        # Check for the Run Length Encoding value
        if val == RLE_CODE_INT:
            # If using RLE, the next byte is the number of copies to make
            # and the 2nd byte is the value to repeat
            copies = layer_bytes[index]
            code = layer_bytes[index + 1]
            index += 2
            for i in range(copies):
                layer_data.append(code)
        else:
            layer_data.append(val)
    return layer_data


def make_level_from_dat(reader):
    """Reads all the data to construct a single level from the active reader
    Note that this assumes the reader is at new level section in the file.
    This code does not error check for invalid data
    Args:
        reader (BufferedReader) : active reader reading a DAT file
    Returns:
        A CCLevel object constructed with the read data
    """
    level = cc_data.CCLevel()
    level.num_bytes = int.from_bytes(do_read(reader, 2), byteorder=cc_data.BYTE_ORDER)
    level.level_number = int.from_bytes(do_read(reader, 2), byteorder=cc_data.BYTE_ORDER)
    level.time = int.from_bytes(do_read(reader, 2), byteorder=cc_data.BYTE_ORDER)
    level.num_chips = int.from_bytes(do_read(reader, 2), byteorder=cc_data.BYTE_ORDER)
    # Note: Map Detail is not used and is expected to always be 1
    map_detail = int.from_bytes(do_read(reader, 2), byteorder=cc_data.BYTE_ORDER)
    upper_layer_byte_count = int.from_bytes(do_read(reader, 2), byteorder=cc_data.BYTE_ORDER)
    upper_layer_bytes = do_read(reader, upper_layer_byte_count)
    lower_layer_byte_count = int.from_bytes(do_read(reader, 2), byteorder=cc_data.BYTE_ORDER)
    lower_layer_bytes = do_read(reader, lower_layer_byte_count)
    level.upper_layer = make_layer_from_bytes(upper_layer_bytes)
    level.lower_layer = make_layer_from_bytes(lower_layer_bytes)
    level.optional_fields = make_optional_fields_from_dat(reader)
    return level


def make_cc_data_from_dat(dat_file):
    """Reads a DAT file and constructs a CCDataFile object out of it
    This code assumes a valid DAT file and does not error check for invalid data
    Args:
        dat_file (string) : the filename of the DAT file to read in
    Returns:
        A CCDataFile object constructed with the data from the given file
    """
    data = cc_data.CCDataFile()
    with open(dat_file, 'rb') as reader:
        header_bytes = do_read(reader, 4)
        if header_bytes != CC_DAT_HEADER_CODE:
            print("ERROR: Invalid header found. Expected " + str(CC_DAT_HEADER_CODE) + ", but found " + header_bytes)
            return
        num_levels = int.from_bytes(do_read(reader, 2), byteorder=cc_data.BYTE_ORDER)
        for i in range(num_levels):
            level = make_level_from_dat(reader)
            data.levels.append(level)
    return data


def calculate_option_field_byte_size(field):
    """Returns the size of a given field if converted to binary form
    Note: The total byte count of field entry is the type (1 byte) + size (1 byte) and size of the data in byte form
    Args:
        field (CCField)
    """
    byte_data = field.byte_data
    return len(byte_data) + 2


def calculate_total_optional_field_byte_size(optional_fields):
    """Returns the total size of all the given optional fields if converted to binary form
    Note: The total byte count of field entry is the type (1 byte) + size (1 byte) and size of the data in byte form
    Args:
        optional_fields (list of CCFields)
    """
    optional_fields_size = 0
    for field in optional_fields:
        optional_fields_size += calculate_option_field_byte_size(field)
    return optional_fields_size


def calculate_level_byte_size(level):
    """Returns the total size of the given level if converted to binary form
    The total byte count of level entry is:
    size (2) + level number (2) + time (2) + chip count (2) +
    map detail (2) + layer1 size (2) + number of bytes in layer1 + layer2 size (2) + number of bytes in layer2 +
    size of optional fields
    Args:
        level (CCLevel)
    """
    optional_fields_size = calculate_total_optional_field_byte_size(level.optional_fields)
    upper_layer_size = len(level.upper_layer)
    lower_layer_size = len(level.lower_layer)
    return 14 + upper_layer_size + lower_layer_size + optional_fields_size


def write_field_to_dat(field, writer):
    """Writes the given field in binary form to the given writer
    Args:
        field (CCField): the field to write
        writer (BufferedWriter): the active writer in binary write mode
    """
    byte_data = field.byte_data
    writer.write(field.type_val.to_bytes(1, cc_data.BYTE_ORDER))
    writer.write(len(byte_data).to_bytes(1, cc_data.BYTE_ORDER))
    writer.write(byte_data)


def write_layer_to_dat(layer, writer):
    """Writes the given layer in binary form to the given writer
    Note: while the DAT file format supports run length encoding, this function does not implement it
    Args:
        layer (list of ints): the layer to write
        writer (BufferedWriter): the active writer in binary write mode
    """
    byte_size = len(layer)
    writer.write(byte_size.to_bytes(2, cc_data.BYTE_ORDER))
    for val in layer:
        if type(val) is int:
            byte_val = val.to_bytes(1, cc_data.BYTE_ORDER)
        else:
            byte_val = val
        writer.write(byte_val)


def write_level_to_dat(level, writer):
    """Writes the given level in binary form to the given writer
    Args:
        level (CCLevel): the level to write
        writer (BufferedWriter): the active writer in binary write mode
    """
    level_bytes = calculate_level_byte_size(level)
    writer.write(level_bytes.to_bytes(2, cc_data.BYTE_ORDER))
    writer.write(level.level_number.to_bytes(2, cc_data.BYTE_ORDER))
    writer.write(level.time.to_bytes(2, cc_data.BYTE_ORDER))
    writer.write(level.num_chips.to_bytes(2, cc_data.BYTE_ORDER))
    writer.write(b'\x01\x00')  # Write the "map detail" which is always a 2 byte number set to 1
    write_layer_to_dat(level.upper_layer, writer)
    write_layer_to_dat(level.lower_layer, writer)
    total_field_byte_size = calculate_total_optional_field_byte_size(level.optional_fields)
    writer.write(total_field_byte_size.to_bytes(2, cc_data.BYTE_ORDER))
    for field in level.optional_fields:
        write_field_to_dat(field, writer)


def write_cc_data_to_dat(cc_dat, dat_file):
    """Writes the given CC dat in binary form to the file
    Args:
        cc_dat (CCData): the cc data to write
        dat_file (string): the filename of the output file
    """
    with open(dat_file, 'wb') as writer: # Note: DAT files are opened in binary mode
        # Basic DAT file format is: DAT header, total number of levels, level 1, level 2, etc.
        writer.write(CC_DAT_HEADER_CODE)
        writer.write(cc_dat.level_count.to_bytes(2, cc_data.BYTE_ORDER))
        for level in cc_dat.levels:
            write_level_to_dat(level, writer)
