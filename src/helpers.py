import re

def pedirRuta():
  # Pedir ruta del archivo por input
  pathFile = input('Ingrese la ruta del archivo a analizar: ')
  # Remover comillas
  pathClean = re.sub(
      r'\'|"',
      '',
      pathFile
  )
  return pathClean.strip()