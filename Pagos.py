# Pagos.py
from datetime import datetime
from Archivos import cargarpagos, guardarpagos

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
            print(f"{pago['fecharegistro']} | {pago['proveedor']} | {pago['monto']:.2f} Córdobas | {estado}")
            total += pago["monto"]
    print(f"\nTotal registrado: {total:.2f} Córdobas\n")