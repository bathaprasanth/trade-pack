# Trade Opportunities API

A FastAPI service that analyzes market data and provides trade opportunity insights for specific sectors in India using DuckDuckGo Search and Google Gemini.

## Features
- **Market Analysis**: Analyzes specific sectors (e.g., Pharmaceuticals, Technology) using AI.
- **Web Search**: Integrates DuckDuckGo to fetch real-time market news.
- **Security**: Simple API Key authentication.
- **Rate Limiting**: Limits requests to 5 per minute per IP to prevent abuse.
- **FastAPI**: High-performance async API.

## Setup

1. **Clone the repository** (or navigate to the directory).
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   (Or manually: `pip install fastapi uvicorn google-generativeai duckduckgo-search slowapi python-jose pydantic-settings python-multipart requests`)

3. **Configure Environment**:
   Create a `.env` file in the `trade_opportunities_api` directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

## Running the Application
```bash
cd trade_opportunities_api
uvicorn app.main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

## API Usage

### Endpoint: `GET /analyze/{sector}`
**Headers**:
- `X-API-Key`: `gemini-trade-api`

**Example Request**:
```bash
curl -X GET "http://127.0.0.1:8000/analyze/technology" \
     -H "X-API-Key: gemini-trade-api"
```

**Response**:
Returns a JSON object containing the sector name and a Markdown formatted analysis report.

## Deployment

### Option A: Render (Recommended)
1. **GitHub**: Push this repository to GitHub.
2. **Dashboard**: Go to [render.com](https://render.com) and create a "New Web Service".
3. **Connect**: Select your repository.
4. **Settings**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. **Environment Variables**:
   Add your keys in the "Environment" tab:
   - `GEMINI_API_KEY`: `your_google_key`

### Option B: Railway
1. **GitHub**: Push to GitHub.
2. **Dashboard**: Go to [railway.app](https://railway.app) and "New Project" > "Deploy from GitHub repo".
3. **Variables**: Add `GEMINI_API_KEY` in the variables tab.

## Documentation
Interactive API docs are available at `/docs` on your deployed URL.
