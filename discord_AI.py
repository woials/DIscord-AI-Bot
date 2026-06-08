import os

import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from gemini_result import get_gemini_result

load_dotenv()
intents = discord.Intents.default()

bot=commands.Bot(command_prefix="/",intents=intents,help_command=None)
tree=bot.tree

@bot.event
async def on_ready():
    await tree.sync()
    print("準備完了")

@tree.command(name="ask",description="AIに質問します")
@app_commands.describe(
    name="質問したいことを入力してください"
)
async def ask_gemini(interaction:discord.Interaction,name:str):
    await interaction.response.defer(ephemeral=True)
    result=await get_gemini_result(name)
    title=result.title
    summary=result.summary
    main=result.main_text
    embed=discord.Embed(
        title=title,
        description=summary,
        color=discord.Colour.blue(),
    )
    current_headline="本文"
    current_paragraphs=[]
    #mainをheadlineでセクション分け
    for block in main:
        if block.type=="headline":
            if current_paragraphs:
                embed.add_field(
                    name=current_headline,
                    value="\n\n".join(current_paragraphs),
                    inline=False
                )
                current_paragraphs=[]
            current_headline=block.text
        elif block.type=="paragraph":
            current_paragraphs.append(block.text)
    if current_paragraphs:
        embed.add_field(
            name=current_headline,
            value="\n\n".join(current_paragraphs),
            inline=False
        )
    await interaction.followup.send(embed=embed,ephemeral=True)

bot.run(os.getenv("DISCORD_TOKEN"))