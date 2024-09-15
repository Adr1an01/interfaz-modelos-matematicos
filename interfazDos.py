import tkinter as tk
from tkinter import messagebox
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class InterfazDos:
    def __init__(self, parent):
        self.parent = parent
        self.child_windows = []  # Para rastrear las ventanas hijas
        # Crear un marco para los paneles izquierdo y derecho
        self.main_frame = tk.Frame(self.parent)
        self.main_frame.pack(fill="both", expand=True)

        # Crear panel izquierdo para ingreso de datos
        self.left_panel = tk.Frame(self.main_frame)
        self.left_panel.pack(side="left", fill="y", padx=10, pady=10)

        # Crear panel derecho para mostrar la matriz u otros datos
        self.right_panel = tk.Frame(self.main_frame)
        self.right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Etiqueta y entrada para la cantidad de estados en el panel izquierdo
        self.label_states = tk.Label(self.left_panel, text="Cantidad de estados:", font=("Arial", 14))
        self.label_states.grid(row=0, column=0, pady=10, sticky="w")
        
        self.entry_states = tk.Entry(self.left_panel, font=("Arial", 14))
        self.entry_states.grid(row=1, column=0, pady=10, sticky="w")
        
        # Botón para enviar la cantidad de estados en el panel izquierdo
        self.submit_button = tk.Button(self.left_panel, text="Enviar", command=self.submit_states, font=("Arial", 14))
        self.submit_button.grid(row=2, column=0, pady=20)

    def on_closing(self):
        # Cerrar todas las ventanas hijas
        for window in self.child_windows:
            window.destroy()
        # Destruir la ventana principal
        self.parent.destroy()

    def submit_states(self):
        # Obtener la cantidad de estados ingresada
        num_states = self.entry_states.get()

        try:
            num_states = int(num_states)
            if num_states <= 0:
                raise ValueError

            # Crear una nueva ventana para ingresar los datos de la matriz
            self.create_matrix_entry_window(num_states)
        except ValueError:
            # Mostrar un popup de error si la entrada no es válida
            messagebox.showerror("Error", "Por favor, ingrese un número entero positivo.")

    def create_matrix_entry_window(self, num_states):
        matrix_window = tk.Toplevel(self.parent)
        self.child_windows.append(matrix_window)  # Agregar a la lista de ventanas hijas
        matrix_window.title("Ingresar Datos de la Matriz de Transición")

        # Crear un marco en la nueva ventana para los campos de entrada
        matrix_frame = tk.Frame(matrix_window)
        matrix_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Etiqueta en la nueva ventana
        label = tk.Label(matrix_frame, text=f"Ingrese datos para la matriz de transición ({num_states}x{num_states}):", font=("Arial", 14))
        label.grid(row=0, column=0, columnspan=num_states, pady=10)

        # Crear una lista para las entradas
        self.entries = []

        # Crear etiquetas y campos de entrada para la matriz
        for i in range(num_states):
            for j in range(num_states):
                entry = tk.Entry(matrix_frame, width=5, font=("Arial", 12))
                entry.grid(row=i+1, column=j, padx=5, pady=5)
                if len(self.entries) <= i:
                    self.entries.append([])
                self.entries[i].append(entry)

        # Botón para enviar los datos
        submit_button = tk.Button(matrix_frame, text="Enviar Datos", command=self.submit_matrix_data, font=("Arial", 14))
        submit_button.grid(row=num_states+1, column=0, columnspan=num_states, pady=20)

    def submit_matrix_data(self):
        # Obtener y validar los datos ingresados en la matriz
        try:
            matrix_data = []
            for row_entries in self.entries:
                row_data = []
                for entry in row_entries:
                    try:
                        value = float(entry.get())
                        if value < 0:
                            raise ValueError("Los valores deben ser no negativos.")
                        row_data.append(value)
                    except ValueError:
                        raise ValueError("Por favor, ingrese solo números válidos.")
                matrix_data.append(row_data)

            # Verificar que las columnas sumen exactamente 1
            num_states = len(matrix_data)
            for j in range(num_states):
                column_sum = sum(matrix_data[i][j] for i in range(num_states))
                if not (0.99 <= column_sum <= 1.01):  # Usar un rango para permitir pequeñas imprecisiones numéricas
                    raise ValueError(f"La columna {j+1} no suma exactamente 1. La suma es {column_sum:.2f}")

            # Calcular los estados
            states = [f'E{i+1}' for i in range(num_states)]
            
            # Limpiar el panel derecho antes de dibujar el nuevo gráfico
            for widget in self.right_panel.winfo_children():
                widget.destroy()

            # Dibujar el diagrama de estado
            self.draw_markov_chain(matrix_data, states)

        except ValueError as e:
            # Mostrar mensaje de error si las columnas no suman 1 o hay otros problemas
            messagebox.showerror("Error", str(e))

    def draw_markov_chain(self, transition_matrix, states):
        # Crear un grafo dirigido
        G = nx.DiGraph()
        # Agregar nodos
        for state in states:
            G.add_node(state)

        # Agregar aristas con probabilidades
        num_states = len(states)
        for i in range(num_states):
            for j in range(num_states):
                prob = transition_matrix[i][j]
                if prob > 0:
                    G.add_edge(states[i], states[j], weight=prob, label=f'{prob:.2f}')

        # Crear una figura y un eje para la visualización
        fig, ax = plt.subplots(figsize=(6, 6))
        pos = nx.spring_layout(G, k=0.5, iterations=50)  # layout for better visualization
        edge_labels = nx.get_edge_attributes(G, 'label')
        
        # Dibujar nodos con colores
        node_colors = ['skyblue' if i % 2 == 0 else 'lightgreen' for i in range(len(states))]
        nx.draw_networkx_nodes(G, pos, node_size=700, node_color=node_colors, edgecolors='black')
        
        # Dibujar aristas con flechas más gruesas
        nx.draw_networkx_edges(G, pos, arrows=True, arrowstyle='-|>', arrowsize=20, edge_color='black', width=2, connectionstyle='arc3,rad=0.1')
        
        # Dibujar etiquetas de aristas más resaltadas
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='blue', font_size=10, font_weight='bold', label_pos=0.3, bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
        
        # Dibujar etiquetas de nodos
        nx.draw_networkx_labels(G, pos, font_size=13, font_weight='bold')

        # Agregar el gráfico al panel derecho de la interfaz
        canvas = FigureCanvasTkAgg(fig, master=self.right_panel)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
