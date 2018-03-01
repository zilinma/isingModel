import numpy as np
import matplotlib.pyplot as plt
import csv
import time

SIZE = 100
STEPS = 2000
T = 2.31
PATH = './data'
lattice = np.full((SIZE, SIZE), 1)
energyIncrement = {4: np.exp(-4/T), 8:np.exp(-8/T)}

def nearestNeighbor(lattice, row, col):
    '''
    Calculate nearest neighbor
    :param lattice: spin lattice
    :param row:
    :param col:
    :return:
    '''
    right = lattice[row][col] * lattice[(row + 1) % SIZE][col]
    left = lattice[row][col] * lattice[row][(col + 1) % SIZE]
    up = lattice[row][col] * lattice[row-1 ][col]
    down = lattice[row][col] * lattice[row][col - 1]
    return -(right + left + up + down)

def totalEnergy(lattice):
    '''
        Calcualte the total energy
    '''
    r = np.roll(lattice, 1, axis=1)  # roll right
    d = np.roll(lattice, 1, axis=0)  # roll down
    energy = np.sum((lattice * (r + d)))
    return -energy/SIZE ** 2

def totalMag(lattice):
    '''
    Calculates the total magnetization
    :param lattice:
    :return:
    '''
    mag = np.sum(lattice) / SIZE ** 2


    return mag

def step(lattice):
    '''
        Step once Monte Carlo step
    '''

    for i in range(SIZE ** 2):

        # flip
        pos = np.random.randint(0, SIZE, size=2)
        #print(pos)

        before = nearestNeighbor(lattice, pos[0], pos[1])
        lattice[pos[0]][pos[1]] *= -1
        after = nearestNeighbor(lattice, pos[0], pos[1])            # eee
        if after > before:
            dE = after - before


            prob = energyIncrement[dE]

            if (np.random.sample(1) >= prob):
                lattice[pos[0]][pos[1]] *= -1



energies = np.zeros(STEPS)
mags = np.zeros(STEPS)
with open(PATH +'/' +str(T) + '_' + str(SIZE) + '_'+ str(STEPS)+'.csv', 'w', newline='') as csvfile:
    testWriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    testWriter.writerow(["Step", "Energy", "Magnetization"])
    for i in range(STEPS):
        timerStart = time.time()
        step(lattice)
        timerEnd = time.time()
        print("Elpsed", timerEnd - timerStart)
        E = totalEnergy(lattice)
        M = totalMag(lattice)
        energies[i] = E
        mags[i] = M
        testWriter.writerow([i,E, M])
        #if i %100 == 0:
        print("Step:", i)
        print("total energy", E)
        print("total magnetization", M)

np.average(energies[70:])
np.average(mags[70:])
np.std(energies[70:])
np.std(mags[70:])


f, ax1 = plt.subplots(1, 2, figsize=(7, 3))

ax1[0].plot(energies)
ax1[1].plot(mags)

plt.show()
