import os
import sqlite3
import uuid
from pathlib import Path
from datetime import datetime, date

from flask import (
    Flask, render_template, request, redirect, url_for,
    session, flash, jsonify, g
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from config import Config
from services.disease_service import CropDiseaseService
from services.weather_service import WeatherService
from services.irrigation_service import IrrigationService
from services.crop_advisor import CropAdvisorService
from services.market_service import MarketService
from services.chatbot_service import KrishiChatbotService

app = Flask(__name__)
app.config.from_object(Config)

# Ensure upload directory exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Database Helper
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(app.config["DATABASE_PATH"])
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop("db", None)
    if db is not None:
        db.close()

# Allowed file check
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

# Context processor for session user, language, and notifications count
@app.context_processor
def inject_global_data():
    lang = session.get("lang", "en")
    user = None
    unread_notifs = 0
    if "user_id" in session:
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT id, username, email, full_name, role, preferred_language FROM users WHERE id = ?", (session["user_id"],))
        user_row = cur.fetchone()
        if user_row:
            user = dict(user_row)
        
        cur.execute("SELECT COUNT(*) FROM notifications WHERE user_id = ? AND is_read = 0", (session["user_id"],))
        unread_notifs = cur.fetchone()[0]

    return {
        "current_user": user,
        "current_lang": lang,
        "unread_notifications_count": unread_notifs,
        "current_year": datetime.now().year
    }

# Language Switcher
@app.route("/set-language/<lang_code>")
def set_language(lang_code):
    if lang_code in app.config["LANGUAGES"]:
        session["lang"] = lang_code
        if "user_id" in session:
            db = get_db()
            db.execute("UPDATE users SET preferred_language = ? WHERE id = ?", (lang_code, session["user_id"]))
            db.commit()
    return redirect(request.referrer or url_for("home"))

# ----------------- AUTHENTICATION ROUTES -----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        identifier = request.form.get("identifier", "").strip()
        password = request.form.get("password", "")

        if not identifier or not password:
            flash("Please enter both username/email and password.", "danger")
            return render_template("auth/login.html")

        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT * FROM users WHERE username = ? OR email = ?", (identifier, identifier))
        user = cur.fetchone()

        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]
            session["lang"] = user["preferred_language"] or "en"
            flash(f"Welcome back, {user['full_name']}! / స్వాగతం!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials. Please verify your login details.", "danger")

    return render_template("auth/login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        username = request.form.get("username", "").strip().lower()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "")
        role = request.form.get("role", "farmer")
        state = request.form.get("state", "Andhra Pradesh")
        district = request.form.get("district", "Guntur")
        village = request.form.get("village", "")
        land_size = request.form.get("land_size_acres", "2.0")
        soil_type = request.form.get("soil_type", "Black Cotton Soil")
        primary_crops = request.form.get("primary_crops", "Paddy, Chilli")

        if not full_name or not username or not email or not password:
            flash("Please fill in all mandatory fields.", "warning")
            return render_template("auth/register.html")

        db = get_db()
        cur = db.cursor()

        # Check existing user
        cur.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
        if cur.fetchone():
            flash("Username or Email already registered. Please log in.", "danger")
            return render_template("auth/register.html")

        # Create user
        pwd_hash = generate_password_hash(password)
        cur.execute("""
            INSERT INTO users (username, email, password_hash, full_name, phone, role, preferred_language)
            VALUES (?, ?, ?, ?, ?, ?, 'en')
        """, (username, email, pwd_hash, full_name, phone, role))
        user_id = cur.lastrowid

        # Create profile
        cur.execute("""
            INSERT INTO farmer_profiles (user_id, state, district, village, land_size_acres, soil_type, primary_crops)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, state, district, village, float(land_size or 2.0), soil_type, primary_crops))

        # Add welcome notification
        cur.execute("""
            INSERT INTO notifications (user_id, title_en, title_te, message_en, message_te, category, action_url)
            VALUES (?, 'Welcome to Smart Krishi!', 'స్మార్ట్ కృషికి స్వాగతం!', 
                    'Explore AI Crop Doctor, Live Weather, Mandi Prices, and Smart Irrigation advice.', 
                    'క్రాప్ డాక్టర్, వాతావరణం, మార్కెట్ ధరలు మరియు నీటిపారుదల సలహాలను ఉపయోగించండి.', 'general', '/dashboard')
        """, (user_id,))

        db.commit()

        # Log user in
        session["user_id"] = user_id
        session["username"] = username
        session["role"] = role
        session["lang"] = "en"
        flash("Registration successful! Welcome to Smart Krishi.", "success")
        return redirect(url_for("dashboard"))

    return render_template("auth/register.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been safely logged out. / మీరు విజయవంతంగా లాగౌట్ అయ్యారు.", "info")
    return redirect(url_for("home"))

# ----------------- MAIN HOMEPAGE -----------------
@app.route("/")
def home():
    db = get_db()
    cur = db.cursor()
    
    # Fetch sample market prices for ticker
    cur.execute("SELECT crop_name_en, crop_name_te, mandi_name, modal_price, price_trend, trend_pct FROM market_prices LIMIT 6")
    mandi_ticker = [dict(r) for r in cur.fetchall()]

    # Quick preview weather for Guntur
    quick_weather = WeatherService.get_weather("Guntur")

    # Sample active marketplace listings
    cur.execute("""
        SELECT ml.*, u.full_name as farmer_name 
        FROM marketplace_listings ml
        JOIN users u ON ml.user_id = u.id
        WHERE ml.status = 'active'
        ORDER BY ml.created_at DESC LIMIT 3
    """)
    featured_listings = [dict(r) for r in cur.fetchall()]

    return render_template("index.html", 
                           mandi_ticker=mandi_ticker, 
                           weather=quick_weather, 
                           listings=featured_listings)

# ----------------- FARMER DASHBOARD -----------------
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Please log in to access your farmer dashboard.", "warning")
        return redirect(url_for("login"))

    db = get_db()
    cur = db.cursor()
    user_id = session["user_id"]

    # Farmer profile
    cur.execute("SELECT * FROM farmer_profiles WHERE user_id = ?", (user_id,))
    profile_row = cur.fetchone()
    profile = dict(profile_row) if profile_row else {"district": "Guntur", "village": "Kollipara", "land_size_acres": 4.0, "soil_type": "Black Cotton Soil"}

    # Current Weather
    weather = WeatherService.get_weather(profile.get("district", "Guntur"))

    # Active Crops
    cur.execute("SELECT * FROM crop_records WHERE user_id = ? ORDER BY sowing_date DESC", (user_id,))
    crops = [dict(r) for r in cur.fetchall()]

    # Upcoming Calendar Tasks
    cur.execute("SELECT * FROM farming_calendar_tasks WHERE user_id = ? ORDER BY scheduled_date ASC LIMIT 4", (user_id,))
    tasks = [dict(r) for r in cur.fetchall()]

    # Latest Notifications
    cur.execute("SELECT * FROM notifications WHERE user_id = ? ORDER BY created_at DESC LIMIT 5", (user_id,))
    notifications = [dict(r) for r in cur.fetchall()]

    # Top Mandi Prices
    cur.execute("SELECT * FROM market_prices ORDER BY modal_price DESC LIMIT 5")
    market_rates = [dict(r) for r in cur.fetchall()]

    # Recent Leaf Diagnoses
    cur.execute("SELECT * FROM disease_history WHERE user_id = ? ORDER BY created_at DESC LIMIT 2", (user_id,))
    recent_diagnoses = [dict(r) for r in cur.fetchall()]

    return render_template("dashboard/index.html",
                           profile=profile,
                           weather=weather,
                           crops=crops,
                           tasks=tasks,
                           notifications=notifications,
                           market_rates=market_rates,
                           recent_diagnoses=recent_diagnoses)

# ----------------- AI CROP DOCTOR -----------------
@app.route("/crop-doctor", methods=["GET", "POST"])
def crop_doctor():
    diagnosis_result = None
    uploaded_image_url = None

    if request.method == "POST":
        file = request.files.get("leaf_image")
        crop_type = request.form.get("crop_type", "Chilli")

        if not file or file.filename == "":
            flash("Please select a leaf photograph to analyze.", "warning")
        elif not allowed_file(file.filename):
            flash("Invalid image format. Allowed formats: PNG, JPG, JPEG, WEBP.", "danger")
        else:
            ext = file.filename.rsplit(".", 1)[1].lower()
            unique_name = f"leaf_{uuid.uuid4().hex[:10]}.{ext}"
            saved_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_name)
            file.save(saved_path)
            uploaded_image_url = url_for("static", filename=f"uploads/{unique_name}")

            # Execute Disease Diagnosis Engine
            diagnosis_result = CropDiseaseService.analyze_leaf_image(saved_path, crop_type)

            # Record in database if user is logged in
            if diagnosis_result.get("success") and "user_id" in session:
                raw_sev = str(diagnosis_result.get("severity", "Moderate")).lower()
                if "sev" in raw_sev or "high" in raw_sev:
                    clean_sev = "Severe"
                elif "mild" in raw_sev or "low" in raw_sev:
                    clean_sev = "Mild"
                elif "health" in raw_sev:
                    clean_sev = "Healthy"
                else:
                    clean_sev = "Moderate"

                db = get_db()
                db.execute("""
                    INSERT INTO disease_history 
                    (user_id, crop_name, image_filename, predicted_disease_en, predicted_disease_te, confidence, severity, 
                     causes_en, causes_te, remedies_chemical_en, remedies_chemical_te, remedies_organic_en, remedies_organic_te, 
                     prevention_en, prevention_te, is_demo_mode)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
                """, (
                    session["user_id"],
                    diagnosis_result["crop_name"],
                    unique_name,
                    diagnosis_result["disease_name_en"],
                    diagnosis_result["disease_name_te"],
                    diagnosis_result["confidence"],
                    clean_sev,
                    diagnosis_result["causes_en"],
                    diagnosis_result["causes_te"],
                    diagnosis_result["remedies_chemical_en"],
                    diagnosis_result["remedies_chemical_te"],
                    diagnosis_result["remedies_organic_en"],
                    diagnosis_result["remedies_organic_te"],
                    diagnosis_result["prevention_en"],
                    diagnosis_result["prevention_te"]
                ))
                db.commit()

    return render_template("crop_doctor/index.html", 
                           result=diagnosis_result, 
                           image_url=uploaded_image_url)

@app.route("/crop-doctor/history")
def crop_doctor_history():
    if "user_id" not in session:
        flash("Please log in to view your crop diagnosis history.", "warning")
        return redirect(url_for("login"))

    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM disease_history WHERE user_id = ? ORDER BY created_at DESC", (session["user_id"],))
    records = [dict(r) for r in cur.fetchall()]
    return render_template("crop_doctor/history.html", records=records)

# ----------------- WEATHER MODULE -----------------
@app.route("/weather", methods=["GET", "POST"])
def weather():
    query_location = "Guntur"
    
    # If logged in, default to farmer's district
    if "user_id" in session:
        db = get_db()
        cur = db.cursor()
        cur.execute("SELECT district FROM farmer_profiles WHERE user_id = ?", (session["user_id"],))
        prof = cur.fetchone()
        if prof and prof["district"]:
            query_location = prof["district"]

    if request.method == "POST":
        input_loc = request.form.get("location", "").strip()
        if input_loc:
            query_location = input_loc

    weather_data = WeatherService.get_weather(query_location)
    return render_template("weather/index.html", weather=weather_data, query=query_location)

@app.route("/api/weather")
def api_weather():
    loc = request.args.get("location", "Guntur")
    data = WeatherService.get_weather(loc)
    return jsonify(data)

# ----------------- SMART IRRIGATION ASSISTANT -----------------
@app.route("/irrigation", methods=["GET", "POST"])
def irrigation():
    calculation = None
    form_data = {
        "crop": "chilli",
        "soil": "black_clay",
        "area": 2.5,
        "stage": "vegetative",
        "rainfall": 0.0,
        "method": "drip"
    }

    if request.method == "POST":
        form_data["crop"] = request.form.get("crop", "chilli")
        form_data["soil"] = request.form.get("soil", "black_clay")
        form_data["area"] = float(request.form.get("area", 2.5) or 2.5)
        form_data["stage"] = request.form.get("stage", "vegetative")
        form_data["rainfall"] = float(request.form.get("rainfall", 0) or 0)
        form_data["method"] = request.form.get("method", "drip")

        calculation = IrrigationService.calculate_irrigation(
            form_data["crop"],
            form_data["soil"],
            form_data["area"],
            form_data["stage"],
            form_data["rainfall"],
            form_data["method"]
        )

        # Log into database if user is logged in
        if "user_id" in session and calculation.get("success"):
            db = get_db()
            db.execute("""
                INSERT INTO irrigation_logs
                (user_id, crop_name, soil_type, field_area_acres, growth_stage, irrigation_method, recent_rainfall_mm,
                 water_req_liters, schedule_interval_days, water_saving_pct, tips_en, tips_te)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session["user_id"],
                calculation["crop_name_en"],
                calculation["soil_type_en"],
                form_data["area"],
                form_data["stage"],
                calculation["method_en"],
                form_data["rainfall"],
                calculation["daily_water_liters"],
                calculation["cycle_frequency_days"],
                calculation["water_savings_percent"],
                "\n".join(calculation["tips_en"]),
                "\n".join(calculation["tips_te"])
            ))
            db.commit()

    return render_template("irrigation/index.html", calculation=calculation, form=form_data)

# ----------------- CROP RECOMMENDATION SYSTEM -----------------
@app.route("/advisor", methods=["GET", "POST"])
def advisor():
    recommendations = None
    form_data = {
        "soil_type": "black",
        "season": "kharif",
        "water_avail": "medium",
        "ph": 7.0,
        "n_level": "medium",
        "p_level": "medium",
        "k_level": "high",
        "land_area": 3.0
    }

    if request.method == "POST":
        form_data["soil_type"] = request.form.get("soil_type", "black")
        form_data["season"] = request.form.get("season", "kharif")
        form_data["water_avail"] = request.form.get("water_avail", "medium")
        ph_input = request.form.get("ph")
        form_data["ph"] = float(ph_input) if ph_input else 7.0
        form_data["n_level"] = request.form.get("n_level", "medium")
        form_data["p_level"] = request.form.get("p_level", "medium")
        form_data["k_level"] = request.form.get("k_level", "high")
        area_input = request.form.get("land_area")
        form_data["land_area"] = float(area_input) if area_input else 1.0

        recommendations = CropAdvisorService.recommend_crops(
            soil_type=form_data["soil_type"],
            season=form_data["season"],
            water_avail=form_data["water_avail"],
            ph=form_data["ph"],
            n_val=form_data["n_level"],
            p_val=form_data["p_level"],
            k_val=form_data["k_level"],
            land_area=form_data["land_area"]
        )

    return render_template("advisor/index.html", recommendations=recommendations, form=form_data)

# ----------------- MARKET PRICE INTELLIGENCE -----------------
@app.route("/market")
def market():
    search = request.args.get("q", "").strip()
    selected_mandi = request.args.get("mandi", "all")

    prices = MarketService.get_all_prices(search, selected_mandi)
    mandis = MarketService.get_mandi_list()

    # Pre-fetch default trend for top crop
    top_crop = prices[0]["crop_name_en"] if prices else "Red Chilli"
    trends = MarketService.get_historical_trends(top_crop)

    return render_template("market/index.html", 
                           prices=prices, 
                           mandis=mandis, 
                           selected_mandi=selected_mandi, 
                           search=search,
                           trends=trends)

@app.route("/api/market-chart")
def api_market_chart():
    crop = request.args.get("crop", "Red Chilli")
    data = MarketService.get_historical_trends(crop)
    return jsonify(data)

# ----------------- FARMER-TO-BUYER MARKETPLACE -----------------
@app.route("/marketplace")
def marketplace():
    category = request.args.get("category", "all")
    district = request.args.get("district", "all")
    q = request.args.get("q", "").strip()

    db = get_db()
    cur = db.cursor()

    query = """
        SELECT ml.*, u.full_name as seller_name, u.phone as seller_phone
        FROM marketplace_listings ml
        JOIN users u ON ml.user_id = u.id
        WHERE ml.status = 'active'
    """
    params = []

    if category != "all":
        query += " AND ml.category = ?"
        params.append(category)
    if district != "all":
        query += " AND ml.district = ?"
        params.append(district)
    if q:
        query += " AND (ml.crop_name LIKE ? OR ml.variety LIKE ? OR ml.village LIKE ?)"
        term = f"%{q}%"
        params.extend([term, term, term])

    query += " ORDER BY ml.created_at DESC"
    cur.execute(query, params)
    listings = [dict(r) for r in cur.fetchall()]

    return render_template("marketplace/index.html", listings=listings, category=category, district=district, q=q)

@app.route("/marketplace/sell", methods=["GET", "POST"])
def marketplace_sell():
    if "user_id" not in session:
        flash("Please log in to list your agricultural produce for sale.", "warning")
        return redirect(url_for("login"))

    db = get_db()
    cur = db.cursor()

    if request.method == "POST":
        crop_name = request.form.get("crop_name", "").strip()
        variety = request.form.get("variety", "").strip()
        category = request.form.get("category", "Grains")
        quantity = float(request.form.get("quantity_quintals", 1.0) or 1.0)
        price = float(request.form.get("price_per_quintal", 1000.0) or 1000.0)
        is_negotiable = 1 if request.form.get("is_negotiable") else 0
        description = request.form.get("description", "").strip()
        village = request.form.get("village", "").strip()
        district = request.form.get("district", "").strip()
        delivery = request.form.get("delivery_options", "Farm Gate Pickup")
        contact_phone = request.form.get("contact_phone", "").strip()

        file = request.files.get("crop_photo")
        image_name = None
        if file and allowed_file(file.filename):
            ext = file.filename.rsplit(".", 1)[1].lower()
            image_name = f"produce_{uuid.uuid4().hex[:10]}.{ext}"
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], image_name))

        cur.execute("""
            INSERT INTO marketplace_listings 
            (user_id, crop_name, variety, category, quantity_quintals, price_per_quintal, is_negotiable,
             description, image_filename, village, district, delivery_options, contact_phone, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'active')
        """, (session["user_id"], crop_name, variety, category, quantity, price, is_negotiable,
              description, image_name, village, district, delivery, contact_phone))
        db.commit()

        flash("Your crop produce listing has been published in the marketplace! / మీ పంట మార్కెట్‌లో విజయవంతంగా జాబితా చేయబడింది!", "success")
        return redirect(url_for("marketplace"))

    # Fetch farmer default details for convenience
    cur.execute("SELECT * FROM farmer_profiles WHERE user_id = ?", (session["user_id"],))
    prof = cur.fetchone()
    return render_template("marketplace/create_listing.html", profile=prof)

@app.route("/marketplace/inquire", methods=["POST"])
def marketplace_inquire():
    listing_id = request.form.get("listing_id")
    buyer_name = request.form.get("buyer_name", "").strip()
    buyer_phone = request.form.get("buyer_phone", "").strip()
    offered_price = request.form.get("offered_price")
    quantity_requested = float(request.form.get("quantity_requested", 1.0) or 1.0)
    message = request.form.get("message", "").strip()

    if not listing_id or not buyer_name or not buyer_phone:
        flash("Please provide your contact name and mobile number.", "warning")
        return redirect(request.referrer or url_for("marketplace"))

    db = get_db()
    cur = db.cursor()
    cur.execute("""
        INSERT INTO marketplace_inquiries 
        (listing_id, buyer_id, buyer_name, buyer_phone, offered_price_per_quintal, quantity_requested, message, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'new')
    """, (listing_id, session.get("user_id"), buyer_name, buyer_phone, float(offered_price or 0.0), quantity_requested, message))

    # Also notify seller
    cur.execute("SELECT user_id, crop_name FROM marketplace_listings WHERE id = ?", (listing_id,))
    listing = cur.fetchone()
    if listing:
        cur.execute("""
            INSERT INTO notifications (user_id, title_en, title_te, message_en, message_te, category, action_url)
            VALUES (?, 'New Buyer Inquiry Received!', 'కొత్త కొనుగోలుదారు విచారణ!',
                    ?, ?, 'market', '/marketplace')
        """, (
            listing["user_id"],
            f"Buyer {buyer_name} ({buyer_phone}) requested {quantity_requested} quintals of {listing['crop_name']}.",
            f"కొనుగోలుదారు {buyer_name} ({buyer_phone}) {quantity_requested} క్వింటాళ్ల {listing['crop_name']} కోసం సంప్రదించారు."
        ))

    db.commit()
    flash("Inquiry sent directly to the farmer! They will contact you shortly. / విచారణ రైతుకు పంపబడింది!", "success")
    return redirect(url_for("marketplace"))

# ----------------- 14. ADDITIONAL UNIQUE INNOVATIVE FEATURES -----------------

# Feature 1: Farming Calendar & Reminders
@app.route("/calendar", methods=["GET", "POST"])
def calendar():
    if "user_id" not in session:
        flash("Please log in to manage your farming schedule and reminders.", "warning")
        return redirect(url_for("login"))

    db = get_db()
    cur = db.cursor()
    user_id = session["user_id"]

    if request.method == "POST":
        task_title_en = request.form.get("task_title", "").strip()
        crop_name = request.form.get("crop_name", "Paddy")
        task_type = request.form.get("task_type", "fertilizer")
        scheduled_date = request.form.get("scheduled_date", str(date.today()))
        priority = request.form.get("priority", "medium")
        notes = request.form.get("notes", "").strip()

        cur.execute("""
            INSERT INTO farming_calendar_tasks 
            (user_id, crop_name, task_title_en, task_title_te, task_type, scheduled_date, priority, status, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'pending', ?)
        """, (user_id, crop_name, task_title_en, task_title_en, task_type, scheduled_date, priority, notes))
        db.commit()
        flash("Farming activity reminder added to your calendar! / క్యాలెండర్‌లో కొత్త పని చేర్చబడింది!", "success")

    cur.execute("SELECT * FROM farming_calendar_tasks WHERE user_id = ? ORDER BY scheduled_date ASC", (user_id,))
    tasks = [dict(r) for r in cur.fetchall()]
    return render_template("calendar/index.html", tasks=tasks)

@app.route("/calendar/toggle/<int:task_id>")
def calendar_toggle(task_id):
    if "user_id" in session:
        db = get_db()
        db.execute("""
            UPDATE farming_calendar_tasks 
            SET status = CASE WHEN status = 'completed' THEN 'pending' ELSE 'completed' END
            WHERE id = ? AND user_id = ?
        """, (task_id, session["user_id"]))
        db.commit()
    return redirect(url_for("calendar"))

# Feature 2: Crop Expense & Profit Calculator
@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    calculation = None
    form = {
        "crop": "Paddy (Rice)",
        "acres": 2.0,
        "seed_cost": 2400,
        "fertilizer_cost": 7500,
        "pesticide_cost": 3800,
        "irrigation_cost": 2000,
        "machinery_cost": 6500,
        "labor_cost": 11000,
        "expected_yield_quintals": 50,
        "expected_price_per_quintal": 2350
    }

    if request.method == "POST":
        for k in form.keys():
            if k == "crop":
                form[k] = request.form.get(k, "Paddy")
            else:
                form[k] = float(request.form.get(k, 0) or 0)

        total_cost = (
            form["seed_cost"] + form["fertilizer_cost"] + form["pesticide_cost"] +
            form["irrigation_cost"] + form["machinery_cost"] + form["labor_cost"]
        )
        expected_revenue = form["expected_yield_quintals"] * form["expected_price_per_quintal"]
        net_profit = expected_revenue - total_cost
        cost_per_acre = round(total_cost / max(1.0, form["acres"]), 2)
        profit_per_acre = round(net_profit / max(1.0, form["acres"]), 2)
        roi_percentage = round((net_profit / max(1.0, total_cost)) * 100, 1)

        calculation = {
            "total_cost": total_cost,
            "expected_revenue": expected_revenue,
            "net_profit": net_profit,
            "cost_per_acre": cost_per_acre,
            "profit_per_acre": profit_per_acre,
            "roi_percentage": roi_percentage,
            "is_profitable": net_profit > 0
        }

    return render_template("calculator/index.html", form=form, calculation=calculation)

# Feature 3: Government Agricultural Schemes
@app.route("/schemes")
def schemes():
    return render_template("schemes/index.html")

# Feature 7: Soil Health Records Tracker
@app.route("/soil-health", methods=["GET", "POST"])
def soil_health():
    if "user_id" not in session:
        flash("Please log in to manage your soil health cards and test records.", "warning")
        return redirect(url_for("login"))

    db = get_db()
    cur = db.cursor()
    user_id = session["user_id"]

    if request.method == "POST":
        sample_id = request.form.get("sample_id", f"SHC-{uuid.uuid4().hex[:6].upper()}")
        test_date = request.form.get("test_date", str(date.today()))
        soil_type = request.form.get("soil_type", "Black Cotton Soil")
        ph = float(request.form.get("ph_level", 7.0) or 7.0)
        ec = float(request.form.get("electrical_conductivity", 0.4) or 0.4)
        oc = float(request.form.get("organic_carbon_pct", 0.5) or 0.5)
        n = float(request.form.get("nitrogen_kg_ha", 220) or 220)
        p = float(request.form.get("phosphorus_kg_ha", 25) or 25)
        k = float(request.form.get("potassium_kg_ha", 300) or 300)
        recommendations = request.form.get("recommendations", "Apply organic compost and green manuring.")

        cur.execute("""
            INSERT INTO soil_health_records 
            (user_id, test_date, sample_id, soil_type, ph_level, electrical_conductivity, organic_carbon_pct,
             nitrogen_kg_ha, phosphorus_kg_ha, potassium_kg_ha, status, recommendations_en, recommendations_te)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Tested', ?, ?)
        """, (user_id, test_date, sample_id, soil_type, ph, ec, oc, n, p, k, recommendations, recommendations))
        db.commit()
        flash("New Soil Health Record successfully saved! / భూసార పరీక్ష వివరాలు భద్రపరచబడ్డాయి!", "success")

    cur.execute("SELECT * FROM soil_health_records WHERE user_id = ? ORDER BY test_date DESC", (user_id,))
    records = [dict(r) for r in cur.fetchall()]
    return render_template("soil_health/index.html", records=records)

# Feature 8: Verified Agricultural Experts Directory
@app.route("/experts")
def experts():
    district = request.args.get("district", "all")
    db = get_db()
    cur = db.cursor()
    if district != "all":
        cur.execute("SELECT * FROM expert_contacts WHERE district = ? ORDER BY id ASC", (district,))
    else:
        cur.execute("SELECT * FROM expert_contacts ORDER BY id ASC")
    expert_list = [dict(r) for r in cur.fetchall()]
    return render_template("experts/index.html", experts=expert_list, selected_district=district)

# Feature 9: Multilingual Farming AI Chatbot (Krishi Mitra)
@app.route("/chatbot")
def chatbot():
    return render_template("chatbot/index.html")

@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json() or {}
    message = data.get("message", "")
    lang = session.get("lang", data.get("lang", "en"))
    response = KrishiChatbotService.get_response(message, lang)
    return jsonify(response)

# Feature 10: Crop-Loss Reporting Tool (PMFBY Insurance Assistance)
@app.route("/loss-report", methods=["GET", "POST"])
def loss_report():
    if "user_id" not in session:
        flash("Please log in to record and file a crop loss assessment.", "warning")
        return redirect(url_for("login"))

    db = get_db()
    cur = db.cursor()
    user_id = session["user_id"]

    if request.method == "POST":
        claim_id = f"PMFBY-{uuid.uuid4().hex[:8].upper()}"
        crop_name = request.form.get("crop_name", "").strip()
        survey_number = request.form.get("survey_number", "").strip()
        village = request.form.get("village", "").strip()
        district = request.form.get("district", "").strip()
        acreage_affected = float(request.form.get("acreage_affected", 1.0) or 1.0)
        cause_of_loss = request.form.get("cause_of_loss", "Excessive Rainfall / Floods")
        damage_date = request.form.get("damage_date", str(date.today()))
        loss_percentage = int(request.form.get("loss_percentage", 50) or 50)
        estimated_loss = float(request.form.get("estimated_loss", 25000) or 25000)
        remarks = request.form.get("remarks", "").strip()

        file = request.files.get("evidence_photo")
        img_name = None
        if file and allowed_file(file.filename):
            ext = file.filename.rsplit(".", 1)[1].lower()
            img_name = f"loss_{uuid.uuid4().hex[:10]}.{ext}"
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], img_name))

        cur.execute("""
            INSERT INTO crop_loss_reports 
            (user_id, claim_id, crop_name, survey_number, village, district, acreage_affected,
             cause_of_loss, damage_date, loss_percentage, estimated_financial_loss, evidence_image, remarks, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'submitted')
        """, (user_id, claim_id, crop_name, survey_number, village, district, acreage_affected,
              cause_of_loss, damage_date, loss_percentage, estimated_loss, img_name, remarks))
        db.commit()

        flash(f"Crop loss claim #{claim_id} recorded successfully! Keep this for PMFBY verification. / పంట నష్టం నమోదు చేయబడింది!", "success")
        return redirect(url_for("loss_report"))

    cur.execute("SELECT * FROM crop_loss_reports WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
    reports = [dict(r) for r in cur.fetchall()]
    return render_template("loss_report/index.html", reports=reports)

# Contact Us
@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
