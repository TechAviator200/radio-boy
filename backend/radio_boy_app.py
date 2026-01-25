"""
Radio Boy - Apple Music-style chat interface
Uses OpenAI for music recommendations and Deezer for 30-second previews
"""
import os
import httpx
from typing import Optional
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
from dotenv import load_dotenv
import uvicorn
import json
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-vercel-domain.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI()

# Store collected emails (in production, use a database)
collected_emails = []

# Serve static files (video, etc.)
app.mount("/public", StaticFiles(directory="public"), name="public")

# System prompt for Radio Boy
SYSTEM_PROMPT = """You are Radio Boy, a cool and knowledgeable music curator, songwriting assistant, and creative workflow manager with the vibe of a late-night radio DJ meets studio producer.

You have THREE core capabilities:

## 1. MUSIC DISCOVERY
When users describe a vibe, mood, or ask for music recommendations:
- Give a brief, enthusiastic comment (1-2 sentences)
- Recommend 2-3 specific songs that match

## 2. SONGWRITING ASSISTANCE
When users share rough ideas, melodies, or want help with songwriting:
- Turn rough ideas into lyrics concepts
- Create hooks, ad-libs, and catchy phrases
- Suggest song structure (verse, chorus, bridge, outro)
- Provide reference tracks for inspiration
- Help with rhyme schemes and flow

## 3. WORKFLOW MANAGEMENT
When users need help organizing their creative process:
- Create and manage session notes
- Build to-do lists for their project
- Track versions of their work
- Provide release checklists
- Set milestones and deadlines

IMPORTANT: Always respond with valid JSON in this exact format:
{
    "message": "Your response here - can be longer for songwriting/workflow tasks",
    "tracks": [
        {"artist": "Artist Name", "title": "Song Title"}
    ],
    "lyrics": {
        "hook": "The catchy hook line if applicable",
        "verse": "Verse lyrics if applicable",
        "structure": "Song structure suggestion if applicable",
        "adlibs": ["ad-lib 1", "ad-lib 2"]
    },
    "workflow": {
        "type": "note|todo|checklist|version",
        "title": "Title of the item",
        "items": ["item 1", "item 2", "item 3"]
    }
}

Rules:
- Only include "tracks" array if recommending music (otherwise empty array)
- Only include "lyrics" object if helping with songwriting (otherwise null)
- Only include "workflow" object if managing workflow (otherwise null)
- Keep your vibe cool and creative, like a producer in the studio
- Use music industry slang naturally
- Be encouraging and collaborative"""


async def search_deezer(artist: str, title: str) -> Optional[dict]:
    """Search Deezer for a track and return preview URL"""
    query = f"{artist} {title}"
    async with httpx.AsyncClient() as http_client:
        try:
            response = await http_client.get(
                "https://api.deezer.com/search",
                params={"q": query, "limit": 1}
            )
            data = response.json()
            if data.get("data") and len(data["data"]) > 0:
                track = data["data"][0]
                return {
                    "id": track["id"],
                    "title": track["title"],
                    "artist": track["artist"]["name"],
                    "album": track["album"]["title"],
                    "cover": track["album"]["cover_medium"],
                    "preview": track["preview"]  # 30-second preview URL
                }
        except Exception as e:
            print(f"Deezer search error: {e}")
    return None


# The Apple Music-style HTML template with email gateway
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Radio Boy</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background: #000;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        }

        /* Email Gateway Overlay */
        .gateway-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.95);
            display: flex;
            z-index: 1000;
        }

        .gateway-overlay.hidden {
            display: none;
        }

        .gateway-left {
            width: 400px;
            background: #1c1c1e;
            padding: 40px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            border-right: 1px solid #3a3a3c;
        }

        .gateway-right {
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 40px;
        }

        .gateway-right video {
            max-width: 400px;
            max-height: 400px;
            border-radius: 24px;
            box-shadow: 0 20px 60px rgba(255, 45, 85, 0.3);
        }

        .gateway-logo {
            font-size: 32px;
            font-weight: 700;
            color: #fff;
            margin-bottom: 8px;
        }

        .gateway-tagline {
            font-size: 16px;
            color: #ff2d55;
            margin-bottom: 40px;
        }

        .gateway-title {
            font-size: 24px;
            font-weight: 600;
            color: #fff;
            margin-bottom: 8px;
        }

        .gateway-subtitle {
            font-size: 14px;
            color: #8e8e93;
            margin-bottom: 24px;
        }

        .google-btn {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            width: 100%;
            padding: 14px 20px;
            background: #fff;
            border: none;
            border-radius: 12px;
            font-size: 15px;
            font-weight: 600;
            color: #1c1c1e;
            cursor: pointer;
            transition: background 0.2s;
            margin-bottom: 20px;
        }

        .google-btn:hover {
            background: #f0f0f0;
        }

        .google-btn svg {
            width: 20px;
            height: 20px;
        }

        .divider {
            display: flex;
            align-items: center;
            margin: 20px 0;
        }

        .divider::before,
        .divider::after {
            content: '';
            flex: 1;
            height: 1px;
            background: #3a3a3c;
        }

        .divider span {
            padding: 0 16px;
            color: #8e8e93;
            font-size: 13px;
        }

        .email-input {
            width: 100%;
            padding: 14px 16px;
            background: #2c2c2e;
            border: 1px solid #3a3a3c;
            border-radius: 12px;
            font-size: 15px;
            color: #fff;
            outline: none;
            margin-bottom: 16px;
        }

        .email-input::placeholder {
            color: #8e8e93;
        }

        .email-input:focus {
            border-color: #ff2d55;
        }

        .continue-btn {
            width: 100%;
            padding: 14px 20px;
            background: #ff2d55;
            border: none;
            border-radius: 12px;
            font-size: 15px;
            font-weight: 600;
            color: #fff;
            cursor: pointer;
            transition: background 0.2s;
        }

        .continue-btn:hover {
            background: #ff375f;
        }

        .continue-btn:disabled {
            background: #3a3a3c;
            cursor: not-allowed;
        }

        .gateway-footer {
            margin-top: 24px;
            font-size: 12px;
            color: #8e8e93;
            text-align: center;
        }

        .gateway-footer a {
            color: #ff2d55;
            text-decoration: none;
        }

        .email-error {
            color: #ff453a;
            font-size: 13px;
            margin-bottom: 12px;
            display: none;
        }

        .email-error.show {
            display: block;
        }

        /* Main App Card */
        .card {
            background: #1c1c1e;
            border-radius: 24px;
            overflow: hidden;
            border: 1px solid #3a3a3c;
            box-shadow: 0 20px 40px rgba(0,0,0,0.45);
            width: 100%;
            max-width: 420px;
            color: #fff;
        }

        .video-container {
            width: 100%;
            aspect-ratio: 1/1;
            background: #000;
            position: relative;
        }

        .video-container video {
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
        }

        .now-playing {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: linear-gradient(transparent, rgba(0,0,0,0.9));
            padding: 40px 16px 16px;
            display: none;
        }

        .now-playing.active {
            display: block;
        }

        .now-playing-content {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .now-playing-cover {
            width: 48px;
            height: 48px;
            border-radius: 6px;
            object-fit: cover;
        }

        .now-playing-info {
            flex: 1;
            min-width: 0;
        }

        .now-playing-title {
            font-size: 14px;
            font-weight: 600;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .now-playing-artist {
            font-size: 12px;
            color: #ff2d55;
        }

        .content {
            padding: 20px;
        }

        .header-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 4px;
        }

        .title {
            font-size: 22px;
            font-weight: 700;
            color: #ffffff;
        }

        .user-email {
            font-size: 12px;
            color: #8e8e93;
            background: #2c2c2e;
            padding: 4px 10px;
            border-radius: 12px;
        }

        .user-section {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .signout-btn {
            font-size: 11px;
            color: #ff453a;
            background: transparent;
            border: 1px solid #ff453a;
            padding: 4px 10px;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.2s;
        }

        .signout-btn:hover {
            background: #ff453a;
            color: #fff;
        }

        .subtitle {
            font-size: 14px;
            color: #ff2d55;
            margin-bottom: 14px;
        }

        .conversation {
            font-size: 15px;
            line-height: 1.6;
            color: #d1d1d6;
            max-height: 300px;
            overflow-y: auto;
            margin-bottom: 16px;
        }

        .conversation::-webkit-scrollbar {
            width: 6px;
        }

        .conversation::-webkit-scrollbar-track {
            background: #1c1c1e;
        }

        .conversation::-webkit-scrollbar-thumb {
            background: #3a3a3c;
            border-radius: 3px;
        }

        .message {
            margin-bottom: 12px;
        }

        .message.user .speaker {
            color: #ff2d55;
            font-weight: 600;
        }

        .message.assistant .speaker {
            color: #ffffff;
            font-weight: 600;
        }

        .message .text {
            color: #d1d1d6;
        }

        .tracks {
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin-top: 10px;
        }

        .track-card {
            display: flex;
            align-items: center;
            gap: 10px;
            background: #2c2c2e;
            border-radius: 10px;
            padding: 10px;
            cursor: pointer;
            transition: background 0.2s;
        }

        .track-card:hover {
            background: #3a3a3c;
        }

        .track-card.playing {
            background: #ff2d55;
        }

        .track-cover {
            width: 44px;
            height: 44px;
            border-radius: 6px;
            object-fit: cover;
        }

        .track-info {
            flex: 1;
            min-width: 0;
        }

        .track-title {
            font-size: 14px;
            font-weight: 600;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .track-artist {
            font-size: 12px;
            color: #8e8e93;
        }

        .track-card.playing .track-artist {
            color: rgba(255,255,255,0.8);
        }

        .play-btn {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: #ff2d55;
            border: none;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            flex-shrink: 0;
        }

        .track-card.playing .play-btn {
            background: #fff;
        }

        .play-btn svg {
            width: 14px;
            height: 14px;
            fill: #fff;
        }

        .track-card.playing .play-btn svg {
            fill: #ff2d55;
        }

        .input-container {
            display: flex;
            gap: 10px;
        }

        .input-container input {
            flex: 1;
            background: #2c2c2e;
            border: 1px solid #3a3a3c;
            border-radius: 12px;
            padding: 12px 16px;
            color: #fff;
            font-size: 15px;
            outline: none;
            font-family: inherit;
        }

        .input-container input::placeholder {
            color: #8e8e93;
        }

        .input-container input:focus {
            border-color: #ff2d55;
        }

        .input-container button {
            background: #ff2d55;
            border: none;
            border-radius: 12px;
            padding: 12px 20px;
            color: #fff;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            font-family: inherit;
            transition: background 0.2s;
        }

        .input-container button:hover {
            background: #ff375f;
        }

        .input-container button:disabled {
            background: #3a3a3c;
            cursor: not-allowed;
        }

        .empty-state {
            color: #8e8e93;
            font-style: italic;
        }

        /* Lyrics Section */
        .lyrics-section {
            background: linear-gradient(135deg, #2c2c2e 0%, #1c1c1e 100%);
            border: 1px solid #3a3a3c;
            border-radius: 12px;
            padding: 14px;
            margin-top: 10px;
        }

        .lyrics-header {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 10px;
            font-size: 13px;
            color: #ff2d55;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .lyrics-header svg {
            width: 16px;
            height: 16px;
            fill: #ff2d55;
        }

        .lyrics-part {
            margin-bottom: 12px;
        }

        .lyrics-label {
            font-size: 11px;
            color: #8e8e93;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 4px;
        }

        .lyrics-content {
            font-size: 14px;
            color: #fff;
            line-height: 1.5;
            font-style: italic;
        }

        .lyrics-hook {
            font-size: 16px;
            font-weight: 600;
            color: #ff2d55;
            font-style: normal;
        }

        .adlibs {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }

        .adlib-tag {
            background: #ff2d55;
            color: #fff;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 500;
        }

        /* Workflow Section */
        .workflow-section {
            background: linear-gradient(135deg, #1a2f1a 0%, #1c1c1e 100%);
            border: 1px solid #2d4a2d;
            border-radius: 12px;
            padding: 14px;
            margin-top: 10px;
        }

        .workflow-header {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 10px;
            font-size: 13px;
            color: #30d158;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .workflow-header svg {
            width: 16px;
            height: 16px;
            fill: #30d158;
        }

        .workflow-title {
            font-size: 15px;
            font-weight: 600;
            color: #fff;
            margin-bottom: 10px;
        }

        .workflow-items {
            list-style: none;
        }

        .workflow-item {
            display: flex;
            align-items: flex-start;
            gap: 10px;
            padding: 8px 0;
            border-bottom: 1px solid #2d4a2d;
            font-size: 14px;
            color: #d1d1d6;
        }

        .workflow-item:last-child {
            border-bottom: none;
        }

        .workflow-checkbox {
            width: 18px;
            height: 18px;
            border: 2px solid #30d158;
            border-radius: 4px;
            flex-shrink: 0;
            margin-top: 2px;
        }

        .workflow-number {
            width: 22px;
            height: 22px;
            background: #30d158;
            color: #000;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: 600;
            flex-shrink: 0;
        }

        .loading {
            display: inline-block;
            width: 16px;
            height: 16px;
            border: 2px solid #3a3a3c;
            border-top-color: #ff2d55;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
            margin-left: 8px;
            vertical-align: middle;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        @media (max-width: 800px) {
            .gateway-overlay {
                flex-direction: column;
            }
            .gateway-left {
                width: 100%;
                border-right: none;
                border-bottom: 1px solid #3a3a3c;
            }
            .gateway-right {
                display: none;
            }
        }
    </style>
</head>
<body>
    <!-- Email Gateway Overlay -->
    <div class="gateway-overlay" id="gateway">
        <div class="gateway-left">
            <div class="gateway-logo">Radio Boy</div>
            <div class="gateway-tagline">Your AI Music Curator</div>

            <div class="gateway-title">Get Started</div>
            <div class="gateway-subtitle">Enter your email to discover personalized music recommendations</div>

            <button class="google-btn" onclick="signInWithGoogle()">
                <svg viewBox="0 0 24 24">
                    <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                    <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                    <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                    <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                </svg>
                Continue with Google
            </button>

            <div class="divider"><span>or</span></div>

            <input type="email" class="email-input" id="emailInput" placeholder="Enter your email address">
            <div class="email-error" id="emailError">Please enter a valid email address</div>
            <button class="continue-btn" onclick="submitEmail()">Continue</button>

            <div class="gateway-footer">
                By continuing, you agree to receive music recommendations.<br>
                <a href="#">Privacy Policy</a>
            </div>
        </div>
        <div class="gateway-right">
            <video src="/public/animation.mp4" autoplay loop muted playsinline></video>
        </div>
    </div>

    <!-- Main App Card -->
    <div class="card">
        <div class="video-container">
            <video src="/public/animation.mp4" autoplay loop muted playsinline></video>
            <div class="now-playing" id="nowPlaying">
                <div class="now-playing-content">
                    <img class="now-playing-cover" id="npCover" src="" alt="">
                    <div class="now-playing-info">
                        <div class="now-playing-title" id="npTitle"></div>
                        <div class="now-playing-artist" id="npArtist"></div>
                    </div>
                </div>
            </div>
        </div>

        <div class="content">
            <div class="header-row">
                <div class="title">Radio Boy</div>
                <div class="user-section">
                    <div class="user-email" id="userEmailDisplay"></div>
                    <button class="signout-btn" id="signoutBtn" onclick="signOut()">Sign Out</button>
                </div>
            </div>
            <div class="subtitle">I hear a vibe - let us build it out.</div>

            <div class="conversation" id="conversation">
                <div class="empty-state">Tell me your vibe and I will find the perfect tracks.</div>
            </div>

            <div class="input-container">
                <input type="text" id="input" placeholder="What is your vibe?" autocomplete="off">
                <button id="send" onclick="sendMessage()">Send</button>
            </div>
        </div>
    </div>

    <audio id="audioPlayer"></audio>

    <script>
        const gateway = document.getElementById('gateway');
        const emailInput = document.getElementById('emailInput');
        const emailError = document.getElementById('emailError');
        const conversationEl = document.getElementById('conversation');
        const inputEl = document.getElementById('input');
        const sendBtn = document.getElementById('send');
        const audioPlayer = document.getElementById('audioPlayer');
        const nowPlaying = document.getElementById('nowPlaying');
        const userEmailDisplay = document.getElementById('userEmailDisplay');

        let userEmail = localStorage.getItem('radioboy_email');
        let history = [];
        let currentlyPlaying = null;

        const playIcon = '<svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>';
        const pauseIcon = '<svg viewBox="0 0 24 24"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg>';

        // Check if user already logged in
        if (userEmail) {
            gateway.classList.add('hidden');
            userEmailDisplay.textContent = userEmail;
            document.getElementById('signoutBtn').style.display = 'inline-block';
            inputEl.focus();
        } else {
            document.getElementById('signoutBtn').style.display = 'none';
        }

        function validateEmail(email) {
            const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return re.test(email);
        }

        function signInWithGoogle() {
            // For demo, prompt for email (in production, use real Google OAuth)
            const email = prompt('Enter your Google email:');
            if (email && validateEmail(email)) {
                saveEmail(email);
            }
        }

        function submitEmail() {
            const email = emailInput.value.trim();
            if (!validateEmail(email)) {
                emailError.classList.add('show');
                return;
            }
            emailError.classList.remove('show');
            saveEmail(email);
        }

        async function saveEmail(email) {
            userEmail = email;
            localStorage.setItem('radioboy_email', email);

            // Send to backend
            try {
                await fetch('/collect-email', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email: email })
                });
            } catch (e) {
                console.error('Failed to save email:', e);
            }

            gateway.classList.add('hidden');
            userEmailDisplay.textContent = email;
            document.getElementById('signoutBtn').style.display = 'inline-block';
            inputEl.focus();
        }

        function signOut() {
            // Clear localStorage
            localStorage.removeItem('radioboy_email');
            userEmail = null;

            // Clear conversation history
            history = [];
            renderConversation();

            // Stop any playing audio
            audioPlayer.pause();
            currentlyPlaying = null;
            nowPlaying.classList.remove('active');

            // Hide user email and sign out button
            userEmailDisplay.textContent = '';
            document.getElementById('signoutBtn').style.display = 'none';

            // Show the gateway overlay
            gateway.classList.remove('hidden');
        }

        // Allow Enter key on email input
        emailInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') submitEmail();
        });

        const micIcon = '<svg viewBox="0 0 24 24"><path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/><path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/></svg>';
        const checklistIcon = '<svg viewBox="0 0 24 24"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-9 14l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>';

        function renderConversation() {
            if (history.length === 0) {
                conversationEl.innerHTML = '<div class="empty-state">Tell me your vibe, share song ideas, or ask me to help manage your creative workflow.</div>';
                return;
            }

            conversationEl.innerHTML = history.map((msg, idx) => {
                let tracksHtml = '';
                let lyricsHtml = '';
                let workflowHtml = '';

                // Render tracks
                if (msg.tracks && msg.tracks.length > 0) {
                    tracksHtml = '<div class="tracks">' + msg.tracks.map((track, trackIdx) => {
                        const safeTitle = track.title.replace(/'/g, "&#39;");
                        const safeArtist = track.artist.replace(/'/g, "&#39;");
                        return '<div class="track-card" data-preview="' + track.preview + '" data-title="' + safeTitle + '" data-artist="' + safeArtist + '" data-cover="' + track.cover + '" onclick="playTrack(this)">' +
                            '<img class="track-cover" src="' + track.cover + '" alt="">' +
                            '<div class="track-info">' +
                                '<div class="track-title">' + track.title + '</div>' +
                                '<div class="track-artist">' + track.artist + '</div>' +
                            '</div>' +
                            '<button class="play-btn">' + playIcon + '</button>' +
                        '</div>';
                    }).join('') + '</div>';
                }

                // Render lyrics
                if (msg.lyrics) {
                    let lyricsParts = '';
                    if (msg.lyrics.hook) {
                        lyricsParts += '<div class="lyrics-part"><div class="lyrics-label">Hook</div><div class="lyrics-content lyrics-hook">' + msg.lyrics.hook + '</div></div>';
                    }
                    if (msg.lyrics.verse) {
                        lyricsParts += '<div class="lyrics-part"><div class="lyrics-label">Verse</div><div class="lyrics-content">' + msg.lyrics.verse.replace(/\\n/g, '<br>') + '</div></div>';
                    }
                    if (msg.lyrics.structure) {
                        lyricsParts += '<div class="lyrics-part"><div class="lyrics-label">Structure</div><div class="lyrics-content">' + msg.lyrics.structure + '</div></div>';
                    }
                    if (msg.lyrics.adlibs && msg.lyrics.adlibs.length > 0) {
                        lyricsParts += '<div class="lyrics-part"><div class="lyrics-label">Ad-libs</div><div class="adlibs">' +
                            msg.lyrics.adlibs.map(a => '<span class="adlib-tag">' + a + '</span>').join('') + '</div></div>';
                    }
                    if (lyricsParts) {
                        lyricsHtml = '<div class="lyrics-section"><div class="lyrics-header">' + micIcon + ' Songwriting</div>' + lyricsParts + '</div>';
                    }
                }

                // Render workflow
                if (msg.workflow && msg.workflow.items && msg.workflow.items.length > 0) {
                    const isChecklist = msg.workflow.type === 'todo' || msg.workflow.type === 'checklist';
                    const itemsHtml = msg.workflow.items.map((item, i) => {
                        const indicator = isChecklist ?
                            '<div class="workflow-checkbox"></div>' :
                            '<div class="workflow-number">' + (i + 1) + '</div>';
                        return '<div class="workflow-item">' + indicator + '<span>' + item + '</span></div>';
                    }).join('');
                    workflowHtml = '<div class="workflow-section"><div class="workflow-header">' + checklistIcon + ' ' + (msg.workflow.type || 'Workflow') + '</div>' +
                        '<div class="workflow-title">' + (msg.workflow.title || '') + '</div>' +
                        '<div class="workflow-items">' + itemsHtml + '</div></div>';
                }

                return '<div class="message ' + msg.role + '">' +
                    '<span class="speaker">' + (msg.role === 'user' ? 'You' : 'Radio Boy') + ':</span>' +
                    '<span class="text"> ' + msg.text + '</span>' +
                    tracksHtml + lyricsHtml + workflowHtml +
                '</div>';
            }).join('');

            conversationEl.scrollTop = conversationEl.scrollHeight;
        }

        function playTrack(element) {
            const preview = element.dataset.preview;
            const title = element.dataset.title;
            const artist = element.dataset.artist;
            const cover = element.dataset.cover;

            document.querySelectorAll('.track-card').forEach(el => {
                el.classList.remove('playing');
                el.querySelector('.play-btn').innerHTML = playIcon;
            });

            if (currentlyPlaying === preview && !audioPlayer.paused) {
                audioPlayer.pause();
                currentlyPlaying = null;
                nowPlaying.classList.remove('active');
            } else {
                audioPlayer.src = preview;
                audioPlayer.play();
                currentlyPlaying = preview;
                element.classList.add('playing');
                element.querySelector('.play-btn').innerHTML = pauseIcon;

                document.getElementById('npCover').src = cover;
                document.getElementById('npTitle').textContent = title;
                document.getElementById('npArtist').textContent = artist;
                nowPlaying.classList.add('active');
            }
        }

        audioPlayer.addEventListener('ended', () => {
            document.querySelectorAll('.track-card').forEach(el => {
                el.classList.remove('playing');
                el.querySelector('.play-btn').innerHTML = playIcon;
            });
            currentlyPlaying = null;
            nowPlaying.classList.remove('active');
        });

        async function sendMessage() {
            const text = inputEl.value.trim();
            if (!text) return;

            inputEl.disabled = true;
            sendBtn.disabled = true;

            history.push({ role: 'user', text: text, tracks: [] });
            renderConversation();
            inputEl.value = '';

            conversationEl.innerHTML += '<div class="message assistant"><span class="speaker">Radio Boy:</span><span class="loading"></span></div>';
            conversationEl.scrollTop = conversationEl.scrollHeight;

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text, email: userEmail })
                });

                const data = await response.json();
                history.push({
                    role: 'assistant',
                    text: data.message,
                    tracks: data.tracks || [],
                    lyrics: data.lyrics || null,
                    workflow: data.workflow || null
                });
                renderConversation();
            } catch (error) {
                console.error('Error:', error);
                history.push({ role: 'assistant', text: 'Oops, something went wrong. Try again!', tracks: [], lyrics: null, workflow: null });
                renderConversation();
            }

            inputEl.disabled = false;
            sendBtn.disabled = false;
            inputEl.focus();
        }

        inputEl.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def get_home():
    return HTML_TEMPLATE


@app.post("/collect-email")
async def collect_email(request: Request):
    data = await request.json()
    email = data.get("email", "")
    if email and email not in collected_emails:
        collected_emails.append(email)
        print(f"New email collected: {email}")
    return JSONResponse({"status": "ok"})


@app.get("/emails")
async def get_emails():
    """Admin endpoint to see collected emails"""
    return JSONResponse({"emails": collected_emails, "count": len(collected_emails)})


@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "")
    user_email = data.get("email", "")

    try:
        # Call OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.8
        )

        content = response.choices[0].message.content.strip()

        # Parse JSON response
        try:
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]

            parsed = json.loads(content)
            message = parsed.get("message", "Let me find some tracks for you...")
            track_requests = parsed.get("tracks", [])
            lyrics = parsed.get("lyrics", None)
            workflow = parsed.get("workflow", None)
        except json.JSONDecodeError:
            message = content
            track_requests = []
            lyrics = None
            workflow = None

        # Search Deezer for each track
        tracks = []
        for track_req in track_requests[:3]:
            artist = track_req.get("artist", "")
            title = track_req.get("title", "")
            if artist and title:
                track_data = await search_deezer(artist, title)
                if track_data:
                    tracks.append(track_data)

        return JSONResponse({
            "message": message,
            "tracks": tracks,
            "lyrics": lyrics,
            "workflow": workflow
        })

    except Exception as e:
        print(f"Error: {e}")
        return JSONResponse({
            "message": "Sorry, I hit a snag. Try again!",
            "tracks": [],
            "lyrics": None,
            "workflow": None
        })


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
