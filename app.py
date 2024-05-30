import openai
from flask import Flask, render_template, request
from dotenv import dotenv_values
import json

config = dotenv_values(".env")
openai.api_key = config["OPENAI_API_KEY"]

app = Flask(__name__,
            template_folder='templates',
            static_folder='static',
            static_url_path='')


def get_colors(input_text):
    system_prompt = f"""
    You are a color palette generating assistant that responds to text prompts for color palettes
    You should generate color palettes that fit the theme, mood or instructions in the prompt. The palettes should be between 2 and 8 colors.
    Desired Format: a JSON array of hexadecimal color codes. Don't include json formatting. Include # in front of the hex codes.
    """
    user_prompt1 = "Ocean tones"
    assistant_answer = ["#0077be", "#4f819d", "#a8c4d0", "#61a0a8", "#2b6d84"]
    
    user_prompt2 = {input_text}
    
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
              "role": "system",
              "content": system_prompt
            },
            {
              "role": "user",
              "content": user_prompt1
            },
            {
              "role": "assistant",
              "content": assistant_answer
            },
            {
              "role": "user",
              "content": user_prompt2
            }
        ]
    )
    colors = json.loads(response.choices[0].message.content)
    # app.logger.info(colors)
    return colors

@app.route("/palette", methods=["POST"])
def prompt_to_palette():
    
    query = request.form.get("query")
    colors = get_colors(query)
    return {"colors": colors}

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)