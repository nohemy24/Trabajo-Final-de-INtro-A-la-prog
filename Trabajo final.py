from datetime import datetime
import pwinput
import re

# Archivos
USUARIOSFILE = "usuarios.txt"
PAGOSFILE = "pagos.txt"

# Funciones de archivo
def cargarusuarios():
    usuarios = {}
    try:
        with open(USUARIOSFILE, 'r') as file:
            for line in file:
                try:
                    usuario, contraseña, tipo = line.strip().split('|')
                    usuarios[usuario] = f"{contraseña}|{tipo}"
                except:
                    continue
    except FileNotFoundError:
        pass
    return usuarios

def cargarpagos():
    pagos = []
    try:
        with open(PAGOSFILE, 'r') as file:
            for line in file:
                try:
                    datos = line.strip().split('|')
                    pago = {
                        "usuario": datos[0],
                        "proveedor": datos[1],
                        "tipogasto": datos[2],
                        "monto": float(datos[3]),
                        "fechavencimiento": datos[4],
                        "frecuenciapago": datos[5],
                        "categoria": datos[6],
                        "formapago": datos[7],
                        "pagado": datos[8] == "True",
                        "fecharegistro": datos[9]
                    }
                    pagos.append(pago)
                except:
                    continue
    except FileNotFoundError:
        pass
    return pagos

def guardarusuarios(usuarios):
    with open(USUARIOSFILE, 'w') as file:
        for usuario, datos in usuarios.items():
            contraseña, tipo = datos.split('|')
            file.write(f"{usuario}|{contraseña}|{tipo}\n")

def guardarpagos(pagos):
    with open(PAGOSFILE, 'w') as file:
        for pago in pagos:
            linea = (
                f"{pago['usuario']}|{pago['proveedor']}|{pago['tipogasto']}|"
                f"{pago['monto']}|{pago['fechavencimiento']}|{pago['frecuenciapago']}|"
                f"{pago['categoria']}|{pago['formapago']}|{pago['pagado']}|{pago['fecharegistro']}\n"
            )
            file.write(linea)

# Funciones principales
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
        contraseña = pwinput.pwinput("Ingrese su contraseña, si es empresarial debe incluir letras, números y símbolos y ser de al menos 12 caracteres, de lo contrario mínimo 6 caracteres: ", mask="*").strip()
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

def registrarpago(usuario):
    pagos = cargarpagos()
    print("\n--- REGISTRO DE PAGO ---")

    proveedor = input("Nombre del proveedor: ").strip()
    tipogasto = input("Tipo de gasto: ").strip()

    while True:
        try:
            monto = float(input("Monto en córdobas: ").strip())
            if monto <= 0:
                print(" El monto debe ser mayor a 0.")
                continue
            break
        except ValueError:
            print(" Ingrese un valor numérico válido para el monto.")

    while True:
        fechavencimiento = input("Fecha de vencimiento (DD/MM/AAAA): ").strip()
        try:
            datetime.strptime(fechavencimiento, "%d/%m/%Y")
            break
        except ValueError:
            print(" Fecha inválida. Usa el formato DD/MM/AAAA.")

    frecuencias_validas = ["diario", "mensual", "trimestral", "anual"]
    while True:
        frecuenciapago = input("Frecuencia de pago (diario/mensual/trimestral/anual): ").strip().lower()
        if frecuenciapago in frecuencias_validas:
            break
        else:
            print(" Frecuencia no válida.")

    categorias_validas = ["Servicios", "Préstamos", "Nómina", "Otros"]
    while True:
        categoria = input("Categoría (Servicios/Préstamos/Nómina/Otros): ").strip()
        if categoria in categorias_validas:
            break
        else:
            print(" Categoría inválida.")

    formapago = input("Forma de pago: ").strip()

    nuevo_pago = {
        "usuario": usuario,
        "proveedor": proveedor,
        "tipogasto": tipogasto,
        "monto": monto,
        "fechavencimiento": fechavencimiento,
        "frecuenciapago": frecuenciapago,
        "categoria": categoria,
        "formapago": formapago,
        "pagado": False,
        "fecharegistro": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }

    pagos.append(nuevo_pago)
    guardarpagos(pagos)
    print(" Pago registrado exitosamente.\n")

def mostrarpagos(usuario):
    pagos = cargarpagos()
    print("\n--- TUS PAGOS PENDIENTES ---")
    hoy = datetime.now()
    encontrados = False

    for pago in pagos:
        if pago["usuario"] == usuario and not pago["pagado"]:
            try:
                vencimiento = datetime.strptime(pago["fechavencimiento"], "%d/%m/%Y")
                diasrestantes = (vencimiento - hoy).days
                print(f"\nProveedor: {pago['proveedor']}")
                print(f"Tipo: {pago['tipogasto']} | Monto: {pago['monto']:.2f} Córdobas")
                print(f"Vence: {pago['fechavencimiento']} ({diasrestantes} días)")
                print(f"Frecuencia: {pago['frecuenciapago']} | Categoría: {pago['categoria']}")
                print(f"Forma de pago: {pago['formapago']}")
                if diasrestantes <= 10:
                    print(" ¡PAGO PRÓXIMO A VENCER! ")
                encontrados = True
            except:
                continue
    if not encontrados:
        print("No hay pagos pendientes.\n")

def generarreporte(usuario):
    pagos = cargarpagos()
    print("\n--- REPORTE DE PAGOS EMPRESARIALES ---")
    total = 0
    for pago in pagos:
        if pago["usuario"] == usuario:
            estado = "Pagado" if pago["pagado"] else "Pendiente"
            print(f"{pago['fecharegistro']} | {pago['proveedor']} | {pago['monto']:.2f} C$ | {estado}")
            total += pago["monto"]
    print(f"\nTotal registrado: {total:.2f} Córdobas\n")

def menuprincipal(usuario, tipo):
    while True:
        print(f"\n=== MENÚ PRINCIPAL === (Usuario: {usuario} | Tipo: {tipo})")
        print("1. Registrar nuevo pago")
        print("2. Mostrar pagos pendientes")
        if tipo == "empresarial":
            print("3. Generar reporte de pagos")
            print("4. Cerrar sesión")
        else:
            print("3. Cerrar sesión")

        opcion = input("Seleccione opción: ").strip()

        if opcion == "1":
            registrarpago(usuario)
        elif opcion == "2":
            mostrarpagos(usuario)
        elif opcion == "3" and tipo == "empresarial":
            generarreporte(usuario)
        elif (opcion == "3" and tipo == "personal") or (opcion == "4" and tipo == "empresarial"):
            print("Sesión finalizada.\n")
            break
        else:
            print(" Opción no válida.")

def main():
    while True:
        print("\n=== Sistema de Gestión de Pagos ===")
        print("1. Registrar nueva cuenta")
        print("2. Iniciar sesión")
        print("3. Salir")

        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            registrarusuario()
        elif opcion == "2":
            usuario, tipo = iniciarsesion()
            if usuario:
                menuprincipal(usuario, tipo)
        elif opcion == "3":
            print("Gracias por utilizar el sistema.")
            break
        else:
            print(" Opción inválida.")

if __name__ == "__main__":
    main()