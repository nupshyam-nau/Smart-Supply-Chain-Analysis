import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import base64

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Supply Chain Analysis",
    page_icon="supplychainlogo.png",
    layout="wide"
)

# Logo
st.logo(
    "supplychainlogo.png",
    size="large",
    icon_image="supplychainlogo.png"
)


# =====================================================
# SIDE BAR
# =====================================================

with st.sidebar:
    st.image("supplychainlogo.png", width=220)

    file = st.file_uploader(
        "Upload Dataset (CSV / Excel)",
        type=["csv", "xlsx"]
    )

    st.markdown("### Navigation")

    menu = st.radio(
        "Go to",
        ["Data Overview", "Statistics", "Visualization", "Filter Data"]
    )

    st.markdown("---")

    st.caption("Built with ❤️ using Streamlit")


# =====================================================
# LOAD DATA
# =====================================================

if file is not None:

    try:

        if file.name.endswith(".csv"):
            df = pd.read_csv(file)

        else:
            df = pd.read_excel(file)

        st.sidebar.success(
            "Dataset Loaded Successfully ✅"
        )

    except Exception as e:

        st.error(
            f"Error loading dataset: {e}"
        )

        st.stop()

else:

    df = pd.read_csv(
        "shipments.csv"
    )

    st.sidebar.info(
        "Default Dataset is Loaded"
    )


# =====================================================
# DATE CONVERSION
# =====================================================

df["Shipment_Date"] = pd.to_datetime(
    df["Shipment_Date"],
    errors="coerce"
)


# =====================================================
# DATA OVERVIEW
# =====================================================

if menu == "Data Overview":

    # =====================================================
    # LOAD BACKGROUND IMAGE
    # =====================================================

        with open("scimage.jpg", "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()

        # Hero Section
        st.markdown(
        f"""
    <style>

    .hero {{
        height: 520px;
        width: 100%;
        position: relative;
        overflow: hidden;
        border-radius: 15px;

        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
    }}

    /* Blurred background */
    .hero::before {{
        content: "";
        position: absolute;
        top: -15px;
        left: -15px;
        right: -15px;
        bottom: -15px;

        background-image:
            linear-gradient(
                rgba(0,0,0,0.30),
                rgba(0,0,0,0.30)
            ),
            url("data:image/png;base64,{encoded}");

        background-size: cover;
        background-position: center;

        filter: blur(3px);

        z-index: 0;
    }}

    /* Text stays sharp */
    .hero-content {{
        position: relative;
        z-index: 1;
    }}

    .hero h1 {{
        color: white;
        font-size: 62px;
        font-weight: 800;
        margin: 0 0 20px 0;

        text-shadow:
            3px 3px 8px rgba(0,0,0,0.9);
    }}

    .hero p {{
        color: white;
        font-size: 26px;
        font-weight: 400;
        line-height: 1.5;
        max-width: 850px;
        margin: 0 auto;

        text-shadow:
            2px 2px 6px rgba(0,0,0,0.9);
    }}

    </style>

    <div class="hero"><div class="hero-content"><h1> Smart Supply Chain Analysis </h1><p> Explore supply chain performance, shipments, delivery times, inventory, suppliers, customers, and business insights.</p></div></div>
    """,
        unsafe_allow_html=True
    )

        st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)

    # =====================================================
    # KEY PERFORMANCE INDICATORS
    # =====================================================

        # 1. Total Shipments

        total_shipments = df[
                "Shipment_ID"
            ].nunique()

            # 2. On-Time Rate

        valid_status = df[
                "Disruption_Status"
            ].notna().sum()

        on_time_shipments = (
                df["Disruption_Status"] == "On Time"
            ).sum()

        on_time_rate = (
                on_time_shipments / valid_status * 100
                if valid_status > 0
                else 0
            )

            # 3. Average Delay Hours

        avg_delay = df[
                "Delay_Hours"
            ].mean()

            # 4. Delay Rate

        delayed_shipments = df["Disruption_Status"].isin(
            ["Delayed", "Highly Delayed", "Disrupted"]
        ).sum()

        delay_rate = ( delayed_shipments / valid_status * 100
            if valid_status > 0
            else 0
        )

            # 5. Total Delivery Cost

        total_delivery_cost = df[
                "Delivery_Cost"
            ].sum()

            # 6. Total Fuel Cost

        total_fuel_cost = df[
                "Fuel_Cost"
            ].sum()


    # =====================================================
    # KPI CARDS
    # =====================================================

        col1, col2, col3, col4, col5, col6 = st.columns(6)


        with col1:

            st.metric(
                label="Total Shipments",
                value=f"{total_shipments:,}"
            )


        with col2:

            st.metric(
                label="On-Time Rate",
                value=f"{on_time_rate:.2f}%"
            )


        with col3:

            st.metric(
                label="Avg Delay",
                value=f"{avg_delay:.2f} hrs"
            )

        with col4:

            st.metric(
                label="Delay Rate",
                value=f"{delay_rate:.2f}%"
            )

        def compact_currency(value):
            if value >= 1_000_000_000:
                return f"₹{value / 1_000_000_000:.2f}B"
            elif value >= 1_000_000:
                return f"₹{value / 1_000_000:.2f}M"
            elif value >= 1_000:
                return f"₹{value / 1_000:.2f}K"
            else:
                return f"₹{value:.2f}"

        with col5:

            st.metric(
        "Total Delivery Cost",
        compact_currency(total_delivery_cost)
        )


        with col6:

            st.metric(
        "Total Fuel Cost",
        compact_currency(total_fuel_cost)
        )


        st.markdown("---")


        # =====================================================
        # DATASET OVERVIEW
        # =====================================================

        st.header("Dataset Overview")


        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                label="Total Records",
                value=f"{df.shape[0]:,}"
            )


        with col2:

            st.metric(
                label="Total Columns",
                value=f"{df.shape[1]:,}"
            )


        with col3:

            st.metric(
                label="Total Suppliers",
                value=f"{df['Supplier_ID'].nunique():,}"
            )


        with col4:

            st.metric(
                label="Total Warehouses",
                value=f"{df['Warehouse_ID'].nunique():,}"
            )

        st.markdown("---")


        # =====================================================
        # DATA DESCRIPTION
        # =====================================================

        st.subheader("About the Dataset")

        st.write(
            f"""
            A comprehensive **Supply Chain & Shipment dataset** containing
            **{len(df):,} shipment records** with information on
            transportation, suppliers, warehouses, delivery performance,
            costs, delays, traffic, weather, and disruptions.
            """
        )


        st.subheader("Purpose")

        st.write(
            """
            Analyze shipment data to improve on-time deliveries, 
            reduce transportation costs, identify the impact of 
            traffic and weather conditions, and to increase overall 
            supply chain efficiency through data-driven insights.
            """
        )


    # =====================================================
    # DATASET SUMMARY
    # =====================================================

        st.subheader("Dataset Summary")


        summary_data = {

            "Metric": [
                "Total Records",
                "Total Columns",
                "Unique Shipments",
                "Unique Orders",
                "Suppliers",
                "Warehouses",
                "Transport Modes",
                "Weather Conditions",
                "Traffic Levels",
                "Customer Priorities",
                "Start Date",
                "End Date"
            ],

            "Value": [
                f"{df.shape[0]:,}",
                f"{df.shape[1]:,}",
                f"{df['Shipment_ID'].nunique():,}",
                f"{df['Order_ID'].nunique():,}",
                f"{df['Supplier_ID'].nunique():,}",
                f"{df['Warehouse_ID'].nunique():,}",
                f"{df['Transport_Mode'].nunique():,}",
                f"{df['Weather_Condition'].nunique():,}",
                f"{df['Traffic_Level'].nunique():,}",
                f"{df['Customer_Priority'].nunique():,}",

                (
                    df["Shipment_Date"].min().strftime(
                        "%d %B %Y"
                    )
                    if df["Shipment_Date"].notna().any()
                    else "N/A"
                ),

                (
                    df["Shipment_Date"].max().strftime(
                        "%d %B %Y"
                    )
                    if df["Shipment_Date"].notna().any()
                    else "N/A"
                )
            ]

        }


        summary_df = pd.DataFrame(
            summary_data
        )


        st.dataframe(
            summary_df,
            use_container_width=True,
            hide_index=True
        )


        # =====================================================
        # DATA PREVIEW
        # =====================================================

        st.markdown("---")

        st.header("Data Preview")


        st.dataframe(
            df,
            use_container_width=True,
            height=600
        )


# =====================================================
# STATISTICS
# =====================================================

elif menu == "Statistics":

    st.subheader("Dataset Statistics")

    st.write(
            df.describe(
                include="all"
            )
        )

        # -------------------------------------------------
        # Missing Values Per Column
        # -------------------------------------------------

    st.subheader("Missing Values Per Column")

    st.bar_chart(
            df.isnull().sum()
        )

        # -------------------------------------------------
        # Duplicate Rows
        # -------------------------------------------------

    st.subheader("Duplicate Rows")

    st.write(
            f"Total Duplicate Rows: **{df.duplicated().sum():,}**"
        )

        # -------------------------------------------------
        # Data Types
        # -------------------------------------------------

    st.subheader("Data Types")

    st.dataframe(
            df.dtypes.to_frame("Data Type"),
            use_container_width=True
        )


# =====================================================
# VISUALIZATION
# =====================================================

elif menu == "Visualization":

    st.subheader("Interactive Visualizations")

# ============================================================
# INTERACTIVE VISUALIZATIONS
# ============================================================

    st.markdown(
        """
        <p style="text-align:center; color:gray;">
            Explore shipment performance across transportation, delivery,
            cost, suppliers, weather, disruptions and time.
        </p>
        """,
        unsafe_allow_html=True
    )

    # ------------------------------------------------------------
    # DATA PREPARATION
    # ------------------------------------------------------------

    viz_df = df.copy()

    # Date conversion
    if "Shipment_Date" in viz_df.columns:
        viz_df["Shipment_Date"] = pd.to_datetime(
            viz_df["Shipment_Date"],
            errors="coerce"
        )

    # Numeric conversion
    for col in [
        "Delay_Hours",
        "Delivery_Cost",
        "Fuel_Cost",
        "Route_Distance",
        "Holiday_Flag"
    ]:
        if col in viz_df.columns:
            viz_df[col] = pd.to_numeric(
                viz_df[col],
                errors="coerce"
            )


    # ------------------------------------------------------------
    # HELPER FUNCTION
    # ------------------------------------------------------------

    def unique_shipments(data, group_column):

        return (
            data.groupby(group_column)["Shipment_ID"]
            .nunique()
            .reset_index(name="Shipment_Count")
        )


    # ============================================================
    # 1. TRANSPORTATION ANALYSIS
    # ============================================================

    with st.expander(
        "1. Transportation Analysis",
        expanded=False
    ):

        analysis = st.selectbox(
            "Select Analysis",
            [
                "Shipments by Transport Mode",
                "Average Delay by Transport Mode",
                "Transport Mode Cost Comparison"
            ],
            key="transport_analysis"
        )

        # --------------------------------------------------------
        # Shipments by Transport Mode
        # --------------------------------------------------------

        if analysis == "Shipments by Transport Mode":

            chart_type = st.selectbox(
                "Chart Type",
                [
                    "Bar",
                    "Donut"
                ],
                key="transport_shipments_chart"
            )

            temp = unique_shipments(
                viz_df.dropna(
                    subset=["Transport_Mode"]
                ),
                "Transport_Mode"
            )

            if chart_type == "Bar":

                fig = px.bar(
                    temp,
                    x="Transport_Mode",
                    y="Shipment_Count",
                    title="Shipments by Transport Mode",
                    labels={
                        "Transport_Mode": "Transport Mode",
                        "Shipment_Count": "Shipment Count"
                    },
                    text_auto=True
                )

            else:

                fig = px.pie(
                    temp,
                    names="Transport_Mode",
                    values="Shipment_Count",
                    hole=0.45,
                    title="Shipments by Transport Mode"
                )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # --------------------------------------------------------
        # Average Delay by Transport Mode
        # --------------------------------------------------------

        elif analysis == "Average Delay by Transport Mode":

            chart_type = st.selectbox(
                "Chart Type",
                [
                    "Bar",
                    "Column"
                ],
                key="transport_delay_chart"
            )

            temp = (
                viz_df.dropna(
                    subset=[
                        "Transport_Mode",
                        "Delay_Hours"
                    ]
                )
                .groupby("Transport_Mode")["Delay_Hours"]
                .mean()
                .reset_index()
            )

            if chart_type == "Bar":

                fig = px.bar(
                    temp.sort_values("Delay_Hours"),
                    y="Transport_Mode",
                    x="Delay_Hours",
                    orientation="h",
                    title="Average Delay by Transport Mode",
                    labels={
                        "Delay_Hours":
                        "Average Delay Hours"
                    },
                    text_auto=".2f"
                )

            else:

                fig = px.bar(
                    temp,
                    x="Transport_Mode",
                    y="Delay_Hours",
                    title="Average Delay by Transport Mode",
                    labels={
                        "Delay_Hours":
                        "Average Delay Hours"
                    },
                    text_auto=".2f"
                )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # --------------------------------------------------------
        # Transport Mode Cost Comparison
        # --------------------------------------------------------

        else:

            chart_type = st.selectbox(
                "Chart Type",
                [
                    "Grouped Bar",
                    "Stacked Bar"
                ],
                key="transport_cost_chart"
            )

            temp = (
                viz_df.groupby("Transport_Mode")[
                    [
                        "Delivery_Cost",
                        "Fuel_Cost"
                    ]
                ]
                .mean()
                .reset_index()
            )

            temp_long = temp.melt(
                id_vars="Transport_Mode",
                value_vars=[
                    "Delivery_Cost",
                    "Fuel_Cost"
                ],
                var_name="Cost_Type",
                value_name="Average_Cost"
            )

            if chart_type == "Grouped Bar":

                fig = px.bar(
                    temp_long,
                    x="Transport_Mode",
                    y="Average_Cost",
                    color="Cost_Type",
                    barmode="group",
                    title="Transport Mode Cost Comparison",
                    labels={
                        "Average_Cost":
                        "Average Cost"
                    }
                )

            else:

                fig = px.bar(
                    temp_long,
                    x="Transport_Mode",
                    y="Average_Cost",
                    color="Cost_Type",
                    barmode="stack",
                    title="Transport Mode Cost Comparison",
                    labels={
                        "Average_Cost":
                        "Average Cost"
                    }
                )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    # ============================================================
    # 2. DELIVERY & DELAY ANALYSIS
    # ============================================================

    with st.expander(
        "2. Delivery & Delay Analysis",
        expanded=False
    ):

        analysis = st.selectbox(
            "Select Analysis",
            [
                "Delay Distribution",
                "Average Delay by Customer Priority",
                "Delay Trend Over Time"
            ],
            key="delivery_delay_analysis"
        )

        # --------------------------------------------------------
        # Delay Distribution
        # --------------------------------------------------------

        if analysis == "Delay Distribution":

            chart_type = st.selectbox(
                "Chart Type",
                [
                    "Histogram",
                    "Box Plot"
                ],
                key="delay_distribution_chart"
            )

            temp = viz_df.dropna(
                subset=["Delay_Hours"]
            )

            if chart_type == "Histogram":

                fig = px.histogram(
                    temp,
                    x="Delay_Hours",
                    nbins=30,
                    title="Delay Distribution",
                    labels={
                        "Delay_Hours":
                        "Delay Hours"
                    }
                )

            else:

                fig = px.box(
                    temp,
                    y="Delay_Hours",
                    title="Delay Distribution",
                    labels={
                        "Delay_Hours":
                        "Delay Hours"
                    }
                )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # --------------------------------------------------------
        # Average Delay by Customer Priority
        # --------------------------------------------------------

        elif analysis == "Average Delay by Customer Priority":

            chart_type = st.selectbox(
                "Chart Type",
                [
                    "Bar",
                    "Column"
                ],
                key="priority_delay_chart"
            )

            temp = (
                viz_df.dropna(
                    subset=[
                        "Customer_Priority",
                        "Delay_Hours"
                    ]
                )
                .groupby(
                    "Customer_Priority"
                )["Delay_Hours"]
                .mean()
                .reset_index()
            )

            if chart_type == "Bar":

                fig = px.bar(
                    temp.sort_values("Delay_Hours"),
                    y="Customer_Priority",
                    x="Delay_Hours",
                    orientation="h",
                    title="Average Delay by Customer Priority",
                    text_auto=".2f"
                )

            else:

                fig = px.bar(
                    temp,
                    x="Customer_Priority",
                    y="Delay_Hours",
                    title="Average Delay by Customer Priority",
                    text_auto=".2f"
                )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # --------------------------------------------------------
        # Delay Trend Over Time
        # --------------------------------------------------------

        else:

            chart_type = st.selectbox(
                "Chart Type",
                [
                    "Line",
                    "Area"
                ],
                key="delay_trend_chart"
            )

            temp = (
                viz_df.dropna(
                    subset=[
                        "Shipment_Date",
                        "Delay_Hours"
                    ]
                )
                .groupby("Shipment_Date")["Delay_Hours"]
                .mean()
                .reset_index()
            )

            if chart_type == "Line":

                fig = px.line(
                    temp,
                    x="Shipment_Date",
                    y="Delay_Hours",
                    title="Delay Trend Over Time",
                    labels={
                        "Delay_Hours":
                        "Average Delay Hours",
                        "Shipment_Date":
                        "Shipment Date"
                    }
                )

            else:

                fig = px.area(
                    temp,
                    x="Shipment_Date",
                    y="Delay_Hours",
                    title="Delay Trend Over Time",
                    labels={
                        "Delay_Hours":
                        "Average Delay Hours",
                        "Shipment_Date":
                        "Shipment Date"
                    }
                )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    # ============================================================
    # 3. COST ANALYSIS
    # ============================================================

    with st.expander(
        "3. Cost Analysis",
        expanded=False
    ):

        analysis = st.selectbox(
            "Select Analysis",
            [
                "Delivery Cost by Transport Mode",
                "Delivery Cost vs Fuel Cost",
            ],
            key="cost_analysis"
        )

        # --------------------------------------------------------
        # Delivery Cost by Transport Mode
        # --------------------------------------------------------

        if analysis == "Delivery Cost by Transport Mode":

            chart_type = st.selectbox(
                "Chart Type",
                [
                    "Bar",
                    "Column"
                ],
                key="delivery_mode_cost_chart"
            )

            temp = (
                viz_df.groupby("Transport_Mode")[
                    "Delivery_Cost"
                ]
                .mean()
                .reset_index()
            )

            if chart_type == "Bar":

                fig = px.bar(
                    temp.sort_values("Delivery_Cost"),
                    y="Transport_Mode",
                    x="Delivery_Cost",
                    orientation="h",
                    title="Delivery Cost by Transport Mode",
                    text_auto=".2f"
                )

            else:

                fig = px.bar(
                    temp,
                    x="Transport_Mode",
                    y="Delivery_Cost",
                    title="Delivery Cost by Transport Mode",
                    text_auto=".2f"
                )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # --------------------------------------------------------
        # Delivery Cost vs Fuel Cost
        # --------------------------------------------------------

        elif analysis == "Delivery Cost vs Fuel Cost":

            chart_type = st.selectbox(
                "Chart Type",
                [
                    "Grouped Bar",
                    "Stacked Bar"
                ],
                key="delivery_fuel_cost_chart"
            )

            temp = (
                viz_df.groupby("Transport_Mode")[
                    [
                        "Delivery_Cost",
                        "Fuel_Cost"
                    ]
                ]
                .mean()
                .reset_index()
            )

            temp_long = temp.melt(
                id_vars="Transport_Mode",
                value_vars=[
                    "Delivery_Cost",
                    "Fuel_Cost"
                ],
                var_name="Cost_Type",
                value_name="Average_Cost"
            )

            if chart_type == "Grouped Bar":

                fig = px.bar(
                    temp_long,
                    x="Transport_Mode",
                    y="Average_Cost",
                    color="Cost_Type",
                    barmode="group",
                    title="Delivery Cost vs Fuel Cost"
                )

            else:

                fig = px.bar(
                    temp_long,
                    x="Transport_Mode",
                    y="Average_Cost",
                    color="Cost_Type",
                    barmode="stack",
                    title="Delivery Cost vs Fuel Cost"
                )

            st.plotly_chart(
                fig,
                use_container_width=True
            )
    # ============================================================
    # 4. SUPPLIER & WAREHOUSE ANALYSIS
    # ============================================================

    with st.expander(
        "4. Supplier & Warehouse Analysis",
        expanded=False
    ):

        analysis = st.selectbox(
            "Select Analysis",
            [
                "Top Suppliers by Shipment Volume",
                "Average Delay by Warehouse",
                "Supplier/Warehouse Shipment Distribution"
            ],
            key="supplier_warehouse_analysis"
        )

        # --------------------------------------------------------
        # Top Suppliers
        # --------------------------------------------------------

        if analysis == "Top Suppliers by Shipment Volume":

            chart_type = st.selectbox(
                "Chart Type",
                [
                    "Horizontal Bar",
                    "Column"
                ],
                key="top_supplier_chart"
            )

            temp = (
                unique_shipments(
                    viz_df.dropna(
                        subset=["Supplier_ID"]
                    ),
                    "Supplier_ID"
                )
                .sort_values(
                    "Shipment_Count",
                    ascending=False
                )
                .head(10)
            )

            if chart_type == "Horizontal Bar":

                fig = px.bar(
                    temp.sort_values("Shipment_Count"),
                    y="Supplier_ID",
                    x="Shipment_Count",
                    orientation="h",
                    title="Top 10 Suppliers by Shipment Volume",
                    text_auto=True
                )

            else:

                fig = px.bar(
                    temp,
                    x="Supplier_ID",
                    y="Shipment_Count",
                    title="Top 10 Suppliers by Shipment Volume",
                    text_auto=True
                )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # --------------------------------------------------------
        # Average Delay by Warehouse
        # --------------------------------------------------------

        elif analysis == "Average Delay by Warehouse":

            chart_type = st.selectbox(
                "Chart Type",
                [
                    "Bar",
                    "Column"
                ],
                key="warehouse_delay_chart"
            )

            temp = (
                viz_df.dropna(
                    subset=[
                        "Warehouse_ID",
                        "Delay_Hours"
                    ]
                )
                .groupby("Warehouse_ID")["Delay_Hours"]
                .mean()
                .reset_index()
                .sort_values(
                    "Delay_Hours",
                    ascending=False
                )
                .head(10)
            )

            if chart_type == "Bar":

                fig = px.bar(
                    temp.sort_values("Delay_Hours"),
                    y="Warehouse_ID",
                    x="Delay_Hours",
                    orientation="h",
                    title="Top 10 Warehouses by Average Delay",
                    text_auto=".2f"
                )

            else:

                fig = px.bar(
                    temp,
                    x="Warehouse_ID",
                    y="Delay_Hours",
                    title="Top 10 Warehouses by Average Delay",
                    text_auto=".2f"
                )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # --------------------------------------------------------
        # Supplier / Warehouse Distribution
        # --------------------------------------------------------

        else:

            chart_type = st.selectbox(
                "Chart Type",
                [
                    "Heatmap",
                    "Stacked Bar"
                ],
                key="supplier_warehouse_distribution_chart"
            )

            temp = (
                viz_df.groupby(
                    [
                        "Supplier_ID",
                        "Warehouse_ID"
                    ]
                )["Shipment_ID"]
                .nunique()
                .reset_index(
                    name="Shipment_Count"
                )
            )

            # Top 10 suppliers
            top_suppliers = (
                temp.groupby("Supplier_ID")[
                    "Shipment_Count"
                ]
                .sum()
                .nlargest(10)
                .index
            )

            temp = temp[
                temp["Supplier_ID"].isin(
                    top_suppliers
                )
            ]

            if chart_type == "Heatmap":

                pivot = temp.pivot_table(
                    index="Supplier_ID",
                    columns="Warehouse_ID",
                    values="Shipment_Count",
                    aggfunc="sum",
                    fill_value=0
                )

                fig = px.imshow(
                    pivot,
                    aspect="auto",
                    title="Supplier/Warehouse Shipment Distribution",
                    labels={
                        "x": "Warehouse",
                        "y": "Supplier",
                        "color": "Shipments"
                    }
                )

            else:

                fig = px.bar(
                    temp,
                    x="Supplier_ID",
                    y="Shipment_Count",
                    color="Warehouse_ID",
                    barmode="stack",
                    title="Supplier/Warehouse Shipment Distribution"
                )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    # ============================================================
    # 5. WEATHER & TRAFFIC ANALYSIS
    # ============================================================

    with st.expander(
        "5. Weather & Traffic Analysis",
        expanded=False
    ):

        analysis = st.selectbox(
            "Select Analysis",
            [
                "Shipments by Weather Condition",
                "Average Delay by Traffic Level",
                "Weather vs Traffic Impact on Delay"
            ],
            key="weather_traffic_analysis"
        )

        # --------------------------------------------------------
        # Shipments by Weather
        # --------------------------------------------------------

        if analysis == "Shipments by Weather Condition":

            chart_type = st.selectbox(
                "Chart Type",
                [
                    "Donut",
                    "Bar"
                ],
                key="weather_shipments_chart"
            )

            temp = unique_shipments(
                viz_df.dropna(
                    subset=["Weather_Condition"]
                ),
                "Weather_Condition"
            )

            if chart_type == "Donut":

                fig = px.pie(
                    temp,
                    names="Weather_Condition",
                    values="Shipment_Count",
                    hole=0.45,
                    title="Shipments by Weather Condition"
                )

            else:

                fig = px.bar(
                    temp,
                    x="Weather_Condition",
                    y="Shipment_Count",
                    title="Shipments by Weather Condition",
                    text_auto=True
                )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # --------------------------------------------------------
        # Average Delay by Traffic
        # --------------------------------------------------------

        elif analysis == "Average Delay by Traffic Level":

            chart_type = st.selectbox(
                "Chart Type",
                [
                    "Bar",
                    "Column"
                ],
                key="traffic_delay_chart"
            )

            temp = (
                viz_df.dropna(
                    subset=[
                        "Traffic_Level",
                        "Delay_Hours"
                    ]
                )
                .groupby("Traffic_Level")[
                    "Delay_Hours"
                ]
                .mean()
                .reset_index()
            )

            if chart_type == "Bar":

                fig = px.bar(
                    temp.sort_values("Delay_Hours"),
                    y="Traffic_Level",
                    x="Delay_Hours",
                    orientation="h",
                    title="Average Delay by Traffic Level",
                    text_auto=".2f"
                )

            else:

                fig = px.bar(
                    temp,
                    x="Traffic_Level",
                    y="Delay_Hours",
                    title="Average Delay by Traffic Level",
                    text_auto=".2f"
                )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # --------------------------------------------------------
        # Weather vs Traffic Impact
        # --------------------------------------------------------

        else:

            chart_type = st.selectbox(
                "Chart Type",
                [
                    "Heatmap",
                    "Grouped Bar"
                ],
                key="weather_traffic_impact_chart"
            )

            temp = (
                viz_df.dropna(
                    subset=[
                        "Weather_Condition",
                        "Traffic_Level",
                        "Delay_Hours"
                    ]
                )
                .groupby(
                    [
                        "Weather_Condition",
                        "Traffic_Level"
                    ]
                )["Delay_Hours"]
                .mean()
                .reset_index()
            )

            if chart_type == "Heatmap":

                pivot = temp.pivot(
                    index="Weather_Condition",
                    columns="Traffic_Level",
                    values="Delay_Hours"
                )

                fig = px.imshow(
                    pivot,
                    aspect="auto",
                    title="Weather vs Traffic Impact on Delay",
                    labels={
                        "x": "Traffic Level",
                        "y": "Weather Condition",
                        "color": "Average Delay"
                    }
                )

            else:

                fig = px.bar(
                    temp,
                    x="Weather_Condition",
                    y="Delay_Hours",
                    color="Traffic_Level",
                    barmode="group",
                    title="Weather vs Traffic Impact on Delay",
                    labels={
                        "Delay_Hours":
                        "Average Delay Hours"
                    }
                )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    # ============================================================
    # 6. DISRUPTION ANALYSIS
    # ============================================================

    with st.expander(
        "6. Disruption Analysis",
        expanded=False
    ):

        analysis = st.selectbox(
            "Select Analysis",
            [
                "Disruption Status Distribution",
                "Disruptions by Transport Mode",
                "Disruption Trend Over Time"
            ],
            key="disruption_analysis"
        )

        # --------------------------------------------------------
        # Disruption Status Distribution
        # --------------------------------------------------------

        if analysis == "Disruption Status Distribution":

            chart_type = st.selectbox(
                "Chart Type",
                [
                    "Donut",
                    "Bar"
                ],
                key="disruption_distribution_chart"
            )

            temp = unique_shipments(
                viz_df.dropna(
                    subset=["Disruption_Status"]
                ),
                "Disruption_Status"
            )

            if chart_type == "Donut":

                fig = px.pie(
                    temp,
                    names="Disruption_Status",
                    values="Shipment_Count",
                    hole=0.45,
                    title="Disruption Status Distribution"
                )

            else:

                fig = px.bar(
                    temp,
                    x="Disruption_Status",
                    y="Shipment_Count",
                    title="Disruption Status Distribution",
                    text_auto=True
                )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # --------------------------------------------------------
        # Disruptions by Transport Mode
        # --------------------------------------------------------

        elif analysis == "Disruptions by Transport Mode":

            chart_type = st.selectbox(
                "Chart Type",
                [
                    "Stacked Bar",
                    "Grouped Bar"
                ],
                key="disruption_transport_chart"
            )

            temp = (
                viz_df.dropna(
                    subset=[
                        "Transport_Mode",
                        "Disruption_Status"
                    ]
                )
                .groupby(
                    [
                        "Transport_Mode",
                        "Disruption_Status"
                    ]
                )["Shipment_ID"]
                .nunique()
                .reset_index(
                    name="Shipment_Count"
                )
            )

            if chart_type == "Stacked Bar":

                fig = px.bar(
                    temp,
                    x="Transport_Mode",
                    y="Shipment_Count",
                    color="Disruption_Status",
                    barmode="stack",
                    title="Disruptions by Transport Mode"
                )

            else:

                fig = px.bar(
                    temp,
                    x="Transport_Mode",
                    y="Shipment_Count",
                    color="Disruption_Status",
                    barmode="group",
                    title="Disruptions by Transport Mode"
                )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # --------------------------------------------------------
        # Disruption Trend Over Time
        # --------------------------------------------------------

        else:

            chart_type = st.selectbox(
                "Chart Type",
                [
                    "Line",
                    "Area"
                ],
                key="disruption_trend_chart"
            )

            temp = (
                viz_df.dropna(
                    subset=[
                        "Shipment_Date",
                        "Disruption_Status"
                    ]
                )
                .groupby(
                    [
                        "Shipment_Date",
                        "Disruption_Status"
                    ]
                )["Shipment_ID"]
                .nunique()
                .reset_index(
                    name="Shipment_Count"
                )
            )

            if chart_type == "Line":

                fig = px.line(
                    temp,
                    x="Shipment_Date",
                    y="Shipment_Count",
                    color="Disruption_Status",
                    title="Disruption Trend Over Time"
                )

            else:

                fig = px.area(
                    temp,
                    x="Shipment_Date",
                    y="Shipment_Count",
                    color="Disruption_Status",
                    title="Disruption Trend Over Time"
                )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


    # ============================================================
    # 7. TIME ANALYSIS
    # ============================================================

    with st.expander(
        "7. Time Analysis",
        expanded=False
    ):

        analysis = st.selectbox(
            "Select Analysis",
            [
                "Shipment Volume Over Time",
                "Monthly Shipment Volume",
                "Monthly Cost Trend"
            ],
            key="time_analysis"
        )

        # --------------------------------------------------------
        # Shipment Volume Over Time
        # --------------------------------------------------------

        if analysis == "Shipment Volume Over Time":

            chart_type = st.selectbox(
                "Chart Type",
                [
                    "Line",
                    "Area"
                ],
                key="shipment_volume_time_chart"
            )

            temp = (
                viz_df.dropna(
                    subset=["Shipment_Date"]
                )
                .groupby("Shipment_Date")[
                    "Shipment_ID"
                ]
                .nunique()
                .reset_index(
                    name="Shipment_Count"
                )
            )

            if chart_type == "Line":

                fig = px.line(
                    temp,
                    x="Shipment_Date",
                    y="Shipment_Count",
                    title="Shipment Volume Over Time",
                    labels={
                        "Shipment_Count":
                        "Shipment Count",
                        "Shipment_Date":
                        "Shipment Date"
                    }
                )

            else:

                fig = px.area(
                    temp,
                    x="Shipment_Date",
                    y="Shipment_Count",
                    title="Shipment Volume Over Time",
                    labels={
                        "Shipment_Count":
                        "Shipment Count",
                        "Shipment_Date":
                        "Shipment Date"
                    }
                )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # --------------------------------------------------------
        # Monthly Shipment Volume
        # --------------------------------------------------------

        elif analysis == "Monthly Shipment Volume":

            chart_type = st.selectbox(
                "Chart Type",
                [
                    "Column",
                    "Bar"
                ],
                key="monthly_shipment_chart"
            )

            temp = viz_df.dropna(
                subset=["Shipment_Date"]
            ).copy()

            temp["Year_Month"] = (
                temp["Shipment_Date"]
                .dt.to_period("M")
                .astype(str)
            )

            temp = (
                temp.groupby("Year_Month")[
                    "Shipment_ID"
                ]
                .nunique()
                .reset_index(
                    name="Shipment_Count"
                )
            )

            if chart_type == "Column":

                fig = px.bar(
                    temp,
                    x="Year_Month",
                    y="Shipment_Count",
                    title="Monthly Shipment Volume",
                    text_auto=True
                )

            else:

                fig = px.bar(
                    temp.sort_values("Shipment_Count"),
                    y="Year_Month",
                    x="Shipment_Count",
                    orientation="h",
                    title="Monthly Shipment Volume",
                    text_auto=True
                )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # --------------------------------------------------------
        # Monthly Cost Trend
        # --------------------------------------------------------

        else:

            chart_type = st.selectbox(
                "Chart Type",
                [
                    "Line",
                    "Area"
                ],
                key="monthly_cost_trend_chart"
            )

            temp = viz_df.dropna(
                subset=["Shipment_Date"]
            ).copy()

            temp["Year_Month"] = (
                temp["Shipment_Date"]
                .dt.to_period("M")
                .astype(str)
            )

            temp = (
                temp.groupby("Year_Month")[
                    [
                        "Delivery_Cost",
                        "Fuel_Cost"
                    ]
                ]
                .mean()
                .reset_index()
            )

            temp_long = temp.melt(
                id_vars="Year_Month",
                value_vars=[
                    "Delivery_Cost",
                    "Fuel_Cost"
                ],
                var_name="Cost_Type",
                value_name="Average_Cost"
            )

            if chart_type == "Line":

                fig = px.line(
                    temp_long,
                    x="Year_Month",
                    y="Average_Cost",
                    color="Cost_Type",
                    markers=True,
                    title="Monthly Cost Trend",
                    labels={
                        "Average_Cost":
                        "Average Cost",
                        "Year_Month":
                        "Month"
                    }
                )

            else:

                fig = px.area(
                    temp_long,
                    x="Year_Month",
                    y="Average_Cost",
                    color="Cost_Type",
                    title="Monthly Cost Trend",
                    labels={
                        "Average_Cost":
                        "Average Cost",
                        "Year_Month":
                        "Month"
                    }
                )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


# =====================================================
# FILTER DATA
# =====================================================

elif menu == "Filter Data":

    st.subheader("Filter Dataset")

    # ---------------- SELECT COLUMNS ----------------

    st.markdown("### Select Columns")

    selected_columns = st.multiselect(
        "Choose columns to display",
        df.columns.tolist(),
        default=df.columns.tolist()
    )

    # ---------------- SELECT NUMBER OF ROWS ----------------

    st.markdown("### Select Number of Rows")

    total_rows = len(df)

    number_of_rows = st.number_input(
        "How many rows do you want to download?",
        min_value=1,
        max_value=total_rows,
        value=min(100, total_rows),
        step=1
    )

    # ---------------- SELECT ROWS ----------------

    filtered_df = df.head(number_of_rows)

    # ---------------- FILTERED DATASET ----------------

    st.markdown("### Filtered Dataset")

    if len(selected_columns) > 0:

        filtered_display = filtered_df[selected_columns]

        st.dataframe(
            filtered_display,
            use_container_width=True
        )

        # ---------------- DATASET SHAPE ----------------

        st.write(
            "Filtered Data Shape:",
            filtered_display.shape
        )

        # ---------------- DOWNLOAD ----------------

        csv = filtered_display.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            "⬇ Download Filtered Data",
            csv,
            "filtered_dataset.csv",
            "text/csv"
        )

    else:
        st.warning(
            "Please select at least one column."
        )
