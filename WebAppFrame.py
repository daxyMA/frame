from flask import Flask, render_template, request, send_file
from PIL import Image
import io

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            img = Image.open(file)
            frame = Image.open("static/frame.png").convert("RGBA")

            img = img.resize((945, 960))
            img.paste(frame, (0, 0), frame)

            img_io = io.BytesIO()
            img.save(img_io, "PNG")
            img_io.seek(0)
            return send_file(img_io, mimetype="image/png", as_attachment=True, download_name="framed.png")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)