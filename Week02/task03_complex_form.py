'''
Complex number operator
Author: Zaw Min Tun
Description:
    This program will switch the phasor form to Cartesian form, and vice versa
'''
import math #For calculations
import re #To use regular expression to evaluate and hanlde user input data

from enum import Enum #To use types of complex number forms

class ComplexNumberForm(Enum):
    Invalid = -1
    Cartesian = 0
    Phasor = 1


class NumberFormatter():
    @staticmethod
    def format_number_minimal(n):
        return f"{n:.2f}".rstrip('0').rstrip('.')
    

#Class to get input, operate and show the results
class ComplexNumber:
    def __init__(self):
        #Initialize form as Invalid at first
        self.input_form = ComplexNumberForm.Invalid

        #Initialize all properties of a complex number as None first
        self.real = None
        self.imaginary = None
        self.angle = None
        self.magnitude = None

        #Initialize all forms as None
        self.cartesian = None
        self.phasor = None
        
        #To keep the user input as exactly as given by the user
        self.user_input = ""

    
    def get_input(self):
        #To cover all the possible Cartesian inputs: E.g. 1 + 2i; 2i + 1; 1; 2i; 0;
        expected_pattern_cartesian = r'^([+-]?\d*)([+-]\d*i)?$|^([+-]?\d*i)([+-]\d*)?$|^0$' 
        expected_pattern_phasor = r'^\s*\(?\s*([+-]?(?:\d+\.?\d*|\.\d+))\s*,\s*([+-]?(?:\d+\.?\d*|\.\d+))\s*\)?\s*$'
        self.user_input = input("Give a complex number in Cartesian form (E.g. a + bi) or phasor form (magnitude, angle): ")
        str_input = self.user_input.replace(" ", "") #Trimmig all spaces to simplify the processing
        re_match = re.fullmatch(expected_pattern_cartesian, str_input)
        if re_match:
            groups = re_match.groups()
            self.real, self.imaginary = 0, 0
            if groups[0] or groups[1]: #Format: a+bi or a-bi or a
                self.input_form = ComplexNumberForm.Cartesian
                real_part = groups[0] or '0'
                imaginary_part = groups[1] or '0i'
                self.real = int(real_part) if real_part else 0
                self.imaginary = int(imaginary_part.replace('i', '')) if imaginary_part else 0
            elif groups[2] or groups[3]: #Format: bi+a or bi-a or bi
                self.input_form = ComplexNumberForm.Cartesian
                imaginary_part = groups[2] or '0i'
                real_part = groups[3] or '0'
                self.real = int(real_part) if real_part else 0
                self.imaginary = int(imaginary_part.replace('i', '')) if imaginary_part else 0
        
        #Still need to check if the input is in phasor format
        if self.input_form == ComplexNumberForm.Invalid: 
            re_match = re.fullmatch(expected_pattern_phasor, str_input)
            if re_match:
                groups = re_match.groups()
                if len(groups) == 2:
                    self.input_form = ComplexNumberForm.Phasor
                    self.magnitude = float(groups[0])
                    self.angle = float(groups[1])

        #Then only real and imaginary are populated, others need to be calculated
        if self.input_form == ComplexNumberForm.Cartesian: 
            self.magnitude = math.sqrt(self.real**2 + self.imaginary**2)
            self.angle = math.degrees(math.atan2(self.imaginary, self.real))
        elif self.input_form == ComplexNumberForm.Phasor:
            radians = math.radians(self.angle)
            self.real = math.cos(radians) * self.magnitude
            self.imaginary = math.sin(radians) * self.magnitude


    def cartesian_form(self):
        if self.input_form != ComplexNumberForm.Invalid:
            return f"{NumberFormatter.format_number_minimal(self.real)} + {NumberFormatter.format_number_minimal(self.imaginary)}i"
        
        return "Invalid input form"


    def phasor_form(self):
        if self.input_form != ComplexNumberForm.Invalid:
            return f"({NumberFormatter.format_number_minimal(self.magnitude)}, {NumberFormatter.format_number_minimal(self.angle)})"
        
        return "Invalid input form"


def main():
    #Initialize the complex number and get the input
    complex_num = ComplexNumber() 
    complex_num.get_input() 

    if complex_num.input_form == ComplexNumberForm.Cartesian:
        print(f"Phasor form: {complex_num.phasor_form()}")
    elif complex_num.input_form == ComplexNumberForm.Phasor:
        print(f"Cartesian form: {complex_num.cartesian_form()}")

if __name__ == "__main__":
    main()