# Multilingual Money Changer

A multilingual currency conversion application powered by AI that understands natural language input and converts between currencies using real-time exchange rates.

## Features

- **Multilingual Support**: Accept currency conversion requests in any language
- **Natural Language Processing**: Uses GPT-4o-mini to understand user intent and extract currency codes
- **Real-time Exchange Rates**: Integrates with ExchangeRate-API for accurate, up-to-date rates
- **Web UI**: Built with Gradio for easy browser-based access
- **Tracing & Observability**: Integrated with LangSmith for monitoring and debugging

## Prerequisites

- Python 3.8+
- API Keys:
  - [ExchangeRate-API](https://www.exchangerate-api.com/) key
  - [GitHub Token](https://github.com/settings/tokens) for GitHub Models (GPT-4o-mini access)
  - [LangSmith API Key](https://smith.langchain.com/) (optional, for tracing)

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root:
   ```
   EXCHANGERATE_API_KEY=your_exchangerate_api_key
   GITHUB_TOKEN=your_github_token
   LANGSMITH_API_KEY=your_langsmith_api_key
   LANGSMITH_TRACING=true
   LANGSMITH_PROJECT=your_project_name
   ```

## Running the Application

```bash
python main.py
```

The application will start a Gradio web server (typically at `http://localhost:7860`). Open this URL in your browser.

## Usage Examples

- `100 USD to EUR`
- `100 US money to England money`
- `50 ユーロをドルに変換` (Japanese: "Convert 50 euros to dollars")
- `Convierte 1000 pesos a dólares` (Spanish: "Convert 1000 pesos to dollars")

## Project Structure

```
moneychanger/
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py            # Configuration & environment variables
│   │   ├── tools.py             # Exchange rate API integration
│   │   └── pipeline.py          # Business logic orchestration
│   ├── llm/
│   │   ├── __init__.py
│   │   └── llm_service.py       # LLM (GPT-4o-mini) integration
│   ├── ui/
│   │   ├── __init__.py
│   │   └── ui.py                # Gradio web interface
│   └── __init__.py
├── main.py                       # Application entry point
├── requirements.txt              # Python dependencies
├── README.md                     # This file
└── test_moneychanger.py         # Tests
```

### Module Descriptions

**src/core/**
- **config.py**: Loads environment variables and sets up LangSmith tracing
- **tools.py**: Contains `get_exchange_rate()` function that calls the ExchangeRate-API
- **pipeline.py**: Orchestrates the complete workflow (user input → LLM → function calling → result)

**src/llm/**
- **llm_service.py**: Handles communication with GPT-4o-mini via GitHub Models, including function calling setup

**src/ui/**
- **ui.py**: Defines the Gradio interface with input/output components

**Root**
- **main.py**: Entry point that initializes the application

## How It Works

1. User enters a conversion request in the Gradio interface
2. **pipeline.py** sends the input to **llm_service.py**
3. GPT-4o-mini processes the request and decides whether to call `get_exchange_rate`
4. If function calling is triggered:
   - LLM extracts base currency, target currency, and amount
   - **tools.py** fetches the exchange rate from ExchangeRate-API
   - Result is formatted and returned to the UI
5. If no function calling needed, LLM responds directly with clarification

## Dependencies

See `requirements.txt` for the complete list:
- `gradio` - Web UI framework
- `openai` - OpenAI/GitHub Models client
- `requests` - HTTP requests
- `python-dotenv` - Environment variable management
- `langsmith` - LLM tracing and observability
- `truststore` - SSL certificate handling

## Troubleshooting

**Error: "API key not found"**
- Ensure your `.env` file is in the project root directory
- Check that all required keys are set

**Error: "Connection refused"**
- Verify your internet connection
- Check that API endpoints are accessible
- Confirm API keys are valid

**No function calling happening**
- Check LangSmith traces to see what the LLM decided
- Verify the input clearly indicates a currency conversion request

## Future Enhancements

- Cache exchange rates to reduce API calls
- Support for cryptocurrency conversions
- Historical rate charts
- Batch conversion support
- Multi-language UI

## License

MIT