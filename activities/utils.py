import random
import math
from fractions import Fraction


def generate_valid_fraction():
    while True:
        numerator = random.randint(-9, 9)
        denominator = random.choices([random.randint(2, 9), -random.randint(1, 9)], weights=[0.75, 0.25])[0]
        # Ensure that the numerator and denominator are not the same and denominator is not zero
        if numerator != 0 and denominator != 0 and numerator != denominator and numerator != -denominator:
            return (numerator, denominator)


def generate_valid_integer():
    integer = random.randint(-9, 9)
    while integer == 0:
        integer = random.randint(-9, 9)
    return integer


def add_subtract_fractions(term1, term2, operator):
    steps = []

    # Convert integers to fractions if needed
    if isinstance(term1, int):
        term1 = (term1, 1)
    if isinstance(term2, int):
        term2 = (term2, 1)

    num1, denom1 = term1
    num2, denom2 = term2

    # Step 1: Find common denominator
    lcm_denominator = math.lcm(denom1, denom2)
    num1_adjusted = num1 * (lcm_denominator // denom1)
    num2_adjusted = num2 * (lcm_denominator // denom2)
    steps.append(f"({num1} * {lcm_denominator // denom1})/{lcm_denominator} {operator} ({num2} * {lcm_denominator // denom2})/{lcm_denominator}")

    # Step 2: Combine numerators
    combined_numerator = num1_adjusted + num2_adjusted if operator == "+" else num1_adjusted - num2_adjusted
    steps.append(f"({num1_adjusted} {operator} {num2_adjusted})/{lcm_denominator}")

    # Step 3: Simplify fraction
    simplified_fraction = Fraction(combined_numerator, lcm_denominator)
    final_numerator, final_denominator = simplified_fraction.numerator, simplified_fraction.denominator

    # Convert fraction to int if the denominator is 1 or it's equivalent to 0
    if final_denominator == 1 or final_numerator == 0:
        final_numerator = int(final_numerator)
        final_denominator = 1
    steps.append(f"{final_numerator}/{final_denominator}")

    return steps, simplified_fraction


def simplify_multiply_fractions(term1, term2):
    steps = []
    
    # Convert integers to fractions if needed
    if isinstance(term1, int):
        term1 = (term1, 1)
    if isinstance(term2, int):
        term2 = (term2, 1)

    num1, denom1 = term1
    num2, denom2 = term2

    # Step 1: Write out the multiplication expression
    steps.append(f"({num1} * {num2}) / ({denom1} * {denom2})")

    # Step 2: Simplify across numerator and denominator (look for common factors)
    gcd_1_2 = math.gcd(num1, denom2)  # gcd of num1 with denom2
    gcd_2_1 = math.gcd(num2, denom1)  # gcd of num2 with denom1

    # Simplify by dividing both numerator and denominator by their common factors
    if gcd_1_2 > 1:
        num1 //= gcd_1_2
        denom2 //= gcd_1_2
        steps.append(f"({num1} * {num2}) / ({denom1} * {denom2})")
    
    if gcd_2_1 > 1:
        num2 //= gcd_2_1
        denom1 //= gcd_2_1
        steps.append(f"({num1} * {num2}) / ({denom1} * {denom2})")

    # Step 3: Multiply the numerators and denominators
    combined_numerator = num1 * num2
    combined_denominator = denom1 * denom2
    steps.append(f"{combined_numerator} / {combined_denominator}")

    # Step 4: Final simplification (if necessary)
    gcd_final = math.gcd(combined_numerator, combined_denominator)
    simplified_numerator = combined_numerator // gcd_final
    simplified_denominator = combined_denominator // gcd_final

    # Final step: Convert to a simpler form if the denominator is 1 or the numerator is 0
    if simplified_denominator == 1 or simplified_numerator == -1:
        simplified_numerator = int(simplified_numerator)
        simplified_denominator = 1
        
    
    simplified_fraction = Fraction(simplified_numerator, simplified_denominator)
    if f"{simplified_fraction}"!=f"{combined_numerator}/{combined_denominator}":
        steps.append(f"{simplified_fraction}")

    # Return steps and the simplified result

    return steps


def generate_basic_expression():
    def choose_terms():
        # Adjust weights to favor fractions
        term1 = random.choice([generate_valid_fraction(), generate_valid_integer()])
        term2 = random.choice([generate_valid_fraction(), generate_valid_integer()])

        while isinstance(term1, int) and isinstance(term2, int):
            term2 = random.choice([generate_valid_fraction(), generate_valid_integer()])

        while term1 == term2:
            term2 = random.choice([generate_valid_fraction(), generate_valid_integer()])

        return term1, term2

    term1, term2 = choose_terms()
    operators = ["+", "-", "*", "/"]
    operator_weights = [0.5, 0.5, 0, 0]
    operator = random.choices(operators, weights=operator_weights, k=1)[0]
    steps = []

    simplified_fraction = None  # Initialize simplified_fraction to ensure it's available in all cases

    # Addition or Subtraction Case
    if operator in ["+", "-"]:
        expression = f"{format_fraction(term1)} {operator} {format_fraction(term2)}"
        steps, simplified_fraction = add_subtract_fractions(term1, term2, operator)
        if steps and format_fraction(simplified_fraction) != steps[-1]:
            steps.append(f"{format_fraction(simplified_fraction)}")

    # Multiplication Case
    elif operator == "*":
        expression = f"{format_fraction(term1)} * {format_fraction(term2)}"
        steps= simplify_multiply_fractions(term1, term2)
        # Division case
    elif operator == "/":
        # Ensure term2 is in fraction form
        if isinstance(term2, int):
            term2 = (term2, 1)
            
        # Invert the second term for division
        term2_inverted = (term2[1], term2[0])
        expression = f"{format_fraction(term1)} / {format_fraction(term2)}"
        steps.append(f"{format_fraction(term1)} * {format_fraction(term2_inverted)}")
        
        # Now handle it as a multiplication case
        steps += simplify_multiply_fractions(term1, term2_inverted)

    # Now, add the final simplified result as a step, not the final expression

    return expression, steps


def format_fraction(term):
    if isinstance(term, tuple):
        num, denom = term
        # Simplify fractions like -4/1 to -4 and 0/2 to 0
        if denom == 1:
            return str(num)  # Return as integer
        # Add parentheses around negative numerators or denominators
        if num < 0:
            num = f"({num})"
        if denom < 0:
            denom = f"({denom})"
        return f"{num}/{denom}"  # Return as fraction with possible parentheses
    return str(term)  # Return as integer if it's not a fraction






def generate_intermediate_expression():
    # Example generation for a basic level expression involving fractions
    fractions = [f"{random.randint(1, 9)}/{random.randint(1, 9)}" for _ in range(4)]
    operators = ["+", "-", "*", "/"]
    expression = f"{fractions[0]} {random.choice(operators)} {fractions[1]} {random.choice(operators)} {fractions[2]} {random.choice(operators)} {fractions[3]}"
    return expression



'''def generate_intermediate_expression():
    # Example generation for an intermediate level expression involving fractions and brackets
    fractions = [f"{random.randint(1, 9)}/{random.randint(1, 9)}" for _ in range(3)]
    operators = ["+", "-", "*", "/"]
    expression = f"{random.randint(1, 9)} - ({fractions[0]} {random.choice(operators)} {fractions[1]}) {random.choice(operators)} {fractions[2]}"
    return expression

'''