"""Traducciones de las actividades de seed_data.py (que están en español), por `slug`.

Solo hace falta poner los campos que cambian: lo que falte se muestra en español
(por ejemplo, "Isla Gorriti" o "Playa Mansa" son nombres propios y no se traducen).
Idiomas: en (inglés), pt (portugués de Brasil), de (alemán).
"""

TRANSLATIONS: dict[str, dict[str, dict[str, str]]] = {
    "la-mano-playa-brava": {
        "en": {
            "title": "La Mano (The Hand)",
            "description": (
                "The symbol of Punta del Este: five giant fingers rising out of the sand, by Chilean "
                "artist Mario Irarrázabal. The must-have photo of the trip, with Playa Brava in the "
                "background."
            ),
            "duration": "30 min",
        },
        "pt": {
            "title": "La Mano (A Mão)",
            "description": (
                "O símbolo de Punta del Este: cinco dedos gigantes saindo da areia, obra do artista "
                "chileno Mario Irarrázabal. A foto obrigatória da viagem, com a Playa Brava ao fundo."
            ),
            "duration": "30 min",
        },
        "de": {
            "title": "La Mano (Die Hand)",
            "description": (
                "Das Wahrzeichen von Punta del Este: fünf riesige Finger, die aus dem Sand ragen, ein "
                "Werk des chilenischen Künstlers Mario Irarrázabal. Das Pflichtfoto jeder Reise, mit "
                "der Playa Brava im Hintergrund."
            ),
            "duration": "30 Min.",
        },
    },
    "puerto-punta-del-este": {
        "en": {
            "title": "Port and sea lions",
            "description": (
                "Stroll among yachts, fishermen and restaurants. With luck you'll spot sea lions "
                "coming up to the dock looking for scraps of fish. Lovely in the afternoon."
            ),
            "zone": "Port",
            "duration": "1 to 2 hours",
        },
        "pt": {
            "title": "Porto e lobos-marinhos",
            "description": (
                "Caminhe entre iates, pescadores e restaurantes. Com sorte, você verá lobos-marinhos "
                "se aproximando do cais em busca de restos de peixe. Ótimo para ir à tarde."
            ),
            "zone": "Porto",
            "duration": "1 a 2 horas",
        },
        "de": {
            "title": "Hafen und Seelöwen",
            "description": (
                "Schlendern Sie zwischen Yachten, Fischern und Restaurants. Mit etwas Glück sehen Sie "
                "Seelöwen, die am Pier nach Fischresten suchen. Besonders schön am Nachmittag."
            ),
            "zone": "Hafen",
            "duration": "1 bis 2 Stunden",
        },
    },
    "isla-de-lobos": {
        "en": {
            "title": "Isla de Lobos excursion",
            "description": (
                "A boat trip to this nature reserve, home to a large sea lion colony. Departures leave "
                "from the port and depend on sea conditions."
            ),
            "zone": "Departs from the port",
            "duration": "Half a day",
        },
        "pt": {
            "title": "Excursão à Isla de Lobos",
            "description": (
                "Uma travessia de barco até esta reserva natural, lar de uma grande colônia de "
                "lobos-marinhos. As saídas partem do porto e dependem das condições do mar."
            ),
            "zone": "Saída do porto",
            "duration": "Meio dia",
        },
        "de": {
            "title": "Ausflug zur Isla de Lobos",
            "description": (
                "Eine Bootsfahrt zu diesem Naturschutzgebiet, Heimat einer großen Seelöwenkolonie. Die "
                "Abfahrten starten im Hafen und hängen vom Seegang ab."
            ),
            "zone": "Abfahrt vom Hafen",
            "duration": "Halber Tag",
        },
    },
    "isla-gorriti": {
        "en": {
            "description": (
                "A few minutes by boat from the port: calm-water beaches, walking trails and remains of "
                "historic fortifications. A perfect plan for a full day out."
            ),
            "zone": "Departs from the port",
            "duration": "Full day",
        },
        "pt": {
            "description": (
                "A poucos minutos de lancha do porto: praias de águas calmas, trilhas e restos de "
                "fortificações históricas. Um programa perfeito para passar o dia."
            ),
            "zone": "Saída do porto",
            "duration": "Dia inteiro",
        },
        "de": {
            "description": (
                "Nur wenige Bootsminuten vom Hafen entfernt: Strände mit ruhigem Wasser, Wanderwege und "
                "Reste historischer Befestigungsanlagen. Ein perfekter Plan für einen ganzen Tag."
            ),
            "zone": "Abfahrt vom Hafen",
            "duration": "Ganzer Tag",
        },
    },
    "casapueblo": {
        "en": {
            "title": "Casapueblo and sunset",
            "description": (
                "Carlos Páez Vilaró's white house-studio on the cliffs of Punta Ballena. You can visit "
                "its museum, and it is one of the classic spots to watch the sunset over the sea."
            ),
            "duration": "2 to 3 hours",
        },
        "pt": {
            "title": "Casapueblo e pôr do sol",
            "description": (
                "A casa-ateliê branca de Carlos Páez Vilaró sobre os penhascos de Punta Ballena. Dá para "
                "visitar o museu, e é um dos lugares clássicos para ver o pôr do sol sobre o mar."
            ),
            "duration": "2 a 3 horas",
        },
        "de": {
            "title": "Casapueblo und Sonnenuntergang",
            "description": (
                "Das weiße Haus-Atelier von Carlos Páez Vilaró auf den Klippen von Punta Ballena. Man "
                "kann das Museum besichtigen, und es ist einer der klassischen Orte, um den "
                "Sonnenuntergang über dem Meer zu erleben."
            ),
            "duration": "2 bis 3 Stunden",
        },
    },
    "playa-mansa": {
        "en": {
            "description": (
                "Calmer waters on the river side, with a promenade for walking and great sunsets. Ideal "
                "with kids or when Brava is windy."
            ),
            "zone": "Peninsula",
            "duration": "Half a day",
        },
        "pt": {
            "description": (
                "Águas mais calmas, do lado do rio, com calçadão para caminhar e ótimos pores do sol. "
                "Ideal para ir com crianças ou quando a Brava está com muito vento."
            ),
            "zone": "Península",
            "duration": "Meio dia",
        },
        "de": {
            "description": (
                "Ruhigeres Wasser auf der Flussseite, mit Promenade zum Spazieren und wunderschönen "
                "Sonnenuntergängen. Ideal mit Kindern oder wenn an der Brava starker Wind weht."
            ),
            "zone": "Halbinsel",
            "duration": "Halber Tag",
        },
    },
    "faro-punta-del-este": {
        "en": {
            "title": "Punta del Este Lighthouse",
            "description": (
                "The southern tip of the peninsula. A relaxed stroll among low houses, with sea views "
                "and the Candelaria Church just steps away."
            ),
            "zone": "Peninsula",
            "duration": "1 hour",
        },
        "pt": {
            "title": "Farol de Punta del Este",
            "description": (
                "A ponta sul da península. Um passeio tranquilo entre casas baixas, com vista para o mar "
                "e a Igreja da Candelária a poucos passos."
            ),
            "zone": "Península",
            "duration": "1 hora",
        },
        "de": {
            "title": "Leuchtturm von Punta del Este",
            "description": (
                "Die Südspitze der Halbinsel. Ein ruhiger Spaziergang zwischen niedrigen Häusern, mit "
                "Meerblick und der Kirche La Candelaria nur wenige Schritte entfernt."
            ),
            "zone": "Halbinsel",
            "duration": "1 Stunde",
        },
    },
    "playa-montoya": {
        "en": {
            "description": (
                "In La Barra, with waves that attract surfers and a relaxed, young atmosphere. Close to "
                "the area's bars and restaurants."
            ),
            "duration": "Half a day",
        },
        "pt": {
            "description": (
                "Em La Barra, com ondas que atraem surfistas e um clima descontraído e jovem. Perto dos "
                "bares e restaurantes da região."
            ),
            "duration": "Meio dia",
        },
        "de": {
            "description": (
                "In La Barra, mit Wellen, die Surfer anziehen, und einer entspannten, jungen "
                "Atmosphäre. In der Nähe der Bars und Restaurants der Gegend."
            ),
            "duration": "Halber Tag",
        },
    },
    "puente-de-la-barra": {
        "en": {
            "title": "La Barra wavy bridge",
            "description": (
                "The famous wavy bridge over the Maldonado stream, a symbol of La Barra. A classic stop "
                "to take in the surroundings and snap some photos."
            ),
            "duration": "30 min",
        },
        "pt": {
            "title": "Ponte ondulante de La Barra",
            "description": (
                "A famosa ponte ondulada sobre o arroio Maldonado, símbolo de La Barra. Uma parada "
                "clássica para ver o entorno e tirar fotos."
            ),
            "duration": "30 min",
        },
        "de": {
            "title": "Wellenbrücke von La Barra",
            "description": (
                "Die berühmte wellenförmige Brücke über den Arroyo Maldonado, ein Wahrzeichen von La "
                "Barra. Ein klassischer Stopp, um die Umgebung zu genießen und Fotos zu machen."
            ),
            "duration": "30 Min.",
        },
    },
    "arboretum-lussich": {
        "en": {
            "description": (
                "A forest with species from around the world, planted over a century ago by Antonio "
                "Lussich, with trails and viewpoints. Plenty of shade for hot days."
            ),
            "duration": "1 to 2 hours",
        },
        "pt": {
            "description": (
                "Uma floresta com espécies de todo o mundo, plantada há mais de um século por Antonio "
                "Lussich, com trilhas e mirantes. Muita sombra para os dias de calor."
            ),
            "duration": "1 a 2 horas",
        },
        "de": {
            "description": (
                "Ein Wald mit Pflanzenarten aus aller Welt, vor mehr als einem Jahrhundert von Antonio "
                "Lussich angelegt, mit Wanderwegen und Aussichtspunkten. Viel Schatten für heiße Tage."
            ),
            "duration": "1 bis 2 Stunden",
        },
    },
    "museo-ralli": {
        "en": {
            "title": "Ralli Museum",
            "description": (
                "A contemporary Latin American art museum with free admission. An ideal plan for rainy "
                "days or when the sun is too strong."
            ),
            "duration": "1 to 2 hours",
        },
        "pt": {
            "title": "Museu Ralli",
            "description": (
                "Museu de arte latino-americana contemporânea com entrada gratuita. Um programa ideal "
                "para dias de chuva ou de muito sol."
            ),
            "duration": "1 a 2 horas",
        },
        "de": {
            "title": "Ralli-Museum",
            "description": (
                "Museum für zeitgenössische lateinamerikanische Kunst mit freiem Eintritt. Ein idealer "
                "Plan für Regentage oder bei starker Sonne."
            ),
            "duration": "1 bis 2 Stunden",
        },
    },
    "fundacion-atchugarry": {
        "en": {
            "title": "Pablo Atchugarry Foundation",
            "description": (
                "Open-air sculpture park and museum of Uruguayan artist Pablo Atchugarry, in "
                "Manantiales. Art in the middle of nature."
            ),
            "duration": "2 hours",
        },
        "pt": {
            "title": "Fundação Pablo Atchugarry",
            "description": (
                "Parque de esculturas ao ar livre e museu do artista uruguaio Pablo Atchugarry, em "
                "Manantiales. Arte em meio à natureza."
            ),
            "duration": "2 horas",
        },
        "de": {
            "title": "Pablo-Atchugarry-Stiftung",
            "description": (
                "Skulpturenpark unter freiem Himmel und Museum des uruguayischen Künstlers Pablo "
                "Atchugarry in Manantiales. Kunst mitten in der Natur."
            ),
            "duration": "2 Stunden",
        },
    },
    "feria-plaza-artigas": {
        "en": {
            "title": "Plaza Artigas crafts fair",
            "description": (
                "Handicrafts, jewelry and souvenirs at the Plaza Artigas fair, steps from the Gorlero "
                "pedestrian street. Livelier in high season."
            ),
            "zone": "Downtown",
            "duration": "1 hour",
        },
        "pt": {
            "title": "Feira de artesanato da Plaza Artigas",
            "description": (
                "Artesanato, joias e lembranças na feira da Plaza Artigas, a poucos passos da rua de "
                "pedestres Gorlero. Mais animada na alta temporada."
            ),
            "zone": "Centro",
            "duration": "1 hora",
        },
        "de": {
            "title": "Kunsthandwerksmarkt an der Plaza Artigas",
            "description": (
                "Kunsthandwerk, Schmuck und Souvenirs auf dem Markt an der Plaza Artigas, nur wenige "
                "Schritte von der Fußgängerzone Gorlero entfernt. In der Hochsaison besonders lebhaft."
            ),
            "zone": "Zentrum",
            "duration": "1 Stunde",
        },
    },
    "museo-del-mar": {
        "en": {
            "title": "Sea Museum",
            "description": (
                "A museum dedicated to the marine world, in La Barra. A good plan for rainy or very "
                "windy days."
            ),
            "duration": "1 hour",
        },
        "pt": {
            "title": "Museu do Mar",
            "description": (
                "Um museu dedicado ao mundo marinho, em La Barra. Bom programa para dias de chuva ou de "
                "muito vento."
            ),
            "duration": "1 hora",
        },
        "de": {
            "title": "Meeresmuseum",
            "description": (
                "Ein dem Meer und seiner Tierwelt gewidmetes Museum in La Barra. Ein guter Plan für "
                "Regentage oder bei starkem Wind."
            ),
            "duration": "1 Stunde",
        },
    },
    # ── Restaurantes ──
    "zazu-puerto": {
        "en": {
            "description": (
                "Restaurant on the harbor promenade, known for its good service and original decor. "
                "Among the most recommended dishes: risotto, octopus, salmon and desserts."
            ),
            "zone": "Port",
        },
        "pt": {
            "description": (
                "Restaurante na orla do porto, conhecido pelo bom atendimento e pela decoração "
                "original. Entre os pratos mais recomendados: risoto, polvo, salmão e sobremesas."
            ),
            "zone": "Porto",
        },
        "de": {
            "description": (
                "Restaurant an der Hafenpromenade, bekannt für guten Service und ein originelles "
                "Ambiente. Besonders empfohlen: Risotto, Oktopus, Lachs und Desserts."
            ),
            "zone": "Hafen",
        },
    },
    "lo-de-tere": {
        "en": {
            "description": (
                "A harbor restaurant with a menu built around Uruguayan products and seafood from the "
                "Atlantic and the local lagoons. Its dining room looks out over the port."
            ),
            "zone": "Port",
        },
        "pt": {
            "description": (
                "Restaurante do porto com cozinha focada em produtos uruguaios e em frutos do mar do "
                "Atlântico e das lagoas da região. O salão tem vista para o porto."
            ),
            "zone": "Porto",
        },
        "de": {
            "description": (
                "Restaurant am Hafen mit einer Küche rund um uruguayische Produkte und Meeresfrüchte "
                "aus dem Atlantik und den Lagunen der Region. Der Speisesaal blickt auf den Hafen."
            ),
            "zone": "Hafen",
        },
    },
    "virazon": {
        "en": {
            "description": (
                "Restaurant by the harbor, with views of the boats and nautical decor. Fish and "
                "seafood are the stars of the menu."
            ),
            "zone": "Port",
        },
        "pt": {
            "description": (
                "Restaurante junto ao porto, com vista para os barcos e decoração marinheira. Peixes e "
                "frutos do mar são os protagonistas do cardápio."
            ),
            "zone": "Porto",
        },
        "de": {
            "description": (
                "Restaurant am Hafen mit Blick auf die Boote und maritimem Dekor. Fisch und "
                "Meeresfrüchte stehen im Mittelpunkt der Speisekarte."
            ),
            "zone": "Hafen",
        },
    },
    "la-posta-del-cangrejo": {
        "en": {
            "description": "La Barra's most traditional restaurant: French-inspired cuisine with flavors of the sea.",
        },
        "pt": {
            "description": "O restaurante mais tradicional de La Barra: cozinha de inspiração francesa com sabores do mar.",
        },
        "de": {
            "description": "Das traditionsreichste Restaurant von La Barra: französisch inspirierte Küche mit Meeresaromen.",
        },
    },
    # ── Supermercados ──
    "devoto-express-gorlero": {
        "en": {
            "description": (
                "Devoto supermarket on Gorlero Avenue, right in the center of the peninsula. Handy for "
                "picking up the basics."
            ),
            "zone": "Peninsula",
        },
        "pt": {
            "description": (
                "Supermercado da rede Devoto na avenida Gorlero, bem no centro da península. Prático "
                "para comprar o básico."
            ),
            "zone": "Península",
        },
        "de": {
            "description": (
                "Devoto-Supermarkt an der Avenida Gorlero, mitten im Zentrum der Halbinsel. Praktisch "
                "für den Einkauf des Nötigsten."
            ),
            "zone": "Halbinsel",
        },
    },
    "disco-peninsula": {
        "en": {
            "title": "Disco (Peninsula)",
            "description": (
                "Disco supermarket on the peninsula, a few blocks from the harbor. Useful for stocking "
                "up if you're staying downtown."
            ),
            "zone": "Peninsula",
        },
        "pt": {
            "description": (
                "Supermercado Disco na península, a poucas quadras do porto. Útil para se abastecer se "
                "você está hospedado no centro."
            ),
            "zone": "Península",
        },
        "de": {
            "title": "Disco (Halbinsel)",
            "description": (
                "Disco-Supermarkt auf der Halbinsel, wenige Straßenzüge vom Hafen entfernt. Praktisch "
                "zum Einkaufen, wenn Sie im Zentrum wohnen."
            ),
            "zone": "Halbinsel",
        },
    },
    "tienda-inglesa-punta-shopping": {
        "en": {
            "description": (
                "One of Tienda Inglesa's largest branches, near Punta Shopping. Plenty of variety for "
                "stocking up during your stay."
            ),
        },
        "pt": {
            "description": (
                "Uma das maiores filiais da Tienda Inglesa, na região do Punta Shopping. Muita "
                "variedade para se abastecer durante a estadia."
            ),
        },
        "de": {
            "description": (
                "Eine der größten Filialen von Tienda Inglesa, in der Nähe des Punta Shopping. Große "
                "Auswahl, um sich für den Aufenthalt einzudecken."
            ),
        },
    },
    "devoto-roosevelt": {
        "en": {
            "description": "Devoto hypermarket on Roosevelt Avenue, on the Playa Mansa side. Ideal for a big shop.",
        },
        "pt": {
            "description": "Hipermercado Devoto na avenida Roosevelt, do lado da Playa Mansa. Ideal para uma compra grande.",
        },
        "de": {
            "description": "Devoto-Hypermarkt an der Avenida Roosevelt, auf der Seite der Playa Mansa. Ideal für einen Großeinkauf.",
        },
    },
    "tienda-inglesa-la-barra": {
        "en": {
            "description": "Tienda Inglesa supermarket in La Barra. Handy if you're staying in that area.",
        },
        "pt": {
            "description": "Supermercado Tienda Inglesa em La Barra. Prático se você está hospedado por lá.",
        },
        "de": {
            "description": "Tienda-Inglesa-Supermarkt in La Barra. Praktisch, wenn Sie in dieser Gegend wohnen.",
        },
    },
}
