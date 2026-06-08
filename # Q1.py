# Q1
text = input("Enter a string: ")
reversed_text = ""

for i in range(len(text) - 1, -1, -1):
    reversed_text += text[i]

print("Reversed string:", reversed_text)

# Q2
num1 = int(input("Enter the first number: "))
num2 = int(input("Enter the second number: "))

print("Prime numbers between", num1, "and", num2, "are:")

for num in range(num1, num2 + 1):
    if num > 1:
        is_prime = True
        for i in range(2, num):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            print(num)

# Q3
numbers = [1, 2, 3, 4, 5, 6]
even_sum = 0

for num in numbers:
    if num % 2 == 0:
        even_sum += num

print("Sum of even numbers:", even_sum)

# Q4
score = int(input("Enter the student's score: "))

if score >= 90:
    print("A")
elif score >= 80:
    print("B")
elif score >= 70:
    print("C")
elif score >= 60:
    print("D")
else:
    print("F")

# Q5
year = int(input("Enter a year: "))

if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
    print(True)
else:
    print(False)


# Q6
numbers = [1, 2, 3, 4, 5, 6]
new_list = []

for i in range(0, len(numbers), 2):
    new_list.append(numbers[i])

print(new_list)

# Q7
numbers = [12, 45, 23, 56, 78, 34]

largest = numbers[0]
smallest = numbers[0]

for num in numbers:
    if num > largest:
        largest = num
    if num < smallest:
        smallest = num

print("Largest element:", largest)
print("Smallest element:", smallest)

# Q8
numbers = [1, 2, 2, 3, 4, 1]
unique_list = []

for num in numbers:
    if num not in unique_list:
        unique_list.append(num)

print(unique_list)

# Q9
squares_of_odds = []

for num in range(1, 21):
    if num % 2 != 0:
        squares_of_odds.append(num ** 2)

print(squares_of_odds)

# Q10
try:
    regular_hours = float(input("Enter regular hours worked: "))
    overtime_hours = float(input("Enter overtime hours worked: "))
    hourly_rate = float(input("Enter hourly rate: "))

    if regular_hours < 0 or overtime_hours < 0 or hourly_rate < 0:
        print("Error: Inputs cannot be negative.")
    elif regular_hours > 40:
        print("Error: Regular hours must be between 0 and 40.")
    else:
        regular_pay = regular_hours * hourly_rate
        overtime_pay = overtime_hours * hourly_rate * 1.5
        total_pay = regular_pay + overtime_pay

        print("Total pay:", total_pay)

except ValueError:
    print("Error: Please enter numeric values only.")

# Q11
set1 = {1, 2, 3, 4}
set2 = {3, 4, 5, 6}

print("Symmetric difference:", set1.symmetric_difference(set2))