# Smart Krishi Crop Advisor & Recommendation Engine
# Based on ICAR and ANGRAU agronomic crop suitability parameters

CROP_DATABASE = [
    {
        "id": "paddy",
        "name_en": "Paddy (Rice / వరి)",
        "name_te": "వరి ధాన్యం",
        "suitable_soils": ["clay", "alluvial", "black"],
        "min_ph": 5.5,
        "max_ph": 7.8,
        "optimal_seasons": ["kharif", "rabi"],
        "water_req": "high",
        "npk_needs": {"n": "high", "p": "medium", "k": "high"},
        "growing_days": "120 - 145 days",
        "estimated_yield_range": "24 - 32 Quintals / Acre",
        "reasons_en": "Alluvial or heavy clay soil with standing water availability matches Rice moisture requirements. High nutrient uptake capacity yields optimal grain panicles.",
        "reasons_te": "నీరు ఎక్కువగా నిల్వ ఉండే బంకమట్టి లేదా నల్లరేగడి నేలలు వరి సాగుకు అత్యంత అనుకూలం. తగినంత నీటి సదుపాయం ఉన్నప్పుడు మంచి దిగుబడి వస్తుంది.",
        "limitations_en": "High water dependence. Vulnerable to water scarcity during flowering. Susceptible to Blast disease under excessive humidity.",
        "limitations_te": "నీటి కొరత ఉంటే దిగుబడి గణనీయంగా తగ్గుతుంది. చలి కాలంలో లేదా ఎక్కువ తేమ ఉన్నప్పుడు అగ్గి తెగులు సోకే ప్రమాదం ఉంది."
    },
    {
        "id": "chilli",
        "name_en": "Chilli (Mirchi / మిరప)",
        "name_te": "ఎర్ర మిరప",
        "suitable_soils": ["black", "red", "loam"],
        "min_ph": 6.0,
        "max_ph": 7.5,
        "optimal_seasons": ["kharif", "rabi"],
        "water_req": "medium",
        "npk_needs": {"n": "high", "p": "medium", "k": "high"},
        "growing_days": "150 - 180 days",
        "estimated_yield_range": "18 - 25 Quintals Dry / Acre",
        "reasons_en": "Well-drained black or red soils with moderate irrigation produce high capsaicin content and vigorous fruiting branches.",
        "reasons_te": "నీరు నిలవని నల్లరేగడి లేదా ఎర్ర నేలల్లో మిరప సాగుకు అత్యధిక మార్కెట్ విలువ లభిస్తుంది.",
        "limitations_en": "Strictly cannot tolerate waterlogging; root rot occurs within 24-48 hours of standing water. Requires intensive vector pest management.",
        "limitations_te": "వర్షపు నీరు నిలిస్తే వేరు కుళ్ళు వ్యాపించి పంట ఎండిపోతుంది. తామర పురుగులు, తెల్లదోమ నివారణకు నిరంతర పర్యవేక్షణ అవసరం."
    },
    {
        "id": "cotton",
        "name_en": "Cotton (పత్తి)",
        "name_te": "పత్తి",
        "suitable_soils": ["black", "deep_loam"],
        "min_ph": 6.2,
        "max_ph": 8.2,
        "optimal_seasons": ["kharif"],
        "water_req": "medium",
        "npk_needs": {"n": "high", "p": "medium", "k": "high"},
        "growing_days": "150 - 170 days",
        "estimated_yield_range": "10 - 15 Quintals / Acre",
        "reasons_en": "Deep black soils with high moisture retention support deep taproot development through prolonged summer dry spells.",
        "reasons_te": "లోతైన నల్లరేగడి నేలలో తేమను పట్టి ఉంచే శక్తి ఎక్కువగా ఉండడం వల్ల పత్తి తల్లివేరు బాగా విస్తరిస్తుంది.",
        "limitations_en": "Sensitive to early waterlogging. Excessive unseasonal rain during boll bursting damages lint quality.",
        "limitations_te": "కాయలు పగిలే దశలో అకాల వర్షాలు కురిస్తే దూది రంగు మారి మార్కెట్ ధర తగ్గుతుంది."
    },
    {
        "id": "maize",
        "name_en": "Maize (Corn / మొక్కజొన్న)",
        "name_te": "మొక్కజొన్న",
        "suitable_soils": ["red", "loam", "alluvial", "black"],
        "min_ph": 5.8,
        "max_ph": 7.5,
        "optimal_seasons": ["kharif", "rabi", "zaid"],
        "water_req": "medium",
        "npk_needs": {"n": "high", "p": "high", "k": "medium"},
        "growing_days": "95 - 110 days",
        "estimated_yield_range": "25 - 35 Quintals / Acre",
        "reasons_en": "Fast growing, adaptable across multiple soil profiles. Consistent demand in poultry and starch industries.",
        "reasons_te": "స్వల్పకాలిక పంట, తక్కువ ఖర్చుతో పౌల్ట్రీ పరిశ్రమల నుంచి స్థిరమైన గిరాకీ ఉంటుంది.",
        "limitations_en": "High susceptibility to Fall Armyworm. Moisture stress during silking and tasseling reduces cob grain setting.",
        "limitations_te": "కత్తెర పురుగు దాడి ఎక్కువగా ఉంటుంది. పూత మరియు కంకి ఏర్పడే దశలో నీటి ఎద్దడి రాకూడదు."
    },
    {
        "id": "groundnut",
        "name_en": "Groundnut (వేరుశనగ)",
        "name_te": "వేరుశనగ",
        "suitable_soils": ["red", "sandy", "loam"],
        "min_ph": 5.8,
        "max_ph": 7.0,
        "optimal_seasons": ["kharif", "rabi"],
        "water_req": "low",
        "npk_needs": {"n": "low", "p": "medium", "k": "high"},
        "growing_days": "105 - 120 days",
        "estimated_yield_range": "12 - 18 Quintals / Acre",
        "reasons_en": "Light, friable red sandy loam allows easy peg penetration and pod expansion with low water requirement.",
        "reasons_te": "తేలికపాటి ఎర్ర నేలల్లో ఊడలు సులభంగా దిగి కాయలు బాగా వృద్ధి చెందుతాయి. తక్కువ నీటితో పండించవచ్చు.",
        "limitations_en": "Heavy clay soils obstruct peg penetration and make harvesting pods difficult. Calcium (gypsum) application required.",
        "limitations_te": "బంక నేలల్లో కాయ ఊరడం కష్టం. కాయలో గింజ బలిష్టంగా మారడానికి జిప్సం తప్పనిసరిగా వేయాలి."
    },
    {
        "id": "bengal_gram",
        "name_en": "Bengal Gram / Chickpea (శనగ)",
        "name_te": "శనగలు",
        "suitable_soils": ["black", "loam"],
        "min_ph": 6.0,
        "max_ph": 8.0,
        "optimal_seasons": ["rabi"],
        "water_req": "low",
        "npk_needs": {"n": "low", "p": "medium", "k": "low"},
        "growing_days": "85 - 100 days",
        "estimated_yield_range": "7 - 12 Quintals / Acre",
        "reasons_en": "Excellent residual moisture crop for Rabi season in black soils. Enriches soil nitrogen via symbiotic root nodules.",
        "reasons_te": "రబీ సీజన్‌లో నల్లరేగడి నేలలోని తేమతోనే అతి తక్కువ నీటితో పండుతుంది. నేలకు నత్రజని అందించి సారవంతం చేస్తుంది.",
        "limitations_en": "Rainfall or high humidity during flowering causes pod drop and collar rot.",
        "limitations_te": "పూత సమయంలో అకాల వర్షాలు కురిస్తే పూత రాలిపోవడం మరియు ఎండు తెగులు వచ్చే ప్రమాదం ఉంది."
    },
    {
        "id": "turmeric",
        "name_en": "Turmeric (పసుపు)",
        "name_te": "పసుపు",
        "suitable_soils": ["loam", "red", "alluvial"],
        "min_ph": 6.0,
        "max_ph": 7.5,
        "optimal_seasons": ["kharif"],
        "water_req": "medium",
        "npk_needs": {"n": "high", "p": "medium", "k": "high"},
        "growing_days": "240 - 270 days",
        "estimated_yield_range": "20 - 28 Quintals Cured / Acre",
        "reasons_en": "High commercial returns in well-drained friable soils with farmyard manure.",
        "reasons_te": "సేంద్రీయ ఎరువులు బాగా వేసిన ఎర్ర నేలల్లో పసుపు కొమ్ముల పరిమాణం మరియు కర్క్యుమిన్ శాతం బాగుంటుంది.",
        "limitations_en": "Long duration (8-9 months) locks land for whole year. High seed rhizome investment.",
        "limitations_te": "దీర్ఘకాలిక పంట (8-9 నెలలు). విత్తన పసుపు కొమ్ముల ఖర్చు అధికంగా ఉంటుంది."
    },
    {
        "id": "tomato",
        "name_en": "Tomato (టమోటా)",
        "name_te": "టమోటా",
        "suitable_soils": ["red", "loam", "black"],
        "min_ph": 6.0,
        "max_ph": 7.0,
        "optimal_seasons": ["kharif", "rabi", "zaid"],
        "water_req": "medium",
        "npk_needs": {"n": "high", "p": "high", "k": "high"},
        "growing_days": "110 - 130 days",
        "estimated_yield_range": "150 - 220 Quintals / Acre",
        "reasons_en": "High yielding short-duration vegetable with quick weekly harvest turnover and cash realization.",
        "reasons_te": "స్వల్పకాలిక పంట; ప్రతి వారం కోతలతో రైతులకు సత్వర నగదు ఆదాయం లభిస్తుంది.",
        "limitations_en": "High market price volatility. Highly perishable; requires nearby cold storage or immediate mandi access.",
        "limitations_te": "మార్కెట్ ధరల్లో తీవ్ర హెచ్చుతగ్గులు ఉంటాయి. ఎక్కువ కాలం నిల్వ ఉండదు కాబట్టి రవాణా సదుపాయం ఉండాలి."
    }
]

class CropAdvisorService:
    @staticmethod
    def recommend_crops(soil_type: str, season: str, water_avail: str, 
                        ph: float = None, n_val: str = None, p_val: str = None, k_val: str = None, 
                        land_area: float = 1.0) -> list:
        """
        Rule-based agronomic suitability matching algorithm.
        Returns scored and sorted list of recommended crops.
        """
        soil = (soil_type or "black").lower().strip()
        seas = (season or "kharif").lower().strip()
        water = (water_avail or "medium").lower().strip()

        scored_crops = []

        for crop in CROP_DATABASE:
            score = 50  # Base score

            # Soil compatibility (30 pts)
            if any(s in soil for s in crop["suitable_soils"]):
                score += 25
            else:
                score -= 15

            # Season compatibility (25 pts)
            if seas in crop["optimal_seasons"]:
                score += 20
            else:
                score -= 20

            # Water availability match (20 pts)
            if water == "high":
                if crop["water_req"] == "high":
                    score += 15
                elif crop["water_req"] == "medium":
                    score += 12
                else:
                    score += 5
            elif water == "medium":
                if crop["water_req"] == "medium":
                    score += 18
                elif crop["water_req"] == "low":
                    score += 15
                else:
                    score -= 15  # High water crop in medium water condition
            elif water == "low":
                if crop["water_req"] == "low":
                    score += 22
                elif crop["water_req"] == "medium":
                    score += 8
                else:
                    score -= 30  # High water crop under low water

            # pH suitability (10 pts)
            if ph is not None and ph > 0:
                if crop["min_ph"] <= ph <= crop["max_ph"]:
                    score += 10
                elif abs(ph - crop["min_ph"]) <= 0.5 or abs(ph - crop["max_ph"]) <= 0.5:
                    score += 3
                else:
                    score -= 10

            # Normalize to 0-100 range
            final_score = max(20, min(98, score))

            scored_crops.append({
                "crop_id": crop["id"],
                "name_en": crop["name_en"],
                "name_te": crop["name_te"],
                "match_score": final_score,
                "suitability_level": "Highly Recommended" if final_score >= 80 else ("Moderately Suitable" if final_score >= 65 else "Conditional / Marginal"),
                "duration": crop["growing_days"],
                "yield_range": crop["estimated_yield_range"],
                "reasons_en": crop["reasons_en"],
                "reasons_te": crop["reasons_te"],
                "limitations_en": crop["limitations_en"],
                "limitations_te": crop["limitations_te"]
            })

        # Sort descending by match score
        scored_crops.sort(key=lambda x: x["match_score"], reverse=True)
        return scored_crops
