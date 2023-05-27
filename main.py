import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

def secante(f, x0, x1, tol, max_iter):
    """
    Encuentra la raíz de una función f(x) utilizando el método de la secante.
        Argumentos:
            f (función): La función a la cual se le quiere encontrar una raíz.
            x0 (float): Primera aproximación.
            x1 (float): Segunda aproximación.
            tol (float): Tolerancia absoluta para la convergencia.
            max_iter (int): Número máximo de iteraciones permitidas.
        Retorna:
            raiz: La aproximación a la raíz de la función f(x).
            num_iter: El número de iteraciones realizadas.
            ABS: Error tolerancia absoluta al finalizar las iteraciones.
            ABS_values: array de error.
    """
    i = 0
    ABS_values = []
    while i < max_iter:
        # Calcula la siguiente aproximación utilizando el método de la secante
        x2 = x1 - (f(x1) * (x1 - x0)) / (f(x1) - f(x0))

        # Definir la iteracion
        i += 1

        # Verifica la convergencia
        ABS = abs((x2 - x0) / x2)
        ABS_values.append(ABS)
        if ABS < tol:
            return x2, i, ABS, ABS_values
            # Si la condicion se cumple terminar la iteracion
            i = max_iter

        # Actualiza las aproximaciones
        x0 = x1
        x1 = x2

    return 0 , i , 0 , 0

def convertir_funcion(funcion):
    funcion = funcion.replace('^', '**')  # Reemplazar '^' con '**' para denotar la potencia en Python
    funcion = funcion.replace(' ', '')    # Eliminar espacios en blanco
    funcion = funcion.replace(',', '.')    # Reemplazar la coma "," por punto "."
    return funcion

def convertir_Pfloat(p):
    p = p.replace(',', '.')    # Reemplazar la coma "," por punto "."
    return p

def grafica(num_iter, ABS_values):
    iteraciones = list(range(2, num_iter + 1)) # Excluye la posición 0 del array
    ABS_values = ABS_values[1:] # Excluye el primer valor de ABS_values
    plt.figure()
    plt.plot(iteraciones, ABS_values, marker='o')
    plt.xlabel("Número de iteraciones")
    plt.ylabel("Error %")
    plt.title("Convergencia del método de la secante (ERROR)")
    plt.grid(True)
    plt.tight_layout()
    
    # Obtener el administrador de la figura actual
    manager = plt.get_current_fig_manager()
     # Cambiar el nombre de la figura
    manager.set_window_title("Convergencia del método")
    # Cambiar el logotipo de la figura
    manager.window.iconbitmap('icono.ico') 
    # Obtener el ancho y la altura de la pantalla
    screen_width, screen_height = manager.window.winfo_screenwidth(), manager.window.winfo_screenheight()
    # Establecer la posición de la ventana de la figura en la parte superior derecha
    manager.window.wm_geometry(f"+{screen_width-700}+0")  # Ajustar el ancho de la ventana según sea necesario
    
    plt.show()


def calcular_raiz():
    error = True
    try:
        if plt.get_fignums():  # Verificar si hay una gráfica abierta
            plt.close()  # Cerrar la gráfica

        # Obtener la función ingresada por el usuario
        func_str = funcion_entry.get()
        func = lambda x: eval(convertir_funcion(func_str))

        # Obtener los demás datos ingresados por el usuario
        X0 = float(convertir_Pfloat(x0_entry.get()))
        X1 = float(convertir_Pfloat(x1_entry.get()))
        error = float(convertir_Pfloat(error_entry.get()))
        inter = 100
        # Calcular la raíz utilizando el método de la secante
        raiz, num_iter, ABS, ABS_values = secante(func, X0, X1, error, inter)

        if num_iter < inter:
            # Mostrar el resultado en la interfaz gráfica
            raiz_label.config(text="La raíz es: {:.10f}".format(raiz))
            iter_label.config(text="Número de iteraciones: {}".format(num_iter))
            error_label.config(text="Error: {:.10f}%".format(ABS * 100))

            # Graficar los valores de ABS en función del número de iteraciones
            if num_iter > 1:
                grafica_label.config(text="")
                grafica(num_iter, ABS_values)
            else:
                grafica_label.config(text="El numero de iteraciones no son suficiente para generar la grafica")
        else:
            raiz_label.config(text="")
            iter_label.config(text="")
            error_label.config(text="")
            grafica_label.config(text="")
            messagebox.showerror("Error de iteración","Iteraciones máximas permitidas, El método no converge")        
        
    except Exception as e:
        raiz_label.config(text="")
        iter_label.config(text="")
        error_label.config(text="")
        grafica_label.config(text="")
        messagebox.showerror("❌ Error de parámetro 🔑","🚫 Campos vacíos o parámetros erróneos 🔢,🔍👀 Verifica cuál de los campos 📋 no cumplen con los parámetros ❌ ")
        print(str(e))
        
# Crear la ventana de la interfaz gráfica
window = tk.Tk()
window.title("Método de Secante")
window.geometry("500x400")

# Establecer el ícono de la ventana
window.iconbitmap('icono.ico')

# Crear los elementos de la interfaz gráfica
funcion_label = tk.Label(window, text="Ingresa la función f(x):")
funcion_label.pack()
funcion_entry = tk.Entry(window)
funcion_entry.pack()

x0_label = tk.Label(window, text="Ingresa X0:")
x0_label.pack()
x0_entry = tk.Entry(window)
x0_entry.pack()

x1_label = tk.Label(window, text="Ingresa X1:")
x1_label.pack()
x1_entry = tk.Entry(window)
x1_entry.pack()

error_label = tk.Label(window, text="Ingresa el error permisible:")
error_label.pack()
error_entry = tk.Entry(window)
error_entry.pack()

calcular_button = tk.Button(window, text="Calcular", command=calcular_raiz)
calcular_button.pack()

raiz_label = tk.Label(window, text="")
raiz_label.pack()

iter_label = tk.Label(window, text="")
iter_label.pack()

error_label = tk.Label(window, text="")
error_label.pack()

grafica_label = tk.Label(window, text="", foreground="red")
grafica_label.pack()

def on_closing():
    if plt.get_fignums():  # Verificar si hay una gráfica abierta
        plt.close()  # Cerrar la gráfica
    window.destroy()  # Cerrar la ventana principal


# Configurar la función que se ejecutará al cerrar la ventana principal
window.protocol("WM_DELETE_WINDOW", on_closing)

# Iniciar la interfaz gráfica
window.mainloop()
