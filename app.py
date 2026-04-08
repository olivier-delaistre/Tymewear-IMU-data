import streamlit as st
import json
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.signal import butter, filtfilt

st.set_page_config(page_title="Tymewear Analysis", layout="wide")
st.title("Tymewear IMU & Chest Data")

uploaded_file = st.file_uploader("Upload your Tymewear JSON file", type=["json"])

if uploaded_file is not None:
    try:
        data = json.load(uploaded_file)
        ax, ay, az, cr, c = [], [], [], [], []
        
        for sample in data['samples']:
            ax.extend(sample['ax'])
            ay.extend(sample['ay'])
            az.extend(sample['az'])
            cr.append(sample['cr'])
            c.append(sample['c'])

        ax, ay, az = np.array(ax), np.array(ay), np.array(az)

        nyq = 0.5 * 125.0
        b, a = butter(2, 15.0 / nyq, btype='low', analog=False)
        ax_f = filtfilt(b, a, ax)
        ay_f = filtfilt(b, a, ay)
        az_f = filtfilt(b, a, az)

        time_imu = np.arange(len(ax)) / 125.0
        time_chest = np.arange(len(cr)) / 25.0

        fig = make_subplots(
            rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.04,
            subplot_titles=("<b>Vertical Axis (X)</b>", "<b>Lateral Axis (Y)</b>", 
                            "<b>Anterior/Posterior (Z)</b>", "<b>Respiration (Processed C)</b>")
        )

        fig.add_trace(go.Scatter(x=time_imu, y=ax, name='Axis X', line=dict(color='#00b4d8', width=1.2), hovertemplate='%{y:.2f}'), row=1, col=1)
        fig.add_trace(go.Scatter(x=time_imu, y=ay, name='Axis Y', line=dict(color='#fca311', width=1.2), hovertemplate='%{y:.2f}'), row=2, col=1)
        fig.add_trace(go.Scatter(x=time_imu, y=az, name='Axis Z', line=dict(color='#e63946', width=1.2), hovertemplate='%{y:.2f}'), row=3, col=1)
        # fig.add_trace(go.Scatter(x=time_chest, y=cr, name='Chest Raw (cr)', line=dict(color='#9b5de5', width=1.5), hovertemplate='%{y:.2f}'), row=4, col=1)
        fig.add_trace(go.Scatter(x=time_chest, y=c, name='Chest Processed (c)', line=dict(color='#1dd3b0', width=1.5), hovertemplate='%{y:.2f}'), row=4, col=1)

        fig.update_layout(
            updatemenus=[dict(
                active=0, direction="down", showactive=True, x=0.0, xanchor="left", y=1.12, yanchor="top",
                bgcolor="white", bordercolor="#d3d3d3", font=dict(color="black", size=12),
                buttons=list([
                    dict(label="Raw Data (No Filter)", method="restyle", args=[{"y": [ax, ay, az]}, [0, 1, 2]]),
                    dict(label="Butterworth Filter (15Hz)", method="restyle", args=[{"y": [ax_f, ay_f, az_f]}, [0, 1, 2]])
                ])
            )]
        )

        fig.update_layout(
            template="plotly_white", paper_bgcolor="white", plot_bgcolor="white",
            font=dict(family="Arial, sans-serif", size=13, color="black"),
            height=950, hovermode="x unified",
            margin=dict(l=40, r=40, t=100, b=40),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            hoverlabel=dict(bgcolor="white", font_size=14, font_family="Arial", font_color="black")
        )

        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#eaeaea', zeroline=False)
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#eaeaea', zeroline=False)
        
        fig.update_xaxes(rangeslider=dict(visible=True, thickness=0.05), row=4, col=1)
        fig.update_xaxes(title_text="<b>Time (seconds)</b>", row=4, col=1)

        st.plotly_chart(fig, use_container_width=True, theme=None)

    except Exception as e:
        st.error("Error processing the JSON file. Please ensure it is a valid Tymewear export.")
        st.write(f"Technical details: {e}")
