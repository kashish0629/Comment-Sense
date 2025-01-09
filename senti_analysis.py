import pandas as pd
import csv
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from nltk.stem import WordNetLemmatizer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import emoji
import matplotlib.pyplot as plt
import seaborn as sns

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize tools
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
tokenizer = TweetTokenizer()
sia = SentimentIntensityAnalyzer()

# Function to clean text
def clean_text(text):
    """
    Cleans the input text:
    - Converts to lowercase
    - Removes special characters and numbers
    - Handles hashtags by keeping the word
    - Converts emojis to text descriptions
    """
    try:
        if not isinstance(text, str):
            text = str(text)  # Convert non-string inputs to strings

        text = text.lower()  # Convert to lowercase
        text = emoji.demojize(text, delimiters=(" ", " "))  # Convert emojis to text
        text = re.sub(r'_', ' ', text)  # Replace underscores in emoji descriptions with spaces
        text = re.sub(r'[^a-zA-Z\s#]', '', text)  # Remove all special characters except letters, spaces, and hashtags
        return text.strip()  # Remove leading and trailing spaces

    except Exception as e:
        # Log or handle the exception gracefully
        print(f"Error cleaning text: {text}. Error: {e}")
        return ""

# Function to handle negations
def handle_negations(text):
    """
    Handles negations like 'not good' to 'NOT_good'.
    """
    negations = ["not", "no", "never", "n't"]
    words = text.split()
    processed = []
    negate = False
    for word in words:
        if negate:
            processed.append(f"NOT {word}")
            negate = False
        elif word in negations:
            negate = True
        else:
            processed.append(word)
    return ' '.join(processed)

# Function to tokenize and lemmatize text
def process_tokens(text):
    """
    Tokenizes, removes stopwords, and lemmatizes the text.
    """
    tokens = tokenizer.tokenize(text)
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    return ' '.join(tokens)

# Function to preprocess the text
def preprocess_text(text):
    """
    Combines all preprocessing steps into one function.
    """
    text = clean_text(text)
    text = handle_negations(text)
    text = process_tokens(text)
    return text 

# Function to analyze sentiment
def analyze_sentiment(text):
    """
    Uses VADER to calculate sentiment scores.
    Adjust thresholds for better accuracy:
    - Positive: compound > 0.3
    - Neutral: -0.3 <= compound <= 0.3
    - Negative: compound < -0.3
    """
    scores = sia.polarity_scores(text)
    compound = scores['compound']
    if compound > 0.1:
        sentiment = 'positive'
    elif compound < -0.1:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'
    return compound, sentiment

# Function to preprocess the dataset
def process_dataset(file_path):
    """
    Loads the dataset, preprocesses comments, and calculates sentiment scores.
    """
    # Load the CSV file
    data = pd.read_csv(file_path)
    data.columns = ['media_id', 'comment']  # Ensure consistent column names

    # Preprocess comments
    data['Cleaned_Comment'] = data['comment'].apply(preprocess_text)

    # Analyze sentiment for each comment
    compound_scores = []
    sentiment_classes = []
    for comment in data['Cleaned_Comment']:
        compound, sentiment = analyze_sentiment(comment)
        compound_scores.append(compound)
        sentiment_classes.append(sentiment)

    data['Sentiment_Score'] = compound_scores
    data['Sentiment_Class'] = sentiment_classes

    return data

# Function to calculate aggregate sentiment scores
def aggregate_scores(data):
    """
    Groups comments by media_id and calculates a weighted average of sentiment scores.
    Longer comments have higher weights.
    """
    data['Weight'] = data['Cleaned_Comment'].str.split().apply(len)  # Comment length as weight
    aggregated_scores = []
    media_ids = []

    for media_id, group in data.groupby('media_id'):
        total_weighted_score = (group['Sentiment_Score'] * group['Weight']).sum()
        total_weight = group['Weight'].sum()
        aggregate_score = total_weighted_score / total_weight
        aggregated_scores.append(aggregate_score)
        media_ids.append(media_id)

    return pd.DataFrame({'media_id': media_ids, 'Aggregate_Score': aggregated_scores})

# Function to find the best-performing post
def find_best_post(aggregated_data):
    """
    Finds the post with the highest aggregate sentiment score.
    """
    best_index = aggregated_data['Aggregate_Score'].idxmax()
    return aggregated_data.loc[best_index]

# Function to visualize sentiment distribution
def visualize_sentiments(aggregated_data):
    """
    Plots the distribution of aggregate sentiment scores.
    """
    sns.histplot(aggregated_data['Aggregate_Score'], bins=20, kde=True)
    plt.title('Aggregate Sentiment Score Distribution')
    plt.xlabel('Aggregate Sentiment Score')
    plt.ylabel('Frequency')
    plt.show()

# Main function to run the analysis
def main(file_path):
    """
    Orchestrates the entire workflow:
    - Loads the dataset
    - Processes comments and calculates sentiment
    - Aggregates scores by post
    - Identifies the best-performing post
    - Visualizes sentiment distribution
    """
    # Process the dataset
    data = process_dataset(file_path)
    print(data)
    def exportProcToCSV(data):
        """
        Exports the processed dataset with sentiment analysis to a CSV file.
        """
        print("Exporting processed data to CSV...")
        csv_file_path = "processed_comments.csv"

        # Save the DataFrame directly to CSV
        data.to_csv(csv_file_path, index=False, encoding='utf-8')
        print(f"Data exported to {csv_file_path}")

        # Aggregate sentiment scores by post
    exportProcToCSV(data)
    #aggregated_data = aggregate_scores(data)

    # Identify the best post
    #best_post = find_best_post(aggregated_data)
   # print("Best Performing Post:")
   # print(best_post)

    # Visualize sentiment distribution
    #visualize_sentiments(aggregated_data)

# Run the program
if __name__ == "__main__":
    file_path = 'comments_export.csv'  # Ensure the CSV file has 'media_id' and 'comment' columns
    main(file_path)

