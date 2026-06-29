# Enterprise Spare Parts Demand Forecasting and Inventory Optimization Platform

## Overview

This project was developed as part of my internship at **Volvo Eicher Commercial Vehicles (VECV)**.

The application provides an end-to-end solution for forecasting spare parts demand, optimizing inventory, monitoring inventory risks, and generating actionable recommendations through an interactive Streamlit dashboard.

The objective of the project is to help improve spare parts availability, reduce inventory costs, and support better planning decisions using data-driven forecasting techniques.

---

## Features

### Data Processing

- Data validation
- Demand profiling
- ABC Inventory Analysis
- XYZ Inventory Analysis

### Forecasting

- Moving Average
- Simple Exponential Smoothing
- Holt Linear Trend
- Holt-Winters
- ARIMA
- Croston Forecasting
- Automatic Best Model Selection
- Forecast Accuracy Evaluation
- 1, 3, 6 and 12 Month Forecast Generation

### Inventory Optimization

- Safety Stock Calculation
- Reorder Point Calculation
- Inventory Coverage Analysis
- Inventory Risk Classification

### Recommendation Engine

- Automatic inventory recommendations
- Risk-based replenishment suggestions

### Interactive Dashboards

- Executive Dashboard
- Demand Forecasting Dashboard
- Inventory Dashboard
- Recommendation Center
- Forecast Accuracy Dashboard
- Risk Monitoring Dashboard
- Planning Dashboard

---

## Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- Scikit-learn
- Statsmodels

---

## Project Structure

```
VECV_SpareParts/

├── app/
│   ├── Home.py
│   ├── assets/
│   └── pages/
│
├── data/
│
├── outputs/
│   └── final/
│
├── src/
│
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository.

```
git clone <repository-url>
```

Install the required packages.

```
pip install -r requirements.txt
```

Run the application.

```
streamlit run app/Home.py
```

---

## Outputs

The application generates the following outputs:

- Demand Profile
- ABC Analysis
- Best Forecasting Model
- Forecast Results (1, 3, 6 and 12 Months)
- Inventory Optimization Report
- Recommendation Report
- Forecast Accuracy Report

---

## Future Scope

- Integration with ERP systems
- Real-time forecasting
- Automated inventory replenishment
- Cloud deployment
- Advanced machine learning models

---

## Developed By

**Kavya Mehta**

B.Tech Computer Science and Engineering (AI & Robotics)

Vellore Institute of Technology Chennai

Intern at Volvo Eicher Commercial Vehicles (VECV)
