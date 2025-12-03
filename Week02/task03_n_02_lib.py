import cmath
import math

try:
    complex_str1 = input("Type in one complex number (strictly in this format of a + bi):")
    complex_num1 = complex(complex_str1.replace(" ", "").replace("i", "j"))
    print(f"Magnitude of {complex_str1}: {abs(complex_num1)}")
    print(f"Phase angle of {complex_str1}: {math.degrees(cmath.phase(complex_num1))}")
    print(f"Conjugate of {complex_str1}: {complex_num1.conjugate()}")

    print("Press ENTER to end the process")
    complex_str2 = input("Type in another complex number (again strictly in this format of a + bi):")
    if len(complex_str2) > 0:
        complex_num2 = complex(complex_str2.replace(" ", "").replace("i", "j"))
        print(f"Magnitude of {complex_str2}: {abs(complex_num2)}")
        print(f"Phase angle of {complex_str2}: {math.degrees(cmath.phase(complex_num2))}")
        print(f"Conjugate of {complex_str2}: {complex_num2.conjugate()}")

        print(f"\n\nComplex operation results for given two complex numbers {complex_str1} and {complex_str2}")
        complex_addition_str = f"{complex_num1 + complex_num2}".replace("j", "i").replace("(", "").replace(")", "")
        complex_subtraction_str = f"{complex_num1 - complex_num2}".replace("j", "i").replace("(", "").replace(")", "")
        complex_multiplication_str = f"{complex_num1 * complex_num2}".replace("j", "i").replace("(", "").replace(")", "")
        complex_division_str = f"{complex_num1 / complex_num2}".replace("j", "i").replace("(", "").replace(")", "")
        print(f"Addition: {complex_addition_str}") 
        print(f"Substraction: {complex_subtraction_str}")     
        print(f"Multiplication: {complex_multiplication_str}")     
        print(f"Division: {complex_division_str}")  
except Exception as x:
    print(f"Error while running: {x}")
