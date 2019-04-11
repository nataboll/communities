import numpy as np

grades = [7, 8, 9, 8, 8, 9, 8, 10, 8, 7, 10, 9, 8, 7, 9, 9, 10, 10, 10, 8, 7, 5, 9, 6, 8, 5, 9, 8, 7, 5, 6, 7, 7, 3, 4, 8, 8, 9, 7, 8, 9, 6, 8, 9, 8, 8, 9, 8, 8, 10, 5, 8, 8, 8, 6, 7, 10, 10, 9, 10, 10, 10, 9, 10, 10]

grades_5 = []
for grade in grades:
    if grade >= 8:
        grades_5.append(5)
    elif grade >= 5:
        grades_5.append(4)
    else:
        grades_5.append(3)

print(np.mean(grades))
print(np.mean(grades_5))
