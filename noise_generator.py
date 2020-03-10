import numpy as np
import matplotlib.pyplot as plt

"""
I got this perlin noise generator from here:
https://stackoverflow.com/questions/42147776/producing-2d-perlin-noise-with-numpy
"""


def perlin(x, y, seed=0):
    # permutation table
    np.random.seed(seed)
    p = np.arange(256, dtype=int)
    np.random.shuffle(p)
    p = np.stack([p, p]).flatten()
    # coordinates of the top-left
    xi = x.astype(int)
    yi = y.astype(int)
    # internal coordinates
    xf = x - xi
    yf = y - yi
    # fade factors
    u = fade(xf)
    v = fade(yf)
    # noise components
    n00 = gradient(p[p[xi] + yi], xf, yf)
    n01 = gradient(p[p[xi] + yi + 1], xf, yf - 1)
    n11 = gradient(p[p[xi + 1] + yi + 1], xf - 1, yf - 1)
    n10 = gradient(p[p[xi + 1] + yi], xf - 1, yf)
    # combine noises
    x1 = lerp(n00, n10, u)
    x2 = lerp(n01, n11, u)
    return lerp(x1, x2, v)


def lerp(a, b, x):
    """linear interpolation"""
    return a + x * (b - a)


def fade(t):
    """6t^5 - 15t^4 + 10t^3"""
    return 6 * t ** 5 - 15 * t ** 4 + 10 * t ** 3


def gradient(h, x, y):
    """grad converts h to the right gradient vector and return the dot product with (x,y)"""
    vectors = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])
    g = vectors[h % 4]
    return g[:, :, 0] * x + g[:, :, 1] * y


def get_terrain_information(seed, width, show_noise=False, show_2d_landscape=False):
    lin = np.linspace(0, width / 20, width, endpoint=False)
    x, y = np.meshgrid(lin, lin)

    perlin_values = perlin(x, y, seed=seed)

    perlin_values_y_offset = perlin_values[50]
    if show_noise:
        plt.imshow(perlin_values, origin='upper')
        plt.show()
    if show_2d_landscape:
        plt.plot(perlin_values_y_offset)
        plt.show()

    return perlin_values_y_offset


if __name__ == '__main__':
    get_terrain_information(115, 10 * 16, True, True)
