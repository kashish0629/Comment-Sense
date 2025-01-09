import google.generativeai as genai
import PIL.Image

def give_prediction_on_the_next_post():
    sample_file_2 = PIL.Image.open(f'static\\top_1.jpg')
    sample_file_3 = PIL.Image.open(f'static\\top_2.jpg')
    sample_file_1 = PIL.Image.open(f'static\\top_3.jpg')

    genai.configure(api_key="your google API key")

    #myfile = genai.upload_file(path="temp_image.jpeg")
    #print(f"{myfile=}")
    prompt="These are the top performaing posts of my instagram, give me a plan for the next five days on what should I post based on what people will like if they have been liking these three posts the best. Keep it short but informative" 

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([prompt, sample_file_2, sample_file_3, sample_file_1])
    return response.text
