# Interactive Learning Game Generator

This project consists of a React frontend and Flask API backend that can generate interactive learning games based on any concept or paragraph. The system uses Google's Gemini LLM to analyze content and create appropriate educational games.

## Architecture

### Backend (Flask API)
- Analyzes concepts using Gemini LLM
- Generates interactive SVG-based games
- Provides game instructions and explanations

### Frontend (React)
- User interface for entering concepts
- Game selection and display
- Interactive game playing experience

## Setup Instructions

### Backend Setup

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv .venv
   source venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install flask flask-cors google-generativeai langchain-google-genai python-dotenv
   ```
4. Create a `.env` file in the root directory with your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
5. Start the Flask server:
   ```
   python app.py
   ```
   The server will run on http://localhost:5000

### Frontend Setup (To be implemented)

1. Navigate to the frontend directory
2. Install dependencies:
   ```
   npm install
   ```
3. Start the development server:
   ```
   npm start
   ```
   The frontend will run on http://localhost:3000

## API Documentation

See the [API Documentation](API_DOCUMENTATION.md) for details on available endpoints.

## Example Games

The system can generate various types of educational games, including:
- Multiple-choice quizzes
- Sequencing games
- Matching exercises
- Simple simulations
- Interactive diagrams
- Memory games

## Technologies Used

- Backend: Flask, Google Generative AI (Gemini), LangChain
- Frontend: React (to be implemented)
- Graphics: SVG with embedded JavaScript for interactivity

## Future Enhancements

- Add user authentication
- Save generated games
- Allow game customization
- Add additional game templates
- Implement analytics to track learning progress