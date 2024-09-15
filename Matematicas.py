import numpy as np
from scipy.integrate import odeint
from Implement import ImplementacionModelos
import matplotlib.pyplot as plt


def runge_kutta_4(f, y0, t, *args):
    """
    Implementación del método de Runge-Kutta de cuarto orden.
    :param f: Función que define el sistema de ODEs
    :param y0: Condiciones iniciales
    :param t: Tiempo
    :return: Solución aproximada en el tiempo t
    """
    n = len(t)
    y = np.zeros((n, len(y0)))
    y[0] = y0
    h = t[1] - t[0]
    for i in range(1, n):
        k1 = h * np.array(f(y[i-1], t[i-1], *args))
        k2 = h * np.array(f(y[i-1] + 0.5 * k1, t[i-1] + 0.5 * h, *args))
        k3 = h * np.array(f(y[i-1] + 0.5 * k2, t[i-1] + 0.5 * h, *args))
        k4 = h * np.array(f(y[i-1] + k3, t[i-1] + h, *args))
        y[i] = y[i-1] + (k1 + 2*k2 + 2*k3 + k4) / 6.0
    return y

def solve(mod, condiciones_iniciales, t, *args):
    """
    Resuelve el sistema de ODEs usando odeint y Runge-Kutta de cuarto orden.
    :param mod: Función que define el sistema de ODEs
    :param x0: Condición inicial para x
    :param y0: Condición inicial para y
    :return: Soluciones exacta y aproximada
    """
    condiciones_iniciales = np.array(condiciones_iniciales)
    sol_exacta = odeint(mod, condiciones_iniciales, t, args=args)
    x_exacta, y_exacta = sol_exacta.T
    sol_rk4 = runge_kutta_4(mod, condiciones_iniciales, t, *args)
    x_rk4, y_rk4 = sol_rk4.T
    return [x_exacta, y_exacta, x_rk4, y_rk4]
