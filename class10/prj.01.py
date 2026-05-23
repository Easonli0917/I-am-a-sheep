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

#######################設定Bot初始化#######################
# 獲取預設的Discord特權
intents = discord.Intents.default()
# 啟用成員特權以能夠存取伺服器成員資訊
intents.message_content = True

# 建立Discord客戶端（Bot）
bot = discord.Client(intents=intents)
# 建立應用指令樹用於管理slash指令
tree = discord.app_commands.CommandTree(bot)


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


#######################Bot啟動#######################
# 在此處編寫Bot啟動代碼
def main():
    bot.run(os.getenv("DC_BOT_TOKEN"))


if __name__ == "__main__":
    main()
