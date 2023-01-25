from enum import Enum
import string
from wiring import *

def position_in_list(letter, letter_list):
    return letter_list.index(letter)

def alphabet_position(letter):
    letter_list = list(string.ascii_uppercase)
    return position_in_list(letter, letter_list)

class RotorType(Enum):
    REGULAR = 1 
    REFLECTOR = 2
    ENTRY_DISC = 3

class Enigma:
    def __init__(self, rotor_3, reflector, entry_disc=None, rotor_2=None, rotor_1=None, disable_rotate=False):
        self.entry_disc = entry_disc
        self.rotor_1 = rotor_1
        self.rotor_2 = rotor_2
        self.rotor_3 = rotor_3
        self.reflector = reflector
        self.disable_rotate = disable_rotate

    def display_rotor(self):
        rotors = ""
        rotors += f"{string.ascii_uppercase[self.reflector.position]}"
        if self.rotor_1:
            rotors += f"{string.ascii_uppercase[self.rotor_1.position]}"
        if self.rotor_2:
            rotors += f"{string.ascii_uppercase[self.rotor_2.position]}"
        rotors += f"{string.ascii_uppercase[self.rotor_3.position]}"
        return rotors

    def reset(self):
        print("Resetting Enigma")
        self.rotor_3.position = 0
        if self.rotor_2:
            self.rotor_2.position = 0
        if self.rotor_1:
            self.rotor_1.position = 0

    def encode(self, letter):
        self.rotor_3.rotate()
        if self.rotor_3.on_notch():
            self.rotor_2.rotate()
            if self.rotor_2.on_notch():
                self.rotor_1.rotate()
        letter = self.rotor_3.encode_letter(letter)
        if self.rotor_2:
           letter = self.rotor_2.encode_letter(letter)
        if self.rotor_1:
            letter = self.rotor_1.encode_letter(letter)
        letter = self.reflector.encode_letter(letter)
        if self.rotor_1:
            letter = self.rotor_1.decode_letter(letter)
        if self.rotor_2:
            letter = self.rotor_2.decode_letter(letter)
        letter = self.rotor_3.decode_letter(letter)
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
        return self.letter_list[letter_number]

    def decode_letter(self, letter):
        letter_number = position_in_list(letter, self.letter_list)
        letter_number -= self.position
        letter_number = letter_number % 26
        new_letter = list(string.ascii_uppercase)[letter_number]
        return new_letter

if __name__ == "__main__":
    rotor_1_letters = list(ROTOR_I['letters'])
    rotor_1_notches = list(ROTOR_I['notch'])
    reflector_letters = list(ROTOR_UKW_B['letters'])
    rotor_2_letters = list(ROTOR_II['letters'])
    rotor_2_notches = list(ROTOR_II['notch'])
    rotor_3_letters = list(ROTOR_III['letters'])
    rotor_3_notches = list(ROTOR_III['notch'])
    reflector = Rotor(RotorType.REFLECTOR, reflector_letters, [], 1)
    rotor_1 = Rotor(RotorType.REGULAR, rotor_1_letters, rotor_1_notches, 1)
    rotor_2 = Rotor(RotorType.REGULAR, rotor_2_letters, rotor_2_notches, 1)
    rotor_3 = Rotor(RotorType.REGULAR, rotor_3_letters, rotor_3_notches, 1)
    enigma = Enigma(rotor_1, reflector, rotor_2, rotor_3)
    result = ""
    for letter in list("CHRIS".replace(" ", "X").upper()):
        print(enigma.display_rotor())
        result += enigma.encode(letter)
    print(result)
    enigma.reset()
    result = ""
    for letter in list("RGSHZ"):
        print(enigma.display_rotor())
        result += enigma.encode(letter)
    print(result)
