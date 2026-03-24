# Deploying HealthTrackAI to Streamlit Cloud

## Prerequisites

1.  **Google Gemini API Key**: You need an API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
2.  **MongoDB Atlas Database**: You need a cloud-hosted MongoDB database (e.g., MongoDB Atlas free tier).
    *   Create a cluster.
    *   Get the connection string (SRV format): `mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority`
    *   Whitelist IP `0.0.0.0/0` in MongoDB Atlas Network Access (Streamlit Cloud uses dynamic IPs).

## Deployment Steps

1.  **Push to GitHub**:
    *   Push this entire project folder to a GitHub repository.

2.  **Streamlit Cloud**:
    *   Go to [share.streamlit.io](https://share.streamlit.io/).
    *   Click **"New app"**.
    *   Select your GitHub repository, branch (`main`), and main file path (`app.py`).

3.  **App Settings (Secrets)**:
    *   Before clicking "Deploy", click **"Advanced settings"** -> **"Secrets"**.
    *   Add your API keys and database connection string in TOML format:

    ```toml
    GOOGLE_API_KEY = "your_google_api_key_here"
    MONGODB_URI = "mongodb+srv://user:pass@cluster.mongodb.net/?retryWrites=true&w=majority"
    MONGODB_DB = "healthtrackAI"
    ```

4.  **Click "Deploy"**:
    *   Streamlit will install dependencies from `requirements.txt` and `packages.txt`.
    *   It will automatically install Tesseract OCR (via `packages.txt`).

## Troubleshooting

*   **PWA**: The Progressive Web App features (install prompt) work on mobile devices when accessed via HTTPS (which Streamlit Cloud provides).
*   **Database**: If the app says "MongoDB Offline", check your MongoDB Atlas Network Access whitelist.
