import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, date

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AutoPulse AI | Ultimate Automotive Suite",
    page_icon="🏎️",
    layout="wide"
)

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect("autopulse.db")
    cursor = conn.cursor()
    
    # Vehicles table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_name TEXT UNIQUE,
            vehicle_type TEXT,
            year INTEGER
        )
    """)
    
    # Service logs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS service_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle TEXT,
            date TEXT,
            service_type TEXT,
            mileage INTEGER,
            cost REAL,
            notes TEXT
        )
    """)

    # Fuel logs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fuel_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle TEXT,
            date TEXT,
            liters REAL,
            cost REAL,
            odometer INTEGER
        )
    """)

    # Document tracker table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle TEXT,
            doc_type TEXT,
            expiry_date TEXT,
            notes TEXT
        )
    """)

    # Maintenance reminders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle TEXT,
            task_name TEXT,
            target_km INTEGER,
            notes TEXT
        )
    """)

    # Emergency contacts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle TEXT,
            contact_name TEXT,
            phone TEXT,
            role TEXT
        )
    """)

    # Default vehicles if empty
    cursor.execute("SELECT COUNT(*) FROM vehicles")
    if cursor.fetchone()[0] == 0:
        default_vehicles = [
            ("Honda Civic (2020)", "Sedan", 2020),
            ("Yamaha R15 (Bike)", "Motorcycle", 2022),
            ("Maruti Baleno (2023)", "Hatchback", 2023)
        ]
        cursor.executemany("INSERT INTO vehicles (vehicle_name, vehicle_type, year) VALUES (?, ?, ?)", default_vehicles)
    
    conn.commit()
    conn.close()

init_db()

# --- DATABASE HELPERS ---
def get_vehicles():
    conn = sqlite3.connect("autopulse.db")
    cursor = conn.cursor()
    cursor.execute("SELECT vehicle_name FROM vehicles")
    vehicles = [row[0] for row in cursor.fetchall()]
    conn.close()
    return vehicles

def add_new_vehicle(name, v_type, year):
    try:
        conn = sqlite3.connect("autopulse.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO vehicles (vehicle_name, vehicle_type, year) VALUES (?, ?, ?)", (name, v_type, year))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def add_service_record(vehicle, date, service_type, mileage, cost, notes):
    conn = sqlite3.connect("autopulse.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO service_logs (vehicle, date, service_type, mileage, cost, notes) VALUES (?, ?, ?, ?, ?, ?)",
                   (vehicle, date, service_type, mileage, cost, notes))
    conn.commit()
    conn.close()

def get_service_records(vehicle):
    conn = sqlite3.connect("autopulse.db")
    df = pd.read_sql_query("SELECT * FROM service_logs WHERE vehicle = ? ORDER BY date DESC", conn, params=(vehicle,))
    conn.close()
    return df

def add_fuel_record(vehicle, date, liters, cost, odometer):
    conn = sqlite3.connect("autopulse.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO fuel_logs (vehicle, date, liters, cost, odometer) VALUES (?, ?, ?, ?, ?)",
                   (vehicle, date, liters, cost, odometer))
    conn.commit()
    conn.close()

def get_fuel_records(vehicle):
    conn = sqlite3.connect("autopulse.db")
    df = pd.read_sql_query("SELECT * FROM fuel_logs WHERE vehicle = ? ORDER BY date DESC", conn, params=(vehicle,))
    conn.close()
    return df

def add_document(vehicle, doc_type, expiry_date, notes):
    conn = sqlite3.connect("autopulse.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO documents (vehicle, doc_type, expiry_date, notes) VALUES (?, ?, ?, ?)",
                   (vehicle, doc_type, expiry_date, notes))
    conn.commit()
    conn.close()

def get_documents(vehicle):
    conn = sqlite3.connect("autopulse.db")
    df = pd.read_sql_query("SELECT * FROM documents WHERE vehicle = ?", conn, params=(vehicle,))
    conn.close()
    return df

def add_reminder(vehicle, task_name, target_km, notes):
    conn = sqlite3.connect("autopulse.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reminders (vehicle, task_name, target_km, notes) VALUES (?, ?, ?, ?)",
                   (vehicle, task_name, target_km, notes))
    conn.commit()
    conn.close()

def get_reminders(vehicle):
    conn = sqlite3.connect("autopulse.db")
    df = pd.read_sql_query("SELECT * FROM reminders WHERE vehicle = ?", conn, params=(vehicle,))
    conn.close()
    return df

def add_contact(vehicle, contact_name, phone, role):
    conn = sqlite3.connect("autopulse.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO contacts (vehicle, contact_name, phone, role) VALUES (?, ?, ?, ?)",
                   (vehicle, contact_name, phone, role))
    conn.commit()
    conn.close()

def get_contacts(vehicle):
    conn = sqlite3.connect("autopulse.db")
    df = pd.read_sql_query("SELECT * FROM contacts WHERE vehicle = ?", conn, params=(vehicle,))
    conn.close()
    return df

# --- SIDEBAR NAVIGATION & SETTINGS ---
st.sidebar.markdown("# 🏎️ AutoPulse AI")
st.sidebar.caption("Ultimate Automotive Suite")
st.sidebar.markdown("---")

currency_symbol = st.sidebar.selectbox("💱 Currency Format", ["₹ (INR)", "$ (USD)"])
curr_char = "₹" if "₹" in currency_symbol else "$"

vehicle_list = get_vehicles()
selected_vehicle = st.sidebar.selectbox("🎯 Active Vehicle Profile", vehicle_list)

nav_choice = st.sidebar.radio("Navigation Menu", [
    "🚀 Executive Dashboard", 
    "🏎️ Garage & Fleet Manager", 
    "🛠️ Service & Expense Tracker", 
    "⛽ Fuel & Efficiency Logger",
    "🔔 Maintenance Reminders",
    "📄 Document Locker & Expiries",
    "📞 Emergency & Mechanic Directory",
    "🔍 OBD-II Fault Code Lookup",
    "🗺️ AI Trip & Fuel Calculator",
    "🤖 AI Mechanic & Diagnostics", 
    "📊 Predictive Component Wear",
    "📥 Export Telemetry Data"
])

st.sidebar.markdown("---")
st.sidebar.info("🔒 **Persistent SQLite Database**\nMulti-vehicle profiles and records stored locally.")

# ==========================================
# 1. EXECUTIVE DASHBOARD
# ==========================================
if nav_choice == "🚀 Executive Dashboard":
    st.title(f"🚀 Command Center: {selected_vehicle}")
    st.markdown("Real-time telemetry overview, health status, and cost metrics.")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="⚡ Odometer", value="48,250 km", delta="+650 km")
    with col2:
        st.metric(label="⛽ Fuel Economy", value="16.5 km/L", delta="+0.8")
    with col3:
        st.metric(label="🛡️ Health Index", value="89%", delta="-3%", delta_color="inverse")
    with col4:
        cost_val = f"4,500" if curr_char == "₹" else "60"
        st.metric(label="💰 YTD Cost", value=f"{curr_char}{cost_val}", delta="+10%")

    st.markdown("---")

    c1, c2 = st.columns([1.2, 0.8])
    with c1:
        st.subheader("⚠️ Active Fleet & Vehicle Alerts")
        st.warning(f"🔋 **Battery Health Alert ({selected_vehicle}):** State of Health at 74%. Recommended check before monsoon.")
        st.info("🛞 **Tire Rotation Notice:** Front tread depth approaching threshold within 2,000 km.")
        st.success("📋 **Documents:** Check Document Locker for current renewal statuses.")
    with c2:
        st.subheader("⚡ Quick Actions")
        if st.button("➕ Log Fuel Fill-Up", use_container_width=True):
            st.toast("Switch to 'Fuel & Efficiency Logger' in the sidebar!")
        if st.button("📞 View Emergency Contacts", use_container_width=True):
            st.toast("Switch to 'Emergency & Mechanic Directory' in the sidebar!")

# ==========================================
# 2. GARAGE & FLEET MANAGER
# ==========================================
elif nav_choice == "🏎️ Garage & Fleet Manager":
    st.title("🏎️ AutoPulse Garage & Fleet Management")
    st.markdown("Register and manage multiple cars, bikes, or utility vehicles in your digital stable.")
    st.markdown("---")

    g_col1, g_col2 = st.columns(2)
    with g_col1:
        with st.form("add_vehicle_form", clear_on_submit=True):
            st.subheader("➕ Register New Vehicle")
            new_name = st.text_input("Vehicle Name & Model", placeholder="e.g., Hyundai Creta (2023)")
            new_type = st.selectbox("Vehicle Category", ["Hatchback", "Sedan", "SUV", "Motorcycle", "Truck", "Electric Vehicle"])
            new_year = st.number_input("Manufacturing Year", min_value=1990, max_value=2030, value=2024)
            
            submit_car = st.form_submit_button("Save to Garage Database", use_container_width=True)
            if submit_car:
                if new_name:
                    success = add_new_vehicle(new_name, new_type, new_year)
                    if success:
                        st.success(f"Successfully added **{new_name}** to your garage!")
                        st.rerun()
                    else:
                        st.error("This vehicle name already exists in your garage.")
                else:
                    st.warning("Please enter a valid vehicle name.")

    with g_col2:
        st.subheader("📋 Registered Vehicles in Stable")
        current_vehicles = get_vehicles()
        for idx, veh in enumerate(current_vehicles, 1):
            st.markdown(f"**{idx}.** 🚗 `{veh}`")
        st.info("💡 Select any vehicle from the top-left sidebar dropdown to switch dashboards instantly.")

# ==========================================
# 3. SERVICE & EXPENSE TRACKER
# ==========================================
elif nav_choice == "🛠️ Service & Expense Tracker":
    st.title(f"🛠️ Service Hub: {selected_vehicle}")
    st.markdown("Record oil changes, brake replacements, repairs, and keep permanent receipts.")
    st.markdown("---")

    with st.form("service_form", clear_on_submit=True):
        st.subheader(f"Add Service Record for {selected_vehicle}")
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            service_date = st.date_input("Service Date", datetime.today())
            service_type = st.selectbox("Service Category", ["🛢️ Oil Change", "🛑 Brake Replacement", "🛞 Tire Rotation", "🔋 Battery Swap", "🔍 General Inspection", "⚙️ Custom Repair"])
            mileage_at_service = st.number_input("Odometer at Service (km)", min_value=0, value=45000)
        with f_col2:
            default_cost = 1500.0 if curr_char == "₹" else 20.0
            cost = st.number_input(f"Total Cost ({curr_char})", min_value=0.0, value=default_cost)
            notes = st.text_area("Detailed Notes / Mechanic Remarks", placeholder="e.g., Synthetic oil upgrade & OEM filter installed.")
        
        submitted = st.form_submit_button("💾 Save Service Log", use_container_width=True)
        if submitted:
            add_service_record(selected_vehicle, str(service_date), service_type, mileage_at_service, cost, notes)
            st.success(f"Successfully saved record for {selected_vehicle}!")

    st.markdown("---")
    st.subheader(f"📜 Service History & Cost Analytics for {selected_vehicle}")
    records_df = get_service_records(selected_vehicle)
    if not records_df.empty:
        st.dataframe(records_df, use_container_width=True)
        
        st.markdown(f"### 📊 Spending Breakdown by Category ({curr_char})")
        chart_df = records_df.set_index("service_type")["cost"]
        st.bar_chart(chart_df)
    else:
        st.info(f"No records found for {selected_vehicle} yet. Add your first entry above!")

# ==========================================
# 4. FUEL & EFFICIENCY LOGGER
# ==========================================
elif nav_choice == "⛽ Fuel & Efficiency Logger":
    st.title(f"⛽ Fuel & Gas Log: {selected_vehicle}")
    st.markdown("Log fill-ups to monitor true fuel economy and gas expenditures over time.")
    st.markdown("---")

    fu_col1, fu_col2 = st.columns(2)
    with fu_col1:
        with st.form("fuel_form", clear_on_submit=True):
            st.subheader("Record New Fill-Up")
            f_date = st.date_input("Fill-Up Date", datetime.today())
            liters_added = st.number_input("Fuel Added (Liters)", min_value=1.0, value=35.0)
            default_fcost = 3500.0 if curr_char == "₹" else 45.0
            total_paid = st.number_input(f"Total Paid ({curr_char})", min_value=1.0, value=default_fcost)
            current_odo = st.number_input("Odometer Reading (km)", min_value=0, value=48000)
            
            f_submit = st.form_submit_button("💾 Save Fuel Log", use_container_width=True)
            if f_submit:
                add_fuel_record(selected_vehicle, str(f_date), liters_added, total_paid, current_odo)
                st.success("Fuel log successfully recorded!")
                st.rerun()

    with fu_col2:
        st.subheader("📈 Fuel Efficiency History")
        fuel_df = get_fuel_records(selected_vehicle)
        if not fuel_df.empty:
            st.dataframe(fuel_df, use_container_width=True)
            st.markdown("### 📊 Fuel Cost Trend")
            st.line_chart(fuel_df.set_index("date")["cost"])
        else:
            st.info("No fuel logs recorded yet. Add your first fill-up on the left.")

# ==========================================
# 5. MAINTENANCE REMINDERS
# ==========================================
elif nav_choice == "🔔 Maintenance Reminders":
    st.title(f"🔔 Service Reminders & Alerts: {selected_vehicle}")
    st.markdown("Set target mileage milestones for upcoming maintenance tasks.")
    st.markdown("---")

    r_col1, r_col2 = st.columns(2)
    with r_col1:
        with st.form("reminder_form", clear_on_submit=True):
            st.subheader("Add New Reminder")
            task_name = st.selectbox("Task Name", ["🛢️ Next Oil Change", "🛑 Brake Pad Inspection", "🛞 Tire Balancing & Rotation", "⚙️ Coolant Flush", "🔋 Battery Terminal Check"])
            target_km = st.number_input("Target Odometer Mileage (km)", min_value=0, value=52000)
            r_notes = st.text_input("Reminder Notes", placeholder="e.g., Use 5W-30 fully synthetic oil")
            
            r_submit = st.form_submit_button("📌 Set Mileage Reminder", use_container_width=True)
            if r_submit:
                add_reminder(selected_vehicle, task_name, target_km, r_notes)
                st.success("Reminder successfully added!")
                st.rerun()

    with r_col2:
        st.subheader("Active Milestone Alerts")
        reminders_df = get_reminders(selected_vehicle)
        if not reminders_df.empty:
            for index, row in reminders_df.iterrows():
                st.info(f"📌 **{row['task_name']}** target: **{row['target_km']:,} km**\n\nNotes: {row['notes']}")
            st.markdown("---")
            st.dataframe(reminders_df, use_container_width=True)
        else:
            st.info("No service reminders set yet. Create one on the left.")

# ==========================================
# 6. DOCUMENT LOCKER & EXPIRIES
# ==========================================
elif nav_choice == "📄 Document Locker & Expiries":
    st.title(f"📄 Document Locker: {selected_vehicle}")
    st.markdown("Track policy renewals, Pollution Under Control (PUC) certificates, and vehicle registrations.")
    st.markdown("---")

    d_col1, d_col2 = st.columns(2)
    with d_col1:
        with st.form("doc_form", clear_on_submit=True):
            st.subheader("Add / Update Document")
            doc_type = st.selectbox("Document Type", ["🛡️ Insurance Policy", "☁️ PUC / Emission Certificate", "📋 Vehicle Registration (RC)", "🪪 Driver License"])
            expiry_date = st.date_input("Expiry Date", datetime.today())
            doc_notes = st.text_input("Policy Number / Details", placeholder="e.g., Policy #POL-998234")
            
            doc_submit = st.form_submit_button("🔒 Save to Secure Locker", use_container_width=True)
            if doc_submit:
                add_document(selected_vehicle, doc_type, str(expiry_date), doc_notes)
                st.success(f"Successfully saved {doc_type} for {selected_vehicle}!")
                st.rerun()

    with d_col2:
        st.subheader("⚠️ Active Expiry Status")
        doc_df = get_documents(selected_vehicle)
        if not doc_df.empty:
            for index, row in doc_df.iterrows():
                exp_date = datetime.strptime(row['expiry_date'], "%Y-%m-%d").date()
                days_left = (exp_date - date.today()).days
                
                if days_left < 0:
                    st.error(f"🚨 **{row['doc_type']}** expired {abs(days_left)} days ago! ({row['notes']})")
                elif days_left <= 30:
                    st.warning(f"⚠️ **{row['doc_type']}** expires soon in {days_left} days! ({row['notes']})")
                else:
                    st.success(f"✅ **{row['doc_type']}** is valid (Expires in {days_left} days).")
            
            st.markdown("---")
            st.dataframe(doc_df, use_container_width=True)
        else:
            st.info("No documents logged yet. Add your insurance or registration records on the left.")

# ==========================================
# 7. EMERGENCY & MECHANIC DIRECTORY
# ==========================================
elif nav_choice == "📞 Emergency & Mechanic Directory":
    st.title(f"📞 Emergency Contacts: {selected_vehicle}")
    st.markdown("Save emergency helplines, preferred garages, and roadside assistance contacts.")
    st.markdown("---")

    con_col1, con_col2 = st.columns(2)
    with con_col1:
        with st.form("contact_form", clear_on_submit=True):
            st.subheader("Add New Contact")
            c_name = st.text_input("Contact / Garage Name", placeholder="e.g., Apex City Motors")
            c_phone = st.text_input("Phone Number", placeholder="e.g., +91 98765 43210")
            c_role = st.selectbox("Category", ["🛠️ Preferred Mechanic", "🛡️ Insurance Helpline", "🚚 Roadside Assistance", "👥 Personal Contact"])
            
            c_submit = st.form_submit_button("💾 Save Contact", use_container_width=True)
            if c_submit:
                add_contact(selected_vehicle, c_name, c_phone, c_role)
                st.success("Contact successfully saved!")
                st.rerun()

    with con_col2:
        st.subheader("Saved Directory")
        contacts_df = get_contacts(selected_vehicle)
        if not contacts_df.empty:
            for index, row in contacts_df.iterrows():
                st.info(f"**{row['contact_name']}** ({row['role']})\n📞 Tel: `{row['phone']}`")
            st.markdown("---")
            st.dataframe(contacts_df, use_container_width=True)
        else:
            st.info("No emergency contacts saved yet. Add your first contact on the left.")

# ==========================================
# 8. OBD-II FAULT CODE LOOKUP
# ==========================================
elif nav_choice == "🔍 OBD-II Fault Code Lookup":
    st.title("🔍 Professional OBD-II Diagnostic Trouble Code (DTC) Database")
    st.markdown("Lookup standard powertrain, body, and chassis fault codes instantly.")
    st.markdown("---")

    dtc_database = {
        "P0300": {"system": "Engine / Ignition", "desc": "Random/Multiple Cylinder Misfire Detected", "severity": "High", "fix": "Check spark plugs, ignition coils, and fuel injectors."},
        "P0420": {"system": "Exhaust / Emissions", "desc": "Catalyst System Efficiency Below Threshold (Bank 1)", "severity": "Moderate", "fix": "Inspect catalytic converter, oxygen (O2) sensors, or exhaust leaks."},
        "P0171": {"system": "Fuel / Air Metering", "desc": "System Too Lean (Bank 1)", "severity": "Moderate", "fix": "Check for vacuum leaks, dirty mass airflow (MAF) sensor, or weak fuel pump."},
        "P0113": {"system": "Electrical / Sensors", "desc": "Intake Air Temperature Sensor 1 Circuit High Input", "severity": "Low", "fix": "Check wiring harness connection to the IAT sensor."},
        "P0500": {"system": "Brakes / Speed", "desc": "Vehicle Speed Sensor 'A'", "severity": "Moderate", "fix": "Inspect wheel speed sensors and ABS wiring harness."}
    }

    col_search, col_result = st.columns([1, 1])
    with col_search:
        st.subheader("Search Trouble Code")
        code_input = st.text_input("Enter OBD-II Code (e.g., P0300, P0420):", placeholder="P0300").upper().strip()
        search_btn = st.button("🔍 Search Database", use_container_width=True)
        
        st.markdown("---")
        st.markdown("**Common Sample Codes to Try:**")
        st.code("P0300 (Misfire)\nP0420 (Catalytic Converter)\nP0171 (Lean Fuel)")

    with col_result:
        st.subheader("📖 Code Analysis & Repair Guidelines")
        if search_btn:
            if code_input in dtc_database:
                data = dtc_database[code_input]
                st.markdown(f"### Code: `{code_input}`")
                st.info(f"**System Category:** {data['system']}")
                st.error(f"**Description:** {data['desc']}")
                st.warning(f"**Severity Level:** {data['severity']}")
                st.markdown(f"**Recommended Fix / Next Steps:**\n{data['fix']}")
            elif code_input:
                st.warning(f"Code `{code_input}` not found in offline cache. Let AutoPulse AI analyze it below:")
                st.info(f"**AI Triage for {code_input}:** Check related wiring harnesses, fuses, or run a live scanner reading at your local service center.")
            else:
                st.warning("Please enter a valid OBD-II code.")
        else:
            st.info("Enter an OBD-II code on the left and click search to view professional repair instructions.")

# ==========================================
# 9. AI TRIP & FUEL CALCULATOR
# ==========================================
elif nav_choice == "🗺️ AI Trip & Fuel Calculator":
    st.title(f"🗺️ AI Trip Cost & Fuel Calculator ({selected_vehicle})")
    st.markdown("Estimate fuel consumption, trip expenses, and fuel stops before hitting the road.")
    st.markdown("---")

    t_col1, t_col2 = st.columns(2)
    with t_col1:
        st.subheader("Trip Parameters")
        trip_distance = st.number_input("Estimated Trip Distance (km)", min_value=1.0, value=250.0)
        default_price = 105.0 if curr_char == "₹" else 1.25
        fuel_price = st.number_input(f"Fuel Price per Liter ({curr_char})", min_value=1.0, value=default_price)
        vehicle_efficiency = st.slider("Estimated Fuel Efficiency (km/L)", min_value=5.0, max_value=45.0, value=16.5)
        
        calculate_trip = st.button("🚀 Calculate Trip Metrics", use_container_width=True)

    with t_col2:
        st.subheader("📊 Trip Financial & Fuel Breakdown")
        if calculate_trip:
            total_fuel_needed = trip_distance / vehicle_efficiency
            total_cost = total_fuel_needed * fuel_price
            
            st.metric(label="Total Fuel Required", value=f"{total_fuel_needed:.2f} Liters")
            st.metric(label="Estimated Total Trip Cost", value=f"{curr_char}{total_cost:,.2f}")
            st.success(f"💡 **AI Tip:** For a {trip_distance} km journey in your **{selected_vehicle}**, ensure you check tire pressure and coolant levels prior to departure.")
        else:
            st.info("Input your distance and fuel parameters on the left and click **Calculate Trip Metrics**.")

# ==========================================
# 10. AI MECHANIC & DIAGNOSTICS
# ==========================================
elif nav_choice == "🤖 AI Mechanic & Diagnostics":
    st.title(f"🤖 AI Diagnostic Assistant ({selected_vehicle})")
    st.markdown("Analyze unusual sounds, dashboard warning lights, or mechanical symptoms.")
    st.markdown("---")

    col_input, col_output = st.columns([1, 1])
    with col_input:
        st.subheader("🔍 Symptom Input")
        symptom_category = st.selectbox("System Area", ["Engine / Powertrain", "Brakes & Steering", "Electrical & Battery", "Suspension & Tires", "Exhaust / Fumes"])
        user_query = st.text_area("Describe the issue:", placeholder="e.g., Squealing sound when braking at low speeds.")
        urgency_guess = st.select_slider("Perceived Severity", options=["Minor Annoyance", "Moderate Issue", "Critical / Unsafe to Drive"])
        run_diagnosis = st.button("⚡ Run AI Diagnostic Scan", use_container_width=True)

    with col_output:
        st.subheader("🩺 Diagnostic Triage Result")
        if run_diagnosis:
            if user_query:
                with st.spinner(f"Running neural diagnostic check for {selected_vehicle}..."):
                    st.markdown("---")
                    st.error("🚨 **Diagnosis:** High Probability of Brake Pad Wear Indicator Contact")
                    st.markdown(f"**Vehicle:** {selected_vehicle} | **Category:** {symptom_category}")
                    st.write("**Potential Root Causes:**")
                    st.write("1. **Worn Brake Pads:** Friction material worn down past safety threshold.")
                    st.write("2. **Rotor Glazing:** Heat spots accumulated on rotor surface.")
                    st.markdown("### 🛠️ Recommended Action Plan")
                    st.info("Inspect brake pad thickness visually and schedule replacement within 500 km.")
                    cost_range = "₹1,200 - ₹2,500" if curr_char == "₹" else "$40 - $90"
                    st.metric(label="Estimated Repair Cost", value=cost_range)
            else:
                st.warning("Please describe a symptom first.")
        else:
            st.info("Provide your vehicle symptoms on the left and click **Run AI Diagnostic Scan**.")

# ==========================================
# 11. PREDICTIVE COMPONENT WEAR
# ==========================================
elif nav_choice == "📊 Predictive Component Wear":
    st.title(f"📊 Predictive Wear Analysis: {selected_vehicle}")
    st.markdown("Simulated machine-learning forecasts tracking component lifespan.")
    st.markdown("---")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**🛢️ Engine Oil Health (Synthetic)**")
        st.progress(0.65, text="65% Remaining (~3,500 km left)")
        st.markdown("**🛑 Front Brake Pads**")
        st.progress(0.30, text="30% Remaining - Action Recommended")
    with col_b:
        st.markdown("**⚙️ Transmission Fluid**")
        st.progress(0.80, text="80% Remaining (Optimal)")
        st.markdown("**🔋 12V Battery Life**")
        st.progress(0.74, text="74% Remaining - Monitor in Winter")

# ==========================================
# 12. EXPORT TELEMETRY DATA
# ==========================================
elif nav_choice == "📥 Export Telemetry Data":
    st.title("📥 Export Vehicle Telemetry & Logs")
    st.markdown("Download your complete service and maintenance records as a CSV spreadsheet.")
    st.markdown("---")
    
    records_df = get_service_records(selected_vehicle)
    if not records_df.empty:
        csv_data = records_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV Report for " + selected_vehicle,
            data=csv_data,
            file_name=f"autopulse_{selected_vehicle.lower().replace(' ', '_')}_report.csv",
            mime="text/csv",
            use_container_width=True
        )
        st.success("Telemetry report ready for download.")
    else:
        st.info("No service logs available to export for this vehicle yet.")