import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Diabetes Risk Analytics Dashboard",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #f8fafc;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .main-title {
        font-size: 38px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 17px;
        color: #64748b;
        margin-bottom: 30px;
    }

    div[data-testid="stMetric"] {
        background-color: white;
        border-radius: 12px;
        padding: 15px;
        border: 1px solid #e2e8f0;
        box-shadow: 0px 3px 10px rgba(0,0,0,0.05);
    }

    .insight-box {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #2563eb;
        margin-bottom: 15px;
        box-shadow: 0px 3px 10px rgba(0,0,0,0.05);
    }

    .section-title {
        font-size: 26px;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    file_name = "diabetes_risk_prediction_dataset.csv"

    df = pd.read_csv(file_name)

    return df


try:
    df = load_data()

except FileNotFoundError:

    st.error(
        """
        ❌ Dataset file not found.

        Please make sure this file is inside your GitHub repository:

        diabetes_risk_prediction_dataset.csv

        Your repository should look like:

        diabetes-risk-dashboard/
        ├── app.py
        ├── requirements.txt
        └── diabetes_risk_prediction_dataset.csv
        """
    )

    st.stop()


# =========================================================
# DATA PREPROCESSING
# =========================================================

data = df.copy()

data.columns = data.columns.str.strip()

# Convert common numeric columns safely
numeric_columns = data.select_dtypes(
    include=np.number
).columns.tolist()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🩺 Diabetes Analytics")

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard Overview",
        "📊 Risk Analysis",
        "🧬 Health Factors",
        "📈 Lifestyle Analysis",
        "👤 Patient Explorer",
        "🔍 Data Explorer"
    ]
)

st.sidebar.markdown("---")

st.sidebar.subheader("🎛 Dataset Filters")


# Gender Filter
if "Gender" in data.columns:

    gender_options = data["Gender"].dropna().unique().tolist()

    selected_gender = st.sidebar.multiselect(
        "Select Gender",
        gender_options,
        default=gender_options
    )

else:
    selected_gender = []


# Diabetes Risk Filter
if "Diabetes_Risk" in data.columns:

    risk_options = data["Diabetes_Risk"].dropna().unique().tolist()

    selected_risk = st.sidebar.multiselect(
        "Select Diabetes Risk",
        risk_options,
        default=risk_options
    )

else:
    selected_risk = []


# Age Filter
if "Age" in data.columns:

    min_age = int(data["Age"].min())
    max_age = int(data["Age"].max())

    age_range = st.sidebar.slider(
        "Age Range",
        min_age,
        max_age,
        (min_age, max_age)
    )

else:
    age_range = (0, 100)


# Apply Filters
filtered_df = data.copy()

if "Gender" in filtered_df.columns and selected_gender:
    filtered_df = filtered_df[
        filtered_df["Gender"].isin(selected_gender)
    ]

if "Diabetes_Risk" in filtered_df.columns and selected_risk:
    filtered_df = filtered_df[
        filtered_df["Diabetes_Risk"].isin(selected_risk)
    ]

if "Age" in filtered_df.columns:
    filtered_df = filtered_df[
        filtered_df["Age"].between(
            age_range[0],
            age_range[1]
        )
    ]


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="main-title">
        🩺 Diabetes Risk Prediction Analytics Dashboard
    </div>

    <div class="subtitle">
        Interactive analysis of patient health, lifestyle and diabetes risk factors
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# PAGE 1 - DASHBOARD OVERVIEW
# =========================================================

if page == "🏠 Dashboard Overview":

    st.markdown(
        '<div class="section-title">📌 Dataset Overview</div>',
        unsafe_allow_html=True
    )

    total_patients = len(filtered_df)

    avg_age = (
        filtered_df["Age"].mean()
        if "Age" in filtered_df.columns
        else 0
    )

    avg_bmi = (
        filtered_df["BMI"].mean()
        if "BMI" in filtered_df.columns
        else 0
    )

    avg_risk_score = (
        filtered_df["Diabetes_Risk_Score"].mean()
        if "Diabetes_Risk_Score" in filtered_df.columns
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "👥 Total Patients",
        f"{total_patients:,}"
    )

    col2.metric(
        "🎂 Average Age",
        f"{avg_age:.1f}"
    )

    col3.metric(
        "⚖️ Average BMI",
        f"{avg_bmi:.2f}"
    )

    col4.metric(
        "🩸 Average Risk Score",
        f"{avg_risk_score:.1f}"
    )


    st.markdown("<br>", unsafe_allow_html=True)

    chart_col1, chart_col2 = st.columns(2)


    # Diabetes Risk Distribution
    if "Diabetes_Risk" in filtered_df.columns:

        risk_counts = (
            filtered_df["Diabetes_Risk"]
            .value_counts()
            .reset_index()
        )

        risk_counts.columns = [
            "Diabetes Risk",
            "Patients"
        ]

        fig = px.pie(
            risk_counts,
            names="Diabetes Risk",
            values="Patients",
            hole=0.5,
            title="Diabetes Risk Distribution"
        )

        chart_col1.plotly_chart(
            fig,
            use_container_width=True
        )


    # BMI Distribution
    if "BMI_CATEGORY" in filtered_df.columns:

        bmi_counts = (
            filtered_df["BMI_CATEGORY"]
            .value_counts()
            .reset_index()
        )

        bmi_counts.columns = [
            "BMI Category",
            "Patients"
        ]

        fig = px.bar(
            bmi_counts,
            x="BMI Category",
            y="Patients",
            title="BMI Category Distribution",
            text_auto=True
        )

        chart_col2.plotly_chart(
            fig,
            use_container_width=True
        )


    st.markdown(
        '<div class="section-title">📊 Key Health Indicators</div>',
        unsafe_allow_html=True
    )

    indicators = [
        "Blood_Glucose",
        "HbA1c",
        "Fasting_Blood_Sugar",
        "BMI",
        "Blood_Pressure_Systolic",
        "Total_Cholesterol"
    ]

    available_indicators = [
        col for col in indicators
        if col in filtered_df.columns
    ]

    if available_indicators:

        health_means = (
            filtered_df[available_indicators]
            .mean()
            .reset_index()
        )

        health_means.columns = [
            "Health Indicator",
            "Average Value"
        ]

        fig = px.bar(
            health_means,
            x="Health Indicator",
            y="Average Value",
            title="Average Health Measurements"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    st.markdown(
        '<div class="section-title">💡 Automated Insights</div>',
        unsafe_allow_html=True
    )

    if len(filtered_df) > 0:

        high_risk_percent = 0

        if "Diabetes_Risk" in filtered_df.columns:

            high_risk_percent = (
                filtered_df["Diabetes_Risk"]
                .astype(str)
                .str.lower()
                .eq("high")
                .mean()
                * 100
            )

        st.markdown(
            f"""
            <div class="insight-box">
            🔴 <b>High Risk Population:</b>
            {high_risk_percent:.2f}% of the filtered patients are classified
            as high diabetes risk.
            </div>
            """,
            unsafe_allow_html=True
        )

        if "BMI" in filtered_df.columns:

            overweight_percent = (
                (filtered_df["BMI"] >= 25)
                .mean()
                * 100
            )

            st.markdown(
                f"""
                <div class="insight-box">
                ⚖️ <b>BMI Insight:</b>
                {overweight_percent:.2f}% of patients have BMI greater than
                or equal to 25, indicating overweight or obesity risk.
                </div>
                """,
                unsafe_allow_html=True
            )

        if "Blood_Glucose" in filtered_df.columns:

            avg_glucose = filtered_df[
                "Blood_Glucose"
            ].mean()

            st.markdown(
                f"""
                <div class="insight-box">
                🩸 <b>Blood Glucose Insight:</b>
                The average blood glucose level in the selected population is
                <b>{avg_glucose:.2f}</b>.
                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# PAGE 2 - RISK ANALYSIS
# =========================================================

elif page == "📊 Risk Analysis":

    st.markdown(
        '<div class="section-title">📊 Diabetes Risk Analysis</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)


    # Age vs Diabetes Risk
    if (
        "Age" in filtered_df.columns
        and "Diabetes_Risk" in filtered_df.columns
    ):

        fig = px.box(
            filtered_df,
            x="Diabetes_Risk",
            y="Age",
            color="Diabetes_Risk",
            title="Age Distribution by Diabetes Risk"
        )

        col1.plotly_chart(
            fig,
            use_container_width=True
        )


    # BMI vs Risk
    if (
        "BMI" in filtered_df.columns
        and "Diabetes_Risk" in filtered_df.columns
    ):

        fig = px.box(
            filtered_df,
            x="Diabetes_Risk",
            y="BMI",
            color="Diabetes_Risk",
            title="BMI Distribution by Diabetes Risk"
        )

        col2.plotly_chart(
            fig,
            use_container_width=True
        )


    st.markdown(
        '<div class="section-title">🩸 Risk Score Relationships</div>',
        unsafe_allow_html=True
    )

    if (
        "Blood_Glucose" in filtered_df.columns
        and "Diabetes_Risk_Score" in filtered_df.columns
        and "Diabetes_Risk" in filtered_df.columns
    ):

        fig = px.scatter(
            filtered_df.sample(
                min(5000, len(filtered_df)),
                random_state=42
            ),
            x="Blood_Glucose",
            y="Diabetes_Risk_Score",
            color="Diabetes_Risk",
            hover_data=[
                "Age",
                "BMI",
                "HbA1c"
            ] if "HbA1c" in filtered_df.columns else None,
            title="Blood Glucose vs Diabetes Risk Score"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # Risk Score Histogram
    if "Diabetes_Risk_Score" in filtered_df.columns:

        fig = px.histogram(
            filtered_df,
            x="Diabetes_Risk_Score",
            nbins=30,
            title="Distribution of Diabetes Risk Score"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# PAGE 3 - HEALTH FACTORS
# =========================================================

elif page == "🧬 Health Factors":

    st.markdown(
        '<div class="section-title">🧬 Health Factor Analysis</div>',
        unsafe_allow_html=True
    )


    health_features = [
        "Blood_Glucose",
        "HbA1c",
        "Fasting_Blood_Sugar",
        "Insulin_Level",
        "BMI",
        "Waist_Circumference_cm",
        "Total_Cholesterol",
        "HDL",
        "LDL",
        "Triglycerides"
    ]

    available_features = [
        col for col in health_features
        if col in filtered_df.columns
    ]


    if len(available_features) > 1:

        correlation = filtered_df[
            available_features
        ].corr()

        fig = px.imshow(
            correlation,
            text_auto=".2f",
            title="Health Feature Correlation Matrix"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    col1, col2 = st.columns(2)


    if (
        "Blood_Glucose" in filtered_df.columns
        and "Diabetes_Risk" in filtered_df.columns
    ):

        fig = px.violin(
            filtered_df,
            x="Diabetes_Risk",
            y="Blood_Glucose",
            color="Diabetes_Risk",
            box=True,
            title="Blood Glucose by Diabetes Risk"
        )

        col1.plotly_chart(
            fig,
            use_container_width=True
        )


    if (
        "HbA1c" in filtered_df.columns
        and "Diabetes_Risk" in filtered_df.columns
    ):

        fig = px.violin(
            filtered_df,
            x="Diabetes_Risk",
            y="HbA1c",
            color="Diabetes_Risk",
            box=True,
            title="HbA1c by Diabetes Risk"
        )

        col2.plotly_chart(
            fig,
            use_container_width=True
        )


    if (
        "Blood_Pressure_Systolic" in filtered_df.columns
        and "Blood_Pressure_Diastolic" in filtered_df.columns
    ):

        fig = px.scatter(
            filtered_df.sample(
                min(5000, len(filtered_df)),
                random_state=42
            ),
            x="Blood_Pressure_Systolic",
            y="Blood_Pressure_Diastolic",
            color="Diabetes_Risk"
            if "Diabetes_Risk" in filtered_df.columns
            else None,
            title="Systolic vs Diastolic Blood Pressure"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# PAGE 4 - LIFESTYLE ANALYSIS
# =========================================================

elif page == "📈 Lifestyle Analysis":

    st.markdown(
        '<div class="section-title">📈 Lifestyle & Diabetes Risk Analysis</div>',
        unsafe_allow_html=True
    )


    col1, col2 = st.columns(2)


    if (
        "Physical_Activity_Level" in filtered_df.columns
        and "Diabetes_Risk" in filtered_df.columns
    ):

        activity_risk = pd.crosstab(
            filtered_df["Physical_Activity_Level"],
            filtered_df["Diabetes_Risk"]
        ).reset_index()

        fig = px.bar(
            activity_risk,
            x="Physical_Activity_Level",
            y=[
                col for col in activity_risk.columns
                if col != "Physical_Activity_Level"
            ],
            barmode="group",
            title="Physical Activity vs Diabetes Risk"
        )

        col1.plotly_chart(
            fig,
            use_container_width=True
        )


    if (
        "Diet_Quality" in filtered_df.columns
        and "Diabetes_Risk" in filtered_df.columns
    ):

        diet_risk = pd.crosstab(
            filtered_df["Diet_Quality"],
            filtered_df["Diabetes_Risk"]
        ).reset_index()

        fig = px.bar(
            diet_risk,
            x="Diet_Quality",
            y=[
                col for col in diet_risk.columns
                if col != "Diet_Quality"
            ],
            barmode="group",
            title="Diet Quality vs Diabetes Risk"
        )

        col2.plotly_chart(
            fig,
            use_container_width=True
        )


    col1, col2 = st.columns(2)


    if (
        "Exercise_Hours_Per_Week" in filtered_df.columns
        and "Diabetes_Risk" in filtered_df.columns
    ):

        fig = px.box(
            filtered_df,
            x="Diabetes_Risk",
            y="Exercise_Hours_Per_Week",
            color="Diabetes_Risk",
            title="Exercise Hours by Diabetes Risk"
        )

        col1.plotly_chart(
            fig,
            use_container_width=True
        )


    if (
        "Sleep_Hours" in filtered_df.columns
        and "Diabetes_Risk" in filtered_df.columns
    ):

        fig = px.box(
            filtered_df,
            x="Diabetes_Risk",
            y="Sleep_Hours",
            color="Diabetes_Risk",
            title="Sleep Hours by Diabetes Risk"
        )

        col2.plotly_chart(
            fig,
            use_container_width=True
        )


    if (
        "Stress_Level" in filtered_df.columns
        and "Diabetes_Risk" in filtered_df.columns
    ):

        stress_data = pd.crosstab(
            filtered_df["Stress_Level"],
            filtered_df["Diabetes_Risk"]
        ).reset_index()

        fig = px.bar(
            stress_data,
            x="Stress_Level",
            y=[
                col for col in stress_data.columns
                if col != "Stress_Level"
            ],
            barmode="stack",
            title="Stress Level and Diabetes Risk"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# =========================================================
# PAGE 5 - PATIENT EXPLORER
# =========================================================

elif page == "👤 Patient Explorer":

    st.markdown(
        '<div class="section-title">👤 Individual Patient Explorer</div>',
        unsafe_allow_html=True
    )


    if "Patient_ID" in filtered_df.columns:

        patient_ids = filtered_df[
            "Patient_ID"
        ].unique()

        selected_patient = st.selectbox(
            "Select Patient ID",
            patient_ids
        )

        patient = filtered_df[
            filtered_df["Patient_ID"]
            == selected_patient
        ]


        if not patient.empty:

            st.subheader(
                f"Patient ID: {selected_patient}"
            )


            metric_columns = [
                "Age",
                "BMI",
                "Blood_Glucose",
                "HbA1c",
                "Diabetes_Risk_Score"
            ]

            available_metrics = [
                col for col in metric_columns
                if col in patient.columns
            ]


            cols = st.columns(
                len(available_metrics)
            )


            for index, column in enumerate(
                available_metrics
            ):

                value = patient.iloc[0][column]

                if pd.notna(value):

                    cols[index].metric(
                        column.replace("_", " "),
                        f"{value:.2f}"
                        if isinstance(
                            value,
                            (float, np.floating)
                        )
                        else value
                    )


            st.markdown("### 🩺 Patient Information")

            display_columns = [
                "Age",
                "Gender",
                "BMI",
                "BMI_CATEGORY",
                "Blood_Glucose",
                "HbA1c",
                "Fasting_Blood_Sugar",
                "Insulin_Level",
                "Blood_Pressure_Systolic",
                "Blood_Pressure_Diastolic",
                "Physical_Activity_Level",
                "Diet_Quality",
                "Exercise_Hours_Per_Week",
                "Sleep_Hours",
                "Stress_Level",
                "Family_History_Diabetes",
                "Hypertension",
                "Diabetes_Risk",
                "AI_Health_Recommendation",
                "Doctor_Consultation_Needed"
            ]

            display_columns = [
                col for col in display_columns
                if col in patient.columns
            ]

            patient_display = patient[
                display_columns
            ].T.reset_index()

            patient_display.columns = [
                "Health Feature",
                "Value"
            ]

            st.dataframe(
                patient_display,
                use_container_width=True
            )


# =========================================================
# PAGE 6 - DATA EXPLORER
# =========================================================

elif page == "🔍 Data Explorer":

    st.markdown(
        '<div class="section-title">🔍 Dataset Explorer</div>',
        unsafe_allow_html=True
    )


    tab1, tab2, tab3 = st.tabs(
        [
            "📄 Data Preview",
            "🧹 Data Quality",
            "📊 Statistical Summary"
        ]
    )


    # DATA PREVIEW
    with tab1:

        st.subheader("Filtered Dataset")

        st.dataframe(
            filtered_df,
            use_container_width=True,
            height=500
        )


        csv = filtered_df.to_csv(
            index=False
        ).encode("utf-8")


        st.download_button(
            label="📥 Download Filtered Dataset",
            data=csv,
            file_name="filtered_diabetes_data.csv",
            mime="text/csv"
        )


    # DATA QUALITY
    with tab2:

        st.subheader("Missing Value Analysis")

        missing_data = (
            filtered_df.isnull()
            .sum()
            .reset_index()
        )

        missing_data.columns = [
            "Column",
            "Missing Values"
        ]

        fig = px.bar(
            missing_data,
            x="Column",
            y="Missing Values",
            title="Missing Values by Column"
        )

        fig.update_layout(
            xaxis_tickangle=-45
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


        st.subheader("Duplicate Records")

        duplicates = filtered_df.duplicated().sum()

        st.metric(
            "Duplicate Rows",
            duplicates
        )


    # STATISTICAL SUMMARY
    with tab3:

        st.subheader(
            "Numerical Features Summary"
        )

        st.dataframe(
            filtered_df.describe().T,
            use_container_width=True
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:#64748b;">
        🩺 Diabetes Risk Prediction Analytics Dashboard |
        Built with Python, Pandas, Plotly and Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
