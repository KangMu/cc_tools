import cc_dat_utils
import cc_data
import sys
import json

def make_cc_data_from_json(json_data):
    cc_data_object = cc_data.CCDataFile()
    for json_level in json_data:
        cc_level = cc_data.CCLevel()
        cc_level.time = json_level["time"]
        cc_level.level_number = json_level["level_number"]
        cc_level.num_chips = json_level["chip_number"]
        cc_level.upper_layer = json_level["upper_layer"]
        cc_level.lower_layer = json_level["lower_layer"]

        for json_field in json_level["optional_fields"]:
            if json_field["type"] == 3:
                field_title = json_field["title"]
                cc_field = cc_data.CCMapTitleField(field_title)
            elif json_field["type"] == 4:
                json_traps = json_field["traps"]
                cc_traps = []
                cc_buttons = []
                for json_trap in json_traps:
                    bx = json_trap[0]
                    by = json_trap[1]
                    tx = json_trap[2]
                    ty = json_trap[3]
                    button_coord = cc_data.CCCoordinate(bx, by)
                    trap_coord = cc_data.CCCoordinate(tx, ty)
                    cc_buttons.append(button_coord)
                    cc_traps.append(trap_coord)
                cc_field = cc_data.CCTrapControlsField(cc_traps, cc_buttons)
            elif json_field["type"] == 5:
                json_machines = json_field["machines"]
                cc_buttons = []
                cc_machines = []
                for json_machine in json_machines:
                    bx = json_machine[0]
                    by = json_machine[1]
                    tx = json_machine[2]
                    ty = json_machine[3]
                    button_coord = cc_data.CCCoordinate(bx, by)
                    machine_coord = cc_data.CCCoordinate(tx, ty)
                    cc_buttons.append(button_coord)
                    cc_machines.append(machine_coord)
                cc_field = cc_data.CCCloningMachineControlsField(cc_buttons, cc_machines)
            elif json_field["type"] == 6:
                json_password = json_field["password"]
                cc_passwords = []
                for json_password in json_password:
                    w = json_password[0]
                    x = json_password[1]
                    y = json_password[2]
                    z = json_password[3]
                cc_field = cc_data.CCEncodedPasswordField(w, x, y, z)
            elif json_field["type"] == 7:
                field_hint = json_field["hint"]
                cc_field = cc_data.CCMapHintField(field_hint)
            elif json_field["type"] == 10:
                json_monsters = json_field["monsters"]
                cc_monsters = []
                for json_monster in json_monsters:
                    x = json_monster[0]
                    y = json_monster[1]
                    monster_coord = cc_data.CCCoordinate(x,y)
                    cc_monsters.append(monster_coord)
                cc_field = cc_data.CCMonsterMovementField(cc_monsters)
            cc_level.add_field(cc_field)
        cc_data_object.add_level(cc_level)
    return cc_data_object

# Handling command line arguments
#  Note: sys.argv is a list of strings that contains each command line argument
#        The first element in the list is always the name of the python file being run
# Command line format: <input json filename> <output dat filename>

default_input_json_file = "data/json_data.json"
default_output_dat_file = "data/example_dat.dat"

if len(sys.argv) == 3:
    input_json_file = sys.argv[1]
    output_dat_file = sys.argv[2]
    print("Using command line args:", input_json_file, output_dat_file)
else:
    input_json_file = default_input_json_file
    output_dat_file = default_output_dat_file
    print("Unknown command line options. Using default values:", input_json_file, output_dat_file)

# Reading the JSON data in from the input file
json_reader = open(input_json_file, "r")
json_data = json.load(json_reader)
json_reader.close() #Close the file now that we're done using it

make_cc_data_from_json(json_data)