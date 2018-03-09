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
        testReader = csv.reader(csvfile, delimiter=',',
                                quotechar='|')
        next(testReader, None)
        for row in testReader:
            temperature.append(float(row[0]))
            magnetization.append(float(row[1]))
            energy.append(float(row[2]))

    return energy, magnetization, temperature


def theoryMag(x):

    return np.power(1-np.power(np.sinh(2/x),-4),1/8)


def plotEMDEDT(energy, magnetization, temperature):
    '''
    Plots E/T, M/T and dE/T
    :param energy: an array that contains energy values for different T.
    :param magnetization: an array that contains magnetization values for different T.
    :param temperature: an array that contains all of the temperature
    '''
    derivative = (np.roll(energy[::5], 1) - energy[::5])/ (np.roll(temperature[::5], 1) - temperature[::5])
    f, ax = plt.subplots(1, 3, figsize=(7, 3))

    ax[0].plot(temperature, energy, 'ro')
    #ax[0].axhline()
    ax[0].set_title("E")

    ax[1].plot(temperature, magnetization, 'ro')
    x = np.linspace(1.9, 2.268, 1000)
    ax[1].plot(np.append(x, 2.269),
                  np.append(theoryMag(x), 0))
    #ax[0][1].axhline()
    ax[1].set_title("M")


    ax[2].plot(temperature[::5], derivative)
    #ax[2].axhline()
    ax[2].set_title(r'$\frac{dE}{dT}$')
    plt.show()


energy, magnetization, temperature = readTot("isingTot.csv")
plotEMDEDT(energy, magnetization, temperature)
