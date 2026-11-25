# Smart Supply Chain Analytics

### Data Analyst Project | Python • MySQL • Power BI • Streamlit

## Project Overview

Smart Supply Chain Analytics is a data analytics project focused on analyzing shipment operations, delivery performance, supplier reliability, transportation efficiency and logistics costs.

A global logistics company manages shipments across multiple suppliers, warehouses, cities and transportation routes. Delivery delays and cost variations can occur due to several factors, including weather conditions, traffic levels, supplier performance, fuel costs and port congestion.

The objective of this project is to analyze shipment data, identify meaningful business patterns, generate actionable insights and support data-driven decision-making using Python, MySQL, Power BI and Streamlit.

## Business Objectives

- Analyze total shipment volume and delivery performance.
- Identify delayed shipments and calculate average delay hours.
- Evaluate supplier performance and reliability.
- Identify high-risk routes based on observed delivery delays.
- Compare transportation modes (Truck, Rail, Air and Ship).
- Analyze the impact of weather, traffic and port congestion on delivery delays.
- Analyze delivery costs and fuel expenses.
- Develop an interactive Power BI dashboard.
- Build a simple Streamlit application for exploring shipment records.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data cleaning, EDA, analysis and business metrics |
| Pandas & NumPy | Data manipulation and analysis |
| Matplotlib & Seaborn | Data visualization |
| MySQL | Database management and SQL analysis |
| Power BI | Interactive dashboards and business insights |
| Streamlit | Interactive shipment data explorer |

## Dataset Description

The project uses a supply chain dataset containing **50,000+ shipment records**.

The dataset includes the following categories:

| Category | Important Columns |
|---|---|
| Shipment | Shipment_ID, Order_ID, Shipment_Date, Delivery_Date, Delivery_Time |
| Supplier | Supplier_ID, Supplier_Name, Supplier_Rating, Supplier_Location |
| Warehouse | Warehouse_ID, Warehouse_City, Warehouse_Capacity |
| Transportation | Transport_Mode, Route_Distance, Fuel_Cost |
| External Factors | Weather_Condition, Traffic_Level, Port_Congestion, Holiday_Flag |
| Business Metrics | Delivery_Cost, Delay_Hours, Customer_Priority |
| Status | Disruption_Status |

## Python – Data Cleaning & Exploratory Data Analysis

Python is used to clean, transform and analyze the shipment dataset.

**Data Cleaning:**
- Loading and inspecting raw shipment data.
- Handling missing values.
- Identifying and removing duplicate records where required.
- Converting date columns into appropriate datetime formats.
- Validating numerical columns.
- Standardizing categorical values.
- Preparing the cleaned dataset for further analysis.

**Exploratory Data Analysis (EDA):**

- Total shipment analysis.
- Delayed shipment analysis.
- Delay rate and average delay hours.
- Shipment trends over time.
- Supplier performance analysis.
- Route performance analysis.
- Transportation mode comparison.
- Weather and traffic impact on delays.
- Port congestion analysis.
- Delivery cost analysis.

**Derived Business Metrics:**

- Delay Rate
- Average Delay Hours by Supplier
- Average Delay Hours by Route
- Supplier Reliability Score
- Route Risk Score
- Transportation Efficiency Metric

## MySQL – Database & SQL Analysis

MySQL is used to store structured shipment data and perform analytical queries.

**Database:** `smart_supply_chain`

**Tables:**
- Suppliers
- Warehouses
- Shipments

**SQL Concepts Implemented:**

- CREATE DATABASE and CREATE TABLE
- INSERT and SELECT
- WHERE, GROUP BY, HAVING and ORDER BY
- INNER JOIN and LEFT JOIN
- CASE Statements
- Common Table Expressions (CTEs)
- Window Functions (RANK, DENSE_RANK)
- Views
- Aggregate Functions (COUNT, SUM, AVG)

**Business Questions Explored:**

- Which suppliers handle the highest shipment volume?
- Which suppliers have the highest average delivery delays?
- Which routes have the highest delay rates?
- Which transportation mode has the lowest average delivery cost?
- Which warehouses handle the highest shipment volume?
- How do traffic and weather conditions affect delivery delays?
- What are the top 10 high-risk routes?
- Which suppliers have the highest reliability?

## Power BI – Interactive Dashboard

Power BI serves as the primary business intelligence and visualization tool for the project.

The dashboard is organized into five analytical pages:

**1. Executive Overview**
- Total Shipments
- Delayed Shipments
- Delay Rate
- Average Delay Hours
- Total Delivery Cost
- Shipment, Delay and Cost Trends

**2. Supplier Analytics**
- Supplier Shipment Volume
- Average Delay by Supplier
- Supplier Delay Rate
- Supplier Reliability
- High-Risk Suppliers

**3. Route Analytics**
- Route Performance
- Top High-Risk Routes
- Average Delay by Route
- Delay Rate by Route
- Route Distance vs Delivery Cost

**4. Transportation Analytics**
- Shipment Volume by Transportation Mode
- Average Delay by Mode
- Average Delivery Cost by Mode
- Fuel Cost Comparison

**5. External Factors & Delay**
- Weather vs Delay
- Traffic vs Delay
- Port Congestion vs Delay
- Holiday Comparison
- Delay Distribution

## Streamlit – Interactive Data Explorer

A simple Streamlit application is developed to provide an interactive interface for exploring shipment records.

**Key Features:**
- Shipment dataset overview.
- Interactive shipment data table.
- Filters for Supplier, Warehouse and Transport Mode.
- Date range filtering.
- Summary statistics for filtered shipments.
- Selected shipment details.
- Download filtered data as CSV.

The Streamlit application complements the Power BI dashboard by providing a simple way to explore individual shipment records.

## Project Workflow

1. Load the raw shipment dataset using Python.
2. Perform data cleaning and validation.
3. Conduct Exploratory Data Analysis (EDA).
4. Calculate important business metrics.
5. Export the cleaned dataset.
6. Create the MySQL database and tables.
7. Load cleaned data into MySQL.
8. Perform analytical SQL queries.
9. Connect the analytical data to Power BI.
10. Develop interactive Power BI dashboards.
11. Build the Streamlit shipment data explorer.
12. Validate important results across Python, MySQL, Power BI and Streamlit.
13. Prepare final business insights and recommendations.

## Project Structure

```text
Smart_Supply_Chain_Data_Analyst_Project/
│
├── data/
│   ├── raw_shipments.csv
│   └── cleaned_shipments.csv
│
├── python/
│   ├── Data_Cleaning.ipynb
│   ├── EDA.ipynb
│   └── Feature_Analysis.ipynb
│
├── mysql/
│   ├── schema.sql
│   ├── queries.sql
│   └── views.sql
│
├── powerbi/
│   └── Smart_Supply_Chain_Analytics.pbix
│
├── streamlit_app/
│   └── app.py
│
└── README.md
```

## Expected Business Insights

This project aims to identify meaningful patterns that can help improve supply chain operations.

- Identify suppliers experiencing higher delivery delays.
- Discover routes with higher observed delay rates.
- Compare transportation modes based on cost and delivery performance.
- Understand how external factors influence shipment delays.
- Identify unusual shipment, delay and cost patterns.
- Support better supplier, route and transportation decisions through data-driven insights.

## Running the Streamlit Application

**Step 1: Clone the repository**

```bash
git clone https://github.com/nupshyam-nau/Smart-Supply-Chain-Analysis.git
```

**Step 2: Navigate to the project directory**

```bash
cd Smart-Supply-Chain-Analysis
```

**Step 3: Install the required packages**

```bash
pip install streamlit pandas
```

**Step 4: Run the application**

```bash
streamlit run streamlit_app/app.py
```

The application will open in your default web browser.

## Project Team

This is a collaborative Data Analyst project developed by:

1. Neha Upshyam
2. Ayush Junankar

## Project Scope

This project focuses on Data Analytics and Business Intelligence using Python, MySQL, Power BI and Streamlit.

It does not include Machine Learning models or predictive analytics. The primary dashboard is developed in Power BI, while Streamlit is used exclusively as a simple interactive data explorer.

---

**Built with Python, MySQL, Power BI & Streamlit.**
