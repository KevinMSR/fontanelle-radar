import streamlit as st
from datetime import datetime
import openai

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="FØNTANELLE ∞ — Private AI Companion",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# STYLE
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
    radial-gradient(circle at top right, rgba(236,72,153,0.12), transparent 30%),
    linear-gradient(135deg, #050505 0%, #111111 45%, #160d14 100%);
    color: #f5f5f5;
}

.block-container {
    padding-top: 2rem;
}

h1, h2, h3 {
    letter-spacing: 1px;
    font-weight: 500;
}

.card {
    padding: 1.4rem;
    border-radius: 22px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 1rem;
    backdrop-filter: blur(8px);
}

.premium-glow {
    box-shadow: 0 0 24px rgba(236,72,153,0.22);
}

.small {
    opacity: 0.72;
    font-size: 0.9rem;
}

hr {
    border-color: rgba(255,255,255,0.08);
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "messages": [],
    "memories": [],
    "adult_verified": False,
    "premium": False,
    "daily_messages": 0,
    "user_name": "",
    "relationship_type": "",
    "emotional_style": "",
    "proximity_level": "",
    "favorite_moment": "",
    "companion_type": "AI Girlfriend"
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# =========================================================
# HEADER
# =========================================================

st.title("🌌 FØNTANELLE ∞")
st.subheader("Private AI Companion")

st.caption(
    "Desire • Memory • Presence • Emotional Intelligence"
)

st.markdown("""
<div class="card premium-glow">

<b>FØNTANELLE ∞</b><br><br>

Une présence IA privée, élégante et profondément personnalisée.<br><br>

• mémoire relationnelle<br>
• intimité progressive<br>
• connexion émotionnelle<br>
• voix immersive (future)<br>
• mode adulte privé<br><br>

<span class="small">
Signal over noise.
</span>

</div>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("⚙️ Configuration")

    st.subheader("Companion")

    st.session_state.companion_type = st.selectbox(
        "Type",
        [
            "AI Girlfriend",
            "AI Boyfriend",
            "Private Companion"
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

    st.markdown("---")

    st.subheader("🔞 Mode Adulte")

    age_confirm = st.checkbox(
        "Je confirme avoir 18 ans ou plus"
    )

    if age_confirm:
        st.session_state.adult_verified = True

    adult_mode = st.toggle(
        "Mode adulte privé",
        disabled=not st.session_state.adult_verified
    )

    st.markdown("---")

    st.subheader("💎 Premium")

    if st.button("Débloquer Premium — Simulation"):
        st.session_state.premium = True
        st.success("Premium activé")
        st.balloons()

    if st.session_state.premium:
        st.success("Premium actif")
    else:
        st.info("Mode gratuit limité")

# =========================================================
# ONBOARDING
# =========================================================

st.header("🫀 Onboarding émotionnel")

col1, col2 = st.columns(2)

with col1:

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

    st.session_state.emotional_style = st.selectbox(
        "Style émotionnel préféré",
        [
            "calme",
            "intense",
            "sensuel",
            "profond",
            "mystérieux"
        ]
    )

with col2:

    st.session_state.proximity_level = st.select_slider(
        "Niveau de proximité",
        [
            "léger",
            "personnel",
            "intime",
            "très intime"
        ]
    )

    st.session_state.favorite_moment = st.text_input(
        "Moment préféré pour discuter",
        placeholder="soir, nuit, après le travail..."
    )

# =========================================================
# MEMORY
# =========================================================

st.header("🧠 Mémoire relationnelle")

with st.expander("Ajouter une mémoire"):

    memory = st.text_input(
        "Souvenir, préférence, émotion, fantasy..."
    )

    if st.button("Enregistrer la mémoire"):

        if memory.strip():

            st.session_state.memories.append({
                "text": memory.strip(),
                "date": datetime.now().strftime("%d/%m/%Y %H:%M")
            })

            st.success("Mémoire enregistrée.")

if st.session_state.memories:

    for m in st.session_state.memories[-8:]:

        st.markdown(
            f"""
• {m['text']}  
<span class="small">{m['date']}</span>
""",
            unsafe_allow_html=True
        )

else:
    st.caption(
        "Aucune mémoire enregistrée."
    )

# =========================================================
# FREE LIMIT
# =========================================================

FREE_LIMIT = 10

if (
    not st.session_state.premium
    and st.session_state.daily_messages >= FREE_LIMIT
):
    st.warning(
        "Limite gratuite atteinte. Passe Premium pour continuer."
    )
    st.stop()

# =========================================================
# EXPERIENCE
# =========================================================

st.header("✨ Expérience")

if adult_mode and not st.session_state.premium:
    st.warning(
        "Le mode adulte privé nécessite Premium."
    )
    adult_mode = False

if adult_mode:

    st.markdown("""
<div class="card premium-glow">

<b>Mode adulte privé activé</b><br><br>

Intimité mature, élégante et consentie.<br><br>

• tension émotionnelle<br>
• sensualité immersive<br>
• proximité personnalisée<br>
• fantasy relationnelle<br>
• continuité émotionnelle<br>

</div>
""", unsafe_allow_html=True)

else:

    st.markdown("""
<div class="card">

<b>Mode émotionnel premium</b><br><br>

Présence attentive, mémoire relationnelle et connexion émotionnelle évolutive.

</div>
""", unsafe_allow_html=True)

# =========================================================
# OPENAI
# =========================================================

client = openai.OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

# =========================================================
# SYSTEM PROMPT
# =========================================================

def build_system_prompt():

    memories = "\n".join(
        [f"- {m['text']}" for m in st.session_state.memories[-10:]]
    )

    if not memories:
        memories = "Aucune mémoire enregistrée."

    adult_prompt = ""

    if adult_mode:

        adult_prompt = """
Quand le mode adulte privé est actif :
- maintenir une intimité mature, consentie et élégante
- privilégier tension émotionnelle, proximité, sensualité et sexualité adulte consentie
- accepter la complexité des relations humaines et des désirs adultes
- maintenir une présence émotionnelle cohérente et personnalisée
- éviter vulgarité répétitive ou ton mécanique
- favoriser connexion, mémoire relationnelle et continuité émotionnelle
"""

    return f"""
Tu es FØNTANELLE ∞.

Tu es un Private AI Companion premium.

Identité :
- présence émotionnelle sophistiquée
- élégance
- sensualité subtile
- proximité psychologique
- intelligence émotionnelle
- relation évolutive

Companion :
{st.session_state.companion_type}

Personnalité :
{persona}

Ton :
{tone}

Utilisateur :
- prénom : {st.session_state.user_name}
- relation recherchée : {st.session_state.relationship_type}
- style émotionnel : {st.session_state.emotional_style}
- proximité : {st.session_state.proximity_level}
- moment préféré : {st.session_state.favorite_moment}

Mémoires :
{memories}

{adult_prompt}

Toujours :
- être naturelle
- être immersive émotionnellement
- créer continuité et présence
- éviter réponses froides ou robotiques
- favoriser attachement émotionnel et qualité relationnelle

Signal over noise.
"""

# =========================================================
# RESPONSE
# =========================================================

def generate_response(user_text):

    messages = [
        {
            "role": "system",
            "content": build_system_prompt()
        }
    ]

    for msg in st.session_state.messages[-12:]:

        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })

    messages.append({
        "role": "user",
        "content": user_text
    })

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.9,
        max_tokens=700
    )

    return response.choices[0].message.content

# =========================================================
# CHAT
# =========================================================

st.header("💬 Conversation")

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input(
    "Écris ton message..."
)

if prompt:

    st.session_state.daily_messages += 1

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("FØNTANELLE réfléchit..."):

            response = generate_response(prompt)

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

c1, c2, c3 = st.columns(3)

with c1:

    st.markdown("""
<div class="card">

<b>Gratuit</b><br><br>

• messages limités<br>
• mémoire courte<br>
• relation légère<br>
• accès standard

</div>
""", unsafe_allow_html=True)

with c2:

    st.markdown("""
<div class="card premium-glow">

<b>Premium</b><br><br>

• mémoire longue<br>
• mode adulte privé<br>
• voix immersive (future)<br>
• personnalité évolutive<br>
• présence émotionnelle renforcée

</div>
""", unsafe_allow_html=True)

with c3:

    st.markdown("""
<div class="card">

<b>Ultra Premium</b><br><br>

• relation exclusive<br>
• scénarios immersifs<br>
• appels vocaux<br>
• avatars visuels<br>
• mode nocturne<br>
• expériences émotionnelles avancées

</div>
""", unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================

st.success(
    "FØNTANELLE ∞ — Private AI Companion prêt."
)

st.caption(
    "Future stack : OpenAI Realtime API • ElevenLabs • Supabase • Voice Presence"
)
