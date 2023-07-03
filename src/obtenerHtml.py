import re

documentTitleExpr = r'<article>[\w\W]+?<title>([\w\W]+?)(?=<\/)'

sectionTitleExpr = r'<section>[\w\W]+?<title>([\w\W]+?)(?=<\/)'

paraExpr = r'<para>([\w\W]+?)(?=<\/)'
simparaExpr = r'<simpara>([\w\W]+?)(?=<\/)'

infoContentExpr = r'<info>([\w\W]*?)<\/info>'

importantExpr = r'<important>([\w\W]*?)<\/important>'

itemizedListExpr = r'<itemizedlist>([\w\W]*?)<\/itemizedlist>'
listItemExpr = r'<listitem>([\w\W]*?)<\/listitem>'

tagContentExpr = r'<([^>]+)>(.*?)<\/\1>'
innerTagsExpr = r'<(\w+)>([\w\W]*?)<\/\>'


tagExpr = r'<\/?[a-zA-Z]+\b[^>]*>'


def exportarHtml(fileContent, pathFile):  # Recibo el contenido del archivo y su path
  
    searchStr = '\\' if ("\\" in pathFile) else '/'  # Reviso si el archivo se encuentra en una ruta con barras diagonales invertidas (\) o barras diagonales (/)

    rawFileName = pathFile.split(searchStr)[-1]  # Obtengo el nombre del archivo sin la ruta
    fileName = rawFileName.split('.txt')[0]  # Obtengo el nombre del archivo sin la extensión
    
    contentArr = []  # Lista para almacenar el contenido del archivo HTML
    contentArr.append(
        f'''<!DOCTYPE html>\n<html>\n<head>\n\t<meta charset="utf-8">\n\t<title>{fileName}</title>\n</head>\n<body>'''
    )
    
 
    # Extraer información del canal
    cdocumentTitle = f'<H1>{re.findall(documentTitleExpr, fileContent)[0].strip()}</H1>'  # Busca y captura el título del Documento y lo envuelve en la etiqueta <h1>
    contentArr.extend([cdocumentTitle])  
        
    csectionsTitle = re.findall(sectionTitleExpr, fileContent)   # Busca y captura todos los titulos de secciones
    
    for section in csectionsTitle:
      csectionTitle = f'<H2>{section}</H2>'  # Busca y captura todos los titulos de secciones y lo envuelve en la etiqueta <h2>
      contentArr.extend([csectionTitle])  

    cInfo = re.findall(infoContentExpr, fileContent)  # DETECTO TODO EL CONTENIDO DEL INFO
    
    tagsIntoInfo = detectTagsIntoInfo(cInfo)  # Detecto cada tag dentro de info y lo devuelvo
    
    for tags in tagsIntoInfo:
      contentArr.extend([tags])   # Por cada tag de info correcto, lo anado al html de salida
      
    cImportant = re.findall(importantExpr, fileContent)
    tagsIntoImportant = detectTagsIntoImportant(cImportant)
    
    for tagsImpo in tagsIntoImportant:
      contentArr.extend([tagsImpo]) 
      
    citemizedlist = re.findall(itemizedListExpr, fileContent)
    
    tagsIntoIL = tagsIntoItemizedList(citemizedlist)
    
    for tags in tagsIntoIL:
      contentArr.extend([tags])
    
    
    
    # for important in cimportant:
    #   removido = f'<div style="background-color:red; color: white; font-size:8px;"> {removeTags(important)} </div>' 
    #   contentArr.extend([removido])  

    # cparas = re.findall(paraExpr, fileContent)

    # for para in cparas:
    #   cpara = f'<p>{para}</p>'
    #   contentArr.extend([cpara])  


    contentArr.append('\n</body>\n</html>')  # Agrega el cierre del archivo HTML
    
    
    
    with open(f'{fileName}.html', 'w', encoding='UTF8') as f:
      for line in contentArr:
        f.write(line)
    f.close()
    
def removeTags(match):
    content = match
    encontrado = re.findall(tagExpr, match)
    print(
          )
    
    # if encontrado != []:
    #   cparas = re.findall(paraExpr, match)
    #   for para in cparas:
    #     cpara = f'<p>{para}</p>'
    #     return [cpara] 
    
def detectTagsIntoInfo(match):
  tagsArray = []
  for content in match:
    detectados = re.findall(tagContentExpr, content) # POR CADA TAG, DEBO CONVERTIRLO A UN PARRAFO CON FONDO VERDE, LETRA DE COLOR BLANCO Y 8 PX
    for detectado in detectados:
      if(detectado[0] != 'title') and (detectado[0] != 'para') and (detectado[0] != 'simpara')  :
        tagsArray.append(f'<p style= background-color:green; color:white; font-size:8px >{detectado[1]}</p>')   # VER SI ES TITLE Y TRANSFORMARLO A H1, SI ES PARA, TRANSFORMARLO A PARA, SI ES SIMPARA, TRANSFORMARLO EN SIMPARA
  return tagsArray  

def detectTagsIntoImportant(match):
  tagsArray=[]
  tagsArray.append(f'<div style="background-color:red; color:white;">')
  for content in match:
    detectados = re.findall(tagContentExpr, content)
    for detectado in detectados:
      if(detectado[0] == 'para'):
        tagsArray.append(f'<p> {detectado[1]} </p>')
      elif(detectado[0] != 'title') and (detectado[0] != 'para') and (detectado[0] != 'simpara'):
        tagsArray.append(f'{detectado[1]}')
  tagsArray.append(f'</div>')
  return tagsArray


def tagsIntoItemizedList(match):
  tagsArray =[]
  tagsArray.append('<ul>')   
  for content in match:
    detectados = re.findall(listItemExpr, content)
    for detectado in detectados:
      tagsArray.append(f'<li> {detectado} </li> ')
  tagsArray.append('</ul>')
  return tagsArray
