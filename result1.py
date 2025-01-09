from instagrapi import Client
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import requests
from io import BytesIO
import numpy 
from prompt import give_prediction_on_the_next_post

# Login to Instagram
def insta_login(username, password):
    print("Logging in...")
    cl = Client()
    cl.login(username, password)
    return cl

# Fetch thumbnail URL for a media ID
def fetch_thumbnail_url(cl, media_id):
    """
    Fetches the thumbnail URL for a given media ID.
    """
    try:
        media_info = cl.media_info(media_id)
        return media_info.thumbnail_url
    except Exception as e:
        print(f"Error fetching thumbnail for media_id {media_id}: {e}")
        return None

# Aggregate sentiment scores
def aggregate_scores(data):
    """
    Groups comments by media_id and calculates a weighted average of sentiment scores.
    Handles missing or invalid values in Cleaned_Comment.
    """
    data['Cleaned_Comment'] = data['Cleaned_Comment'].fillna("").astype(str)
    data['Weight'] = data['Cleaned_Comment'].str.split().apply(len)

    aggregated_scores = []
    media_ids = []

    for media_id, group in data.groupby('media_id'):
        total_weighted_score = (group['Sentiment_Score'] * group['Weight']).sum()
        total_weight = group['Weight'].sum()
        if total_weight > 0:
            aggregate_score = total_weighted_score / total_weight
        else:
            aggregate_score = 0
        aggregated_scores.append(aggregate_score)
        media_ids.append(media_id)

    return pd.DataFrame({'media_id': media_ids, 'Aggregate_Score': aggregated_scores})

# Find top 3 and worst 3 posts
def find_top_and_worst_posts(aggregated_data):
    """
    Finds the top 3 and worst 3 posts based on aggregate sentiment scores.
    """
    sorted_data = aggregated_data.sort_values(by='Aggregate_Score', ascending=False)
    top_3 = sorted_data.head(3)
    worst_3 = sorted_data.tail(3)
    return top_3, worst_3

# Plot graph with thumbnails
def plot_graph_with_thumbnails(aggregated_data, cl):
    """
    Plots Post IDs vs Aggregate Sentiment Scores with thumbnails displayed at graph points.
    """
    fig, ax = plt.subplots(figsize=(12, 8))

    # Plot the sentiment scores
    ax.scatter(aggregated_data['media_id'], aggregated_data['Aggregate_Score'], color='blue', s=100)
    ax.set_title('Post Sentiment Analysis', fontsize=16)
    ax.set_xlabel('Media ID', fontsize=12)
    ax.set_ylabel('Aggregate Sentiment Score', fontsize=12)

    # Add thumbnails to graph points
    for i, row in aggregated_data.iterrows():
        media_id = row['media_id']
        score = row['Aggregate_Score']
        thumbnail_url = fetch_thumbnail_url(cl, media_id)
        if thumbnail_url:
            try:
                response = requests.get(thumbnail_url, stream=True)
                print("hellloooooooo")
                img = plt.imread(BytesIO(response.content), format='jpeg')
                imagebox = OffsetImage(img, zoom=0.05)
                ab = AnnotationBbox(imagebox, (i, score), frameon=False)
                ax.add_artist(ab)
            except Exception as e:
                print(f"Error displaying thumbnail for media_id {media_id}: {e}")
    

    plt.xticks(rotation=90)
    plt.tight_layout()
    print("Saving graph with thumbnails...")
    plt.savefig("static\\graph_with_thumbnails.png")
    plt.close(fig)

def save_images_to_local_via_media_id(cl, media_ids):
    i=3
    for media_id in media_ids:
        thumbnail_url = fetch_thumbnail_url(cl, media_id)
        if thumbnail_url:
            try:
                response = requests.get(thumbnail_url, stream=True)
                img = plt.imread(BytesIO(response.content), format='jpeg')
                plt.imsave(f"static\\top_{i}.jpg", img)
                i=i-1
            except Exception as e:
                print(f"Error saving thumbnail for media_id {media_id}: {e}")

# Main function
def main():
    

    # Load processed sentiment data
    data = pd.read_csv('processed_comments.csv')

    # Aggregate sentiment scores
    aggregated_data = aggregate_scores(data)

    # Find the top 3 and worst 3 posts
    top_3, worst_3 = find_top_and_worst_posts(aggregated_data)
    
    print("Saving top 3 thumbnails to local...")
    media_ids = []
    for media_data in top_3.to_numpy():
        media_ids.append(media_data[0])
        
    print(media_ids)
    save_images_to_local_via_media_id(cl, media_ids)

    print("\nTop 3 Posts:")
    print(top_3)
    print("\nWorst 3 Posts:")
    print(worst_3)

    # Plot Post IDs vs Sentiment Scores with thumbnails
    plot_graph_with_thumbnails(aggregated_data, cl)
    
    

# Run the program
if __name__ == "__main__":
    main()
