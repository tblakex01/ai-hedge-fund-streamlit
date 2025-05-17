import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
from src.main import run_hedge_fund
from src.utils.analysts import ANALYST_ORDER
from src.llm.models import LLM_ORDER, get_model_info, ModelProvider

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(page_title="AI Hedge Fund", page_icon="📈", layout="wide", initial_sidebar_state="expanded")

# Apply custom CSS for a modern look
st.markdown(
    """
<style>
    .stButton button {
        background-color: #FF5252;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton button:hover {
        background-color: #FF7272;
    }
    div.stMultiSelect > div[data-baseweb="select"] > div {
        background-color: #2C3E50;
    }
    div.stSelectbox > div[data-baseweb="select"] > div {
        background-color: #2C3E50;
    }
    .agent-tag {
        display: inline-block;
        background-color: #FF5252;
        color: white;
        padding: 0.3rem 0.6rem;
        border-radius: 5px;
        margin-right: 5px;
        margin-bottom: 5px;
    }
    .sidebar .sidebar-content {
        background-color: #1E293B;
    }
    h1, h2, h3 {
        color: #4DA8DA;
    }
    .info-box {
        background-color: #2C3E50;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    .small-input {
        max-width: 200px;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Sidebar for configuration
with st.sidebar:
    st.title("Configuration")

    # Stock Tickers input
    ticker_help = "Enter comma-separated stock ticker symbols (e.g., AAPL,MSFT,NVDA)"
    tickers = st.text_input("Stock Tickers (comma-separated)", value="AAPL,MSFT", help=ticker_help)

    # Date range
    col1, col2 = st.columns(2)
    with col1:
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        start_date = st.date_input("Start Date", value=yesterday - timedelta(days=1))
    with col2:
        end_date = st.date_input("End Date", value=yesterday)

    # Initial capital
    initial_capital = st.number_input("Initial Capital ($)", min_value=1000.0, max_value=10000000.0, value=100000.0, step=1000.0, help="Initial investment amount")

    # Margin requirement
    margin_requirement = st.slider("Margin Requirement (%)", min_value=0.0, max_value=100.0, value=0.0, step=5.0, help="Percentage of margin required for short positions")

    # LLM Model selection
    model_options = [display for display, _, _ in LLM_ORDER]
    model_values = {display: value for display, value, _ in LLM_ORDER}
    model_providers = {display: provider for display, _, provider in LLM_ORDER}

    selected_model_display = st.selectbox("LLM Model", options=model_options, index=model_options.index("[deepseek] deepseek-v3") if "[deepseek] deepseek-v3" in model_options else 0)

    selected_model = model_values[selected_model_display]
    selected_model_provider = model_providers[selected_model_display]

    # Analyst selection
    analyst_options = [display for display, _ in ANALYST_ORDER]
    analyst_values = {display: value for display, value in ANALYST_ORDER}

    selected_analysts_display = st.multiselect("Select Analysts", options=analyst_options, default=["Ben Graham", "Bill Ackman", "Cathie Wood"])

    selected_analysts = [analyst_values[display] for display in selected_analysts_display]

    # Run button
    run_button = st.button("Run Analysis", type="primary")

# Main content area
st.title("AI Hedge Fund Analysis")

# Display sample portfolio structure
if "portfolio" not in st.session_state:
    st.session_state.portfolio = {"cash": float(initial_capital), "margin_requirement": float(margin_requirement) / 100, "positions": {}, "realized_gains": {}}  # Convert percentage to decimal

# Initialize portfolio positions for selected tickers
ticker_list = [t.strip() for t in tickers.split(",")]
for ticker in ticker_list:
    if ticker not in st.session_state.portfolio["positions"]:
        st.session_state.portfolio["positions"][ticker] = {
            "long": 0,
            "short": 0,
            "long_cost_basis": 0.0,
            "short_cost_basis": 0.0,
        }
    if ticker not in st.session_state.portfolio["realized_gains"]:
        st.session_state.portfolio["realized_gains"][ticker] = {
            "long": 0.0,
            "short": 0.0,
        }

# Update portfolio when configurations change
if initial_capital != st.session_state.portfolio["cash"]:
    st.session_state.portfolio["cash"] = float(initial_capital)

if margin_requirement / 100 != st.session_state.portfolio["margin_requirement"]:
    st.session_state.portfolio["margin_requirement"] = float(margin_requirement) / 100

# Run the analysis when button is clicked
if run_button:
    with st.spinner("Running analysis..."):
        try:
            # Convert dates to string format
            start_date_str = start_date.strftime("%Y-%m-%d")
            end_date_str = end_date.strftime("%Y-%m-%d")

            result = run_hedge_fund(tickers=ticker_list, start_date=start_date_str, end_date=end_date_str, portfolio=st.session_state.portfolio, selected_analysts=selected_analysts, model_name=selected_model, model_provider=selected_model_provider, show_reasoning=True)

            # Store the result in session state
            st.session_state.result = result
            st.session_state.run_complete = True

        except Exception as e:
            st.error(f"Error running analysis: {e}")
            st.session_state.run_complete = False

# Display results if available
if st.session_state.get("run_complete", False):
    try:
        result = st.session_state.result
        decisions = result.get("decisions", {})
        analyst_signals = result.get("analyst_signals", {})

        # Display decisions for each ticker
        st.subheader("Trading Decisions")

        for ticker in ticker_list:
            if ticker in decisions:
                decision = decisions[ticker]
                action = decision.get("action", "").upper()
                quantity = decision.get("quantity", 0)
                confidence = decision.get("confidence", 0)
                reasoning = decision.get("reasoning", "No reasoning provided")

                # Create expandable section for each ticker
                with st.expander(f"{ticker} - {action} {quantity} shares ({confidence:.1f}% confidence)", expanded=True):
                    cols = st.columns(3)
                    cols[0].metric("Action", action)
                    cols[1].metric("Quantity", quantity)
                    cols[2].metric("Confidence", f"{confidence:.1f}%")

                    st.markdown("#### Reasoning")
                    st.info(reasoning)

                    # Analyst signals for this ticker
                    st.markdown("#### Analyst Signals")

                    # Create a table of signals
                    signal_data = []
                    for agent_name, signals in analyst_signals.items():
                        if ticker in signals:
                            signal = signals[ticker]
                            agent_display = agent_name.replace("_agent", "").replace("_", " ").title()
                            signal_type = signal.get("signal", "").upper()
                            confidence = signal.get("confidence", 0)

                            signal_data.append({"Analyst": agent_display, "Signal": signal_type, "Confidence": f"{confidence:.1f}%"})

                    if signal_data:
                        st.table(pd.DataFrame(signal_data))
                    else:
                        st.warning("No analyst signals available for this ticker")

        # Portfolio summary
        st.subheader("Portfolio Summary")

        portfolio = st.session_state.portfolio

        # Calculate total position value
        total_position_value = 0
        for ticker in ticker_list:
            position = portfolio["positions"].get(ticker, {})
            # This is just a placeholder, we'd need current prices to calculate real position values
            # For now, display the position details
            if position:
                st.markdown(f"**{ticker}**: {position.get('long', 0)} shares long, {position.get('short', 0)} shares short")

        col1, col2, col3 = st.columns(3)
        col1.metric("Cash Balance", f"${portfolio['cash']:,.2f}")
        col2.metric("Margin Requirement", f"{portfolio['margin_requirement']*100:.1f}%")
        # We would need to calculate these values
        col3.metric("Realized Gains", "$0.00")  # Placeholder

    except Exception as e:
        st.error(f"Error displaying results: {e}")
        st.code(str(st.session_state.result))  # Display raw result for debugging

# Display instructions if no analysis has been run
if not st.session_state.get("run_complete", False):
    st.info(
        """
    Configure your analysis parameters in the sidebar and click "Run Analysis" to start.
    
    The AI Hedge Fund will:
    1. Analyze selected stocks using multiple AI analyst agents
    2. Generate trading signals based on fundamental, technical, and sentiment analysis
    3. Provide detailed reasoning for each recommendation
    """
    )

# Footer
st.markdown("---")
st.markdown("AI Hedge Fund - For Educational Purposes Only")
