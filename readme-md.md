# AI Hedge Fund Web Interface

This is a web interface for the AI Hedge Fund project. It provides a user-friendly way to interact with the AI-powered trading system.

## Features

- Configure stock tickers for analysis
- Set date ranges for analysis
- Adjust initial capital and margin requirements
- Select LLM models from multiple providers (OpenAI, Anthropic, DeepSeek, etc.)
- Choose trading analysts to include in the analysis
- View detailed analyst signals and trading recommendations
- Modern, minimalist UI with expandable sections

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/ai-hedge-fund.git
cd ai-hedge-fund
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables by creating a `.env` file:
```bash
# Create .env file for your API keys
cp .env.example .env
```

4. Fill in the required API keys in your `.env` file:
```bash
# For running LLMs hosted by anthropic (claude-3-5-sonnet, claude-3-opus, claude-3-5-haiku)
ANTHROPIC_API_KEY=your-anthropic-api-key

# For running LLMs hosted by deepseek (deepseek-chat, deepseek-reasoner, etc.)
DEEPSEEK_API_KEY=your-deepseek-api-key

# For running LLMs hosted by groq (deepseek, llama3, etc.)
GROQ_API_KEY=your-groq-api-key

# For running LLMs hosted by gemini (gemini-2.0-flash, gemini-2.0-pro)
GOOGLE_API_KEY=your-google-api-key

# For getting financial data to power the hedge fund
FINANCIAL_DATASETS_API_KEY=your-financial-datasets-api-key

# For running LLMs hosted by openai (gpt-4o, gpt-4o-mini, etc.)
OPENAI_API_KEY=your-openai-api-key
```

## Running the Web Interface

Run the Streamlit app:

```bash
streamlit run app.py
```

The web interface will open in your default browser at `http://localhost:8501`.

## Usage

1. Configure your analysis parameters in the sidebar:
   - Enter comma-separated stock ticker symbols
   - Set start and end dates for the analysis
   - Adjust initial capital and margin requirements
   - Select an LLM model
   - Choose which analyst agents to include

2. Click "Run Analysis" to start the analysis

3. Review the results in the main panel:
   - Trading decisions for each ticker
   - Detailed reasoning behind each decision
   - Analyst signals and confidence scores
   - Portfolio summary

## Disclaimer

This project is for **educational and research purposes only**.

- Not intended for real trading or investment
- No warranties or guarantees provided
- Past performance does not indicate future results
- Creator assumes no liability for financial losses
- Consult a financial advisor for investment decisions

By using this software, you agree to use it solely for learning purposes.
