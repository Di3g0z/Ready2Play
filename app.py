
import streamlit as st
import datetime
import time
import base64
import mimetypes
import pytz

# Configurazione Pagina
st.set_page_config(page_title="Ready2Play", page_icon="logo_r2p.png", layout="centered")

# --- STATO ---
if 'invite_status' not in st.session_state:
    st.session_state.invite_status = "pending"

if 'booking_target' not in st.session_state:
    st.session_state.booking_target = None

if 'bookings' not in st.session_state:
    st.session_state.bookings = []

if 'search_results' not in st.session_state:
    st.session_state.search_results = []

if 'invite_booking' not in st.session_state:
    st.session_state.invite_booking = None

if 'invited_people' not in st.session_state:
    st.session_state.invited_people = {}

if 'accepted_invite' not in st.session_state:
    st.session_state.accepted_invite = None

if 'joined_matches' not in st.session_state:
    st.session_state.joined_matches = []

if 'balance' not in st.session_state:
    st.session_state.balance = 50.00

if 'price_per_person' not in st.session_state:
    st.session_state.price_per_person = 5.00

if 'smart_access_target' not in st.session_state:
    st.session_state.smart_access_target = None

if 'show_reload_input' not in st.session_state:
    st.session_state.show_reload_input = False

# --- STYLE & COLORS (Deep Dark Navy) ---
st.markdown("""
    <style>
    :root {
        --r2p-dark: #000B18;
        --r2p-navy: #001F3F;
        --r2p-green: #7CFF01;
    }
    
    .stApp { background-color: var(--r2p-dark); color: white; }
    
    /* Tabs Navigation */
    .stTabs [data-baseweb="tab-list"] {
        background-color: var(--r2p-navy);
        padding: 10px;
        border-radius: 50px;
        justify-content: center;
        gap: 30px;
        margin-bottom: 25px;
        border: 1px solid rgba(124, 255, 1, 0.1);
    }
    .stTabs [data-baseweb="tab"] { color: #888 !important; font-weight: bold; border: none !important; }
    .stTabs [aria-selected="true"] { 
        color: var(--r2p-green) !important; 
        background: rgba(124, 255, 1, 0.05) !important;
        border-radius: 25px;
    }

    /* Cards */
    .field-card {
        background: var(--r2p-navy);
        border-radius: 24px;
        overflow: hidden;
        margin-bottom: 30px;
        border: 1px solid rgba(255,255,255,0.05);
        transition: 0.3s;
        min-height: 320px;
    }
    .field-card:hover { border-color: var(--r2p-green); }

    .social-card {
        background: linear-gradient(135deg, var(--r2p-navy) 0%, #003366 100%);
        padding: 20px;
        border-radius: 25px;
        border-left: 5px solid var(--r2p-green);
        margin-bottom: 15px;
    }

    /* Chat Items */
    .chat-item {
        display: flex;
        padding: 15px;
        background: rgba(255,255,255,0.03);
        border-radius: 15px;
        margin-bottom: 10px;
        align-items: center;
    }
    .chat-avatar {
        width: 45px; height: 45px;
        background: var(--r2p-green);
        border-radius: 50%;
        margin-right: 15px;
        display: flex; align-items: center; justify-content: center;
        color: var(--r2p-dark);
        font-weight: bold;
    }

    /* Bottoni */
    .stButton>button {
        background-color: var(--r2p-green) !important;
        color: var(--r2p-dark) !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        border: none !important;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---

# 1. Funzione rapida per leggere l'immagine locale
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

_image_uri_cache = {}

def get_image_uri(image_path):
    if image_path not in _image_uri_cache:
        mime_type, _ = mimetypes.guess_type(image_path)
        if not mime_type:
            mime_type = "image/png"
        _image_uri_cache[image_path] = f"data:{mime_type};base64,{get_base64(image_path)}"
    return _image_uri_cache[image_path]

# Carica l'immagine (assicurati che il nome file sia corretto)
try:
    img_base64 = get_base64("logo_r2p.png")
    
    # 2. Mostra l'Header con il tuo stile
    col_img, col_header = st.columns([1, 4], gap="small")
    with col_img:
        st.markdown(f"""
        <div style="background: white; padding: 10px; border-radius: 15px; box-shadow: 0px 4px 10px rgba(0,0,0,0.1); width: fit-content; margin-bottom: 20px;">
            <img src="data:image/png;base64,{img_base64}" width="80">
        </div>
        """, unsafe_allow_html=True)
    with col_header:
        # Mostra il saldo con il pulsante + letteralmente accanto
        col_balance, col_plus = st.columns([0.8, 0.5])
        with col_balance:
            st.markdown(f"""
            <div style="display:flex; flex-direction:column; justify-content:center; margin-bottom: 20px;">
                <h1 style='margin:0; font-size: 2.5em; color: white; font-family: sans-serif;'>READY2PLAY</h1>
                <span style='color:#7CFF01; font-size:0.95em;'>Saldo: €{st.session_state.balance:.2f}</span>
            </div>
            """, unsafe_allow_html=True)
        with col_plus:
            if st.button("RICARICA SALDO +", key="show_reload_plus", help="Mostra il selettore per ricaricare il saldo"):
                st.session_state.show_reload_input = not st.session_state.show_reload_input

    if st.session_state.show_reload_input:
        amount = st.number_input("Importo da ricaricare", min_value=1.00, max_value=500.00, value=20.00, step=5.00, format="%.2f", key="reload_amount")
        if st.button("Ricarica saldo", key="reload_balance"):
            if amount > 0:
                st.session_state.balance += float(amount)
                st.success(f"Saldo ricaricato di €{amount:.2f}!")
                time.sleep(1)
                st.rerun()
            else:
                st.warning("Inserisci un importo valido maggiore di 0.")

except FileNotFoundError:
    st.error("Errore: Il file 'logo_r2p.png' non è stato trovato nella cartella del progetto.")


# --- NAVIGATION ---
tabs = st.tabs(["🏠 HOME", "🔍 RICERCA", "👥 SOCIAL", "💬 CHAT", "📅 PRENOTAZIONI", "⚡ SMART ACCESS"])

# --- TAB 1: HOME (Più consigliati) ---
with tabs[0]:
    st.markdown("### ✨ Campi Consigliati")
    campi = [
        {"n": "Fermi Soccer Arena", "s": "Calcio a 5", "d": "1.2 km", "r": "4.8", "img": "calcio.jpg"},
        {"n": "Padel Hub Brindisi", "s": "Padel", "d": "0.5 km", "r": "4.9", "img": "padel.jpg"},
        {"n": "Basket Park", "s": "Basket", "d": "2.1 km", "r": "4.7", "img": "basket.jpg"},
        {"n": "Tennis Fermi Club", "s": "Tennis", "d": "1.8 km", "r": "4.6", "img": "tennis.jpg"}
    ]
    for c in campi:
        # Rendering della card
        st.markdown(f"""
        <div class="field-card">
            <img src="{get_image_uri(c['img'])}" style="width:100%; height:240px; object-fit:cover;">
            <div style="padding:15px;">
                <span style="float:right; color:#7CFF01;">★ {c['r']}</span>
                <b style="font-size:1.1em;">{c['n']}</b><br>
                <small style="color:#888;">{c['s']} • 📍 {c['d']}</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Bottone per attivare la prenotazione
        if st.button(f"Prenota", key=f"btn_{c['n']}"):
            st.session_state.booking_target = c['n']
            st.rerun()

        # Il menu appare QUI, solo sotto la card corrispondente
        if st.session_state.booking_target == c['n']:
            st.markdown(f'<div class="booking-panel">', unsafe_allow_html=True)
            st.subheader(f"Prenota: {c['n']}")
            
            col_d, col_t = st.columns(2)
            data = col_d.date_input("Data", key=f"date_val_{c['n']}")
            ora = col_t.time_input("Orario", key=f"time_val_{c['n']}")
            persone = st.number_input("Persone", min_value=1, max_value=10, value=1, key=f"people_{c['n']}")
            prezzo = st.session_state.price_per_person
            totale = persone * prezzo
            st.markdown(f"<div style='margin-bottom:12px; color:#7CFF01;'><small>Prezzo: €{prezzo:.2f} a persona · Totale: €{totale:.2f}</small></div>", unsafe_allow_html=True)
            
            c_conf, c_ann = st.columns(2)
            if st.session_state.balance >= totale:
                if c_conf.button("CONFERMA E PAGA", key=f"conf_btn_{c['n']}"):
                    st.session_state.balance -= totale
                    st.session_state.bookings.append({"campo": c['n'], "data": data, "ora": ora, "people": persone, "price_per_person": prezzo, "total": totale})
                    st.success(f"Prenotazione confermata per {c['n']} il {data.strftime('%d/%m/%Y')} alle {ora.strftime('%H:%M')} per {persone} persone. Totale: €{totale:.2f}")
                    st.balloons()
                    time.sleep(1)
                    st.session_state.booking_target = None
                    st.rerun()
            else:
                st.error(f"Saldo insufficiente! Hai €{st.session_state.balance:.2f} ma servono €{totale:.2f}")
                c_conf.button("SALDO INSUFFICIENTE", key=f"conf_btn_{c['n']}", disabled=True)
            
            if c_ann.button("ANNULLA", key=f"ann_btn_{c['n']}"):
                st.session_state.booking_target = None
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)


# --- TAB 2: RICERCA (Ripristinata con Filtri) ---
with tabs[1]:
    st.markdown("### 🔍 Trova il tuo campo")
    sport = st.selectbox("Seleziona Sport", ["Tutti", "Calcio", "Padel", "Basket", "Tennis"])
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        distanza = st.slider("Distanza massima (km)", 1, 50, 15)
        data = st.date_input("Data")
    with col_f2:
        ora = st.time_input("Ora partita")
    
    if st.button("APPLICA FILTRI E CERCA"):
        st.markdown("---")
        st.markdown("#### Risultati della ricerca")
        # Filtra i risultati in base ai filtri
        risultati = []
        for c in campi:
            # Filtro sport
            if sport != "Tutti" and sport not in c['s']:
                continue
            # Filtro distanza
            dist_num = float(c['d'].split()[0])
            if dist_num > distanza:
                continue
            risultati.append(c)
        
        st.session_state.search_results = risultati
    
    # Mostra i risultati se presenti
    if st.session_state.search_results:
        if not st.session_state.search_results:
            st.write("Nessun campo trovato con i filtri selezionati.")
        else:
            for c in st.session_state.search_results:
                st.markdown(f"""
                <div class="field-card">
                    <img src="{get_image_uri(c['img'])}" style="width:100%; height:240px; object-fit:cover;">
                    <div style="padding:15px;">
                        <span style="float:right; color:#7CFF01;">★ {c['r']}</span>
                        <b style="font-size:1.1em;">{c['n']}</b><br>
                        <small style="color:#888;">{c['s']} • 📍 {c['d']}</small>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Prenota", key=f"search_btn_{c['n']}"):
                    st.session_state.booking_target = c['n']
                    st.rerun()

                if st.session_state.booking_target == c['n']:
                    st.markdown(f'<div class="booking-panel">', unsafe_allow_html=True)
                    st.subheader(f"Prenota: {c['n']}")
                    
                    col_d, col_t = st.columns(2)
                    data = col_d.date_input("Data", key=f"search_date_val_{c['n']}")
                    ora = col_t.time_input("Orario", key=f"search_time_val_{c['n']}")
                    persone = st.number_input("Persone", min_value=1, max_value=10, value=1, key=f"search_people_{c['n']}")
                    prezzo = st.session_state.price_per_person
                    totale = persone * prezzo
                    st.markdown(f"<div style='margin-bottom:12px; color:#7CFF01;'><small>Prezzo: €{prezzo:.2f} a persona · Totale: €{totale:.2f}</small></div>", unsafe_allow_html=True)
                    
                    c_conf, c_ann = st.columns(2)
                    if st.session_state.balance >= totale:
                        if c_conf.button("CONFERMA E PAGA", key=f"search_conf_btn_{c['n']}"):
                            st.session_state.balance -= totale
                            st.session_state.bookings.append({"campo": c['n'], "data": data, "ora": ora, "people": persone, "price_per_person": prezzo, "total": totale})
                            st.success(f"Prenotazione confermata per {c['n']} il {data.strftime('%d/%m/%Y')} alle {ora.strftime('%H:%M')} per {persone} persone. Totale: €{totale:.2f}")
                            st.balloons()
                            time.sleep(1)
                            st.session_state.booking_target = None
                            st.rerun()
                    else:
                        st.error(f"Saldo insufficiente! Hai €{st.session_state.balance:.2f} ma servono €{totale:.2f}")
                        c_conf.button("SALDO INSUFFICIENTE", key=f"search_conf_btn_{c['n']}", disabled=True)
                    
                    if c_ann.button("ANNULLA", key=f"search_ann_btn_{c['n']}"):
                        st.session_state.booking_target = None
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
        

# --- TAB 3: SOCIAL (Gestione Inviti e Unione) ---
with tabs[2]:
    st.markdown("### 🤝 Social Matchmaking")
    
    # Sezione Inviti
    st.markdown("#### I tuoi inviti")
    if st.session_state.invite_status == "pending":
        st.markdown("""
        <div class="social-card">
            <b>Invito da: Diego Candita</b><br>
            <span>Match: Calcetto 5vs5</span><br>
            <small>📍 Fermi Arena | 🕒 Oggi, 18:00</small>
        </div>
        """, unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        if c1.button("✅ ACCETTA"):
            st.session_state.invite_status = "accepted"
            st.session_state.accepted_invite = {
                "campo": "Fermi Arena",
                "data": datetime.date.today(),
                "ora": datetime.time(hour=18, minute=0)
            }
            st.rerun()
        if c2.button("❌ RIFIUTA"):
            st.session_state.invite_status = "declined"
            st.session_state.accepted_invite = None
            st.rerun()
    elif st.session_state.invite_status == "accepted":
        st.success("Sei in squadra per il match di oggi!")
        if st.button("Abbandona Match"):
            st.session_state.invite_status = "pending"
            st.session_state.accepted_invite = None
            st.rerun()
    
    # Sezione Unione
    st.markdown("#### Unisciti a una partita")
    partite = [
        {"name": "Padel Double", "host": "Jacopo P.", "spots": 1, "ora": datetime.time(hour=18, minute=30)},
        {"name": "Basket 3vs3", "host": "Francesca L.", "spots": 3, "ora": datetime.time(hour=20, minute=0)}
    ]
    for partita in partite:
        joined = partita["name"] in st.session_state.joined_matches
        remaining = max(0, partita["spots"] - (1 if joined else 0))
        if remaining == 1:
            status_text = f"{remaining} posto disponibile"
        else:
            status_text = f"{remaining} posti disponibili"
        status_label = "<span style='color:#7CFF01; font-weight:bold;'>Sei dentro</span>" if joined else f"<span style='color:#7CFF01; font-weight:bold;'>{status_text}</span>"

        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.03); padding:15px; border-radius:15px; margin-bottom:10px; display:flex; justify-content:space-between; align-items:center;">
            <div><b>{partita['name']}</b><br><small>Host: {partita['host']} • Ora: {partita['ora'].strftime('%H:%M')}</small></div>
            <div>{status_label}</div>
        </div>
        """, unsafe_allow_html=True)

        if not joined:
            if st.button(f"Unisciti a {partita['name']}", key=f"join_{partita['name']}"):
                st.session_state.joined_matches.append(partita['name'])
                st.session_state.bookings.append({
                    "campo": partita['name'],
                    "data": datetime.date.today(),
                    "ora": partita['ora'],
                    "source": "social"
                })
                st.success(f"Sei entrato in {partita['name']} alle {partita['ora'].strftime('%H:%M')}!")
                st.rerun()

# --- TAB 4: CHAT (Ripristinato) ---
with tabs[3]:
    st.markdown("### 💬 Messaggi")
    messaggi = [
        ("DC", "Diego Candita", "Ci sei per il calcetto?"),
        ("FL", "Francesca Lecci", "Prenotazione confermata!"),
        ("JP", "Jacopo Pomes", "Manca solo il quarto per il padel.")
    ]
    for init, user, msg in messaggi:
        st.markdown(f"""
        <div class="chat-item">
            <div class="chat-avatar">{init}</div>
            <div>
                <b>{user}</b><br>
                <small style="color:#888;">{msg}</small>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- TAB 4: PRENOTAZIONI ---
with tabs[4]:
    st.markdown("### 📅 Le tue prenotazioni")
    show_bookings = list(st.session_state.bookings)
    if st.session_state.accepted_invite:
        show_bookings.insert(0, st.session_state.accepted_invite)

    if show_bookings:
        for b in show_bookings:
            is_accepted = (
                st.session_state.accepted_invite is not None
                and b['campo'] == st.session_state.accepted_invite['campo']
                and b['data'] == st.session_state.accepted_invite['data']
                and b['ora'] == st.session_state.accepted_invite['ora']
            )
            booking_key = f"{b['campo']}_{b['data'].strftime('%Y%m%d')}_{b['ora'].strftime('%H%M')}"
            is_social_join = b.get('source') == 'social'
            status_label = ""
            if is_accepted:
                status_label = "<span style='color:#7CFF01; font-weight:bold;'>Invito accettato</span>"
            elif is_social_join:
                status_label = "<span style='color:#7CFF01; font-weight:bold;'>Unito da Social</span>"
            booking_details = ""
            if 'people' in b and 'total' in b:
                booking_details = f"<br><small>{b['people']} persone • Totale: €{b['total']:.2f}</small>"
            st.markdown(f"""
            <div style="background: var(--r2p-navy); padding: 15px; border-radius: 15px; margin-bottom: 10px; border-left: 5px solid var(--r2p-green);">
                <b>{b['campo']}</b><br>
                <small>Data: {b['data'].strftime('%d/%m/%Y')} | Ora: {b['ora'].strftime('%H:%M')}</small>{booking_details}<br>
                {status_label}
            </div>
            """, unsafe_allow_html=True)

            is_social_join = b.get('source') == 'social'
            if not is_accepted and not is_social_join:
                booking_key = f"{b['campo']}_{b['data'].strftime('%Y%m%d')}_{b['ora'].strftime('%H%M')}"
                invite_col, _ = st.columns([1, 3])
                if invite_col.button("Invita +", key=f"invite_plus_{booking_key}"):
                    st.session_state.invite_booking = booking_key
                    st.rerun()

                if st.session_state.invite_booking == booking_key:
                    st.markdown(f'<div class="booking-panel">', unsafe_allow_html=True)
                    st.subheader(f"Invita persone a {b['campo']}")
                    name = st.text_input("Nome ospite", key=f"invite_name_{booking_key}")
                    if st.button("Invia invito", key=f"send_invite_{booking_key}"):
                        if name:
                            st.session_state.invited_people.setdefault(booking_key, []).append(name)
                            st.success(f"Invito inviato a {name}!")
                            st.session_state.invite_booking = None
                            st.rerun()
                        else:
                            st.warning("Inserisci un nome prima di inviare l'invito.")
                    if st.button("Chiudi", key=f"close_invite_{booking_key}"):
                        st.session_state.invite_booking = None
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
            elif is_accepted:
                st.markdown("<div style='padding-left:10px; margin-bottom:10px; color:#AAAAAA;'><small>Non è possibile invitare altri partecipanti su una partita accettata.</small></div>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='padding-left:10px; margin-bottom:10px; color:#AAAAAA;'><small>Non è possibile invitare altri partecipanti su una partita unita da Social.</small></div>", unsafe_allow_html=True)

            if booking_key in st.session_state.invited_people:
                invited_list = st.session_state.invited_people[booking_key]
                st.markdown(f"<div style='padding-left:10px; margin-bottom:15px; color:#7CFF01;'><small>Invitati: {', '.join(invited_list)}</small></div>", unsafe_allow_html=True)
    else:
        st.write("Nessuna prenotazione effettuata.")

# --- TAB 5: SMART ACCESS ---
with tabs[5]:
    st.markdown("### ⚡ Controllo IoT")
    if not st.session_state.bookings:
        st.warning("Nessuna prenotazione disponibile per lo Smart Access.")
    else:
        tz_italy = pytz.timezone('Europe/Rome')
        now = datetime.datetime.now(tz_italy)
        eligible_bookings = []
        for b in st.session_state.bookings:
            match_start = tz_italy.localize(datetime.datetime.combine(b['data'], b['ora']))
            if now <= match_start <= now + datetime.timedelta(minutes=30):
                eligible_bookings.append((b, match_start))

        if not eligible_bookings:
            st.warning("Nessuna partita con inizio entro 30 minuti.")
        else:
            st.info("Seleziona la prenotazione da sbloccare entro 30 minuti dall'inizio.")
            options = [f"{b['campo']} - {match_start.strftime('%d/%m %H:%M')}" for b, match_start in eligible_bookings]
            selected_option = st.selectbox("Seleziona la prenotazione", options, key="smart_access_select")
            if st.button("SBLOCCA E ACCENDI LUCI"):
                st.session_state.smart_access_target = selected_option
                with st.spinner("Invio segnale IoT..."):
                    time.sleep(1.5)
                    st.success(f"{selected_option} sbloccata con successo!")
                    st.balloons()


