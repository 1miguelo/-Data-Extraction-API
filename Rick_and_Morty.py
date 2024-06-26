import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
import os

# Función para verificar las credenciales
def validar_credenciales(usuario, contrasena):
    ruta_carpeta = os.path.dirname(os.path.abspath(__file__))  # Obtener la carpeta del script actual
    ruta_archivo = os.path.join(ruta_carpeta, "usuarios.txt")
    try:
        with open(ruta_archivo, "r") as file:
            for line in file:
                usuario_archivo, contrasena_archivo = line.strip().split(":")
                if usuario == usuario_archivo and contrasena == contrasena_archivo:
                    return True
    except FileNotFoundError:
        messagebox.showerror("Error", "El archivo 'usuarios.txt' no se ha encontrado.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al leer el archivo 'usuarios.txt': {e}")
    return False

# Función para mostrar la imagen de Rick y Morty
def mostrar_imagen_rick_morty():
    ruta_imagen_rick_morty = os.path.join(os.path.dirname(os.path.abspath(__file__)), "RickAndMorty.jpg")
    imagen_rick_morty = Image.open(ruta_imagen_rick_morty)
    imagen_rick_morty = imagen_rick_morty.resize((600, 400), Image.ANTIALIAS)  # Redimensionar la imagen al doble de tamaño
    foto_rick_morty = ImageTk.PhotoImage(imagen_rick_morty)
    etiqueta_imagen_rick_morty = tk.Label(marco_login, image=foto_rick_morty)
    etiqueta_imagen_rick_morty.image = foto_rick_morty
    etiqueta_imagen_rick_morty.pack()

# Función para hacer login
def iniciar_sesion():
    usuario = entrada_usuario.get()
    contrasena = entrada_contrasena.get()
    
    if validar_credenciales(usuario, contrasena):
        messagebox.showinfo("Inicio de sesión", "¡Inicio de sesión exitoso!")
        mostrar_personajes()
    else:
        messagebox.showerror("Inicio de sesión", "Usuario o contraseña incorrectos")

# Función para mostrar la información de los personajes
def mostrar_personajes():
    marco_login.pack_forget()  # Esconder la pantalla de login

    canvas = tk.Canvas(raiz)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(raiz, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    marco_personajes = tk.Frame(canvas)
    canvas.create_window((0, 0), window=marco_personajes, anchor=tk.NW)

    num_personajes = int(entrada_num_personajes.get())
    if num_personajes < 1 or num_personajes > 32:
        messagebox.showerror("Error", "El número de personajes debe estar entre 1 y 32")
        return
    
    respuesta = requests.get(f'https://rickandmortyapi.com/api/character/1,{",".join(str(i) for i in range(2, num_personajes + 1))}')
    if respuesta.status_code == 200:
        personajes = respuesta.json()
        
        fila = 0
        columna = 0

        for personaje in personajes:
            nombre = personaje['name']
            especie = personaje['species']
            genero = personaje['gender']
            url_imagen = personaje['image']
            
            # Traducción de especie y género
            especie_es = "Especie: " + ("Humano" if especie == "Human" else "Humanoide" if especie == "Humanoid" else "Desconocido" if especie == "unknown" else especie)
            genero_es = "Género: " + ("Masculino" if genero == "Male" else "Femenino" if genero == "Female" else genero)
            
            # Descargar la imagen
            respuesta_imagen = requests.get(url_imagen)
            datos_imagen = respuesta_imagen.content
            imagen = Image.open(BytesIO(datos_imagen))
            imagen = imagen.resize((100, 100), Image.ANTIALIAS)  # Redimensionar la imagen
            foto = ImageTk.PhotoImage(imagen)
            
            # Crear widgets para mostrar la información
            marco = tk.Frame(marco_personajes, borderwidth=2, relief="groove")
            etiqueta_nombre = tk.Label(marco, text=f"Nombre: {nombre}")
            etiqueta_especie = tk.Label(marco, text=especie_es)
            etiqueta_genero = tk.Label(marco, text=genero_es)
            etiqueta_imagen = tk.Label(marco, image=foto)
            etiqueta_imagen.image = foto  # Necesario para evitar que la imagen sea recolectada por el garbage collector
            
            etiqueta_nombre.grid(row=0, column=0, padx=5, pady=5)
            etiqueta_especie.grid(row=1, column=0, padx=5, pady=5)
            etiqueta_genero.grid(row=2, column=0, padx=5, pady=5)
            etiqueta_imagen.grid(row=3, column=0, padx=5, pady=5)

            marco.grid(row=fila, column=columna, padx=5, pady=5)
            
            columna += 1
            if columna == 8:
                columna = 0
                fila += 1

        # Botón para salir del programa
        def salir():
            raiz.destroy()

        boton_salir = tk.Button(marco_personajes, text="Salir", command=salir)
        boton_salir.grid(row=fila, column=0, columnspan=8, pady=10)

    else:
        messagebox.showerror("Error", "No se pudo obtener la información de los personajes")

# Crear la ventana principal
raiz = tk.Tk()
raiz.title("Rick y Morty INFO")

# Frame para el login
marco_login = tk.Frame(raiz)
marco_login.pack(fill='both', expand=True)

# Mostrar la imagen de Rick y Morty en la parte superior
mostrar_imagen_rick_morty()

tk.Label(marco_login, text="Usuario").pack(pady=5)
entrada_usuario = tk.Entry(marco_login)
entrada_usuario.pack(pady=5)

tk.Label(marco_login, text="Contraseña").pack(pady=5)
entrada_contrasena = tk.Entry(marco_login, show="*")
entrada_contrasena.pack(pady=5)

tk.Label(marco_login, text="Número de personajes").pack(pady=5)
entrada_num_personajes = tk.Entry(marco_login)
entrada_num_personajes.insert(0, "32")  # Valor por defecto
entrada_num_personajes.pack(pady=5)

boton_iniciar_sesion = tk.Button(marco_login, text="Iniciar sesión", command=iniciar_sesion)
boton_iniciar_sesion.pack(pady=20)

raiz.mainloop()
