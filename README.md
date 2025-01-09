# Instagram-Comment-Sentiment-Analysis

This repository contains a Flask web application that analyzes sentiment in Instagram post comments. It identifies the top and worst-performing posts, predicts trends for future posts, and visualizes sentiment scores alongside post thumbnails. 

---

## Features

### Core Functionalities
1. **User Authentication**: Secure login using your Instagram username and password.
2. **Comment Extraction**: Scrape comments from the latest Instagram posts.
3. **Sentiment Analysis**:
   - Processes comments using NLP techniques to determine sentiment scores (positive, neutral, negative).
   - Calculates aggregate sentiment scores for each post.
4. **Data Visualization**:
   - Graphical representation of sentiment scores with post thumbnails.
   - Highlight top and worst-performing posts based on sentiment scores.
5. **Future Content Prediction**:
   - Suggests a plan for future posts based on trends in user engagement with previous posts.

### Technical Highlights
- **Backend**:
  - Flask framework for routing and rendering HTML templates.
  - `instagrapi` for interacting with the Instagram API.
  - Sentiment analysis using NLTK and VADER.
  - Data visualization with Matplotlib.
- **Frontend**:
  - `login.html`: Accepts Instagram credentials.
  - `analysis.html`: Displays sentiment analysis results, graphs, and predictions.
- **Data Handling**:
  - Export comments and sentiment data to CSV.
  - Predict trends using generative AI (Google GenAI API).

---

## Prerequisites

### Environment Setup
- **Python**: Version 3.8 or higher
- **Libraries**: Install the dependencies listed in `requirements.txt`.

### API Keys
- **Google Generative AI**: Add your API key to use the prediction feature in `prompt.py`:
  ```python
  genai.configure(api_key="YOUR_GOOGLE_GENAI_API_KEY")
  ```

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/instagram-sentiment-analysis.git
   cd instagram-sentiment-analysis
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate # For Linux/Mac
   venv\Scripts\activate    # For Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Flask app**:
   ```bash
   python app.py
   ```
   The app will start at `http://127.0.0.1:5000/`.

2. **Login Page** (`login.html`):
   - Enter your Instagram username and password.
   - The app authenticates your account and retrieves recent posts.

3. **Analysis Page** (`analysis.html`):
   - View sentiment analysis results.
   - See top and worst-performing posts with their thumbnails.
   - Access a graphical representation of sentiment scores.
   - Get predictions for future posts.

---


## Dependencies

Install the required Python libraries:
```bash
pip install flask instagrapi pandas matplotlib nltk vaderSentiment seaborn emoji google-generativeai pillow
```

---

## How It Works

1. **Login**: Enter Instagram credentials.
2. **Comment Extraction**: Fetches comments from the 15 most recent posts.
3. **Sentiment Analysis**:
   - Processes and cleans the comments.
   - Calculates sentiment scores using NLP and VADER.
4. **Visualization**:
   - Creates a graph with post thumbnails and sentiment scores.
   - Displays top and worst-performing posts.
5. **Future Predictions**: Generates suggestions for the next 5 days' posts using generative AI.

---

## Outputs

- **CSV Exports**:
  - `comments_export.csv`: Raw comments data.
  - `processed_comments.csv`: Comments with sentiment scores.
- **Visuals**:
  - Graph with post thumbnails: `static/graph_with_thumbnails.png`.
  - Thumbnails of top-performing posts: `static/top_1.jpg`, `top_2.jpg`, `top_3.jpg`.


- **Libraries**: Flask, Instagrapi, NLTK, VADER, Matplotlib, Google GenAI API
- **Inspiration**: Leveraging NLP and AI to enhance social media analytics.
