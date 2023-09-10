import numpy as np
import matplotlib.pyplot as plt

# I considered abstractifying this for different distributions
# but

# TO-DO: function descriptions


def generate_samples(s, n, p):
    samples = []
    for i in range(s):
        samples += [np.random.exponential(scale=1/170, size=n)]
        if i < p:

            # TO-DO: improve figure and ax formatting
            # histogram formatting
            fig = plt.figure()
            ax = fig.add_subplot()  # don't really understand what this is tbh

            plt.title('Sample' + str(i))
            plt.xlabel('Observation')
            plt.ylabel('Counts')
            # plt.grid(axis='y', alpha=0.75)

            ax.hist(samples[i], bins=25)

            # save histograms as image files if there is a reasonable amount of them
            fig.savefig('output' + str(i) + '.png')

            plt.clf()
    return samples


def generate_sample_mean_distribution(s, n, p=0):
    samples = generate_samples(s, n, p)
    # print(samples)
    sample_means = list(map(np.mean, samples))
    fig = plt.figure()
    ax = fig.add_subplot()

    plt.title('Sample Mean Density Plot')
    plt.xlabel('Observed Sample Mean')
    plt.ylabel('Counts')

    ax.hist(sample_means, bins=25)
    fig.savefig('sample_means.png')


def run():
    n = int(input("Enter sample size: "))
    s = int(input("Enter number of samples: "))
    p = int(input("Enter number of sample histograms to be generated: "))
    generate_sample_mean_distribution(s, n, p)


run()
