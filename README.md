# 🎨 PromoLogos — AI-Powered Logo Generator

A Python-based web application that generates custom logos from natural language client prompts using AI image generation APIs.

## ✨ Features

- **Prompt-driven logo generation** — describe your logo in plain text, get a professional result
- **Multiple style presets** — minimalist, corporate, retro, modern, gradient, etc.
- **Color palette customization** — specify brand colors or let AI suggest harmonious palettes
- **Format export** — download logos as PNG, SVG, or PDF
- **History & versioning** — keep track of all generated logos per client
- **REST API** — integrate logo generation into your own pipeline
- **Web UI** — simple browser-based interface for non-technical users

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11, FastAPI |
| AI Engine | OpenAI DALL·E 3 / Stable Diffusion (configurable) |
| Image Processing | Pillow, CairoSVG |
| Frontend | HTML5 + Vanilla JS (Jinja2 templates) |
| Storage | Local filesystem / AWS S3 (configurable) |
| Config | python-dotenv |

## 📁 Project Structure

```
promo_logos/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration and environment variables
│   ├── generator.py         # Logo generation logic
│   ├── image_utils.py       # Image processing utilities
│   ├── models.py            # Pydantic request/response models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── api.py           # REST API routes
│   │   └── web.py           # Web UI routes
│   └── templates/
│       ├── index.html       # Main web UI
│       └── result.html      # Result display page
├── outputs/                 # Generated logo files (gitignored)
├── tests/
│   ├── test_generator.py
│   └── test_api.py
├── .env.example             # Environment variable template
├── requirements.txt         # Python dependencies
├── Dockerfile               # Container setup
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- An OpenAI API key (or a running Stable Diffusion instance)

### Installation

```bash
# Clone the repository
git clone https://github.com/chereshnya497/promo_logos.git
cd promo_logos

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate      # Linux/macOS
# venv\Scripts\activate       # Windows

# Install dependencies
pip install -r requirements.txt

# Copy and fill in your environment variables
cp .env.example .env
```

### Configuration

Edit `.env`:

```env
OPENAI_API_KEY=your_openai_api_key_here
AI_BACKEND=openai          # or "stable_diffusion"
SD_API_URL=http://localhost:7860  # only if using Stable Diffusion
OUTPUT_DIR=outputs
MAX_LOGOS_PER_REQUEST=5
IMAGE_SIZE=1024x1024
```

### Run the App

```bash
uvicorn app.main:app --reload
```

Open your browser at **http://localhost:8000**

## 📡 API Usage

### Generate a Logo

```http
POST /api/generate
Content-Type: application/json

{
  "prompt": "A modern tech startup logo with a rocket and the letter T, blue and white palette",
  "style": "minimalist",
  "colors": ["#0A84FF", "#FFFFFF"],
  "format": "png",
  "size": "1024x1024"
}
```

**Response:**
```json
{
  "id": "logo_20260604_abc123",
  "url": "/outputs/logo_20260604_abc123.png",
  "prompt": "A modern tech startup logo...",
  "created_at": "2026-06-04T12:00:00Z"
}
```

### List Generated Logos

```http
GET /api/logos?limit=10&offset=0
```

## 🐳 Docker

```bash
docker build -t promo_logos .
docker run -p 8000:8000 --env-file .env promo_logos
```

## 🧪 Tests

```bash
pytest tests/ -v
```

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "Add my feature"`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request
