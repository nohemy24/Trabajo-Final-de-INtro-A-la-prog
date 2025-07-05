# Auth.py
import pwinput
import re
from Archivos import cargarusuarios, guardarusuarios

def registrarusuario():
    usuarios = cargarusuarios()
    print("\n--- REGISTRO DE USUARIO ---")

    while True:
        tipo = input("Tipo de cuenta (personal/empresarial): ").strip().lower()
        if tipo not in ["personal", "empresarial"]:
            print(" Tipo inválido. Elija 'personal' o 'empresarial'.")
        else:
            break

    while True:
        usuario = input("Ingrese su nombre de usuario: ").strip()
        if not usuario or any(c in usuario for c in "|/\\ "):
            print(" Usuario inválido. Evite espacios o caracteres especiales.")
            continue
        if usuario in usuarios:
            print(" Usuario ya existente. Inicie sesión.")
            return
        break

    while True:
        contraseña = pwinput.pwinput("Ingrese su contraseña: ", mask="*").strip()
        if tipo == "empresarial":
            if len(contraseña) < 12 or not re.search(r"[A-Za-z]", contraseña) or not re.search(r"\d", contraseña) or not re.search(r"[^\w\s]", contraseña):
                print(" La contraseña empresarial debe tener al menos 12 caracteres, incluir letras, números y símbolos.")
                continue
        else:
            if len(contraseña) < 6:
                print(" La contraseña debe tener al menos 6 caracteres.")
                continue
        break

    usuarios[usuario] = f"{contraseña}|{tipo}"
    guardarusuarios(usuarios)
    print(" Cuenta creada exitosamente.\n")

def iniciarsesion():
    usuarios = cargarusuarios()
    print("\n--- INICIO DE SESIÓN ---")

    for intento in range(1, 4):
        usuario = input("Usuario: ").strip()
        contraseña = pwinput.pwinput("Contraseña: ", mask="*").strip()

        if usuario in usuarios:
            datos = usuarios[usuario].split('|')
            if datos[0] == contraseña:
                print(" Acceso concedido.\n")
                return usuario, datos[1]
        faltan = 3 - intento
        print(" Usuario o contraseña incorrectos.")
        if faltan:
            print(f"Te quedan {faltan} intentos.\n")
        else:
            print(" Has agotado los 3 intentos. Acceso denegado.\n")
    return None, None