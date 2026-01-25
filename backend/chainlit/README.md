# Radio Boy - Chainlit Backend

## Local Development

```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
python -m pip install -r requirements.txt

# Verify installation
python -m chainlit --version

# Run the app
python -m chainlit run radio_boy_chainlit.py --host 0.0.0.0 --port 8000
```

Opens at http://localhost:8000

> **Note:** Always use `python -m chainlit` instead of just `chainlit` to avoid PATH issues.

## Deploy to Render

### Start Command

```bash
python -m chainlit run radio_boy_chainlit.py --host 0.0.0.0 --port $PORT
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `PORT` | Auto | Set by Render automatically |
| `OPENAI_API_KEY` | Optional | Required if using AI responses (friend_agent.py) |

### Build Command

```bash
python -m pip install -r requirements.txt
```

## Static Assets

The `public/` folder contains:
- `animation.mp4` - Header video
- `apple-theme.css` - Custom UI theme
- `style.css` - Additional styles

These are served at `/public/*` by Chainlit automatically.
