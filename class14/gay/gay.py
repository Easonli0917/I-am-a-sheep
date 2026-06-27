#######################模組#######################
# 導入requests用於發送HTTP請求
import requests
import openai


#######################WeatherAPI類#######################
# 建立WeatherAPI類用於與OpenWeatherMap API互動以取得天氣資訊
class WeatherAPI:
    def __init__(self, api_key, lang="zh_tw"):
        """初始化WeatherAPI物件

        Args:
            api_key: OpenWeatherMap API金鑰
            lang: 回應語言代碼，預設為繁體中文(zh_tw)
        """
        # 儲存OpenWeatherMap API金鑰
        self.api_key = api_key
        # 設置溫度單位為攝氏度
        self.units = "metric"
        # 設置回應語言
        self.lang = lang
        # 設置OpenWeatherMap API基本URL
        self.base_url = "https://api.openweathermap.org/data/2.5/weather?"
        # 設置天氣圖示基本URL
        self.forecast_url = "https://api.openweathermap.org/data/2.5/forecast?"
        self.icon_url = "http://openweathermap.org/img/wn/"

    def get_current_weather(self, city_name):
        """取得指定城市的當前天氣資訊

        Args:
            city_name: 城市名稱

        Returns:
            JSON格式的天氣資訊字典
        """
        # 組合完整的API請求URL，包含API金鑰、城市名稱、溫度單位和語言設定
        send_url = f"{self.base_url}appid={self.api_key}&q={city_name}&units={self.units}&lang={self.lang}"
        # 發送GET請求到OpenWeatherMap API
        response = requests.get(send_url)
        # 將回應轉換為JSON格式並回傳
        return response.json()

    def get_weather_summary(self, icon_code):
        """取得天氣資訊摘要

        Args:
            icon_code: 城市名稱（用於查詢API）

        Returns:
            包含城市名稱、溫度、天氣描述和天氣圖示代碼的字典，若無有效資訊則回傳None
        """
        # 調用get_current_weather方法取得完整的天氣資訊
        info = self.get_current_weather(icon_code)

        # 檢查API回應中是否包含"weather"和"main"欄位
        if "weather" in info and "main" in info:
            # 整理並回傳天氣資訊摘要
            return {
                # 取得城市名稱，若不存在則使用預設值"city_name"
                "city_name": info.get("name", "city_name"),
                # 取得溫度（攝氏度）並四捨五入到小數點後2位
                "temperature_celsius": round(info["main"]["temp"], 2),
                # 取得天氣狀況描述（如晴天、下雨等）
                "description": info["weather"][0]["description"],
                # 取得天氣圖示代碼用於顯示天氣圖示
                "icon code": info["weather"][0]["icon"],
            }

        # 若API回應不包含所需資訊則回傳None
        return None

    def get_icon_url(self, icon_code):
        """根據天氣圖示代碼取得天氣圖示的完整URL

        Args:
            icon_code: 天氣圖示代碼

        Returns:
            天氣圖示的完整URL字串
        """
        # 組合天氣圖示基本URL、圖示代碼和解析度，並回傳完整URL
        return f"{self.icon_url}{icon_code}@2x.png"

    def get_weather_icon(self, icon_code):
        """下載天氣圖示

        Args:
            icon_code: 天氣圖示代碼

        Returns:
            天氣圖示的二進制內容，若下載失敗則回傳None
        """
        # 取得天氣圖示URL
        icon_url = self.get_icon_url(icon_code)
        # 發送GET請求下載圖示
        response = requests.get(icon_url)
        # 檢查是否成功下載圖示（response.content非空）
        if response.content:
            # 回傳圖示的二進制內容
            return response.content
        # 若下載失敗則回傳None
        return None

    def get_weather_forecast(self, city_name):
        send_url = f"{self.forecast_url}q={city_name}&appid={self.api_key}&units={self.units}&lang={self.lang}"
        response = requests.get(send_url)
        response.raise_for_status()
        return response.json()

    def get_forecast_summary(self, city_name, count=10):
        forecast_count = max(0, count)
        try:
            info = self.get_weather_forecast(city_name)
        except requests.HTTPError as error:
            response = error.response
            if response is not None and response.status_code == 404:
                return None
            raise
        if "city" not in info or "list" not in info:
            return None
        city_label = info["city"].get("name", "city_name")
        forecast_summary = []

        for forecast in info["list"][:forecast_count]:
            forecast_summary.append(
                {
                    "city_name": city_label,
                    "datetime": forecast["dt_txt"],
                    "temperature_celsius": round(forecast["main"]["temp"], 2),
                    "description": forecast["weather"][0]["description"],
                    "icon_code": forecast["weather"][0]["icon"],
                }
            )
        return forecast_summary


class AIAssistant:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = api_key

    def ask(self, system_prompt, user_message, temperature=0.2, model="gpt-4o"):
        if not self.api_key:
            return None, "尚未設定OPENAI_API_KEY，請先在.env檔案中完成設定。"

        messages = [{"role": "system", "content": system_prompt}] + [
            {"role": "user", "content": user_message}
        ]

        try:

            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
            )
            assistant_message = response.choices[0].message.content

            return assistant_message, None
        except Exception as e:
            return None, f"發生錯誤:{e}"
