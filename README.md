# Labubot
Labubot es un sistema de filtración de ofertas laborales de LinkedIn de manera automatizada.

Se utiliza Selenium para scrapear las ofertas laborales, Gemini para comprobar si el currículum es compatible con la oferta laboral y la API de Telegram para enviar las ofertas a un chat.

Las ofertas se catalogan en 3 tipos:

🟢 Las cuales son las más compatibles.

🟡 Las cuales no son del todo compatibles, quedando a disposición del usuario decidir su compatibilidad.

🔴 Las cuales no son compatibles. Estas últimas no se envían al chat de Telegram.

## Instalación
Se necesita tener Python 3.12 o superior.

1. Clonar el repositorio.

2. Instalar Poetry usando `pip install poetry`.

3. Ingresar a la carpeta del proyecto y ejecutar los siguientes comandos: `poetry install` y `poetry shell`.

4. Renombrar el archivo `.env.example` a `.env`.

5. Reemplazar los valores correspondientes en el archivo `.env`.

6. Generar un chatbot en Telegram. Para ello, busque "BotFather" en el buscador de Telegram y siga los pasos indicados.
   
## Ejecución
Ejecutar el siguiente comando: `poetry run start`.

## Cosas a tener en cuenta
El sistema, al estar scrapeando la página de *LinkedIn*, puede tener problemas con el scraping. Si se cuelga, reinicie el script.

