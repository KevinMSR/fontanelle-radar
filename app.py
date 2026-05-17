import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import requests

st.set_page_config(page_title="Stock Insight", page_icon="📈", layout="wide")

st.markdown("""
<style>
.stApp { background:#f8fafc; }
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#0f172a,#111827);
}
section[data-testid="stSidebar"] * { color:white !important; }
.block-container { padding-top:2rem; max-width:1200px; }
.card {
    background:white;
    border:1px solid #e5e7eb;
    border-radius:18px;
    padding:22px;
    box-shadow:0 8px 28px rgba(15,23,42,.08);
    margin-bottom:18px;
}
.kpi {
    background:white;
    border:1px solid #e5e7eb;
    border-radius:16px;
    padding:18px;
    box-shadow:0 6px 20px rgba(15,23,42,.06);
}
.kpi-title { color:#64748b; font-size:13px; font-weight:700; text-transform:uppercase; }
.kpi-value { font-size:26px; font-weight:800; color:#0f172a; margin-top:6px; }
.notice {
    background:#ecfdf5;
    border:1px solid #86efac;
    color:#166534;
    padding:14px 18px;
    border-radius:14px;
    margin-bottom:18px;
}
.tip {
    background:#eff6ff;
    border:1px solid #bfdbfe;
    color:#1e40af;
    padding:14px;
    border-radius:14px;
}
.stock-button button {
    background:linear-gradient(135deg,#6366f1,#8b5cf6) !important;
    color:white !important;
    border-radius:12px !important;
    border:0 !important;
    width:100%;
    font-weight:700;
}
</style>
""", unsafe_allow_html=True)

COMMON = {
    "apple": "AAPL", "aapl": "AAPL",
    "microsoft": "MSFT", "tesla": "TSLA",
    "amazon": "AMZN", "google": "GOOGL",
    "alphabet": "GOOGL", "meta": "META", "nvidia": "NVDA",
    "lvmh": "MC.PA", "total": "TTE.PA", "airbus": "AIR.PA",
    "bitcoin": "BTC-USD", "ethereum": "ETH-USD",
}

def yahoo_search(query):
    try:
        url = "https://query1.finance.yahoo.com/v1/finance/search"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, params={"q": query, "quotes_count": 6}, headers=headers, timeout=8)
        data = r.json()
        out = []
        for q in data.get("quotes", []):
            sym = q.get("symbol")
            name = q.get("shortname") or q.get("longname") or sym
            if sym:
                out.append((sym, name))
        return out
    except Exception:
        return []

def money(x):
    try:
        x = float(x)
        if abs(x) >= 1_000_000_000_000:
            return f"${x/1_000_000_000_000:.2f}T"
        if abs(x) >= 1_000_000_000:
            return f"${x/1_000_000_000:.2f}B"
        if abs(x) >= 1_000_000:
            return f"${x/1_000_000:.2f}M"
        return f"${x:,.2f}"
    except Exception:
        return "N/D"

def val(info, key):
    v = info.get(key)
    return "N/D" if v in [None, ""] else v

def french_description(info):
    name = val(info, "longName")
    sector = val(info, "sector")
    industry = val(info, "industry")
    country = val(info, "country")
    employees = val(info, "fullTimeEmployees")
    return f"""
**{name}** est une entreprise basée principalement en **{country}**.  
Elle évolue dans le secteur **{sector}**, avec une activité liée à **{industry}**.

Cette fiche donne une lecture simplifiée de l’entreprise : activité, prix, capitalisation, performance récente, ratios financiers et niveau de risque.

**Employés :** {employees}
"""

def recommendation(hist, info):
    close = hist["Close"]
    last = float(close.iloc[-1])
    ma20 = float(close.tail(20).mean())
    ma60 = float(close.tail(60).mean()) if len(close) >= 60 else ma20
    perf = ((last - float(close.iloc[0])) / float(close.iloc[0])) * 100
    vol = close.pct_change().std() * (252 ** 0.5) * 100
    pe = info.get("trailingPE")

    score = 0
    if last > ma20: score += 1
    if last > ma60: score += 1
    if perf > 5: score += 1
    if vol < 35: score += 1
    if pe and pe < 35: score += 1

    if score >= 4:
        avis = "profil intéressant à surveiller, avec une tendance plutôt constructive."
    elif score >= 2:
        avis = "profil neutre : l’action mérite une analyse complémentaire."
    else:
        avis = "profil risqué ou fragile : prudence avant toute décision."

    return f"""
### Recommandation éducative : {avis}

- Prix actuel : **${last:.2f}**
- Moyenne 20 jours : **${ma20:.2f}**
- Moyenne 60 jours : **${ma60:.2f}**
- Performance 6 mois : **{perf:.2f}%**
- Volatilité estimée : **{vol:.2f}%**

⚠️ Ceci n’est pas un conseil financier. Investir comporte un risque de perte en capital.
"""

with st.sidebar:
    st.markdown("## 📈 Stock Insight")
    st.caption("Analyse boursière simplifiée")
    st.markdown("---")

    query = st.text_input("🔍 Rechercher une action", value="Apple")

    q = query.lower().strip()
    results = []
    if q in COMMON:
        results.append((COMMON[q], query.title()))

    results += yahoo_search(query)

    seen = set()
    clean = []
    for s, n in results:
        if s not in seen:
            clean.append((s, n))
            seen.add(s)

    if not clean:
        clean = [(query.upper(), query.upper())]

    st.write("Sélectionnez un résultat :")
    selected = st.radio(
        "Résultats",
        clean,
        format_func=lambda x: f"{x[0]} — {x[1]}",
        label_visibility="collapsed"
    )

    st.markdown('<div class="stock-button">', unsafe_allow_html=True)
    analyze = st.button("▶ Analyser")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.caption("Données fournies par Yahoo Finance.")
    st.caption("Outil éducatif gratuit.")

symbol = selected[0]

ticker = yf.Ticker(symbol)
info = ticker.info
hist = ticker.history(period="6mo")

if hist.empty:
    st.error("Données indisponibles pour cette action.")
    st.stop()

name = val(info, "longName")
sector = val(info, "sector")
industry = val(info, "industry")
country = val(info, "country")
website = info.get("website")
price = float(hist["Close"].iloc[-1])
previous = float(hist["Close"].iloc[-2]) if len(hist) > 1 else price
change = ((price - previous) / previous) * 100 if previous else 0

st.markdown('<div class="notice">⚠️ Cet avis est généré à partir de données publiques. Il ne constitue pas un conseil financier.</div>', unsafe_allow_html=True)

st.title(f"{name}")
st.caption(f"{symbol} · {sector} · {country}")

tabs = st.tabs(["🏠 Accueil", "📊 Marché", "📈 Performance", "💰 Ratios", "⚠️ Risque", "📝 Résumé"])

with tabs[0]:
    left, right = st.columns([1, 1.5])

    with left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🏢 L'entreprise en bref")
        st.write(f"**Secteur :** {sector}")
        st.write(f"**Industrie :** {industry}")
        st.write(f"**Pays :** {country}")
        st.write(f"**Employés :** {val(info, 'fullTimeEmployees')}")
        if website:
            st.markdown(f"[🌐 Site officiel]({website})")
        st.markdown("</div>", unsafe_allow_html=True)

        k1, k2 = st.columns(2)
        with k1:
            st.markdown(f'<div class="kpi"><div class="kpi-title">Market Cap</div><div class="kpi-value">{money(info.get("marketCap"))}</div></div>', unsafe_allow_html=True)
        with k2:
            st.markdown(f'<div class="kpi"><div class="kpi-title">Prix actuel</div><div class="kpi-value">${price:.2f}</div></div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📄 À propos de l'entreprise")
        st.markdown(french_description(info))
        st.markdown('<div class="tip">💡 Conseil débutant : la capitalisation boursière représente la valeur totale estimée de l’entreprise en bourse.</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.subheader("📊 Vue d'ensemble rapide")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Prix", f"${price:.2f}", f"{change:.2f}%")
    c2.metric("P/E", val(info, "trailingPE"))
    c3.metric("+ Haut 52 sem.", val(info, "fiftyTwoWeekHigh"))
    c4.metric("+ Bas 52 sem.", val(info, "fiftyTwoWeekLow"))

with tabs[1]:
    st.subheader("📊 Graphique du marché")
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=hist.index,
        open=hist["Open"],
        high=hist["High"],
        low=hist["Low"],
        close=hist["Close"],
        name=symbol
    ))
    fig.update_layout(template="plotly_white", height=560, xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

with tabs[2]:
    st.subheader("📈 Performance")
    first = float(hist["Close"].iloc[0])
    perf = ((price - first) / first) * 100
    c1, c2, c3 = st.columns(3)
    c1.metric("Début période", f"${first:.2f}")
    c2.metric("Prix actuel", f"${price:.2f}")
    c3.metric("Performance 6 mois", f"{perf:.2f}%")
    st.line_chart(hist["Close"])

with tabs[3]:
    st.subheader("💰 Ratios financiers")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("P/E", val(info, "trailingPE"))
    c2.metric("EPS", val(info, "trailingEps"))
    c3.metric("Beta", val(info, "beta"))
    c4.metric("Dividend Yield", val(info, "dividendYield"))

with tabs[4]:
    st.subheader("⚠️ Risque")
    volatility = hist["Close"].pct_change().std() * (252 ** 0.5) * 100
    drawdown = ((hist["Close"] / hist["Close"].cummax()) - 1).min() * 100
    c1, c2 = st.columns(2)
    c1.metric("Volatilité estimée", f"{volatility:.2f}%")
    c2.metric("Perte max période", f"{drawdown:.2f}%")
    st.warning("Une forte volatilité signifie que le prix peut varier rapidement. Aucun rendement n’est garanti.")

with tabs[5]:
    st.subheader("📝 Résumé & recommandation")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(recommendation(hist, info))
    st.markdown("</div>", unsafe_allow_html=True)

st.caption("Stock Insight — application éducative gratuite. Aucune API payante obligatoire.")
