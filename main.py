from flask import Flask, request, render_template
from pytube import YouTube
import openai  # Replace this with your API key setup

# Initialize Flask app
app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = "YOUR_API_KEY"

def summarize_transcript(transcript):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Summarize this YouTube transcript:\n{transcript}",
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error during summarization: {e}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/summarize", methods=["POST"])
def summarize():
    video_url = request.form.get("video_url")
    try:
        yt = YouTube(video_url)
        transcript = yt.captions.get_by_language_code('en').generate_srt_captions()  # Ensure captions exist
        summary = summarize_transcript(transcript)
        return render_template("index.html", summary=summary, url=video_url)
    except Exception as e:
        return render_template("index.html", error=f"Error: {e}", url=video_url)

if __name__ == "__main__":
    app.run(debug=True)
