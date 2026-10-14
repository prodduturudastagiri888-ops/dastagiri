# SMART KRISHI – Intelligent Farming Assistance System
> **"Empowering Farmers, Growing a Better Future."**
> **"రైతుకు చేయూత – వ్యవసాయానికి సరికొత్త భరోసా."**

Smart Krishi is a modern, responsive, full-stack agricultural assistance web application designed specifically for Indian farmers. It combines real-time agrometeorological forecasting, computer vision plant pathology, agronomic water budgeting, mandi price intelligence, and direct farmer-to-buyer commerce.

---

## 🌟 Key Features & Modules

### 1. 🌾 Homepage & Agromet Ticker
- Professional agricultural green-and-white theme with accessible high-contrast design.
- Live Mandi Price Ticker showing daily modal rates across AP and Telangana markets.
- Quick preview weather widget for immediate village condition awareness.
- Responsive design tailored for mobile, tablet, and desktop devices.

### 2. 📊 Farmer Dashboard
- Personalized greeting with farmer name, village, mandal, district, and farm acreage.
- Live weather conditions with actionable agricultural field advisories.
- Scheduled farming tasks calendar with completion tracking.
- Today's irrigation reminder and water volume targets.
- Severe weather and pest warning alerts.
- Quick-action shortcuts for instant diagnostics, weather, and produce sales.

### 3. 🔬 AI Crop Doctor (Plant Pathology)
- Upload leaf photographs via drag-and-drop or mobile camera.
- Computer vision colorimetry and texture heterogeneity analysis engine.
- Instant diagnosis of major crop ailments:
  - Rice Blast (*Pyricularia oryzae*)
  - Chilli Leaf Curl & Anthracnose
  - Cotton Bacterial Blight / Angular Leaf Spot
  - Tomato Early Blight (*Alternaria solani*)
  - Maize Fall Armyworm (*Spodoptera frugiperda*)
  - Healthy Plant Tissue
- Scientific explanations in English and Telugu.
- Dual remedies: chemical spray recommendations + zero-budget natural organic remedies (Jeevamrutha, Neem oil, buttermilk).
- Prominent agricultural expert disclaimer advising consultation before expensive chemical inputs.

### 4. ⛅ Real-Time Weather Forecast & Disaster Warning
- Integrated with the **Open-Meteo Free Global Forecast API** (no API key required, zero configuration).
- Geocoding support for searching villages, mandals, and districts across India.
- Current temperature, humidity, rainfall probability, and wind speed.
- Interactive **Chart.js** 7-day temperature & rain probability curve.
- Automated severe weather warnings (heavy rain >60%, heatwave >40°C, gusty winds).
- Forecast-based farming advisories (spraying rules, drainage precautions).

### 5. 💧 Smart Irrigation Assistant
- Based on FAO-56 Penman-Monteith crop water factor approximations.
- Inputs: Crop type, soil texture, field area (acres), crop growth stage, recent rainfall, and irrigation method (Drip, Sprinkler, Furrow, Flood).
- Outputs: Daily water requirement in Liters, recommended watering intervals, motor pumping hours per cycle, and water savings percentage (up to 55% saved with drip).

### 6. 🌱 Scientific Crop Advisor
- Rule-based agronomic recommendation engine matching ICAR and state agricultural university criteria.
- Inputs: Soil type, planting season (Kharif, Rabi, Zaid), water availability, and optional soil pH/NPK values.
- Outputs: Scored and ranked crops with detailed rationale and critical limitation warnings.

### 7. 📈 Mandi Market Price Intelligence
- Daily modal, minimum, and maximum prices per quintal for major Indian crops.
- Key yards covered: Guntur Mirchi Yard, Warangal Enamamula, Tenali, Nizamabad, Kurnool, Suryapet, Khammam, Madanapalle.
- Interactive **Chart.js** historical price trend graphs (7-day and 30-day).
- Nearby market yard distance and price comparison to optimize transport expenses.

### 8. 🛒 Farmer-to-Buyer Direct Marketplace
- Farmers list agricultural produce directly with photos, quantity (quintals), asking price, and delivery terms.
- Search and filter by category (Grains, Spices, Commercial, Pulses) and district.
- Safe contact mechanism: direct phone calls, WhatsApp inquiries, and formal inquiry submission modals.
- Fraud safeguards: clear policy stating physical verification prior to cash settlement.

### 9. 🌐 Bilingual Support (English & Telugu - తెలుగు)
- Dedicated translation dictionary (`static/js/translations.js`) covering all interface labels, buttons, and advisories.
- Real-time client-side language switching without page reload, plus session synchronization.
- Rural-friendly vocabulary and typography.

### 10. 💡 10 Unique Innovative Features
1. **Farming Calendar**: Sowing, fertilizer top-dressing, and harvest reminders with priority tags.
2. **Crop Expense & Profit Calculator**: Calculate input costs (seeds, fertilizer, labor, machinery) vs expected revenue, net profit per acre, and ROI % with a Chart.js expense distribution doughnut.
3. **Government Agricultural Schemes Portal**: Direct links, eligibility criteria, and benefits for PM-KISAN, PMFBY (Crop Insurance), PM-KUSUM (Solar Pumps), and Soil Health Card.
4. **Voice-Friendly Interface**: Integrated **Web Speech API** for speaking questions via microphone and audio readout (Text-to-Speech) of diagnostic advice.
5. **Low-Bandwidth Mode**: Toggle button to disable heavy graphics and optimize typography for 2G/3G rural networks.
6. **Offline Advice Caching**: Saves viewed farming advice to browser `localStorage` for offline reference during network dropouts.
7. **Soil Health Records Tracker**: Log chemical soil test values (pH, Organic Carbon, N, P, K) to track soil fertility across seasons.
8. **Verified KVK Scientists Directory**: Direct contact numbers, WhatsApp links, and emails for Krishi Vigyan Kendra scientists and extension officers.
9. **Krishi Mitra Multilingual AI Chatbot**: Interactive conversational helper answering questions on pests, fertilizers, and government policies.
10. **Crop-Loss Reporting Tool**: Record flood, storm, or drought damage with survey numbers, photo evidence, and damage percentage to generate formal PMFBY insurance claims.

---

## 🛠️ Technology Stack
- **Frontend**: HTML5, CSS3, JavaScript (ES6+), Bootstrap 5.3, Font Awesome 6.
- **Charts**: Chart.js 4.4.
- **Backend**: Python 3.11, Flask 3.1.
- **Database**: SQLite 3 with parameterized queries and foreign keys.
- **Image Processing**: Pillow 12.3.
- **Weather API**: Open-Meteo Global Environmental Model.
- **Speech**: Web Speech API (SpeechRecognition + SpeechSynthesis).

---

## 🚀 Quick Setup & Run Instructions

### 1. Requirements
- Python 3.10 or higher.

### 2. Installation
Open your terminal in the `smart_krishi` project folder:
```bash
# Install dependencies
pip install -r requirements.txt
```

### 3. Initialize Database
Initialize the SQLite database with schema and rich demonstration records:
```bash
python database/init_db.py
```

### 4. Run Application
```bash
python app.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 👤 Demo Login Credentials
To test personalized farmer and buyer experiences immediately:

| Role | Username / Email | Password |
|---|---|---|
| **Farmer** | `farmer@smartkrishi.com` | `farmer123` |
| **Buyer / Trader** | `buyer@smartkrishi.com` | `buyer123` |

*(You can also click "Register" on the top navigation bar to create a new farmer profile).*

---

## 📁 Project Structure
```
smart_krishi/
├── app.py                      # Main Flask application and API routes
├── config.py                   # Configuration and environment settings
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── README.md                   # Documentation
├── database/
│   ├── schema.sql              # Database schema (14 tables)
│   ├── init_db.py              # Initializer & realistic seed data
│   └── smart_krishi.db         # SQLite database
├── services/
│   ├── disease_service.py      # AI Crop Doctor pathology engine
│   ├── weather_service.py      # Real Open-Meteo weather integration
│   ├── irrigation_service.py   # FAO-56 irrigation calculator
│   ├── crop_advisor.py         # Agronomic crop recommendation engine
│   ├── market_service.py       # Mandi market prices and comparisons
│   └── chatbot_service.py      # Krishi Mitra multilingual AI assistant
├── static/
│   ├── css/
│   │   └── style.css           # Custom green & white responsive CSS
│   ├── js/
│   │   ├── translations.js     # English & Telugu translation dictionary
│   │   ├── voice.js            # Web Speech API (STT & TTS)
│   │   ├── charts.js           # Chart.js visualization setups
│   │   └── main.js             # Low-bandwidth, offline cache & dropzone
│   └── uploads/                # Leaf photos & produce listings
└── templates/
    ├── base.html               # Main layout with navbar & footer
    ├── index.html              # Homepage with hero & mandi ticker
    ├── contact.html            # Helplines & emergency support
    ├── auth/                   # Login & registration templates
    ├── dashboard/              # Personalized farmer dashboard
    ├── crop_doctor/            # AI leaf disease diagnosis & history
    ├── weather/                # Forecast, alerts & agromet advice
    ├── irrigation/             # Smart water budgeting tool
    ├── advisor/                # Crop recommendation system
    ├── market/                 # Mandi prices & trends
    ├── marketplace/            # Direct produce trading & listing form
    ├── calendar/               # Farm activity scheduler
    ├── calculator/             # Crop expense & profit calculator
    ├── schemes/                # Government welfare schemes
    ├── soil_health/            # Soil health records tracker
    ├── experts/                # KVK scientists directory
    ├── chatbot/                # Krishi Mitra AI assistant
    └── loss_report/            # PMFBY crop loss reporting tool
```

---

## 🔒 Security & Privacy Safeguards
- **Password Hashing**: Uses Werkzeug's secure SHA-256 PBKDF2 hashing algorithm.
- **Database Safety**: Parameterized queries across all database operations to prevent SQL injection.
- **File Upload Protection**: Validates extensions (`.png`, `.jpg`, `.jpeg`, `.webp`), secures filenames with `secure_filename`, and limits uploads to 16 MB.
- **Privacy First**: Buyer inquiries are safely routed without exposing sensitive personal banking details.
