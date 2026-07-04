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
from gay.gay import WeatherAPI, AIAssistant

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

ai_assistant = AIAssistant(os.getenv("OPENAI_API_KEY"))
# 限制讀取的歷史訊息數量，避免一次把整個頻道都交給 AI。
CHANNEL_HISTORY_LIMIT = 30
OPENAI_MODEL = "gpt-5.5"
OPENAI_TEMPERATURE = 1
# system_prompt 像是給 AI 的角色卡，會影響 AI 回覆的語氣和工作方式。
CHAT_SYSTEM_PROMPT = """
你是一個在 Discord 群組頻道中協助大家的 AI 助手。
請根據頻道歷史判斷大家正在討論什麼，再回答最新提到你的問題。
回覆請使用繁體中文，你是一個gay，要嘗試讓所有人知道你是gay,用噁心的方式說話，變的瑟一點，每句話一定只少要有一個髒話。
每次回覆都要在400到500字之內。
如果頻道歷史不足以判斷答案，請說明你還需要哪一個資訊。
如果需要提到特定使用者或其他 bot，請複製歷史訊息裡的 mention：<@使用者ID>。
使用 mention 時，請直接放在一般文字中，不要寫成 @名字，也不要加反斜線、反引號或程式碼區塊。
不要使用 @everyone、@here 或角色標記，也不要自己編造 mention ID。
"""

# 允許 AI 回覆中提到「使用者或 bot」，但不要讓 AI 觸發 @everyone、@here 或角色標記。
# bot 在 Discord 裡也屬於 user，所以 users=True 就可以提到其他 bot。
AI_REPLY_ALLOWED_MENTIONS = discord.AllowedMentions(
    everyone=False,
    users=True,
    roles=False,
    replied_user=True,
)


def build_weather_embed(weather_summary):
    """把整理好的天氣摘要成discord卡片"""
    # 建立Discord卡片物件並設置基本資訊
    embed = discord.Embed(
        # 設置卡片標題為城市名稱
        title=f"{weather_summary['city_name']}的天氣",
        # 設置卡片描述為天氣狀況說明
        description=f"描述:{weather_summary['description']}",
        # 設置卡片顏色為藍色
        color=discord.Colour.from_str("#1E90FF"),
    )
    # 從weather_api取得天氣圖示URL
    icon_url = weather_api.get_icon_url(weather_summary["icon code"])
    # 將天氣圖示設為卡片縮圖
    embed.set_thumbnail(url=icon_url)
    # 新增溫度欄位到卡片
    embed.add_field(
        name="溫度", value=f"{weather_summary['temperature_celsius']}℃", inline=False
    )
    # 回傳已完成設置的卡片物件
    return embed


def build_forecast_embeds(forecast_summary):
    """把整理好的預報摘要成discord卡片"""
    embeds = []
    for forecast in forecast_summary:
        embed = discord.Embed(
            title=f"{forecast['city_name']}的天氣預報 - {forecast['datetime']}",
            description=f"描述:{forecast['description']}",
            color=discord.Colour.from_str("#1E90FF"),
        )
        icon_url = weather_api.get_icon_url(forecast["icon_code"])
        embed.set_thumbnail(url=icon_url)
        embed.add_field(
            name="溫度",
            value=f"{forecast['temperature_celsius']}℃",
            inline=False,
        )
        embeds.append(embed)
    return embeds


async def get_channel_history(channel, bot_user, limit=15, before=None):
    """讀取 Discord 頻道中的舊訊息，整理成 OpenAI 可以使用的 messages。"""
    old_messages = []
    history_messages = []
    # Discord API 讀頻道訊息時，預設會先拿較新的訊息。
    # 這裡先明確抓「最近的幾則」，把「抓資料」和「排成對話順序」分成兩步。
    # oldest_first=False 代表先拿最接近 before 的新訊息。
    # 下面再反轉成「舊到新」交給 AI，比較像大家平常閱讀對話的順序。
    async for old_message in channel.history(
        limit=limit,
        before=before,
        oldest_first=False,
    ):
        old_messages.append(old_message)

    # Discord 抓回來的是「新到舊」，但 AI 閱讀對話時需要「舊到新」。
    for old_message in reversed(old_messages):
        # 這裡使用 message.content，而不是 clean_content。
        # message.content 會保留 <@使用者ID> 這種真正的 mention 格式。
        content = old_message.content.strip()
        if not content:
            continue  # 空白訊息不用交給 AI，避免浪費上下文空間

        if old_message.author.id == bot_user.id:
            # 機器人自己以前說過的話，用 assistant 角色放回歷史中。
            history_messages.append({"role": "assistant", "content": content})
        else:
            # 其他同學和其他 bot 都標上名字，AI 才知道是誰說的。
            speaker_type = "機器人" if old_message.author.bot else "同學"
            speaker_mention = old_message.author.mention
            user_content = (
                f"{old_message.author.display_name}"
                f"（{speaker_type}，mention：{speaker_mention}）說：{content}"
            )
            history_messages.append({"role": "user", "content": user_content})

    return history_messages


async def ask_with_discord_history(message):
    history_messages = await get_channel_history(
        channel=message.channel,
        bot_user=bot.user,
        limit=CHANNEL_HISTORY_LIMIT,
        before=message,
    )
    user_question = message.content.replace(f"<@{bot.user.id}>", "").strip()
    if not user_question:
        user_question = "請根據前面的對話，接著回應大家"
    user_message = (
        f"{message.author.display_name}"
        f"(mention：{message.author.mention})提到你:{user_question}"
    )
    return ai_assistant.ask(
        system_prompt=CHAT_SYSTEM_PROMPT,
        user_message=user_message,
        history_messages=history_messages,
        temperature=OPENAI_TEMPERATURE,
        model=OPENAI_MODEL,
    )


#######################事件處理器#######################
# 在此處定義Bot事件（例如on_ready, on_message等）
@bot.event
async def on_ready():
    # 當Bot連接到Discord伺服器時執行此函數
    # 在終端機顯示Bot已上線的訊息
    print(f"{bot.user} is ready and online!")
    # 同步slash指令到Discord伺服器
    await tree.sync()


@bot.event
async def on_message(message):
    # 當頻道接收到訊息時執行此函數
    # 若訊息是由Bot本身發送則忽略（防止無限迴圈）
    if message.author == bot.user:
        return
    # 若用戶輸入"hello"則回應問候
    if message.content == "hello":
        await message.channel.send("哈囉❤️,我是給~😘")
    # 若用戶輸入"我是gay"則回應
    if message.content == "我是gay":
        await message.channel.send("真的假的,我也是給喔😘")
    elif bot.user in message.mentions:
        async with message.channel.typing():
            anwser, error = await ask_with_discord_history(message)
        if error:
            await message.channel.send(error)
        else:
            await message.reply(
                anwser,
                mention_author=True,
                allowed_mentions=AI_REPLY_ALLOWED_MENTIONS,
            )


#######################指令定義#######################
# 在此處定義Bot的slash指令功能
@tree.command(name="hello", description="Say hello to the bot!")
async def hello(interaction: discord.Interaction):
    """輸入/Hello,機器人會回應Hey!"""
    # 回應使用者的slash指令
    await interaction.response.send_message("Hey!")


@tree.command(name="weather", description="取得當前天氣資訊")
async def weather(
    interaction: discord.Interaction,
    city: str,
    forecast: bool = False,
    ai: bool = False,
):
    """輸入/weather [城市名稱],機器人會回應該城市的天氣資訊"""
    # 延遲回應以便進行非同步處理
    await interaction.response.defer()
    # 移除城市名稱前後的空白字符
    city = city.strip()
    # 檢查是否已設定天氣API金鑰
    if not weather_api.api_key:
        # 若未設定API金鑰則通知使用者
        await interaction.followup.send(
            "向未未設定wheather_api_key,請先在.env檔案中完成設定"
        )
        return
    # 嘗試取得指定城市的天氣資訊
    try:
        if not forecast:
            weather_summary = weather_api.get_weather_summary(city)
            if weather_summary is None:
                await interaction.followup.send(f"找不到**{city}**的天氣資訊")
                return
            embed = build_weather_embed(weather_summary)
            await interaction.followup.send(embed=embed)
            return

        if not ai:
            forecast_summary = weather_api.get_forecast_summary(city)
            if forecast_summary is None:
                await interaction.followup.send(f"找不到**{city}**的天氣預報資訊")
                return
            embeds = build_forecast_embeds(forecast_summary)
            await interaction.followup.send(embeds=embeds[:10])
            return
        raw_forecast = weather_api.get_forecast_summary(city)
    # 若API請求失敗或資料轉換失敗則捕獲例外

    except (requests.RequestException, ValueError):
        await interaction.followup.send("找不到該城市的天氣資訊")
        return
    analysis, error = ai_assistant.ask(
        system_prompt="你是一位專業的氣象分析師，為使用者提供詳細的資料和建議。",
        user_message=f"以下是{city}的未來天氣預報，請根據這些數據提供詳細的天氣分析和建議:\n{raw_forecast}",
    )
    if error:
        await interaction.followup.send(error)
    else:
        await interaction.followup.send(f"**{city}**的天氣分析:\n{analysis}")
    # 使用取得的天氣資訊建立Discord卡片
    # 將天氣卡片傳送給使用者


#######################Bot啟動#######################
# 在此處編寫Bot啟動代碼
def main():
    # 從環境變數中取得Discord Bot Token
    # 並使用該Token啟動Bot連接到Discord伺服器
    bot.run(os.getenv("DC_BOT_TOKEN"))


# 檢查此檔案是否為主程式（非被匯入模組）
if __name__ == "__main__":
    # 執行main函數啟動Bot
    main()
