# Archivos.py
from datetime import datetime

USUARIOSFILE = "usuarios.txt"
PAGOSFILE = "pagos.txt"

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

def guardarusuarios(usuarios):
    with open(USUARIOSFILE, 'w') as file:
        for usuario, datos in usuarios.items():
            contraseña, tipo = datos.split('|')
            file.write(f"{usuario}|{contraseña}|{tipo}\n")

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

def guardarpagos(pagos):
    with open(PAGOSFILE, 'w') as file:
        for pago in pagos:
            linea = (
                f"{pago['usuario']}|{pago['proveedor']}|{pago['tipogasto']}|"
                f"{pago['monto']}|{pago['fechavencimiento']}|{pago['frecuenciapago']}|"
                f"{pago['categoria']}|{pago['formapago']}|{pago['pagado']}|{pago['fecharegistro']}\n"
            )
            file.write(linea)