-- Smart Krishi SQLite Database Schema
PRAGMA foreign_keys = ON;

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    phone TEXT,
    role TEXT CHECK(role IN ('farmer', 'buyer', 'expert', 'admin')) DEFAULT 'farmer',
    preferred_language TEXT CHECK(preferred_language IN ('en', 'te')) DEFAULT 'en',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Farmer Profiles Table
CREATE TABLE IF NOT EXISTS farmer_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    state TEXT DEFAULT 'Andhra Pradesh',
    district TEXT DEFAULT 'Guntur',
    mandal TEXT DEFAULT 'Tenali',
    village TEXT DEFAULT 'Kollipara',
    pin_code TEXT DEFAULT '522304',
    land_size_acres REAL DEFAULT 4.5,
    soil_type TEXT DEFAULT 'Black Cotton Soil',
    irrigation_source TEXT DEFAULT 'Borewell & Canal',
    primary_crops TEXT DEFAULT 'Paddy, Chilli, Cotton',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 3. Crop Records Table
CREATE TABLE IF NOT EXISTS crop_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    crop_name TEXT NOT NULL,
    variety TEXT,
    season TEXT CHECK(season IN ('Kharif', 'Rabi', 'Zaid')) DEFAULT 'Kharif',
    sowing_date DATE,
    expected_harvest_date DATE,
    acreage REAL,
    status TEXT CHECK(status IN ('sown', 'growing', 'harvested', 'planned')) DEFAULT 'growing',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 4. Disease Diagnosis History Table
CREATE TABLE IF NOT EXISTS disease_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    crop_name TEXT NOT NULL,
    image_filename TEXT,
    predicted_disease_en TEXT NOT NULL,
    predicted_disease_te TEXT NOT NULL,
    confidence REAL NOT NULL,
    severity TEXT CHECK(severity IN ('Mild', 'Moderate', 'Severe', 'Healthy')),
    causes_en TEXT,
    causes_te TEXT,
    remedies_chemical_en TEXT,
    remedies_chemical_te TEXT,
    remedies_organic_en TEXT,
    remedies_organic_te TEXT,
    prevention_en TEXT,
    prevention_te TEXT,
    is_demo_mode INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- 5. Weather Cache Table
CREATE TABLE IF NOT EXISTS weather_cache (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    district TEXT UNIQUE NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    temp_c REAL,
    humidity_percent INTEGER,
    rainfall_prob_percent INTEGER,
    wind_speed_kmh REAL,
    weather_desc TEXT,
    weather_icon TEXT,
    forecast_json TEXT,
    alerts_json TEXT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Irrigation Recommendations Log
CREATE TABLE IF NOT EXISTS irrigation_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    crop_name TEXT NOT NULL,
    soil_type TEXT NOT NULL,
    field_area_acres REAL NOT NULL,
    growth_stage TEXT NOT NULL,
    irrigation_method TEXT NOT NULL,
    recent_rainfall_mm REAL DEFAULT 0,
    water_req_liters REAL NOT NULL,
    schedule_interval_days INTEGER NOT NULL,
    water_saving_pct REAL NOT NULL,
    tips_en TEXT,
    tips_te TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- 7. Market Prices Table (Mandi Intelligence)
CREATE TABLE IF NOT EXISTS market_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    crop_name_en TEXT NOT NULL,
    crop_name_te TEXT NOT NULL,
    mandi_name TEXT NOT NULL,
    district TEXT NOT NULL,
    state TEXT DEFAULT 'Andhra Pradesh',
    modal_price REAL NOT NULL,
    min_price REAL NOT NULL,
    max_price REAL NOT NULL,
    price_unit TEXT DEFAULT '₹ / Quintal',
    price_trend TEXT CHECK(price_trend IN ('up', 'down', 'stable')) DEFAULT 'stable',
    trend_pct REAL DEFAULT 0.0,
    price_date DATE NOT NULL,
    is_demo_data INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8. Marketplace Listings (Farmer-to-Buyer)
CREATE TABLE IF NOT EXISTS marketplace_listings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    crop_name TEXT NOT NULL,
    variety TEXT,
    category TEXT DEFAULT 'Grains',
    quantity_quintals REAL NOT NULL,
    price_per_quintal REAL NOT NULL,
    is_negotiable INTEGER DEFAULT 1,
    description TEXT,
    image_filename TEXT,
    village TEXT NOT NULL,
    district TEXT NOT NULL,
    state TEXT DEFAULT 'Andhra Pradesh',
    delivery_options TEXT DEFAULT 'Farm Gate Pickup / Local Delivery',
    harvest_date DATE,
    contact_phone TEXT NOT NULL,
    status TEXT CHECK(status IN ('active', 'pending', 'sold')) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 9. Marketplace Inquiries Table
CREATE TABLE IF NOT EXISTS marketplace_inquiries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    listing_id INTEGER NOT NULL,
    buyer_id INTEGER,
    buyer_name TEXT NOT NULL,
    buyer_phone TEXT NOT NULL,
    offered_price_per_quintal REAL,
    quantity_requested REAL NOT NULL,
    message TEXT,
    status TEXT CHECK(status IN ('new', 'contacted', 'accepted', 'rejected')) DEFAULT 'new',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (listing_id) REFERENCES marketplace_listings(id) ON DELETE CASCADE,
    FOREIGN KEY (buyer_id) REFERENCES users(id) ON DELETE SET NULL
);

-- 10. Notifications Table
CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title_en TEXT NOT NULL,
    title_te TEXT NOT NULL,
    message_en TEXT NOT NULL,
    message_te TEXT NOT NULL,
    category TEXT CHECK(category IN ('weather', 'market', 'irrigation', 'disease', 'scheme', 'general')) DEFAULT 'general',
    action_url TEXT,
    is_read INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 11. Farming Calendar Tasks Table
CREATE TABLE IF NOT EXISTS farming_calendar_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    crop_name TEXT NOT NULL,
    task_title_en TEXT NOT NULL,
    task_title_te TEXT NOT NULL,
    task_type TEXT CHECK(task_type IN ('sowing', 'irrigation', 'fertilizer', 'pesticide', 'weeding', 'harvesting')) NOT NULL,
    scheduled_date DATE NOT NULL,
    priority TEXT CHECK(priority IN ('low', 'medium', 'high')) DEFAULT 'medium',
    status TEXT CHECK(status IN ('pending', 'completed')) DEFAULT 'pending',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 12. Soil Health Records Table
CREATE TABLE IF NOT EXISTS soil_health_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    test_date DATE NOT NULL,
    sample_id TEXT,
    soil_type TEXT NOT NULL,
    ph_level REAL NOT NULL,
    electrical_conductivity REAL,
    organic_carbon_pct REAL,
    nitrogen_kg_ha REAL,
    phosphorus_kg_ha REAL,
    potassium_kg_ha REAL,
    zinc_ppm REAL,
    iron_ppm REAL,
    status TEXT DEFAULT 'Healthy',
    recommendations_en TEXT,
    recommendations_te TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 13. Crop Loss Reports Table (PMFBY Insurance Assistance)
CREATE TABLE IF NOT EXISTS crop_loss_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    claim_id TEXT UNIQUE NOT NULL,
    crop_name TEXT NOT NULL,
    survey_number TEXT NOT NULL,
    village TEXT NOT NULL,
    district TEXT NOT NULL,
    acreage_affected REAL NOT NULL,
    cause_of_loss TEXT CHECK(cause_of_loss IN ('Excessive Rainfall / Floods', 'Cyclone / High Winds', 'Severe Drought', 'Hailstorm', 'Pest Outbreak', 'Crop Disease')) NOT NULL,
    damage_date DATE NOT NULL,
    loss_percentage INTEGER NOT NULL,
    estimated_financial_loss REAL,
    evidence_image TEXT,
    remarks TEXT,
    status TEXT CHECK(status IN ('draft', 'submitted', 'under_verification', 'approved')) DEFAULT 'submitted',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- 14. Expert Contacts Directory
CREATE TABLE IF NOT EXISTS expert_contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_en TEXT NOT NULL,
    name_te TEXT NOT NULL,
    designation_en TEXT NOT NULL,
    designation_te TEXT NOT NULL,
    organization_en TEXT NOT NULL,
    organization_te TEXT NOT NULL,
    district TEXT NOT NULL,
    state TEXT DEFAULT 'Andhra Pradesh',
    specialization_en TEXT,
    specialization_te TEXT,
    phone TEXT NOT NULL,
    whatsapp TEXT,
    email TEXT,
    available_hours TEXT DEFAULT '10:00 AM - 5:00 PM'
);
