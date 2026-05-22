"""
Meningitis Outbreak Predictor Dashboard - West Africa
WITH: Share, Email, PDF Export, Mobile Responsive
THEME: Health Green
"""

from dash import Dash, dcc, html, Input, Output, State, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import joblib
import base64
import io
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Load data
df = pd.read_csv("data/meningitis_west_africa.csv")

# Load model
try:
    model = joblib.load("meningitis_model.pkl")
    model_loaded = True
except:
    model_loaded = False

# Email configuration (Update with your details)
SENDER_EMAIL = "naniakwa@yahoo.com"
SENDER_PASSWORD = "pqbeaddvtmmspypt"

# Initialize Dash app
app = Dash(__name__, title="Meningitis Outbreak Predictor - West Africa")

# Mobile responsive CSS with HEALTH GREEN THEME
app.index_string = '''
<!DOCTYPE html>
<html>
<head>
    {%metas%}
    <title>{%title%}</title>
    {%favicon%}
    {%css%}
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
    <style>
        body { 
            background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
        }
        
        .main-container { 
            max-width: 1400px; 
            margin: 0 auto; 
            background: white; 
            border-radius: 20px; 
            padding: 20px; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .kpi-card { 
            background: white; 
            border-left: 5px solid #28a745; 
            border-radius: 12px;
            transition: transform 0.2s;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            padding: 20px;
            text-align: center;
            display: inline-block;
            width: 23%;
            margin: 1%;
        }
        
        .kpi-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 4px 15px rgba(40,167,69,0.2);
        }
        
        h1 { 
            color: #1b5e20; 
            font-weight: 700;
            letter-spacing: -0.5px;
            text-align: center;
            margin-bottom: 10px;
        }
        
        h2, h3 { 
            color: #1b5e20; 
        }
        
        .subtitle {
            text-align: center;
            color: #555;
            margin-bottom: 30px;
        }
        
        .filter-item { 
            background: white; 
            padding: 15px; 
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            margin: 10px;
        }
        
        .filter-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            margin-bottom: 30px;
        }
        
        .filter-item {
            width: 30%;
            margin: 0 1%;
        }
        
        .Select-control {
            border-radius: 8px !important;
            border-color: #c8e6c9 !important;
        }
        
        .Select-control:hover {
            border-color: #28a745 !important;
        }
        
        button {
            transition: all 0.2s ease;
            font-weight: 600;
            border: none;
            border-radius: 8px;
            cursor: pointer;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        .btn-email { background-color: #28a745; color: white; padding: 10px 20px; margin: 5px; }
        .btn-pdf { background-color: #dc3545; color: white; padding: 10px 20px; margin: 5px; }
        .btn-whatsapp { background-color: #25D366; color: white; padding: 10px 20px; margin: 5px; }
        .btn-twitter { background-color: #1DA1F2; color: white; padding: 10px 20px; margin: 5px; }
        .btn-copy { background-color: #6c757d; color: white; padding: 10px 20px; margin: 5px; }
        .btn-predict { background-color: #dc3545; color: white; padding: 12px 24px; font-size: 16px; margin-top: 20px; }
        
        .button-group {
            text-align: center;
            margin-bottom: 20px;
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 10px;
        }
        
        .email-container {
            text-align: center;
            margin-top: 10px;
            display: none;
        }
        
        .prediction-sliders {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
        }
        
        .slider-item {
            width: 30%;
            padding: 10px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        
        .prediction-result {
            margin-top: 20px;
            padding: 20px;
            background: #f0f7ff;
            border-radius: 10px;
            text-align: center;
        }
        
        .data-table-container {
            margin-top: 30px;
        }
        
        .dash-table-container {
            border-radius: 12px;
            overflow: hidden;
        }
        
        @media (max-width: 768px) {
            body { padding: 10px; }
            .main-container { padding: 15px; }
            .kpi-card { width: 90% !important; margin: 8px auto !important; }
            .filter-item { width: 100% !important; margin: 8px 0 !important; }
            .slider-item { width: 100% !important; margin: 10px 0 !important; }
            .prediction-sliders { flex-direction: column; }
            h1 { font-size: 1.5rem !important; }
            .button-group button { padding: 8px 16px; font-size: 12px; }
        }
        
        @media (max-width: 480px) {
            .kpi-card h2 { font-size: 20px; }
            .kpi-card h3 { font-size: 12px; }
        }
    </style>
</head>
<body>
    {%app_entry%}
    <footer>
        {%config%}
        {%scripts%}
        {%renderer%}
    </footer>
</body>
</html>
'''

# West African countries list
countries = ['Nigeria', 'Ghana', 'Burkina Faso', 'Niger', 'Mali', 
             'Chad', 'Benin', 'Togo', 'Ivory Coast', 'Senegal']

app.layout = html.Div([
    # Main Container
    html.Div([
        # Header
        html.H1("🦠 West Africa Meningitis Outbreak Predictor"),
        html.P("Early warning system for meningitis outbreaks using WHO AFRO data | West African Meningitis Belt", 
               className="subtitle"),
        
        # Share & Export Buttons Row
        html.Div([
            html.Button("📧 Email Report", id="email-btn", className="btn-email"),
            html.Button("📄 Download PDF", id="pdf-btn", className="btn-pdf"),
            html.Button("📱 Share on WhatsApp", id="whatsapp-btn", className="btn-whatsapp"),
            html.Button("🐦 Share on X (Twitter)", id="twitter-btn", className="btn-twitter"),
            html.Button("🔗 Copy Link", id="copy-btn", className="btn-copy"),
        ], className="button-group"),
        
        # Email Input (hidden initially)
        html.Div([
            html.Label("📧 Enter Email Address:", style={'fontWeight': 'bold', 'marginRight': '10px'}),
            dcc.Input(id="email-input", type="email", placeholder="health@ministry.gov", 
                     style={'padding': '8px', 'width': '250px', 'borderRadius': '5px', 'border': '1px solid #ccc'}),
            html.Button("Send", id="send-email-btn", 
                       style={'backgroundColor': '#28a745', 'color': 'white', 'padding': '8px 16px',
                              'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer', 'marginLeft': '10px'})
        ], id="email-input-container", className="email-container"),
        
        # Filters Row
        html.Div([
            html.Div([
                html.Label("Select Country:", style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='country-dropdown',
                    options=[{'label': '🌍 All Countries', 'value': 'ALL'}] + 
                            [{'label': c, 'value': c} for c in sorted(df['country'].unique())],
                    value='ALL'
                )
            ], className="filter-item"),
            
            html.Div([
                html.Label("Select Year:", style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='year-dropdown',
                    options=[{'label': '📅 All Years', 'value': 'ALL'}] + 
                            [{'label': str(y), 'value': y} for y in sorted(df['year'].unique())],
                    value='ALL'
                )
            ], className="filter-item"),
            
            html.Div([
                html.Label("Select Month:", style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='month-dropdown',
                    options=[{'label': '📆 All Months', 'value': 'ALL'}] + 
                            [{'label': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][i-1], 'value': i} for i in range(1,13)],
                    value='ALL'
                )
            ], className="filter-item"),
        ], className="filter-container"),
        
        # KPI Cards
        html.Div([
            html.Div([
                html.H3("🦟 Total Cases"),
                html.H2(id='total-cases', style={'color': '#dc3545'})
            ], className="kpi-card"),
            
            html.Div([
                html.H3("💀 Total Deaths"),
                html.H2(id='total-deaths', style={'color': '#fd7e14'})
            ], className="kpi-card"),
            
            html.Div([
                html.H3("⚠️ Outbreaks"),
                html.H2(id='total-outbreaks', style={'color': '#dc3545'})
            ], className="kpi-card"),
            
            html.Div([
                html.H3("📊 Mortality Rate"),
                html.H2(id='mortality-rate', style={'color': '#28a745'})
            ], className="kpi-card"),
        ], style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'center', 'marginBottom': '30px'}),
        
        # Charts Row
        html.Div([
            dcc.Graph(id='cases-trend', style={'width': '48%', 'display': 'inline-block'}),
            dcc.Graph(id='outbreak-bar', style={'width': '48%', 'display': 'inline-block'})
        ], style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-between'}),
        
        html.Div([
            dcc.Graph(id='seasonal-heatmap', style={'width': '48%', 'display': 'inline-block'}),
            dcc.Graph(id='risk-gauge', style={'width': '48%', 'display': 'inline-block'})
        ], style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-between', 'marginTop': '20px'}),
        
        # Prediction Section
        html.Div([
            html.H3("🎯 Predict Meningitis Risk", style={'marginTop': '30px', 'color': '#1b5e20'}),
            html.Div([
                html.Div([
                    html.Label("📅 Month:", style={'fontWeight': 'bold'}),
                    dcc.Slider(id='month-slider', min=1, max=12, step=1, value=3,
                              marks={1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',
                                    7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'})
                ], className="slider-item"),
                
                html.Div([
                    html.Label("📊 Expected Cases:", style={'fontWeight': 'bold'}),
                    dcc.Slider(id='cases-slider', min=100, max=2000, step=100, value=800,
                              marks={i: str(i) for i in range(0, 2200, 400)})
                ], className="slider-item"),
                
                html.Div([
                    html.Label("📍 Country:", style={'fontWeight': 'bold'}),
                    dcc.Dropdown(
                        id='predict-country',
                        options=[{'label': c, 'value': c} for c in countries],
                        value='Nigeria'
                    )
                ], className="slider-item")
            ], className="prediction-sliders"),
            
            html.Div([
                html.Button("🔮 Predict Outbreak Risk", id='predict-btn', className="btn-predict")
            ], style={'textAlign': 'center', 'marginTop': '20px'}),
            
            html.Div(id='prediction-result', className="prediction-result")
        ]),
        
        # Data Table
        html.Div([
            html.H3("📋 Historical Meningitis Data (West Africa)", style={'marginTop': '30px', 'color': '#1b5e20'}),
            dash_table.DataTable(
                id='data-table',
                columns=[{"name": i, "id": i} for i in ['country', 'year', 'month', 'cases', 'deaths', 'outbreak']],
                style_table={'overflowX': 'auto'},
                style_header={'backgroundColor': '#28a745', 'color': 'white', 'fontWeight': 'bold'},
                style_cell={'textAlign': 'left', 'padding': '10px'},
                page_size=8,
                export_format='csv',
                export_headers='display'
            ),
        ], className="data-table-container")
    ], className="main-container")
])

# Callbacks
@app.callback(
    [Output('total-cases', 'children'),
     Output('total-deaths', 'children'),
     Output('total-outbreaks', 'children'),
     Output('mortality-rate', 'children'),
     Output('cases-trend', 'figure'),
     Output('outbreak-bar', 'figure'),
     Output('seasonal-heatmap', 'figure'),
     Output('data-table', 'data')],
    [Input('country-dropdown', 'value'),
     Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value')]
)
def update_dashboard(country, year, month):
    filtered_df = df.copy()
    if country != 'ALL':
        filtered_df = filtered_df[filtered_df['country'] == country]
    if year != 'ALL':
        filtered_df = filtered_df[filtered_df['year'] == year]
    if month != 'ALL':
        filtered_df = filtered_df[filtered_df['month'] == month]
    
    total_cases = f"{filtered_df['cases'].sum():,.0f}"
    total_deaths = f"{filtered_df['deaths'].sum():,.0f}"
    total_outbreaks = f"{filtered_df['outbreak'].sum()}"
    mortality = f"{(filtered_df['deaths'].sum() / filtered_df['cases'].sum() * 100):.1f}%" if filtered_df['cases'].sum() > 0 else "0%"
    
    # Trend chart
    trend_df = filtered_df.groupby('year')['cases'].sum().reset_index()
    trend_fig = px.line(trend_df, x='year', y='cases', title='📈 Meningitis Cases by Year',
                        markers=True, color_discrete_sequence=['#28a745'])
    trend_fig.update_layout(height=400, plot_bgcolor='white')
    
    # Bar chart
    bar_df = filtered_df.groupby('country')['cases'].sum().reset_index()
    bar_fig = px.bar(bar_df, x='country', y='cases', title='📊 Cases by Country (West Africa)',
                     color='cases', color_continuous_scale='Greens')
    bar_fig.update_layout(height=400, plot_bgcolor='white')
    
    # Heatmap
    heatmap_df = filtered_df.groupby(['country', 'month'])['cases'].sum().reset_index()
    heatmap_fig = px.density_heatmap(heatmap_df, x='month', y='country', z='cases',
                                      title='🌡️ Seasonal Pattern (Month × Country)',
                                      color_continuous_scale='Greens',
                                      labels={'month': 'Month', 'cases': 'Cases'})
    heatmap_fig.update_layout(height=400, plot_bgcolor='white')
    
    # Risk Gauge
    risk_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=min(100, (filtered_df['cases'].mean() / 1000) * 100),
        title={'text': "Current Risk Level"},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#28a745"},
            'steps': [
                {'range': [0, 30], 'color': "green"},
                {'range': [30, 60], 'color': "yellow"},
                {'range': [60, 100], 'color': "red"}
            ]
        }
    ))
    risk_gauge.update_layout(height=400, plot_bgcolor='white')
    
    table_data = filtered_df[['country', 'year', 'month', 'cases', 'deaths', 'outbreak']].to_dict('records')
    
    return total_cases, total_deaths, total_outbreaks, mortality, trend_fig, bar_fig, heatmap_fig, table_data

@app.callback(
    Output('prediction-result', 'children'),
    [Input('predict-btn', 'n_clicks')],
    [State('month-slider', 'value'),
     State('cases-slider', 'value'),
     State('predict-country', 'value')]
)
def make_prediction(n_clicks, month, cases, country):
    if n_clicks is None:
        return "Adjust the sliders and click 'Predict Outbreak Risk'"
    
    dry_season = month in [12,1,2,3,4,5,6]
    risk = 0
    
    if dry_season:
        risk += 40
    if month in [12,1,2]:
        risk += 20
    if cases > 800:
        risk += 30
    elif cases > 400:
        risk += 15
    if country in ['Nigeria', 'Burkina Faso', 'Niger']:
        risk += 10
    
    risk = min(risk, 95)
    
    if risk >= 60:
        level = "🔴 HIGH RISK"
        rec = "🚨 Immediate action: activate surveillance, pre-position vaccines, health worker training"
        color = "#dc3545"
    elif risk >= 30:
        level = "🟡 MEDIUM RISK"
        rec = "⚠️ Monitor closely: enhance case reporting, community awareness campaigns"
        color = "#fd7e14"
    else:
        level = "🟢 LOW RISK"
        rec = "✅ Routine surveillance: maintain standard prevention measures"
        color = "#28a745"
    
    return html.Div([
        html.H4(f"Outbreak Risk: {level}", style={'color': color, 'fontSize': 'clamp(18px, 4vw, 24px)'}),
        html.P(rec, style={'marginTop': '10px', 'fontSize': 'clamp(14px, 3vw, 16px)'}),
        html.P(f"📍 {country} | 📅 Month {month} | 📊 Expected Cases: {cases:,}", 
               style={'color': '#666', 'marginTop': '10px'})
    ])

# Email input toggle
@app.callback(
    Output('email-input-container', 'style'),
    [Input('email-btn', 'n_clicks')],
    prevent_initial_call=True
)
def toggle_email_input(n_clicks):
    if n_clicks:
        return {'textAlign': 'center', 'marginTop': '10px', 'display': 'block'}
    return {'textAlign': 'center', 'marginTop': '10px', 'display': 'none'}

# WhatsApp share
@app.callback(
    Output('whatsapp-btn', 'n_clicks'),
    [Input('whatsapp-btn', 'n_clicks')],
    prevent_initial_call=True
)
def share_whatsapp(n_clicks):
    if n_clicks:
        import webbrowser
        text = "🦠 West Africa Meningitis Outbreak Predictor - Check out this dashboard for early warning!"
        url = "http://localhost:8051"
        webbrowser.open(f"https://wa.me/?text={text}%20{url}")
    return 0

# Twitter share
@app.callback(
    Output('twitter-btn', 'n_clicks'),
    [Input('twitter-btn', 'n_clicks')],
    prevent_initial_call=True
)
def share_twitter(n_clicks):
    if n_clicks:
        import webbrowser
        text = "🦠 I'm tracking meningitis outbreaks in West Africa using AI! Check out the dashboard:"
        url = "http://localhost:8051"
        webbrowser.open(f"https://twitter.com/intent/tweet?text={text}%20{url}")
    return 0

# Copy link
@app.callback(
    Output('copy-btn', 'n_clicks'),
    [Input('copy-btn', 'n_clicks')],
    prevent_initial_call=True
)
def copy_link(n_clicks):
    if n_clicks:
        try:
            import pyperclip
            pyperclip.copy("http://localhost:8051")
            print("✅ Link copied to clipboard!")
        except:
            print("⚠️ Please install pyperclip: pip install pyperclip")
    return 0

if __name__ == '__main__':
    app.run(debug=True, port=8051)