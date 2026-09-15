import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json

# ==========================================
# --- STREAMLIT PREMIUM ROYAL CSS ---
# ==========================================
custom_css = """
<style>
    /* Import Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Lato:wght@300;400;700&display=swap');

    /* Main App Background */
    .stApp {
        background-color: #0A192F;
        color: #E0E0E0;
        font-family: 'Lato', sans-serif;
    }

    /* Headers */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: #C5A059 !important;
    }
    
    /* Subheaders & Text */
    p, span, label {
        font-family: 'Lato', sans-serif !important;
        color: #E0E0E0 !important;
    }

    /* Input Fields */
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div, .stNumberInput > div > div {
        background-color: #112240 !important;
        border: 1px solid rgba(197, 160, 89, 0.4) !important;
        border-radius: 8px !important;
        color: #FDFBF7 !important;
    }

    /* Input Text Color */
    input, div[data-baseweb="select"] {
        color: #FDFBF7 !important;
    }

    /* Primary Buttons (Teal to Gold) */
    .stButton > button {
        background-color: #2A9D8F !important;
        color: white !important;
        border: 1px solid #2A9D8F !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 10px rgba(42, 157, 143, 0.2);
    }
    .stButton > button:hover {
        background-color: #C5A059 !important;
        border: 1px solid #C5A059 !important;
        color: #0A192F !important;
        box-shadow: 0 6px 15px rgba(197, 160, 89, 0.4);
    }

    /* Tabs Design */
    button[data-baseweb="tab"] {
        background-color: transparent !important;
        color: #8892B0 !important;
        font-weight: bold;
        font-family: 'Lato', sans-serif !important;
        font-size: 16px !important;
    }
    button[aria-selected="true"] {
        color: #C5A059 !important;
        border-bottom: 3px solid #C5A059 !important;
    }

    /* Info/Success/Warning Boxes */
    .stAlert {
        background: linear-gradient(135deg, rgba(42, 157, 143, 0.1), rgba(197, 160, 89, 0.05)) !important;
        border-left: 4px solid #2A9D8F !important;
        color: #E0E0E0 !important;
    }

    /* Horizontal Rule */
    hr {
        border-color: rgba(197, 160, 89, 0.3) !important;
        margin-top: 25px !important;
        margin-bottom: 25px !important;
    }
    
    /* Checkbox and Radio text */
    .stRadio div[role="radiogroup"] label p, .stCheckbox label p {
        color: #E0E0E0 !important;
        font-size: 16px !important;
    }
    
    /* Result Box in Tab 5 */
    .custom-result-box {
        background-color: #112240;
        border: 1px solid rgba(42, 157, 143, 0.5);
        border-radius: 6px;
        padding: 7px 12px;
        color: #C5A059;
        font-size: 15px;
        height: 38px;
        display: flex;
        align-items: center;
        font-weight: bold;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)


# ==========================================
# --- STREAMLIT SAFE MEMORY HACK ---
# ==========================================
def save_safe_state():
    for key in list(st.session_state.keys()):
        if not key.startswith("SAFE_") and key != "page" and not key.startswith("btn_"):
            st.session_state["SAFE_" + key] = st.session_state[key]

for key in list(st.session_state.keys()):
    if key.startswith("SAFE_"):
        widget_key = key.replace("SAFE_", "")
        if widget_key not in st.session_state:
            try:
                st.session_state[widget_key] = st.session_state[key]
            except Exception:
                pass 
# ==========================================


# --- Page Setup & Session State Initialization ---
st.title("Welcome to FINXHORIZON")
st.write("---")

if 'page' not in st.session_state:
    st.session_state.page = 'welcome'


# ==========================================
# PAGE 1: Welcome & Basic Info Form
# ==========================================

if st.session_state.page == 'welcome':
    st.subheader("Hello, may I know your full name?")

    name = st.text_input("NAME:", key='name')

    phone = st.text_input("Phone Number:", key='phone')
    email = st.text_input("Email Address:", key='email')

    gender = st.radio(
        "Kindly select your gender",
        ('MALE', 'FEMALE', 'OTHER'), 
        index=None,
        key='gender'
    )

    if name and gender:
        first_name = name.split()[0]
        if gender == "MALE":
            st.success(f"Thank You {first_name} Sir, it is a pleasure to have you. Kindly fill the form to proceed further.")
        elif gender == "FEMALE":
            st.success(f"Thank You {first_name} Mam, it is a pleasure to have you. Kindly fill the form to proceed further.")
        else:
            st.success(f"Thank You {first_name}, it is a pleasure to have you. Kindly fill the form to proceed further.")

    if st.button("Go to Form"):
        if name and gender and phone and email:
            try:
                scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
                secret_dict = json.loads(st.secrets["google_sheets_secret"])
                creds = Credentials.from_service_account_info(secret_dict, scopes=scope)
                client = gspread.authorize(creds)
                
                sheet = client.open("Client_Test").sheet1
                
                sheet.append_row([name, gender, phone, email])
                
                save_safe_state()
                
                st.session_state.page = 'main_form'
                st.rerun()
                
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Doya kore sokol field thikvabe puron korun!")

# ==========================================
# PAGE 2: Main Form (Personal Information)
# ==========================================

elif st.session_state.page == 'main_form':
    st.subheader("Personal Information")
    
    st.info(f"**Name:** {st.session_state.get('name')}  \n**Phone:** {st.session_state.get('phone')}  \n**Email:** {st.session_state.get('email')}  \n**Gender:** {st.session_state.get('gender')}")
    
    def switch_tab(tab):
        st.session_state.current_tab = tab

    def on_tab_change():
        pass

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        [
            "Personal Info", 
            "Spouse Details",
            "Child Details",
            "Dependent Member",
            "Future Expenses Projection", 
            "Final Goals"
        ], 
        on_change=on_tab_change, 
        key="current_tab"
    )

    # 1st ট্যাব এর ডিজাইন
    with tab1:
        st.subheader("Personal Information")
        
        age = st.selectbox(
            "May I know what age are you?", 
            [None] + list(range(18, 101)), 
            format_func=lambda x: "Select age" if x is None else str(x),
            key="p_age"
        )
    
        profession = st.radio(
            "Kindly select your profession:",
            ('Business', 'Service(Govt. / Pvt.)', 'Self Employed', 'Non Earning member'),
            index=None,
            key="p_prof"
        )
    
        if profession in ["Business", "Self Employed", "Service(Govt. / Pvt.)"]:
            income = st.number_input("What is your approximate monthly income?", min_value=0, step=1000, key="p_inc")
        else:
            income = 0
    
        expenses = st.number_input("What is your approximate monthly household expenses?", min_value=0, step=1000, key="p_exp")
    
        married = st.radio(
            "Are you married?",
            ('YES', 'NO'),
            index=None,
            key="p_married"
        )

        is_valid = bool((age is not None) and (profession is not None) and (married is not None))
        
        if not is_valid:
            st.warning("⚠️ Please fill in your age, profession, and marital status to enable the Next button.")
    
        if st.button("Next", key="btn_tab1_next", disabled=not is_valid, on_click=switch_tab, args=("Spouse Details",)):
            save_safe_state()
            st.success("Personal information saved! Moving to the next step...")


    # 2nd ট্যাব এর ডিজাইন
    with tab2:
        st.subheader("Spouse Details")
        
        if st.session_state.get('p_married') == 'YES':
            spouse_name = st.text_input("Kindly mention your spouse name:", key="sp_name")
            
            spouse_age = st.selectbox(
                "May I know what is the age of your spouse?", 
                [None] + list(range(18, 101)), 
                format_func=lambda x: "Select age" if x is None else str(x),
                key="sp_age"
            )
        
            spouse_profession = st.radio(
                "Kindly select your spouse's profession:",
                ('Business', 'Service(Govt. / Pvt.)', 'Self Employed', 'Non Earning member'),
                index=None,
                key="sp_prof"
            )
        
            if spouse_profession in ["Business", "Self Employed", "Service(Govt. / Pvt.)"]:
                spouse_income = st.number_input("What is your spouse's approximate monthly income?", min_value=0, step=1000, key="sp_inc")
            else:
                spouse_income = 0
        
            spouse_expenses = st.number_input("What is your spouse's approximate monthly household expenses?", min_value=0, step=1000, key="sp_exp")
        
            child = st.radio(
                "Do you have children?",
                ('YES', 'NO'),
                index=None,
                key="sp_child"
            )

            is_valid = bool(spouse_name and (spouse_age is not None) and (spouse_profession is not None) and (child is not None))
            
            if not is_valid:
                st.warning("⚠️ Please fill in all spouse details to enable the Next button.")
       
            if st.button("Next", key="btn_tab2_next", disabled=not is_valid, on_click=switch_tab, args=("Child Details",)):
                save_safe_state()
                st.success("Spouse information saved! Moving to the next step...")
        
        elif st.session_state.get('p_married') == 'NO':
            st.info("Since you are unmarried, this section is not applicable.")
            if st.button("Skip to Next Step", key="btn_tab2_skip", on_click=switch_tab, args=("Child Details",)):
                save_safe_state()
                pass
                
        else:
            st.warning("Please fill the Personal Info tab first.")


    # 3rd ট্যাব এর ডিজাইন
    with tab3:
        st.subheader("Child & Dependent Details")
        
        children_data = []
        if st.session_state.get('sp_child') == 'YES':
            num_children = st.number_input("How many children do you have?", min_value=1, max_value=10, step=1, key="num_child")
            
            st.write("---")
            for i in range(num_children):
                st.markdown(f"**Child {i+1} Details:**")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    c_name = st.text_input("Name", key=f"c_name_{i}")
                with col2:
                    c_gender = st.selectbox("Gender", ['MALE', 'FEMALE', 'OTHER'], index=None, key=f"c_gender_{i}")
                with col3:
                    c_age = st.selectbox("Age", [None] + list(range(0, 51)), format_func=lambda x: "Select age" if x is None else f"{x} Years", key=f"c_age_{i}")
                
                children_data.append({"Name": c_name, "Gender": c_gender, "Age": c_age})
                st.write("")
                
            st.session_state.children_data = children_data
                
        elif st.session_state.get('sp_child') == 'NO':
            st.info("Since you do not have children, child details are not applicable.")
            st.session_state.children_data = []
            
        elif st.session_state.get('p_married') == 'NO':
             st.info("Since you are unmarried, child details are not applicable.")
             st.session_state.children_data = []
             
        else:
             st.warning("Please fill the Spouse Details tab first.")

        st.write("---")
        dependent = st.radio(
            "Do you have any member in your family who is completely dependent on your income?",
            ('YES', 'NO'),
            index=None,
            key="has_dependent"
        )
        
        target_tab = "Dependent Member" if dependent == 'YES' else "Future Expenses Projection"
        
        all_filled = True
        if st.session_state.get('sp_child') == 'YES':
            all_filled = all(child["Name"] and child["Gender"] and child["Age"] is not None for child in children_data)
        
        is_valid = all_filled and (dependent is not None)
        
        if not is_valid:
            st.warning("⚠️ Please fill in all details and answer the dependent question to enable the Next button.")

        if st.button("Next", key="btn_tab3_next", disabled=not is_valid, on_click=switch_tab, args=(target_tab,)):
            save_safe_state()
            st.success("Details saved successfully! Moving to the next step...")


    # 4th ট্যাব এর ডিজাইন
    with tab4:
        st.subheader("Dependent Member Details")
        
        dependents_data = []
        if st.session_state.get('has_dependent') == 'YES':
            st.info("Please provide the details of your dependent family members below:")
            
            num_dependents = st.number_input(
                "HOW MANY DEPENDENT MEMBERS ARE THERE IN YOUR FAMILY?", 
                min_value=1, max_value=10, step=1, key="num_dep"
            )
            
            st.write("---") 
            for i in range(num_dependents):
                st.markdown(f"**Dependent Member {i+1}:**")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    d_name = st.text_input("Name", key=f"d_name_{i}")
                with col2:
                    d_gender = st.selectbox("Gender", ['MALE', 'FEMALE', 'OTHER'], index=None, key=f"d_gender_{i}")
                with col3:
                    d_age = st.selectbox("Age", [None] + list(range(0, 101)), format_func=lambda x: "Select age" if x is None else f"{x} Years", key=f"d_age_{i}")
                with col4:
                    d_relation = st.selectbox("Relation", ['FATHER', 'MOTHER', 'BROTHER', 'SISTER', 'OTHER'], index=None, key=f"d_rel_{i}")
                
                dependents_data.append({"Name": d_name, "Gender": d_gender, "Age": d_age, "Relation": d_relation})
                st.write("")
            
            st.session_state.dependents_data = dependents_data
            
            is_valid = all(dep["Name"] and dep["Gender"] and (dep["Age"] is not None) and dep["Relation"] for dep in dependents_data)
            
            if not is_valid:
                st.warning("⚠️ Please fill in the Name, Gender, Age, and Relation for all dependent members to enable the Next button.")
                
            if st.button("Next", key="btn_tab4_next", disabled=not is_valid, on_click=switch_tab, args=("Future Expenses Projection",)):
                save_safe_state()
                st.success("Dependent members' details saved successfully! Moving to the next step...")
                
        elif st.session_state.get('has_dependent') == 'NO':
            st.info("Since you do not have any dependent family members, this section is not applicable.")
            if st.button("Skip to Income & Expenses", key="btn_tab4_skip", on_click=switch_tab, args=("Future Expenses Projection",)):
                save_safe_state()
                
        else:
            st.warning("Please complete the Child & Dependent Details tab first.")


    # 5th ট্যাব এর ডিজাইন (Future Expenses Projection & Goal Planning)
    with tab5:
        st.subheader("Future Expenses Projection")

        location = st.selectbox(
            "Where do you live?",
            ["Village", "Semi-village", "Small City", "City", "Megacity"],
            index=None,
            key="location_type"
        )

        st.write("---")

        if location:
            user_count = 1
            is_married = st.session_state.get('p_married') == 'YES'
            spouse_count = 1 if is_married else 0
            
            child_data = st.session_state.get('children_data', [])
            child_count = len(child_data) if st.session_state.get('sp_child') == 'YES' else 0
            
            dep_data = st.session_state.get('dependents_data', [])
            dep_count = len(dep_data) if st.session_state.get('has_dependent') == 'YES' else 0

            total_member = user_count + spouse_count + child_count + dep_count

            user_exp = st.session_state.get('p_exp', 0)
            spouse_exp = st.session_state.get('sp_exp', 0)
            total_expense = user_exp + spouse_exp

            exp_per_head = total_expense / total_member if total_member > 0 else 0

            levels = ["Basic", "Modest", "Standard", "Comfortable", "Upper_Middle class", "Affluent", "Luxury", "Elite"]
            lvl = 0 

            if location == "Village":
                if exp_per_head <= 5000: lvl = 0
                elif exp_per_head <= 10000: lvl = 1
                elif exp_per_head <= 15000: lvl = 2
                elif exp_per_head <= 20000: lvl = 3
                elif exp_per_head <= 30000: lvl = 4
                elif exp_per_head <= 50000: lvl = 5
                elif exp_per_head <= 75000: lvl = 6
                else: lvl = 7
            elif location == "Semi-village":
                if exp_per_head <= 8000: lvl = 0
                elif exp_per_head <= 12000: lvl = 1
                elif exp_per_head <= 20000: lvl = 2
                elif exp_per_head <= 35000: lvl = 3
                elif exp_per_head <= 50000: lvl = 4
                elif exp_per_head <= 75000: lvl = 5
                elif exp_per_head <= 100000: lvl = 6
                else: lvl = 7
            elif location == "Small City":
                if exp_per_head <= 10000: lvl = 0
                elif exp_per_head <= 15000: lvl = 1
                elif exp_per_head <= 22000: lvl = 2
                elif exp_per_head <= 40000: lvl = 3
                elif exp_per_head <= 60000: lvl = 4
                elif exp_per_head <= 100000: lvl = 5
                elif exp_per_head <= 120000: lvl = 6
                else: lvl = 7
            elif location == "City":
                if exp_per_head <= 12000: lvl = 0
                elif exp_per_head <= 18000: lvl = 1
                elif exp_per_head <= 25000: lvl = 2
                elif exp_per_head <= 50000: lvl = 3
                elif exp_per_head <= 80000: lvl = 4
                elif exp_per_head <= 110000: lvl = 5
                elif exp_per_head <= 130000: lvl = 6
                else: lvl = 7
            elif location == "Megacity":
                if exp_per_head <= 15000: lvl = 0
                elif exp_per_head <= 20000: lvl = 1
                elif exp_per_head <= 22000: lvl = 2
                elif exp_per_head <= 30000: lvl = 3
                elif exp_per_head <= 60000: lvl = 4
                elif exp_per_head <= 100000: lvl = 5
                elif exp_per_head <= 150000: lvl = 6
                else: lvl = 7

            style_status = levels[lvl]

            st.info(f"📊 **Calculation:** Total Members: **{total_member}** | Total Family Expense: **₹ {total_expense:,.2f}** | Per Head Expense: **₹ {exp_per_head:,.2f}**")
            st.success(f"As per your expenses, your default lifestyle status is: **{style_status.upper()}**")

            st.write("---")

            st.markdown("### 🎯 Customized Goal List")
            final_goals_list = []

            if not is_married:
                st.info("Since you are unmarried, here is your customized recommended goal list:")
                st.markdown("#### 📌 Recommended Goals")
                
                col1, col2 = st.columns(2)
                with col1:
                    g_retire = st.checkbox("Retirement Fund", value=True, key="u_retire")
                    g_med_emerg = st.checkbox("Medical Emergency Fund", value=True, key="u_med_emerg")
                    g_emerg = st.checkbox("Contingency/Emergency Fund", value=True, key="u_emerg")
                    
                with col2:
                    g_marriage = st.checkbox("Marriage", value=True, key="u_marriage")
                    g_child_plan = st.checkbox("Child Planning", value=True, key="u_child_plan")
                    
                    num_planned_child = 0
                    child_goals_status = {}
                    
                    if g_child_plan:
                        num_planned_child = st.number_input("How many children do you plan to have?", min_value=1, max_value=10, value=1, step=1, key="u_plan_child_qty")
                        for i in range(1, num_planned_child + 1):
                            st.markdown(f"**🔹 For Child {i}:**")
                            child_goals_status[f"c{i}_edu"] = st.checkbox(f"Child {i} Education", value=True, key=f"u_chk_c{i}_edu")
                            child_goals_status[f"c{i}_mar"] = st.checkbox(f"Child {i} Marriage", value=True, key=f"u_chk_c{i}_mar")

                st.write("---")
                st.markdown("#### ➕ Additional Goals")
                
                additional_goals = ["House", "Car", "Vacation", "Lavish Accessories", "Business Set up fund", "Gadgets"]
                selected_additional_goals = {}
                
                add_cols = st.columns(3)
                for idx, goal_name in enumerate(additional_goals):
                    col = add_cols[idx % 3]
                    with col:
                        is_checked = st.checkbox(goal_name, value=False, key=f"u_chk_{goal_name}")
                        if is_checked:
                            qty = st.number_input(f"Qty", min_value=1, value=1, step=1, key=f"u_qty_{goal_name}")
                            selected_additional_goals[goal_name] = qty

                if g_retire: final_goals_list.append("Retirement Fund")
                if g_med_emerg: final_goals_list.append("Medical Emergency Fund")
                if g_emerg: final_goals_list.append("Contingency/Emergency Fund")
                if g_marriage: final_goals_list.append("Marriage")
                
                if g_child_plan and num_planned_child > 0:
                    for i in range(1, num_planned_child + 1):
                        if child_goals_status[f"c{i}_edu"]: final_goals_list.append(f"Child {i} Education")
                        if child_goals_status[f"c{i}_mar"]: final_goals_list.append(f"Child {i} Marriage")
                
                for goal, qty in selected_additional_goals.items():
                    if qty == 1: final_goals_list.append(goal)
                    else:
                        for i in range(1, qty + 1): final_goals_list.append(f"{goal} {i}")
            
            else:
                st.info("Since you are married, here is your customized recommended goal list:")
                st.markdown("#### 📌 Recommended Goals")
                
                col1, col2 = st.columns(2)
                with col1:
                    m_retire = st.checkbox("Retirement Fund", value=True, key="m_retire")
                    m_med_emerg = st.checkbox("Medical Emergency Fund", value=True, key="m_med_emerg")
                    m_emerg = st.checkbox("Contingency/Emergency Fund", value=True, key="m_emerg")
                
                with col2:
                    has_child = st.session_state.get('sp_child') == 'YES'
                    m_child_plan = False
                    num_planned_child = 0
                    planned_child_status = {}
                    
                    if not has_child:
                        m_child_plan = st.checkbox("Child Planning", value=True, key="m_child_plan")
                        if m_child_plan:
                            num_planned_child = st.number_input("How many children do you plan to have?", min_value=1, max_value=10, value=1, step=1, key="m_plan_child_qty")
                            for i in range(1, num_planned_child + 1):
                                st.markdown(f"**🔹 For Future Child {i}:**")
                                planned_child_status[f"fc{i}_edu"] = st.checkbox(f"Future Child {i} Education", value=True, key=f"m_chk_fc{i}_edu")
                                planned_child_status[f"fc{i}_mar"] = st.checkbox(f"Future Child {i} Marriage", value=True, key=f"m_chk_fc{i}_mar")

                existing_child_status = {}
                if has_child:
                    st.write("---")
                    st.markdown("#### 👶 Existing Children Goals")
                    for i, kid in enumerate(child_data):
                        kid_name = kid['Name'] if kid['Name'] else f"Child {i+1}"
                        st.markdown(f"**🔹 For {kid_name}:**")
                        existing_child_status[f"{kid_name}_edu"] = st.checkbox(f"Education Expense for {kid_name}", value=True, key=f"m_chk_ex_{i}_edu")
                        existing_child_status[f"{kid_name}_mar"] = st.checkbox(f"Marriage Expense for {kid_name}", value=True, key=f"m_chk_ex_{i}_mar")
                
                st.write("---")
                st.markdown("#### ➕ Additional Goals")
                
                additional_goals = ["House", "Car", "Vacation", "Lavish Accessories", "Business Set up fund", "Gadgets"]
                if has_child:
                    additional_goals.insert(0, "Additional Child Planning")
                    
                selected_additional_goals = {}
                add_cols = st.columns(3)
                for idx, goal_name in enumerate(additional_goals):
                    col = add_cols[idx % 3]
                    with col:
                        is_checked = st.checkbox(goal_name, value=False, key=f"m_add_{idx}")
                        if is_checked:
                            qty = st.number_input(f"Qty", min_value=1, value=1, step=1, key=f"m_qty_{idx}")
                            selected_additional_goals[goal_name] = qty

                if m_retire: final_goals_list.append("Retirement Fund")
                if m_med_emerg: final_goals_list.append("Medical Emergency Fund")
                if m_emerg: final_goals_list.append("Contingency/Emergency Fund")
                
                if not has_child and m_child_plan and num_planned_child > 0:
                    for i in range(1, num_planned_child + 1):
                        if planned_child_status[f"fc{i}_edu"]: final_goals_list.append(f"Future Child {i} Education")
                        if planned_child_status[f"fc{i}_mar"]: final_goals_list.append(f"Future Child {i} Marriage")
                
                if has_child:
                    for i, kid in enumerate(child_data):
                        kid_name = kid['Name'] if kid['Name'] else f"Child {i+1}"
                        if existing_child_status[f"{kid_name}_edu"]: final_goals_list.append(f"Education Expense for {kid_name}")
                        if existing_child_status[f"{kid_name}_mar"]: final_goals_list.append(f"Marriage Expense for {kid_name}")
                
                for goal, qty in selected_additional_goals.items():
                    if goal == "Additional Child Planning":
                        for i in range(1, qty + 1):
                            final_goals_list.append(f"Additional Child {i} Education")
                            final_goals_list.append(f"Additional Child {i} Marriage")
                    elif qty == 1: 
                        final_goals_list.append(goal)
                    else:
                        for i in range(1, qty + 1): final_goals_list.append(f"{goal} {i}")

            st.session_state.final_goals_list = final_goals_list

            # ==============================================================
            # ৭. ৬-কলামের টেবিল তৈরি 
            # ==============================================================
            if len(final_goals_list) > 0:
                st.write("---")
                st.markdown("### 📋 Your Customized Goal Table")
                
                total_monthly_income = st.session_state.get('p_inc', 0) + st.session_state.get('sp_inc', 0)
                annual_income = total_monthly_income * 12
                annual_expense = total_expense * 12 
                
                user_age = st.session_state.get('p_age', 30) or 30
                
                kids_dict = {}
                for i, kid in enumerate(child_data):
                    k_name = kid.get('Name') if kid.get('Name') else f"Child {i+1}"
                    kids_dict[k_name] = kid
                
                h1, h2, h3, h4, h5, h6 = st.columns(6)
                h1.markdown("**Goal Name**")
                h2.markdown("**Present Value (₹)**")
                h3.markdown("**Duration (Yrs)**")
                h4.markdown("**Inflation (%)**") 
                h5.markdown("**Future Value (₹)**") 
                h6.markdown("**Col 6**")
                st.markdown("---")
                
                goal_custom_names = {} 
                goal_present_values = {}
                goal_durations = {} 
                goal_inflations = {} 
                goal_future_values = {} 
                
                for i, goal in enumerate(final_goals_list):
                    c1, c2, c3, c4, c5, c6 = st.columns(6)
                    
                    with c2: 
                        default_val = 0.0
                        if goal == "Retirement Fund":
                            if style_status == "Basic": default_val = (annual_income * 0.40) / 0.09
                            elif style_status == "Modest": default_val = (annual_income * 0.45) / 0.09
                            elif style_status == "Standard": default_val = (annual_income * 0.50) / 0.09
                            elif style_status == "Comfortable": default_val = (annual_income * 0.60) / 0.09
                            elif style_status == "Upper_Middle class": default_val = (annual_income * 0.70) / 0.09
                            elif style_status == "Affluent": default_val = (annual_income * 0.80) / 0.09
                            elif style_status == "Luxury": default_val = (annual_income * 0.90) / 0.09
                            elif style_status == "Elite": default_val = annual_income / 0.09 
                        elif goal == "Medical Emergency Fund":
                            default_val = float(annual_expense * 5)
                        elif goal == "Contingency/Emergency Fund":
                            default_val = float(annual_income * 3)
                        elif "Education" in goal:
                            if style_status == "Basic": default_val = 500000.0      
                            elif style_status == "Modest": default_val = 1000000.0     
                            elif style_status == "Standard": default_val = 1500000.0     
                            elif style_status == "Comfortable": default_val = 2500000.0     
                            elif style_status == "Upper_Middle class": default_val = 4000000.0     
                            elif style_status == "Affluent": default_val = 6500000.0     
                            elif style_status == "Luxury": default_val = 10000000.0    
                            elif style_status == "Elite": default_val = 20000000.0    
                        elif "Marriage" in goal:
                            if style_status == "Basic": default_val = 1000000.0      
                            elif style_status == "Modest": default_val = 1500000.0     
                            elif style_status == "Standard": default_val = 2000000.0     
                            elif style_status == "Comfortable": default_val = 2500000.0     
                            elif style_status == "Upper_Middle class": default_val = 4000000.0     
                            elif style_status == "Affluent": default_val = 6000000.0     
                            elif style_status == "Luxury": default_val = 10000000.0    
                            elif style_status == "Elite": default_val = 25000000.0 
                        
                        pv_value = st.number_input(
                            f"PV for {goal}",
                            value=float(st.session_state.get(f"pv_{goal}", default_val)), 
                            min_value=0.0, step=1000.0, format="%0.2f", 
                            key=f"pv_{goal}", label_visibility="collapsed"
                        )
                        goal_present_values[goal] = pv_value

                        if goal == "Retirement Fund":
                            st.markdown(f"<div style='font-size:12px; color:gray; margin-top:-10px; margin-bottom:10px;'>Pension: ₹ {(pv_value * 0.09) / 12:,.2f} /mo</div>", unsafe_allow_html=True)

                    with c3: 
                        default_dur = 0
                        if goal == "Retirement Fund": default_dur = max(0, 60 - user_age)
                        elif goal in ["Medical Emergency Fund", "Contingency/Emergency Fund"]: default_dur = 0
                        elif "Future Child" in goal or "Additional Child" in goal or (goal.startswith("Child ") and not is_married):
                            if "Education" in goal: default_dur = 17
                            elif "Marriage" in goal: default_dur = 24
                        elif goal.startswith("Education Expense for "):
                            k_name = goal.replace("Education Expense for ", "")
                            default_dur = max(0, 17 - (kids_dict.get(k_name, {}).get("Age") or 0))
                        elif goal.startswith("Marriage Expense for "):
                            k_name = goal.replace("Marriage Expense for ", "")
                            k_info = kids_dict.get(k_name, {})
                            k_age, k_gen = k_info.get("Age") or 0, k_info.get("Gender", "FEMALE")
                            default_dur = max(0, 28 - k_age) if k_gen == "MALE" else max(0, 24 - k_age)
                        
                        dur_value = st.number_input(
                            f"Dur for {goal}",
                            value=int(st.session_state.get(f"dur_{goal}", default_dur)),
                            min_value=0, step=1, key=f"dur_{goal}", label_visibility="collapsed"
                        )
                        goal_durations[goal] = dur_value

                    with c4:
                        default_inf = 5.0 
                        if "Education" in goal: default_inf = 7.0
                        elif "Medical" in goal: default_inf = 8.0
                            
                        inf_value = st.number_input(
                            f"Inf for {goal}",
                            value=float(st.session_state.get(f"inf_{goal}", default_inf)),
                            min_value=0.0, step=0.5, format="%0.1f", 
                            key=f"inf_{goal}", label_visibility="collapsed"
                        )
                        goal_inflations[goal] = inf_value

                    with c5:
                        fv_value = pv_value * ((1 + (inf_value / 100)) ** dur_value)
                        goal_future_values[goal] = fv_value
                        
                        st.markdown(
                            f"<div class='custom-result-box'>{fv_value:,.2f}</div>", 
                            unsafe_allow_html=True
                        )

                        if goal == "Retirement Fund":
                            st.markdown(f"<div style='font-size:12px; color:#2A9D8F; font-weight:bold; margin-top:5px; margin-bottom:10px;'>Pension: ₹ {(fv_value * 0.09) / 12:,.2f} /mo</div>", unsafe_allow_html=True)

                    with c1: 
                        if "Gadget" in goal:
                            custom_name = st.text_input(
                                f"Name for {goal}",
                                value=st.session_state.get(f"name_{goal}", goal),
                                key=f"name_{goal}",
                                label_visibility="collapsed"
                            )
                            goal_custom_names[goal] = custom_name
                        else:
                            st.write(f"🎯 **{goal}**")
                            goal_custom_names[goal] = goal 
                        
                    with c6: st.write("-")
                    
            st.session_state.goal_custom_names = goal_custom_names
            st.session_state.goal_present_values = goal_present_values
            st.session_state.goal_durations = goal_durations
            st.session_state.goal_inflations = goal_inflations
            st.session_state.goal_future_values = goal_future_values

            # ==============================================================
            # ৮. Finalize Goal Button 
            # ==============================================================
            st.write("---")
            
            if st.button("Finalize your goal", type="primary", key="btn_finalize_goals"):
                save_safe_state() 
                st.session_state.page = 'timeline_page'
                st.rerun()

        else:
            st.warning("⚠️ Please select your location to see your lifestyle calculation and enable the Next button.")


# ==========================================
# PAGE 3: Timeline & Final Calculation
# ==========================================
elif st.session_state.page == 'timeline_page':
    
    if st.button("⬅️ Back to Form"):
        save_safe_state()
        st.session_state.page = 'main_form'
        st.rerun()
        
    st.title("⏳ Your Financial Timeline")
    st.write("---")
    
    st.markdown("### Based on your age and goals, here is your timeline:")

save_safe_state()
