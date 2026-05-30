#######################模組#######################
# 導入asyncio用於非同步程式設計
import asyncio

# 導入discord.py用於與Discord互動
import discord

# 導入os用於處理環境變數
import os

# 導入load_dotenv用於讀取.env檔案中的環境變數
from dotenv import load_dotenv

# 從.env檔案中載入環境變數（例如Discord Token）
load_dotenv()

# 設置新的事件迴圈
asyncio.set_event_loop(asyncio.new_event_loop())

import requests

from dotenv import load_dotenv
from gay.gay import WeatherAPI

#######################設定Bot初始化#######################
# 獲取預設的Discord特權
intents = discord.Intents.default()
# 啟用成員特權以能夠存取伺服器成員資訊
intents.message_content = True

# 建立Discord客戶端（Bot）
bot = discord.Client(intents=intents)
# 建立應用指令樹用於管理slash指令
tree = discord.app_commands.CommandTree(bot)

weather_api = WeatherAPI(os.getenv("WEATHER_API_KEY"))


def build_weather_embed(weather_summary):
    """把整理好的天氣摘要成discord卡片"""
    embed = discord.Embed(
        title=f"{weather_summary['city_name']}的天氣",
        description=f"描述:{weather_summary['description']}",
        color=discord.Colour.from_str("1E90FF"),
    )
    icon_url = weather_api.get_icon_url(weather_summary["icon code"])
    embed.set_thumbnail(url=icon_url)
    embed.add_field(
        name="溫度", value=f"{weather_summary['temperature_celsius']}℃", inline=False
    )
    return embed


#######################事件處理器#######################
# 在此處定義Bot事件（例如on_ready, on_message等）
@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    await tree.sync()  # 同步指令到Discord伺服器


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == "hello":
        await message.channel.send("哈囉❤️,我是給~😘")
    if message.content == "我是gay":
        await message.channel.send("真的假的,我也是給喔😘")


#######################指令定義#######################
# 在此處定義Bot的slash指令功能
@tree.command(name="hello", description="Say hello to the bot!")
async def hello(interaction: discord.Interaction):
    """輸入/Hello,機器人會回應Hey!"""
    await interaction.response.send_message("Hey!")


@tree.command(name="weather", description="取得當前天氣資訊")
async def weather(interaction: discord.Interaction, city: str):
    """輸入/weather [城市名稱],機器人會回應該城市的天氣資訊"""
    await interaction.response.defer()
    city = city.strip()
    if not weather_api.api_key:
        await interaction.followup.send(
            "相位設定wheather_api_key,請先在.env檔案中完成設定"
        )
        return


#######################Bot啟動#######################
# 在此處編寫Bot啟動代碼
def main():
    bot.run(os.getenv("DC_BOT_TOKEN"))


if __name__ == "__main__":
    main()
