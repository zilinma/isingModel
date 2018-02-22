import numpy as np
import matplotlib.pyplot as plt

SIZE = 100
STEPS = 300
T = 2

lattice = np.full((SIZE, SIZE), 1)


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
            prob = np.exp(-dE/T)
            if (np.random.sample(1) >= prob):
                lattice[pos[0]][pos[1]] *= -1


def writeEandMTo():
    '''
        Write to something
    '''

energies = np.zeros(STEPS)
mags = np.zeros(STEPS)
for i in range(STEPS):
    step(lattice)
    E = totalEnergy(lattice)
    M = totalMag(lattice)
    energies[i] = E
    mags[i] = M
    #if i %100 == 0:
    print("Step:", i)
    print("total energy", E)
    print("total magnetization", M)



f, ax1 = plt.subplots(1, 2, figsize=(7, 3))

ax1[0].plot(energies)
ax1[1].plot(mags)

plt.show()
