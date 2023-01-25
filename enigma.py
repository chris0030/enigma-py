from enum import Enum
import string
from wiring import *

ALPHABET = list(string.ascii_uppercase)

def position_in_list(letter, letter_list):
    # Returns index integer of letter in list
    return letter_list.index(letter)

def alphabet_position(letter):
    # Returns index integer of letter in alphabet
    return position_in_list(letter, ALPHABET)

class RotorType(Enum):
    REGULAR = 1 
    REFLECTOR = 2
    ENTRY_DISC = 3

class Enigma:
    def __init__(self, rotors):
        self.rotors = rotors

    def display_rotor(self):
        rotor_string = ""
        for rotor in self.rotors:
            rotor_string += f"{ALPHABET[rotor.position]}"
        return rotor_string

    def reset(self):
        print("Resetting Enigma")
        for rotor in self.rotors:
            rotor.position = 0

    def process_rotation(self):
        first = True
        for rotor in reversed(self.rotors):
            if first:
                rotor.rotate()
                first = False
            if rotor.on_notch():
                previous_rotor_index = self.rotors.index(rotor)
                self.rotors[previous_rotor_index].rotate()

    def encode(self, letter):
        self.process_rotation()
        for rotor in reversed(self.rotors):
            letter = rotor.encode_letter(letter)
        for rotor in self.rotors[1:]:
            letter = rotor.decode_letter(letter)
        return letter


class Rotor:
    def __init__(self, rotor_type, letter_list, notch_list, ring_setting):
        self.rotor_type = rotor_type
        self.letter_list = letter_list
        self.position = 0
        self.notch_list = notch_list
        self.ring_setting = ring_setting

    def on_notch(self):
        if string.ascii_uppercase[self.position] in self.notch_list:
            return True

    def rotate(self):
        if self.position == 25:
            self.position = 0
        else:
            self.position += 1

    def encode_letter(self, letter):
        letter_number = alphabet_position(letter)  # A=0 B=1 ... Z=25
        letter_number += self.position + self.ring_setting - 1
        letter_number = letter_number % 26
        new_letter = self.letter_list[letter_number]
        return new_letter

    def decode_letter(self, letter):
        letter_number = position_in_list(letter, self.letter_list)
        letter_number -= self.position
        letter_number = letter_number % 26
        new_letter = list(string.ascii_uppercase)[letter_number]
        return new_letter

if __name__ == "__main__":
    reflector = Rotor(
        RotorType.REFLECTOR,
        ROTORS['ROTOR_UKW_C']['letters'],
        [],
        1
    )
    rotor_1 = Rotor(
        RotorType.REGULAR,
        ROTORS['ROTOR_I']['letters'],
        ROTORS['ROTOR_I']['notch'],
        1
    )
    rotor_2 = Rotor(
        RotorType.REGULAR,
        ROTORS['ROTOR_II']['letters'],
        ROTORS['ROTOR_II']['notch'],
        1
    )
    rotor_3 = Rotor(
        RotorType.REGULAR,
        ROTORS['ROTOR_III']['letters'],
        ROTORS['ROTOR_III']['notch'],
        1
    )
    enigma = Enigma([reflector, rotor_1, rotor_2, rotor_3])
    result = ""
    for letter in list("CHRIS".replace(" ", "X").upper()):
        print(enigma.display_rotor())
        result += enigma.encode(letter)
    print(result)
    enigma.reset()
    result = ""
    for letter in list("FZCWD"):
        print(enigma.display_rotor())
        result += enigma.encode(letter)
    print(result)
