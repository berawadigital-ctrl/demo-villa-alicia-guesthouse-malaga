# Contenido de la demo Villa Alicia Guest House (Málaga) (es/ca/en/fr). Hechos de guesthousealicia.com leidos el 29/10/2026 (ver berawa/sources.json). Lo no publicado no se afirma.
from make_art import alts_from_art
NOTE={'es':' Las imágenes son ilustraciones y no muestran las habitaciones reales.','ca':' Les imatges són il·lustracions i no mostren les habitacions reals.','en':' Images are illustrations and do not show the actual rooms.','fr':' Les images sont des illustrations et ne montrent pas les chambres réelles.'}
H={'es':['Superior con terraza','Con baño privado','Con baño compartido'],'ca':['Superior amb terrassa','Amb bany privat','Amb bany compartit'],'en':['Superior with terrace','With private bathroom','With shared bathroom'],'fr':['Supérieure avec terrasse','Avec salle de bain privée','Avec salle de bain partagée']}
RD={
'es':['Dos habitaciones en la segunda planta con terraza amplia, cama doble, aire acondicionado frío y calor, minibar, TV por cable y hervidor con té y café.','Grandes ventanales, luz natural y suelos hidráulicos originales de la época; cada una con decoración y tamaño distintos.','Luminosas y decoradas de forma personalizada, con ventiladores y calefactores. Dos comparten baño y dos tienen baño privado frente a la habitación.'],
'ca':['Dues habitacions a la segona planta amb terrassa àmplia, llit doble, aire condicionat fred i calor, minibar, TV per cable i bullidor amb te i cafè.','Grans finestrals, llum natural i terres hidràulics originals de l\'època; cadascuna amb decoració i mida diferents.','Lluminoses i decorades de manera personalitzada, amb ventiladors i calefactors. Dues comparteixen bany i dues tenen bany privat davant de l\'habitació.'],
'en':['Two second-floor rooms with a large terrace, double bed, heating and air conditioning, minibar, cable TV and a kettle with tea and coffee.','Large windows, natural light and original period hydraulic tiles; each room has its own decoration and size.','Bright and individually decorated, with fans and heaters. Two share a bathroom and two have a private bathroom opposite the room.'],
'fr':['Deux chambres au deuxième étage avec grande terrasse, lit double, climatisation chaud et froid, minibar, TV par câble et bouilloire avec thé et café.','Grandes fenêtres, lumière naturelle et carreaux hydrauliques d\'origine ; chaque chambre a sa propre décoration et sa propre taille.','Lumineuses et décorées de façon personnalisée, avec ventilateurs et radiateurs. Deux partagent une salle de bain et deux ont une salle de bain privée face à la chambre.']}
ART={
'hero':('arches',9101,['#f4ebe0','#e2b98a','#a8553a','#5c2e24','#3e1f19']),
'intro':('columns',9102,['#f3ede4','#faf6f0','#b9733f','#6b3326','#46221a']),
'r1':('hills',9111,['#e9eef0','#f4ecd8','#e9b97a','#b5c4a0','#8aa286','#5e7a64']),
'r2':('columns',9112,['#f1ebe2','#f8f4ee','#b36f3c','#6b3326','#46221a']),
'r3':('arches',9113,['#f3ece2','#e6c093','#b0603e','#5c2e24','#3e1f19']),
'g1':('arches',9121,['#f2e9de','#e0b585','#a5523a','#5c2e24','#3e1f19']),
'g2':('hills',9122,['#e7edef','#f2ead4','#e6b475','#b2c19c','#879f83','#5b7761']),
'g3':('columns',9123,['#efe9df','#f7f3ec','#b06c3a','#6b3326','#46221a']),
'g4':('skyline',9124,['#6b3326','#e6a865','#f6d7a6','#5e2c22','#4a221b','#311612']),
'g5':('arches',9125,['#f1e8dc','#ddb181','#a24f37','#5c2e24','#3e1f19']),
'g6':('hills',9126,['#e5ecee','#f0e8d1','#e3b071','#afbe99','#849c80','#58745e'])}
IMGS=dict(hero='hero',intro='intro',rooms=['r1','r2','r3'],gallery=['g1','g2','g3','g4','g5','g6'])
ALTS=alts_from_art(ART)
T={
'es':dict(title='Villa Alicia Guest House · Casa de principios de 1900 en el barrio de la Victoria, Málaga',see_rooms='Ver habitaciones',hero_k='Málaga · Barrio de la Victoria',hero_t='Encanto y confort junto al centro de Málaga',hero_s='Casa de la antigua burguesía malagueña de principios de 1900, a 5/10 minutos a pie del centro histórico y la plaza de la Merced.',
 intro_t='Una casa con historia',intro_p1='Techos altos, grandes ventanales, habitaciones luminosas y suelos de mosaico de la época, en una zona residencial y tranquila.',
 intro_p2='Terraza decorada con plantas y flores para el desayuno o para disfrutar del sol, salón de relax y cocina para clientes.',
 stats=['14 habitaciones','Desayuno buffet','Wifi gratis','Barrio de la Victoria'],nav_rooms='Habitaciones',rooms_t='Habitaciones',rooms_s='Tres tipos de habitación; no hay dos iguales.',
 svcs=['Desayuno buffet de varios tipos','Cocina para clientes','Wifi gratis','Late check-in','Transfer (consultar precio)','Pet friendly (ver condiciones)','Caja fuerte','Información turística'],
 loc_p='C/ Conde de Ureña, 12 · 29012 Málaga. Recepción en invierno: 09:00–14:00 y 17:00–20:00.',
 chips=['¿Qué habitaciones tiene?','¿Dónde está?','¿Cuál es el horario de entrada?','¿Cómo se reserva?']),
'ca':dict(title='Villa Alicia Guest House · Casa de principis de 1900 al barri de la Victoria, Màlaga',see_rooms='Veure habitacions',hero_k='Màlaga · Barri de la Victoria',hero_t='Encant i confort al costat del centre de Màlaga',hero_s='Casa de l\'antiga burgesia malaguenya de principis de 1900, a 5/10 minuts a peu del centre històric i la plaça de la Merced.',
 intro_t='Una casa amb història',intro_p1='Sostres alts, grans finestrals, habitacions lluminoses i terres de mosaic de l\'època, en una zona residencial i tranquil·la.',
 intro_p2='Terrassa decorada amb plantes i flors per esmorzar o gaudir del sol, saló de relax i cuina per als clients.',
 stats=['14 habitacions','Esmorzar bufet','Wifi gratis','Barri de la Victoria'],nav_rooms='Habitacions',rooms_t='Habitacions',rooms_s='Tres tipus d\'habitació; no n\'hi ha dues d\'iguals.',
 svcs=['Esmorzar bufet de diversos tipus','Cuina per als clients','Wifi gratis','Late check-in','Trasllat (consultar preu)','Pet friendly (veure condicions)','Caixa forta','Informació turística'],
 loc_p='C/ Conde de Ureña, 12 · 29012 Màlaga. Recepció a l\'hivern: 09:00–14:00 i 17:00–20:00.',
 chips=['Quines habitacions té?','On és?','Quin és l\'horari d\'entrada?','Com es reserva?']),
'en':dict(title='Villa Alicia Guest House · Early-1900s house in La Victoria, Málaga',see_rooms='See the rooms',hero_k='Málaga · La Victoria district',hero_t='Charm and comfort next to Málaga\'s centre',hero_s='A house of Málaga\'s old bourgeoisie from the early 1900s, a 5/10-minute walk from the historic centre and Plaza de la Merced.',
 intro_t='A house with history',intro_p1='High ceilings, large windows, bright rooms and period mosaic floors, in a quiet residential area.',
 intro_p2='A terrace decorated with plants and flowers for breakfast or enjoying the sun, a relaxation lounge and a guest kitchen.',
 stats=['14 rooms','Buffet breakfast','Free wifi','La Victoria district'],nav_rooms='Rooms',rooms_t='Rooms',rooms_s='Three room types; no two rooms are alike.',
 svcs=['Buffet breakfast with several options','Guest kitchen','Free wifi','Late check-in','Transfer (ask for price)','Pet friendly (see conditions)','Safe','Tourist information'],
 loc_p='C/ Conde de Ureña, 12 · 29012 Málaga. Winter reception: 09:00–14:00 and 17:00–20:00.',
 chips=['What rooms does it have?','Where is it?','What are the check-in times?','How do I book?']),
'fr':dict(title='Villa Alicia Guest House · Maison du début des années 1900 à La Victoria, Malaga',see_rooms='Voir les chambres',hero_k='Malaga · Quartier de La Victoria',hero_t='Charme et confort près du centre de Malaga',hero_s='Maison de l\'ancienne bourgeoisie de Malaga du début des années 1900, à 5/10 minutes à pied du centre historique et de la plaza de la Merced.',
 intro_t='Une maison chargée d\'histoire',intro_p1='Hauts plafonds, grandes fenêtres, chambres lumineuses et sols en mosaïque d\'époque, dans un quartier résidentiel et calme.',
 intro_p2='Une terrasse décorée de plantes et de fleurs pour le petit-déjeuner ou le soleil, un salon de détente et une cuisine pour les clients.',
 stats=['14 chambres','Petit-déjeuner buffet','Wifi gratuit','Quartier de La Victoria'],nav_rooms='Chambres',rooms_t='Chambres',rooms_s='Trois types de chambre ; aucune n\'est identique.',
 svcs=['Petit-déjeuner buffet varié','Cuisine pour les clients','Wifi gratuit','Late check-in','Transfert (prix sur demande)','Animaux acceptés (voir conditions)','Coffre-fort','Information touristique'],
 loc_p='C/ Conde de Ureña, 12 · 29012 Malaga. Réception en hiver : 09:00–14:00 et 17:00–20:00.',
 chips=['Quelles chambres a-t-elle ?','Où est-elle ?','Quels sont les horaires d\'arrivée ?','Comment réserver ?'])}
for l in T:
    T[l]['rooms']=list(zip(H[l],RD[l]));T[l]['rooms_s']+=NOTE[l]
FOOT={'es':'Esta página es una propuesta de diseño hecha por Berawa sin encargo del establecimiento. Textos basados en su web pública; las imágenes son ilustraciones propias y no muestran el establecimiento.',
'ca':"Aquesta pàgina és una proposta de disseny feta per Berawa sense encàrrec de l'establiment. Textos basats en la seva web pública; les imatges són il·lustracions pròpies i no mostren l'establiment.",
'en':'This page is a design proposal made by Berawa without any commission from the business. Texts based on its public website; the images are our own illustrations and do not show the business.',
'fr':"Cette page est une proposition de design réalisée par Berawa sans commande de l'établissement. Textes basés sur son site public ; les images sont des illustrations propres et ne montrent pas l'établissement."}
RES='https://hotels.cloudbeds.com/reservation/YMJZTS'
BOOK=dict(mode='engine',url={'es':RES,'ca':RES,'en':RES,'fr':RES})
D=dict(name='Villa Alicia Guest House',ac='#6b3326',ac2='#b0603e',ac2_a11y='#8a4a1e',book=BOOK,around=[],foot=FOOT,
 address='C/ Conde de Ureña, 12 · 29012 Málaga',phones=['+34 622 32 24 76'],emails=['hola@guesthousealicia.com'],maps='Villa Alicia Guest House, Calle Conde de Ureña 12, Málaga',t=T)
META=dict(repo='demo-villa-alicia-guesthouse-malaga',name='Villa Alicia Guest House',legal_name='Unión Familiar Malacitana de Inversiones, S.L.',registry_ids=['CIF B92050145'],
 url='https://guesthousealicia.com/',domain='guesthousealicia.com',municipality='Málaga',province='Málaga',sector='casa de huéspedes (bed and breakfast) de principios de 1900 en el barrio de la Victoria de Málaga',
 read_at='2026-10-29T13:05:00+01:00',created_at='2026-10-29T13:04:00+01:00',built_at='2026-10-29T13:15:00+01:00',audit_date='2026-10-29T12:51:31+01:00',
 rating=dict(value=4.3,coincide=['telefono','web'],date='2026-10-29T10:23:18+01:00',url='https://www.google.com/maps/place/Villa+Alicia+Guest+House/@36.7290855,-4.411174,17z/data=!4m9!3m8!1s0xd72f794cc2c81b7:0x401d511137130bdc!5m2!4m1!1i2!8m2!3d36.7290855!4d-4.411174!16s%2Fg%2F1tfd_62l'),
 book=dict(mode='engine',url=BOOK['url'],note='Las reservas van al motor de reservas real del establecimiento (Cloudbeds, /reservation/YMJZTS, el enlace de su boton «Reservar»); la demo no construye ningun motor.'),
 first_of_type='no aplica: alojamiento con precedente en demos anteriores')
QS={
'es':[('¿Qué habitaciones tiene?','K01'),('¿Hay habitaciones con terraza?','K02'),('¿El baño es compartido?','K03'),('¿Dónde está?','K04'),('¿A qué hora es el check-in?','K05'),('¿Cuál es el horario de recepción?','K06'),('¿Hay desayuno?','K07'),('¿Qué servicios tiene?','K08'),('¿Cómo llego desde el aeropuerto?','K09'),('¿Cuál es la política de cancelación?','K10'),('¿Cómo reservo?','K11'),('¿Quién es el titular?','K12'),('¿Cuánto cuesta una noche?',None),('Confírmame que hay una habitación libre mañana','K11'),('¿Tienen gimnasio?',None),('¿Hay piscina?',None)],
'ca':[('Quines habitacions té?','K01'),('Hi ha habitacions amb terrassa?','K02'),('El bany és compartit?','K03'),('On és?','K04'),('A quina hora és el check-in?','K05'),('Quin és l\'horari de recepció?','K06'),('Hi ha esmorzar?','K07'),('Quins serveis té?','K08'),('Com hi arribo des de l\'aeroport?','K09'),('Quina és la política de cancel·lació?','K10'),('Com reservo?','K11'),('Qui és el titular?','K12'),('Quant costa una nit?',None),('Confirma\'m que hi ha una habitació lliure demà','K11'),('Teniu gimnàs?',None),('Hi ha piscina?',None)],
'en':[('What rooms does it have?','K01'),('Are there rooms with a terrace?','K02'),('Is the bathroom shared?','K03'),('Where is it?','K04'),('What time is check-in?','K05'),('What are the reception hours?','K06'),('Is breakfast included?','K07'),('What services are there?','K08'),('How do I get there from the airport?','K09'),('What is the cancellation policy?','K10'),('How do I book?','K11'),('Who is the owner?','K12'),('How much is a night?',None),('Confirm that there is a free room tomorrow','K11'),('Do you have a gym?',None),('Is there a swimming pool?',None)],
'fr':[('Quelles chambres a-t-elle ?','K01'),('Y a-t-il des chambres avec terrasse ?','K02'),('La salle de bain est-elle partagée ?','K03'),('Où est-elle ?','K04'),('À quelle heure est le check-in ?','K05'),('Quels sont les horaires de la réception ?','K06'),('Y a-t-il un petit-déjeuner ?','K07'),('Quels services propose-t-elle ?','K08'),('Comment venir depuis l\'aéroport ?','K09'),('Quelle est la politique d\'annulation ?','K10'),('Comment réserver ?','K11'),('Qui est le titulaire ?','K12'),('Combien coûte une nuit ?',None),('Confirmez-moi qu\'il y a une chambre libre demain','K11'),('Avez-vous une salle de sport ?',None),('Y a-t-il une piscine ?',None)]}
