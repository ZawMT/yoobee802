'''
Complex number operator
Author: Zaw Min Tun
Description:
    This program will operate two complex numbers to get addition, substraction, multiplication and division.
    This program will also give the conjugates of the input complex number(s)
'''
import math #For calculations
import re #To use regular expression to evaluate and hanlde user input data

from enum import Enum #To use types of complex number forms

class ComplexNumberForm(Enum):
    Invalid = -1
    Cartesian = 0
    Phasor = 1


#Class to get input, operate and show the results
class ComplexNumber:
    def __init__(self, form = None, param1 = None, param2 = None):
         #To keep the user input as exactly as given by the user
        self.user_input = ""
            
        if form != None and form != ComplexNumberForm.Invalid and param1 != None and param2 != None:
            self.input_form = form
            if form == ComplexNumberForm.Cartesian:
                self.real = param1
                self.imaginary = param2
            elif form == ComplexNumberForm.Phasor:
                self.magnitude = param1
                self.angle = param2

            self.__populate_properties()
        else:
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
        
        self.__populate_properties()


    def cartesian_form(self):
        if self.input_form != ComplexNumberForm.Invalid:
            return f"{self.__number_minimal(self.real)} {self.__imaginary_number_minimal(self.imaginary)}i"
        
        return "Invalid Complex Number"


    def phasor_form(self):
        if self.input_form != ComplexNumberForm.Invalid:
            return f"({self.__number_minimal(self.magnitude)}, {self.__number_minimal(self.angle)})"
        
        return "Invalid Complex Number"


    def __populate_properties(self):
        #Only real and imaginary are populated, others need to be calculated
        if self.input_form == ComplexNumberForm.Cartesian: 
            self.magnitude = math.sqrt(self.real**2 + self.imaginary**2)
            self.angle = math.degrees(math.atan2(self.imaginary, self.real))
        #Only real and imaginary are populated, others need to be calculated
        elif self.input_form == ComplexNumberForm.Phasor:
            radians = math.radians(self.angle)
            self.real = math.cos(radians) * self.magnitude
            self.imaginary = math.sin(radians) * self.magnitude

    def __number_minimal(self, n):
        return f"{n:.2f}".rstrip('0').rstrip('.')
    
    def __imaginary_number_minimal(self, n):
        if n >= 0:
            return f"+ {n:.2f}".rstrip('0').rstrip('.')
        
        n = abs(n)
        return f"- {n:.2f}".rstrip('0').rstrip('.')
    

class ComplexNumberOperator:
    @staticmethod
    def add(c1: ComplexNumber, c2: ComplexNumber) -> ComplexNumber:
        if c1.input_form != ComplexNumberForm.Invalid and c2.input_form != ComplexNumberForm.Invalid:
            return ComplexNumber(ComplexNumberForm.Cartesian, c1.real + c2.real, c1.imaginary + c2.imaginary)
        
        return None
        
    def substract(c1: ComplexNumber, c2: ComplexNumber) -> ComplexNumber:
        if c1.input_form != ComplexNumberForm.Invalid and c2.input_form != ComplexNumberForm.Invalid:
                    return ComplexNumber(ComplexNumberForm.Cartesian, c1.real - c2.real, c1.imaginary - c2.imaginary)
        
        return None
    
    
    def multiply(c1: ComplexNumber, c2: ComplexNumber) -> ComplexNumber:
        if c1.input_form != ComplexNumberForm.Invalid and c2.input_form != ComplexNumberForm.Invalid:
            return ComplexNumber(ComplexNumberForm.Cartesian, c1.real * c2.real - c1.imaginary * c2.imaginary, c1.real * c2.imaginary + c1.imaginary * c2.real)
        
        return None
    
    def divide(c1: ComplexNumber, c2: ComplexNumber) -> ComplexNumber:
        if c1.input_form != ComplexNumberForm.Invalid and c2.input_form != ComplexNumberForm.Invalid:
            denominator = c2.real**2 + c2.imaginary**2
            if denominator == 0:
                return None
            
            return ComplexNumber(ComplexNumberForm.Cartesian, (c1.real * c2.real + c1.imaginary * c2.imaginary) / denominator, (c1.imaginary * c2.real - c1.real * c2.imaginary) / denominator)
        
        return None
    
    def conjugate(c: ComplexNumber) -> ComplexNumber:
        if c.input_form != ComplexNumberForm.Invalid:
            return ComplexNumber(ComplexNumberForm.Cartesian, c.real, -1 * c.imaginary)
        
def main():
    #Initialize the complex numbers
    complex_num1 = ComplexNumber() 
    complex_num2 = ComplexNumber() 

    #Get the input
    complex_num1.get_input() 
    complex_num2.get_input()

    #Initialize the results
    complex_add = None
    complex_substract = None
    complex_multiplication = None
    complex_division = None
    complex_conjugate1 = None
    complex_conjugate2 = None
    
    if complex_num1.input_form != ComplexNumberForm.Invalid and complex_num2.input_form != ComplexNumberForm.Invalid:
        complex_add = ComplexNumberOperator.add(complex_num1, complex_num2)
        complex_substract = ComplexNumberOperator.substract(complex_num1, complex_num2)
        complex_multiplication = ComplexNumberOperator.multiply(complex_num1, complex_num2)
        complex_division = ComplexNumberOperator.divide(complex_num1, complex_num2)
    
    if complex_num1 != ComplexNumberForm.Invalid:
        complex_conjugate1 = ComplexNumberOperator.conjugate(complex_num1)

    if complex_num2 != ComplexNumberForm.Invalid:
        complex_conjugate2 = ComplexNumberOperator.conjugate(complex_num2) 

    print(f"Operation results for two given complex numbers: {complex_num1.user_input} and {complex_num2.user_input}")
    print(f"Conjugates: {complex_conjugate1.cartesian_form()} and {complex_conjugate2.cartesian_form()}") 
    print(f"Addition: {complex_add.cartesian_form()}") 
    print(f"Substraction: {complex_substract.cartesian_form()}")     
    print(f"Multiplication: {complex_multiplication.cartesian_form()}")     
    print(f"Division: {complex_division.cartesian_form()}")     

if __name__ == "__main__":
    main()