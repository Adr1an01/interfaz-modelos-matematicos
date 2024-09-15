import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from Implement import ImplementacionModelos
from Matematicas import solve

class InterfazUno:
    def __init__(self, parent):
        self.parent = parent

        self.main_frame = tk.Frame(self.parent)
        self.main_frame.pack(fill="both", expand=True)
        
        self.panel1 = tk.Frame(self.main_frame, bg="#D3D3D3", width=300)
        self.panel1.pack(side="left", fill="y")
        self.combo_box = ttk.Combobox(self.panel1, values=["Modelo riñon artificial", "Opción 2", "Opción 3"], state="readonly")
        self.combo_box.pack(padx=10, pady=10, fill="x")
        
        self.dynamic_frame = tk.Frame(self.panel1, bg="#D3D3D3")
        self.dynamic_frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.combo_box.bind("<<ComboboxSelected>>", self.update_label)
        
        self.panel2 = tk.Frame(self.main_frame)
        self.panel2.pack(side="right", fill="both", expand=True)
        self.notebook = ttk.Notebook(self.panel2)
        self.tab1 = tk.Frame(self.notebook)
        self.tab2 = tk.Frame(self.notebook)
        self.tab3 = tk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Gráfica en el tiempo")
        self.notebook.add(self.tab2, text="Diagrama de fase")
        self.notebook.add(self.tab3, text="Análisis Numérico")
        self.notebook.pack(expand=True, fill="both")
        
        self.treeview = ttk.Treeview(self.tab3, show='headings')
        self.treeview.pack(expand=True, fill="both")
    def plot_graph(self, t, x_exacta, y_exacta, x_rk4, y_rk4):
        for widget in self.tab1.winfo_children():
            widget.destroy()
        fig = Figure(figsize=(10, 6), dpi=100)
        ax = fig.add_subplot(111)        
        ax.plot(t, x_exacta, 'b-', label='x_exacta (odeint)')
        ax.plot(t, y_exacta, 'g-', label='y_exacta (odeint)')
        ax.plot(t, x_rk4, 'r--', label='x_rk4 (RK4)')
        ax.plot(t, y_rk4, 'm--', label='y_rk4 (RK4)')        
        ax.set_title('Gráfica en el Tiempo')
        ax.set_xlabel('Tiempo')
        ax.set_ylabel('Valor')
        ax.legend()        
        canvas = FigureCanvasTkAgg(fig, master=self.tab1)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill='both', padx=10, pady=10)

    def show_phase_plane(self, model_func, *model_params):
        for widget in self.tab2.winfo_children():
            widget.destroy()

        x = np.linspace(-1, 1, 20)
        y = np.linspace(-1, 1, 20)
        X, Y = np.meshgrid(x, y)
        
        DX, DY = np.array([model_func([x, y], *model_params) for x, y in zip(np.ravel(X), np.ravel(Y))]).T
        DX = DX.reshape(X.shape)
        DY = DY.reshape(Y.shape)

        fig = Figure(figsize=(10, 8), dpi=100)
        ax = fig.add_subplot(111)
        ax.streamplot(X, Y, DX, DY, color='blue')
        ax.quiver(X, Y, DX, DY, color='red', alpha=0.3) 
        ax.set_title('Plano fase')
        ax.set_xlabel('Concentración de impurezas en la sangre (x)')
        ax.set_ylabel('Concentración de impurezas en el líquido de diálisis (y)')

        canvas = FigureCanvasTkAgg(fig, master=self.tab2)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill='both', padx=10, pady=10)

    def clear_tabs(self):
        for widget in self.tab1.winfo_children():
            widget.destroy()
        
        
        for widget in self.tab2.winfo_children():
            widget.destroy()
        
        
        self.treeview.delete(*self.treeview.get_children())

    def update_label(self, event):
        self.clear_panel()
        self.clear_tabs() 
        selected_option = self.combo_box.get()

        if selected_option == "Modelo riñon artificial":
            tk.Label(self.dynamic_frame, text="Eficacia del líquido de diálisis (a):", bg="#D3D3D3").pack(padx=10, pady=5, anchor="w")
            self.a_entry_value = tk.StringVar()
            a_entry = tk.Entry(self.dynamic_frame, textvariable=self.a_entry_value)
            a_entry.pack(padx=10, pady=5, anchor="w")

            tk.Label(self.dynamic_frame, text="Tasas de flujo volumétrico de la sangre (v):", bg="#D3D3D3").pack(padx=10, pady=5, anchor="w")
            self.v_entry_value = tk.StringVar()
            v_entry = tk.Entry(self.dynamic_frame, textvariable=self.v_entry_value)
            v_entry.pack(padx=10, pady=5, anchor="w")
            
            tk.Label(self.dynamic_frame, text="Tasas de flujo del líquido de diálisis (V):", bg="#D3D3D3").pack(padx=10, pady=5, anchor="w")
            self.V_entry_value = tk.StringVar()
            V_entry = tk.Entry(self.dynamic_frame, textvariable=self.V_entry_value)
            V_entry.pack(padx=10, pady=5, anchor="w")

            tk.Label(self.dynamic_frame, text="Condición inicial (x0) :", bg="#D3D3D3").pack(padx=10, pady=5, anchor="w")
            self.x0_entry_value = tk.StringVar()
            x0_entry = tk.Entry(self.dynamic_frame, textvariable=self.x0_entry_value)
            x0_entry.pack(padx=10, pady=5, anchor="w")

            tk.Label(self.dynamic_frame, text="Condición inicial (y0) :", bg="#D3D3D3").pack(padx=10, pady=5, anchor="w")
            self.y0_entry_value = tk.StringVar()
            y0_entry = tk.Entry(self.dynamic_frame, textvariable=self.y0_entry_value)
            y0_entry.pack(padx=10, pady=5, anchor="w")

            tk.Label(self.dynamic_frame, text="Número de puntos en el intervalo de tiempo:", bg="#D3D3D3").pack(padx=10, pady=5, anchor="w")
            self.t_puntos_entry_value = tk.StringVar()
            t_puntos_entry = tk.Entry(self.dynamic_frame, textvariable=self.t_puntos_entry_value)
            t_puntos_entry.pack(padx=10, pady=5, anchor="w")

            tk.Label(self.dynamic_frame, text="Tiempo final:", bg="#D3D3D3").pack(padx=10, pady=5, anchor="w")
            self.t_entry_value = tk.StringVar()
            t_entry = tk.Entry(self.dynamic_frame, textvariable=self.t_entry_value)
            t_entry.pack(padx=10, pady=5, anchor="w")

            calculate_button = tk.Button(self.dynamic_frame, text="Calcular", command=self.on_calculate)
            calculate_button.pack(pady=10)
        elif selected_option =="Opción 2":
            print('aquí implementar otra opcion')
        
    def clear_panel(self):
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()
    def on_calculate(self):
        try:
            a = float(self.a_entry_value.get())
            v = float(self.v_entry_value.get())
            V = float(self.V_entry_value.get())
            t_ = float(self.t_entry_value.get())
            x0_ = float(self.x0_entry_value.get())
            y0_ = float(self.y0_entry_value.get())
            
            t_puntos = int(self.t_puntos_entry_value.get())
            
            def modelo_riñon_artificial_wrapper(r_, t, a, v, V):
                modelo = ImplementacionModelos()
                return modelo.modelo_riñon_artificial(r_, a, v, V)
            
            condiciones_iniciales = [x0_, y0_]
            t = np.linspace(0, t_, t_puntos)
            soluciones = solve(modelo_riñon_artificial_wrapper, condiciones_iniciales, t, a, v, V)
            df = pd.DataFrame({
                't' : t,
                'x_exacta': soluciones[0],
                'y_exacta': soluciones[1],
                'x_rk4': soluciones[2],
                'y_rk4': soluciones[3]
            })
            self.update_treeview(df)
            x_exacta, y_exacta, x_rk4, y_rk4 = soluciones
            self.plot_graph(t, x_exacta, y_exacta, x_rk4, y_rk4)                    
            
            def modelo_riñon_artificial_phase_plane(r_, a, v, V):
                modelo = ImplementacionModelos()
                return modelo.modelo_riñon_artificial(r_, a, v, V)
            
            self.show_phase_plane(modelo_riñon_artificial_phase_plane, a, v, V)
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese números válidos en todos los campos.")

    def update_treeview(self, df):
        
        self.treeview.delete(*self.treeview.get_children())
        
        
        self.treeview["columns"] = list(df.columns)
        for col in df.columns:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, width=100, anchor="center")
        
        
        for _, row in df.iterrows():
            rounded_values = [f"{value:.4f}" if isinstance(value, float) else value for value in row]
            self.treeview.insert("", "end", values=rounded_values)
        

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazUno(root)
    root.mainloop()
