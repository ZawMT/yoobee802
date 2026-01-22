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
    def __init__(self, form = None, param1 = None, param2 = None, tag = ""):
         #To keep the user input as exactly as given by the user
        self.user_input = ""
        self.tag = tag   
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
    
    @property
    def is_zero(self):
        if self.real == 0 and self.imaginary == 0:
            return True
        return False
    
    @property
    def is_invalid(self):
        if self.input_form == ComplexNumberForm.Invalid:
            return True
        return False
    
    @property
    def tag_info(self):
        if self.tag is not None and len(self.tag) > 0:
            return self.tag
        return ""

    def get_input(self, label):
        if label is None or len(label) == 0:
            label = "Give a complex number in Cartesian form (E.g. a + bi) or phasor form (magnitude, angle): " 
        #To cover all the possible Cartesian inputs: E.g. 1 + 2i; 2i + 1; 1; 2i; 0;
        expected_pattern_cartesian = r'^([+-]?\d*)([+-]\d*i)?$|^([+-]?\d*i)([+-]\d*)?$|^0$' 
        expected_pattern_phasor = r'^\s*\(?\s*([+-]?(?:\d+\.?\d*|\.\d+))\s*,\s*([+-]?(?:\d+\.?\d*|\.\d+))\s*\)?\s*$'
        self.user_input = input(label)
        str_input = self.user_input.replace(" ", "") #Trimmig all spaces to simplify the processing
        if len(str_input) == 0:
            str_input = "0"
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
        
        if len(self.tag) > 0:
            return self.tag
        
        return "Invalid Complex Number"
    

    def cartesian_form_compact(self):
            width_to_use = 16
            if self.input_form != ComplexNumberForm.Invalid:
                if self.real != 0 and self.imaginary != 0:
                    return f"{self.__number_minimal(self.real)} {self.__imaginary_number_minimal(self.imaginary)}i".ljust(width_to_use)
                elif self.real != 0:
                    return f"{self.__number_minimal(self.real)}".ljust(width_to_use)
                elif self.imaginary != 0:
                    return f"{self.__imaginary_number_minimal(self.imaginary, True)}i".ljust(width_to_use)
                else:
                    return "0".ljust(width_to_use)
                
            if len(self.tag) > 0:
                return self.tag.ljust(width_to_use)
            
            return "Invalid Number".ljust(width_to_use)


    def phasor_form(self):
        if self.input_form != ComplexNumberForm.Invalid:
            return f"({self.__number_minimal(self.magnitude)}, {self.__number_minimal(self.angle)})"
        
        if len(self.tag) > 0:
            return self.tag
        
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
    

    def __imaginary_number_minimal(self, n, strip_sign_if_positive = False):
        if n >= 0:
            if strip_sign_if_positive:
                return f"{n:.2f}".rstrip('0').rstrip('.')
            
            return f"+ {n:.2f}".rstrip('0').rstrip('.')
        
        n = abs(n)
        return f"- {n:.2f}".rstrip('0').rstrip('.')
    
class ComplexNumberOperator:
    @staticmethod
    def add(c1: ComplexNumber, c2: ComplexNumber) -> ComplexNumber:
        if c1.input_form != ComplexNumberForm.Invalid and c2.input_form != ComplexNumberForm.Invalid:
            return ComplexNumber(ComplexNumberForm.Cartesian, c1.real + c2.real, c1.imaginary + c2.imaginary)
        
        return None
    

    @staticmethod
    def subtract(c1: ComplexNumber, c2: ComplexNumber) -> ComplexNumber:
        if c1.input_form != ComplexNumberForm.Invalid and c2.input_form != ComplexNumberForm.Invalid:
                    return ComplexNumber(ComplexNumberForm.Cartesian, c1.real - c2.real, c1.imaginary - c2.imaginary)
        
        return None
    
    
    @staticmethod
    def multiply(c1: ComplexNumber, c2: ComplexNumber) -> ComplexNumber:
        if c1.input_form != ComplexNumberForm.Invalid and c2.input_form != ComplexNumberForm.Invalid:
            return ComplexNumber(ComplexNumberForm.Cartesian, c1.real * c2.real - c1.imaginary * c2.imaginary, c1.real * c2.imaginary + c1.imaginary * c2.real)
        
        return None
    

    @staticmethod
    def divide(c1: ComplexNumber, c2: ComplexNumber) -> ComplexNumber:
        if c1.input_form != ComplexNumberForm.Invalid and c2.input_form != ComplexNumberForm.Invalid:
            denominator = c2.real**2 + c2.imaginary**2
            if denominator == 0:
                return None
            
            return ComplexNumber(ComplexNumberForm.Cartesian, (c1.real * c2.real + c1.imaginary * c2.imaginary) / denominator, (c1.imaginary * c2.real - c1.real * c2.imaginary) / denominator)
        
        return None
    

    @staticmethod
    def conjugate(c: ComplexNumber) -> ComplexNumber:
        if c.input_form != ComplexNumberForm.Invalid:
            return ComplexNumber(ComplexNumberForm.Cartesian, c.real, -1 * c.imaginary)
        
        
    @staticmethod
    def negate(c: ComplexNumber) -> ComplexNumber:
        if c.input_form != ComplexNumberForm.Invalid:
            return ComplexNumber(ComplexNumberForm.Cartesian, -1 * c.real, -1 * c.imaginary)