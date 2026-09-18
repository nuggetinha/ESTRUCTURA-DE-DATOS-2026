# ==========================================
#       DAMAS INGLESAS
#       VERSION CON REPETICION DE PARTIDA
# ==========================================

import time

# ------------------------------------------
# CREAR TABLERO
# ------------------------------------------

def crear_tablero():
    tablero = [
        ['.', 'o', '.', 'o', '.', 'o', '.', 'o'],
        ['o', '.', 'o', '.', 'o', '.', 'o', '.'],
        ['.', 'o', '.', 'o', '.', 'o', '.', 'o'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['x', '.', 'x', '.', 'x', '.', 'x', '.'],
        ['.', 'x', '.', 'x', '.', 'x', '.', 'x'],
        ['x', '.', 'x', '.', 'x', '.', 'x', '.']
    ]

    return tablero


# ------------------------------------------
# COPIAR TABLERO
# ------------------------------------------

def copiar_tablero(tablero):

    copia = []

    for fila in tablero:
        copia.append(fila[:])

    return copia


# ------------------------------------------
# MOSTRAR TABLERO
# ------------------------------------------

def mostrar_tablero(tablero):

    print()
    print("    a b c d e f g h")
    print("  -----------------")

    for i in range(7, -1, -1):
        print(str(i + 1) + " |", end=" ")

        for j in range(8):
            print(tablero[i][j], end=" ")

        print("| " + str(i + 1))

    print("  -----------------")
    print("    a b c d e f g h")
    print()


# ------------------------------------------
# CONVERTIR LETRA A COLUMNA
# ------------------------------------------

def columna(letra):

    if letra == 'a':
        return 0
    if letra == 'b':
        return 1
    if letra == 'c':
        return 2
    if letra == 'd':
        return 3
    if letra == 'e':
        return 4
    if letra == 'f':
        return 5
    if letra == 'g':
        return 6
    if letra == 'h':
        return 7

    return -1


# ------------------------------------------
# CONVERTIR NUMERO DE COLUMNA A LETRA
# ------------------------------------------

def letra_columna(c):

    letras = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

    return letras[c]


# ------------------------------------------
# CONVERTIR JUGADA
# ------------------------------------------

def convertir_casilla(casilla):

    letra = casilla[0]
    numero = int(casilla[1])

    c = columna(letra)
    f = numero - 1

    return f, c


# ------------------------------------------
# SABER SI ESTA DENTRO DEL TABLERO
# ------------------------------------------

def dentro(fila, col):

    if fila >= 0 and fila < 8:
        if col >= 0 and col < 8:
            return True

    return False


# ------------------------------------------
# SABER SI ES DEL JUGADOR
# ------------------------------------------

def es_del_jugador(pieza, jugador):

    if jugador == 'x':
        if pieza == 'x' or pieza == 'X':
            return True

    if jugador == 'o':
        if pieza == 'o' or pieza == 'O':
            return True

    return False


# ------------------------------------------
# SABER SI ES ENEMIGA
# ------------------------------------------

def es_enemiga(pieza, jugador):

    if jugador == 'x':
        if pieza == 'o' or pieza == 'O':
            return True

    if jugador == 'o':
        if pieza == 'x' or pieza == 'X':
            return True

    return False


# ------------------------------------------
# MOVIMIENTO SIMPLE
# ------------------------------------------

def movimiento_simple(tablero, fi, ci, ff, cf, jugador):

    pieza = tablero[fi][ci]

    if not es_del_jugador(pieza, jugador):
        return False

    if tablero[ff][cf] != '.':
        return False

    # --------------------------------------
    # DAMA
    # --------------------------------------

    if pieza == 'X' or pieza == 'O':

        diferencia_fila = ff - fi
        diferencia_col = cf - ci

        if diferencia_fila == 1 and diferencia_col == 1:
            return True

        if diferencia_fila == 1 and diferencia_col == -1:
            return True

        if diferencia_fila == -1 and diferencia_col == 1:
            return True

        if diferencia_fila == -1 and diferencia_col == -1:
            return True

        return False

    # --------------------------------------
    # FICHA NORMAL
    # --------------------------------------

    if jugador == 'x':

        # Las negras avanzan hacia las filas menores
        if ff == fi - 1:
            if cf == ci + 1 or cf == ci - 1:
                return True

    if jugador == 'o':

        # Las blancas avanzan hacia las filas mayores
        if ff == fi + 1:
            if cf == ci + 1 or cf == ci - 1:
                return True

    return False


# ------------------------------------------
# CAPTURA
# ------------------------------------------

def puede_capturar(tablero, fi, ci, ff, cf, jugador):

    pieza = tablero[fi][ci]

    if not es_del_jugador(pieza, jugador):
        return False

    if tablero[ff][cf] != '.':
        return False

    diferencia_fila = ff - fi
    diferencia_col = cf - ci

    # --------------------------------------
    # CAPTURA DE UNA DAMA
    # --------------------------------------

    if pieza == 'X' or pieza == 'O':

        if abs(diferencia_fila) == 2:
            if abs(diferencia_col) == 2:

                fm = fi + diferencia_fila // 2
                cm = ci + diferencia_col // 2

                if es_enemiga(tablero[fm][cm], jugador):
                    return True

    # --------------------------------------
    # CAPTURA DE FICHA NORMAL
    # --------------------------------------

    else:

        if jugador == 'x':

            if diferencia_fila == -2:
                if abs(diferencia_col) == 2:

                    fm = fi - 1
                    cm = ci + diferencia_col // 2

                    if es_enemiga(tablero[fm][cm], jugador):
                        return True

        if jugador == 'o':

            if diferencia_fila == 2:
                if abs(diferencia_col) == 2:

                    fm = fi + 1
                    cm = ci + diferencia_col // 2

                    if es_enemiga(tablero[fm][cm], jugador):
                        return True

    return False


# ------------------------------------------
# SABER SI UNA PIEZA CONCRETA PUEDE CAPTURAR
# ------------------------------------------

def tiene_captura(tablero, f, c, jugador):

    direcciones = [
        (2, 2),
        (2, -2),
        (-2, 2),
        (-2, -2)
    ]

    for movimiento in direcciones:

        nf = f + movimiento[0]
        nc = c + movimiento[1]

        if dentro(nf, nc):

            if puede_capturar(tablero, f, c, nf, nc, jugador):
                return True

    return False


# ------------------------------------------
# REALIZAR MOVIMIENTO
# ------------------------------------------

def mover(tablero, fi, ci, ff, cf, jugador):

    pieza = tablero[fi][ci]

    # --------------------------------------
    # SI ES CAPTURA
    # --------------------------------------

    if puede_capturar(tablero, fi, ci, ff, cf, jugador):

        fm = (fi + ff) // 2
        cm = (ci + cf) // 2

        # Quitar pieza enemiga
        tablero[fm][cm] = '.'

        # Mover pieza
        tablero[ff][cf] = pieza
        tablero[fi][ci] = '.'

        # Coronación
        if pieza == 'x' and ff == 0:
            tablero[ff][cf] = 'X'

        if pieza == 'o' and ff == 7:
            tablero[ff][cf] = 'O'

        return True

    # --------------------------------------
    # MOVIMIENTO NORMAL
    # --------------------------------------

    if movimiento_simple(tablero, fi, ci, ff, cf, jugador):

        tablero[ff][cf] = pieza
        tablero[fi][ci] = '.'

        # Coronación
        if pieza == 'x' and ff == 0:
            tablero[ff][cf] = 'X'

        if pieza == 'o' and ff == 7:
            tablero[ff][cf] = 'O'

        return True

    return False


# ------------------------------------------
# EXISTE ALGUNA CAPTURA
# ------------------------------------------

def hay_captura(tablero, jugador):

    for f in range(8):
        for c in range(8):

            if es_del_jugador(tablero[f][c], jugador):

                if tiene_captura(tablero, f, c, jugador):
                    return True

    return False


# ------------------------------------------
# CONTAR FICHAS
# ------------------------------------------

def contar_fichas(tablero, jugador):

    cantidad = 0

    for f in range(8):
        for c in range(8):

            if es_del_jugador(tablero[f][c], jugador):
                cantidad = cantidad + 1

    return cantidad


# ------------------------------------------
# SABER SI PUEDE MOVER
# ------------------------------------------

def puede_mover(tablero, jugador):

    for f in range(8):
        for c in range(8):

            if es_del_jugador(tablero[f][c], jugador):

                # Movimientos de una casilla
                movimientos = [
                    (1, 1),
                    (1, -1),
                    (-1, 1),
                    (-1, -1)
                ]

                for movimiento in movimientos:

                    nf = f + movimiento[0]
                    nc = c + movimiento[1]

                    if dentro(nf, nc):

                        if movimiento_simple(
                            tablero,
                            f,
                            c,
                            nf,
                            nc,
                            jugador
                        ):
                            return True

                # Movimientos de captura
                if tiene_captura(tablero, f, c, jugador):
                    return True

    return False


# ------------------------------------------
# COMPROBAR FORMATO DE UNA CASILLA
# ------------------------------------------

def formato_correcto(casilla):

    if len(casilla) != 2:
        print("Casilla incorrecta.")
        return False

    if casilla[0] < 'a' or casilla[0] > 'h':
        print("Columna incorrecta.")
        return False

    if casilla[1] < '1' or casilla[1] > '8':
        print("Fila incorrecta.")
        return False

    return True


# ------------------------------------------
# MOSTRAR UN PASO DE LA REPETICION
# ------------------------------------------

def mostrar_paso(historial, posicion):

    total = len(historial) - 1

    texto = historial[posicion][0]
    tablero = historial[posicion][1]

    print()
    print("=== REPETICION: paso " + str(posicion) + " de " + str(total) + " ===")
    print(texto)

    mostrar_tablero(tablero)


# ------------------------------------------
# VER REPETICION DE LA PARTIDA
# ------------------------------------------

def ver_repeticion(historial):

    total = len(historial) - 1

    if total == 0:
        print("No hay movimientos para repetir.")
        return

    print()
    print("================================")
    print("     REPETICION DE LA PARTIDA")
    print("================================")
    print()
    print("Controles:")
    print("  Enter  = siguiente movimiento")
    print("  a      = movimiento anterior")
    print("  i      = ir al inicio")
    print("  f      = ir al final")
    print("  p      = reproducir automaticamente")
    print("           (Ctrl+C para detener)")
    print("  numero = saltar a ese movimiento")
    print("  q      = salir de la repeticion")

    posicion = 0
    mostrar = True

    while True:

        if mostrar:
            mostrar_paso(historial, posicion)

        mostrar = True

        opcion = input("Repeticion> ").strip().lower()

        # ----------------------------------
        # SALIR
        # ----------------------------------

        if opcion == 'q':
            print("Repeticion terminada.")
            break

        # ----------------------------------
        # SIGUIENTE
        # ----------------------------------

        elif opcion == '':

            if posicion < total:
                posicion = posicion + 1
            else:
                print("Ya estas en el ultimo movimiento.")
                mostrar = False

        # ----------------------------------
        # ANTERIOR
        # ----------------------------------

        elif opcion == 'a':

            if posicion > 0:
                posicion = posicion - 1
            else:
                print("Ya estas en la posicion inicial.")
                mostrar = False

        # ----------------------------------
        # INICIO / FINAL
        # ----------------------------------

        elif opcion == 'i':
            posicion = 0

        elif opcion == 'f':
            posicion = total

        # ----------------------------------
        # REPRODUCCION AUTOMATICA
        # ----------------------------------

        elif opcion == 'p':

            if posicion == total:
                posicion = 0
                mostrar_paso(historial, posicion)
                time.sleep(1)

            print("Reproduciendo... (Ctrl+C para detener)")

            try:

                while posicion < total:
                    posicion = posicion + 1
                    mostrar_paso(historial, posicion)
                    time.sleep(1)

                print("Fin de la repeticion.")

            except KeyboardInterrupt:
                print()
                print("Reproduccion detenida.")

            # El ultimo paso ya se mostro
            mostrar = False

        # ----------------------------------
        # SALTAR A UN MOVIMIENTO
        # ----------------------------------

        elif opcion.isdigit():

            numero = int(opcion)

            if numero >= 0 and numero <= total:
                posicion = numero
            else:
                print("Elige un numero entre 0 y " + str(total) + ".")
                mostrar = False

        else:
            print("Opcion no valida.")
            mostrar = False


# ------------------------------------------
# MENU AL TERMINAR LA PARTIDA
# Devuelve True si se quiere jugar de nuevo
# ------------------------------------------

def menu_final(historial):

    while True:

        print()
        print("================================")
        print("       PARTIDA FINALIZADA")
        print("================================")
        print("1 = Ver repeticion de la partida")
        print("2 = Jugar de nuevo")
        print("3 = Salir")
        print()

        opcion = input("Elige una opcion: ").strip()

        if opcion == '1':
            ver_repeticion(historial)

        elif opcion == '2':
            return True

        elif opcion == '3':
            return False

        else:
            print("Opcion no valida.")


# ------------------------------------------
# PARTIDA
# Devuelve el historial para la repeticion
# ------------------------------------------

def jugar():

    tablero = crear_tablero()

    jugador = 'x'

    # Casilla obligada cuando hay captura multiple
    # Vale None cuando no hay ninguna obligacion
    obligada = None

    # Historial: lista de (texto, tablero) con el
    # estado del tablero despues de cada movimiento
    historial = [("Posicion inicial", copiar_tablero(tablero))]
    numero_movimiento = 0

    print("================================")
    print("        DAMAS INGLESAS")
    print("================================")
    print()
    print("x = Negras")
    print("o = Blancas")
    print("X = Dama negra")
    print("O = Dama blanca")
    print()
    print("Las negras comienzan.")
    print()
    print("Ejemplo de movimiento:")
    print("c6 d5")
    print()
    print("Escribe q para terminar la partida.")
    print()

    while True:

        mostrar_tablero(tablero)

        # ----------------------------------
        # COMPROBAR SI QUEDAN FICHAS
        # ----------------------------------

        fichas = contar_fichas(tablero, jugador)

        if fichas == 0:

            if jugador == 'x':
                print("¡Ganan las BLANCAS!")
            else:
                print("¡Ganan las NEGRAS!")

            break

        # ----------------------------------
        # COMPROBAR SI PUEDE MOVER
        # ----------------------------------

        if not puede_mover(tablero, jugador):

            if jugador == 'x':
                print("¡Ganan las BLANCAS!")
            else:
                print("¡Ganan las NEGRAS!")

            print("El jugador no puede realizar movimientos.")
            break

        # ----------------------------------
        # MOSTRAR TURNO
        # ----------------------------------

        if jugador == 'x':
            print("Turno de las NEGRAS")
        else:
            print("Turno de las BLANCAS")

        # ----------------------------------
        # CAPTURA OBLIGATORIA
        # ----------------------------------

        captura_obligatoria = hay_captura(tablero, jugador)

        if obligada != None:

            print("¡DEBES SEGUIR CAPTURANDO CON LA FICHA DE "
                  + letra_columna(obligada[1])
                  + str(obligada[0] + 1)
                  + "!")

        elif captura_obligatoria:
            print("¡CAPTURA OBLIGATORIA!")

        # ----------------------------------
        # PEDIR JUGADA
        # ----------------------------------

        if obligada != None:

            origen = letra_columna(obligada[1]) + str(obligada[0] + 1)
            print("Casilla de origen: " + origen)

        else:
            origen = input("Casilla de origen: ").lower()

            # ------------------------------
            # SALIR
            # ------------------------------

            if origen == 'q':
                print("Partida terminada.")
                break

        destino = input("Casilla de destino: ").lower()

        if destino == 'q':
            print("Partida terminada.")
            break

        # ----------------------------------
        # COMPROBAR FORMATO
        # ----------------------------------

        if not formato_correcto(origen):
            continue

        if not formato_correcto(destino):
            continue

        # ----------------------------------
        # CONVERTIR CASILLAS
        # ----------------------------------

        fi, ci = convertir_casilla(origen)
        ff, cf = convertir_casilla(destino)

        # ----------------------------------
        # COMPROBAR QUE LA PIEZA SEA DEL
        # JUGADOR
        # ----------------------------------

        if not es_del_jugador(tablero[fi][ci], jugador):

            print("Esa pieza no te pertenece.")
            continue

        # ----------------------------------
        # SI HAY CAPTURA OBLIGATORIA
        # ----------------------------------

        es_captura = puede_capturar(tablero, fi, ci, ff, cf, jugador)

        if captura_obligatoria and not es_captura:

            print("Debes realizar una captura.")
            continue

        # ----------------------------------
        # REALIZAR MOVIMIENTO
        # ----------------------------------

        era_ficha_normal = tablero[fi][ci] == 'x' or tablero[fi][ci] == 'o'

        if mover(tablero, fi, ci, ff, cf, jugador):

            print("Movimiento realizado.")

            # ------------------------------
            # SABER SI ACABA DE CORONAR
            # ------------------------------

            corono = False

            if era_ficha_normal:
                if tablero[ff][cf] == 'X' or tablero[ff][cf] == 'O':
                    corono = True

            # ------------------------------
            # GUARDAR EN EL HISTORIAL
            # ------------------------------

            numero_movimiento = numero_movimiento + 1

            if jugador == 'x':
                nombre = "Negras"
            else:
                nombre = "Blancas"

            texto = ("Movimiento " + str(numero_movimiento) + ": "
                     + nombre + " " + origen + " -> " + destino)

            if es_captura:
                texto = texto + " (captura)"

            if corono:
                texto = texto + " (corona)"

            historial.append((texto, copiar_tablero(tablero)))

            # ------------------------------
            # CAPTURA MULTIPLE
            # ------------------------------

            sigue_capturando = False

            if es_captura and not corono:
                if tiene_captura(tablero, ff, cf, jugador):
                    sigue_capturando = True

            if sigue_capturando:

                # La misma ficha vuelve a mover
                obligada = (ff, cf)

            else:

                obligada = None

                # --------------------------
                # CAMBIAR TURNO
                # --------------------------

                if jugador == 'x':
                    jugador = 'o'
                else:
                    jugador = 'x'

        else:

            print("Movimiento ilegal.")

    return historial


# ------------------------------------------
# PROGRAMA PRINCIPAL
# ------------------------------------------

def programa():

    while True:

        historial = jugar()

        if not menu_final(historial):
            break

    print("¡Gracias por jugar!")


# ------------------------------------------
# INICIAR PROGRAMA
# ------------------------------------------

programa()
