# Works, but axes are non responsive

import sys
import admin
import pypingn
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style


style.use('seaborn-darkgrid')
mpl.rcParams['toolbar'] = 'None'
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)
xar = []
yar = []


def animate(i):
    val = (str(pypingn.ping("104.160.131.3", 2)) + "\n").replace("(", "").replace(")", "")
    x, y = val.split(',')
    xar.append(float(x))
    yar.append(float(y))
    return ax1.plot(xar, yar, 'C0', animated=True)


def run():
    if not admin.isUserAdmin():
        rc = admin.runAsAdmin()
    else:
        rc = 0
        ani = animation.FuncAnimation(fig,
                                      animate,
                                      frames=200,
                                      interval=1,
                                      save_count=100,
                                      blit=True
                                      )
        plt.show()
    return rc


if __name__ == '__main__':
    sys.exit(run())
