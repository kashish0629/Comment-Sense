from instagrapi import Client
import csv



def insta_login(username, password):
    print("Logging you in...")
    cl = Client()
    cl.login(username, password)
    return cl

def getUserId(cl,username):
    print("Getting user id...")
    user_id = cl.user_id_from_username("username")
    return user_id

def returnUserMedia(user_id,n,cl):
    print("Getting user media...")
    medias = cl.user_medias(user_id, n)
    media_ids = [media.id for media in medias]
    return media_ids

def returnUserCommentsText(cl,media_ids):
    print("Getting user comments...")
    comments_data = []
    for media_id in media_ids:
        comments = []
        for(comment) in cl.media_comments(media_id):
            comments.append(comment.text)
            
        comments_data.append({
            "media_ID": media_id,
            "comments": comments
        })
    return comments_data

def exportToCSV(comments_data):
    print("Exporting to CSV...")
    csv_data = []
    print(comments_data)
    for item in comments_data:
        media_id = item['media_ID'] 
        comments = item['comments']
        for comment in comments:
            csv_data.append({'media_id': media_id, 'comment': comment})
    csv_file_path = "comments_export.csv"
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['media_id', 'comment'])
        writer.writeheader()
        writer.writerows(csv_data)
        
    
if __name__ == "__main__":
   
    #exportToCSV(comments_data)
    print("Comments exported to comments_export.csv")
