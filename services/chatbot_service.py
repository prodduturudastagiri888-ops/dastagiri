import re

class KrishiChatbotService:
    KNOWLEDGE_BASE = [
        {
            "patterns": [r"blast", r"వరి అగ్గి", r"neck blast", r"paddy disease", r"leaf spot"],
            "reply_en": "🌾 For **Rice Blast (అగ్గి తెగులు)**: Spray Tricyclazole 75% WP @ 0.6g/L or Isoprothiolane 40% EC @ 1.5ml/L of water. Avoid excessive urea fertilizer; apply balanced potash. Drain excess standing water if field is waterlogged.",
            "reply_te": "🌾 **వరి అగ్గి తెగులు నివారణకు**: లీటరు నీటికి ట్రైసైక్లాజోల్ 75% WP 0.6 గ్రాములు లేదా ఐసోప్రోథియోలేన్ 1.5 మి.లీ కలిపి పిచికారీ చేయండి. యూరియా వాడకాన్ని తగ్గించి, పొటాష్ ఎరువును వేయండి. పొలంలో నీరు ఎక్కువగా నిల్వ ఉండకుండా చూసుకోండి."
        },
        {
            "patterns": [r"thrips", r"chilli", r"leaf curl", r"ముడుత", r"మిరప", r"whitefly"],
            "reply_en": "🌶️ For **Chilli Leaf Curl & Thrips (తామర పురుగులు & ఆకు ముడుత)**: Install 15 yellow & 15 blue sticky traps per acre. Spray Fipronil 5% SC @ 2ml/L or Diafenthiuron 50% WP @ 1.25g/L. In early stages, spray 5ml/L 10,000 ppm Neem oil.",
            "reply_te": "🌶️ **మిరప ఆకు ముడుత మరియు తామర పురుగులకు**: ఎకరాకు 15 పసుపు, 15 నీలి రంగు జిగురు అట్టలను అమర్చండి. ఫిప్రోనిల్ 5% SC లీటరుకు 2 మి.లీ లేదా డయాఫెంథియురాన్ 1.25 గ్రాములు పిచికారీ చేయండి. ప్రారంభంలో వేపనూనె (10,000 ppm) 5 మి.లీ వాడవచ్చు."
        },
        {
            "patterns": [r"fertilizer", r"urea", r"npk", r"ఎరువు", r"పోషకాలు"],
            "reply_en": "🌱 **Fertilizer Management**: Apply fertilizers based on your Soil Health Card test. Generally, apply phosphorus (DAP/SSP) entirely as a basal dose before sowing. Split nitrogen (Urea) into 3 equal splits: basal, tillering/vegetative, and panicle initiation.",
            "reply_te": "🌱 **ఎరువుల యాజమాన్యం**: భూసార పరీక్ష ఆధారంగా ఎరువులు వాడండి. భాస్వరం ఎరువులను (DAP/సూపర్ ఫాస్ఫేట్) ఆఖరి దుక్కిలోనే వేయాలి. యూరియాను ఒకేసారి వేయకుండా 3 దఫాలుగా విభజించి వేయడం ద్వారా పైరు బలంగా ఎదుగుతుంది."
        },
        {
            "patterns": [r"pm kisan", r"scheme", r"rythu bharosa", r"సబ్సిడీ", r"పథకం", r"బీమా"],
            "reply_en": "🏛️ **Government Agricultural Schemes**: Under PM-KISAN, eligible farmers receive ₹6,000 annually in 3 installments of ₹2,000. Under PMFBY (Crop Insurance), notify crop damage within 72 hours. Check our 'Schemes' section for direct application portals.",
            "reply_te": "🏛️ **ప్రభుత్వ పథకాలు**: పీఎం-కిసాన్ ద్వారా అర్హులైన రైతులకు ఏడాదికి ₹6,000 (3 విడతల్లో ₹2,000 చొప్పున) అందుతాయి. పంట నష్టం జరిగితే 72 గంటల్లోగా 'క్రాప్ లాస్' విభాగంలో నమోదు చేసి PMFBY బీమాకు దరఖాస్తు చేసుకోవచ్చు."
        },
        {
            "patterns": [r"irrigation", r"water", r"నీరు", r"తడి", r"డ్రిప్", r"drip"],
            "reply_en": "💧 **Smart Irrigation Advice**: Drip irrigation saves 40-60% water and enhances yields by 25%. Always irrigate during early morning or evening hours to avoid evaporation losses. Check our 'Smart Irrigation' calculator for your exact field requirements.",
            "reply_te": "💧 **నీటిపారుదల సూచన**: బిందు సేద్యం (డ్రిప్) ద్వారా 50% నీరు ఆదా అవుతుంది మరియు కలుపు సమస్య తగ్గుతుంది. ఉదయం లేదా సాయంత్రం వేళల్లోనే నీటి తడులు ఇవ్వండి. మీ పొలానికి ఎంత నీరు కావాలో 'స్మార్ట్ ఇరిగేషన్' విభాగంలో లెక్కించవచ్చు."
        },
        {
            "patterns": [r"price", r"mandi", r"ధర", r"మార్కెట్", r"రేటు"],
            "reply_en": "📊 **Mandi Prices**: Current market rates in major Andhra & Telangana yards: Teja Chilli ₹19,800/Qtl, BPT Paddy ₹2,320-2,450/Qtl, Long Staple Cotton ₹7,850/Qtl. View the 'Market Prices' tab for live daily updates and historical trends.",
            "reply_te": "📊 **మార్కెట్ ధరలు**: గుంటూరు మిర్చి యార్డులో తేజ రకం క్వింటాలుకు సగటున ₹19,800 పలుకుతోంది. వరి ధాన్యం ₹2,320 - ₹2,450 మరియు పత్తి ₹7,850 వరకు ఉంది. పూర్తి వివరాలకు 'మార్కెట్ ధరలు' పేజీని చూడండి."
        },
        {
            "patterns": [r"weather", r"rain", r"వర్షం", r"ఎండ", r"వాతావరణం"],
            "reply_en": "⛅ **Weather Advisory**: Check the 'Weather' tab for real-time live Open-Meteo forecasts in your village. Never spray pesticides if rainfall probability exceeds 50% or during wind speeds over 25 km/h.",
            "reply_te": "⛅ **వాతావరణ సూచన**: మీ గ్రామంలో ప్రస్తుత వాతావరణం తెలుసుకోవడానికి 'వాతావరణం' ట్యాబ్ చూడండి. 50% కంటే ఎక్కువ వర్ష సూచన లేదా ఈదురు గాలులు ఉన్నప్పుడు మందులు పిచికారీ చేయవద్దు."
        }
    ]

    @staticmethod
    def get_response(user_query: str, lang: str = "en") -> dict:
        query_lower = (user_query or "").strip().lower()
        
        matched_reply_en = None
        matched_reply_te = None

        for item in KrishiChatbotService.KNOWLEDGE_BASE:
            for pat in item["patterns"]:
                if re.search(pat, query_lower, re.IGNORECASE):
                    matched_reply_en = item["reply_en"]
                    matched_reply_te = item["reply_te"]
                    break
            if matched_reply_en:
                break

        if not matched_reply_en:
            matched_reply_en = (
                "🌿 Hello! I am **Krishi Mitra**, your digital farming companion. "
                "I can assist you with Crop Diseases (Blast, Leaf Curl, Blight), Fertilizers (NPK, Urea doses), "
                "Smart Irrigation schedules, Weather alerts, Government schemes (PM-KISAN, PMFBY), and Mandi rates. "
                "Please describe your crop question or symptom!"
            )
            matched_reply_te = (
                "🌿 నమస్కారం! నేను మీ **కృషి మిత్ర** (రైతు సహాయకుడు). "
                "పంట తెగుళ్లు (అగ్గి తెగులు, ఆకు ముడుత), ఎరువుల మోతాదు, స్మార్ట్ నీటిపారుదల, వాతావరణ హెచ్చరికలు, "
                "ప్రభుత్వ పథకాలు (పీఎం-కిసాన్) మరియు మార్కెట్ ధరల గురించి నన్ను అడగవచ్చు. మీ సందేహాన్ని ఇక్కడ రాయండి!"
            )

        reply_text = matched_reply_te if lang == "te" else matched_reply_en

        return {
            "success": True,
            "response": reply_text,
            "language": lang,
            "disclaimer_en": "Krishi Mitra provides general agronomic guidance based on ICAR recommendations. In emergency outbreaks, contact your local Mandal Agricultural Officer or call 1800-180-1551.",
            "disclaimer_te": "కృషి మిత్ర ఇచ్చే సమాచారం ప్రాథమిక వ్యవసాయ సలహా మాత్రమే. అత్యవసర పరిస్థితుల్లో మీ గ్రామ వ్యవసాయ అధికారిని లేదా కిసాన్ కాల్ సెంటర్ 1800-180-1551 ను సంప్రదించండి."
        }
