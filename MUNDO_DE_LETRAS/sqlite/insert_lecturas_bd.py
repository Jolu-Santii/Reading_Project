import sqlite3 as sql
import os, json

bd_path = os.path.join(os.path.dirname(__file__), "..\\preguntas\\lecturas.db")

lecturas = [
  (1, 'DECIR LO QUE PIENSAS Y PENSAR EN LO QUE DICES', """Entonces, continuó la Liebre, debieras decir lo que piensas.
- Pero ¡si es lo que estoy haciendo!, se apresuró a decir Alicia. Al menos…, 
al menos pienso lo que digo…, que después de todo viene a ser la misma cosa, ¿no?
- ¿La misma cosa? ¡De ninguna manera!, negó enfáticamente el Sombrerero. ¡Hala! 
Si fuera así, entonces también daría igual decir: “Veo cuanto como” que
“como cuanto veo”.
- ¡Qué barbaridad!, coreó la Liebre de Marzo. Sería como decir que da
lo mismo afirmar “me gusta cuanto tengo”, que “tengo cuanto me gusta”.
- Valdría tanto como querer afirmar, añadió el Lirón, que parecía hablar
en sueños, que da igual decir “respiro cuando duermo” que “duermo
cuando respiro”.
- Eso sí que te da igual a ti, exclamó el Sombrerero.
Y con esto cesó la conversación."""),
  (2, 'LAS RANAS DE NATA', """Había una vez dos ranas que cayeron en un recipiente lleno de nata espesa. Al instante
notaron que se hundían y que nadar allí era casi imposible. Desesperadas, 
comenzaron a patalear con todas sus fuerzas, pero no lograban avanzar ni salir a la superficie.

Una de ellas, agotada y sin esperanza, exclamó: “Esto no tiene sentido. 
Es inútil seguir luchando si de todas formas voy a morir”.
Así que dejó de esforzarse y se hundió rápidamente en la nata.

La otra, más tenaz, pensó: “Aunque no pueda avanzar, lucharé hasta el final. 
No me rendiré antes de tiempo”. Así que siguió moviéndose sin descanso, pataleando 
y agitando sus patas sin cesar. Horas más tarde, su esfuerzo provocó un milagro: 
la nata se convirtió en mantequilla. La rana, sorprendida, dio un salto, 
llegó al borde del recipiente y logró escapar croando feliz rumbo a casa."""),
  (3, 'LA TORTUGA Y EL ANTÍLOPE', """Había una vez un antílope que se enorgullecía de su gran velocidad.
Un día, una tortuga decidió darle una lección y lo desafió a una carrera. 
El antílope, confiado y burlón, aceptó de inmediato.Antes del reto, 
la tortuga reunió a sus hermanas y las colocó a lo largo del camino, indicándoles que, 
cuando el antílope pasara y preguntara si ella estaba ahí, respondieran con un “Sí, aquí estoy”.

El día de la carrera, la tortuga propuso al antílope que, como era tan pequeña, 
él le preguntara de vez en cuando si seguía allí, a lo que ella respondería. 
El antílope aceptó, seguro de que no tenía nada que temer.

La carrera comenzó, y el antílope salió disparado. Pronto preguntó: “Amiga, ¿estás ahí?”, 
y escuchó sorprendido: “Sí, aquí estoy”. Volvió a acelerar, preguntó de nuevo más adelante, 
y otra vez recibió la misma respuesta.
Desconcertado, siguió corriendo, hasta que al llegar a la meta vio a la tortuga celebrando su llegada. 
Desde entonces, el orgulloso antílope aprendió que no todo es velocidad, y que la astucia también corre rápido."""),
  (4, 'EL ÚLTIMO MOHICANO', """Era un hombre endurecido por la vida desde su juventud, habituado a la fatiga y las dificultades. 
Vestía un sayo de cazador verde con vivos amarillos descoloridos 
y llevaba en la cabeza un gorro de piel ya muy gastado. En su cinturón adornado 
con cuentas de madreperla colgaba un cuchillo, y sus pies calzaban mocasines de piel 
de gamo al estilo indígena. Bajo el sayo se asomaban unas polainas altas del mismo 
material, atadas con lazos y nervios de corzo. Un cuerno para pólvora, una bolsa 
para municiones y un largo rifle completaban su equipo.

Sus ojos, pequeños y agudos, se movían sin cesar, como si siempre estuviera alerta, 
ya fuera en busca de una presa o pendiente de un enemigo oculto. Sin embargo, 
esa vigilancia constante no le restaba autenticidad: su rostro no mostraba falsedad 
ni afectación alguna, sino que reflejaba con claridad una honradez firme y natural."""),
  (5, 'EL PRINCIPITO', """El zorro le dice al principito que, si lo domestica, su vida cambiará: 
aprenderá a reconocer sus pasos entre todos los demás, y los campos de trigo, 
antes vacíos de sentido, le recordarán su cabello dorado. Así, el zorro 
sentirá alegría con el viento entre las espigas, porque le hablarán de su amigo. 
Le ruega que lo domestique, pero el principito duda, pues tiene poco tiempo: 
debe encontrar amigos y conocer muchas cosas. El zorro le responde que solo se
conoce bien lo que se domestica, que los hombres ya no tienen tiempo para hacer
amigos porque todo lo quieren comprar, pero no existen mercaderes de amistad. 
Para tener un amigo, hay que crear lazos.

Le explica que el primer paso es la paciencia: sentarse juntos sin hablar, 
acercándose poco a poco cada día. Al día siguiente, el zorro le dice que habría 
sido mejor venir a la misma hora, porque entonces podría prepararse para la felicidad, 
anticiparla, sentirla crecer. Eso es lo que hacen los ritos: hacen especial 
una hora o un día. Al despedirse, el zorro le entrega su secreto, simple y profundo: 
“no se ve bien sino con el corazón; lo esencial es invisible a los ojos”."""),
  (6, 'Y COLORÍN COLORADO...', """En la clase de Manuel, la maestra contó un cuento para enseñar la diferencia entre ser 
egoísta y ser generoso. Narró que un peregrino visitó un pueblo en China donde la gente, 
aunque rodeada de alimentos, tenía aspecto hambriento. Todos intentaban comer con 
palillos tan largos como remos, pero no lograban llevarse nada a la boca.

El peregrino siguió su camino, cruzó un río, una montaña y llegó a un valle hermoso, 
con otro pueblo lleno de belleza. Allí también había una gran mesa con manjares y palillos largos, 
pero todos lucían felices y saludables. La diferencia era que, en este lugar, 
cada persona usaba sus palillos para alimentar a quien tenía enfrente.
El peregrino se sentó luego a la orilla del río y, al mirar el agua clara, 
pensó: “Los del primer pueblo eran egoístas, y los de este viven como hermanos”.
Y la maestra terminó el cuento con su frase favorita: “Y colorín colorado, 
este cuento se ha acabado”, como lo hacía su abuela. Pero Manuel, encantado, le pidió que siguiera.

—“Por favor”, “señorita”, siga más.
—Pero si ya se ha acabado —respondió ella con una sonrisa—. 
Ahora, a jugar al recreo."""),
  (7, 'MOZART', """Wolfgang Amadeus Mozart tenía un gran sentido del humor, y también una extraordinaria nariz.
Él bromeaba a menudo sobre las dimensiones de su apéndice nasal.Con el fin de gastar una broma 
al compositor Franz Joseph Haydn, le hizo la siguiente apuesta:

- Maestro, ¿a que no podéis tocar estos compases que he compuesto?
Haydn se sentó al piano y empezó a ejecutar aquellas notas, sin problemas…, 
hasta que tuvo que pararse y dijo:

- No puedo continuar, porque aquí en medio hay una nota para la que
me faltan dedos, ya que tengo ambas manos ocupadas.
Mozart rió divertido, y le dijo: Dejadme…

Se sentó y tocó su propia creación, y cuando llegó a la nota que
quedaba suelta y no había forma de tocarla por estar todos los dedos
ocupados, agachó la cabeza y la tocó con su nariz. Tras esto, ambos rieron, y dijo Haydn:
- Tocáis con toda el alma, pero también con todo el cuerpo, sin olvidar la nariz…"""),
  (8, 'EL COLMILLO BLANCO', """Aquella noche los dos amigos acamparon temprano. Los perros del trineo daban
señales de estar rendidos. Los hombres se acostaron pronto, después de que Bill
cuidara de que los perros quedaran atados y a distancia uno de otro para que no
pudieran roer las correas del vecino.

Pero los lobos iban atreviéndose a acercarse, y más de una vez nuestros viajeros
fueron despertados por ellos. Tan cerca los tenían, que los perros comenzaron a
mostrarse locos de terror, y fue necesario ir renovando y aumentando de cuando el
cuando el fuego de la hoguera a fin de mantener a los lobos a una distancia segura.

-Varias veces he oído contar a los marineros cómo los tiburones siguen a los
barcos -dijo después de añadir leña a la hoguera-. Los lobos son los tiburones de la
tierra. Saben lo que hacen mucho mejor que nosotros. Siguen nuestra pista porque
saben que acabarán por apoderarse de nosotros. Seguro que nos cazan.
-¡Basta! Cuando un hombre dice que lo van a devorar, ya está andado la mitad del
camino. Y tú estás ya medio comido, sólo por hablar tanto que lo vas a ser."""),
  (9, 'TINTÍN, EL NIÑO AVISPA', """Tintín volvía a casa sin merienda porque, como casi siempre, un niño mayor se la había 
quitado amenazándolo. Enfadado, se sentó en el parque, pero pronto se distrajo observando 
las flores. Entonces vio una avispa y se asustó. Al apartarse, pensó en lo curioso que era que 
algo tan pequeño como una avispa pudiera causar tanto miedo. Comprendió que no hacía falta 
ser fuerte para defenderse, sino saber cómo asustar a los demás.

Esa noche, pensó en qué cosas podían dar miedo a los abusones y preparó su propia “picadura”. 
Al día siguiente, ya no caminaba cabizbajo: se sentía valiente y seguro. Uno de los abusones 
se comió un bocadillo picantísimo y no quiso volver a probar su comida. A otro le recordó los
teléfonos de sus padres y profesores para advertirle de las consecuencias. Y a otro más le 
entregó una tarjeta escrita por un policía amigo, advirtiéndole que no lo robara.

Gracias a su ingenio, los abusones empezaron a dejarle en paz. Solo una vez tuvo que cumplir 
una amenaza, y el castigo fue tal que aquel niño terminó protegiéndolo. Así, Tintín se convirtió 
en una pequeña avispa valiente: no necesitaba pelear, solo saber cómo defenderse."""),
  (10, 'LOS PERRITOS', """Los peritios son unos animales que vivían en la Atlántida. Eran mitad ciervo, mitad ave. Tenían la
cabeza y las patas del ciervo. En cuanto al cuerpo, era como el de un pájaro con sus alas y
plumas. Lo sorprendente de estos animales consiste en que cuando les daba el sol, su
sombra era la de un hombre. Algunos piensan que los peritios son espíritus de personas que
murieron sin que les perdonaran alguna cosa mal hecha.

Se les ha sorprendido comiendo tierra seca. Volaban en bandadas a gran altura.
Los peritios eran temibles enemigos de los hombres. Parece ser que
cuando lograban matar a un hombre, hacían coincidir su sombra con el
hombre muerto y alcanzaban el perdón. Después se revolcaban en la
sangre y luego huían hacia las alturas, desapareciendo.
No existen armas para luchar con los peritios, si bien el animal no
puede matar a más de un hombre. Nadie ha podido ver nunca un peritio
porque son animales inventados; nunca existieron.""")
]

con = sql.connect(bd_path)
cur = con.cursor()

cur.executemany('INSERT INTO lecturas VALUES(?, ?, ?)', lecturas)
con.commit()

cur.close()
con.close()