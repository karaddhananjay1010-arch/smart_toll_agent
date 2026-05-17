# frontend/dashboard.py

import streamlit as st
import requests
import pandas as pd



st.set_page_config(
    page_title="Smart City Toll Dashboard",
    page_icon="🚦",
    layout="wide"
)

st.title("Smart City Automated Toll Enforcement Portal")
st.subheader("Connected Vehicle Telemetry Core Scanner & Billing Interface")
st.markdown("---")


st.sidebar.header("Toll Station Controls")

vehicle_id = st.sidebar.text_input(
    "Scan Vehicle License Plate ID:",
    value="MH-12-NX-4567"
)

st.sidebar.markdown("""
### Operator Guidance:
1. Input the vehicle registration ID scanned at the gate.
2. Upload the extracted internal telemetry log file.
3. Click **Process Invoice** to initiate the AI reasoning loop.
""")


col1, col2 = st.columns(2)



with col1:

    st.header("Step 1: Extract Telemetry Data")

    uploaded_file = st.file_uploader(
        "Upload Onboard Recorder Log (.csv)",
        type=["csv"]
    )

    if uploaded_file is not None:

        st.success("File uploaded successfully into scanner memory buffers.")

        # Preview CSV data
        df_preview = pd.read_csv(uploaded_file)

        st.dataframe(
            df_preview,
            use_container_width=True
        )

        # Reset file pointer
        uploaded_file.seek(0)


with col2:

    st.header("Step 2: AI Toll Inspector")

    st.markdown("""
    AI Deduction Engine will inspect:

    - Vehicle speed
    - Toll crossing duration
    - Distance metrics
    - Rule violations
    - Tax calculations
    - Fine deductions
    """)

    if uploaded_file is not None:

        if st.button(
            "Process Toll & Run Deductions",
            type="primary"
        ):

            with st.spinner(
                "Agent evaluating laws, processing logs, and running calculations..."
            ):

                try:



                    files = {
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            "text/csv"
                        )
                    }

                    params = {
                        "vehicle_id": vehicle_id
                    }



                    backend_api_url = "http://localhost:8000/process-toll/"

                    api_response = requests.post(
                        backend_api_url,
                        params=params,
                        files=files
                    )


                    if api_response.status_code == 200:

                        data = api_response.json()

                        if data.get("status") == "success":

                            st.success(
                                "Toll processing workflow completed successfully!"
                            )

                            # Display report
                            st.markdown("## Official Toll Audit Log Report")

                            st.info(data.get("report"))

                            # Display summary cards
                            st.markdown("### Billing Summary")

                            c1, c2, c3 = st.columns(3)

                            with c1:
                                st.metric(
                                    "Base Toll",
                                    f"₹{data.get('base_toll', 0)}"
                                )

                            with c2:
                                st.metric(
                                    "Penalty",
                                    f"₹{data.get('penalty', 0)}"
                                )

                            with c3:
                                st.metric(
                                    "Final Amount",
                                    f"₹{data.get('final_amount', 0)}"
                                )

                        else:

                            st.error(
                                f"Backend Engine Refusal: {data.get('message')}"
                            )

                    else:

                        st.error(
                            f"HTTP Connection Failure Code: {api_response.status_code}"
                        )


                except Exception as e:

                    st.error(
                        f"Could not connect to the FastAPI backend API service. "
                        f"Is it offline?\n\nDetail: {e}"
                    )

    else:

        st.info(
            "Awaiting sensor telemetry log upload data from the left input deck panel."
        )