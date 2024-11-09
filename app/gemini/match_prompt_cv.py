import google.generativeai as genai

from ..constants.constants import CV, SECRET_KEY
from ..constants.match_enum import Match_Color

genai.configure(api_key=SECRET_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


def match_cv(job: str) -> enumerate:
    try:
        response = model.generate_content(f"""
Vas a evaluar una oferta laboral y un CV para determinar su compatibilidad. Sigue las condiciones detalladas a continuación y solo escribe el color correspondiente (GREEN, YELLOW o RED) basado en el nivel de ajuste:

Condiciones de descarte:
1. Descarta ofertas para puestos de nivel senior.
2. Si la oferta está mayoritariamente en inglés, descártala.
3. Descarta ofertas en blanco.
4. Si la oferta es para trabajo presencial fuera de Argentina o Buenos Aires, descártala.

Instrucciones de clasificación:
- Escribe **"GREEN"** solo si la oferta es altamente compatible con el CV, es decir, la experiencia solicitada es razonable y la mayoría de las tecnologías pedidas están presentes en el CV.
- Escribe **"YELLOW"** solo si la oferta es moderadamente compatible, es decir, si faltan varias tecnologías solicitadas, la oferta requiere más de 2 años de experiencia o un nivel de inglés más alto que el del CV.
- Escribe **"RED"** solo si la oferta no es compatible. Esto incluye casos en los que se requieren tecnologías muy diferentes o demasiados años de experiencia, o si la oferta cumple alguna de las condiciones de descarte (1, 2, 3 o 4).

**Solo escribe el color determinado según la evaluación de compatibilidad. No agregues nada más.**

Oferta laboral: {job}
CV: {CV}
""")  # noqa: E501
        return Match_Color(response.text.strip())
    except Exception:
        match_cv(job)
