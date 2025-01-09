from flask import render_template, Flask, request, redirect, url_for
from instagrapi import Client
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import requests
from io import BytesIO
from extract import insta_login, getUserId, returnUserMedia, returnUserCommentsText, exportToCSV
from senti_analysis import process_dataset
from result1 import aggregate_scores, find_top_and_worst_posts, plot_graph_with_thumbnails, save_images_to_local_via_media_id
from prompt import give_prediction_on_the_next_post


app = Flask(__name__)

@app.route('/')
def login():    
    return render_template('login.html')

@app.route('/analyze' , methods=['POST'])
def analyze():
    username = request.form.get('username')
    password = request.form.get('password')
    cl = insta_login(username, password)
    user_id = getUserId(cl,username)
    media_ids = returnUserMedia(user_id,15,cl)
    comments_data = returnUserCommentsText(cl,media_ids)
    exportToCSV(comments_data)
    print("Comments exported to comments_export.csv")
    
    #sentiment analysis
    file_path = 'comments_export.csv'
    data = process_dataset(file_path)
    print(data)
    print("Exporting processed data to CSV...")
    csv_file_path = "processed_comments.csv"

    # Save the DataFrame directly to CSV
    data.to_csv(csv_file_path, index=False, encoding='utf-8')
    print(f"Data exported to {csv_file_path}")
    
    #result
    data = pd.read_csv('processed_comments.csv')

   
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
    plot_graph_with_thumbnails(aggregated_data, cl)
    prediction_for_next_post = give_prediction_on_the_next_post()

    # Plot Post IDs vs Sentiment Scores with thumbnails
    # plot_graph_with_thumbnails(aggregated_data, cl)
    
    return render_template('analysis.html', username=username, prediction_post_text = prediction_for_next_post)

if __name__ == '__main__':
    app.run(debug=True)
