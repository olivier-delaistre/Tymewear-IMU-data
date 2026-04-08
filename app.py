import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Tymewear Analysis", layout="wide")
st.title("Tymewear Acceleration Data")


uploaded_file = st.file_uploader("Upload your Tymewear CSV file here", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, sep=";")
        df.columns = df.columns.str.strip()

        # Create time axis (125 Hz)
        df['Time'] = df.index / 125.0

        nom_x = 'ax'
        nom_y = 'ay'
        nom_z = 'az'

        fig = make_subplots(
            rows=3, cols=1, 
            shared_xaxes=True,
            vertical_spacing=0.06,
            subplot_titles=("<b>Vertical Axis (X)</b>", "<b>Lateral Axis (Y)</b>", "<b>Anterior/Posterior Axis (Z)</b>")
        )

        fig.add_trace(go.Scatter(
            x=df['Time'], y=df[nom_x], name='Axis X', 
            line=dict(color='#00b4d8', width=1.5), hovertemplate='%{y:.2f}'
        ), row=1, col=1)

        fig.add_trace(go.Scatter(
            x=df['Time'], y=df[nom_y], name='Axis Y', 
            line=dict(color='#fca311', width=1.5), hovertemplate='%{y:.2f}'
        ), row=2, col=1)

        fig.add_trace(go.Scatter(
            x=df['Time'], y=df[nom_z], name='Axis Z', 
            line=dict(color='#e63946', width=1.5), hovertemplate='%{y:.2f}'
        ), row=3, col=1)

        fig.update_layout(
            template="plotly_white",
            height=850,
            hovermode="x unified",
            showlegend=False,
            font=dict(family="Arial, sans-serif", size=13, color="#2b2b2b"),
            margin=dict(l=40, r=40, t=60, b=40),
            hoverlabel=dict(bgcolor="white", font_size=14, font_family="Arial")
        )

        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0', zeroline=False)
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0', zeroline=False)

        fig.update_xaxes(rangeslider_visible=True, row=3, col=1)
        fig.update_xaxes(title_text="<b>Time (seconds)</b>", row=3, col=1)

        st.plotly_chart(fig, use_container_width=True, theme =None)

    except Exception as e:
        st.error("Oops, an error occurred while reading the file. Please check the CSV format.")
        st.write(f"Technical details: {e}")
