# Main.py
from Auth import registrarusuario, iniciarsesion
from Pagos import registrarpago, mostrarpagos, generarreporte

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