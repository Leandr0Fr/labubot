import google.generativeai as genai

from ..constants.constants import CV, SECRET_KEY
from ..constants.match_enum import Match_Color

genai.configure(api_key=SECRET_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


def match_cv(job: str) -> enumerate:
    prompt_cv = f"""
    Vas a evaluar una oferta laboral y un CV para determinar su compatibilidad según las condiciones y criterios detallados. Responde únicamente con el color correspondiente (GREEN, YELLOW o RED):

    ### Condiciones de descarte:
    1. Descarta ofertas para puestos de nivel senior.
    2. Descarta ofertas escritas en cualquier idioma distinto al español.
    3. Descarta ofertas en blanco.
    4. Descarta ofertas de trabajo presencial fuera de Argentina o de la Ciudad de Buenos Aires.
    5. Descarta ofertas que soliciten más de 4 años de experiencia.

    ### Instrucciones de clasificación:
    - Escribe **"GREEN"** si la oferta es altamente compatible con el CV: la experiencia solicitada es razonable y la mayoría de las tecnologías requeridas están presentes en el CV.
    - Escribe **"YELLOW"** si la oferta es moderadamente compatible: faltan varias tecnologías solicitadas, requiere más de 2 años de experiencia o un nivel de inglés más alto que el indicado en el CV.
    - Escribe **"RED"** si la oferta no es compatible. Esto incluye casos en los que se requieren tecnologías muy diferentes, demasiados años de experiencia, o si la oferta cumple alguna de las condiciones de descarte.

    **Importante**:
    - Solo analiza ofertas en español relacionadas con sistemas, programación y áreas similares.
    - Responde únicamente con el color determinado según la evaluación de compatibilidad.

    Oferta laboral: {job}
    CV: {CV}
    """  # noqa: E501

    prompt_is_english = f"La siguiente oferta laboral está en inglés? {job}. Sí está en inglés responde 'SI', en caso contrario 'NO'"  # noqa: E501
    try:
        response_is_english = model.generate_content(prompt_is_english)
        if response_is_english.text.strip() == "SI":
            return Match_Color("RED")
        response = model.generate_content(prompt_cv)
        return Match_Color(response.text.strip())
    except Exception:
        match_cv(job)
