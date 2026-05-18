import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Stock Insight",
    page_icon="📡",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0b1020 0%, #111827 45%, #061826 100%);
    color: white;
}

.big-title {
    font-size: 48px;
    font-weight: 900;
    background: linear-gradient(90deg, #38bdf8, #e879f9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.card {
    background: rgba(15, 23, 42, 0.85);
    border: 1px solid rgba(56, 189, 248, 0.25);
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 18px;
}

.metric-card {
    background: rgba(15, 23, 42, 0.90);
    border: 1px solid rgba(168, 85, 247, 0.35);
    border-radius: 18px;
    padding: 20px;
    min-height: 130px;
}

.metric-label {
    color: #94a3b8;
    font-size: 14px;
    font-weight: 700;
    text-transform: uppercase;
}

.metric-value {
    color: white;
    font-size: 30px;
    font-weight: 900;
}

.small-muted {
    color: #94a3b8;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)


def is_missing(value):
    if value is None:
        return True
    try:
        return pd.isna(value)
    except Exception:
        return False


def fmt(value, suffix="", decimals=2):
    if is_missing(value):
        return "N/D"

    if isinstance(value, str):
        return value

    try:
        value = float(value)

        if abs(value) >= 1_000_000_000:
            return f"{value / 1_000_000_000:.{decimals}f} Md{suffix}"

        if abs(value) >= 1_000_000:
            return f"{value / 1_000_000:.{decimals}f} M{suffix}"

        if abs(value) >= 1_000:
            return f"{value:,.0f}{suffix}".replace(",", " ")

        return f"{value:.{decimals}f}{suffix}"

    except Exception:
        return str(value)


def fmt_percent(value):
    if is_missing(value):
        return "N/D"

    if isinstance(value, str):
        return value

    try:
        value = float(value)
        if abs(value) < 1:
            value *= 100
        return f"{value:.2f} %"
    except Exception:
        return "N/D"


ALIASES = {
    "apple": "AAPL",
    "aapl": "AAPL",
    "microsoft": "MSFT",
    "msft": "MSFT",
    "google": "GOOGL",
    "alphabet": "GOOGL",
    "amazon": "AMZN",
    "tesla": "TSLA",
    "nvidia": "NVDA",
    "amd": "AMD",
    "meta": "META",
    "facebook": "META",
    "netflix": "NFLX",

    "bitcoin": "BTC-USD",
    "btc": "BTC-USD",
    "ethereum": "ETH-USD",
    "ether": "ETH-USD",
    "eth": "ETH-USD",
    "solana": "SOL-USD",
    "sol": "SOL-USD",
    "cardano": "ADA-USD",
    "ada": "ADA-USD",
    "xrp": "XRP-USD",
    "dogecoin": "DOGE-USD",
    "doge": "DOGE-USD",
    "bnb": "BNB-USD",
    "litecoin": "LTC-USD",
    "ltc": "LTC-USD",
}


def normalize_query(query):
    if not query:
        return None

    q = query.lower().strip().replace("$", "")

    if q in ALIASES:
        return ALIASES[q]

    if q.endswith("-usd"):
        return q.upper()

    if len(q) <= 8 and q.replace(".", "").replace("-", "").isalnum():
        return q.upper()

    return None


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_market_data(symbol):
    data = {
        "symbol": symbol,
        "name": symbol,
        "type": "N/D",
        "currency": "N/D",
        "exchange": "N/D",
        "price": None,
        "previous_close": None,
        "open": None,
        "day_high": None,
        "day_low": None,
        "market_cap": None,
        "volume": None,
        "avg_volume": None,
        "pe": None,
        "forward_pe": None,
        "dividend_yield": None,
        "beta": None,
        "history": pd.DataFrame(),
        "error": None,
    }

    try:
        ticker = yf.Ticker(symbol)

        try:
            info = ticker.info or {}
        except Exception:
            info = {}

        try:
            fast = dict(ticker.fast_info or {})
        except Exception:
            fast = {}

        try:
            hist = ticker.history(period="6mo", interval="1d", auto_adjust=False)
        except Exception:
            hist = pd.DataFrame()

        is_crypto = symbol.upper().endswith("-USD")

        data["history"] = hist

        data["name"] = (
            info.get("shortName")
            or info.get("longName")
            or info.get("displayName")
            or symbol
        )

        data["type"] = (
            "Crypto"
            if is_crypto
            else info.get("quoteType")
            or info.get("typeDisp")
            or "N/D"
        )

        data["currency"] = (
            info.get("currency")
            or fast.get("currency")
            or ("USD" if is_crypto else "N/D")
        )

        data["exchange"] = (
            info.get("exchange")
            or info.get("fullExchangeName")
            or ("Crypto" if is_crypto else "N/D")
        )

        data["price"] = (
            fast.get("lastPrice")
            or fast.get("last_price")
            or info.get("regularMarketPrice")
            or info.get("currentPrice")
        )

        data["previous_close"] = (
            fast.get("previousClose")
            or fast.get("previous_close")
            or info.get("regularMarketPreviousClose")
            or info.get("previousClose")
        )

        data["open"] = (
            fast.get("open")
            or info.get("regularMarketOpen")
            or info.get("open")
        )

        data["day_high"] = (
            fast.get("dayHigh")
            or fast.get("day_high")
            or info.get("regularMarketDayHigh")
            or info.get("dayHigh")
        )

        data["day_low"] = (
            fast.get("dayLow")
            or fast.get("day_low")
            or info.get("regularMarketDayLow")
            or info.get("dayLow")
        )

        data["market_cap"] = (
            fast.get("marketCap")
            or fast.get("market_cap")
            or info.get("marketCap")
        )

        data["volume"] = (
            info.get("volume")
            or info.get("regularMarketVolume")
            or fast.get("lastVolume")
            or fast.get("last_volume")
        )

        data["avg_volume"] = (
            info.get("averageVolume")
            or info.get("averageDailyVolume10Day")
            or info.get("averageVolume10days")
        )

        if hist is not None and not hist.empty:
            hist_clean = hist.dropna(how="all")

            if not hist_clean.empty:
                last_row = hist_clean.iloc[-1]

                if is_missing(data["price"]) and "Close" in hist_clean.columns:
                    data["price"] = last_row.get("Close")

                if is_missing(data["volume"]) and "Volume" in hist_clean.columns:
                    data["volume"] = last_row.get("Volume")

                if is_missing(data["open"]) and "Open" in hist_clean.columns:
                    data["open"] = last_row.get("Open")

                if is_missing(data["day_high"]) and "High" in hist_clean.columns:
                    data["day_high"] = last_row.get("High")

                if is_missing(data["day_low"]) and "Low" in hist_clean.columns:
                    data["day_low"] = last_row.get("Low")

                if is_missing(data["previous_close"]) and len(hist_clean) >= 2:
                    data["previous_close"] = hist_clean["Close"].dropna().iloc[-2]

                if is_missing(data["avg_volume"]) and "Volume" in hist_clean.columns:
                    data["avg_volume"] = hist_clean["Volume"].dropna().tail(30).mean()

        if is_crypto:
            data["pe"] = "Non applicable"
            data["forward_pe"] = "Non applicable"
            data["dividend_yield"] = "Non applicable"
            data["beta"] = "Non applicable"
        else:
            data["pe"] = info.get("trailingPE")
            data["forward_pe"] = info.get("forwardPE")
            data["dividend_yield"] = info.get("dividendYield")
            data["beta"] = info.get("beta")

        return data

    except Exception as e:
        data["error"] = str(e)
        return data


with st.sidebar:
    st.markdown('<div class="big-title">Stock Insight</div>', unsafe_allow_html=True)
    st.write("Radar financier cyberpunk sans API payante")
    st.divider()

    query = st.text_input(
        "🔎 Recherche action / crypto / ETF / forex",
        value="Apple"
    )

    detected_symbol = normalize_query(query)

    st.write("Palette de marché")

    manual_symbol = st.text_input(
        "Ticker Yahoo Finance",
        value=detected_symbol or "",
        placeholder="Ex : AAPL, ETH-USD, BTC-USD"
    )

    run = st.button("⚡ Analyser", use_container_width=True)

    st.divider()
    st.caption("Données publiques via Yahoo Finance / yfinance.")
    st.caption("Certaines données peuvent être indisponibles selon l’actif.")


symbol = manual_symbol.strip().upper() if manual_symbol else detected_symbol

if not symbol:
    st.warning("Entre une action ou une crypto : Apple, AAPL, Ethereum, ETH, Bitcoin, BTC...")
    st.stop()

data = fetch_market_data(symbol)

if data["error"]:
    st.error(f"Erreur lors du chargement : {data['error']}")
    st.stop()


st.markdown(f"# {data['name']}")
st.markdown(
    f"<div class='small-muted'>{data['symbol']} · {data['type']} · {data['currency']} · {data['exchange']}</div>",
    unsafe_allow_html=True
)

tabs = st.tabs([
    "🏠 Accueil",
    "🌍 Marché",
    "📈 Performance",
    "📊 Ratios",
    "⚠️ Risque",
    "🧠 Résumé"
])


with tabs[0]:
    st.markdown("## 🏠 Accueil")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Prix</div>
            <div class="metric-value">{fmt(data["price"])} {data["currency"]}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Capitalisation</div>
            <div class="metric-value">{fmt(data["market_cap"])}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Volume</div>
            <div class="metric-value">{fmt(data["volume"])}</div>
        </div>
        """, unsafe_allow_html=True)


with tabs[1]:
    st.markdown("## 🌍 Marché")

    st.markdown(f"""
    <div class="card">
        <p><b>Type :</b> {data["type"]}</p>
        <p><b>Devise :</b> {data["currency"]}</p>
        <p><b>Exchange :</b> {data["exchange"]}</p>
        <p><b>Prix :</b> {fmt(data["price"])} {data["currency"]}</p>
        <p><b>Ouverture :</b> {fmt(data["open"])}</p>
        <p><b>Plus haut jour :</b> {fmt(data["day_high"])}</p>
        <p><b>Plus bas jour :</b> {fmt(data["day_low"])}</p>
        <p><b>Clôture précédente :</b> {fmt(data["previous_close"])}</p>
        <p><b>Volume :</b> {fmt(data["volume"])}</p>
        <p><b>Volume moyen :</b> {fmt(data["avg_volume"])}</p>
    </div>
    """, unsafe_allow_html=True)


with tabs[2]:
    st.markdown("## 📈 Performance")

    hist = data["history"]

    if hist is None or hist.empty or "Close" not in hist.columns:
        st.warning("Historique indisponible pour cet actif.")
    else:
        close = hist["Close"].dropna()

        perf_1d = ((close.iloc[-1] / close.iloc[-2]) - 1) * 100 if len(close) >= 2 else None
        perf_5d = ((close.iloc[-1] / close.iloc[-6]) - 1) * 100 if len(close) >= 6 else None
        perf_1m = ((close.iloc[-1] / close.iloc[-22]) - 1) * 100 if len(close) >= 22 else None

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">1 jour</div>
                <div class="metric-value">{fmt_percent(perf_1d)}</div>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">5 jours</div>
                <div class="metric-value">{fmt_percent(perf_5d)}</div>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">1 mois</div>
                <div class="metric-value">{fmt_percent(perf_1m)}</div>
            </div>
            """, unsafe_allow_html=True)

        st.line_chart(close)


with tabs[3]:
    st.markdown("## 📊 Ratios")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">P/E</div>
            <div class="metric-value">{fmt(data["pe"])}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Forward P/E</div>
            <div class="metric-value">{fmt(data["forward_pe"])}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        dividend = data["dividend_yield"]
        dividend_display = dividend if isinstance(dividend, str) else fmt_percent(dividend)

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Dividend Yield</div>
            <div class="metric-value">{dividend_display}</div>
        </div>
        """, unsafe_allow_html=True)

    st.caption(
        "Les ratios fondamentaux ne sont pas toujours disponibles pour les ETF, cryptomonnaies ou certains actifs Yahoo Finance."
    )


with tabs[4]:
    st.markdown("## ⚠️ Risque")

    hist = data["history"]

    if hist is None or hist.empty or "Close" not in hist.columns:
        st.warning("Données insuffisantes pour calculer le risque.")
    else:
        close = hist["Close"].dropna()
        returns = close.pct_change().dropna()

        if returns.empty:
            st.warning("Données insuffisantes pour calculer la volatilité.")
        else:
            volatility = returns.std() * np.sqrt(252) * 100
            max_drawdown = ((close / close.cummax()) - 1).min() * 100

            c1, c2, c3 = st.columns(3)

            with c1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Volatilité annualisée</div>
                    <div class="metric-value">{fmt_percent(volatility)}</div>
                </div>
                """, unsafe_allow_html=True)

            with c2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Max Drawdown</div>
                    <div class="metric-value">{fmt_percent(max_drawdown)}</div>
                </div>
                """, unsafe_allow_html=True)

            with c3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Beta</div>
                    <div class="metric-value">{fmt(data["beta"])}</div>
                </div>
                """, unsafe_allow_html=True)


with tabs[5]:
    st.markdown("## 🧠 Résumé")

    price = data["price"]
    prev = data["previous_close"]

    if not is_missing(price) and not is_missing(prev) and prev != 0:
        daily_change = ((float(price) / float(prev)) - 1) * 100
        tendance = "positive" if daily_change > 0 else "négative" if daily_change < 0 else "stable"
        daily_text = f"{daily_change:.2f} %"
    else:
        tendance = "indéterminée"
        daily_text = "N/D"

    st.markdown(f"""
    <div class="card">
        <p><b>{data["name"]}</b> est identifié avec le symbole <b>{data["symbol"]}</b>.</p>
        <p>Type : <b>{data["type"]}</b></p>
        <p>Devise : <b>{data["currency"]}</b></p>
        <p>Exchange : <b>{data["exchange"]}</b></p>
        <p>Prix actuel estimé : <b>{fmt(data["price"])} {data["currency"]}</b></p>
        <p>Variation journalière estimée : <b>{daily_text}</b></p>
        <p>Tendance courte période : <b>{tendance}</b></p>
    </div>
    """, unsafe_allow_html=True)

    st.caption(
        "Ce résumé est informatif et ne constitue pas un conseil financier."
    )
