import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk  
from interfazUno import InterfazUno
from interfazDos import InterfazDos

class Principal:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicación Principal")
        self.root.geometry("900x600")

        try:
            self.bg_image1 = Image.open("logo.png")
            photo = ImageTk.PhotoImage(self.bg_image1)
            self.root.iconphoto(True, photo)
        except Exception as e:
            print(f"No se pudo cargar el ícono: {e}")

        # Configurar el color de fondo
        self.root.configure(bg='gray')
        
        # Crear la barra de menú
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        # Crear un menú "Menú"
        self.interface_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Menú", menu=self.interface_menu)
        self.interface_menu.add_command(label="Mostrar Interfaz Uno", command=self.show_interfaz_uno)
        self.interface_menu.add_command(label="Mostrar Interfaz Dos", command=self.show_interfaz_dos)
        
        # Añadir el menú "Ayuda"
        self.about_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Ayuda", menu=self.about_menu)
        self.about_menu.add_command(label="Acerca de", command=self.show_about)

        # Frame principal para contener las interfaces
        self.main_frame = tk.Frame(self.root, bg='gray')
        self.main_frame.pack(fill="both", expand=True)

        # Agregar el instructivo en la parte restante
        self.add_instruction()

        # Agregar la imagen de fondo después de que la ventana ha sido cargada
        self.root.update_idletasks()
        self.add_background_image()

        # Inicialmente, no mostramos ninguna interfaz
        self.current_interface = None

    def show_interfaz_uno(self):
        self.clear_main_frame()
        self.current_interface = InterfazUno(self.main_frame)

    def show_interfaz_dos(self):
        self.clear_main_frame()
        self.current_interface = InterfazDos(self.main_frame)

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_about(self):
        messagebox.showinfo("Acerca de", "Proyecto para el curso de Modelos de la Ciencia")

    def add_background_image(self):
        # Cargar la imagen de fondo
        self.bg_image = Image.open("fondo.jpg")

        # Redimensionar la imagen
        self.bg_image = self.bg_image.resize((600, 600), Image.LANCZOS)
        self.bg_image_tk = ImageTk.PhotoImage(self.bg_image)

        # Crear un Label para mostrar la imagen de fondo en la parte derecha
        self.bg_label = tk.Label(self.main_frame, image=self.bg_image_tk)
        self.bg_label.place(x=300, y=0, width=600, height=600)  # Colocar en la parte derecha de la ventana

    def add_instruction(self):
        # Agregar el instructivo en la parte izquierda de la ventana
        instructive_text = "Seleccionar Menú:\n\n" \
                           "Interfaz Uno: Modelos matemáticos\n" \
                           "Interfaz Dos: Cadenas de Markov"
        
        # Crear un Label para el instructivo con un ancho fijo de 300 píxeles
        self.instruction_label = tk.Label(self.main_frame, text=instructive_text, bg='#2e2e2e', fg='white', font=('Arial', 12, 'bold'), padx=20, pady=20, anchor='nw', borderwidth=2, relief='solid')
        self.instruction_label.place(x=0, y=0, width=300, relheight=1)  # Ancho fijo de 300 píxeles

if __name__ == "__main__":
    root = tk.Tk()
    app = Principal(root)
    root.mainloop()
