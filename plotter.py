import numpy as np
import matplotlib.pyplot as plt
import csv
def readTot(filePath):
    '''
    reads data
    :param filePath: path to the data
    :return: energy, magnetization, temperature
    '''
    energy = []
    magnetization = []
    temperature = []
    with open(filePath) as csvfile:
        testReader = csv.reader(csvfile, delimiter=' ',
                                quotechar='|')
        for row in testReader:
            temperature.append(row[0])
            magnetization.append(row[1])
            energy.append([2])

    return energy, magnetization, temperature

def plotEMDEDT(energy, magnetization, temperature):
    '''
    Plots E/T, M/T and dE/T
    :param energy: an array that contains energy values for different T.
    :param magnetization: an array that contains magnetization values for different T.
    :param temperature: an array that contains all of the temperature
    '''
    derivative = (np.roll(energy, 1) - energy)/ (np.roll(temperature, 1) - temperature)
    f, ax = plt.subplots(3, figsize=(7, 3))

    ax[0].plot(temperature, energy)
    ax[0].axhline()
    ax[0].set_title("E")
    ax[1].plot(temperature, magnetization)
    ax[1].axhline()
    ax[1].set_title("M")

    ax[2].plot(temperature, derivative)
    ax[2].axhline()
    ax[2].set_title(r'$\frac{dE}{dT}$')
    plt.show()