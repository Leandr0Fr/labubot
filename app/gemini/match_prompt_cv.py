import google.generativeai as genai

from ..constants.constants import CV, SECRET_KEY
from ..constants.match_enum import Match_Color  # noqa: F401

genai.configure(api_key=SECRET_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


def match_cv(job: str) -> enumerate:
    response = model.generate_content(f"""
    Compare la siguiente oferta laboral: {job}
    con el siguiente CV: {CV}
    Si es compatible escribe 'GREEN'.
    Si no tan compatible (capaz por año de experiencia o tecnologías faltantes) escribe 'YELLOW'.
    Si no es compatible escribe 'RED'.
    Además, una breve razón de porqué el color seleccionado.
    """)
    print(response.text)
