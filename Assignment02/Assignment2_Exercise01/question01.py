# Exercise 1: Create a math_utils module with functions for area calculations
from math_utils import area_circle, area_rectangle, area_triangle, area_square

# Test the area calculation functions
print("=" * 50)
print("Area Calculations using math_utils module")
print("=" * 50)

# Circle area
radius = 5
circle_area = area_circle(radius)
print(f"\nCircle with radius {radius}: Area = {circle_area:.2f}")

# Rectangle area
length = 10
width = 5
rectangle_area = area_rectangle(length, width)
print(f"Rectangle {length} x {width}: Area = {rectangle_area}")

# Triangle area
base = 8
height = 6
triangle_area = area_triangle(base, height)
print(f"Triangle with base {base} and height {height}: Area = {triangle_area}")

# Square area
side = 7
square_area = area_square(side)
print(f"Square with side {side}: Area = {square_area}")

print("\n" + "=" * 50)