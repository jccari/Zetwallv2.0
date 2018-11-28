# !/usr/bin/env python
# -*- coding: utf-8 -*
import re

file = open('codigoFuente.txt', 'r')
data = file.readlines()
file.close()
listaTokens = []

# Comentarios
#-----------------------------------------------------------------------------
def removeComments(string):
    string = re.sub(re.compile("/\*.*?\*/",re.DOTALL ) ,"" ,string) # Remove all occurance streamed comments (/*COMMENT */) from string
    string = re.sub(re.compile("//.*?\n" ) ,"" ,string) # Remove all occurance singleline comments (//COMMENT\n ) from string
    if (re.compile("//*.*?\n"), "", string):
        string = re.sub(re.compile("//*.*?\n"), "#@", string)
    return string

# Preprocesamiento
#-----------------------------------------------------------------------------
def preprocesamiento():
    contador = 0
    linea = 1
    lexema = []
    numLinea = []
    token = []
    #print (data)
    for renglon in data:
        noCommetns = removeComments(renglon)
        #print(renglon)
        for palabra in  noCommetns.split(' '):
            subpalabras = list(filter(None, re.split(r"([+]|-|[*]|[/]|;|,|=|<=|>=|<|>|[(]|[)]|[[]|[]]|{|}|[\r])", palabra)))
            for delimitadores in subpalabras:
                if(delimitadores == "#@"):
                    print ("Error de comentario en la Linea: ",linea)
                    contador += 1
                    break
                contador += 1
                #print '%s) %s' % (str(contador), delimitadores)
                if (delimitadores == "true"):
                    lexema.append(delimitadores)
                    numLinea.append(linea)
                    token.append("TKN_True")
                elif (delimitadores == "false"):
                    lexema.append(delimitadores)
                    numLinea.append(linea)
                    token.append("TKN_False")
                elif (delimitadores != ('\n')):
                    if (delimitadores != ('\r')):
                        lexema.append(delimitadores)
                        numLinea.append(linea)
                        token.append("TKN_Undefined")

        linea = linea + 1

    for x in range(0, len(lexema)):
        lista = []
        lista.append(lexema[x])
        lista.append(numLinea[x])
        lista.append(token[x])
        listaTokens.append(lista)


# Diccionario Tokens
# -----------------------------------------------------------------------------
tknIdentificador = re.compile('[a-zA-Z]+[a-zA-Z1-9]*')
tknNumero = re.compile('[0-9]+')
tknFLoat = re.compile('[\d]+\.[\d]+')
tknString = re.compile('"[a-zA-Z]+[a-zA-Z1-9]*"')

# Autómatas
# LEXICAL ANALYZER
#-----------------------------------------------------------------------------
def tokens(listaTokens):
    for token in range(0,len(listaTokens)):
        if listaTokens[token][0] == "int":
            listaTokens[token][2] = "tkn_Int"
        elif listaTokens[token][0] == "float":
            listaTokens[token][2] = "tkn_Float"
        elif listaTokens[token][0] == "string":
            listaTokens[token][2] = "tkn_String"
        elif listaTokens[token][0] == "double":
            listaTokens[token][2] = "tkn_Double"
        elif listaTokens[token][0] == "bool":
            listaTokens[token][2] = "tkn_Bool"

        elif listaTokens[token][0] == "(":
            listaTokens[token][2] = "("
        elif listaTokens[token][0] == ")":
            listaTokens[token][2] = ")"
        elif listaTokens[token][0] == "{":
            listaTokens[token][2] = "{"
        elif listaTokens[token][0] == "}":
            listaTokens[token][2] = "}"
        elif listaTokens[token][0] == "[":
            listaTokens[token][2] = "["
        elif listaTokens[token][0] == "]":
            listaTokens[token][2] = "]"

        elif listaTokens[token][0] == ";":
            listaTokens[token][2] = ";"
        elif listaTokens[token][0] == ",":
            listaTokens[token][2] = ","
        elif listaTokens[token][0] == "=":
            listaTokens[token][2] = "="
        elif listaTokens[token][0] == "&&":
            listaTokens[token][2] = "tkn_And"
        elif listaTokens[token][0] == "||":
            listaTokens[token][2] = "tkn_Or"

        elif listaTokens[token][0] == "<":
            listaTokens[token][2] = "<"
        elif listaTokens[token][0] == ">":
            listaTokens[token][2] = ">"
        elif listaTokens[token][0] == "<=":
            listaTokens[token][2] = "<="
        elif listaTokens[token][0] == ">=":
            listaTokens[token][2] = ">="
        elif listaTokens[token][0] == "==":
            listaTokens[token][2] = "=="
        elif listaTokens[token][0] == "!=":
            listaTokens[token][2] = "!="
        elif listaTokens[token][0] == "+":
            listaTokens[token][2] = "+"
        elif listaTokens[token][0] == "-":
            listaTokens[token][2] = "-"
        elif listaTokens[token][0] == "*":
            listaTokens[token][2] = "*"
        elif listaTokens[token][0] == "/":
            listaTokens[token][2] = "/"
        elif listaTokens[token][0] == "%":
            listaTokens[token][2] = "%"

        elif listaTokens[token][0] == "main":
            listaTokens[token][2] = "tkn_Main"
        elif listaTokens[token][0] == "return":
            listaTokens[token][2] = "tkn_Return"

        elif listaTokens[token][0] == "while":
            listaTokens[token][2] = "tkn_While"
        elif listaTokens[token][0] == "if":
            listaTokens[token][2] = "tkn_If"
        elif listaTokens[token][0] == "else":
            listaTokens[token][2] = "tkn_Else"

        elif listaTokens[token][2] != "TKN_True" and listaTokens[token][2] != "TKN_False" and re.match(tknIdentificador, listaTokens[token][0]):
            m = re.match(tknIdentificador, listaTokens[token][0])
            print ("!! " + m.group(0))
            if len(m.group(0)) == len(listaTokens[token][0]):
                listaTokens[token][2] = "tkn_Identificador"
            else:
                print ("Error cadena no encontrada en la Linea: ", listaTokens[token][1])

        elif re.match(tknFLoat, str(listaTokens[token][0])):
            m = re.match(tknFLoat, listaTokens[token][0])
            listaTokens[token][2] = "tkn_Numero_Float"

        elif re.match(tknNumero, listaTokens[token][0]):
            m = re.match(tknNumero, listaTokens[token][0])
            if len(m.group(0)) == len(listaTokens[token][0]):
                listaTokens[token][2] = "tkn_Numero"
            else:
                print ("Error cadena no encontrada en la Linea: ", listaTokens[token][1])

        elif re.match(tknString, listaTokens[token][0]):
            m = re.match(tknString, listaTokens[token][0])
            listaTokens[token][2] = "tkn_String"
        else:
            print ("Error cadena no encontrada en la Linea: ",listaTokens[token][1])
            #Agregar a tabla de errores

# Tabla de Símbolos
#-----------------------------------------------------------------------------
tablaSimbolos = {}

# Hasta antes de Semántico, solo registra los identificadores en la TS.
def tablaSim(listaTokens):
    for id in range(0,len(listaTokens)):
        if listaTokens[id][2] == "tkn_Main":
            tablaSimbolos[listaTokens[id][0]] = {'Lexema': listaTokens[id][0],'Funcion':1,'Retorno':'','Linea': [listaTokens[id][1]]}
        elif listaTokens[id][2] == "tkn_Identificador" and listaTokens[id+1][2]=='[' and listaTokens[id+2][2]=='tkn_Numero' and listaTokens[id+3][2]==']':
            tam = int(listaTokens[id+2][0])
            if (tablaSimbolos.has_key(listaTokens[id][0]) == False):
                tablaSimbolos[listaTokens[id][0]] = {'Lexema': listaTokens[id][0], 'Valor': '','Tam': tam, 'Type':'','Funcion':0,'Linea': [listaTokens[id][1]]}
                for x in range(0,tam):
                    lexemaArray = listaTokens[id][0] + str(x)
                    tam = 0
                    tablaSimbolos[lexemaArray] = {'Lexema': lexemaArray, 'Valor': '', 'Tam': tam,'Type': '','Funcion':0, 'Linea': [listaTokens[id][1]]}
            #Else actualiza linea.
        elif listaTokens[id][2] == "tkn_Identificador":
            if (tablaSimbolos.has_key(listaTokens[id][0]) == False):
                tablaSimbolos[listaTokens[id][0]] = {'Lexema': listaTokens[id][0], 'Valor': '','Tam': '', 'Type':'','Funcion':0,'Linea': [listaTokens[id][1]]}
            else:
                # Si ya están indexados, se actualiza numLínea
                tablaSimbolos[listaTokens[id][0]]['Linea'].append(listaTokens[id][1])


def imprimirTS():
    for key in tablaSimbolos:
        print key, ":", tablaSimbolos[key]


# Imprimir
#-----------------------------------------------------------------------------
def imprimir(listaTokens):
    contador = 0
    for x in range(0, len(listaTokens)):
        contador += 1
        print '%s) %s' % (str(contador), listaTokens[x])
    print ("***********************************************")


# Tabla Sintáctica
#  -----------------------------------------------------------------------------

terminales =     { 'tkn_Include':1,	 'tkn_Int':2, 'tkn_Float':3,	'tkn_Double':4,	'tkn_Bool':5, 'tkn_String':6,	'tkn_Main':7,	'(':8,
                   ')':9,	'{':10,	'}':11,	'[':12,	']':13,	';':14, ',':15,	 '=':16,
                   'tkn_Return':17,	'tkn_Numero_Entero':18,	'tkn_And':19,	'tkn_Or':20,	'<':21,	'>':22,	'>=':23, '<=':24,
                   '==':25,	'!=':26,	 '+':27,	'-':28,	'*':29,	'/':30,	'%':31,	'tkn_Identificador':32,
                   'tkn_If':33,	'tkn_While':34,	'tkn_Else':35,	'tkn_Numero':36, '$':37,
                 }


noTerminales = {   'programa':1, 'lista_sentencias':2, 'def_basica':3, 'tipo_Dato':4, 'lista_def':5, 'lista_defp':6, 'def_espec':7, 'def_especp' :8,
                   'def_especpp':9, 'acceso_array':10, 'simple_asign':11, 'sentencia':12, 'sentenciap':13, 'WHILE':14, 'IF_ELSE':15, 'IF_ELSEp':16, 'IF':17,
                   'Wp':18, 'condicion':19, 'condicionp':20, 'condicion_logica':21, 'operadores_log':22, 'operadores':23, 'op_aditivos':24, 'op_multiplicativos':25,
                   'E':26, 'Ep':27, 'T':28, 'Tp':29, 'F':30, 'Fp':31,
               }



tablaSintactica = { 1:['tkn_Include', 'programa'],   2:['tkn_Int', 'tkn_Main','(',')','{', 'lista_sentencias' ,'tkn_Return' ,'tkn_Numero',';','}'],         3:[''],                                 4:[''],                                         5: [''],                                    6:[''],                                     7: [''],                    8:[''],                                                     9:[''],         10:[''],                                            11:[''],                            12:[''],                            13:[''],                14:[''],        15:[''],                     16:[''],                    17:[''],            18:[''],        19:[''],                                            20:[''],                            21:[''],            22:[''],            23:[''],            24:[''],            25:[''],            26:[''],            27:[''],                                28:[''],                            29:[''],                            30:[''],                                        31:[''],                    32:[''],                                                           33:[''],                                                 34:[''],                                        35:[''],                    36:[''],                                37:[''],
                    38:[''],                        39:['sentencia','lista_sentencias'],                                                                    40:['sentencia','lista_sentencias'],    41:['sentencia','lista_sentencias'],            42: ['sentencia','lista_sentencias'],       43:['sentencia','lista_sentencias'],        44: [''],                   45:['sentencia','lista_sentencias'],                        46:[''],        47:['sentencia','lista_sentencias'],                48:['empty'],                       49:[''],                            50:[''],                51:[''],        52:[''],                     53:[''],                    54:['empty'],       55:[''],        56:[''],                                            57:[''],                            58:[''],            59:[''],            60:[''],            61:[''],            62:[''],            63:[''],            64:[''],                                65:[''],                            66:[''],                            67:[''],                                        68:[''],                    69:['sentencia','lista_sentencias'],                               70:['sentencia','lista_sentencias'],                     71:['sentencia','lista_sentencias'],            72:[''],                    73:['sentencia','lista_sentencias'],    74:[''],
                    75:[''],                        76:['tipo_Dato','3','lista_def',';'],                                                                   77:['tipo_Dato','3','lista_def',';'],   78:['tipo_Dato','3','lista_def',';'],           79: ['tipo_Dato','3','lista_def',';'],      80:['tipo_Dato','lista_def',';'],           81: [''],                   82:[''],                                                    83:[''],        84:[''],                                            85:[''],                            86:[''],                            87:[''],                88:[''],        89:[''],                     90:[''],                    91:[''],            92:[''],        93:[''],                                            94:[''],                            95:[''],            96:[''],            97:[''],            98:[''],            99:[''],            100:[''],           101:[''],                               102:[''],                           103:[''],                           104:[''],                                       105:[''],                   106:[''],                                                          107:[''],                                                108:[''],                                       109:[''],                   110:[''],                               111:[''],
                    112:[''],                       113:['tkn_Int','4'],                                                                                    114:['tkn_Float','4'],                  115:['tkn_Double','4'],                         116: ['tkn_Bool','4'],                      117:['tkn_String','4'],                     118: [''],                  119:[''],                                                   120:[''],       121:[''],                                           122:[''],                           123:[''],                           124:[''],               125:[''],       126:[''],                    127:[''],                   128:[''],           129:[''],       130:[''],                                           131:[''],                           132:[''],           133:[''],           134:[''],           135:[''],           136:[''],           137:[''],           138:[''],                               139:[''],                           140:[''],                           141:[''],                                       142:[''],                   143:[''],                                                          144:[''],                                                145:[''],                                       146:[''],                   147:[''],                               148:[''],
                    149:[''],                       150:[''],                                                                                               151:[''],                               152:[''],                                       153: [''],                                  154:[''],                                   155: [''],                  156:[''],                                                   157:[''],       158:[''],                                           159:[''],                           160:[''],                           161:[''],               162:[''],       163:[''],                    164:[''],                   165:[''],           166:[''],       167:[''],                                           168:[''],                           169:[''],           170:[''],           171:[''],           172:[''],           173:[''],           174:[''],           175:[''],                               176:[''],                           177:[''],                           178:[''],                                       179:[''],                   180:['3','def_espec','3','lista_defp'],                            181:[''],                                                182:[''],                                       183:[''],                   184:[''],                               185:[''],
                    186:[''],                       187:[''],                                                                                               188: [''],                              189:[''],                                       190: [''],                                  191:[''],                                   192:[''],                   193:[''],                                                   194:[''],       195:[''],                                           196:[''],                           197:[''],                           198:[],                 199:['empty'],  200:[',','3','lista_def'],   201:[''],                   202:[''],           203:[''],       204:[''],                                           205:[''],                           206:[''],           207:[''],           208:[''],           209:[''],           210:[''],           211:[''],           212:[''],                               213:[''],                           214:[''],                           215:[''],                                       216:[''],                   217:[''],                                                          218:[''],                                                219:[''],                                       220:[''],                   221:[''],                               222:[''],



                    223:[''],                       224:[''],                                                                                               225:[''],                               226:[''],                                       227: [''],                                  228:[''],                                   229: [''],                  230:[''],                                                    231:[''],      232:[''],                                           233:[''],                           234:[''],                           235:[''],               236:[''],       237:[''],                    238:[''],                   239:[''],           240:[''],       241:[''],                                           242:[''],                           243:[''],           244:[''],           245:[''],           246:[''],           247:[''],           248:[''],           249:[''],                               250:[''],                           251:[''],                           252:[''],                                       253:[''],                   254:['tkn_Identificador','5','6','def_especp'],                    255:[''],                                               256:[''],                                       257:[''],                   258:[''],                               259:[''],
                    260:[''],                       261:[''],                                                                                               262:[],                                 263:[''],                                       264: [''],                                  265:[''],                                   266: [''],                  267:[''],                                                    268:[''],      269:[''],                                           270:[''],                           271:['6','acceso_array'],           272:[''],               273:['empty'],  274:['empty'],               275:['6','simple_asign'],   276:[''],           277:[''],       278:[''],                                           279:[''],                           280:[''],           281:[''],           282:[''],           283:[''],           284:[''],           285:[''],           286:[''],                               287:[''],                           288:[''],                           289:[''],                                       290:[''],                   291:[''],                                                          292:[''],                                               293:[''],                                       294:[''],                   295:[''],                               296:[''],
                    297:[''],                       298:[''],                                                                                               299:[''],                               300:[''],                                       301: [''],                                  302:[''],                                   303: [''],                  304:[''],                                                    305:[''],      306:[''],                                           307:[''],                           308:[''],                           309:[''],               310:['empty'],  311:['empty'],               312:['6','simple_asign'],   313:[''],           314:[''],       315:[''],                                           316:[''],                           317:[''],           318:[''],           319:[''],           320:[''],           321:[''],           322:[''],           323:[''],                               324:[''],                           325:[''],                           326:[''],                                       327:[''],                   328:[''],                                                           329:[''],                                               330:[''],                                       331:[''],                   332:[''],                               333:[''],

                    334:[''],                       335:[''],                                                                                               336:[''],                               337:[''],                                       338: [''],                                  339:[''],                                   340: [''],                  341:[''],                                                    342:[''],      343:[''],                                           344:[''],                           345:['[','tkn_Numero_Entero',']','7'],  346:[''],           347:[''],       348:[''],                    349:[''],                   350:[''],           351:[''],       352:[''],                                           353:[''],                           354:[''],           355:[''],           356:[''],           357:[''],           358:[''],           359:[''],           360:[''],                               361:[''],                           362:[''],                           363:[''],                                       364:[''],                   365:[''],                                                           366:[''],                                               367:[''],                                       368:[''],                   369:[''],                               370:[''],
                    371:[''],                       372:[''],                                                                                               373:[''],                               374:[''],                                       375: [''],                                  376:[''],                                   377: [''],                  378:[''],                                                    379:[''],      380:[''],                                           381:[''],                           382:[''],                           383:[''],               384:['empty'],  385:['empty'],               386:['=','E','1'],          387:[''],           388:[''],       389:[''],                                           390:[''],                           391:[''],           392:[''],           393:[''],           394:[''],           395:[''],           396:[''],           397:[''],                               398:[''],                           399:[''],                           400:[''],                                       401:[''],                   402:[''],                                                           403:[''],                                               404:[''],                                       405:[''],                   406:[''],                               407:[''],
                    408:[''],                       409:['def_basica'],                                                                                     410:['def_basica'],                     411:['def_basica'],                             412: ['def_basica'],                        413:['def_basica'],                         414: [''],                  415:['(','E',')',';'],                                       416:[''],      417:[''],                                           418:[''],                           419:[''],                           420:[''],               421:[''],       422:[''],                    423:[''],                   424:[''],           425:[''],       426:[''],                                           427:[''],                           428:[''],           429:[''],           430:[''],           431:[''],           432:[''],           433:[''],           434:[''],                               435:[''],                           436:[''],                           437:[''],                                       438:[''],                   439:['tkn_Identificador','sentenciap','1',';'],                     440:['IF_ELSE'],                                        441:['WHILE'],                                  442:[''],                   443:['tkn_Numero','Tp','Ep',';'],       444:[''],
                    445:[''],                       446:[''],                                                                                               447:[''],                               448:[''],                                       449: [''],                                  450:[''],                                   451: [''],                  452:[''],                                                    453:[''],      454:[''],                                           455:[''],                           456:['Fp','Tp','Ep'],               457:[''],               458:['empty'],  459:[''],                    460:['def_especp','2'],     461:[''],           462:[''],       463:[''],                                           464:[''],                           465:[''],           466:[''],           467:[''],           468:[''],           469:[''],           470:[''],           471:['operadores','=','E','2'],         472:['operadores','=','E','2'],     473:['operadores','=','E','2'],     474:['operadores','=','E','2'],                 475:['operadores','=','E','2'], 476:['def_especp','2'],                                         477:[''],                                               478:[''],                                       479:[''],                   480:[''],                               481:[''],
                    482:[''],                       483:[''],                                                                                               484:[''],                               485:[''],                                       486: [''],                                  487:[''],                                   488: [''],                  489:[''],                                                    490:[''],      491:[''],                                           492:[''],                           493:[''],                           494:[''],               495:[''],       496:[''],                    497:[''],                   498:[''],           499:[''],       500:[''],                                           501:[''],                           502:[''],           503:[''],           504:[''],           505:[''],           506:[''],           507:[''],           508:[''],                               509:[''],                           510:[''],                           511:[''],                                       512:[''],                   513:[''],                                                           514:[''],                                               515:['tkn_While','(','condicion',')','Wp'],     516:[''],                   517:[''],                               518:[''],
                    519:[''],                       520:[''],                                                                                               521:[''],                               522:[''],                                       523: [''],                                  524:[''],                                   525: [''],                  526:[''],                                                    527:[''],      528:[''],                                           529:[''],                           530:[''],                           531:[''],               532:[''],       533:[''],                    534:[''],                   535:[''],           536:[''],       537:[''],                                           538:[''],                           539:[''],           540:[''],           541:[''],           542:[''],           543:[''],           544:[''],           545:[''],                               546:[''],                           547:[''],                           548:[''],                                       549:[''],                   550:[''],                                                           551:['IF'],                                             552:[''],                                       553:[''],                   554:[''],                               555:[''], #551 FIX
                    556:[''],                       557:[''],                                                                                               558:[''],                               559:[''],                                       560: [''],                                  561:[''],                                   562: [''],                  563:[''],                                                    564:[''],      565:[''],                                           566:[''],                           567:[''],                           568:[''],               569:[''],       570:[''],                    571:[''],                   572:[''],           573:[''],       574:[''],                                           575:[''],                           576:[''],           577:[''],           578:[''],           579:[''],           580:[''],           581:[''],           582:[''],                               583:[''],                           584:[''],                           585:[''],                                       586:[''],                   587:[''],                                                           588:[''],                                               589:[''],                                       590:['tkn_Else','Wp'],      591:[''],                               592:[''],
                    593:[''],                       594:[''],                                                                                               595:[''],                               596:[''],                                       597: [''],                                  598:[''],                                   599: [''],                  600:[''],                                                    601:[''],      602:[''],                                           603:[''],                           604:[''],                           605:[''],               606:[''],       607:[''],                    608:[''],                   609:[''],           610:[''],       611:[''],                                           612:[''],                           613:[''],           614:[''],           615:[''],           616:[''],           617:[''],           618:[''],           619:[''],                               620:[''],                           621:[''],                           622:[''],                                       623:[''],                   624:[''],                                                           625:['tkn_If','(','condicion',')','Wp'],                626:[''],                                       627:[''],                   628:[''],                               629:[''],

                    630:[''],                       631:['sentencia'],                                                                                      632:['sentencia'],                      633:['sentencia'],                              634: ['sentencia'],                         635:['sentencia'],                          636: [''],                  637:['sentencia'],                                           638:[''],      639:['{','lista_sentencias','}'],                   640:[''],                           641:[''],                           642:[''],               643:[''],       644:[''],                    645:[''],                   646:[''],           647:[''],       648:[''],                                           649:[''],                           650:[''],           651:[''],           652:[''],           653:[''],           654:[''],           655:[''],           656:[''],                               657:[''],                           658:[''],                           659:[''],                                       660:[''],                   661:['sentencia'],                                                  662:[''],                                               663:[''],                                       664:[''],                   665:[''],                               666:[''],
                    667:[''],                       668:[''],                                                                                               669:[''],                               670:[''],                                       671: [''],                                  672:[''],                                   673: [''],                  674:[''],                                                    675:[''],      676:['condicion_logica','8','condicionp','8'],      677:[''],                           678:[''],                           679:[''],               680:[''],       681:[''],                    682:[''],                   683:[''],           684:[''],       685:[''],                                           686:[''],                           687:[''],           688:[''],           689:[''],           690:[''],           691:[''],           692:[''],           693:[''],                               694:[''],                           695:[''],                           696:[''],                                       697:[''],                   698:['condicion_logica','8','condicionp','8'],                      699:[''],                                               700:[''],                                       701:[''],                   702:['condicion_logica','8','condicionp','8'],  703:[''],
                    704:[''],                       705:[''],                                                                                               706:[''],                               707:[''],                                       708: [''],                                  709:[''],                                   710: [''],                  711:[''],                                                    712:['empty'], 713:[''],                                           714:[''],                           715:[''],                           716:[''],               717:[''],       718:[''],                    719:[''],                   720:[''],           721:[''],       722:['tkn_And','condicion_logica','14'],            723:['tkn_Or','condicion_logica','14'],  724:[''],      725:[''],           726:[''],           727:[''],           728:[''],           729:[''],           730:[''],                               731:[''],                           732:[''],                           733:[''],                                       734:[''],                   735:[''],                                                           736:[''],                                               737:[''],                                       738:[''],                   739:[''],                               740:[''],
                    741:[''],                       742:[''],                                                                                               743:[''],                               744:[''],                                       745: [''],                                  746:[''],                                   747: [''],                  748:['E','operadores_log','E','15'],                         749:[''],      750:[''],                                           751:[''],                           752:[''],                           753:[''],               754:[''],       755:[''],                    756:[''],                   757:[''],           758:[''],       759:[''],                                           760:[''],                           761:[''],           762:[''],           763:[''],           764:[''],           765:[''],           766:[''],           767:[''],                               768:[''],                           769:[''],                           770:[''],                                       771:[''],                   772:['E','operadores_log','E','15'],                                773:[''],                                               774:[''],                                       775:[''],                   776:['E','operadores_log','E','15'],    777:[''],
                    778:[''],                       779:[''],                                                                                               780:[''],                               781:[''],                                       782: [''],                                  783:[''],                                   784: [''],                  785:[''],                                                    786:[''],      787:[''],                                           788:[''],                           789:[''],                           790:[''],               791:[''],       792:[''],                    793:[''],                   794:[''],           795:[''],       796:[''],                                           797:[''],                           798:['<','16'],     799:['>','16'],     800:['>=','16'],    801:['<=','16'],    802:['==','16'],    803:['!=','16'],    804:[''],                               805:[''],                           806:[''],                           807:[''],                                       808:[''],                   809:[''],                                                           810:[''],                                               811:[''],                                       812:[''],                   813:[''],                               814:[''],
                    815:[''],                       816:[''],                                                                                               817:[''],                               818:[''],                                       819: [''],                                  820:[''],                                   821: [''],                  822:[''],                                                    823:[''],      824:[''],                                           825:[''],                           826:[''],                           827:[''],               828:[''],       829:[''],                    830:[''],                   831:[''],           832:[''],       833:[''],                                           834:[''],                           835:[''],           836:[''],           837:[''],           838:[''],           839:[''],           840:[''],           841:['op_aditivos','17'],               842:['op_aditivos','17'],           843:['op_multiplicativos','17'],    844:['op_multiplicativos','17'],                845:['op_multiplicativos','17'], 846:[''],                                                      847:[''],                                               848:[''],                                       849:[''],                   850:[''],                               851:[''],
                    852:[''],                       853:[''],                                                                                               854:[''],                               855:[''],                                       856: [''],                                  857:[''],                                   858: [''],                  859:[''],                                                    860:[''],      861:[''],                                           862:[''],                           863:[''],                           864:[''],               865:[''],       866:[''],                    867:[''],                   868:[''],           869:[''],       870:[''],                                           871:[''],                           872:[''],           873:[''],           874:[''],           875:[''],           876:[''],           877:[''],           878:['+','16'],                         879:['-','16'],                     880:[''],                           881:[''],                                       882:[''],                   883:[''],                                                           884:[''],                                               885:[''],                                       886:[''],                   887:[''],                               888:[''],

                    889:[''],                       890:[''],                                                                                               891:[''],                               892:[''],                                       893: [''],                                  894:[''],                                   895: [''],                  896:[''],                                                    897:[''],      898:[''],                                           899:[''],                           900:[''],                           901:[''],               902:[''],       903:[''],                    904:[''],                   905:[''],           906:[''],       907:[''],                                           908:[''],                           909:[''],           910:[''],           911:[''],           912:[''],           913:[''],           914:[''],           915:[''],                               916:[''],                           917:['*','16'],                     918:['/','16'],                                 919:['%','16'],             920:[''],                                                           921:[''],                                               922:[''],                                       923:[''],                   924:[''],                               925:[''],
                    926:[''],                       927:[''],                                                                                               928:[''],                               929:[''],                                       930: [''],                                  931:[''],                                   932: [''],                  933:['(','E',')','8'],                                       934:[''],      935:[''],                                           936:[''],                           937:[''],                           938:[''],               939:[''],       940:[''],                    941:[''],                   942:[''],           943:[''],       944:[''],                                           945:[''],                           946:[''],           947:[''],           948:[''],           949:[''],           950:[''],           951:[''],           952:[''],                               953:[''],                           954:[''],                           955:[''],                                       956:[''],                   957:['T','8','Ep','8'],                                             958:[''],                                               959:[''],                                       960:[''],                   961:['T','8','Ep','8'],                 962:[''],
                    963:[''],                       964:[''],                                                                                               965:[''],                               966:[''],                                       967: [''],                                  968:[''],                                   969: [''],                  970:[''],                                                    971:['empty'], 972:[''],                                           973:[''],                           974:[''],                           975:[''],               976:['empty'],  977:['empty'],               978:[''],                   979:[''],           980:[''],       981:['empty'],                                      982:['empty'],                      983:['empty'],      984:['empty'],      985:['empty'],      986:['empty'],      987:['empty'],      988:['empty'],      989:['op_aditivos','E','9'],            990:['op_aditivos','E','9'],        991:[''],                           992:[''],                                       993:[''],                   994:[''],                                                           995:[''],                                               996:[''],                                       997:[''],                   998:[''],                               999:[''],
                    1000:[''],                      1001:[''],                                                                                              1002:[''],                              1003:[''],                                      1004: [''],                                 1005:[''],                                  1006: [''],                 1007:[''],                                                   1008:[''],     1009:[''],                                          1010:[''],                          1011:[''],                          1012:[''],              1013:[''],      1014:[''],                   1015:[''],                  1016:[''],          1017:[''],      1018:[''],                                          1019:[''],                          1020:[''],          1021:[''],          1022:[''],          1023:[''],          1024:[''],          1025:[''],          1026:[''],                              1027:[''],                          1028:[''],                          1029:[''],                                      1030:[''],                  1031:['F','8','Tp','8'],                                            1032:[''],                                              1033:[''],                                      1034:[''],                  1035:['F','8','Tp','8'],                1036:[''],
                    1037:[''],                      1038:[''],                                                                                              1039:[''],                              1040:[''],                                      1041: [''],                                 1042:[''],                                  1043: [''],                 1044:[''],                                                   1045:['empty'],1046:[''],                                          1047:[''],                          1048:[''],                          1049:[''],              1050:['empty'], 1051:['empty'],              1052:[''],                  1053:[''],          1054:[''],      1055:['empty'],                                     1056:['empty'],                     1057:['empty'],     1058:['empty'],     1059:['empty'],     1060:['empty'],     1061:['empty'],     1062:['empty'],     1063:['empty'],                         1064:['empty'],                     1065:['op_multiplicativos','T','9'],1066:['op_multiplicativos','T','9'],            1067:['op_multiplicativos','T','9'],1068:[''],                                                  1069:[''],                                              1070:[''],                                      1071:[''],                  1072:[''],                              1073:[''],
                    1074:[''],                      1075:[''],                                                                                              1076:[''],                              1077:[''],                                      1078: [''],                                 1079:[''],                                  1080: [''],                 1081:[''],                                                   1082:[''],     1083:[''],                                          1084:[''],                          1085:[''],                          1086:[''],              1087:[''],      1088:[''],                   1089:[''],                  1090:[''],          1091:[''],      1092:[''],                                          1093:[''],                          1094:[''],          1095:[''],          1096:[''],          1097:[''],          1098:[''],          1099:[''],          1100:[''],                              1101:[''],                          1102:[''],                          1103:[''],                                      1104:[''],                  1105:['tkn_Identificador','11','Fp','8'],                           1106:[''],                                              1107:[''],                                      1108:[''],                  1109:['tkn_Numero','12'],               1110:[''],
                    1111:[''],                      1112:[''],                                                                                              1113:[''],                              1114:[''],                                      1115: [''],                                 1116:[''],                                  1117: [''],                 1118:[''],                                                   1119:['empty'],1120:[''],                                          1121:[''],                          1122:['tkn_Numero','3'],            1123:[''],              1124:['empty'], 1125:['empty'],              1126:[''],                  1127:[''],          1128:[''],      1129:['empty'],                                     1130:['empty'],                     1131:['empty'],     1132:['empty'],     1133:['empty'],     1134:['empty'],     1135:['empty'],     1136:['empty'],     1137:['empty'],                         1138:['empty'],                     1139:['empty'],                     1140:['empty'],                                 1141:['empty'],             1142:[''],                                                          1143:[''],                                              1144:[''],                                      1145:[''],                  1146:[''],                              1147:[''],


                  }


# Atributos No Terminales
# -----------------------------------------------------------------------------

class NoTerminal:
    def __init__(self):
        self.lexema = None  # Me permite acceder a mi TS en la pos "lexema"
        self.tipo = None
        self.value = None
        self.tam = None

class Variable:
    def __init__(self):
        self.lexema = None  # Me permite acceder a mi TS en la pos "lexema"
        self.tipo = None
        self.value = None
        self.tam = None

# Inicializar No Terminales
# -----------------------------------------------------------------------------

lista_sentencias     = NoTerminal()
def_basica           = NoTerminal()
tipo_Dato            = NoTerminal()
lista_def            = NoTerminal()
lista_defp           = NoTerminal()
def_espec            = NoTerminal()
def_especp           = NoTerminal()
def_especpp          = NoTerminal()
acceso_array         = NoTerminal()
simple_asign         = NoTerminal()
sentencia            = NoTerminal()
sentenciap           = NoTerminal()
condicion            = NoTerminal()
condicionp           = NoTerminal()
condicion_logica     = NoTerminal()
operadores_log       = NoTerminal()
operadores           = NoTerminal()
op_aditivos          = NoTerminal()
op_multiplicativos   = NoTerminal()
E                    = NoTerminal()
Ep                   = NoTerminal()
T                    = NoTerminal()
Tp                   = NoTerminal()
F                    = NoTerminal()
Fp                   = NoTerminal()


# Reglas Semánticas
#-----------------------------------------------------------------------------
def operacion(objeto1,objeto2,operador):
    if operador == '*':
        return objeto1 * objeto2
    elif operador == '/':
        return objeto1 / objeto2
    elif operador == '%':
        return objeto1 % objeto2
    elif operador == '+':
        return objeto1 + objeto2
    elif operador == '-':
        return objeto1 - objeto2
    elif operador == '==':
        return objeto1 == objeto2
    elif operador == '!=':
        return objeto1 != objeto2
    elif operador == '>=':
        return objeto1 >= objeto2
    elif operador == '<=':
        return objeto1 <= objeto2
    elif operador == '>':
        return objeto1 > objeto2
    elif operador == '<':
        return objeto1 < objeto2

def getValue(id):
    return tablaSimbolos[id]['Valor']

def getLexema(id):
    return tablaSimbolos[id]['Lexema']
def getTam(id):
    return tablaSimbolos[id]['Tam']

def getType(id):
    return tablaSimbolos[id]['Type']

def setValue(id,value):
    tablaSimbolos[id]['Valor'] = value

def setType(id,type):
    tablaSimbolos[id]['Type'] = type

def setTam(id,tam):
    tablaSimbolos[id]['Tam'] = tam

# Comprobación de tipos && SetValue
def rule_1(id, objeto1):
    print "RULE 1"
    if objeto1.tipo == getType(id):
        print id, " = ", objeto1.value
        setValue(id, objeto1.value)
    else:
        print "Error de tipo"

# Comprobación de tipos && Paso de Valor
def rule_2(objeto1, objeto2):
    if objeto1.tipo == objeto2.tipo:
        objeto1.value = objeto2.value
    else:
        print "Error de tipo"

# Paso de Tipo
def _3(objeto1, objeto2):
    objeto1.tipo = objeto2.tipo

# Sintetizado Tipo
def _4(objeto1, objeto2):
    objeto1.tipo = objeto2

# SetType && SetTam = 0
def _5(objeto1, id):
    setType(id,objeto1.tipo)
    setTam(id,0)

# Paso de Tipo && Paso de Lexema
def _6(objeto1,objeto2,id):
    objeto1.tipo = objeto2.tipo
    objeto1.lexema = getLexema(id)


# Array: Sobreescribimos Tam y asignamos Tipo array[0] ... array[Numero-1]
def _7(objeto1,Numero):
    setTam(objeto1.lexema,Numero)
    tipo = getType(objeto1)
    for x in range(0,Numero):
        lexema = objeto1 + str(x)
        setType(lexema,tipo)

# Paso de Tipo y Valor
def _8(objeto1, objeto2):
    objeto1.tipo = objeto2.tipo
    objeto1.value = objeto2.value

# Operaciones Aritméticas
def _9(objeto1, objeto2,operador):
    if objeto1.tipo == objeto2.tipo:
        objeto1.value = operacion (objeto1.value,objeto2.value,operador.lexema)
    print "Error de tipo"

# GetType && GetValue && GetLexema
def _11(objeto1, id):
    objeto1.tipo = getType(id)
    objeto1.value = getValue(id)
    objeto1.lexema = getLexema(id)

# Paso de Tipo y Numero as Value
def _12(objeto1, objeto2):
    objeto1.tipo = 'int' #Falta
    objeto1.value = objeto2

# Array índice
def _13(objeto1,Numero):
    if Numero>-1 and Numero<getTam(objeto1):
        lexema = objeto1 + str(Numero)
        objeto1.value = getValue(lexema)
    else:
        print "Error, no existe esa posición de memoria"

#Condicion
def _14(objeto1,objeto2):
    if objeto1.tipo != objeto2.tipo:
        print "Error de tipo"

# Operaciones Logicas
def _15(objeto1, objeto2,objeto3, operador):
    if objeto1.tipo != objeto2.tipo:
        print "Error de tipos"
    else:
        objeto3.value = operacion(objeto1.value, objeto2.value, operador.lexema)
        objeto3.tipo = 'bool'

# Sintetizado Operador
def _16(objeto1, objeto2):
    objeto1.lexema = objeto2


# Paso de Lexema
def _17(objeto1, objeto2):
    objeto1.lexema = objeto2.lexema

# Análisis Sintáctico
#-----------------------------------------------------------------------------
pila = ['programa','$']
#entrada = ['tkn_Int','tkn_Main','(',')','{','tkn_Int','tkn_Identificador',';','tkn_Return','tkn_Numero',';','}','$']
#entrada = ['tkn_Int','tkn_Main','(',')','{','tkn_Identificador','=','tkn_Identificador',';','tkn_Identificador','=','tkn_Numero','+','tkn_Numero',';','tkn_Return','tkn_Numero',';','}','$']


#Se trabaja con la Lista de Tokens.
#-----------------------------------------------------------------------------
preprocesamiento()
tokens(listaTokens)
entrada = []
lexema = []  #Contendrá los lexemnas de los tkn_Identificadores para ubicarlos en la TS


for x in range(0, len(listaTokens)):
    entrada.append(listaTokens[x][2])
    lexema.append(listaTokens[x][0])

entrada.append('$')
lexema.append('$')
print "ENTRADA, LEXEMAS"
print entrada
print lexema

##AUXILIAR FUNCTIONS
def getAllLexems(listTokens):
    lexems = []
    for i in range (0,len(listaTokens)):
        lexems.append(listaTokens[i][0])

    return lexems

def getAllTokens(listTokens):
    tokens = []
    for i in range (0,len(listaTokens)):
        tokens.append(listaTokens[i][2])
    return tokens


# Pila Sintáctica
#-----------------------------------------------------------------------------
def tablaSintac(entrada,pila):
    while(len(entrada)>0):
        print "\n"
        print "Pila:", pila[::-1]
        print "Entrada:", entrada
        if(terminales.has_key(pila[0])):
            if (entrada[0] == pila[0]):
                if entrada[0] == '$' and pila[0] == '$':
                    print("Cadena aceptada sintacticamente")
                pila.pop(0)
                entrada.pop(0)
                lexema.pop(0)
            else:
                print("Error sintactico: No se esperaba Token", entrada[0])
                pila.pop(0)
                entrada.pop(0)
                lexema.pop(0)

        else:
            #Si es entero -> es regla Ejécutala (con q params?)
            if pila[0].isdigit():
                pila.pop(0)
            else:
                # saco y pongo al revez
                fila = noTerminales[pila[0]] - 1
                columna = terminales[entrada[0]]
                empila = tablaSintactica[fila * 37 + columna]
                #print "data", fila * 37 + columna
                empilar = empila[::-1]
                print 'empila: ', empilar
                pila.pop(0)
                for j in range(0,len(empilar)):
                    if(empilar[j] == ''):
                        print("Error sintactico: No se encuentra Token en la Tabla Sintactica ",entrada[0])
                        entrada.pop(0)
                        lexema.pop(0)
                    elif(empilar[j] != 'empty'):
                        pila.insert(0,empilar[j])


def semanticAnalyzer(listaTokens, pila):
    print "\nSemantic Analizer"
    lexemList = getAllLexems(listaTokens)
    tokenList = getAllTokens(listaTokens)

    for i in range(0,5):
        tokenList.pop(0)
        lexemList.pop(0)

    '''print " ANTES"
    print "TOKENS", tokenList
    print "LEXEMS", lexemList
    '''
    stack = []
    ##for i in range (0,len(lexemList)):
    while len(tokenList) > 5:
        print "\nTOKENS", tokenList
        print "LEXEMS", lexemList
        token = tokenList.pop(0)
        lexem = lexemList.pop(0)
        if token in noTerminales:
            fila = noTerminales[pila[0]] - 1
            columna = terminales[entrada[0]]
            empila = tablaSintactica[fila * 37 + columna]
            print empila, "nt"
            pila.pop(0)
        elif token in terminales:
            #print token, "t"
            if token in ("tkn_Int", "tkn_Float", "tkn_String", "tkn_Bool"):
                nToken = tokenList.pop(0)
                nLexem = lexemList.pop(0) # variable name
                if nToken == "tkn_Identificador":
                    nnToken = tokenList.pop(0)
                    nnLexem = lexemList.pop(0) #semicolon or equal
                    if nnToken == ";": # variable definition
                        val = Variable()
                        print "adsf", token
                        if token == "tkn_Int":
                            val.tipo = nLexem
                            val.tam = 4
                            setType(nLexem, 'int')
                            setValue(nLexem, 0)

                        ##TODO: hacer para los demas tipos de datos
                    elif nnToken == "=":
                        nnnToken = tokenList.pop(0)
                        nnnLexem = lexemList.pop(0)

                        val = Variable()
                        if nnnToken == "tkn_Numero":
                            val.tipo = "int"
                            val.value = nnnLexem
                            setType(nLexem, 'int')
                            rule_1(nLexem, val)
                    # removing semicolon
                    #print "removing:", tokenList.pop(0)
                    #print "removing:", lexemList.pop(0)
                    continue

            elif token == "tkn_If":
                print " case TOKEN IF"
                tokenList.pop(0) #removing keys
                lexemList.pop(0)
                #print tokenList
                endPosition = tokenList.index(")")
                #print "final: ", endPosition

                '''
                for i in range(0, endPosition):
                    ntoken = tokenList.pop(0)
                    nLexem = lexemList.pop(0)
                    boolOpPos = tokenList.index("&&")
                    '''
                #if endPosition =
                nToken = tokenList.pop(0)
                nLexem = lexemList.pop(0)

                nnToken = tokenList.pop(0)
                nnLexem = lexemList.pop(0)

                nnnToken = tokenList.pop(0)
                nnnLexem = lexemList.pop(0)

                val1 = Variable()
                val2 = Variable()

                val1.lexema = nLexem
                val2.lexema = nnnLexem

                variables = {
                    'tkn_Numero_Float': 'float',
                    'tkn_Numero': 'int'
                }

                #print "operators: ", nLexem, nnLexem, nnnLexem
                if nnToken in ("==", "!=", "<", "<=", ">", ">="):

                    #print nLexem," - ", nnnLexem
                    if tablaSimbolos.has_key(nLexem) and tablaSimbolos.has_key(nnnLexem): # ambos son variables
                        #print getType(nLexem)
                        #print getType(nnnLexem)
                        if getType(nLexem) != getType(nnnLexem):
                            print "Error semantico"
                    elif tablaSimbolos.has_key(nLexem): # primer item es variable
                        #print getType(nLexem)
                        #print getType(nnnLexem)
                        print getType(nLexem), nnnToken
                        if getType(nLexem) != variables[nnnToken]:
                            print "Error semantico"
                    elif tablaSimbolos.has_key(nnnLexem): # segundo item es variable
                        print getType(nLexem), nnnToken
                        if getType(nnnLexem) != variables[nToken]:
                            print "Error semantico"



                continue

    print " DESPUES"
    print tokenList
    print lexemList
    

#sentenciap.tipo =  'int'
#sentenciap.value = 48


#preprocesamiento()
#imprimir(listaTokens)
#tokens(listaTokens)
imprimir(listaTokens)
tablaSim(listaTokens)
imprimirTS()

#_1(sentenciap,listaTokens[6][0]);

#for key in tablaSimbolos:
 #   print key, ":", tablaSimbolos[key]

pilatmp = pila
#tablaSintac(entrada, pila)
semanticAnalyzer(listaTokens, pilatmp)

imprimirTS()

