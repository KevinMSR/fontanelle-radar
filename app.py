import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# ===================== CONFIG =====================

st.set_page_config(
    page_title="FØNTANELLE ∞ — European Market Radar",
    layout="wide"
)

st.title("🌌 FØNTANELLE ∞")
st.subheader("European Market Radar")
st.caption("Signal over noise.")
st.markdown(f"**Dernière mise à jour : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}**")

# ===================== DATA =====================

indices = {
    "CAC 40": "^FCHI",
    "Euro Stoxx 50": "^STOXX50E",
    "DAX Allemagne": "^GDAXI",
    "FTSE 100 UK": "^FTSE",
    "IBEX 35 Espagne": "^IBEX"
}

actions_eu = [
    "AI.PA", "AIR.PA", "MC.PA", "OR.PA", "TTE.PA", "SAN.PA", "BNP.PA",
    "CS.PA", "RMS.PA", "ASML.AS", "SIE.DE", "SU.PA", "DG.PA", "VIE.PA"
]

# ===================== SIDEBAR =====================

st.sidebar.header("Options")

periode = st.sidebar.selectbox(
    "Période du graphique",
    ["1d", "5d", "1mo", "3mo", "6mo", "1y"],
    index=3
)

afficher_volume = st.sidebar.checkbox("Afficher le volume", value=True)

# ===================== INDICES =====================

st.header("📊 Indices européens")

cols = st.columns(len(indices))

for i, (nom, ticker) in enumerate(indices.items()):
    with cols[i]:
        try:
            data = yf.Ticker(ticker).history(period="2d")

            if len(data) >= 2:
                dernier = float(data["Close"].iloc[-1])
                precedent = float(data["Close"].iloc[-2])
                variation = ((dernier - precedent) / precedent) * 100

                st.metric(
                    label=nom,
                    value=f"{dernier:,.2f}",
                    delta=f"{variation:+.2f}%"
                )
            else:
                st.warning("Données insuffisantes")

        except Exception:
            st.error(f"Erreur : {ticker}")

# ===================== SCANNER =====================

st.header("🔥 Scanner FØNTANELLE")

@st.cache_data(ttl=300)
def get_scanner(tickers):
    results = []

    data = yf.download(
        tickers,
        period="5d",
        group_by="ticker",
        progress=False,
        auto_adjust=False
    )

    for tick in tickers:
        try:
            df = data[tick]

            if df.empty or len(df) < 2:
                continue

            close = df["Close"].dropna()
            volume = df["Volume"].dropna() if "Volume" in df.columns else pd.Series(dtype=float)

            if len(close) < 2:
                continue

            prix = float(close.iloc[-1])
            perf_1d = ((close.iloc[-1] - close.iloc[-2]) / close.iloc[-2]) * 100
            perf_5d = ((close.iloc[-1] - close.iloc[0]) / close.iloc[0]) * 100
            volume_moyen = int(volume.mean()) if not volume.empty else 0

            score_fontanelle = (perf_5d * 0.6) + (perf_1d * 0.4)

            results.append({
                "Ticker": tick,
                "Prix": round(prix, 2),
                "Perf 1j (%)": round(float(perf_1d), 2),
                "Perf 5j (%)": round(float(perf_5d), 2),
                "Score FØNTANELLE": round(float(score_fontanelle), 2),
                "Volume moyen": volume_moyen
            })

        except Exception:
            continue

    return pd.DataFrame(results)

df_scanner = get_scanner(actions_eu)

if not df_scanner.empty:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🚀 Top signaux positifs")
        st.dataframe(
            df_scanner.sort_values("Score FØNTANELLE", ascending=False).head(8),
            use_container_width=True
        )

    with col2:
        st.subheader("⚠️ Top signaux négatifs")
        st.dataframe(
            df_scanner.sort_values("Score FØNTANELLE", ascending=True).head(8),
            use_container_width=True
        )
else:
    st.warning("Aucune donnée disponible pour le scanner.")

# ===================== GRAPH =====================

st.header("📈 Graphique détaillé")

options = {**indices, **{ticker: ticker for ticker in actions_eu}}

choix = st.selectbox(
    "Choisis un titre ou indice",
    list(options.keys())
)

ticker_choisi = options[choix]
intervalle = "1h" if periode == "1d" else "1d"

data = yf.download(
    ticker_choisi,
    period=periode,
    interval=intervalle,
    progress=False,
    auto_adjust=False
)

if not data.empty:
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    fig = go.Figure()

    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data["Open"],
            high=data["High"],
            low=data["Low"],
            close=data["Close"],
            name="Prix"
        )
    )

    if afficher_volume and "Volume" in data.columns:
        fig.add_trace(
            go.Bar(
                x=data.index,
                y=data["Volume"],
                name="Volume",
                opacity=0.25,
                yaxis="y2"
            )
        )

    fig.update_layout(
        title=f"{choix} — {periode}",
        yaxis=dict(title="Prix"),
        yaxis2=dict(
            title="Volume",
            overlaying="y",
            side="right",
            showgrid=False
        ),
        height=650,
        template="plotly_dark",
        xaxis_rangeslider_visible=False
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Données indisponibles pour ce titre.")

# ===================== EXPORT =====================

st.header("📁 Export")

if not df_scanner.empty:
    csv = df_scanner.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Télécharger le scanner en CSV",
        data=csv,
        file_name=f"fontanelle_scanner_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

# ===================== FOOTER =====================

st.success("Radar opérationnel FØNTANELLE ∞ prêt.")
st.info("Pour lancer localement : streamlit run app.py")
