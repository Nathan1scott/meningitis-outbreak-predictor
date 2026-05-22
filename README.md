# 🦠 West Africa Meningitis Outbreak Predictor

[![Python](https://img.shields.io/badge/Python-3.10-blue)](https://python.org)
[![Dash](https://img.shields.io/badge/Dash-4.1.0-red)](https://dash.plotly.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

An AI-powered early warning system for meningitis outbreaks in the African Meningitis Belt.

## Problem Statement

Meningitis kills thousands annually in West Africa's "Meningitis Belt" during dry season (December-June). Health ministries lack real-time predictive tools.

## Key Features

- Real WHO AFRO Data - Historical meningitis records for 10+ West African countries
- Seasonal Prediction - Predicts outbreaks 4-6 weeks ahead using dry season patterns
- Interactive Dashboard - Filter by country, year, month
- Risk Scoring - HIGH/MEDIUM/LOW risk levels with color-coded alerts
- Share & Export - Email reports, PDF export, WhatsApp/Twitter sharing
- Mobile Responsive - Works on phones, tablets, desktops

## Tech Stack

- Python, Dash, Plotly
- Pandas, NumPy
- Scikit-learn Random Forest

## Quick Start

```bash
git clone https://github.com/Nathan1scott/meningitis-outbreak-predictor.git
cd meningitis-outbreak-predictor
pip install -r requirements.txt
python meningitis_dashboard.py
