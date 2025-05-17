import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import json
from dotenv import load_dotenv
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
    .analyst-card {
        cursor: pointer;
        transition: all 0.3s ease;
        border-radius: 5px;
    }
    .analyst-card:hover {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        transform: translateY(-2px);
    }
    .bullish {
        border-left: 4px solid #4CAF50;
    }
    .bearish {
        border-left: 4px solid #F44336;
    }
    .neutral {
        border-left: 4px solid #FFC107;
    }
    .analyst-heading {
        font-weight: bold;
        margin-bottom: 5px;
    }
    .clickable-text {
        cursor: pointer;
        text-decoration: underline;
        color: #4DA8DA;
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

    # Check if environment variables are set
    env_status = {}
    for provider, env_var in [("OpenAI", "OPENAI_API_KEY"), ("Anthropic", "ANTHROPIC_API_KEY"), ("DeepSeek", "DEEPSEEK_API_KEY"), ("Groq", "GROQ_API_KEY"), ("Google", "GOOGLE_API_KEY"), ("Financial Datasets", "FINANCIAL_DATASETS_API_KEY")]:
        env_status[provider] = os.environ.get(env_var) is not None

    # Only display models from providers with API keys set
    available_models = []
    for display, value, provider in LLM_ORDER:
        provider_name = provider.split()[0] if " " in provider else provider
        if env_status.get(provider_name, False):
            available_models.append((display, value, provider))

    if not available_models:
        st.warning("No API keys set. Please add at least one API key to your .env file.")
        available_models = [("[deepseek] deepseek-v3", "deepseek-chat", "DeepSeek")]

    # LLM Model selection
    model_options = [display for display, _, _ in available_models]
    model_values = {display: value for display, value, _ in available_models}
    model_providers = {display: provider for display, _, provider in available_models}

    # Display info about available models
    available_providers = [p.split()[0] for p in model_providers.values()]
    if len(available_providers) < len([p for p, s in env_status.items() if s]):
        missing_providers = [p for p, s in env_status.items() if s and p not in available_providers]
        if missing_providers:
            info_text = f"Only {', '.join(available_providers)} models are available for selection."
            st.info(info_text)

    selected_model_display = st.selectbox("LLM Model", options=model_options, index=0)

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

# Initialize state for selected analyst reasoning
if "selected_analyst" not in st.session_state:
    st.session_state.selected_analyst = {}

# Run the analysis when button is clicked
if run_button:
    if not selected_analysts:
        st.error("Please select at least one analyst.")
    else:
        with st.spinner("Running analysis..."):
            try:
                # Convert dates to string format
                start_date_str = start_date.strftime("%Y-%m-%d")
                end_date_str = end_date.strftime("%Y-%m-%d")

                # Reset any cached data between runs
                try:
                    from src.data.cache import reset_cache

                    reset_cache()
                except ImportError:
                    # If reset_cache doesn't exist, we'll continue without it
                    pass

                # Call the run_hedge_fund function
                result = run_hedge_fund(tickers=ticker_list, start_date=start_date_str, end_date=end_date_str, portfolio=st.session_state.portfolio, selected_analysts=selected_analysts, model_name=selected_model, model_provider=selected_model_provider, show_reasoning=True)

                # Store the result in session state
                st.session_state.result = result
                st.session_state.run_complete = True

                # Reset selected analyst state for each ticker
                st.session_state.selected_analyst = {ticker: None for ticker in ticker_list}

            except Exception as e:
                st.error(f"Error running analysis: {str(e)}")
                import traceback

                st.code(traceback.format_exc())
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

                    st.markdown("#### Final Reasoning")
                    st.info(reasoning)

                    # Analyst signals for this ticker
                    st.markdown("#### Analyst Signals")

                    # Create a list of signals with class based on signal type
                    signal_data = []
                    for agent_name, signals in analyst_signals.items():
                        if ticker in signals:
                            signal = signals[ticker]
                            agent_display = agent_name.replace("_agent", "").replace("_", " ").title()
                            signal_type = signal.get("signal", "").upper()
                            confidence = signal.get("confidence", 0)
                            signal_class = signal.get("signal", "neutral").lower()

                            signal_data.append({"agent_name": agent_name, "agent_display": agent_display, "signal_type": signal_type, "confidence": confidence, "signal_class": signal_class, "reasoning": signal.get("reasoning", "No reasoning provided")})

                    if signal_data:
                        # Sort analysts by confidence level (descending)
                        signal_data.sort(key=lambda x: x["confidence"], reverse=True)

                        # Create 3 columns for displaying analysts
                        analyst_cols = st.columns(3)

                        # Display analyst cards in columns
                        for i, signal in enumerate(signal_data):
                            col_idx = i % 3

                            # Create a clickable card for each analyst
                            analyst_card = f"""
                            <div class="analyst-card {signal['signal_class']}" 
                                style="padding: 10px; margin-bottom: 10px; background-color: #2C3E50;">
                                <div class="analyst-heading">{signal['agent_display']}</div>
                                <div>Signal: <span style="font-weight: bold;">{signal['signal_type']}</span></div>
                                <div>Confidence: {signal['confidence']:.1f}%</div>
                                <div><span class="clickable-text">View Reasoning</span></div>
                            </div>
                            """

                            # When clicked, set the selected analyst for this ticker
                            if analyst_cols[col_idx].markdown(analyst_card, unsafe_allow_html=True):
                                st.session_state.selected_analyst[ticker] = signal["agent_name"]

                            # Alternative click detection method using a button
                            if analyst_cols[col_idx].button(f"View {signal['agent_display']} Reasoning", key=f"{ticker}_{signal['agent_name']}", use_container_width=True):
                                st.session_state.selected_analyst[ticker] = signal["agent_name"]

                        # Display selected analyst reasoning
                        if st.session_state.selected_analyst.get(ticker):
                            selected_agent = st.session_state.selected_analyst[ticker]
                            selected_signal = next((s for s in signal_data if s["agent_name"] == selected_agent), None)

                            if selected_signal:
                                st.markdown(f"#### {selected_signal['agent_display']} Reasoning")

                                # Format reasoning based on signal type
                                signal_color = {"BULLISH": "success", "BEARISH": "error", "NEUTRAL": "warning"}.get(selected_signal["signal_type"], "info")

                                st.markdown(f"**Signal:** {selected_signal['signal_type']} | **Confidence:** {selected_signal['confidence']:.1f}%")
                                st.markdown("**Reasoning:**")
                                st.markdown(f"<div style='padding: 10px; border-radius: 5px;'>{selected_signal['reasoning']}</div>", unsafe_allow_html=True)
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
        st.error(f"Error displaying results: {str(e)}")
        import traceback

        st.code(traceback.format_exc())
        # Display raw result for debugging
        if st.checkbox("Show raw results data"):
            st.json(st.session_state.result)

# Display instructions if no analysis has been run
if not st.session_state.get("run_complete", False):
    st.info(
        """
    Configure your analysis parameters in the sidebar and click "Run Analysis" to start.
    
    The AI Hedge Fund will:
    1. Analyze selected stocks using multiple AI analyst agents
    2. Generate trading signals based on fundamental, technical, and sentiment analysis
    3. Provide detailed reasoning for each recommendation
    
    You can click on each analyst to view their detailed reasoning!
    """
    )

# Footer
st.markdown("---")
st.markdown("AI Hedge Fund - For Educational Purposes Only")
