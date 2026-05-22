import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE SETUP & THEME ---
st.set_page_config(
    page_title="Germany EV Charging Infrastructure Dashboard",
    page_icon="🔌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject modern UI styling and premium aesthetics
st.markdown("""
    <style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
    
    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    /* Glassmorphism KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.03));
        border: 1px border solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.15);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 12px;
    }
    
    .kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.25);
        border: 1px solid rgba(0, 204, 150, 0.3);
    }
    
    .kpi-title {
        font-size: 14px;
        color: #8892b0;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 8px;
    }
    
    .kpi-value {
        font-size: 32px;
        font-weight: 800;
        font-family: 'Outfit', sans-serif;
        color: #ffffff;
        background: linear-gradient(120deg, #ffffff, #00cc96);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .kpi-subtitle {
        font-size: 12px;
        color: #00cc96;
        margin-top: 4px;
        font-weight: 600;
    }
    
    /* Styled container headers */
    .section-header {
        font-size: 20px;
        font-weight: 700;
        margin-bottom: 15px;
        color: #ffffff;
        border-left: 4px solid #00cc96;
        padding-left: 12px;
    }
    
    /* Sidebar adjustments */
    .css-1d391tw {
        background-color: #0e1117;
    }
    </style>
""", unsafe_allow_html=True)

# --- DATA LOADING & CACHING ---
@st.cache_data(show_spinner="Analyzing German EV Charging Infrastructure Dataset...")
def load_data():
    # Load dataset with standard semicolon separator
    df = pd.read_csv(
        'rhein-kreis-neuss-ladesaulen-in-deutschland.csv',
        delimiter=';',
        on_bad_lines='skip'
    )
    
    # Clean and parse coordinates
    df = df.dropna(subset=['koordinaten'])
    coords = df['koordinaten'].str.split(',', expand=True)
    df['lat'] = pd.to_numeric(coords[0].str.strip(), errors='coerce')
    df['lon'] = pd.to_numeric(coords[1].str.strip(), errors='coerce')
    df = df.dropna(subset=['lat', 'lon'])
    
    # Fill missing values and convert types
    df['Anzahl Ladepunkte'] = pd.to_numeric(df['Anzahl Ladepunkte'], errors='coerce').fillna(1).astype(int)
    df['Nennleistung Ladeeinrichtung [kW]'] = pd.to_numeric(df['Nennleistung Ladeeinrichtung [kW]'], errors='coerce').fillna(0)
    
    # Extract operator name cleanses (handling NaNs)
    df['Betreiber'] = df['Betreiber'].fillna('Unknown Operator')
    
    # Create simple Fast Charging flag
    df['is_fast'] = df['Art der Ladeeinrichung'].apply(
        lambda x: 'Fast (Schnellladeeinrichtung)' if 'Schnell' in str(x) else 'Normal (Normalladeeinrichtung)'
    )
    
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading CSV data: {e}")
    st.info("Please make sure the file 'rhein-kreis-neuss-ladesaulen-in-deutschland.csv' is present in the workspace.")
    st.stop()

# --- SIDEBAR FILTERS ---
st.sidebar.image("https://img.icons8.com/nolan/96/lightning-bolt.png", width=80)
st.sidebar.title("Filters Panel")
st.sidebar.markdown("Refine the EV Infrastructure dataset")

# Operator Filter (Top 20 + search option)
top_operators = list(df['Betreiber'].value_counts().head(30).index)
operator_choice = st.sidebar.multiselect(
    "Select Operator (Betreiber)",
    options=sorted(df['Betreiber'].unique()),
    default=[],
    placeholder="Showing all operators"
)

# District/City Filter
districts = sorted(df['Kreis/kreisfreie Stadt'].unique())
selected_districts = st.sidebar.multiselect(
    "Select District (Landkreis)",
    options=districts,
    default=[],
    placeholder="Showing all districts"
)

# Charging Type Filter
charging_type_choice = st.sidebar.multiselect(
    "Charging Class",
    options=df['is_fast'].unique(),
    default=df['is_fast'].unique()
)

# Power capacity (kW) slider
min_kw, max_kw = int(df['Nennleistung Ladeeinrichtung [kW]'].min()), int(df['Nennleistung Ladeeinrichtung [kW]'].max())
selected_power_range = st.sidebar.slider(
    "Charging Power Range (kW)",
    min_value=min_kw,
    max_value=max_kw,
    value=(min_kw, max_kw)
)

# Apply filters
filtered_df = df.copy()

if operator_choice:
    filtered_df = filtered_df[filtered_df['Betreiber'].isin(operator_choice)]

if selected_districts:
    filtered_df = filtered_df[filtered_df['Kreis/kreisfreie Stadt'].isin(selected_districts)]

if charging_type_choice:
    filtered_df = filtered_df[filtered_df['is_fast'].isin(charging_type_choice)]

filtered_df = filtered_df[
    (filtered_df['Nennleistung Ladeeinrichtung [kW]'] >= selected_power_range[0]) &
    (filtered_df['Nennleistung Ladeeinrichtung [kW]'] <= selected_power_range[1])
]

# --- MAIN DASHBOARD LAYOUT ---
st.title("🔌 EV Charging Stations Germany")
st.markdown("An interactive analysis of electric vehicle charging infrastructure distribution, capacity, and operators across Germany.")

# --- KPI METRIC CARDS ---
kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)

total_stations = len(filtered_df)
total_points = filtered_df['Anzahl Ladepunkte'].sum()
total_power_mw = filtered_df['Nennleistung Ladeeinrichtung [kW]'].sum() / 1000.0

if total_stations > 0:
    pct_fast = (filtered_df['is_fast'].str.contains('Fast').sum() / total_stations) * 100
    avg_power = filtered_df['Nennleistung Ladeeinrichtung [kW]'].mean()
else:
    pct_fast = 0
    avg_power = 0

with kpi_col1:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Stations</div>
            <div class="kpi-value">{total_stations:,}</div>
            <div class="kpi-subtitle">Charging locations</div>
        </div>
    """, unsafe_allow_html=True)

with kpi_col2:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Plugs</div>
            <div class="kpi-value">{total_points:,}</div>
            <div class="kpi-subtitle">Individual connections</div>
        </div>
    """, unsafe_allow_html=True)

with kpi_col3:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Total Capacity</div>
            <div class="kpi-value">{total_power_mw:,.1f} MW</div>
            <div class="kpi-subtitle">Combined power output</div>
        </div>
    """, unsafe_allow_html=True)

with kpi_col4:
    st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Fast Charger Share</div>
            <div class="kpi-value">{pct_fast:.1f}%</div>
            <div class="kpi-subtitle">Avg power: {avg_power:.1f} kW</div>
        </div>
    """, unsafe_allow_html=True)

# --- MAP SECTION ---
st.markdown('<div class="section-header">Spatial Distribution Map</div>', unsafe_allow_html=True)

if total_stations == 0:
    st.warning("No charging stations match your active filters. Adjust your inputs in the sidebar.")
else:
    # Use dark premium map styling
    # Enable clustering for high density areas
    fig_map = px.scatter_map(
        filtered_df,
        lat="lat",
        lon="lon",
        color="is_fast",
        size="Anzahl Ladepunkte",
        hover_name="Betreiber",
        hover_data={
            "Ort": True,
            "Nennleistung Ladeeinrichtung [kW]": ":.1f kW",
            "Anzahl Ladepunkte": True,
            "is_fast": False,
            "lat": False,
            "lon": False
        },
        color_discrete_map={
            "Normal (Normalladeeinrichtung)": "#00cc96",
            "Fast (Schnellladeeinrichtung)": "#ef553b"
        },
        zoom=5,
        height=650,
        title=f"Geographical View of Charging Stations ({total_stations:,} locations)"
    )
    
    # Configure styling and clustering
    fig_map.update_traces(cluster=dict(enabled=True))
    fig_map.update_layout(
        map_style="carto-darkmatter",
        margin=dict(l=0, r=0, t=40, b=0),
        legend=dict(
            title="Charging Class",
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(14, 17, 23, 0.8)",
            font=dict(color="#ffffff")
        )
    )
    st.plotly_chart(fig_map, use_container_width=True)

# --- ANALYTICS AND CHARTS ---
st.markdown('<div class="section-header">Infrastructure Insights & Analytics</div>', unsafe_allow_html=True)
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.markdown("### Top Charging Station Operators")
    if total_stations > 0:
        op_counts = filtered_df['Betreiber'].value_counts().head(10).reset_index()
        op_counts.columns = ['Operator', 'Stations']
        
        fig_ops = px.bar(
            op_counts,
            y='Operator',
            x='Stations',
            orientation='h',
            text='Stations',
            color='Stations',
            color_continuous_scale='Viridis',
            labels={'Stations': 'Number of Stations', 'Operator': ''},
            height=380
        )
        fig_ops.update_layout(
            margin=dict(l=0, r=0, t=10, b=10),
            coloraxis_showscale=False,
            yaxis=dict(autorange="reversed")
        )
        st.plotly_chart(fig_ops, use_container_width=True)
    else:
        st.info("No data to plot")

with col_chart2:
    st.markdown("### Charging Power Output Distribution (kW)")
    if total_stations > 0:
        fig_dist = px.histogram(
            filtered_df,
            x="Nennleistung Ladeeinrichtung [kW]",
            color="is_fast",
            labels={'Nennleistung Ladeeinrichtung [kW]': 'Power Capacity (kW)'},
            color_discrete_map={
                "Normal (Normalladeeinrichtung)": "#00cc96",
                "Fast (Schnellladeeinrichtung)": "#ef553b"
            },
            log_y=True,
            nbins=40,
            height=380
        )
        fig_dist.update_layout(
            margin=dict(l=0, r=0, t=10, b=10),
            bargap=0.05,
            showlegend=False
        )
        st.plotly_chart(fig_dist, use_container_width=True)
    else:
        st.info("No data to plot")

# --- DATA TABLE EXPLORER ---
st.markdown('<div class="section-header">Dataset Explorer</div>', unsafe_allow_html=True)
with st.expander("Show Detailed Data Table & Export Options"):
    display_cols = [
        'Betreiber', 'Art der Ladeeinrichung', 'Anzahl Ladepunkte', 
        'Nennleistung Ladeeinrichtung [kW]', 'Kreis/kreisfreie Stadt', 
        'Ort', 'Postleitzahl', 'Straße', 'Hausnummer'
    ]
    st.dataframe(filtered_df[display_cols], use_container_width=True)
    
    # Download CSV button
    csv_data = filtered_df[display_cols].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Filtered Data as CSV 📥",
        data=csv_data,
        file_name="germany_ev_charging_stations_filtered.csv",
        mime="text/csv"
    )
