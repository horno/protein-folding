0.1
# Introducció
- Plantejament problema general
     
- Plantejament metode d'estudi

# Context
- Parlar sobre les utilitats de plegar proteines

# Desenvolupament de la temàtica
- Diferents tipus de relaxacions del model

# Conclusions

# Referències

https://www.sciencedirect.com/topics/neuroscience/molecular-dynamics
https://slides.com/jonathonhope/comp4130-tech-talk#/3


El tema tractat en aquest informe és el de protein folding, plegar proteines.
Per donar una mica de background, les proteines són cadenes llargues d'aminoàcids
- | Funcions que fan les proteines

Per a que cada proteina pugui fer la seva funció ha de tenir una forma determinada.
Per aconseguir aquesta forma s'ha de plegar d'una forma específica, ja que quan
la proteina es crea està estirada, si està estirada no té la forma característica
i es diu que està "morta"



Les proteines poden ser cadenes tant de 10 aminoàcids (proteines simples), com
de 1000 o més aminoacids. Les formes de plegar una proteina són moltes, de fet,
massa. Creixen exponencialment amb la llargada de la cadena, i la forma que fa
que la proteina compleixi la seva funció normalment és una sola. En altres paraules,
s'ha de trobar l'agulla en el pallar de plegs possibles d'aquella proteina. 

El procés natural pel que les proteines es pleguen és un camp molt desconegut, 
es suposa que tota la informació sobre com plegar una proteina es troba en ella 
mateixa, és a dir, no hi ha cap "manual de l'Ikea" que utilitza la cèl·lula per 
plegar la proteina. El problema combinatori és tant difícil que no se sap com 
la cèl·lula adquereix l'estat de mínima energia per lesseves proteines, que és el
que les fa funcionals (amb altres configuracions es considera que la proteina 
està "morta").


- | El que es podria aconseguir si conseguissim plegar proteines en temps polinomial

Sent més realistes i específics, el que normalment es busca no és la forma de 
plegar una proteína en específic, sinó la forma d'entrellaçar i plegar varies
proteines per fer una estructura que compleixi la funció que volem. Si trobar
una configuració de plegament d'una proteina ja era extremadament difícil, això
ho és ordres de magnitud més, ja que s'ha de tenir en compte totes combinacions
de cada proteina per separat, més les interaccions de cada proteina amb totes 
les demés. 
Per si això no fos suficient, hi ha desenes de  factors que canvien la forma 
en que les proteines interactuen, alguns de molt determinants són la temperatura,
el líquid en el que estan suspeses, els tipus d'aminoacids que formen la proteina
i les càrregues elèctriques dels mateixos. 

- |Hi ha un camp que es centra en l'estudi de lo mencionat anteriorment, 
   es diu dinàmica de molècules (molecular dynamics)

Al no haver un procés directe per torbar la configuració de mínima energia, 
és a dir, la forma en que la proteina és funcional, el que s'acaba fent és
generar totes les configuracions possibles i mirar quina és la millor. No 
obstant, a la que la proteina deixa de ser absurdament petita, les combinacions
creixen tant que no hi ha cap ordinador actual capaç de realitzar els càlculs
en un temps que no superi la mort freda de l'univers.

Per trobar la forma de les proteines que existeixen en la natura, el que es
fa és * cristalitzar la proteina i fer una foto del seu estat.

Per trobar la configuració natural del pleg de les proteines que tenim al cos
es necessita fer un process que requereix molta recerca, molts diners, i temps.
El que es fa és cristalitzar la proteina (que pot portar mesos de recerca),
d'aquest cristall es fa una foto on es recrea en 3D.


Per proteines que ens agradaria crear per fer una funció específica (exemples
mencionats anteriorment) això no ho podem fer, l'hem de simular nosaltres mateixos.
El que s'acaba fent per aquests casos és utilitzar una combinació de tàctiques:
la creativitat humana, junt amb força computacional per generar combinacions,
guiada per unes heurístiques.
Aquestes heurístiques no es poden aplicar sempre, normalment són heurístiques
específiques per cada cas. Per exemple, si es vol fer una estructura a partir
de proteines plegades que tingui la funció de deixar passar globuls vermells
però no glòbuls blancs, es podria fer un estudi de conjunts de proteines que
facin funcions similars, i generar combinacions basades en modificacions 
d'aquelles proteines, etc, etc.
El que vull donar a entendre amb això és que el procés és molt tediós, i tenir
una forma de trobar les formes de plegar les proteines en temps polinomial 
seria una revolució mundial.



El problema de doblegar proteines (protein folding), com hem mencionat anteriorment
té un nombre de combinacions a provar que creix exponencialment a mesura que
creix la llargada de la proteina. Per tant, no es pot resoldre en temps polinomial,
no obstant, donada una una configuració, és trivial comprovar si és o no la
configuració d'energia mínima. Donades les premises anteriors, podem concloure
que és un problema NP-Hard (i perque es pot extrapolar en temps polinomial a un 
problema NP-Complet).

Com que és un camp que té moltíssim potencial, s'han fet múltiples relaxacions
del problema per poder estudiar-lo en més profunditat, i per generar heurístiques.
El problema general és el mencionat, plegar proteines formades per cadenes de 
24 possibles tipus d'aminoàcids proteinogènics en un espai tridimensional,
continu, amb centenars de variables ambientals que canvien la coherencia de 
les interaccions.
Tipus de relaxacions:
- Relaxació d'espai, ara en ves de ser continu serà discret:
   + Quadrícula 2D: ara els aminoàcids hauràn de col·locar-se sobre una graella 
   quadrículada bidimensional, és a dir, menys combinacions a teinr en compte.
   + Graella triangular 2D: el mateix que la quadrícula però amb una graella
   formada per triangles, més combinacions que l'anterior
   + Quadrícula 3D: els aminoàcids ara es podràn col·locar sobre una graella
   quadricular (cubs) de tres dimensions, més combinacions que l'anterior
   + Quadrícula 3D amb centres: mateixa graella que l'anterior però formada 
   per una graella triangular tridimensional, més combinacions que l'anterior

- Relaxació de variables: Redueix el nombre de variables a tenir en compte, com
per exemple, no tenir en compte la temperatura, o les iteraccions de les
càrregues elèctriques dels aminoàcids.

## Relaxació escollida
Una relaxació molt estudiada i molt simple per explicar el problema és el model
2D HP en quadrícula bidimensional. Aquest model només té 2 tipus d'aminoàcids, H
i P (d'aquí el nom HP). Això vol dir que una proteina serà una cadena formada
només per H i P (paraula formada per un diccionari E={H,P}estrella), per
exemple, una proteina podria ser la següent
                            HHPPHPHPPHHPH
o encara més senzill
                            HP

Les molecules H fan referència a les molècules hidrofòbiques i les P fan 
referència a les polars. Com el nom indica, les H no volen tenir res a veure
amb l'aigua, i les P (també es poden dir hidrofíliques) sí.
En el nostre cos les proteines estan suspeses en aigua (o majoritariament aigua)
, malgrat això, alguns aminoacids no poden estar en contacte amb ella (reaccionen),
mentre altres sí que poden. Quan les proteines es pleguen, les partícules H han
de quedar amagades a l'interior, i les P a l'exterior, d'aquesta forma les H no
estan en contacte amb el medi (aigua), i les P les protegeixen. 

Una forma de plegar una proteina, per exemple, seria aquesta:

                    P-P-P
                        |
                    P-H P
                    |   |
                    P-P-P

En aquest pleg, com es pot veure, l'aminoàcid H està al'interior, cobert per els
aminoàcids P. En aquest model el que es vol maximitzar és el nombre de de H que
estàn juntes (per qualsevol cantó), com més gran sigui
el nombre, més agrupades estan, i menys superfície d'elles està tocant l'exterior,
on hi ha el seu enemic, l'aigua.

## Observacions d'aquest problema 
- En aquest problema, al ser en una quadrícula, tots els aminoàcids que formen
la cadena (excepte els de la punta) tenen 2 veins inmutables (els que venen donats
per la cadena) i 2 veins mutables.
- La forma òptima de plegar una determinada proteina té la puntuació màxima.
- Donada una cadena de molecules, les H parelles
poden enllaçar-se només amb les imparelles, viceversa(ja que estan en una quarícula)
- La puntuació màxima (òptima, OPT) serà de la forma   
OPT <= 2·min{#H parells,#H imparells}. Explicació:
    + Cada enllaç H-H defineix un parell i un imparell
    + Cada parell i imparell pot tenir fins a 2 veins (no mutables)
    + Si hi ha més parells que imparells o viceversa, no es poden aprofitar, ja
   que no hi ha forma d'emparellar parells amb imparells

### Complexitat
Trobar el pleg de d'proteina que doni la puntuació òptima, fins i tot en aquesta
reducció del problema, és NP-Hard. Primer va ser
demostrat que per malles 3D ho era, i més tard que per les 2D també.













# Idees random que colocar
- Una bona analogia per entendre-ho és la seguent:
 De le mateixa forma que si tu tires una pilota muntanya avall, aquesta passarà
 d'un estat d'energina potencial elevat a un estat d'energia potencial mínim
 (quan finalment la pilota es pari). La proteina també té aquest estat d'energia
 mínim, a mesura que la proteina es plega d'una forma o d'una altra, té una
 energia determinada. La forma de plegar la proteina que té l'energia mínima, 
 és la forma en que la proteina és funcional.

- Si s'introdueix en un organisme una protenia que no té la configuració 
òptima no sol pot no servir, sinó que pot ser molt perjudicial, i pot portar a
resultats en cadena incontrolables 

- 23 aminoàcids proteinogènics



