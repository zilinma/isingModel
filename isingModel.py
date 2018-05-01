import numpy as np
import matplotlib.pyplot as plt
import csv
import time

SIZE = 100      # size of the lattice

STEPS = 4000    # number of MC steps
T = 1.9         # reduced temperature
PATH = './data' # path to the data. Should mkdir one if doesn't exist.
lattice = np.full((SIZE, SIZE), 1)  # initialize lattice

'''
    Defines probability for flipping. There are only 5 change in
    energies and only 2 of them are positive (makes the energy go up).
    This change makes decent speed up, roughtly about 20%. As for speed
    up, np is doing a good job by computing all of the matrixes in more
    efficient languages i.e. C family. 
'''
energyIncrement = {4: np.exp(-4/T), 8:np.exp(-8/T)}

def nearestNeighbor(lattice, row, col):
    '''
    Calculate nearest neighbor
    Neighbors are defined as
        UP
    LEFT  RIGHT
       DOWN
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
        Calcualte the total energy. Using the rolling method from James
    '''
    r = np.roll(lattice, 1, axis=1)  # roll right
    d = np.roll(lattice, 1, axis=0)  # roll down
    energy = np.sum((lattice * (r + d)))
    return -energy/SIZE ** 2

def totalMag(lattice):
    '''
    Calculates the total magnetization
    just the sum of all M moments then normalize.
    :param lattice
    :return:
    '''
    mag = np.sum(lattice) / SIZE ** 2
    return mag

def step(lattice):
    '''
        Step Monte Carlo for 1 step
    '''

    for i in range(SIZE ** 2):

        # flip
        pos = np.random.randint(0, SIZE, size=2)
        #print(pos)

        before = nearestNeighbor(lattice, pos[0], pos[1])
        lattice[pos[0]][pos[1]] *= -1
        
        after = nearestNeighbor(lattice, pos[0], pos[1])
        if after > before:
            dE = after - before
            prob = energyIncrement[dE]

            if (np.random.sample(1) >= prob):
                lattice[pos[0]][pos[1]] *= -1


def runIsing():
    """
    Runs ising model and save the data to different files.
    CSV data for magnetization and energy --
        Naming convention:
            T_SIZE_STEPS.csv

    Lattice data after each finished run --
        Naming convention:
            T_SIZE_STEPS.npy     -> numpy arrays pickle file. np.load will load these.
            T_SIZE_STEPS.txt     -> human readable txt files.
    :return:
    """
    energies = np.zeros(STEPS)
    mags = np.zeros(STEPS)
    with open(PATH +'/' +str(round(T, 2)) + '_' + str(SIZE) + '_'+ str(STEPS)+'.csv', 'w', newline='') as csvfile:
        testWriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        testWriter.writerow(["Step", "Energy", "Magnetization"])
        for i in range(STEPS):
            #timerStart = time.time()
            step(lattice)
            #timerEnd = time.time()
            #print("Elpsed", timerEnd - timerStart)
            E = totalEnergy(lattice)
            M = totalMag(lattice)
            energies[i] = E
            mags[i] = M
            testWriter.writerow([i,E, M])
            #if i %100 == 0:
            print("Step:", i)
            print("total energy", E)
            print("total magnetization", M)

    with open(PATH + '/matrixes' +'/' +str(round(T, 2)) + '_' + str(SIZE) + '_'+ str(STEPS), 'w', newline='') as file:
        np.save(file, lattice)

'''
f, ax1 = plt.subplots(1, 2, figsize=(7, 3))

ax1[0].plot(energies)
ax1[1].plot(mags)

plt.show()

'''
for i in range(30):
    '''
        runs ising models in multiple runs. Good for overnight experiments.
    '''
    runIsing()
    T += 0.01               # update T
    lattice = np.full((SIZE, SIZE), 1)          # initialize lattice
    energyIncrement = {4: np.exp(-4 / T), 8: np.exp(-8 / T)}            # initialize energy increments

