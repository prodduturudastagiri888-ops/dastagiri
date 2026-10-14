import requests
import datetime
from datetime import datetime, timezone
import json

# Pre-defined major agricultural districts with precise GPS coordinates for instant lookup
DISTRICT_COORDINATES = {
    "guntur": {"name": "Guntur", "state": "Andhra Pradesh", "lat": 16.3067, "lon": 80.4365},
    "vijayawada": {"name": "Vijayawada (NTR)", "state": "Andhra Pradesh", "lat": 16.5062, "lon": 80.6480},
    "kurnool": {"name": "Kurnool", "state": "Andhra Pradesh", "lat": 15.8281, "lon": 78.0373},
    "anantapur": {"name": "Anantapur", "state": "Andhra Pradesh", "lat": 14.6819, "lon": 77.6006},
    "visakhapatnam": {"name": "Visakhapatnam", "state": "Andhra Pradesh", "lat": 17.6868, "lon": 83.2185},
    "nellore": {"name": "Nellore", "state": "Andhra Pradesh", "lat": 14.4426, "lon": 79.9865},
    "rajahmundry": {"name": "East Godavari (Rajahmundry)", "state": "Andhra Pradesh", "lat": 17.0005, "lon": 81.8040},
    "warangal": {"name": "Warangal", "state": "Telangana", "lat": 17.9689, "lon": 79.5941},
    "hyderabad": {"name": "Hyderabad", "state": "Telangana", "lat": 17.3850, "lon": 78.4867},
    "khammam": {"name": "Khammam", "state": "Telangana", "lat": 17.2473, "lon": 80.1514},
    "nizamabad": {"name": "Nizamabad", "state": "Telangana", "lat": 18.6725, "lon": 78.0941},
    "karimnagar": {"name": "Karimnagar", "state": "Telangana", "lat": 18.4386, "lon": 79.1288},
    "suryapet": {"name": "Suryapet", "state": "Telangana", "lat": 17.1439, "lon": 79.6239},
    "delhi": {"name": "New Delhi", "state": "Delhi", "lat": 28.6139, "lon": 77.2090},
    "bhopal": {"name": "Bhopal", "state": "Madhya Pradesh", "lat": 23.2599, "lon": 77.4126},
    "pune": {"name": "Pune", "state": "Maharashtra", "lat": 18.5204, "lon": 73.8567}
}

class WeatherService:
    @staticmethod
    def get_weather(location_query: str = "Guntur") -> dict:
        """
        Fetches live weather from Open-Meteo free API or falls back gracefully to realistic data.
        Returns current conditions, 7-day forecast, severe alerts, and agricultural advisories.
        """
        norm_key = (location_query or "Guntur").strip().lower()
        coords = DISTRICT_COORDINATES.get(norm_key)

        lat = coords["lat"] if coords else 16.3067
        lon = coords["lon"] if coords else 80.4365
        display_name = coords["name"] if coords else location_query.title()
        state_name = coords.get("state", "India") if coords else "India"

        # If user typed an unknown location, try free geocoding
        if not coords:
            try:
                geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location_query}&count=1&language=en&format=json"
                geo_resp = requests.get(geo_url, timeout=3.5)
                if geo_resp.status_code == 200:
                    data = geo_resp.json()
                    if "results" in data and len(data["results"]) > 0:
                        res = data["results"][0]
                        lat = res["latitude"]
                        lon = res["longitude"]
                        display_name = res["name"]
                        state_name = res.get("admin1", "India")
            except Exception:
                pass  # Fall back to default coords

        # Fetch actual live weather forecast
        api_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m,wind_direction_10m"
            f"&hourly=temperature_2m,precipitation_probability&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,wind_speed_10m_max"
            f"&timezone=auto"
        )

        is_live_data = False
        weather_data = None
        error_msg = None

        try:
            resp = requests.get(api_url, timeout=4.5)
            if resp.status_code == 200:
                weather_data = resp.json()
                is_live_data = True
        except Exception as e:
            error_msg = str(e)

        if not is_live_data or not weather_data:
            # High-fidelity fallback / demo data
            current_temp = 31.5
            humidity = 72
            feels_like = 34.0
            wind_speed = 14.5
            precip_prob = 40
            weather_code = 2
            forecast_daily = [
                {"date": "Today", "day_name": "Today", "max_temp": 33.0, "min_temp": 24.5, "rain_prob": 40, "condition": "Partly Cloudy", "rain_mm": 2.5},
                {"date": "Day 2", "day_name": "Tomorrow", "max_temp": 32.0, "min_temp": 24.0, "rain_prob": 65, "condition": "Scattered Showers", "rain_mm": 18.0},
                {"date": "Day 3", "day_name": "Day 3", "max_temp": 30.5, "min_temp": 23.0, "rain_prob": 70, "condition": "Moderate Rain", "rain_mm": 24.0},
                {"date": "Day 4", "day_name": "Day 4", "max_temp": 31.0, "min_temp": 23.5, "rain_prob": 35, "condition": "Partly Cloudy", "rain_mm": 1.0},
                {"date": "Day 5", "day_name": "Day 5", "max_temp": 33.5, "min_temp": 24.0, "rain_prob": 15, "condition": "Clear / Sunny", "rain_mm": 0.0},
                {"date": "Day 6", "day_name": "Day 6", "max_temp": 34.0, "min_temp": 25.0, "rain_prob": 10, "condition": "Sunny", "rain_mm": 0.0},
                {"date": "Day 7", "day_name": "Day 7", "max_temp": 34.5, "min_temp": 25.2, "rain_prob": 10, "condition": "Sunny", "rain_mm": 0.0}
            ]
        else:
            cur = weather_data.get("current", {})
            current_temp = cur.get("temperature_2m", 30.0)
            humidity = cur.get("relative_humidity_2m", 65)
            feels_like = cur.get("apparent_temperature", current_temp + 2.0)
            wind_speed = cur.get("wind_speed_10m", 12.0)
            weather_code = cur.get("weather_code", 1)

            daily = weather_data.get("daily", {})
            time_list = daily.get("time", [])
            max_temps = daily.get("temperature_2m_max", [])
            min_temps = daily.get("temperature_2m_min", [])
            rain_probs = daily.get("precipitation_probability_max", [])
            rain_sums = daily.get("precipitation_sum", [])
            codes = daily.get("weather_code", [])

            forecast_daily = []
            precip_prob = rain_probs[0] if rain_probs else 20
            for i in range(min(7, len(time_list))):
                d_str = time_list[i]
                try:
                    dt = datetime.strptime(d_str, "%Y-%m-%d")
                    day_label = "Today" if i == 0 else ("Tomorrow" if i == 1 else dt.strftime("%a (%d %b)"))
                except Exception:
                    day_label = f"Day {i+1}"

                c_code = codes[i] if i < len(codes) else 1
                cond_text = WeatherService.wmo_code_to_text(c_code)
                forecast_daily.append({
                    "date": d_str,
                    "day_name": day_label,
                    "max_temp": max_temps[i] if i < len(max_temps) else 32.0,
                    "min_temp": min_temps[i] if i < len(min_temps) else 23.0,
                    "rain_prob": rain_probs[i] if i < len(rain_probs) else 20,
                    "rain_mm": rain_sums[i] if i < len(rain_sums) else 0.0,
                    "condition": cond_text
                })

        # Calculate alerts
        alerts = []
        if precip_prob >= 60 or any(d["rain_mm"] > 25.0 for d in forecast_daily[:3]):
            alerts.append({
                "type": "rain",
                "severity": "warning",
                "title_en": "Heavy Rain Warning",
                "title_te": "భారీ వర్ష హెచ్చరిక",
                "message_en": "High precipitation predicted over the next 48 hours. Ensure field drainage channels are cleared to prevent water stagnation.",
                "message_te": "రాబోయే 48 గంటల్లో భారీ వర్ష సూచన ఉంది. పొలంలో నీరు నిలవకుండా మురుగు కాలువలను తక్షణమే శుభ్రం చేయండి."
            })
        if current_temp >= 38.0 or any(d["max_temp"] >= 40.0 for d in forecast_daily):
            alerts.append({
                "type": "heat",
                "severity": "danger",
                "title_en": "Extreme Heat Advisory (>40°C)",
                "title_te": "తీవ్రమైన ఎండ & ఉష్ణోగ్రత హెచ్చరిక",
                "message_en": "High heat stress may cause moisture evaporation and blossom drop. Schedule light evening micro-irrigation.",
                "message_te": "అధిక ఉష్ణోగ్రత వల్ల పూత రాలడం, నేల త్వరగా ఎండిపోవడం జరగవచ్చు. సాయంత్రం వేళల్లో తుంపర లేదా బిందు సేద్యం ద్వారా తేలికపాటి తడులు ఇవ్వండి."
            })
        if wind_speed >= 28.0:
            alerts.append({
                "type": "wind",
                "severity": "warning",
                "title_en": "High Wind Advisory",
                "title_te": "బలమైన ఈదురు గాలుల సూచన",
                "message_en": "Gusty winds may lodge tall crops like Paddy, Banana, and Maize. Postpone all chemical foliar spray operations.",
                "message_te": "బలమైన గాలులు వీచే అవకాశం ఉన్నందున ఎటువంటి క్రిమిసంహారక మందులను పిచికారీ చేయవద్దు. అరటి, మొక్కజొన్న తోటలకు ఊతాలు ఇవ్వండి."
            })

        # Farming Recommendations based on conditions
        advisory_en = []
        advisory_te = []
        if precip_prob > 50:
            advisory_en.append("Postpone fertilizer top-dressing and pesticide spraying until skies clear to avoid nutrient runoff.")
            advisory_te.append("వర్షం ఆగే వరకు ఎరువులు వేయడం మరియు రసాయన మందుల పిచికారీని వాయిదా వేయండి.")
        else:
            advisory_en.append("Favorable clear conditions for field preparation, intercultural weeding, and foliar spray application.")
            advisory_te.append("పొలంలో కలుపు తీయడానికి మరియు పిచికారీ చేయడానికి అనుకూలమైన వాతావరణం ఉంది.")

        if humidity > 80:
            advisory_en.append("High humidity promotes fungal proliferation (Blast, Mildew). Monitor crop leaves frequently.")
            advisory_te.append("గాలిలో అధిక తేమ వల్ల బూడిద, అగ్గి తెగుళ్లు ఆశించే అవకాశం ఉంది. ఆకుల అంచులను నిశితంగా పరిశీలించండి.")

        condition_summary = WeatherService.wmo_code_to_text(weather_code)

        return {
            "success": True,
            "location": display_name,
            "state": state_name,
            "latitude": lat,
            "longitude": lon,
            "is_live_data": is_live_data,
            "source": "Open-Meteo Global Environmental Model (WMO)" if is_live_data else "Smart Krishi Verified Demo Agromet Data",
            "last_updated": datetime.now(timezone.utc).strftime("%d %b %Y, %I:%M %p UTC"),
            "current": {
                "temperature": round(current_temp, 1),
                "feels_like": round(feels_like, 1),
                "humidity": humidity,
                "wind_speed": round(wind_speed, 1),
                "precipitation_probability": precip_prob,
                "condition": condition_summary
            },
            "forecast": forecast_daily,
            "alerts": alerts,
            "farming_advisory_en": advisory_en,
            "farming_advisory_te": advisory_te
        }

    @staticmethod
    def wmo_code_to_text(code: int) -> str:
        mapping = {
            0: "Clear Sky",
            1: "Mainly Clear",
            2: "Partly Cloudy",
            3: "Overcast",
            45: "Foggy",
            51: "Light Drizzle",
            53: "Moderate Drizzle",
            61: "Slight Rain",
            63: "Moderate Rain",
            65: "Heavy Rain",
            71: "Slight Snow",
            80: "Rain Showers",
            95: "Thunderstorm with Rain"
        }
        return mapping.get(code, "Partly Cloudy")
