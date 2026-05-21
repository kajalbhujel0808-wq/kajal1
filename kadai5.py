scores = [80,55,90,40]

def average(numbers):
     total = 0

     for n in numbers:
        total = total + n

        return total / len(numbers)

print(average(scores))