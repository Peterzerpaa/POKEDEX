import discord
import requests
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

# Evento cuando el bot está listo
@bot.event
async def on_ready():
    print(f'Ha iniciado sesión como {bot.user}')

# Comando para obtener información de un Pokémon usando PokeAPI
@bot.command()
async def pokemon(ctx, nombre: str):
    base_url = f"https://pokeapi.co/api/v2/pokemon/{nombre.lower()}"
    
    try:
        # Hacer la solicitud HTTP a PokeAPI
        response = requests.get(base_url)
        data = response.json()

        # Obtener los datos principales del Pokémon
        nombre_pokemon = data["name"].capitalize()
        peso = data["weight"]
        altura = data["height"]
        tipos = [tipo["type"]["name"] for tipo in data["types"]]
        tipos = ", ".join(tipos).capitalize()
        imagen_url = data["sprites"]["front_default"]  # URL de la imagen del Pokémon

        # Crear un mensaje con los datos del Pokémon
        mensaje = (f"**{nombre_pokemon}**:\n"
                   f"Altura: {altura} decímetros\n"
                   f"Peso: {peso} hectogramos\n"
                   f"Tipos: {tipos}")

        # Enviar el mensaje con la imagen
        embed = discord.Embed(title=f"{nombre_pokemon}", description=mensaje)
        embed.set_image(url=imagen_url)

    except requests.exceptions.RequestException:
        mensaje = "Ocurrió un error al conectarse a PokeAPI."
        await ctx.send(mensaje)
        return
    except KeyError:
        mensaje = f"No se encontró información para el Pokémon '{nombre}'."
        await ctx.send(mensaje)
        return

    # Enviar el embed con la imagen y la información del Pokémon al canal
    await ctx.send(embed=embed)

# Ejecutar el bot con tu token
bot.run("token here")
