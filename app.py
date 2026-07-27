import sqlite3
import pandas as pd
import streamlit as st
from agent import query_database

# Set page configurations with a wide, modern canvas layout
st.set_page_config(page_title="AI Data Analytics Suite", page_icon="📊", layout="wide")

# --- CUSTOM BEAUTIFUL STYLING ---
st.markdown("""
    <style>
    /* Styling headers and fonts */
    .main-title { font-size: 40px !important; font-weight: 700 !important; color: #1E293B; margin-bottom: 5px; }
    .subtitle { color: #64748B; font-size: 16px; margin-bottom: 25px; }
    
    /* Box card container containers */
    .card-container {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        padding: 24px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- DATABASE CRUD HELPERS ---
def get_dataframe():
    try:
        conn = sqlite3.connect("company.db")
        df = pd.read_sql_query("SELECT id as 'ID', name as 'Full Name', department as 'Department', salary as 'Annual Salary ($)' FROM employees", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error reading database: {e}")
        return pd.DataFrame()

def insert_employee(name, dept, salary):
    try:
        conn = sqlite3.connect("company.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO employees (name, department, salary) VALUES (?, ?, ?)", (name, dept, salary))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Failed to save record: {e}")
        return False

def delete_employee_by_id(emp_id):
    try:
        conn = sqlite3.connect("company.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM employees WHERE id = ?", (emp_id,))
        record = cursor.fetchone()
        if record is None:
            conn.close()
            return False, f"ID {emp_id} does not exist."
        cursor.execute("DELETE FROM employees WHERE id = ?", (emp_id,))
        conn.commit()
        conn.close()
        return True, f"Successfully removed {record[0]} (ID: {emp_id})."
    except Exception as e:
        return False, f"Database deletion error: {e}"

# Load current data frame state
df_employees = get_dataframe()

# --- HEADER SECTION ---
st.markdown("<div class='main-title'>📊 Autonomous Text-to-SQL Business Intelligence Suite</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Ask questions naturally, manage records cleanly, and visualize company insights seamlessly.</div>", unsafe_allow_html=True)

# --- DIVISION CHANNELS USING TABS ---
tab_analytics, tab_database_admin = st.tabs(["💡 AI Conversational Analytics", "⚙️ Database Administration"])

# ==========================================
# 1. AI CONVERSATIONAL & VISUAL ANALYTICS TAB
# ==========================================
with tab_analytics:
    # Top Row: AI Natural Language Processing Chat Input Box
    st.markdown("<div class='card-container'>", unsafe_allow_html=True)
    user_query = st.text_input(
        "💬 Ask a business question about employees (Press Enter to execute):", 
        placeholder="e.g., Who has the highest salary in the Engineering department?"
    )
    
    if user_query.strip() != "":
        with st.spinner("Analyzing schema and running queries..."):
            # Catching BOTH the conversational answer and the compiled SQL query string
            answer, sql_query = query_database(user_query)
            
            if "error" in answer.lower() or "failed" in answer.lower():
                st.error(answer)
            else:
                st.info(f"✨ **AI Response:** {answer}")
                
                # --- NEW FEATURE: Dropdown showing the exact backend SQL query ---
                with st.expander("🛠️ View Agent Technical Breakdown"):
                    st.caption("The AI Agent dynamically compiled and executed this SQL query against your database:")
                    st.code(sql_query, language="sql")
                    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Bottom Row: Financial Charts with Room to Stretch
    st.subheader("📈 Interactive Visual Insights")
    if not df_employees.empty:
        col_selector, col_spacer = st.columns([2, 3])
        with col_selector:
            chart_type = st.radio("Toggle Metric View:", ["Salary Breakdown by Employee", "Average Budget by Department"], horizontal=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if chart_type == "Salary Breakdown by Employee":
            st.bar_chart(data=df_employees, x="Full Name", y="Annual Salary ($)", color="#3B82F6")
        else:
            dept_stats = df_employees.groupby("Department")["Annual Salary ($)"].mean().reset_index()
            st.bar_chart(data=dept_stats, x="Department", y="Annual Salary ($)", color="#8B5CF6")
    else:
        st.info("Populate records to generate visualizations.")

# ==========================================
# 2. DATABASE RECORDS & CONTROLS ADMIN TAB
# ==========================================
with tab_database_admin:
    col_table, col_forms = st.columns([3, 2], gap="large")
    
    # Left Column: Beautiful Clean Interactive Table Grid
    with col_table:
        st.subheader("🗄️ Active Records Grid")
        if not df_employees.empty:
            st.dataframe(df_employees, hide_index=True, use_container_width=True, height=400)
            
            # Simple conversion backup utility built right in!
            csv_data = df_employees.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export Table as CSV",
                data=csv_data,
                file_name="employee_backup.csv",
                mime="text/csv"
            )
        else:
            st.warning("No data found in the current company schema.")
            
    # Right Column: Separated Add and Delete Data Fields
    with col_forms:
        # Block 1: Add New Data
        st.subheader("➕ Add New Record")
        with st.form("add_form", clear_on_submit=True):
            new_name = st.text_input("Full Name:")
            new_dept = st.selectbox("Department Assigned:", ["Engineering", "Marketing", "Sales", "HR", "Finance"])
            new_salary = st.number_input("Annual Salary Base ($):", min_value=10000, max_value=500000, step=5000)
            if st.form_submit_button("Save Record", use_container_width=True):
                if new_name.strip() == "":
                    st.error("Name field cannot be left blank.")
                elif insert_employee(new_name, new_dept, new_salary):
                    st.success(f"Added {new_name} successfully!")
                    st.rerun()
                    
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Block 2: Remove Data
        st.subheader("🗑️ Remove Record")
        delete_id = st.number_input("Enter target Row ID:", min_value=1, step=1)
        if st.button("Delete Record From System", type="primary", use_container_width=True):
            success, message = delete_employee_by_id(delete_id)
            if success:
                st.success(message)
                st.rerun()
            else:
                st.error(message)
