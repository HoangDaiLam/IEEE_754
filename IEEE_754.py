"""
IEEE 754 Single Precision Floating-Point Representation
========================================================

Single Precision Format (32 bits):
- 1 bit: Sign (0 = positive, 1 = negative)
- 8 bits: Exponent (biased by 127)
- 23 bits: Mantissa (fraction)

Format: [Sign][Exponent][Mantissa]
        [  1  ][   8   ][   23   ]

Value = (-1)^sign x 2^(exponent-127) x (1.mantissa)
"""

import struct


class IEEE754SinglePrecision:
    """Class to represent and analyze IEEE 754 single precision floats."""
    
    def __init__(self, value):
        """
        Initialize with a float value.
        
        Args:
            value: Float number to represent
        """
        self.value = value
        self.binary_representation = self._get_binary_representation()
        self.sign_bit = self.binary_representation[0]
        self.exponent_bits = self.binary_representation[1:9]
        self.mantissa_bits = self.binary_representation[9:32]
    
    def _get_binary_representation(self):
        """
        Get 32-bit binary representation of the float.
        
        Returns:
            String of 32 binary digits
        """
        # Pack as single precision float, unpack as unsigned int
        packed = struct.pack('!f', self.value)
        as_int = struct.unpack('!I', packed)[0]
        
        # Convert to 32-bit binary string
        binary = format(as_int, '032b')
        return binary
    
    def get_sign(self):
        """Get the sign of the number."""
        return int(self.sign_bit)
    
    def get_exponent_raw(self):
        """Get raw exponent value (biased)."""
        return int(self.exponent_bits, 2)
    
    def get_exponent_unbiased(self):
        """Get unbiased exponent (subtract 127)."""
        return self.get_exponent_raw() - 127
    
    def get_mantissa(self):
        """Get mantissa as binary string."""
        return self.mantissa_bits
    
    def get_mantissa_value(self):
        """
        Calculate actual mantissa value (1.fraction).
        
        Returns:
            Float value of mantissa
        """
        fraction = 0.0
        for i, bit in enumerate(self.mantissa_bits):
            if bit == '1':
                fraction += 2 ** (-(i + 1))
        return 1.0 + fraction
    
    def is_special(self):
        """Check if number is special (NaN, Infinity, Zero, Denormalized)."""
        exponent_raw = self.get_exponent_raw()
        mantissa_int = int(self.mantissa_bits, 2)
        
        if exponent_raw == 255:
            if mantissa_int == 0:
                return "Infinity"
            else:
                return "NaN"
        elif exponent_raw == 0:
            if mantissa_int == 0:
                return "Zero"
            else:
                return "Denormalized"
        return None
    
    def display(self):
        """Display detailed information about the float representation."""
        print("=" * 70)
        print(f"IEEE 754 Single Precision Analysis")
        print("=" * 70)
        print(f"Decimal Value: {self.value}")
        print()
        
        # Binary representation
        print("Binary Representation (32 bits):")
        print(f"  {self.sign_bit} | {self.exponent_bits} | {self.mantissa_bits}")
        print(f"  ↑   ↑{'─' * 8}↑   ↑{'─' * 23}↑")
        print(f"  │   Exponent(8)   Mantissa(23)")
        print(f"  Sign")
        print()
        
        # Check for special values
        special = self.is_special()
        if special:
            print(f"Special Value: {special}")
            if special == "Infinity":
                sign = "Negative" if self.get_sign() == 1 else "Positive"
                print(f"   {sign} Infinity")
            elif special == "Zero":
                sign = "-" if self.get_sign() == 1 else "+"
                print(f"   {sign}0.0")
            print("=" * 70)
            return
        
        # Sign
        sign = self.get_sign()
        sign_str = "Negative (-)" if sign == 1 else "Positive (+)"
        print(f"Sign Bit: {sign}")
        print(f"  → {sign_str}")
        print()
        
        # Exponent
        exp_raw = self.get_exponent_raw()
        exp_unbiased = self.get_exponent_unbiased()
        print(f"Exponent (8 bits): {self.exponent_bits}")
        print(f"  → Raw value: {exp_raw}")
        print(f"  → Unbiased (subtract 127): {exp_raw} - 127 = {exp_unbiased}")
        print(f"  → Power of 2: 2^{exp_unbiased} = {2**exp_unbiased}")
        print()
        
        # Mantissa
        mantissa_val = self.get_mantissa_value()
        print(f"Mantissa (23 bits): {self.mantissa_bits}")
        print(f"  → Implicit leading 1: 1.{self.mantissa_bits}")
        print(f"  → Decimal value: {mantissa_val:.10f}")
        print()
        
        # Final calculation
        sign_multiplier = -1 if sign == 1 else 1
        calculated = sign_multiplier * (2 ** exp_unbiased) * mantissa_val
        
        print("Final Calculation:")
        print(f"  Value = (-1)^sign x 2^exponent x mantissa")
        print(f"  Value = (-1)^{sign} x 2^{exp_unbiased} x {mantissa_val:.10f}")
        print(f"  Value = {sign_multiplier} x {2**exp_unbiased} x {mantissa_val:.10f}")
        print(f"  Value = {calculated}")
        print()
        
        # Hexadecimal
        hex_rep = hex(int(self.binary_representation, 2))
        print(f"Hexadecimal: {hex_rep}")
        print("=" * 70)


def float_to_ieee754(value):
    """
    Convert float to IEEE 754 representation.
    
    Args:
        value: Float to convert
    
    Returns:
        IEEE754SinglePrecision object
    """
    return IEEE754SinglePrecision(value)


def binary_to_float(binary_str):
    """
    Convert 32-bit binary string to float.
    
    Args:
        binary_str: 32-bit binary string
    
    Returns:
        Float value
    """
    if len(binary_str) != 32:
        raise ValueError("Binary string must be 32 bits")
    
    # Convert binary to integer
    as_int = int(binary_str, 2)
    
    # Pack as unsigned int, unpack as float
    packed = struct.pack('!I', as_int)
    value = struct.unpack('!f', packed)[0]
    
    return value


def hex_to_float(hex_str):
    """
    Convert hexadecimal string to float.
    
    Args:
        hex_str: Hexadecimal string (with or without 0x prefix)
    
    Returns:
        Float value
    """
    # Remove 0x prefix if present
    if hex_str.startswith('0x') or hex_str.startswith('0X'):
        hex_str = hex_str[2:]
    
    # Convert hex to integer
    as_int = int(hex_str, 16)
    
    # Pack as unsigned int, unpack as float
    packed = struct.pack('!I', as_int)
    value = struct.unpack('!f', packed)[0]
    
    return value


def interactive_menu():
    """Interactive menu for IEEE 754 analysis."""
    
    print("\n" + "=" * 70)
    print("IEEE 754 Single Precision Floating-Point Analyzer")
    print("=" * 70)
    
    while True:
        print("\nOptions:")
        print("1. Analyze a decimal number")
        print("2. Convert binary (32 bits) to float")
        print("3. Convert hexadecimal to float")
        print("4. Show special values examples")
        print("5. Show common examples")
        print("0. Exit")
        
        choice = input("\nEnter choice: ").strip()
        
        if choice == "1":
            try:
                value = float(input("Enter decimal number: "))
                ieee = float_to_ieee754(value)
                ieee.display()
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        
        elif choice == "2":
            binary = input("Enter 32-bit binary: ").strip()
            try:
                value = binary_to_float(binary)
                print(f"\nDecimal value: {value}")
                ieee = float_to_ieee754(value)
                ieee.display()
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == "3":
            hex_str = input("Enter hexadecimal (e.g., 0x40490FDB): ").strip()
            try:
                value = hex_to_float(hex_str)
                print(f"\nDecimal value: {value}")
                ieee = float_to_ieee754(value)
                ieee.display()
            except Exception as e:
                print(f"Error: {e}")
        
        elif choice == "4":
            show_special_values()
        
        elif choice == "5":
            show_common_examples()
        
        elif choice == "0":
            print("\nGoodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")


def show_special_values():
    """Display special IEEE 754 values."""
    print("\n" + "=" * 70)
    print("Special IEEE 754 Values")
    print("=" * 70)
    
    special_values = [
        ("Zero", 0.0),
        ("Negative Zero", -0.0),
        ("Positive Infinity", float('inf')),
        ("Negative Infinity", float('-inf')),
        ("NaN", float('nan')),
    ]
    
    for name, value in special_values:
        print(f"\n{name}:")
        ieee = float_to_ieee754(value)
        print(f"  Binary: {ieee.binary_representation}")
        print(f"  Parts: {ieee.sign_bit} | {ieee.exponent_bits} | {ieee.mantissa_bits}")


def show_common_examples():
    """Show common example values."""
    print("\n" + "=" * 70)
    print("Common Examples")
    print("=" * 70)
    
    examples = [
        1.0,
        -1.0,
        2.0,
        0.5,
        3.14159,
        -273.15,
        123.456
    ]
    
    for value in examples:
        print(f"\n{value}:")
        ieee = float_to_ieee754(value)
        print(f"  Binary: {ieee.binary_representation}")
        print(f"  Hex: {hex(int(ieee.binary_representation, 2))}")


def main():
    """Main program entry point."""
    print("""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║        IEEE 754 Single Precision Floating-Point Analyzer         ║
    ║                                                                  ║
    ║  Understand how computers represent decimal numbers in binary   ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
    
    #show a quick example
    print("Quick Example: Analyzing 3.14159")
    print("-" * 70)
    example = float_to_ieee754(3.14159)
    example.display()
    
    input("\nPress Enter to continue to interactive menu...")
    
    interactive_menu()


if __name__ == "__main__":
    main()