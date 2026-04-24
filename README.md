# ExplorAR Glasses

ExplorAR Glasses is a modular **augmented reality (AR) travel assistance system** that combines contextual intelligence, location services, navigation, weather updates, translation, OCR, and voice interaction into a single platform.

The project is being developed as a **lightweight MVP** first, with a backend-first architecture that can later be extended into:
- **iPhone applications**
- **Android applications**
- **AR / smart wearable integration**

---

## Overview

Modern travelers often switch between multiple applications for:
- navigation
- translation
- weather updates
- landmark information
- voice assistance

ExplorAR Glasses aims to unify these features into one intelligent system that can later power mobile and wearable travel experiences.

---

## Objectives

- Build a modular travel assistant platform
- Provide contextual information for places and landmarks
- Support navigation and geolocation workflows
- Enable text translation and OCR-based text extraction
- Support voice-query-based interaction
- Keep the MVP lightweight and easy to expand
- Prepare the system for future AR glasses integration

---

## Core Features

- **Contextual Intelligence**
  - Travel, landmark, and place-based information
- **Location Services**
  - Reverse geocoding and location-aware responses
- **Navigation**
  - Route guidance and directional assistance
- **Weather Updates**
  - Real-time or mock weather responses
- **Translation**
  - Text translation into target languages
- **OCR**
  - Extract text from uploaded images
- **Voice Interaction**
  - Query-response architecture for future speech support
- **Caching / Local Data Layer**
  - Lightweight storage for recent data and mock content

---

## System Modules

### 1. Health / System Status Module
Checks whether the backend is running correctly.

### 2. Contextual Intelligence Module
Returns place-based and travel-related contextual information.  
Designed to support future integration with LLM APIs.

### 3. Location Module
Handles reverse geocoding and location query processing.

### 4. Navigation Module
Provides route data and navigation-related responses.

### 5. Weather Module
Fetches or simulates weather information for a requested location.

### 6. Translation Module
Translates plain text into a specified target language.

### 7. OCR Module
Extracts text from uploaded images.

### 8. Voice Interaction Module
Supports query-response architecture for future speech-based assistance.

### 9. Data Layer / Caching Module
Stores recent requests or reusable lightweight travel data.

---

## Project Structure

ExplorAR_Project/
├── backend/
└── mobile_app/

##Backend Structure

backend/
-app.py
-routes/
-service
-data/
-.env\
-.gitignore
-requirements.txt\

## Technology Stack

### Backend
- Python
- Flask
- requests
- python-dotenv

### Frontend
- Flutter
- Chrome (for web-first testing)

### Planned Mobile Targets
- iOS
- Android

### Core Functional Modules
- Contextual Intelligence
- Location Services
- Navigation
- Weather
- Translation
- OCR
- Voice Interaction
- Data Caching / Local Storage

### APIs and External Services
- OpenAI API / Google Gemini API
- OpenWeatherMap API
- OpenCage API / Google Maps Platform / Mapbox
- Google Translate API / LibreTranslate
- Tesseract OCR / OCR.Space / Google Vision API
- Speech-to-Text and Text-to-Speech APIs

### Development Environment
- macOS
- Python virtual environment (venv)
- Git
- GitHub

### Future Integration Targets
- iPhone app
- Android app
- AR smart glasses / wearable devices

## Planned API Endpoints

### Health Check
GET /


### Context Information

GET /context


### Reverse Geocoding
GET /location/reverse-geocode


### Navigation
GET /navigation


### Weather
GET /weather


### Translation
POST /translated

### OCR
POST /ocr

### Voice Query
POST /voice/query


---

## Setup

### 1. Clone the repository

git clone [github.com](https://github.com/YOUR_USERNAME/ExplorAR-Glasses.git)
cd ExplorAR-Glasses


### 2. Create and activate a virtual environment

cd backend
python3 -m venv venv
source venv/bin/activate


### 3. Install dependencies

pip install -r requirements.txt


### 4. Add environment variables
Create a `.env` file inside `backend/`:

- OPENAI_API_KEY=your_key_here
- WEATHER_API_KEY=your_key_here
- GEOCODING_API_KEY=your_key_here
- TRANSLATION_API_KEY=your_key_here
- OCR_API_KEY=your_key_here


### 5. Run the backend

python app.py

---

## Development Approach

This project is being built incrementally:

1. Backend setup
2. Base route implementation
3. Modular service development
4. API integrations
5. Flutter frontend integration
6. Cross-platform mobile support
7. Wearable integration readiness

---

## Git Workflow

Recommended commit style:

git add .
git commit -m "Add backend module setup"
git push origin main

Example commit messages:
- Add initial backend setup
- Add context module
- Add reverse geocoding module
- Add navigation module
- Add translation and OCR modules
- Add voice query module
- Add Flutter frontend scaffold

---

## Important Notes

- Do **not** commit `.env`
- Do **not** commit `venv/`
- Keep API keys private
- Use small, modular commits
- Test each module before expanding it

---

## Current Status

ExplorAR Glasses is currently in the **MVP development phase**, with a backend-first implementation and modular feature development in progress.

---

## Future Scope

- Native Flutter app for Android and iPhone
- AR overlays for real-world travel assistance
- Smart glasses integration
- Offline caching
- Personalized travel recommendations
- Voice-guided wearable interaction

---

## License

This project is currently intended for **academic, prototype, and learning purposes**.  
A formal license can be added later depending on the intended release model.
