import numpy as np

zero_qubit = np.matrix('1; 0')
one_qubit = np.matrix('0; 1')
plus_qubit = 1 / np.sqrt(2) * np.matrix('1; 1')
minus_qubit = 1 / np.sqrt(2) * np.matrix('1; -1')
clockwisearrow_qubit = 1 / np.sqrt(2) * np.matrix([[1], [np.complex(0, 1)]])
counterclockwisearrow_qubit = 1 / np.sqrt(2) * np.matrix([[1], [-np.complex(0, 1)]])


def zero_to_one_qubit(percentage_zero, percentage_one):
    if not percentage_zero + percentage_one == 100 or percentage_zero < 0 or percentage_one < 0: raise Exception(
        "percentages must add up to 100\% and both be positive ")
    return np.sqrt(percentage_zero / 100.) * zero_qubit + np.sqrt(percentage_one / 100.) * one_qubit


def qubit(percentage_first, percentage_second, basis_first, basis_second):
    if not percentage_first + percentage_second == 100 or percentage_first < 0 or percentage_second < 0:
        raise Exception("percentages must add up to 100\% and both be positive ")
    return np.sqrt(percentage_first / 100.) * basis_first + np.sqrt(percentage_second / 100.) * basis_second


def get_bloch_coordinates(qubit):
    def get_x_bloch(qubit):
        qubit_x_basis = 1. / np.sqrt(2) * np.matrix('1 1; 1 -1') * qubit
        prob_zero_qubit = (qubit_x_basis.item(0) * qubit_x_basis.item(0).conjugate()).real
        prob_one_qubit = (qubit_x_basis.item(1) * qubit_x_basis.item(1).conjugate()).real
        return prob_zero_qubit - prob_one_qubit

    def get_y_bloch(qubit):
        qubit_y_basis = 1. / np.sqrt(2) * np.matrix('1 1; 1 -1') * np.matrix([[1, 0], [0, -np.complex(0, 1)]]) * qubit
        prob_zero_qubit = (qubit_y_basis.item(0) * qubit_y_basis.item(0).conjugate()).real
        prob_one_qubit = (qubit_y_basis.item(1) * qubit_y_basis.item(1).conjugate()).real
        return prob_zero_qubit - prob_one_qubit

    def get_z_bloch(qubit):
        qubit_z_basis = qubit
        prob_zero_qubit = (qubit_z_basis.item(0) * qubit_z_basis.item(0).conjugate()).real
        prob_one_qubit = (qubit_z_basis.item(1) * qubit_z_basis.item(1).conjugate()).real
        return prob_zero_qubit - prob_one_qubit

    return (get_x_bloch(qubit), get_y_bloch(qubit), get_z_bloch(qubit))


def plot_bloch(qubit, color='b', ax=None):
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    if not ax:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # draw sphere
        u, v = np.mgrid[0:2 * np.pi:20j, 0:np.pi:10j]
        x = np.cos(u) * np.sin(v)
        y = np.sin(u) * np.sin(v)
        z = np.cos(v)
        ax.plot_wireframe(x, y, z, color="k", alpha=.1)
        ax.grid(False)

    coordinates = get_bloch_coordinates(qubit)
    ax.quiver([0], [0], [0], [coordinates[0]], [coordinates[1]], [coordinates[2]], length=1, color=color,
              arrow_length_ratio=0.3)
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    ax.set_xlabel('x: |"-"> to |"+">')
    ax.set_ylabel('y: |"↺"> to |"↻">')
    ax.set_zlabel('z: |"1"> to |"0">')
    ax.view_init(azim=20)
    return ax

# 这里需要改写为函数，这样plt就能将运行期间的图像存储
def test():
    # Plotting all of our basis qubits, colors and orientation match the textbook figure
    import matplotlib.pyplot as plt
    ax = plot_bloch(zero_qubit, color='xkcd:red')
    plot_bloch(one_qubit, color='xkcd:orange', ax=ax)
    plot_bloch(plus_qubit, color='xkcd:yellow', ax=ax)
    plot_bloch(minus_qubit, color='xkcd:green', ax=ax)
    plot_bloch(clockwisearrow_qubit, color='xkcd:blue', ax=ax)
    plot_bloch(counterclockwisearrow_qubit, color='xkcd:purple', ax=ax)
    plot_bloch(zero_to_one_qubit(10, 90), color="xkcd:turquoise", ax=ax)
    # 缺少这个代码，会出现闪退现象
    plt.show()

# 主函数
if __name__ == '__main__':
    test()

# # Plotting all of our basis qubits, colors and orientation match the textbook figure
# ax = plot_bloch(zero_qubit, color='xkcd:red')
# plot_bloch(one_qubit, color='xkcd:orange', ax=ax)
# plot_bloch(plus_qubit, color='xkcd:yellow', ax=ax)
# plot_bloch(minus_qubit, color='xkcd:green', ax=ax)
# plot_bloch(clockwisearrow_qubit, color='xkcd:blue', ax=ax)
# plot_bloch(counterclockwisearrow_qubit, color='xkcd:purple', ax=ax)
#
# # Now plotting a qubit that is 10% |"0"> and 90% |"1"> in turquoise
# plot_bloch(zero_to_one_qubit(10, 90), color="xkcd:turquoise", ax=ax)
