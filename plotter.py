'''
    This code plots our final results from the experiment.
    We have a pretty good M data and predicted fairly well of the
    critical temperature. After sampling our E data, we get a derivative
    that fits more about the theoretical value of dE/dt, which has a sharp
    peak at the critical temperature.


'''


import numpy as np
import matplotlib.pyplot as plt
import csv
def readTot(filePath):
    '''
    reads in csv format data.
    :param filePath: path to the data. "isingTot.csv"
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
    '''
    Theoretical solution of Ising Model.
    :param x: x axis
    :return: an nparray of the magnetization function.
    '''
    return np.power(1-np.power(np.sinh(2/x),-4),1/8)


def plotEMDEDT(energy, magnetization, temperature):
    '''
    Plots E vs T, M vs T and dE/dT vs T
    :param energy: an array that contains energy values for different T.
    :param magnetization: an array that contains magnetization values for different T.
    :param temperature: an array that contains all of the temperature
    '''

    # calculates derivative. (E rolls 1 - E) / (T rolls 1 - T)
    # sample every 5 of the points since the noise is too big.
    derivative = (np.roll(energy[::5], 1) - energy[::5])/ (np.roll(temperature[::5], 1) - temperature[::5])
    f, ax = plt.subplots(1, 3, figsize=(7, 3))

    ax[0].plot(temperature, energy, 'ro')
    # ax[0].axhline()
    ax[0].set_title("E")

    ax[1].plot(temperature, magnetization, 'ro')
    x = np.linspace(1.9, 2.268, 1000)
    ax[1].plot(np.append(x, 2.269),
                  np.append(theoryMag(x), 0))

    # ax[0][1].axhline()
    ax[1].set_title("M")

    # pop the first element since roll wraps the last point to the first entry,
    ax[2].plot(temperature[::5][1:], derivative[1:])

    # ax[2].axhline()
    ax[2].set_title(r'$\frac{dE}{dT}$')
    plt.show()


energy, magnetization, temperature = readTot("isingTot.csv")
plotEMDEDT(energy, magnetization, temperature)
