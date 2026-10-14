import sqlite3
import os
from pathlib import Path
from werkzeug.security import generate_password_hash
from datetime import datetime, date, timedelta

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "smart_krishi.db"
SCHEMA_PATH = BASE_DIR / "database" / "schema.sql"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    print(f"Initializing database at: {DB_PATH}")
    os.makedirs(DB_PATH.parent, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    
    cursor = conn.cursor()
    
    # Check if users already exist
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] > 0:
        print("Database already initialized with seed data.")
        conn.close()
        return

    print("Seeding initial data...")

    # 1. Seed Users
    # Farmer user: farmer@smartkrishi.com / farmer123
    # Buyer user: buyer@smartkrishi.com / buyer123
    pwd_farmer = generate_password_hash("farmer123")
    pwd_buyer = generate_password_hash("buyer123")
    
    cursor.execute("""
        INSERT INTO users (username, email, password_hash, full_name, phone, role, preferred_language)
        VALUES 
        ('venkat_farmer', 'farmer@smartkrishi.com', ?, 'Venkat Rao M.', '+91 98480 22334', 'farmer', 'te'),
        ('lakshmi_traders', 'buyer@smartkrishi.com', ?, 'Lakshmi Agro Traders', '+91 94401 55667', 'buyer', 'en')
    """, (pwd_farmer, pwd_buyer))
    
    farmer_id = 1
    buyer_id = 2

    # 2. Seed Farmer Profile
    cursor.execute("""
        INSERT INTO farmer_profiles 
        (user_id, state, district, mandal, village, pin_code, land_size_acres, soil_type, irrigation_source, primary_crops)
        VALUES (?, 'Andhra Pradesh', 'Guntur', 'Tenali', 'Kollipara', '522304', 5.0, 'Black Cotton Soil', 'Borewell & Krishna Canal', 'Chilli, Paddy, Cotton')
    """, (farmer_id,))

    # 3. Seed Crop Records
    today = date.today()
    sow_rice = today - timedelta(days=45)
    harvest_rice = today + timedelta(days=75)
    sow_chilli = today - timedelta(days=30)
    harvest_chilli = today + timedelta(days=90)

    cursor.execute("""
        INSERT INTO crop_records (user_id, crop_name, variety, season, sowing_date, expected_harvest_date, acreage, status, notes)
        VALUES 
        (?, 'Paddy (Rice)', 'BPT 5204 (Samba Masuri)', 'Kharif', ?, ?, 3.0, 'growing', 'Tillering stage completed, healthy panicle initiation expected.'),
        (?, 'Chilli', 'Teja / G4 Variety', 'Kharif', ?, ?, 2.0, 'growing', 'Flowering and early fruit formation. Monitor for thrips and mites.')
    """, (farmer_id, sow_rice, harvest_rice, farmer_id, sow_chilli, harvest_chilli))

    # 4. Seed Mandi Market Prices (AP & Telangana key mandis)
    mandi_records = [
        ('Red Chilli (Teja)', 'ఎర్ర మిరపకాయలు (తేజ)', 'Guntur Mirchi Yard', 'Guntur', 'Andhra Pradesh', 19800.0, 16500.0, 22400.0, '₹ / Quintal', 'up', 4.5, today.strftime('%Y-%m-%d'), 1),
        ('Paddy (Common)', 'వరి ధాన్యం (సాధారణ)', 'Tenali AMC', 'Guntur', 'Andhra Pradesh', 2320.0, 2203.0, 2450.0, '₹ / Quintal', 'stable', 0.8, today.strftime('%Y-%m-%d'), 1),
        ('Paddy (Grade A)', 'వరి ధాన్యం (గ్రేడ్-ఎ)', 'Khammam Mandi', 'Khammam', 'Telangana', 2450.0, 2350.0, 2580.0, '₹ / Quintal', 'up', 2.1, today.strftime('%Y-%m-%d'), 1),
        ('Cotton (Medium Staple)', 'పత్తి (మధ్యస్థ పోగు)', 'Warangal Enamamula', 'Warangal', 'Telangana', 7450.0, 6800.0, 7920.0, '₹ / Quintal', 'up', 3.2, today.strftime('%Y-%m-%d'), 1),
        ('Cotton (Long Staple)', 'పత్తి (పొడవాటి పోగు)', 'Adoni Market Yard', 'Kurnool', 'Andhra Pradesh', 7850.0, 7100.0, 8300.0, '₹ / Quintal', 'down', -1.5, today.strftime('%Y-%m-%d'), 1),
        ('Turmeric (Finger)', 'పసుపు కొమ్ములు', 'Nizamabad Mandi', 'Nizamabad', 'Telangana', 14200.0, 12500.0, 16100.0, '₹ / Quintal', 'up', 6.0, today.strftime('%Y-%m-%d'), 1),
        ('Maize (Corn)', 'మొక్కజొన్న', 'Kurnool AMC', 'Kurnool', 'Andhra Pradesh', 2225.0, 2090.0, 2340.0, '₹ / Quintal', 'stable', 0.2, today.strftime('%Y-%m-%d'), 1),
        ('Bengal Gram (Chana)', 'శనగలు', 'Suryapet AMC', 'Suryapet', 'Telangana', 6150.0, 5800.0, 6400.0, '₹ / Quintal', 'down', -1.0, today.strftime('%Y-%m-%d'), 1),
        ('Tomato', 'టమోటా', 'Madanapalle Mandi', 'Annamayya', 'Andhra Pradesh', 1800.0, 1400.0, 2400.0, '₹ / Quintal', 'up', 8.5, today.strftime('%Y-%m-%d'), 1),
        ('Groundnut (Pods)', 'వేరుశనగ కాయలు', 'Anantapur Yard', 'Anantapur', 'Andhra Pradesh', 7200.0, 6600.0, 7650.0, '₹ / Quintal', 'stable', 0.5, today.strftime('%Y-%m-%d'), 1)
    ]

    cursor.executemany("""
        INSERT INTO market_prices 
        (crop_name_en, crop_name_te, mandi_name, district, state, modal_price, min_price, max_price, price_unit, price_trend, trend_pct, price_date, is_demo_data)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, mandi_records)

    # 5. Seed Marketplace Listings
    cursor.execute("""
        INSERT INTO marketplace_listings
        (user_id, crop_name, variety, category, quantity_quintals, price_per_quintal, is_negotiable, description, image_filename, village, district, state, delivery_options, harvest_date, contact_phone, status)
        VALUES
        (?, 'Paddy (Samba Masuri)', 'BPT 5204 A-Grade', 'Grains', 80.0, 2450.0, 1, 'Top quality freshly harvested Samba Masuri paddy with 12% moisture. Sun dried and cleaned.', 'sample_paddy.jpg', 'Kollipara', 'Guntur', 'Andhra Pradesh', 'Farm Gate Pickup / Lorry Transport arrangement', ?, '+91 98480 22334', 'active'),
        (?, 'Red Chilli', 'Teja Medium Best', 'Spices', 25.0, 20500.0, 1, 'Deep red color, high pungency SHU 70000+, properly cold stored, zero moisture contamination.', 'sample_chilli.jpg', 'Duggirala', 'Guntur', 'Andhra Pradesh', 'Direct Yard Delivery / Buyer Transport', ?, '+91 98480 22334', 'active')
    """, (farmer_id, today + timedelta(days=10), farmer_id, today - timedelta(days=5)))

    # 6. Seed Farming Calendar Tasks
    cursor.execute("""
        INSERT INTO farming_calendar_tasks
        (user_id, crop_name, task_title_en, task_title_te, task_type, scheduled_date, priority, status, notes)
        VALUES
        (?, 'Paddy (Rice)', 'Top dressing of Urea & Potash', 'యూరియా మరియు పొటాష్ రెండో దఫా ఎరువు వేయడం', 'fertilizer', ?, 'high', 'pending', 'Apply 25 kg Urea + 15 kg MOP per acre when soil has thin film of water.'),
        (?, 'Chilli', 'Neem Oil Spray for Thrips prevention', 'తామర పురుగుల నివారణకు వేపనూనె పిచికారీ', 'pesticide', ?, 'medium', 'pending', 'Use 5ml 10000 ppm Neem oil per liter of water during evening hours.'),
        (?, 'Paddy (Rice)', 'Intermittent Field Drainage (AWD)', 'నీటి తడుల మధ్య వరి పొలంలో గాలి ఆడేలా చేయడం', 'irrigation', ?, 'medium', 'completed', 'Drained stagnant water for 2 days to encourage deeper root branching.'),
        (?, 'Chilli', 'Fruit borer monitoring & Pheromone traps', 'కాయ తొలిచే పురుగు లింగాకర్షక బుట్టలు అమర్చడం', 'pesticide', ?, 'low', 'pending', 'Install 5 pheromone traps per acre at crop canopy level.')
    """, (farmer_id, (today + timedelta(days=2)).strftime('%Y-%m-%d'),
          farmer_id, (today + timedelta(days=4)).strftime('%Y-%m-%d'),
          farmer_id, (today - timedelta(days=3)).strftime('%Y-%m-%d'),
          farmer_id, (today + timedelta(days=7)).strftime('%Y-%m-%d')))

    # 7. Seed Notifications
    cursor.execute("""
        INSERT INTO notifications
        (user_id, title_en, title_te, message_en, message_te, category, action_url, is_read)
        VALUES
        (?, 'Heavy Rain Alert for Coastal AP', 'కోస్తా జిల్లాలకు భారీ వర్ష సూచన', 'IMD reports cyclonic circulation over Bay of Bengal. Expect moderate to heavy rain in Guntur district over next 48 hours. Secure harvested stock.', 'బంగాళాఖాతంలో అల్పపీడనం కారణంగా రాబోయే 48 గంటల్లో గుంటూరు జిల్లాలో మోస్తరు నుంచి భారీ వర్షాలు కురిసే అవకాశం ఉంది. కోసిన పంటను సురక్షిత ప్రాంతాలకు తరలించండి.', 'weather', '/weather', 0),
        (?, 'Teja Chilli Price Rose to ₹22,400', 'తేజ మిర్చి ధర క్వింటాలుకు ₹22,400 కు చేరింది', 'Demand increased at Guntur Mirchi Yard. Current modal price is ₹19,800/Qtl, high grade reaching ₹22,400/Qtl.', 'గుంటూరు మిర్చి యార్డులో నాణ్యమైన తేజ రకానికి డిమాండ్ పెరిగింది. క్వింటాలుకు గరిష్టంగా ₹22,400 పలుకుతోంది.', 'market', '/market', 0),
        (?, 'PM-KISAN Next Installment Alert', 'పీఎం-కిసాన్ తదుపరి విడత ప్రకటన', 'Check your e-KYC status to receive the ₹2,000 installment directly into your Aadhaar linked bank account.', 'పీఎం కిసాన్ ₹2,000 పొందడానికి మీ ఆధార్ లింక్ మరియు ఇ-కెవైసి సరిచూసుకోండి.', 'scheme', '/schemes', 1)
    """, (farmer_id, farmer_id, farmer_id))

    # 8. Seed Soil Health Record
    cursor.execute("""
        INSERT INTO soil_health_records
        (user_id, test_date, sample_id, soil_type, ph_level, electrical_conductivity, organic_carbon_pct, nitrogen_kg_ha, phosphorus_kg_ha, potassium_kg_ha, zinc_ppm, iron_ppm, status, recommendations_en, recommendations_te)
        VALUES
        (?, ?, 'AP-GNT-2026-884', 'Black Cotton Soil', 7.4, 0.42, 0.58, 210.0, 28.5, 340.0, 0.65, 5.2, 'Moderately Fertile',
        'Nitrogen is slightly low; supplement with green manuring (Dhaincha/Sunn hemp). Phosphorus is medium. Potassium is high. Apply 25 kg Zinc Sulphate per acre before sowing.',
        'నత్రజని శాతం కాస్త తక్కువగా ఉంది; పిల్లిపెసర లేదా జనుము వంటి పచ్చిరొట్ట ఎరువులు వాడండి. భాస్వరం మధ్యస్థం, పొటాష్ సమృద్ధిగా ఉంది. ఎకరాకు 25 కిలోల జింక్ సల్ఫేట్ వేయండి.')
    """, (farmer_id, (today - timedelta(days=60)).strftime('%Y-%m-%d')))

    # 9. Seed Expert Contacts Directory
    experts = [
        ('Dr. K. Srinivasulu, Ph.D.', 'డాక్టర్ కె. శ్రీనివాసులు', 'Senior Scientist (Plant Pathology)', 'సీనియర్ శాస్త్రవేత్త (సస్యరక్షణ)', 'Krishi Vigyan Kendra (KVK), Lam Farm', 'కృషి విజ్ఞాన కేంద్రం (కేవీకే), లాం ఫారం', 'Guntur', 'Andhra Pradesh', 'Pest & Disease Management in Chilli & Cotton', 'మిరప మరియు పత్తి తెగుళ్ల నివారణ', '+91 86325 99401', '+91 94409 11200', 'kvk.guntur@angrau.ac.in', '10:00 AM - 5:00 PM'),
        ('Dr. P. Radhika, Ph.D.', 'డాక్టర్ పి. రాధిక', 'Agronomist & Soil Scientist', 'వ్యవసాయ మరియు భూసార శాస్త్రవేత్త', 'Agricultural Research Station, Tenali', 'వ్యవసాయ పరిశోధనా కేంద్రం, తెనాలి', 'Guntur', 'Andhra Pradesh', 'Soil Fertility, Micro-irrigation, Rice systems', 'భూసార యాజమాన్యం, సూక్ష్మ నీటిపారుదల, వరి సాగు', '+91 86442 23115', '+91 98499 44321', 'ars.tenali@angrau.ac.in', '9:30 AM - 4:30 PM'),
        ('Sri M. Venkateshwarlu', 'శ్రీ ఎం. వెంకటేశ్వర్లు', 'Mandal Agricultural Officer (MAO)', 'మండల వ్యవసాయ అధికారి (ఎం.ఏ.ఓ)', 'Dept of Agriculture, Andhra Pradesh', 'వ్యవసాయ శాఖ, ఆంధ్రప్రదేశ్ ప్రభుత్వం', 'Tenali', 'Andhra Pradesh', 'Subsidies, PMFBY Insurance, Seed Distribution', 'సబ్సిడీలు, పంటల బీమా, విత్తనాల పంపిణీ', '+91 86442 22005', '+91 94906 33110', 'mao.tenali@ap.gov.in', '10:00 AM - 5:00 PM'),
        ('Dr. B. Ramanjaneyulu', 'డాక్టర్ బి. రామాంజనేయులు', 'Senior Agronomist (Dryland & Pulses)', 'సీనియర్ శాస్త్రవేత్త (ఆరుతడి & పప్పుధాన్యాలు)', 'PJTSAU Extension Center', 'ప్రొఫెసర్ జయశంకర్ తెలంగాణ వ్యవసాయ విశ్వవిద్యాలయం', 'Warangal', 'Telangana', 'Cotton, Maize, Redgram & Water Management', 'పత్తి, మొక్కజొన్న, కంది సాగు యాజమాన్యం', '+91 87024 55890', '+91 94405 88712', 'kvk.warangal@pjtsau.edu.in', '10:00 AM - 5:00 PM'),
        ('Kisan Call Centre (All India Free Helpline)', 'కిసాన్ కాల్ సెంటర్ (ఉచిత సహాయ కేంద్రం)', 'Toll-Free Agricultural Support Officers', 'ఉచిత వ్యవసాయ సలహా అధికారులు', 'Ministry of Agriculture & Farmers Welfare, GoI', 'భారత ప్రభుత్వ వ్యవసాయ మరియు రైతు సంక్షేమ మంత్రిత్వ శాఖ', 'National', 'India', '24x7 Agricultural advice in Telugu & English', 'తెలుగు మరియు ఆంగ్లంలో 24 గంటల ఉచిత వ్యవసాయ సలహాలు', '1800-180-1551', '1800-180-1551', 'kcc-dac@nic.in', '6:00 AM - 10:00 PM (Daily)')
    ]

    cursor.executemany("""
        INSERT INTO expert_contacts
        (name_en, name_te, designation_en, designation_te, organization_en, organization_te, district, state, specialization_en, specialization_te, phone, whatsapp, email, available_hours)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, experts)

    conn.commit()
    conn.close()
    print("Database initialization and seed data insertion completed successfully!")

if __name__ == "__main__":
    init_database()
