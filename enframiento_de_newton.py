import tkinter as tk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# --- LÓGICA DEL MODELO (Ecuación Diferencial) ---
def calcular_enfriamiento(T_ambiente, T_inicial, k, tiempo_max):
    """
    Solución analítica de la Ley de Enfriamiento de Newton:
    dT/dt = -k * (T - Ta)
    Solución: T(t) = Ta + (To - Ta) * e^(-k*t)
    """
    t = np.linspace(0, tiempo_max, 100) # Rango de tiempo
    T = T_ambiente + (T_inicial - T_ambiente) * np.exp(-k * t)
    return t, T

# --- INTERFAZ GRÁFICA ---
def graficar():
    try:
        # 1. Obtener y validar datos
        Ta = float(entry_ta.get())
        To = float(entry_to.get())
        k = float(entry_k.get())
        t_max = float(entry_time.get())

        if k <= 0 or t_max <= 0:
            messagebox.showwarning("Advertencia", "La constante 'k' y el tiempo deben ser mayores a 0.")
            return

        # 2. Calcular modelo
        t, T = calcular_enfriamiento(Ta, To, k, t_max)

        # 3. Limpiar gráfica anterior
        ax.clear()

        # 4. Graficar
        ax.plot(t, T, 'b-', linewidth=2, label=f'k={k}')
        ax.axhline(y=Ta, color='r', linestyle='--', alpha=0.5, label=f'Temp. Ambiente ({Ta}°)')
        
        # Decoración de la gráfica
        ax.set_title("Ley de Enfriamiento de Newton", fontsize=12)
        ax.set_xlabel("Tiempo (t)", fontsize=10)
        ax.set_ylabel("Temperatura (T)", fontsize=10)
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.legend()

        # Actualizar canvas
        canvas.draw()

    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos.")

def limpiar():
    entry_ta.delete(0, tk.END)
    entry_to.delete(0, tk.END)
    entry_k.delete(0, tk.END)
    entry_time.delete(0, tk.END)
    ax.clear()
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.set_title("Esperando datos...")
    canvas.draw()

# --- CONFIGURACIÓN VENTANA ---
root = tk.Tk()
root.title("Simulador: Ley de Enfriamiento de Newton")
root.geometry("900x600")
root.configure(bg='white') # Fondo blanco como se pidió

# Título y Explicación
frame_info = tk.Frame(root, bg='white')
frame_info.pack(pady=10)

lbl_titulo = tk.Label(frame_info, text="Modelo de Enfriamiento de Newton", 
                      font=("Arial", 18, "bold"), bg='white', fg='#333')
lbl_titulo.pack()

lbl_ecuacion = tk.Label(frame_info, text="Ecuación Diferencial: dT/dt = -k(T - Ta)", 
                        font=("Consolas", 14), bg='#f0f0f0', fg='blue', padx=10, pady=5)
lbl_ecuacion.pack(pady=5)

# Contenedor Principal
frame_main = tk.Frame(root, bg='white')
frame_main.pack(fill='both', expand=True, padx=20, pady=10)

# Panel Izquierdo (Entradas)
frame_inputs = tk.Frame(frame_main, bg='white', bd=2, relief='groove')
frame_inputs.pack(side='left', fill='y', padx=10, pady=10, anchor='n')

tk.Label(frame_inputs, text="Parámetros", font=("Arial", 12, "bold"), bg='white').pack(pady=10)

# Campos de entrada
def crear_input(texto, var_name):
    frame = tk.Frame(frame_inputs, bg='white')
    frame.pack(pady=5, padx=10, fill='x')
    tk.Label(frame, text=texto, bg='white', width=18, anchor='w').pack(side='left')
    entry = tk.Entry(frame, width=10, justify='center')
    entry.pack(side='right')
    return entry

entry_ta = crear_input("Temp. Ambiente (Ta):", "ta")
entry_to = crear_input("Temp. Inicial (To):", "to")
entry_k = crear_input("Constante (k):", "k")
entry_time = crear_input("Tiempo Máximo:", "tm")

# Valores de ejemplo por defecto
entry_ta.insert(0, "")
entry_to.insert(0, "")
entry_k.insert(0, "")
entry_time.insert(0, "")

# Botones
btn_frame = tk.Frame(frame_inputs, bg='white')
btn_frame.pack(pady=20, fill='x', padx=10)

btn_calc = tk.Button(btn_frame, text="CALCULAR Y GRAFICAR", command=graficar, 
                     bg='#4CAF50', fg='white', font=("Arial", 10, "bold"), cursor='hand2')
btn_calc.pack(fill='x', pady=5)

btn_clean = tk.Button(btn_frame, text="Limpiar", command=limpiar, 
                      bg='#f44336', fg='white', cursor='hand2')
btn_clean.pack(fill='x', pady=5)

# Panel Derecho (Gráfica)
frame_grafica = tk.Frame(frame_main, bg='white')
frame_grafica.pack(side='right', fill='both', expand=True, padx=10, pady=10)

# Configuración Matplotlib
fig = Figure(figsize=(5, 4), dpi=100, facecolor='white')
ax = fig.add_subplot(111)
ax.set_title("Esperando datos...")
ax.grid(True, linestyle=':', alpha=0.6)

canvas = FigureCanvasTkAgg(fig, master=frame_grafica)
canvas.draw()
canvas.get_tk_widget().pack(fill='both', expand=True)

# Firma
tk.Label(root, text="Desarrollado para Actividad 7 - Ecuaciones Diferenciales", 
         bg='white', fg='#888', font=("Arial", 8)).pack(side='bottom', pady=5)

root.mainloop()