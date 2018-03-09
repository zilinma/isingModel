'''
Calculate co


'''


import csv
import numpy as np
import matplotlib.pyplot as plt

SIZE = 100
STEPS = 1500
START = 200
END = 1000
T = 2.48


PATH = './data'
magnetization = np.zeros(STEPS)
energy = np.zeros(STEPS)

def coralation(mag,i):
    a = mag[START:END]
    b = mag[START + i:END + i]
    return (np.mean(b*a) - np.mean(a) * np.mean(b))/(np.std(a) * np.std(b))


with open(PATH +'/' +str(T) + '_' + str(SIZE) + '_'+ str(STEPS)+'.csv', 'r', newline='') as csvfile:
    testReader = csv.reader(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    next(testReader, None)  # skip the headers
    for i,row in enumerate(testReader):
        magnetization[i] = float(row[2])
        energy[i] = float(row[1])
co = np.zeros(STEPS - END)
for i in range(STEPS - END):
    co[i] = coralation(magnetization, i)

f, ax1 = plt.subplots(1, 2, figsize=(7, 3))

ax1[0].plot(energy)
ax1[1].plot(magnetization)
plt.axhline()
plt.show()

print(np.mean(magnetization[200:]))
print(np.mean(energy[200:]))
print(np.var(magnetization[200:]))

print(np.var(energy[200:]))
