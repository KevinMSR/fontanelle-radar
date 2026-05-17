import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests
import streamlit.components.v1 as components
from datetime import datetime

st.set_page_config(page_title="Stock Insight Neon", page_icon="📈", layout="wide")

st.markdown("""
<style>
.stApp {
    background:
    radial-gradient(circle at 20% 10%, rgba(168,85,247,.35), transparent 30%),
    radial-gradient(circle at 80% 0%, rgba(34,211,238,.25), transparent 25%),
    linear-gradient(135deg,#020617,#0f172a 45%,#111827);
    color:#e5e7eb;
}
.block-container { padding-top:2rem; max-width:1250px; }
section[data-testid="stSidebar"] {
    background:linear-gradient(180deg,#020617,#111827,#1e1b4b);
    border-right:1px solid rgba(34,211,238,.25);
}
section[data-testid="stSidebar"] * { color:#f8fafc !important; }
h1,h2,h3 { color:#f8fafc !important; text-shadow:0 0 18px rgba(34,211,238,.35); }
.neon-title {
    font-size:46px;
    font-weight:900;
    background:linear-gradient(90deg,#22d3ee,#a855f7,#f472b6);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    text-shadow:0 0 30px rgba(168,85,247,.7);
}
.card {
    background:rgba(15,23,42,.72);
    border:1px solid rgba(34,211,238,.25);
    border-radius:22px;
    padding:22px;
    box-shadow:0 0 35px rgba(34,211,238,.12);
    backdrop-filter:blur(14px);
    margin-bottom:18px;
}
.kpi {
    background:rgba(15,23,42,.80);
    border:1px solid rgba(168,85,247,.35);
    border-radius:18px;
    padding:18px;
    box-shadow:0 0 24px rgba(168,85,247,.18);
}
.kpi-title { color:#94a3b8; font-size:12px; text-transform:uppercase; font-weight:800; }
.kpi-value { font-size:28px; font-weight:900; color:#f8fafc; }
.notice {
    background:rgba(16,185,129,.12);
    border:1px solid rgba(16,185,129,.45);
    color:#bbf7d0;
    padding:14px 18px;
    border-radius:16px;
}
.glow-btn button {
    background:linear-gradient(135deg,#06b6d4,#8b5cf6,#ec4899)!important;
    color:white!important;
    border:0!important;
    border-radius:14px!important;
    font-weight:900!important;
    box-shadow:0 0 22px rgba(168,85,247,.45)!important;
}
.stTabs [data-baseweb="tab-list"] { gap:10px; }
.stTabs [data-baseweb="tab"] {
    background:rgba(15,23,42,.7);
    border:1px solid rgba(34,211,238,.18);
    border-radius:12px;
    color:#e5e7eb;
}
.stTabs [data-baseweb="tab"] {
    background:rgba(15,23,42,.7);
    border:1px solid rgba(34,211,238,.18);
    border-radius:12px;
    color:#e5e7eb;
}

input, textarea {
    background: rgba(15,23,42,.95) !important;
    color: #f8fafc !important;
    border: 1px solid rgba(34,211,238,.55) !important;
    border-radius: 14px !important;
}

input::placeholder, textarea::placeholder {
    color: #94a3b8 !important;
}

div[data-baseweb="select"] * {
    background-color: rgba(15,23,42,.95) !important;
    color: #f8fafc !important;
}

div[data-testid="stTextInput"] label,
div[data-testid="stSelectbox"] label {
    color: #e5e7eb !important;
}

</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=86400)
def load_catalog():
    rows = []

    base_assets = {
        "Apple": "AAPL", "Microsoft": "MSFT", "Nvidia": "NVDA", "Tesla": "TSLA",
        "Amazon": "AMZN", "Meta": "META", "Google": "GOOGL", "Netflix": "NFLX",
        "AMD": "AMD", "Intel": "INTC", "Palantir": "PLTR", "Coinbase": "COIN",
        "Berkshire Hathaway": "BRK-B", "Visa": "V", "Mastercard": "MA",
        "JPMorgan": "JPM", "BlackRock": "BLK", "McDonald’s": "MCD",
        "Coca-Cola": "KO", "Pepsi": "PEP", "Nike": "NKE",
        "LVMH": "MC.PA", "TotalEnergies": "TTE.PA", "Airbus": "AIR.PA",
        "BNP Paribas": "BNP.PA", "Schneider Electric": "SU.PA", "Hermès": "RMS.PA",
        "Safran": "SAF.PA", "Sanofi": "SAN.PA", "AXA": "CS.PA",
        "CAC 40": "^FCHI", "DAX": "^GDAXI", "FTSE 100": "^FTSE",
        "Euro Stoxx 50": "^STOXX50E", "S&P 500": "^GSPC", "Nasdaq 100": "^NDX",
        "Dow Jones": "^DJI", "Russell 2000": "^RUT",
        "Bitcoin": "BTC-USD", "Ethereum": "ETH-USD", "Solana": "SOL-USD",
        "BNB": "BNB-USD", "XRP": "XRP-USD", "Cardano": "ADA-USD",
        "Dogecoin": "DOGE-USD", "Avalanche": "AVAX-USD", "Chainlink": "LINK-USD",
        "Polkadot": "DOT-USD", "Polygon": "MATIC-USD", "Litecoin": "LTC-USD",
        "Gold": "GC=F", "Silver": "SI=F", "Oil WTI": "CL=F", "Natural Gas": "NG=F",
        "EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X", "USD/JPY": "JPY=X",
        "SPY ETF": "SPY", "QQQ ETF": "QQQ", "Vanguard S&P 500 ETF": "VOO",
        "iShares MSCI World ETF": "URTH", "ARK Innovation ETF": "ARKK",
    }

    for name, symbol in base_assets.items():
        rows.append({"name": name, "symbol": symbol, "type": "Catalogue"})

    try:
        url = "https://www.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt"
        df = pd.read_csv(url, sep="|")
        df = df[df["Test Issue"] == "N"]
        for _, r in df.head(3000).iterrows():
            rows.append({"name": r.get("Security Name", ""), "symbol": r.get("Symbol", ""), "type": "NASDAQ"})
    except Exception:
        pass

    try:
        url = "https://www.nasdaqtrader.com/dynamic/SymDir/otherlisted.txt"
        df = pd.read_csv(url, sep="|")
        df = df[df["Test Issue"] == "N"]
        for _, r in df.head(3000).iterrows():
            sym = str(r.get("ACT Symbol", "")).replace(".", "-")
            rows.append({"name": r.get("Security Name", ""), "symbol": sym, "type": "NYSE/AMEX"})
    except Exception:
        pass

    catalog = pd.DataFrame(rows).dropna()
    catalog = catalog[catalog["symbol"].astype(str).str.len() > 0]
    catalog = catalog.drop_duplicates("symbol")
    return catalog

@st.cache_data(ttl=3600)
def get_history(symbol):
    return yf.Ticker(symbol).history(period="6mo")

@st.cache_data(ttl=3600)
def get_info(symbol):
    try:
        return yf.Ticker(symbol).info
    except Exception:
        return {}

def money(x):
    try:
        x = float(x)
        if abs(x) >= 1_000_000_000_000: return f"${x/1_000_000_000_000:.2f}T"
        if abs(x) >= 1_000_000_000: return f"${x/1_000_000_000:.2f}B"
        if abs(x) >= 1_000_000: return f"${x/1_000_000:.2f}M"
        return f"${x:,.2f}"
    except Exception:
        return "N/D"

def tv_symbol(symbol):
    if symbol.endswith("-USD"): return "CRYPTO:" + symbol.replace("-USD", "USD")
    if symbol.endswith(".PA"): return "EURONEXT:" + symbol.replace(".PA", "")
    if symbol.startswith("^"): return symbol
    return "NASDAQ:" + symbol

catalog = load_catalog()

with st.sidebar:
    st.markdown('<div class="neon-title">Stock Insight</div>', unsafe_allow_html=True)
    st.caption("Radar financier cyberpunk sans API payante")
    st.markdown("---")

    query = st.text_input("🔎 Recherche action / crypto / ETF / forex", "Apple")
    q = query.lower().strip()

    filtered = catalog[
        catalog["name"].str.lower().str.contains(q, na=False) |
        catalog["symbol"].str.lower().str.contains(q, na=False)
    ].head(60)

    if filtered.empty:
        filtered = catalog.head(40)

    selected_label = st.selectbox(
        "Palette de marché",
        filtered.apply(lambda r: f"{r['symbol']} — {r['name']} [{r['type']}]", axis=1)
    )

    symbol = selected_label.split(" — ")[0].strip()

    st.markdown('<div class="glow-btn">', unsafe_allow_html=True)
    st.button("⚡ Scanner l’actif")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.caption(f"Catalogue chargé : {len(catalog)} actifs")
    st.caption("Mise à jour automatique toutes les 24h")

hist = get_history(symbol)
info = get_info(symbol)

if hist.empty:
    st.error("Données indisponibles pour cet actif.")
    st.stop()

name = info.get("longName") or info.get("shortName") or symbol
sector = info.get("sector", "N/D")
industry = info.get("industry", "N/D")
country = info.get("country", "N/D")
price = float(hist["Close"].iloc[-1])
previous = float(hist["Close"].iloc[-2]) if len(hist) > 1 else price
change = ((price - previous) / previous) * 100 if previous else 0

st.markdown('<div class="neon-title">📈 Stock Insight Neon Terminal</div>', unsafe_allow_html=True)
st.markdown('<div class="notice">⚠️ Analyse éducative générée depuis des données publiques. Aucun conseil financier. Aucun abonnement API obligatoire.</div>', unsafe_allow_html=True)

st.title(name)
st.caption(f"{symbol} · {sector} · {industry} · {country}")

tabs = st.tabs(["🏠 Accueil", "📊 Graphique", "🌐 TradingView", "🔥 Heatmap", "🤖 IA Résumé", "⭐ Watchlist"])

with tabs[0]:
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f'<div class="kpi"><div class="kpi-title">Prix</div><div class="kpi-value">${price:.2f}</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="kpi"><div class="kpi-title">Variation</div><div class="kpi-value">{change:.2f}%</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="kpi"><div class="kpi-title">Market Cap</div><div class="kpi-value">{money(info.get("marketCap"))}</div></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="kpi"><div class="kpi-title">Beta</div><div class="kpi-value">{info.get("beta","N/D")}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🏢 Fiche entreprise")
    st.write(f"**Nom :** {name}")
    st.write(f"**Secteur :** {sector}")
    st.write(f"**Industrie :** {industry}")
    st.write(f"**Pays :** {country}")
    st.write(f"**Employés :** {info.get('fullTimeEmployees','N/D')}")
    if info.get("website"):
        st.markdown(f"[🌐 Site officiel]({info.get('website')})")
    st.markdown("</div>", unsafe_allow_html=True)

with tabs[1]:
    st.subheader("📊 Graphe holographique")
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=hist.index,
        open=hist["Open"],
        high=hist["High"],
        low=hist["Low"],
        close=hist["Close"],
        increasing_line_color="#22d3ee",
        decreasing_line_color="#f43f5e"
    ))
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(2,6,23,.85)",
        height=560,
        xaxis_rangeslider_visible=False
    )
    st.plotly_chart(fig, use_container_width=True)

with tabs[2]:
    st.subheader("🌐 TradingView intégré")
    url = f"https://s.tradingview.com/widgetembed/?symbol={tv_symbol(symbol)}&interval=D&theme=dark&style=1&locale=fr"
    components.iframe(url, height=620, scrolling=True)

with tabs[3]:
    st.subheader("🔥 Heatmap néon")
    sample = catalog.head(40).copy()
    perf_rows = []
    for s in sample["symbol"].head(30):
        try:
            h = yf.Ticker(s).history(period="5d")
            if len(h) >= 2:
                p = ((h["Close"].iloc[-1] - h["Close"].iloc[0]) / h["Close"].iloc[0]) * 100
                perf_rows.append({"symbol": s, "performance": p})
        except Exception:
            pass

    if perf_rows:
        dfp = pd.DataFrame(perf_rows)
        fig = px.treemap(
            dfp,
            path=["symbol"],
            values=dfp["performance"].abs() + 1,
            color="performance",
            color_continuous_scale=["#f43f5e", "#111827", "#22d3ee"]
        )
        fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", height=520)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Heatmap temporairement indisponible.")

with tabs[4]:
    st.subheader("🤖 Résumé IA local")
    close = hist["Close"]
    ma20 = close.tail(20).mean()
    ma60 = close.tail(60).mean() if len(close) >= 60 else ma20
    perf = ((close.iloc[-1] - close.iloc[0]) / close.iloc[0]) * 100
    volatility = close.pct_change().std() * (252 ** 0.5) * 100

    score = 0
    if price > ma20: score += 1
    if price > ma60: score += 1
    if perf > 5: score += 1
    if volatility < 35: score += 1

    reco = "intéressant à surveiller" if score >= 3 else "neutre / prudent" if score == 2 else "risqué"

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"""
### Verdict éducatif : **{reco}**

- Prix actuel : **${price:.2f}**
- Moyenne 20 jours : **${ma20:.2f}**
- Moyenne 60 jours : **${ma60:.2f}**
- Performance 6 mois : **{perf:.2f}%**
- Volatilité estimée : **{volatility:.2f}%**

⚠️ Ceci n’est pas un conseil financier. Risque de perte en capital.
""")
    st.markdown("</div>", unsafe_allow_html=True)

with tabs[5]:
    st.subheader("⭐ Watchlist futuriste")
    if "watchlist" not in st.session_state:
        st.session_state.watchlist = []

    if st.button("Ajouter à la watchlist"):
        if symbol not in st.session_state.watchlist:
            st.session_state.watchlist.append(symbol)

    if st.session_state.watchlist:
        st.write(st.session_state.watchlist)
    else:
        st.info("Aucun actif dans la watchlist.")

st.caption("Stock Insight Neon — données publiques, Yahoo Finance via yfinance, sans clé API payante.")
