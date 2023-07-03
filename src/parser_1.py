from logicaMenu import logicaMenu
from helpers import pedirRuta
from obtenerHtml import exportarHtml

import ply.yacc as yacc
import lexer
from lexer import tokens

from importlib import reload

exportarTxt = list()
contadorErrores = 0


# ---- PRODUCCIONES DE LA GRAMATICA ---- #
# Mayusculas = No Terminales
# Minusculas = Terminales (etiquetas/tokens)

def p_SIGMA(p): # Simbolo distinguido
    '''SIGMA : doctype ARTICLE
    '''
    print("Ejecución completa!")
    exportarTxt.append(['Prod. SIGMA -->', p.slice])


def p_ARTICLE(p):
    '''ARTICLE : article INFO TITLE CONT_A_S cierreArticle
				| article INFO TITLE CONT_A_S SECTIONS cierreArticle
				| article TITLE CONT_A_S cierreArticle
                | article TITLE CONT_A_S SECTIONS cierreArticle
                | article INFO CONT_A_S cierreArticle
                | article INFO CONT_A_S SECTIONS cierreArticle
                | article CONT_A_S cierreArticle
    '''
    exportarTxt.append(['Prod. ARTICLE -->', p.slice])
    
def p_INFO(p):
    '''INFO : info CONT_INFO cierreInfo
    '''
    exportarTxt.append(['Prod. INFO -->', p.slice])

def p_CONT_INFO(p):
    '''CONT_INFO : ELEM_INFO CONT_INFO
				| ELEM_INFO
    '''
    exportarTxt.append(['Prod. CONT_INFO -->', p.slice])
    
def p_ELEM_INFO(p):
    '''ELEM_INFO : MEDIA_OBJECT
				| ABSTRACT
                | ADDRESS
                | AUTHOR
                | DATE
                | COPYRIGHT
                | TITLE
    '''
    exportarTxt.append(['Prod. ELEM_INFO -->', p.slice])

def p_SECTION(p):
    '''SECTION : section CONT_A_S cierreSection
				| section CONT_A_S SECTIONS cierreSection
				| section INFO CONT_A_S cierreSection
                | section INFO CONT_A_S SECTIONS cierreSection
                | section TITLE CONT_A_S cierreSection
                | section TITLE CONT_A_S SECTIONS cierreSection
                | section INFO TITLE CONT_A_S cierreSection
                | section INFO TITLE CONT_A_S SECTIONS cierreSection
                | section TITLE cierreSection
    '''
    exportarTxt.append(['Prod. SECTION -->', p.slice])

def p_SECTIONS(p):
    '''SECTIONS : SECTION 
				| SECTION SECTIONS
                | SIMPLE_SEC
                | SIMPLE_SEC SECTIONS
    '''
    exportarTxt.append(['Prod. SECTIONS -->', p.slice])

def p_CONT_A_S(p):
    '''CONT_A_S : CONT_1
				| CONT_1 CONT_A_S
                | SECTION
    '''
    exportarTxt.append(['Prod. CONT_A_S -->', p.slice])

def p_CONT_1(p):
    '''CONT_1 :   ITEMIZED_LIST
				| IMPORTANT
                | PARA
                | SIMPARA
                | ADDRESS
                | MEDIA_OBJECT
                | INFORMAL_TABLE
                | COMMENT
                | ABSTRACT
    '''
    exportarTxt.append(['Prod. CONT_1 -->', p.slice])

def p_SIMPLE_SEC(p):
    '''SIMPLE_SEC : simpleSection CONT_SS cierreSimpleSection
				| simpleSection INFO CONT_SS cierreSimpleSection
                | simpleSection TITLE CONT_SS cierreSimpleSection
                | simpleSection INFO TITLE CONT_SS cierreSimpleSection
    '''
    exportarTxt.append(['Prod. SIMPLE_SEC -->', p.slice])

def p_CONT_SS(p):
    '''CONT_SS : CONT_1
				| CONT_1 CONT_SS
    '''
    exportarTxt.append(['Prod. CONT_SS -->', p.slice])

def p_ABSTRACT(p):
    '''ABSTRACT : abstract TITLE cierreAbstract
				| abstract TITLE PARAS cierreAbstract
    '''
    exportarTxt.append(['Prod. ABSTRACT -->', p.slice])

def p_TITLE(p):
    '''TITLE : title CONT_TITLE cierreTitle
    '''
    exportarTxt.append(['Prod. TITLE -->', p.slice])

def p_CONT_TITLE(p):
    '''CONT_TITLE : ELEM_TITLE
				| ELEM_TITLE CONT_TITLE
    '''
    exportarTxt.append(['Prod. CONT_TITLE -->', p.slice])

def p_ELEM_TITLE(p):
    '''ELEM_TITLE : contenido_texto
				| EMPHASIS
                | LINK
                | EMAIL
    '''
    exportarTxt.append(['Prod. ELEM_TITLE -->', p.slice])

def p_PARAS(p):
    '''PARAS : PARA
				| SIMPARA
                | PARA PARAS
                | SIMPARA PARAS
    '''
    exportarTxt.append(['Prod. PARAS -->', p.slice])

def p_PARA(p):
    '''PARA : para CONT_PARA cierrePara
    '''
    exportarTxt.append(['Prod. PARA -->', p.slice])

def p_CONT_PARA(p):
    '''CONT_PARA : ELEM_PARA
				| ELEM_PARA CONT_PARA
    '''
    exportarTxt.append(['Prod. CONT_PARA -->', p.slice])

def p_ELEM_PARA(p):
    '''ELEM_PARA : contenido_texto
				| EMPHASIS
                | LINK
                | EMAIL
                | AUTHOR
                | COMMENT
                | ITEMIZED_LIST
                | IMPORTANT
                | ADDRESS
                | MEDIA_OBJECT
                | INFORMAL_TABLE
    '''
    exportarTxt.append(['Prod. ELEM_PARA -->', p.slice])

def p_ITEMIZED_LIST(p):
    '''ITEMIZED_LIST : itemizedlist LIST_ITEM cierreItemizedlist
    '''
    exportarTxt.append(['Prod. ITEMIZED_LIST -->', p.slice])

def p_MEDIAO_BJECT(p):
    '''MEDIA_OBJECT : mediaObject INFO CONT_MEDIA_OBJECT cierreMediaObject
				| mediaObject CONT_MEDIA_OBJECT cierreMediaObject
    '''
    exportarTxt.append(['Prod. MEDIA_OBJECT -->', p.slice])

def p_CONT_MEDIA_OBJECT(p):
    '''CONT_MEDIA_OBJECT : IMAGE_OBJECT
				| VIDEO_OBJECT
                | IMAGE_OBJECT MEDIA_OBJECT
                | VIDEO_OBJECT MEDIA_OBJECT
    '''
    exportarTxt.append(['Prod. CONT_MEDIA_OBJECT -->', p.slice])

def p_IMAGE_OBJECT(p):
    '''IMAGE_OBJECT : imageObject INFO imageData cierreImageObject
				| imageObject imageData cierreImageObject
    '''
    exportarTxt.append(['Prod. IMAGE_OBJECT -->', p.slice])

def p_VIDEO_OBJECT(p):
    '''VIDEO_OBJECT : videoObject INFO imageData cierreVideoObject
				| videoObject videoData cierreVideoObject
    '''
    exportarTxt.append(['Prod. VIDEO_OBJECT -->', p.slice])

def p_LIST_ITEM(p):
    '''LIST_ITEM : listItem CONT_ITEM cierreListItem
                |  LIST_ITEM listItem CONT_ITEM cierreListItem
    '''
    exportarTxt.append(['Prod. LIST_ITEM -->', p.slice])

def p_CONT_ITEM(p):
    '''CONT_ITEM : CONT_1
				| CONT_1 CONT_ITEM
    '''
    exportarTxt.append(['Prod. CONT_ITEM -->', p.slice])

def p_AUTHOR(p):
    '''AUTHOR : author CONT_AUTHOR cierreAuthor
    '''
    exportarTxt.append(['Prod. AUTHOR -->', p.slice])

def p_CONT_AUTHOR(p):
    '''CONT_AUTHOR : FIRSTNAME
				| SURNAME
                | EMAIL
                | FIRSTNAME SURNAME
                | FIRSTNAME EMAIL
                | SURNAME EMAIL
                | FIRSTNAME SURNAME EMAIL
    '''
    exportarTxt.append(['Prod. CONT_AUTHOR -->', p.slice])

def p_ADDRESS(p):
    '''ADDRESS : address cierreAddress
                | address CONT_ADDRESS cierreAddress
    '''
    exportarTxt.append(['Prod. ADDRESS -->', p.slice])

def p_CONT_ADDRESS(p):
    '''CONT_ADDRESS : ELEM_ADDRESS
				| ELEM_ADDRESS CONT_ADDRESS
    '''
    exportarTxt.append(['Prod. CONT_ADDRESS -->', p.slice])

def p_ELEM_ADDRESS(p):
    '''ELEM_ADDRESS : STREET
				| CITY
                | STATE
                | PHONE
                | EMAIL
                | contenido_texto
    '''
    exportarTxt.append(['Prod. ELEM_ADDRESS -->', p.slice])

def p_COPYRIGHT(p):
    '''COPYRIGHT : copyright YEAR cierreCopyright
				| copyright YEAR HOLDER cierreCopyright 
    '''
    exportarTxt.append(['Prod. COPYRIGHT -->', p.slice])

def p_SIMPARA(p):
    '''SIMPARA : simpara CONT_SECL cierreSimpara
    '''
    exportarTxt.append(['Prod. SIMPARA -->', p.slice])

def p_EMPHASIS(p):
    '''EMPHASIS : emphasis CONT_SECL cierreEmphasis
    '''
    exportarTxt.append(['Prod. EMPHASIS -->', p.slice])

def p_COMMENT(p):
    '''COMMENT : comment CONT_SECL cierreComment
    '''
    exportarTxt.append(['Prod. COMMENT -->', p.slice])

def p_LINK(p):
    '''LINK : link CONT_SECL cierreLink
    '''
    exportarTxt.append(['Prod. LINK -->', p.slice])

def p_CONT_SECL(p):
    '''CONT_SECL : CONT_2
				| CONT_2 CONT_SECL
    '''
    exportarTxt.append(['Prod. CONT_SECL -->', p.slice])
    
def p_CONT_2(p):
    '''CONT_2 : contenido_texto
				| EMPHASIS
                | LINK
                | EMAIL
                | AUTHOR
                | COMMENT
    '''
    exportarTxt.append(['Prod. CONT_2 -->', p.slice])
    
def p_IMPORTANT(p):
    '''IMPORTANT : important TITLE CONT_IMPORTANT cierreImportant
				| important CONT_IMPORTANT cierreImportant
    '''
    exportarTxt.append(['Prod. IMPORTANT -->', p.slice])

def p_CONT_IMPORTANT(p):
    '''CONT_IMPORTANT : CONT_1
				| CONT_1 CONT_IMPORTANT
    '''
    exportarTxt.append(['Prod. CONT_IMPORTANT -->', p.slice])

def p_CONT_VAR(p):
    '''CONT_VAR : CONT_3
				| CONT_3 CONT_VAR
    '''
    exportarTxt.append(['Prod. CONT_VAR -->', p.slice])

def p_CONT_3(p):
    '''CONT_3 : contenido_texto
				| LINK
                | EMPHASIS
                | COMMENT
    '''
    exportarTxt.append(['Prod. CONT_3 -->', p.slice])

def p_FIRSTNAME(p):
    '''FIRSTNAME : firstname CONT_VAR cierreFirstname
    '''
    exportarTxt.append(['Prod. FIRSTNAME -->', p.slice])

def p_SURNAME(p):
    '''SURNAME : surname CONT_VAR cierreSurname
    '''
    exportarTxt.append(['Prod. SURNAME -->', p.slice])

def p_STREET(p):
    '''STREET : street CONT_VAR cierreStreet
    '''
    exportarTxt.append(['Prod. STREET -->', p.slice])

def p_CITY(p):
    '''CITY : city CONT_VAR cierreCity
    '''
    exportarTxt.append(['Prod. CITY -->', p.slice])

def p_STATE(p):
    '''STATE : state CONT_VAR cierreState
    '''
    exportarTxt.append(['Prod. STATE -->', p.slice])

def p_PHONE(p):
    '''PHONE : phone CONT_VAR cierrePhone
    '''
    exportarTxt.append(['Prod. PHONE -->', p.slice])

def p_EMAIL(p):
    '''EMAIL : email CONT_VAR cierreEmail
    '''
    exportarTxt.append(['Prod. EMAIL -->', p.slice])

def p_DATE(p):
    '''DATE : date CONT_VAR cierreDate
    '''
    exportarTxt.append(['Prod. DATE -->', p.slice])
    
def p_YEAR(p):
    '''YEAR : year CONT_VAR cierreYear
    '''
    exportarTxt.append(['Prod. YEAR -->', p.slice])

def p_HOLDER(p):
    '''HOLDER : holder CONT_VAR cierreHolder
    '''
    exportarTxt.append(['Prod. HOLDER -->', p.slice])

def p_INFORMAL_TABLE(p):
    '''INFORMAL_TABLE : informalTable TABLE_MEDIA cierreInformalTable
				| informalTable TABLE_GROUP cierreInformalTable
    '''
    exportarTxt.append(['Prof. INFORMAL_TABLE -->', p.slice])

def p_TABLE_MEDIA(p):
    '''TABLE_MEDIA : MEDIA_OBJECT
				| MEDIA_OBJECT TABLE_MEDIA
    '''
    exportarTxt.append(['Prod. TABLE_MEDIA -->', p.slice])

def p_TABLE_GROUP(p):
    '''TABLE_GROUP : TGROUP
				| TGROUP TABLE_GROUP
    '''
    exportarTxt.append(['Prod. TABLE_GROUP -->', p.slice])

def p_TGROUP(p):
    '''TGROUP : tgroup THEAD TFOOT TBODY cierreTgroup
				| tgroup THEAD TBODY cierreTgroup
                | tgroup TFOOT TBODY cierreTgroup
                | tgroup TBODY cierreTgroup
    '''
    exportarTxt.append(['Prod. TGROUP -->', p.slice])

def p_CONT_T(p):
    '''CONT_T : ROW
				| ROW CONT_T
    '''
    exportarTxt.append(['Prod. CONT_T -->', p.slice])

def p_THEAD(p):
    '''THEAD : thead CONT_T cierreThead
    '''
    exportarTxt.append(['Prod. THEAD -->', p.slice])

def p_TFOOT(p):
    '''TFOOT : tfoot CONT_T cierreTfoot
    '''
    exportarTxt.append(['Prod. TFOOT -->', p.slice])
    
def p_TBODY(p):
    '''TBODY : tbody CONT_T cierreTbody
    '''
    exportarTxt.append(['Prod. TBODY -->', p.slice])

def p_ROW(p):
    '''ROW : row CONT_ROW cierreRow
    '''
    exportarTxt.append(['Prod. ROW -->', p.slice])

def p_CONT_ROW(p):
    '''CONT_ROW : ENTRY
				| ENTRY CONT_ROW
                | ENTRYTBL
				| ENTRYTBL CONT_ROW
    '''
    exportarTxt.append(['Prod. CONT_ROW_1 -->', p.slice])

def p_ENTRY(p):
    '''ENTRY : entry CONT_ENTRY cierreEntry
    '''
    exportarTxt.append(['Prod. ENTRY -->', p.slice])

def p_ENTRYTBL(p):
    '''ENTRYTBL : entrytbl THEAD TBODY cierreEntrytbl
				| entrytbl TBODY cierreEntrytbl
    '''
    exportarTxt.append(['Prod. ENTRYTBL -->', p.slice])

def p_CONT_ENTRY(p):
    '''CONT_ENTRY : contenido_texto
				| contenido_texto CONT_ENTRY
                | ITEMIZED_LIST
                | ITEMIZED_LIST CONT_ENTRY
                | IMPORTANT
                | IMPORTANT CONT_ENTRY
                | PARA
                | PARA CONT_ENTRY
                | SIMPARA
                | SIMPARA CONT_ENTRY
                | COMMENT
                | COMMENT CONT_ENTRY
                | ABSTRACT
                | ABSTRACT CONT_ENTRY
                | MEDIA_OBJECT
                | MEDIA_OBJECT CONT_ENTRY
    '''
    exportarTxt.append(['Prod. CONT_ENTRY -->', p.slice])


def p_error(p):
    # p regresa como un objeto del Lexer.
    # p.__dict__ -> ver propiedades del objeto.
    global contadorErrores
    if (p):
        print(f'Error en el parser --> Tipo: {p.type} | Valor: {p.value}')
        print('Error sintáctico en la LINEA:', p.lineno)
        exportarTxt.append(['!!! Error parser -->', p])
        
    contadorErrores += 1

parser = yacc.yacc()  # Ignorar warnings.
# error log=yacc.NullLogger()

opcionesMenu = {
    1: 'Analizar texto desde un archivo, indicando su ruta.',
    2: 'Escanear texto línea por línea (escribiendo en terminal).',
    3: 'Salir.',
}

def analizarPorRuta():
    cleanPath = pedirRuta()
    global contadorErrores
    # Ejecución "analisis de archivo de texto"
    try:
        file = open(cleanPath, "r", encoding='utf8')
        strings = file.read()
        file.close()
        result = parser.parse(strings)
        try:
            with open(f'producciones-analizadas.txt', 'w', encoding='UTF8') as f:
                f.write('Producciones analizadas por el parser:\n====================\n')
                contador = 0
                for line in exportarTxt:
                    contador += 1
                    f.write(f'{contador}) {line[0]} | {line[1]}\n')
                    f.write('---------------\n')
                f.write('====================\n')
                f.write(f'Total de tokens analizados: {contador}.\n')
            f.close()
        except:
            print('Error creando logs')
        if contadorErrores > 0:
            print('(⨉) Ocurrió un error sintáctico.')
            # Resetear contador
            contadorErrores = 0
            reload(lexer)
        else:
            print('✅ El archivo es sintacticamente correcto!')
            # Ejecutar exportacion de html
            exportarHtml(strings, cleanPath)
            print('(✅) Sintácticamente correcto.')
            print('(!) Se exportó un .txt con las producciones analizadas.')
    except IOError:
        print('Ocurrió un error leyendo archivo:', cleanPath)


def analizarPorLinea():
    # Ejecución "normal"
    print('Para interrumpir la ejecucion: [ctrl] + [C] | Para volver al menu principal: _salir')
    while True:
        s = input('>> ')
        if s == '_salir':
            break
        result = parser.parse(s)
        print(result)


if __name__ == "__main__":
    logicaMenu(
        'Parser',
        opcionesMenu,
        analizarPorRuta,
        analizarPorLinea,
    )
