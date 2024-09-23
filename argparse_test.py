import argparse

# Definimos las funciones que queremos llamar
def funcion_a():
    print("Función A llamada.")

def funcion_b():
    print("Función B llamada.")

# Crear el objeto ArgumentParser principal
parser = argparse.ArgumentParser(description='Ejemplo de argparse con subcomandos.')

# Crear subparsers
subparsers = parser.add_subparsers(dest='comando', help='Comandos disponibles')

# Subparser para la función A
parser_a = subparsers.add_parser('-a', help='Llama a la función A')
parser_a.set_defaults(func=funcion_a)

# Subparser para la función B
parser_b = subparsers.add_parser('-b', help='Llama a la función B')
parser_b.set_defaults(func=funcion_b)

# Analizar los argumentos
args = parser.parse_args()

# Llamar a la función correspondiente

if hasattr(args, 'func'):
    args.func()
else:
    parser.print_help()
