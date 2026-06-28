import streamlit as st
import pandas as pd

from agents.report_agent import ReportAgent
from agents.visualization_agent import VisualizationAgent

st.set_page_config(
    page_title="AI EDA Copilot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

with st.sidebar:
    st.title("🤖 AI EDA Copilot")
    st.markdown(
        """
        Upload any CSV dataset and let the AI automatically:

        - Profile your dataset
        - Detect data quality issues
        - Perform statistical analysis
        - Generate visualizations
        - Suggest business insights
        """
    )

    uploaded_file = st.file_uploader(
        "Upload CSV",
        type=["csv"]
    )

st.title("🤖 AI EDA Copilot")
st.caption(
    "An AI-powered exploratory data analysis assistant."
)

if uploaded_file:
    with st.spinner("Analyzing dataset..."):
        df = pd.read_csv(uploaded_file)
        report = ReportAgent().generate_report(df)
        figures = VisualizationAgent().render(report)

    st.success("Analysis Completed Successfully!")
    profile = report["dataset_profile"]
    planner = report["planner"]
    st.header("📊 Dataset Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Rows",
            profile.rows
        )

    with col2:
        st.metric(
            "Columns",
            profile.columns
        )

    with col3:
        st.metric(
            "Memory (MB)",
            round(profile.memory_usage_mb, 2)
        )

    st.divider()

    st.header("🧠 Data Understanding")
    c1, c2 = st.columns(2)
    with c1:
        st.metric(
            "Dataset Type",
            planner.get("dataset_type", "Unknown")
        )

        st.metric(
            "Business Domain",
            planner.get("business_domain", "Unknown")
        )

    with c2:
        st.metric(
            "Possible Target",
            planner.get("possible_target", "Unknown")
        )

        identifiers = planner.get("identifiers", [])
        st.metric(
            "Identifiers",
            str(len(identifiers))
        )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Business Metrics")
        metrics = planner.get("metrics", [])
        if metrics:
            for metric in metrics:
                st.success(metric)

        else:
            st.info("No metrics detected.")

    with col2:
        st.subheader("📂 Dimensions")
        dimensions = planner.get("dimensions", [])

        if dimensions:
            for dim in dimensions:
                st.success(dim)

        else:
            st.info("No dimensions detected.")

    st.divider()

    tabs = st.tabs([
        "📊 Overview",
        "🧹 Data Quality",
        "📈 Numerical",
        "🧩 Categorical",
        "🔗 Correlation",
        "📉 Relationships",
        "🤖 AI Insights"
    ])

    analysis_mapping = {
        0: "overview",
        1: "data_quality",
        2: "numerical",
        3: "categorical",
        4: "correlation",
        5: "relationships"
    }

    for index in range(6):

        with tabs[index]:

            section = analysis_mapping[index]

            result = report[section]

            st.subheader(result.title)

            st.write(result.summary)

            if result.findings:

                st.markdown("### 🔍 Findings")

                for finding in result.findings:

                    st.markdown(f"- {finding}")

            if result.recommendations:

                st.markdown("### 💡 Recommendations")

                for rec in result.recommendations:

                    st.markdown(f"- {rec}")

            if section in figures:

                for fig in figures[section]:

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

    st.header("🧠 AI Executive Summary")
    ai = report['ai_insights']
    st.write(ai['executive_summary'])
    st.subheader("Key Findings")

    for item in ai["key_findings"]:
        st.markdown(f" - {item}")

    st.subheader("Business Recommendations")
    for item in ai['business_recommendations']:
        st.markdown(f" - {item}")
    
    st.subheader("ML Readiness")
    st.info(ai['ml_readiness'])

    st.subheader("Feature Engineering")
    for item in ai['feature_engineering']:
        st.markdown(f" - {item}")

    st.subheader("Next Steps")
    for item in ai['next_steps']:
        st.markdown(f" - {item}")


    with tabs[6]:

        st.info(
            "🚀 AI Insights will be available in the next version."
        )

    st.divider()

    with st.expander("📄 View Raw Dataset"):
        st.dataframe(
            df,
            use_container_width=True
        )