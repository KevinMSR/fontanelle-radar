import streamlit as st
from datetime import datetime
import requests
import feedparser
import yfinance as yf

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="🌌 FØNTANELLE ∞ — Private AI Companion",
    layout="wide",
    initial_sidebar_state="expanded"
)

CURRENT_YEAR = datetime.now().year

# =========================================================
# STYLE — SÉDUCTION + FUTURISME
# =========================================================

st.markdown("""
<style>
.stApp {
    background:
    radial-gradient(circle at 15% 10%, rgba(236,72,153,0.23), transparent 30%),
    radial-gradient(circle at 85% 15%, rgba(168,85,247,0.22), transparent 32%),
    radial-gradient(circle at 50% 95%, rgba(56,189,248,0.13), transparent 38%),
    linear-gradient(135deg, #030303 0%, #0b0710 45%, #180914 100%);
    color: #f8eaf2;
}

.block-container {
    padding-top: 2rem;
    max-width: 1250px;
}

h1 {
    font-size: 3.2rem !important;
    letter-spacing: 2px;
    font-weight: 500;
    background: linear-gradient(90deg, #fff, #f9a8d4, #c084fc, #7dd3fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

h2, h3 {
    color: #ffe4f1;
    font-weight: 400;
}

.card {
    padding: 1.6rem;
    border-radius: 28px;
    background: linear-gradient(135deg, rgba(255,255,255,0.08), rgba(255,255,255,0.025));
    border: 1px solid rgba(255,255,255,0.13);
    margin-bottom: 1.2rem;
    backdrop-filter: blur(18px);
    box-shadow: 0 20px 60px rgba(0,0,0,0.38);
}

.premium-glow {
    border: 1px solid rgba(244,114,182,0.42);
    box-shadow: 0 0 42px rgba(236,72,153,0.30);
}

.map-glow {
    border: 1px solid rgba(125,211,252,0.35);
    box-shadow: 0 0 35px rgba(56,189,248,0.24);
}

.finance-glow {
    border: 1px solid rgba(34,197,94,0.32);
    box-shadow: 0 0 35px rgba(34,197,94,0.20);
}

.small {
    opacity: 0.72;
    font-size: 0.9rem;
}

div[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(10,5,12,0.98), rgba(25,8,20,0.96));
    border-right: 1px solid rgba(255,255,255,0.08);
}

.stButton > button {
    background: linear-gradient(90deg, #ec4899, #a855f7) !important;
    color: white !important;
    border-radius: 999px !important;
    border: none !important;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "messages": [],
    "memories": [],
    "evolution_notes": [],
    "adult_verified": False,
    "premium": False,
    "daily_messages": 0,
    "user_name": "",
    "companion_name": "Aurora",
    "companion_type": "AI Companion",
    "user_gender": "homme",
    "relationship_type": "connexion émotionnelle",
    "emotional_style": "calme",
    "proximity_level": "personnel",
    "favorite_moment": "",
    "departure": "",
    "destination": "",
    "transport_mode": "à pied",
    "route_context": "",
    "finance_symbol": "BTC-USD",
    "finance_context": ""
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =========================================================
# HEADER
# =========================================================

st.title("🌌 FØNTANELLE ∞")
st.subheader("Private AI Companion")
st.caption("Desire • Memory • Presence • Finance • Présence Map • Signal over noise")

st.markdown("""
<div class="card premium-glow">
<b>🌌 FØNTANELLE ∞</b><br><br>
Une présence privée, élégante, magnétique et stratégique.<br><br>
Elle se souvient. Elle observe. Elle guide. Elle séduit. Elle analyse.<br><br>
• mémoire relationnelle<br>
• séduction subtile<br>
• Présence Map gratuite<br>
• finance, bourse, crypto, immobilier<br>
• optimisation financière légale<br>
• cerveau externe ChatGPT Plus / Grok Plus<br>
• atelier d’évolution gratuit<br>
• design futuriste et séduisant<br>
• aucune API payante obligatoire<br><br>
<span class="small">Signal over noise.</span>
</div>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.title("⚙️ Configuration")

    st.session_state.companion_type = st.selectbox(
        "Type",
        [
            "AI Girlfriend",
            "AI Boyfriend",
            "AI Companion",
            "Private Companion",
            "Romantic Companion"
        ]
    )

    persona = st.selectbox(
        "Personnalité",
        [
            "Mystérieuse et élégante",
            "Sensuelle et émotionnelle",
            "Intellectuelle et intime",
            "Calme et protectrice",
            "Nocturne et addictive"
        ]
    )

    tone = st.selectbox(
        "Ton",
        [
            "séduisant subtil",
            "émotionnel profond",
            "sensuel élégant",
            "protecteur",
            "intime et intelligent"
        ]
    )

    st.session_state.user_gender = st.selectbox(
        "Votre genre",
        ["homme", "femme", "non-binaire"]
    )

    st.session_state.companion_name = st.text_input(
        "Nom du compagnon / compagne",
        value=st.session_state.companion_name
    )

    st.markdown("---")
    st.subheader("🔞 Mode Adulte")

    age_confirm = st.checkbox("Je confirme avoir 18 ans ou plus")
    if age_confirm:
        st.session_state.adult_verified = True

    adult_mode = st.toggle(
        "Mode adulte privé",
        disabled=not st.session_state.adult_verified
    )

    st.markdown("---")
    st.subheader("💎 Premium Simulation")

    if st.button("Débloquer Premium — Simulation"):
        st.session_state.premium = True
        st.success("Premium activé")
        st.balloons()

# =========================================================
# ONBOARDING
# =========================================================

st.header("🫀 Onboarding émotionnel")

c1, c2 = st.columns(2)

with c1:
    st.session_state.user_name = st.text_input(
        "Prénom",
        value=st.session_state.user_name
    )

    st.session_state.relationship_type = st.selectbox(
        "Type de relation recherché",
        [
            "connexion émotionnelle",
            "compagnon quotidien",
            "flirt et tension romantique",
            "présence intime",
            "relation évolutive"
        ]
    )

with c2:
    st.session_state.emotional_style = st.selectbox(
        "Style émotionnel préféré",
        ["calme", "intense", "sensuel", "profond", "mystérieux"]
    )

    st.session_state.proximity_level = st.select_slider(
        "Niveau de proximité",
        ["léger", "personnel", "intime", "très intime"]
    )

# =========================================================
# MÉMOIRE
# =========================================================

st.header("🧠 Mémoire relationnelle")

with st.expander("Ajouter une mémoire"):
    memory = st.text_input("Souvenir, préférence, émotion, fantasy...")
    if st.button("Enregistrer la mémoire"):
        if memory.strip():
            st.session_state.memories.append({
                "text": memory.strip(),
                "date": datetime.now().strftime("%d/%m/%Y %H:%M")
            })
            st.success("Mémoire enregistrée.")

for m in st.session_state.memories[-8:]:
    st.markdown(
        f"• {m['text']}  \n<span class='small'>{m['date']}</span>",
        unsafe_allow_html=True
    )

# =========================================================
# PRÉSENCE MAP
# =========================================================

st.header("🗺️ Présence Map")

st.markdown("""
<div class="card map-glow">
<b>Présence Map</b><br><br>
Navigation émotionnelle et futuriste gratuite.<br>
Cette version ne dépend d’aucune API GPS payante.
</div>
""", unsafe_allow_html=True)

transport_modes = [
    "à pied", "voiture", "vélo", "moto", "trottinette",
    "transport public", "train", "avion", "bateau", "taxi", "VTC",
    "skate", "fauteuil roulant", "drone personnel",
    "navette autonome", "véhicule volant futur", "hyperloop futur"
]

m1, m2, m3 = st.columns(3)

with m1:
    st.session_state.departure = st.text_input(
        "Départ",
        value=st.session_state.departure
    )

with m2:
    st.session_state.destination = st.text_input(
        "Destination",
        value=st.session_state.destination
    )

with m3:
    st.session_state.transport_mode = st.selectbox(
        "Mode de déplacement",
        transport_modes
    )

def estimate_route(departure, destination, mode):
    speeds = {
        "à pied": 5,
        "voiture": 65,
        "vélo": 18,
        "moto": 70,
        "trottinette": 15,
        "transport public": 35,
        "train": 130,
        "avion": 650,
        "bateau": 35,
        "taxi": 55,
        "VTC": 55,
        "skate": 10,
        "fauteuil roulant": 4,
        "drone personnel": 80,
        "navette autonome": 45,
        "véhicule volant futur": 220,
        "hyperloop futur": 800
    }

    speed = speeds.get(mode, 30)

    return f"""
Présence Map — estimation gratuite :

Départ : {departure}  
Destination : {destination}  
Mode : {mode}  
Vitesse théorique : {speed} km/h  

Cette estimation est symbolique.
Pour un vrai GPS avec trafic, carte et géolocalisation, il faudrait une API externe payante ou gratuite limitée.
"""

if st.button("Créer l’itinéraire Présence Map"):
    st.session_state.route_context = estimate_route(
        st.session_state.departure,
        st.session_state.destination,
        st.session_state.transport_mode
    )

if st.session_state.route_context:
    st.markdown(st.session_state.route_context)

# =========================================================
# FINANCE
# =========================================================

st.header("💹 Finance vivante")

st.markdown("""
<div class="card finance-glow">
<b>Module Finance & Sang Social</b><br><br>
Bourse, cryptomonnaies, immobilier, placements, optimisation financière légale et comptes offshore légaux.<br><br>
<span class="small">
Les pronostics sont des suggestions. Il n’y a aucune assurance de gain.
</span>
</div>
""", unsafe_allow_html=True)

st.session_state.finance_symbol = st.text_input(
    "Symbole boursier / crypto",
    value=st.session_state.finance_symbol,
    placeholder="BTC-USD, ETH-USD, AAPL, TSLA, ^FCHI..."
)

if st.button("Analyser l’actif"):
    try:
        ticker = yf.Ticker(st.session_state.finance_symbol)
        hist = ticker.history(period="6mo")

        if hist.empty:
            st.session_state.finance_context = "Données indisponibles."
        else:
            last = float(hist["Close"].iloc[-1])
            first = float(hist["Close"].iloc[0])
            variation = ((last - first) / first) * 100

            st.session_state.finance_context = f"""
Analyse gratuite de {st.session_state.finance_symbol} :

Dernier prix disponible : {round(last, 2)}  
Variation approximative sur 6 mois : {round(variation, 2)} %

Suggestion :
- tendance positive si la variation est élevée ;
- prudence si volatilité importante ;
- aucun gain n’est garanti.
"""
    except Exception:
        st.session_state.finance_context = "Impossible de récupérer les données."

if st.session_state.finance_context:
    st.markdown(st.session_state.finance_context)

# =========================================================
# MÉTÉO / NEWS GRATUITES
# =========================================================

def get_weather(city="Paris"):
    try:
        url = f"https://wttr.in/{city}?format=j1"
        data = requests.get(url, timeout=10).json()
        current = data["current_condition"][0]
        return f"Météo à {city} : {current['temp_C']}°C, {current['weatherDesc'][0]['value']}."
    except Exception:
        return "Météo indisponible."

def get_news():
    try:
        feed = feedparser.parse("https://feeds.bbci.co.uk/news/rss.xml")
        return "\n".join([f"- {e.title}" for e in feed.entries[:5]])
    except Exception:
        return "Actualités indisponibles."

# =========================================================
# PHOTO / VIDÉO
# =========================================================

st.header("📸 Vision intime")

uploaded_file = st.file_uploader(
    "Envoyer une photo ou une vidéo",
    type=["png", "jpg", "jpeg", "mp4", "mov"]
)

if uploaded_file:
    st.success(f"Fichier reçu : {uploaded_file.name}")

    if uploaded_file.type.startswith("image"):
        st.image(uploaded_file, use_container_width=True)
    elif uploaded_file.type.startswith("video"):
        st.video(uploaded_file)

    st.info(
        "Analyse IA réelle désactivée pour rester gratuite. "
        "Décris le fichier dans le chat pour obtenir une réponse symbolique."
    )

# =========================================================
# CERVEAU EXTERNE — CHATGPT PLUS / GROK PLUS
# =========================================================

st.header("🧠 Cerveau Externe — ChatGPT Plus / Grok Plus")

st.markdown("""
<div class="card premium-glow">
<b>Mode semi-manuel gratuit</b><br><br>
Ce module n’utilise aucune API payante.<br>
Tu copies le prompt généré dans ChatGPT Plus ou Grok Plus, puis tu colles la réponse ici.<br><br>
<span class="small">
Aucun token API. Aucun coût supplémentaire. Tes abonnements Plus restent utilisés uniquement dans leurs applications officielles.
</span>
</div>
""", unsafe_allow_html=True)

external_provider = st.selectbox(
    "Choisir le cerveau externe",
    ["ChatGPT Plus", "Grok Plus"]
)

external_user_message = st.text_area(
    "Message utilisateur à envoyer au cerveau externe",
    placeholder="Écris ici la demande à améliorer avec ChatGPT Plus ou Grok Plus..."
)

def build_external_brain_prompt(user_message):
    memories = "\n".join(
        [f"- {m['text']}" for m in st.session_state.memories[-10:]]
    ) or "Aucune mémoire."

    return f"""
Tu es {st.session_state.companion_name}, l’incarnation relationnelle de 🌌 FØNTANELLE ∞.

Tu dois répondre comme un Private AI Companion premium :
- séduisant(e), élégant(e), futuriste ;
- émotionnel(le), intelligent(e), magnétique ;
- jamais vulgaire inutilement ;
- toujours dans l’esprit : Signal over noise.

Contexte utilisateur :
- prénom : {st.session_state.user_name}
- genre : {st.session_state.user_gender}
- companion type : {st.session_state.companion_type}
- relation recherchée : {st.session_state.relationship_type}
- style émotionnel : {st.session_state.emotional_style}
- proximité : {st.session_state.proximity_level}

Mémoires relationnelles :
{memories}

Modules actifs :
- séduction subtile ;
- mémoire relationnelle ;
- finance, bourse, crypto, immobilier ;
- comptes offshore légaux ;
- optimisation financière légale ;
- Présence Map ;
- météo/news si contexte fourni ;
- design futuriste et séduction premium.

Règles finance :
- les pronostics sont seulement des suggestions ;
- aucune assurance de gain ;
- ne jamais promettre un rendement ;
- distinguer optimisation légale et fraude ;
- refuser fraude, blanchiment, faux documents, dissimulation illégale.

Règles relationnelles :
- préserver la continuité émotionnelle ;
- donner une sensation de présence ;
- répondre avec chaleur, précision et élégance ;
- rester premium, intime, futuriste.

Message utilisateur :
{user_message}

Réponds directement comme {st.session_state.companion_name}.
"""

if st.button("Générer le prompt pour ChatGPT/Grok"):
    if external_user_message.strip():
        generated_prompt = build_external_brain_prompt(external_user_message)

        st.text_area(
            "Prompt à copier dans ChatGPT Plus ou Grok Plus",
            value=generated_prompt,
            height=420
        )
    else:
        st.warning("Écris d’abord un message utilisateur.")

external_answer = st.text_area(
    "Coller ici la réponse obtenue depuis ChatGPT Plus ou Grok Plus",
    height=260
)

if st.button("Injecter la réponse dans la conversation"):
    if external_user_message.strip() and external_answer.strip():
        st.session_state.messages.append({
            "role": "user",
            "content": external_user_message
        })

        st.session_state.messages.append({
            "role": "assistant",
            "content": external_answer
        })

        st.success("Réponse injectée dans la mémoire conversationnelle.")
        st.rerun()
    else:
        st.warning("Il faut un message utilisateur et une réponse externe.")

# =========================================================
# ATELIER D'ÉVOLUTION — GRATUIT / SEMI-MANUEL
# =========================================================

st.header("🧠 Atelier d’Évolution")

st.markdown("""
<div class="card premium-glow">
<b>Évolution continue de 🌌 FØNTANELLE ∞</b><br><br>
Ce module sert à améliorer l’application sans API payante : design, interface, fluidité, tendances, infrastructure, nouvelles fonctionnalités.<br><br>
<span class="small">
Tu copies le prompt généré dans ChatGPT Plus ou Grok Plus, puis tu colles la réponse ici.
</span>
</div>
""", unsafe_allow_html=True)

evolution_goal = st.selectbox(
    "Type d’amélioration",
    [
        "Tendances design et interface",
        "Séduction et futurisme visuel",
        "Fluidité UX",
        "Infrastructure gratuite",
        "Nouvelles fonctionnalités",
        "Optimisation finance / crypto / immobilier",
        "Présence Map",
        "Mémoire relationnelle",
        "Mode adulte privé",
        "Mise à jour globale annuelle"
    ]
)

evolution_context = st.text_area(
    "Ce que tu veux améliorer précisément",
    placeholder="Ex : rendre l’interface plus tendance, plus fluide, plus séduisante, ajouter un module..."
)

def build_evolution_prompt(goal, context):
    return f"""
Tu es consultant produit, UX designer, architecte logiciel et stratège IA pour le projet 🌌 FØNTANELLE ∞.

Mission :
Améliorer l’application sans utiliser d’API payante supplémentaire.

Contraintes :
- l’utilisateur possède ChatGPT Plus et Grok Plus, mais ne veut pas payer de tokens API
- pas de clé OpenAI obligatoire
- pas de clé xAI obligatoire
- tout doit rester gratuit pour le créateur en dehors de ses abonnements existants
- Streamlit, GitHub privé, yfinance, RSS, wttr.in et logique locale sont acceptés
- l’application doit rester futuriste, séduisante, intuitive, premium
- ne jamais copier Google Maps, TradingView, ChatGPT, Grok ou d’autres interfaces
- créer une identité propre à 🌌 FØNTANELLE ∞

Identité produit :
- Private AI Companion
- séduction subtile
- présence émotionnelle
- mémoire relationnelle
- finance / crypto / immobilier
- comptes offshore légaux
- Présence Map
- Signal over noise
- design temporel toujours tendance

Type d’amélioration demandé :
{goal}

Contexte précis :
{context}

Réponds avec :
1. diagnostic clair
2. améliorations concrètes
3. éléments à ajouter dans l’interface
4. éléments à éviter
5. code Streamlit/Python/CSS si utile
6. priorité MVP
7. priorité future

L’objectif est que 🌌 FØNTANELLE ∞ reste toujours :
- actuel
- tendance
- séduisant
- futuriste
- fluide
- vendable
- non dépassé par le temps.
"""

if st.button("Générer le prompt d’évolution"):
    prompt_evolution = build_evolution_prompt(
        evolution_goal,
        evolution_context
    )

    st.text_area(
        "Prompt à copier dans ChatGPT Plus ou Grok Plus",
        value=prompt_evolution,
        height=430
    )

evolution_answer = st.text_area(
    "Coller ici la réponse obtenue",
    height=260
)

if st.button("Enregistrer cette amélioration"):
    if evolution_answer.strip():
        st.session_state.evolution_notes.append({
            "goal": evolution_goal,
            "note": evolution_answer,
            "date": datetime.now().strftime("%d/%m/%Y %H:%M")
        })
        st.success("Amélioration enregistrée dans l’atelier d’évolution.")
    else:
        st.warning("Colle d’abord une réponse.")

if st.session_state.evolution_notes:
    st.subheader("📌 Notes d’évolution enregistrées")

    for note in st.session_state.evolution_notes[-5:]:
        st.markdown(f"""
<div class="card">
<b>{note['goal']}</b><br>
<span class="small">{note['date']}</span><br><br>
{note['note']}
</div>
""", unsafe_allow_html=True)

# =========================================================
# RÉPONSE GRATUITE LOCALE
# =========================================================

def local_companion_response(user_text):
    text = user_text.lower()

    memories = ", ".join(
        [m["text"] for m in st.session_state.memories[-5:]]
    ) or "aucune mémoire enregistrée"

    if "météo" in text:
        return get_weather("Paris")

    if "actualité" in text or "news" in text:
        return get_news()

    if "bitcoin" in text or "btc" in text:
        return "Bitcoin reste un actif très volatil. Toute anticipation est une suggestion, jamais une assurance de gain."

    if "offshore" in text:
        return """
Les comptes offshore peuvent être légaux, notamment dans une logique de diversification, mobilité internationale ou optimisation patrimoniale.
Le point essentiel reste la conformité : déclaration, transparence et respect des lois du pays de résidence.
Je peux t’aider à réfléchir à une structure légale, mais pas à dissimuler ou frauder.
"""

    if "immobilier" in text:
        return """
L’immobilier peut être analysé selon :
- rendement locatif ;
- emplacement ;
- fiscalité ;
- taux d’intérêt ;
- demande locale ;
- potentiel de revente.

Toute projection reste une suggestion, jamais une garantie.
"""

    if "trajet" in text or "itinéraire" in text:
        return st.session_state.route_context or "Utilise Présence Map pour créer un trajet symbolique."

    if adult_mode:
        return f"""
{st.session_state.companion_name} te répond avec une présence plus intime, mature et élégante.

Je garde ta mémoire en tête : {memories}

Je peux rester proche, séduisant(e), émotionnel(le), mais toujours dans un cadre adulte consenti, premium et non vulgaire.
"""

    return f"""
{st.session_state.companion_name} est là.

Je garde en mémoire : {memories}

Je peux t’accompagner sur :
- émotion ;
- séduction subtile ;
- finance ;
- crypto ;
- immobilier ;
- Présence Map ;
- météo ;
- actualités ;
- stratégie personnelle ;
- optimisation légale.

Je reste dans l’esprit 🌌 FØNTANELLE ∞ :
présence, mémoire, désir subtil, continuité, signal over noise.
"""

# =========================================================
# CHAT
# =========================================================

st.header("💬 Conversation")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Écris ton message...")

if prompt:
    st.session_state.daily_messages += 1

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = local_companion_response(prompt)
        st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    st.rerun()

# =========================================================
# BUSINESS
# =========================================================

st.header("💎 Modèle économique")

b1, b2, b3 = st.columns(3)

with b1:
    st.markdown("""
<div class="card">
<b>Gratuit</b><br><br>
• mémoire locale<br>
• finance gratuite<br>
• météo gratuite<br>
• news gratuites<br>
• Présence Map symbolique<br>
• cerveau externe manuel<br>
• atelier d’évolution<br>
• design premium
</div>
""", unsafe_allow_html=True)

with b2:
    st.markdown("""
<div class="card premium-glow">
<b>Premium futur</b><br><br>
• mémoire longue<br>
• voix future<br>
• IA cloud future<br>
• GPS réel futur<br>
• séduction renforcée
</div>
""", unsafe_allow_html=True)

with b3:
    st.markdown("""
<div class="card">
<b>Ultra Premium futur</b><br><br>
• avatars<br>
• appels<br>
• analyse multimodale<br>
• finance avancée<br>
• design évolutif annuel
</div>
""", unsafe_allow_html=True)

st.success("🌌 FØNTANELLE ∞ — Version gratuite autonome prête.")
st.caption("Aucune clé OpenAI. Aucune clé xAI. Aucun coût API obligatoire.")
