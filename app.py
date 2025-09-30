import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import hashlib
import sys, os
import time
import app_leaderboard

from streamlit_scroll_to_top import scroll_to_here
import app_modify_tables, app_modify_GitTable, app_display_results, app_display_parameters, app_email, app_final_result, app_game_description

st.set_page_config(
page_title="Idm-Systems - zenonIZE game 2025",
)

# --- SESSION STATE INIT ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "show_game_intro" not in st.session_state:
    st.session_state.show_game_intro = False
if "attempts" not in st.session_state:
    st.session_state.attempts = [None]*5
if "current_tab" not in st.session_state:
    st.session_state.current_tab = 0
if "show_summary" not in st.session_state:
    st.session_state.show_summary = False
if "confirm_finish" not in st.session_state:
    st.session_state.confirm_finish = False
if "page" not in st.session_state:
    st.session_state.page = "login"
if "nickname" not in st.session_state:
    st.session_state.nickname = ""


# Inicializálás, ha még nem létezik
if "back_to_info_values" not in st.session_state:
    st.session_state.back_to_info_values = {}
if "selections" not in st.session_state:
    st.session_state.selections = {}
if 'scroll_to_top' not in st.session_state:
    st.session_state.scroll_to_top = False
if 'scroll_to_top_Delay' not in st.session_state:
    st.session_state.scroll_to_top_Delay = False
if "sent_result_email" not in st.session_state:
   st.session_state.sent_result_email = False

def scroll():
    st.session_state.scroll_to_top = True

def scroll_Delay():
    st.session_state.scroll_to_top_Delay = True

params = st.query_params
if "page" in params and params["page"] == "leaderboard":
    st.session_state.page = "leaderboard"


#Local vagy Cloud:
try: github_token = st.secrets["GITHUB_TOKEN"]
except: github_token = None

# ------------------ GÖRGETÉS: KEZELÉS ------------------
if st.session_state.scroll_to_top:
    scroll_to_here(0, key="top")  # Scroll to the top of the page
    st.session_state.scroll_to_top = False  # Reset the state after scrolling
    time.sleep(0.2)
    st.rerun() 

elif st.session_state.scroll_to_top_Delay:
    scroll_to_here(0, key="top")  # Scroll to the top of the page
    st.session_state.scroll_to_top_Delay = False  # Reset the state after scrolling
    time.sleep(0.8)
    st.rerun() 


elif st.session_state.page == "leaderboard":
    app_leaderboard.show_leaderboard()  # run the leaderboard script
    st.stop()

elif st.session_state.page == "gtc":
    st.subheader("📄 General Terms and Conditions (GTC)")
    st.markdown("""           
    https://zenonize.idm-systems.hu/

    This agreement is made and entered into by and between IDM-Systems Zrt. (registered office: 4031 Debrecen, Köntösgát sor 1-3., company registration number: 09-10-000604), as Data Controller (hereinafter referred to as the ‘Data Controller’ or the ‘Service Provider’), and the registered user (hereinafter referred to as the ‘User’) of the online game provided on the website https://zenonize.idm-systems.hu/ (hereinafter: “Online Game”), hereinafter collectively referred to as the ‘Parties’, under the following terms and conditions:

    1.	What the Online Game is about?
             
    The Data Controller/Service Provider provides the Online Game available at https://zenonize.idm-systems.hu/ as an online platform designed to offer an interactive simulation of the challenges of modern manufacturing management. The Online Game is accessible via any web browser, mobile application, or other digital device.

    2.	Participation in the Online Game
             
    Participation in the Online Game is free of charge but requires registration.

    3.	Registration \
    The data required for registration are as follows:
        1.	Email address
        2.	Nickname  
                
    Registration is completed by providing the above data and by accepting the present Terms of Conditions.

    4.	Intellectual Property   
                
    The Online Game, including its source code, graphics, music, texts, and other elements, is protected by copyright and constitutes the exclusive property of the Data Controller/Service Provider.
    The User may use the Online Game solely for personal purposes.
    It is prohibited to copy, distribute, modify, or use the content of the Game for commercial purposes.

    5.	Limitation of Liability    
                
    The Data Controller/Service Provider shall make every effort to ensure the uninterrupted operation of the Online Game but does not guarantee that the Game will be free of errors or continuously available. The Data Controller/Service Provider shall not be liable for indirect damages, loss of profit, or data loss suffered by the User. The Data Controller/Service Provider accepts no responsibility for damages arising from the inaccuracy of data provided during registration.

    6.	Data Protection    
                
    The processing of Users’ personal data is carried out in accordance with the [PRIVACY POLICY], available on the Game’s website.

    7.	Amendments   
    
    The Data Controller/Service Provider reserves the right to amend the present Terms of Conditions. Such amendments shall enter into force upon their publication on the website. Continued use of the Online Game shall constitute acceptance of the amended Terms.

    8.	Governing Law and Dispute Resolution   
                
    These Terms of Conditions shall be governed by the laws of Hungary. The parties shall seek to resolve disputes amicably in the first instance. Should this not be possible, disputes shall fall under the jurisdiction of the competent court at the registered office of the Service Provider.
    These General Terms and Conditions are available in multiple languages. In the event of any inconsistency or divergence in interpretation between the language versions, the Hungarian version shall prevail and be deemed authoritative.

    If the User does not agree with any provision of these Terms of Conditions, they will not be able to participate in the Online Game.
    """)
    if st.button("⬅️ Back"):
        st.session_state.page = "login"
        st.rerun()
    st.stop()  # <- important, prevents login page rendering

# --- Contact consent page ---
elif st.session_state.page == "contact":
    st.subheader("📩 PRIVACY POLICY")
    st.markdown(f"""
    https://zenonize.idm-systems.hu/
    <div>
        
    <p>1.	Data Controller’s Information</p>
    <table id="company-details" style="margin-left:20px;">
            <thead></thead>
            <tbody>
                <tr>
                    <td>Company name:</td>
                    <td>IDM-Systems Zrt.</td>
                </tr>
                <tr>
                    <td>Registered office:</td>
                    <td>4031 Debrecen, Köntösgát sor 1-3.</td>
                </tr>
                <tr>
                    <td>Company registration number:</td>
                    <td>09-10-000604</td>
                </tr>
                <tr>
                    <td>Tax number:</td>
                    <td>27962844-2-09.</td>
                </tr>
                <tr>
                    <td>Email:</td>
                    <td><a href="mailto:privacy@idm-systems.hu">privacy@idm-systems.hu</a></td>
                </tr>
            </tbody>
        </table>
        <p> 2.	Details of Data Processing</p>
        <p style="margin-left: 5px;">2.1.	Data processed during the use of the online game available at: <a href="https://zenonize.idm-systems.hu/">https://zenonize.idm-systems.hu/</a></p>
        <table id="details-of-data-processing-1" style="margin-left:50px;">
            <thead></thead>
            <tbody>
                <tr>
                    <td><b>Name of Data Processing:</b></td>
                    <td>Recording, storing, and deletion of the data provided by the registrant for the purpose of using the online game.</td>
                </tr>
                <tr>
                    <td>Purpose of Data Processing:</td>
                    <td>Participation in the online game.</td>
                </tr>
                <tr>
                    <td>Legal Basis for Data Processing:</td>
                    <td><a href="https://net.jogtar.hu/jogszabaly?docid=A1600679.EUP&searchUrl=/gyorskereso?keyword%3Dgdpr%25206.%25201.%2520f">GDPR 6. 1) a)</a> Voluntary consent.</td>
                </tr>
                <tr>
                    <td>Data Processor’s Name and Address:</td>
                    <td><a href="https://forpsi.hu">forpsi.hu</a><br>
                        Company name: BlazeArts Kft.<br>
                        Registered office: 1096 Budapest, Thaly Kálmán 39.<br>
                        Mailing address: 1096 Budapest, Thaly Kálmán 39.<br>
                        Company registration number: 01 09 389087<br>
                        Tax number: 12539833-2-03<br>
                        EU VAT number: HU12539833<br>
                        </td>
                </tr>
                <tr>
                    <td>Data Processor’s Activities Related to Data Processing:</td>
                    <td>Hosting, database, and email services, as well as sending emails from news@idm-systems.hu regarding entry into the game, its completion, and the results.</td>
                </tr>
                <tr>
                    <td>Categories of Personal Data Processed by the Data Controller:</td>
                    <td>Provided by voluntary consent: email address, nickname</td>
                </tr>
                <tr>
                    <td>Retention Period:</td>
                    <td>For the duration of participation in the online game.</td>
                </tr>
                <tr>
                    <td>Source of Data:</td>
                    <td>Provided by voluntary consent.</td>
                </tr>
                <tr>
                    <td>Data Transfers:</td>
                    <td>None.</td>
                </tr>
                <tr>
                    <td>Legal Basis for Data Transfers:</td>
                    <td>Not applicable.</td>
                </tr>
                <tr>
                    <td>Scope of Data Subjects:</td>
                    <td>Individuals participating in the online game.</td>
                </tr>
                <tr>
                    <td>Is Profiling Conducted During the Activity?</td>
                    <td>No.</td>
                </tr>
                <tr>
                    <td>Are Automated Technologies Used for Profiling?</td>
                    <td>Not applicable.</td>
                </tr>
                <tr>
                    <td>Unsubscribing / Withdrawal of Consent:</td>
                    <td>Not applicable.</td>
                </tr>
            </tbody>
        </table>
        <p style="margin-left:5px;">2.2. On the <a href="https://zenonize.idm-systems.hu/">https://zenonize.idm-systems.hu/</a> online game website, the Data Controller provides the possibility to subscribe via the “Contact me” option, whereby the User gives their explicit and voluntary consent for the Data Controller to initiate contact with them within a specified period following the use of the online game.</p>
        <table id="details-of-data-processing-2" style="margin-left:50px;">
            <thead></thead>
            <tbody>
                <tr>
                    <td><b>Name of Data Processing:</b></td>
                    <td>Recording, storing, and deletion of the data of individuals subscribing via the “Contact me” option.</td>
                </tr>
                <tr>
                    <td>Purpose of Data Processing:</td>
                    <td>Establishing contact with potential customers, partners.</td>
                </tr>
                <tr>
                    <td>Legal Basis for Data Processing:</td>
                    <td><a href="https://net.jogtar.hu/jogszabaly?docid=A1600679.EUP&searchUrl=/gyorskereso?keyword%3Dgdpr%25206.%25201.%2520f">GDPR 6. 1) f)</a> Legitimate interest of the Data Controller.</td>
                </tr>
                <tr>
                    <td>Data Processor’s Name and Address:</td>
                    <td><a href="https://forpsi.hu">forpsi.hu</a><br>
                        Company name: BlazeArts Kft.<br>
                        Registered office: 1096 Budapest, Thaly Kálmán 39.<br>
                        Mailing address: 1096 Budapest, Thaly Kálmán 39.<br>
                        Company registration number: 01 09 389087<br>
                        Tax number: 12539833-2-03<br>
                        EU VAT number: HU12539833<br>
                    </td>
                </tr>
                <tr>
                    <td>Data Processor’s Activities Related to Data Processing:</td>
                    <td>Hosting, database, and email services, as well as sending the submitter’s data to sales@idm-systems.hu for the purpose of establishing contact.</td>
                </tr>
                <tr>
                    <td>Categories of Personal Data Processed by the Data Controller:</td>
                    <td>Provided by voluntary consent: email address, nickname</td>
                </tr>
                <tr>
                    <td>Retention Period:</td>
                    <td>14 days following participation in the online game for the purpose of establishing contact.</td>
                </tr>
                <tr>
                    <td>Source of Data:</td>
                    <td>Provided by voluntary consent.</td>
                </tr>
                <tr>
                    <td>Data Transfers:</td>
                    <td>None.</td>
                </tr>
                <tr>
                    <td>Legal Basis for Data Transfers:</td>
                    <td>Not applicable.</td>
                </tr>
                <tr>
                    <td>Scope of Data Subjects:</td>
                    <td>Individuals subscribing via the “Contact me” option.</td>
                </tr>
                <tr>
                    <td>Is Profiling Conducted During the Activity?</td>
                    <td>No</td>
                </tr>
                <tr>
                    <td>Are Automated Technologies Used for Profiling?</td>
                    <td>Not applicable.</td>
                </tr>
                <tr>
                    <td>Unsubscribing / Withdrawal of Consent:</td>
                    <td><a href="mailto:privacy@idm-systems.hu">privacy@idm-systems.hu</a></td>
                </tr>
            </tbody>
        </table>
        <p>3.	What are your rights in relation to data processing and how can you exercise them?<br>
            Rights related to data processing and their enforcement:<br>
            At the postal address or by e-mail indicated in Section 1 you may</p>
                <p style="margin-left:5px;">a)	request information about the processing of your personal data (this is known as the right of access), <br>
                b)	request the rectification or erasure of your personal data,<br>
                c)	request the transfer of your personal data to another controller (this is known as the right to data portability),<br>
                d)	request the restriction of processing.<br>
                e)	may object to the processing,<br>
                f)	can request that the automated decision making does not apply to you,<br>
                g)	may withdraw the consent to the processing at any time.</p><br>
        <p style="margin-left:0px;">Further details related to data processing can be found in the document titled [IDM_Systems_Zrt_Privacy_Notice_for_Website_Visitors_20251001], available on the Data Controller’s website.</p>
    </div>
   
    """, unsafe_allow_html=True)
    if st.button("⬅️ Back"):
        st.session_state.page = "login"
        st.rerun()
    st.stop()  # <- important, prevents login page rendering

# ------------------ LOGIN KEZELÉS ------------------
elif not st.session_state.logged_in:
     # --- Login Page ---
    if st.session_state.page == "login":
        st.image("header.png", width='content')
        st.subheader("Welcome to the Game! 🎮")
        # 🔹 Add Leaderboard button here
        if st.button("🏆 View Leaderboard"):
            st.session_state.page = "leaderboard"
            scroll()
            st.rerun()
        st.markdown("<hr style='border:1px solid #F15922; margin:0px 0'>", unsafe_allow_html=True) #Vízszintes vonal
        email = st.text_input("**E-mail address** * - *it will not be shown publicly*", placeholder="letsplayagame@gmail.com")
        nickname = st.text_input("**Nickname:** * - *this will be your public identifier*", placeholder="I am the winner")

        # A részletes Terms szöveg külön szakaszban
        #with st.expander("Detailed Terms and Conditions"):
        agree = st.checkbox(" I’ve read and accept the General Terms and Conditions(GTC) — I’m ready to play! *")
        if st.button("📄 View GTC"):
            st.session_state.page = "gtc"
            scroll()
            st.rerun()
        
        agree_w_news = st.checkbox("“Contact me“ — I agree and give my consent to be contacted after the Online Game. ")
        if st.button("📩 View Privacy Policy"):
            st.session_state.page = "contact"
            scroll()
            st.rerun()

        # JS script hozzáadása
        st.markdown("""
        <script>
        const theme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
        document.body.setAttribute('data-user-theme', theme);
        </script>
        """, unsafe_allow_html=True)

        if st.button("Login"):

            #Checkolja e-mailt!
            email_valid = False
            if email != "":
                email_valid = app_email.is_valid_email(email)

            nickname = nickname.strip()  # Remove leading/trailing whitespace
            # Attempt login
            if email_valid and nickname and agree:
                
                #Változók mentése:
                st.session_state.email_hash = hashlib.sha256(email.encode()).hexdigest()
                st.session_state.email = email
                st.session_state.nickname = nickname

                if github_token == None: #Lokális futtatás
                    players = app_modify_tables.login_player(nickname, st.session_state.email_hash)
                # else: #Cloud futtatás
                #     players = app_modify_GitTable.login_player(nickname, st.session_state.email_hash, "lapatinszki/simulator-app")
                    


                if players is None:
                    # Player already exists
                    st.warning(f"The nickname '{nickname}' is already taken. Please choose another one.")
                else:
                    # Login successful
                    st.session_state.logged_in = True
                
                    #E-mail küldése bejenlentkezésről! -- Csak guthubos deploy esetén menjen ki az e-mail
                    # if github_token == None: #Lokális futtatás
                    #     print("Not sending e-mail in local run.")
                    # else:
                    app_email.send_email(email, st.session_state.email_hash, nickname, agree_w_news)

                    st.session_state.show_game_intro = True
                    scroll_Delay()
                    st.rerun()
            else:
                if email == "":
                    st.warning("Please enter your e-mail!")
                else:
                    if email_valid == False:
                        st.warning("Please enter a valid e-mail!")
                if nickname == "":               
                    st.warning("Please enter your nickname!")              
                if not agree:
                    st.warning("You must agree to the terms and conditions to proceed.")

# ------------------ JÁTÉK LEÍRÁS OLDAL -------------------
elif st.session_state.show_game_intro:
    st.image("header.png", width='content')
    app_game_description.game_info()
    if st.button("Let's play"):               
        st.session_state.show_game_intro = False
        scroll_Delay()
        st.rerun()
    


# ------------------ VÉGEREDMÉNY FELÜLET ------------------
elif st.session_state.show_summary:
    app_final_result.calculate_results(github_token, st.session_state.nickname, st.session_state.email)




# ------------------ JÁTÉK FELÜLET ------------------
else:
    st.image("header.png", width='content')
    st.subheader(f"Let's play the game, {st.session_state.nickname}! 🎮")
    st.markdown("<hr style='border:1px solid #F15922; margin:0px 0'>", unsafe_allow_html=True) #Vízszintes vonal

    if st.button("Back to description"):
        st.session_state.back_to_info_values = st.session_state.selections.copy()  # selections = aktuális paraméterek
        st.session_state.show_game_intro = True
        scroll()
        st.rerun()
    
    st.markdown("<hr style='border:1px solid rgba(241, 89, 34, 0.3); margin:0px 0'>", unsafe_allow_html=True) #Vízszintes vonal


    @st.cache_data
    def load_data():
        # Import connection functions
        import app_modify_tables
        # Get simulation results from database
        df = app_modify_tables.get_simulation_results()
        return df
    df = load_data()

    #Paraméterek indexel importálás:
    repo_root = os.path.dirname(os.path.abspath(__file__))
    if repo_root not in sys.path:
        sys.path.append(repo_root)
    from app_display_parameters import param_cols

    total_attempts = 5
    current_attempt_display = st.session_state.current_tab + 1
    st.markdown(f"*You have **{total_attempts}** attempts in total. You are currently at your **{current_attempt_display}.** attempt!*")
    # --- Tab logika ---
    tab_labels = []
    for idx in range(total_attempts):
        if st.session_state.attempts[idx] is None:
            tab_labels.append(f"Attempt {idx+1}")
        else:
            # Mask létrehozása
            mask = pd.Series([True]*len(df))
            for col in param_cols:
                val = st.session_state.attempts[idx][col]
                mask &= df[col] == val
            
            if mask.sum() > 0:
                selected_row = df[mask].iloc[0]
                row_index = df[mask].index[0]

                profit = selected_row.get("Profit", None)  # vagy selected_row["Profit"]
                profit_float = float(profit)
                profit_str = f"{profit_float:10.2f}"


                tab_labels.append(f"Attempt {idx+1}     - **Profit: {profit_str} €**")

    selectable_tabs = tab_labels[:st.session_state.current_tab+1]
    selected_tab = st.radio("Select attempt:", selectable_tabs, index=st.session_state.current_tab, format_func=lambda x: x)
    i = tab_labels.index(selected_tab)




    # ------------------------ Paraméterek kiválasztása ------------------------
    if st.session_state.attempts[i] is None:
        st.markdown("<hr style='border:1px solid #F15922; margin:0px 0'>", unsafe_allow_html=True) #Vízszintes vonal
        st.subheader("Select input parameters")
        attempt_idx = st.session_state.current_tab
        selections = app_display_parameters.display_inputs(attempt_idx)
        #st.session_state.back_to_info_values = st.session_state.selections.copy()  # selections = aktuális paraméterek

        # ------------------------ Szimuláció FUTTATÁSA ------------------------
        # ------------------------ Szimuláció FUTTATÁSA ------------------------
        if st.button("Run the simulation!"):

            # --- Megtaláljuk a kiválasztott paramétereknek megfelelő sort ---
            mask = pd.Series([True]*len(df))
            for col_name in param_cols:
                mask &= df[col_name] == selections[col_name]

            if mask.sum() == 0:
                st.error("No row found for the selected parameter combination.")
            else:
                selected_row = df[mask].iloc[0]  # csak egy sor kell

                # --- Profit biztonságos kiolvasása ---
                profit_value = float(selected_row.get("Profit", 0.0))
                nickname = st.session_state.get("nickname")
                email_hash = st.session_state.get("email_hash")

                # --- Show animation and update database ---
                start_time = time.time()
                overlay_placeholder = app_display_results.play_the_GIF()

                # Update database
                if github_token is None:  # Lokális futtatás
                    app_modify_tables.update_player_attempt(nickname, email_hash, profit_value, attempt_idx)
                    app_modify_tables.update_leaderboard(nickname, profit_value)
                # else:  # Cloud futtatás
                #     app_modify_GitTable.update_player_attempt(nickname, email_hash, profit_value, "lapatinszki/simulator-app")
                #     app_modify_GitTable.update_leaderboard(nickname, profit_value, "lapatinszki/simulator-app")

                # Keep animation for minimum duration
                while time.time() - start_time < 5:  # minimum 5 seconds animation
                    time.sleep(0.1)

                overlay_placeholder.empty()  # Remove the GIF

                # --- Attempt mentése Profit-tal együtt ---
                selections_with_profit = selections.copy()
                selections_with_profit["Profit"] = profit_value
                st.session_state.attempts[i] = selections_with_profit

                scroll()
                st.rerun()


    # ------------------------ Eredmények megjelenítése ------------------------
    else:
        selections = st.session_state.attempts[i]
        st.session_state.back_to_info_values = st.session_state.selections.copy()  # selections = aktuális paraméterek

        # Mask létrehozása a kiválasztott paraméterekhez
        mask = pd.Series([True]*len(df))
        for col in param_cols:
            mask &= df[col] == selections[col]

        if mask.sum() == 0:
            st.error("No row found for the selected parameter combination.")
        else:
            # Megtalált sor
            selected_row = df[mask].iloc[0]
            row_index = df[mask].index[0]  # DataFrame sor indexe
            

            #Eredmények:
            app_display_results.display_tables(selected_row, df)
            app_display_results.display_charts(selected_row, df)





            # ---------------------------------------------------------------------
            # ---------------------------------------------------------------------
            # Csak akkor jelenjen meg a "New attempt" gomb és a "View results" gomb,
            # ha az aktuális attemptnél vagyunk
            st.markdown("<hr style='border:1px solid #F15922; margin:0px 0'>", unsafe_allow_html=True) #Vízszintes vonal
            if i == st.session_state.current_tab:
                # New attempt gomb
                if i < total_attempts - 1 and st.session_state.attempts[i+1] is None:
                    if st.button("Next round! Let’s do this! 🔄", key=f"new_attempt_{i}"):
                        scroll_Delay()
                        st.session_state.current_tab = i + 1  
                        st.rerun()
                        

                # Csak akkor kell megerősítés, ha nem az utolsó attempt
                is_last_attempt = (i == total_attempts - 1)

                # Finish the game gomb
                if st.button("Finish the game 🏁", key=f"view_results_{i}"):
                    if is_last_attempt:
                        st.session_state.show_summary = True
                        st.rerun()
                    else:
                        st.session_state.confirm_finish = True
                        st.rerun()

                # Ha megerősítést kérünk
                if st.session_state.confirm_finish:
                    st.warning("⚠️ Are you sure you want to finish the game? You won’t be able to go back after this!")

                    if st.button("✅ Yes, I’m ready for my results!", key=f"confirm_yes_{i}"):
                        scroll_Delay()
                        st.session_state.show_summary = True
                        st.session_state.confirm_finish = False
                        st.rerun()
                    if st.button("❌ No, I'll keep playing!", key=f"confirm_no_{i}"):
                        st.session_state.confirm_finish = False
                        st.rerun()
