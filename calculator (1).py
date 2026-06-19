# ============================================
#        Python CLI Calculator
#        Author: Your Name
#        Description: A full-featured command-line
#                     calculator with history
# ============================================

import math
import os

# Store calculation history
history = []


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def display_banner():
    print("=" * 45)
    print("        🧮  PYTHON CALCULATOR  🧮")
    print("=" * 45)


def display_menu():
    print("\n📌 SELECT OPERATION:")
    print("-" * 45)
    print("  Basic Operations:")
    print("    1. ➕  Addition")
    print("    2. ➖  Subtraction")
    print("    3. ✖️   Multiplication")
    print("    4. ➗  Division")
    print("    5. 📐  Modulus (Remainder)")
    print("    6. 🔢  Power (x ^ y)")
    print("\n  Advanced Operations:")
    print("    7. √   Square Root")
    print("    8. |x| Absolute Value")
    print("    9. %   Percentage")
    print("   10. log Logarithm (base 10)")
    print("\n  Other:")
    print("   11. 📜  View History")
    print("   12. 🗑️   Clear History")
    print("    0. 🚪  Exit")
    print("-" * 45)


def get_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("  ⚠️  Invalid input! Please enter a valid number.")


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero!")
    return a / b


def modulus(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero!")
    return a % b


def power(a, b):
    return a ** b


def square_root(a):
    if a < 0:
        raise ValueError("Cannot take square root of a negative number!")
    return math.sqrt(a)


def absolute_value(a):
    return abs(a)


def percentage(a, b):
    """Calculate what percentage b is of a"""
    if a == 0:
        raise ZeroDivisionError("Base value cannot be zero!")
    return (b / a) * 100


def logarithm(a):
    if a <= 0:
        raise ValueError("Logarithm is only defined for positive numbers!")
    return math.log10(a)


def save_to_history(expression, result):
    history.append(f"{expression} = {result}")


def view_history():
    print("\n📜 CALCULATION HISTORY:")
    print("-" * 45)
    if not history:
        print("  No calculations yet!")
    else:
        for i, record in enumerate(history, 1):
            print(f"  {i}. {record}")
    print("-" * 45)


def clear_history():
    history.clear()
    print("\n  ✅ History cleared!")


def format_result(result):
    """Format result: remove .0 for whole numbers"""
    if isinstance(result, float) and result.is_integer():
        return int(result)
    return round(result, 6)


def run_calculator():
    clear_screen()
    display_banner()

    while True:
        display_menu()

        choice = input("\n👉 Enter your choice: ").strip()

        try:
            if choice == '0':
                print("\n👋 Thank you for using Python Calculator! Goodbye!\n")
                break

            elif choice == '1':
                a = get_number("  Enter first number:  ")
                b = get_number("  Enter second number: ")
                result = add(a, b)
                expr = f"{format_result(a)} + {format_result(b)}"
                print(f"\n  ✅ Result: {expr} = {format_result(result)}")
                save_to_history(expr, format_result(result))

            elif choice == '2':
                a = get_number("  Enter first number:  ")
                b = get_number("  Enter second number: ")
                result = subtract(a, b)
                expr = f"{format_result(a)} - {format_result(b)}"
                print(f"\n  ✅ Result: {expr} = {format_result(result)}")
                save_to_history(expr, format_result(result))

            elif choice == '3':
                a = get_number("  Enter first number:  ")
                b = get_number("  Enter second number: ")
                result = multiply(a, b)
                expr = f"{format_result(a)} × {format_result(b)}"
                print(f"\n  ✅ Result: {expr} = {format_result(result)}")
                save_to_history(expr, format_result(result))

            elif choice == '4':
                a = get_number("  Enter first number:  ")
                b = get_number("  Enter second number: ")
                result = divide(a, b)
                expr = f"{format_result(a)} ÷ {format_result(b)}"
                print(f"\n  ✅ Result: {expr} = {format_result(result)}")
                save_to_history(expr, format_result(result))

            elif choice == '5':
                a = get_number("  Enter first number:  ")
                b = get_number("  Enter second number: ")
                result = modulus(a, b)
                expr = f"{format_result(a)} % {format_result(b)}"
                print(f"\n  ✅ Result: {expr} = {format_result(result)}")
                save_to_history(expr, format_result(result))

            elif choice == '6':
                a = get_number("  Enter base number:   ")
                b = get_number("  Enter exponent:      ")
                result = power(a, b)
                expr = f"{format_result(a)} ^ {format_result(b)}"
                print(f"\n  ✅ Result: {expr} = {format_result(result)}")
                save_to_history(expr, format_result(result))

            elif choice == '7':
                a = get_number("  Enter number: ")
                result = square_root(a)
                expr = f"√{format_result(a)}"
                print(f"\n  ✅ Result: {expr} = {format_result(result)}")
                save_to_history(expr, format_result(result))

            elif choice == '8':
                a = get_number("  Enter number: ")
                result = absolute_value(a)
                expr = f"|{format_result(a)}|"
                print(f"\n  ✅ Result: {expr} = {format_result(result)}")
                save_to_history(expr, format_result(result))

            elif choice == '9':
                a = get_number("  Enter total value:  ")
                b = get_number("  Enter part value:   ")
                result = percentage(a, b)
                expr = f"{format_result(b)} is what % of {format_result(a)}"
                print(f"\n  ✅ Result: {format_result(result)}%")
                save_to_history(expr, f"{format_result(result)}%")

            elif choice == '10':
                a = get_number("  Enter number: ")
                result = logarithm(a)
                expr = f"log10({format_result(a)})"
                print(f"\n  ✅ Result: {expr} = {format_result(result)}")
                save_to_history(expr, format_result(result))

            elif choice == '11':
                view_history()

            elif choice == '12':
                clear_history()

            else:
                print("\n  ⚠️  Invalid choice! Please select a valid option.")

        except ZeroDivisionError as e:
            print(f"\n  ❌ Error: {e}")
        except ValueError as e:
            print(f"\n  ❌ Error: {e}")

        input("\n  Press Enter to continue...")
        clear_screen()
        display_banner()


# ─── Entry Point ───────────────────────────
if __name__ == "__main__":
    run_calculator()
