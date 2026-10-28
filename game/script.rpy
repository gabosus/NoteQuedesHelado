# =====================================================================
#  PANEL DE AJUSTES  (lo que más vas a querer cambiar está aquí)
# =====================================================================
init python:

    # Segundos que dura el paneo del fondo del intro.
    #   Más alto  -> el fondo se mueve más lento.
    #   Más bajo  -> se mueve más rápido.
    # OJO: el texto del intro se reparte dentro de este tiempo. Si lo bajas
    # mucho, el texto pasará demasiado rápido para leerse.
    DURACION_PANEO = 36.0

    # Altura que tendrá el personaje en pantalla, en píxeles (la pantalla mide 1080).
    #   Más alto  -> personaje más grande (si te pasas, se corta la cabeza).
    #   Más bajo  -> personaje más pequeño.
    ALTO_CHICA = 1100

    # Cuántos píxeles se baja el personaje POR DEBAJO del borde de la pantalla.
    # Esto esconde el corte de abajo para que no parezca que flota.
    #   Más alto  -> baja más (se ve menos del cuerpo).
    #   0         -> el borde inferior de la imagen queda justo en el borde de la pantalla.
    BAJA_CHICA = 100

    # Posición horizontal del personaje.
    #   0.0 = pegada a la izquierda, 0.5 = centro, 1.0 = pegada a la derecha.
    X_CHICA = 0.1

    # ---------- Texto del intro ----------

    # Font del texto del intro. DejaVuSans-Bold viene incluido con Ren'Py,
    # es grueso y redondeado, parecido al de tu referencia.
    FONT_INTRO = "DejaVuSans-Bold.ttf"

    # Tamaño de la letra (la pantalla mide 1080 de alto).
    TAMANO_INTRO = 56

    # Color del texto y de su contorno (hexadecimal).
    COLOR_INTRO = "#ffe94d"
    CONTORNO_INTRO = "#3a2a00"

    # Grosor del contorno en píxeles.
    GROSOR_CONTORNO = 5

    # Ancho máximo del bloque de texto en píxeles (la pantalla mide 1920).
    #   Más bajo -> el texto se parte en más líneas.
    ANCHO_INTRO = 1400

    # Segundos que dura cada fundido (entrada y salida) de cada bloque de texto.
    FUNDIDO_INTRO = 0.8

    # Segundos de espera antes de que aparezca el primer bloque.
    ESPERA_INTRO = 1.0

    # Cada elemento de la lista es un bloque que aparece solo, uno tras otro.
    # Cada uno termina en una oración completa.
    TEXTOS_INTRO = [
        "Durante años, la Academia Heladia fue un lugar de aprendizaje, amistad y nuevas oportunidades.",
        "Pero, con el tiempo, las burlas se convirtieron en acoso, los conflictos dividieron a los estudiantes y el silencio permitió que todo empeorara.",
        "Entonces, en medio de la discordia, llegó un alumno nuevo. Sin conocer el pasado de Heladia, pronto descubriría que hasta las decisiones más pequeñas pueden cambiar la vida de alguien.",
        "¿Podrá cambiar el destino de la academia… o se quedará helado mientras todo sucede a su alrededor?",
    ]


# =====================================================================
#  ESCALADO AUTOMÁTICO DE IMÁGENES
# =====================================================================
init python:

    # renpy.image_size() lee el ancho y el alto reales de un archivo.
    # Con eso calculamos cuánto agrandar cada imagen.

    # Fondo del intro: se escala para que mida exactamente 1080 px de alto.
    ancho_bg, alto_bg = renpy.image_size("images/bg intro.png")
    escala_bg = 1080.0 / alto_bg

    # Fondo de la academia: igual que el anterior.
    ancho_ac, alto_ac = renpy.image_size("images/bg academia.png")
    escala_ac = 1080.0 / alto_ac

    # Personaje: se escala para que mida ALTO_CHICA píxeles de alto.
    ancho_ch, alto_ch = renpy.image_size("images/chica normal.png")
    escala_chica = ALTO_CHICA / float(alto_ch)


# =====================================================================
#  HORARIO DEL TEXTO DEL INTRO (se calcula solo)
# =====================================================================
init python:

    # Reparte el tiempo del paneo entre los bloques de texto.
    # Un bloque más largo se queda más tiempo en pantalla (proporcional a sus letras).
    # Resultado: TIEMPOS_INTRO = [(cuándo empieza, cuánto dura), ...] en segundos.
    def calcular_tiempos_intro():
        disponible = DURACION_PANEO - ESPERA_INTRO
        total_letras = float(sum(len(t) for t in TEXTOS_INTRO))
        tiempos = []
        inicio = ESPERA_INTRO
        for t in TEXTOS_INTRO:
            dur = disponible * len(t) / total_letras
            tiempos.append((inicio, dur))
            inicio += dur
        return tiempos

    TIEMPOS_INTRO = calcular_tiempos_intro()

    # Crea el texto con el estilo del panel de ajustes.
    #   text_align=0.5 -> centra las líneas entre sí.
    #   xmaximum       -> ancho máximo antes de partir la línea.
    def texto_intro(s):
        return Text(s, font=FONT_INTRO, size=TAMANO_INTRO, color=COLOR_INTRO,
            outlines=[(GROSOR_CONTORNO, CONTORNO_INTRO, 0, 0)],
            text_align=0.5, xmaximum=ANCHO_INTRO)


# =====================================================================
#  IMÁGENES
# =====================================================================

# "image NOMBRE = ..." crea una imagen con un nombre que luego usas en scene/show.
# Transform(archivo, zoom=X) toma el archivo y lo agranda o achica X veces.
image bg paneo = Transform("images/bg intro.png", zoom=escala_bg)
image bg academia = Transform("images/bg academia.png", zoom=escala_ac)

# Aviso "Clic para saltar".
#   size     -> tamaño de la letra.
#   color    -> color del texto (código hexadecimal, #ffffff es blanco).
#   outlines -> contorno del texto: (grosor, color, desplazamiento x, desplazamiento y).
#               Sirve para que se lea sobre cualquier fondo.
image pista_saltar = Text("Clic para saltar", size=28, color="#ffffff",
    outlines=[(2, "#000000aa", 0, 0)])

# Los 4 bloques de texto del intro, uno por párrafo.
# Cada uno es una imagen aparte para poder mostrarla en su propio momento.
image intro_txt1 = texto_intro(TEXTOS_INTRO[0])
image intro_txt2 = texto_intro(TEXTOS_INTRO[1])
image intro_txt3 = texto_intro(TEXTOS_INTRO[2])
image intro_txt4 = texto_intro(TEXTOS_INTRO[3])


# =====================================================================
#  PERSONAJES
# =====================================================================

# define c = Character("Nombre", color="#colorDelNombre")
#   c      -> la letra corta que escribes antes de cada diálogo (c "Hola").
#   "Roselle" -> el nombre que se ve en el cuadro de diálogo.
#   color  -> color de ese nombre.
# Para otro personaje, copia la línea con otra letra: define m = Character("Marco", color="#6a9cff")
define c = Character("Roselle", color="#f58fb4")


# =====================================================================
#  TRANSFORMS (movimientos y posiciones)
# =====================================================================

# Paneo del fondo del intro.
#   xalign 1.0 -> empieza mostrando el lado derecho de la imagen.
#   ease       -> movimiento que arranca y frena suave (linear sería parejo y mecánico).
#   xalign 0.0 -> termina mostrando el lado izquierdo.
# Resultado: la imagen pasa por la pantalla de izquierda a derecha.
transform paneo:
    xalign 1.0
    ease DURACION_PANEO xalign 0.0

# Texto "Clic para saltar".
#   xalign / yalign -> posición (0.98 y 0.96 = esquina inferior derecha).
#   alpha 0.0       -> empieza invisible.
#   pause 3.0       -> espera 3 segundos.
#   linear 1.0 alpha 0.7 -> en 1 segundo aparece hasta 70% de opacidad.
transform pista:
    xalign 0.98
    yalign 0.96
    alpha 0.0
    pause 3.0
    linear 1.0 alpha 0.7

# Aparición de un bloque de texto del intro.
#   inicio -> segundos que espera invisible antes de aparecer.
#   dur    -> segundos que dura su turno en total (entrada + quieto + salida).
#   xalign / yalign -> posición (0.5 y 0.5 = centro de la pantalla).
#                      Sube yalign (hasta 1.0) para bajarlo.
# Secuencia: invisible -> fundido de entrada -> se queda -> fundido de salida.
transform texto_en_intro(inicio, dur):
    xalign 0.5
    yalign 0.5
    alpha 0.0
    pause inicio
    linear FUNDIDO_INTRO alpha 1.0
    pause dur - 2 * FUNDIDO_INTRO
    linear FUNDIDO_INTRO alpha 0.0

# Entrada del personaje.
#   x    -> posición horizontal (0.0 izquierda, 0.5 centro, 1.0 derecha).
#   z    -> zoom (cuánto se agranda la imagen).
#   baja -> píxeles que se baja por debajo del borde de la pantalla.
transform aparece(x=0.5, z=1.0, baja=0):
    xalign x                # posición horizontal
    yanchor 1.0             # el "punto de agarre" es el borde inferior de la imagen
    ypos 1080 + baja        # ese borde inferior queda en el fondo de la pantalla (1080) + baja
    zoom z                  # tamaño
    alpha 0.0               # empieza invisible
    yoffset 40              # empieza 40 px más abajo de su lugar final
    easein 0.8 alpha 1.0 yoffset 0   # en 0.8 s se hace visible y sube a su lugar

# Hoja que gira y se voltea mientras cae.
#   z      -> tamaño de la hoja.
#   giro   -> segundos que tarda en dar una vuelta completa.
#   volteo -> segundos que tarda en voltearse a medias (efecto 3D).
transform girar(z, giro, volteo):
    zoom z
    parallel:                       # "parallel" hace que los dos movimientos ocurran a la vez
        rotate 0                    # parte sin girar
        linear giro rotate 360      # gira 360 grados en "giro" segundos
        repeat                      # y vuelve a empezar, sin parar
    parallel:
        xzoom 1.0                   # ancho normal
        ease volteo xzoom -1.0      # se estrecha, se da la vuelta y queda espejada
        ease volteo xzoom 1.0       # vuelve a su lado original
        repeat


# =====================================================================
#  HOJAS CAYENDO
# =====================================================================

# SnowBlossom crea muchas partículas que caen.
#   At("hoja.png", girar(...)) -> usa tu imagen aplicándole el giro de arriba.
#   count   -> cuántas hojas hay a la vez (más = más denso, y más pesado para el equipo).
#   border  -> margen fuera de la pantalla donde nacen y mueren las hojas.
#   xspeed  -> velocidad horizontal en px/seg, (mín, máx). NEGATIVO = hacia la izquierda.
#   yspeed  -> velocidad de caída en px/seg, (mín, máx). Más alto = cae más rápido.
#   start   -> segundos que tardan en empezar a aparecer.
#   fast    -> True = la pantalla ya empieza con hojas, sin esperar a que lleguen.

# Hojas de fondo: pequeñas, lentas y muchas.
image hojas_lejos = SnowBlossom(At("hoja.png", girar(0.050, 7.0, 1.6)),
    count=30, border=50,
    xspeed=(-80, -40), yspeed=(60, 110),
    start=0, fast=True)

# Hojas de frente: más grandes, rápidas y pocas (dan sensación de profundidad).
image hojas_cerca = SnowBlossom(At("hoja.png", girar(0.1, 4.0, 1.0)),
    count=12, border=50,
    xspeed=(-200, -120), yspeed=(180, 280),
    start=0, fast=True)


# =====================================================================
#  EL JUEGO
# =====================================================================
label start:

    # ---------- INTRO ----------

    # quick_menu es la barra de abajo (Atrás, Historial, Saltar...). La ocultamos en el intro.
    $ quick_menu = False

    # scene     -> borra todo lo que hubiera en pantalla y pone este fondo.
    # at paneo  -> le aplica el movimiento definido arriba.
    scene bg paneo at paneo

    # show -> agrega algo encima sin borrar lo demás.
    # El orden importa: lo que se muestra después queda por delante.
    show hojas_cerca
    show hojas_lejos
    show pista_saltar at pista

    # Los 4 bloques de texto se muestran AL FINAL, así quedan por encima de
    # todo (fondo, hojas y aviso). Todos se agregan a la vez, pero cada uno
    # empieza invisible y espera su turno (ver transform texto_en_intro).
    # Los tiempos vienen de TIEMPOS_INTRO: (cuándo empieza, cuánto dura).
    show intro_txt1 at texto_en_intro(TIEMPOS_INTRO[0][0], TIEMPOS_INTRO[0][1])
    show intro_txt2 at texto_en_intro(TIEMPOS_INTRO[1][0], TIEMPOS_INTRO[1][1])
    show intro_txt3 at texto_en_intro(TIEMPOS_INTRO[2][0], TIEMPOS_INTRO[2][1])
    show intro_txt4 at texto_en_intro(TIEMPOS_INTRO[3][0], TIEMPOS_INTRO[3][1])

    # with fade -> todo aparece con un fundido desde negro.
    with fade

    # renpy.pause(segundos) espera ese tiempo, pero un clic la interrumpe.
    # Devuelve True si el jugador hizo clic, y False si esperó hasta el final.
    # El "+ 1.0" es un respiro: el plano se queda quieto un segundo al terminar el paneo.
    $ intro_saltada = renpy.pause(DURACION_PANEO + 1.0)

    # ---------- TRANSICIÓN ----------

    # Si el jugador saltó el intro, el disolvido es rápido (0.5 s).
    # Si dejó correr el intro, es lento y suave (2.0 s).
    $ tiempo_transicion = 0.5 if intro_saltada else 2.0

    # scene reemplaza TODO (fondo, hojas, aviso y textos) por el fondo de la academia,
    # y "with Dissolve" hace que el cambio sea un fundido cruzado en vez de un corte.
    scene bg academia
    with Dissolve(tiempo_transicion)

    # Medio segundo para que el fondo se asiente antes de que entre el personaje.
    pause 0.5

    # ---------- PRIMERA ESCENA ----------

    # Volvemos a mostrar la barra de abajo.
    $ quick_menu = True

    # show chica normal -> muestra el archivo "chica normal.png" de la carpeta images.
    #   chica = nombre del personaje, normal = su expresión (así se llama el archivo).
    # at aparece(posición, tamaño, baja) -> usa los valores del panel de ajustes.
    show chica normal at aparece(X_CHICA, escala_chica, BAJA_CHICA)
    pause 0.8

    # c "texto" -> el personaje "c" (Roselle) dice ese texto.
    c "¡Bienvenidos a la academia!"
    c "Me alegra mucho que estén aquí."

    # return -> termina el juego (más adelante aquí seguirás con la historia).
    return