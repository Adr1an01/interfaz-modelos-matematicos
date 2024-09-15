from abc import ABC, abstractmethod

class ModelosMatematicos(ABC):
    @abstractmethod
    def modelo_exponencial(N0, r, t):
        pass
    
    @abstractmethod
    def modelo_riñon_artificial(r_, a, v, V):
        pass
    