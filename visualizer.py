
import matplotlib.pyplot as plot


def plot_2d_projection(data):

    plot.figure()
    plot.plot(-1, -1, 1, 1)

    for name, point in data.items():
        plot.text(point.x, point.y, name, fontsize=(4 + point.power))
    plot.show()



