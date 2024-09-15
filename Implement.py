import numpy as np
from ModMat import ModelosMatematicos

class ImplementacionModelos(ModelosMatematicos):
    @staticmethod
    def modelo_exponencial(N0, r, t):
        """
        Modelo exponencial de crecimiento poblacional.
        N(t) = N0 * exp(r * t)
        :param N0: Población inicial
        :param r: Tasa de crecimiento
        :param t: Tiempo
        :return: Población en el tiempo t
        """
        return N0 * np.exp(r * t)
    
    @staticmethod
    def modelo_riñon_artificial(r_, a, v, V):
        """
        Modelo del riñón artificial.
        :param r_: Estado del sistema (x, y)
        :param a: Constante que mide la eficacia del líquido de diálisis
        :param v: Tasas de flujo volumétrico de la sangre
        :param V: Tasas de flujo del líquido de diálisis
        :return: Derivadas dx_dt y dy_dt
        """
        x, y = r_
        dx_dt = a / v * (y - x)
        dy_dt = a / V *(x - y)
        return np.array([dx_dt, dy_dt])
    
    
#a = 0.5  # Ejemplo de valor para la constante de eficacia
#v = 1.0  # Ejemplo de valor para la tasa de flujo volumétrico de la sangre
#V = 0.8
#r_ = np.array([1.0, 0.5]) 
#res = ImplementacionModelos.modelo_riñon_artificial(r_, a, v, V)
#print(res)
