from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from senti_analysis import process_dataset, preprocess_text, analyze_sentiment
import pandas as pd

def compare_sentiments(test_data, processed_data):
    """
    Compares sentiments excluding unknown labels and handles class imbalance
    """
    # Ensure textID is of the same type in both datasets
    test_data['textID'] = test_data['textID'].astype(str)
    processed_data['textID'] = processed_data['textID'].astype(str)

    # Merge datasets on 'textID'
    merged_data = pd.merge(
        test_data[['textID', 'sentiment']],
        processed_data[['textID', 'Sentiment_Class']],
        on='textID',
        how='inner'
    )

    # Standardize values for comparison
    merged_data['sentiment'] = merged_data['sentiment'].fillna("unknown").str.strip().str.lower()
    merged_data['Sentiment_Class'] = merged_data['Sentiment_Class'].fillna("unknown").str.strip().str.lower()

    # Filter out rows with unknown sentiment in ground truth
    known_sentiments = merged_data[merged_data['sentiment'] != 'unknown'].copy()
    
    if known_sentiments.empty:
        raise ValueError("No known sentiment labels found in the data")

    print("\nData distribution before filtering unknowns:")
    print("Total rows:", len(merged_data))
    print("Ground truth sentiment distribution:", merged_data['sentiment'].value_counts().to_dict())
    print("Predicted sentiment distribution:", merged_data['Sentiment_Class'].value_counts().to_dict())

    print("\nData distribution after filtering unknowns:")
    print("Total rows:", len(known_sentiments))
    print("Ground truth sentiment distribution:", known_sentiments['sentiment'].value_counts().to_dict())
    print("Predicted sentiment distribution:", known_sentiments['Sentiment_Class'].value_counts().to_dict())

    # Get ground truth and predictions
    y_true = known_sentiments['sentiment']
    y_pred = known_sentiments['Sentiment_Class']

    # Calculate metrics
    try:
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, average='weighted')
        recall = recall_score(y_true, y_pred, average='weighted')
        f1 = f1_score(y_true, y_pred, average='weighted')

        print("\nDetailed Classification Report (excluding unknown labels):")
        print(classification_report(y_true, y_pred))
        
        print("\nOverall Metrics (excluding unknown labels):")
        print(f"Accuracy: {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print(f"F1 Score: {f1:.4f}")

        # Print confusion matrix samples
        print("\nSample of misclassifications:")
        misclassified = known_sentiments[y_true != y_pred].head(10)
        print(misclassified[['textID', 'sentiment', 'Sentiment_Class']])

        return accuracy, precision, recall, f1

    except Exception as e:
        print(f"Error calculating metrics: {str(e)}")
        return 0, 0, 0, 0

def process_dataset(file_path):
    """
    Process dataset with improved sentiment handling
    """
    data = pd.read_csv(file_path)
    print(f"Loaded {len(data)} rows from {file_path}")
    
    # Ensure text column is string and handle NaN values
    data['text'] = data['text'].fillna('').astype(str)
    
    # Preprocess text
    print("Preprocessing text...")
    data['Cleaned_Text'] = data['text'].apply(lambda x: safe_preprocess_text(x))
    
    # Perform sentiment analysis
    print("Performing sentiment analysis...")
    sentiment_classes = []
    
    for comment in data['Cleaned_Text']:
        try:
            compound, sentiment = analyze_sentiment(comment)
            # Map empty or invalid sentiments to neutral
            sentiment = sentiment if sentiment in ['positive', 'negative', 'neutral'] else 'neutral'
            sentiment_classes.append(sentiment)
        except Exception as e:
            print(f"Error in sentiment analysis: {str(e)}")
            sentiment_classes.append('neutral')  # default fallback
    
    data['Sentiment_Class'] = sentiment_classes
    
    print("\nSentiment Distribution in processed data:")
    print(data['Sentiment_Class'].value_counts(normalize=True).multiply(100).round(2))
    
    return data[['textID', 'text', 'Sentiment_Class']]

def safe_preprocess_text(text):
    """
    Safely preprocess text with better error handling
    """
    try:
        if pd.isna(text) or text == '':
            return ''
        return preprocess_text(str(text))
    except Exception as e:
        print(f"Error preprocessing text: {str(e)}")
        return ''

def main():
    """
    Main workflow with improved error handling
    """
    try:
        test_file_path = "test.csv"
        processed_file_path = "processed_test_comments_by_model.csv"

        # Process and export the dataset
        print("Processing dataset...")
        processed_data = process_dataset(test_file_path)
        
        print("Exporting processed data...")
        processed_data.to_csv(processed_file_path, index=False, encoding='utf-8')
        
        # Load datasets for comparison
        print("Loading datasets for comparison...")
        test_data = pd.read_csv(test_file_path)
        processed_data = pd.read_csv(processed_file_path)
        
        # Compare sentiments
        print("Comparing sentiments...")
        compare_sentiments(test_data, processed_data)
        
    except Exception as e:
        print(f"Error in main workflow: {str(e)}")

if __name__ == "__main__":
    main()
