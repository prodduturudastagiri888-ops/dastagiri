# Smart Irrigation Assistant Service
# Based on FAO-56 Crop Water Requirement Principles adapted for Indian Agro-Climatic conditions

CROP_WATER_FACTORS = {
    "paddy": {"name_en": "Paddy (Rice)", "name_te": "వరి", "daily_base_mm": 6.8, "stages": {"initial": 0.9, "vegetative": 1.15, "flowering": 1.35, "maturity": 0.85}},
    "chilli": {"name_en": "Chilli", "name_te": "మిరప", "daily_base_mm": 4.2, "stages": {"initial": 0.6, "vegetative": 0.9, "flowering": 1.15, "maturity": 0.75}},
    "cotton": {"name_en": "Cotton", "name_te": "పత్తి", "daily_base_mm": 5.0, "stages": {"initial": 0.5, "vegetative": 0.85, "flowering": 1.2, "maturity": 0.65}},
    "maize": {"name_en": "Maize (Corn)", "name_te": "మొక్కజొన్న", "daily_base_mm": 4.8, "stages": {"initial": 0.45, "vegetative": 0.85, "flowering": 1.15, "maturity": 0.7}},
    "tomato": {"name_en": "Tomato", "name_te": "టమోటా", "daily_base_mm": 4.5, "stages": {"initial": 0.5, "vegetative": 0.8, "flowering": 1.15, "maturity": 0.8}},
    "groundnut": {"name_en": "Groundnut", "name_te": "వేరుశనగ", "daily_base_mm": 4.0, "stages": {"initial": 0.45, "vegetative": 0.75, "flowering": 1.05, "maturity": 0.6}},
    "sugarcane": {"name_en": "Sugarcane", "name_te": "చెరకు", "daily_base_mm": 6.5, "stages": {"initial": 0.5, "vegetative": 1.0, "flowering": 1.25, "maturity": 0.8}},
    "bengal_gram": {"name_en": "Bengal Gram (Chickpea)", "name_te": "శనగలు", "daily_base_mm": 3.2, "stages": {"initial": 0.4, "vegetative": 0.7, "flowering": 0.95, "maturity": 0.45}}
}

SOIL_WATER_CAPACITY = {
    "black_clay": {"name_en": "Black Cotton (Clayey) Soil", "name_te": "నల్లరేగడి నేల", "retention": 1.4, "freq_modifier": 1.3, "notes_en": "High water-holding capacity; avoid overwatering to prevent root asphyxiation.", "notes_te": "నీటిని నిల్వ ఉంచే గుణం ఎక్కువ; వేరు కుళ్ళు నివారించడానికి అధిక నీటిని నిలవనీయవద్దు."},
    "red_loam": {"name_en": "Red Loamy Soil", "name_te": "ఎర్ర నేల", "retention": 1.0, "freq_modifier": 1.0, "notes_en": "Good drainage and moderate moisture retention. Well suited for regular moderate irrigation.", "notes_te": "మధ్యస్థంగా నీటిని నిల్వ ఉంచుకుంటుంది. క్రమం తప్పకుండా తేలికపాటి తడులు ఇవ్వడానికి అనుకూలం."},
    "alluvial": {"name_en": "Alluvial / Silt Soil", "name_te": "ఒండ్రు నేల", "retention": 1.1, "freq_modifier": 1.1, "notes_en": "High fertility with uniform moisture distribution across root depth.", "notes_te": "సారవంతమైన నేల; తేమ సమానంగా వ్యాపిస్తుంది."},
    "sandy": {"name_en": "Sandy / Light Soil", "name_te": "ఇసుక నేల", "retention": 0.65, "freq_modifier": 0.6, "notes_en": "Rapid percolation and low retention; requires frequent light water applications.", "notes_te": "నీరు త్వరగా ఇంకిపోతుంది; స్వల్ప వ్యవధిలో ఎక్కువసార్లు తడులు ఇవ్వాలి."}
}

METHOD_EFFICIENCY = {
    "drip": {"name_en": "Drip Irrigation", "name_te": "బిందు సేద్యం (డ్రిప్)", "efficiency": 0.90, "savings_vs_flood": 55},
    "sprinkler": {"name_en": "Sprinkler Irrigation", "name_te": "తుంపర సేద్యం (స్ప్రింక్లర్)", "efficiency": 0.75, "savings_vs_flood": 35},
    "furrow": {"name_en": "Furrow / Ridge & Furrow", "name_te": "కాలువ పద్ధతి", "efficiency": 0.60, "savings_vs_flood": 15},
    "flood": {"name_en": "Conventional Basin / Flood", "name_te": "సాంప్రదాయ పద్ధతి", "efficiency": 0.45, "savings_vs_flood": 0}
}

class IrrigationService:
    @staticmethod
    def calculate_irrigation(crop_key: str, soil_key: str, area_acres: float, 
                             growth_stage: str, recent_rain_mm: float, method_key: str) -> dict:
        """
        Calculates estimated crop water requirement, recommended schedule, and water-saving advice.
        """
        crop_info = CROP_WATER_FACTORS.get(crop_key, CROP_WATER_FACTORS["chilli"])
        soil_info = SOIL_WATER_CAPACITY.get(soil_key, SOIL_WATER_CAPACITY["black_clay"])
        method_info = METHOD_EFFICIENCY.get(method_key, METHOD_EFFICIENCY["drip"])

        # Base ET mm per day
        base_mm = crop_info["daily_base_mm"]
        stage_kc = crop_info["stages"].get(growth_stage, 1.0)
        daily_crop_water_mm = base_mm * stage_kc

        # Deduct effective rainfall (approx 70% of recent rainfall is effective)
        effective_rain = max(0.0, recent_rain_mm * 0.70)
        net_daily_water_mm = max(0.8, daily_crop_water_mm - (effective_rain / 5.0))

        # Adjust for application efficiency
        gross_water_mm_day = net_daily_water_mm / method_info["efficiency"]

        # 1 mm of water over 1 acre = 4,046.86 Liters
        liters_per_acre_per_day = gross_water_mm_day * 4046.86
        total_liters_per_day = round(liters_per_acre_per_day * area_acres)
        weekly_water_liters = total_liters_per_day * 7

        # Determine interval based on soil and crop
        base_interval_days = 2 if method_key == "drip" else (5 if method_key == "sprinkler" else 8)
        adjusted_interval = max(1, round(base_interval_days * soil_info["freq_modifier"]))

        # Hours per cycle estimate (assuming standard pump 3 HP = ~25,000 L/hr)
        cycle_water_liters = total_liters_per_day * adjusted_interval
        pump_hours_per_cycle = round(cycle_water_liters / 25000.0, 1)

        # Generate actionable water-saving recommendations
        tips_en = [
            f"Switching from conventional flood to {method_info['name_en']} saves an estimated {method_info['savings_vs_flood']}% of total irrigation water.",
            f"With {soil_info['name_en']}, operate irrigation every {adjusted_interval} days for approx {pump_hours_per_cycle} hours per cycle.",
            "Water early in the morning (6:00 AM - 9:00 AM) or after 5:00 PM to eliminate 20-30% loss from midday solar evaporation.",
            "Apply straw or crop residue mulching along crop rows to conserve up to 35% soil moisture."
        ]
        
        tips_te = [
            f"సాంప్రదాయ పద్ధతి కంటే {method_info['name_en']} ద్వారా దాదాపు {method_info['savings_vs_flood']}% వరకు నీటిని ఆదా చేయవచ్చు.",
            f"{soil_info['name_te']} లో ప్రతి {adjusted_interval} రోజులకు ఒకసారి సుమారు {pump_hours_per_cycle} గంటల సేపు మోటారు నడిపితే సరిపోతుంది.",
            "ఎండ వేడి లేని ఉదయం 6:00-9:00 లేదా సాయంత్రం 5:00 తర్వాత నీటి తడులు ఇస్తే 25% ఆవిరి నష్టాన్ని నివారించవచ్చు.",
            "చెరకు, మిరప వరుసల మధ్య ఎండుగడ్డితో మల్చింగ్ చేస్తే నేలలో తేమ 35% ఎక్కువ కాలం నిలిచి ఉంటుంది."
        ]

        return {
            "success": True,
            "crop_name_en": crop_info["name_en"],
            "crop_name_te": crop_info["name_te"],
            "soil_type_en": soil_info["name_en"],
            "area_acres": area_acres,
            "growth_stage": growth_stage.title(),
            "method_en": method_info["name_en"],
            "daily_water_liters": total_liters_per_day,
            "weekly_water_liters": weekly_water_liters,
            "cycle_frequency_days": adjusted_interval,
            "cycle_water_volume_liters": cycle_water_liters,
            "recommended_pump_hours": pump_hours_per_cycle,
            "water_savings_percent": method_info["savings_vs_flood"],
            "tips_en": tips_en,
            "tips_te": tips_te,
            "disclaimer_en": "ESTIMATE ONLY: Water volumes are agronomical estimates derived from FAO Penman-Monteith crop factors and regional soil textures. Exact soil moisture varies with atmospheric humidity, root depth, and ground slope.",
            "disclaimer_te": "అంచనా మాత్రమే: ఈ గణాంకాలు ప్రామాణిక వ్యవసాయ సూత్రాల ఆధారంగా తయారుచేసిన అంచనాలు. క్షేత్రస్థాయిలోని నేల స్వభావం, గాలిలో తేమను బట్టి హెచ్చుతగ్గులు ఉండవచ్చు."
        }
