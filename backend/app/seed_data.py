"""Datos iniciales. Las coordenadas salen de OpenStreetMap.

OJO: precios, horarios y detalles pueden cambiar. Revisá el contenido antes de publicarlo.
price_level: 0 = gratis, 1-3 = de más barato a más caro, None = "consultar".
duration: None cuando no tiene sentido (restaurantes, supermercados): la tarjeta no la muestra.
"""

DESTINATIONS = [
    {
        "slug": "punta-del-este",
        "name": "Punta del Este",
        "country": "Uruguay",
        "latitude": -34.9632,
        "longitude": -54.9440,
        "timezone": "America/Montevideo",
        "activities": [
            {
                "slug": "la-mano-playa-brava",
                "title": "La Mano (Monumento al Ahogado)",
                "category": "paseo",
                "description": (
                    "El símbolo de Punta del Este: cinco dedos gigantes que salen de la arena, "
                    "obra del artista chileno Mario Irarrázabal. La foto obligada del viaje, "
                    "con la Playa Brava de fondo."
                ),
                "zone": "Playa Brava",
                "latitude": -34.95789,
                "longitude": -54.93729,
                "price_level": 0,
                "duration": "30 min",
                "indoor": False,
            },
            {
                "slug": "puerto-punta-del-este",
                "title": "Puerto y lobos marinos",
                "category": "paseo",
                "description": (
                    "Caminá entre yates, pescadores y restaurantes. Con suerte vas a ver lobos "
                    "marinos que se acercan al muelle a buscar restos de pescado. Lindo para ir "
                    "a la tarde."
                ),
                "zone": "Puerto",
                "latitude": -34.96192,
                "longitude": -54.94944,
                "price_level": 0,
                "duration": "1 a 2 horas",
                "indoor": False,
            },
            {
                "slug": "isla-de-lobos",
                "title": "Excursión a Isla de Lobos",
                "category": "naturaleza",
                "description": (
                    "Una travesía en barco hasta esta reserva natural, hogar de una gran colonia "
                    "de lobos marinos. Las salidas parten desde el puerto y dependen del estado "
                    "del mar."
                ),
                "zone": "Salida desde el Puerto",
                "latitude": -35.02724,
                "longitude": -54.88369,
                "price_level": 2,
                "duration": "Medio día",
                "indoor": False,
            },
            {
                "slug": "isla-gorriti",
                "title": "Isla Gorriti",
                "category": "playa",
                "description": (
                    "A pocos minutos en lancha desde el puerto: playas de agua tranquila, "
                    "senderos y restos de fortificaciones históricas. Un plan perfecto para "
                    "pasar el día."
                ),
                "zone": "Salida desde el Puerto",
                "latitude": -34.95458,
                "longitude": -54.97162,
                "price_level": 1,
                "duration": "Día completo",
                "indoor": False,
            },
            {
                "slug": "casapueblo",
                "title": "Casapueblo y atardecer",
                "category": "cultura",
                "description": (
                    "La casa-taller blanca de Carlos Páez Vilaró sobre los acantilados de Punta "
                    "Ballena. Se visita su museo y es uno de los lugares clásicos para ver el "
                    "atardecer sobre el mar."
                ),
                "zone": "Punta Ballena",
                "latitude": -34.90876,
                "longitude": -55.04459,
                "price_level": None,
                "duration": "2 a 3 horas",
                "indoor": False,
            },
            {
                "slug": "playa-mansa",
                "title": "Playa Mansa",
                "category": "playa",
                "description": (
                    "Aguas más calmas, del lado del río, con rambla para caminar y muy buenos "
                    "atardeceres. Ideal para ir con chicos o cuando la Brava está con mucho "
                    "viento."
                ),
                "zone": "Península",
                "latitude": -34.94553,
                "longitude": -54.94379,
                "price_level": 0,
                "duration": "Medio día",
                "indoor": False,
            },
            {
                "slug": "faro-punta-del-este",
                "title": "Faro de Punta del Este",
                "category": "paseo",
                "description": (
                    "El extremo sur de la península. Un paseo tranquilo entre casas bajas, con "
                    "vista al mar y la Iglesia de la Candelaria a pocos pasos."
                ),
                "zone": "Península",
                "latitude": -34.96886,
                "longitude": -54.95164,
                "price_level": 0,
                "duration": "1 hora",
                "indoor": False,
            },
            {
                "slug": "playa-montoya",
                "title": "Playa Montoya",
                "category": "playa",
                "description": (
                    "En La Barra, con olas que atraen a los surfistas y un ambiente relajado y "
                    "joven. Cerca de los bares y restaurantes de la zona."
                ),
                "zone": "La Barra",
                "latitude": -34.91317,
                "longitude": -54.84391,
                "price_level": 0,
                "duration": "Medio día",
                "indoor": False,
            },
            {
                "slug": "puente-de-la-barra",
                "title": "Puente ondulante de La Barra",
                "category": "paseo",
                "description": (
                    "El famoso puente ondulado sobre el arroyo Maldonado, símbolo de La Barra. "
                    "Una parada clásica para ver el entorno y sacar fotos."
                ),
                "zone": "La Barra",
                "latitude": -34.91100,
                "longitude": -54.87286,
                "price_level": 0,
                "duration": "30 min",
                "indoor": False,
            },
            {
                "slug": "arboretum-lussich",
                "title": "Arboretum Lussich",
                "category": "naturaleza",
                "description": (
                    "Un bosque con especies de todo el mundo, plantado hace más de un siglo por "
                    "Antonio Lussich, con senderos y miradores. Mucha sombra para los días de "
                    "calor."
                ),
                "zone": "Punta Ballena",
                "latitude": -34.87035,
                "longitude": -55.02881,
                "price_level": None,
                "duration": "1 a 2 horas",
                "indoor": False,
            },
            {
                "slug": "museo-ralli",
                "title": "Museo Ralli",
                "category": "cultura",
                "description": (
                    "Museo de arte latinoamericano contemporáneo con entrada gratuita. Un plan "
                    "ideal para los días de lluvia o de mucho sol."
                ),
                "zone": "Beverly Hills",
                "latitude": -34.92967,
                "longitude": -54.92705,
                "price_level": 0,
                "duration": "1 a 2 horas",
                "indoor": True,
            },
            {
                "slug": "fundacion-atchugarry",
                "title": "Fundación Pablo Atchugarry",
                "category": "cultura",
                "description": (
                    "Parque de esculturas al aire libre y museo del artista uruguayo Pablo "
                    "Atchugarry, en Manantiales. Arte en medio de la naturaleza."
                ),
                "zone": "Manantiales",
                "latitude": -34.86506,
                "longitude": -54.82509,
                "price_level": None,
                "duration": "2 horas",
                "indoor": False,
            },
            {
                "slug": "feria-plaza-artigas",
                "title": "Feria artesanal de Plaza Artigas",
                "category": "paseo",
                "description": (
                    "Artesanías, joyas y recuerdos en la feria de la Plaza Artigas, a pasos de "
                    "la peatonal Gorlero. Más animada en temporada alta."
                ),
                "zone": "Centro",
                "latitude": -34.96311,
                "longitude": -54.94380,
                "price_level": 0,
                "duration": "1 hora",
                "indoor": False,
            },
            {
                "slug": "museo-del-mar",
                "title": "Museo del Mar",
                "category": "cultura",
                "description": (
                    "Un museo dedicado al mundo marino, en La Barra. Buen plan para los días de "
                    "lluvia o de mucho viento."
                ),
                "zone": "La Barra",
                "latitude": -34.89895,
                "longitude": -54.87038,
                "price_level": None,
                "duration": "1 hora",
                "indoor": True,
            },
            # ── Restaurantes (ejemplos): sin precio ni horario, que cambian seguido ──
            {
                "slug": "zazu-puerto",
                "title": "Zazú Puerto",
                "category": "restaurante",
                "description": (
                    "Restaurante sobre la rambla del puerto, conocido por su buen servicio y su "
                    "decoración original. Entre lo más recomendado: risotto, pulpo, salmón y postres."
                ),
                "zone": "Puerto",
                "latitude": -34.96538,  # Rambla Gral. Artigas 652
                "longitude": -54.94979,
                "price_level": None,
                "duration": None,
                "indoor": True,
            },
            {
                "slug": "lo-de-tere",
                "title": "Lo de Tere",
                "category": "restaurante",
                "description": (
                    "Restaurante del puerto con una cocina centrada en productos uruguayos y en "
                    "mariscos y pescados del Atlántico y de las lagunas de la zona. Su salón mira al puerto."
                ),
                "zone": "Puerto",
                "latitude": -34.96367,
                "longitude": -54.94650,
                "price_level": None,
                "duration": None,
                "indoor": True,
            },
            {
                "slug": "virazon",
                "title": "Virazón",
                "category": "restaurante",
                "description": (
                    "Restaurante junto al puerto, con vista a los botes y decoración marinera. Los "
                    "pescados y mariscos son los protagonistas de la carta."
                ),
                "zone": "Puerto",
                "latitude": -34.96037,
                "longitude": -54.94534,
                "price_level": None,
                "duration": None,
                "indoor": True,
            },
            {
                "slug": "la-posta-del-cangrejo",
                "title": "La Posta del Cangrejo",
                "category": "restaurante",
                "description": (
                    "El restaurante más tradicional de La Barra: cocina de inspiración francesa con "
                    "sabores del mar."
                ),
                "zone": "La Barra",
                "latitude": -34.91581,
                "longitude": -54.85768,
                "price_level": None,
                "duration": None,
                "indoor": True,
            },
            # ── Supermercados ──
            # No se marcan como "bajo techo": ese filtro es para planes de un día de lluvia.
            {
                "slug": "devoto-express-gorlero",
                "title": "Devoto Express (Gorlero)",
                "category": "supermercado",
                "description": (
                    "Supermercado de la cadena Devoto sobre la avenida Gorlero, en pleno centro de la "
                    "península. Práctico para comprar lo básico."
                ),
                "zone": "Península",
                "latitude": -34.96209,
                "longitude": -54.94380,
                "price_level": None,
                "duration": None,
                "indoor": False,
            },
            {
                "slug": "disco-peninsula",
                "title": "Disco (Península)",
                "category": "supermercado",
                "description": (
                    "Supermercado Disco en la península, a pocas cuadras del puerto. Útil para "
                    "abastecerte si te alojás en el centro."
                ),
                "zone": "Península",
                "latitude": -34.96617,
                "longitude": -54.94689,
                "price_level": None,
                "duration": None,
                "indoor": False,
            },
            {
                "slug": "tienda-inglesa-punta-shopping",
                "title": "Tienda Inglesa (Punta Shopping)",
                "category": "supermercado",
                "description": (
                    "Una de las sucursales más grandes de Tienda Inglesa, en la zona del Punta "
                    "Shopping. Mucha variedad para abastecerse durante la estadía."
                ),
                "zone": "Av. Roosevelt",
                "latitude": -34.94031,
                "longitude": -54.93515,
                "price_level": None,
                "duration": None,
                "indoor": False,
            },
            {
                "slug": "devoto-roosevelt",
                "title": "Devoto (Av. Roosevelt)",
                "category": "supermercado",
                "description": (
                    "Hipermercado Devoto sobre la avenida Roosevelt, del lado de Playa Mansa. Ideal "
                    "para una compra grande."
                ),
                "zone": "Av. Roosevelt",
                "latitude": -34.93316,
                "longitude": -54.93954,
                "price_level": None,
                "duration": None,
                "indoor": False,
            },
            {
                "slug": "tienda-inglesa-la-barra",
                "title": "Tienda Inglesa (La Barra)",
                "category": "supermercado",
                "description": "Supermercado Tienda Inglesa en La Barra. Práctico si te alojás por esa zona.",
                "zone": "La Barra",
                "latitude": -34.91582,
                "longitude": -54.85464,
                "price_level": None,
                "duration": None,
                "indoor": False,
            },
        ],
    },
]
