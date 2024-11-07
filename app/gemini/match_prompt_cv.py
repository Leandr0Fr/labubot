import google.generativeai as genai

from ..constants.constants import CV, SECRET_KEY
from ..constants.match_enum import Match_Color

genai.configure(api_key=SECRET_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


def match_cv(job: str) -> enumerate:
    try:
        response = model.generate_content(f"""
        Vas a revisar una oferta laboral y un CV.
        Vas a decidir si el CV es compatible con la oferta laboral.
        pero vas a tener las siguientes condiciones:
        1. Descarta las ofertas para seniors.
        2. Descarta las ofertas que están escritas en inglés.
        3. Descarta las ofertas que están en blanco.
        4. Escribiras "GREEN" sí y solo sí, la oferta sea muy compatible con el
        CV, es decir, la experiencia solicitada sea razonable y 
        las tecnologias pedidas coincidan en su mayoria.
        5. Escribiras "YELLOW" sí y solo sí, la oferta no sea tan compatible con
        con el CV, es decir, no hay tantas tecnologías pedidas que coincidan,
        se pide más de 2 años de experiencia y se pide un nivel de inglés superior
        al del CV.
        6. Escribiras 'RED' sí y solo sí, la oferta no es compatible, es decir, que
        se solicitan tecnologías muy distintas o muchos años de experiencia. También si
        cumple algunas de las siguientes coindiciones: 1, 2 o 3.
                                          
        SOLAMENTE ESCRIBE EL COLOR QUE DEFINISTE CUANDO LO COMPARES, NADA MÁS NI NADA MENOS.
                                    
        Oferta laboral: {job}
        CV: {CV}
        """)
        return Match_Color(response.text.strip())
    except Exception:
        match_cv(job)
