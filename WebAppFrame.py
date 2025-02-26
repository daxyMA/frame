from flask import Flask, render_template, request, send_file
from PIL import Image
import io

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            img = Image.open(file).convert("RGBA")  # Ensuring transparency support
            frame = Image.open("static/frame.png").convert("RGBA")

            # Resize image using high-quality interpolation
            img = img.resize((945, 960), Image.LANCZOS)
            frame = frame.resize((945, 960), Image.LANCZOS)

            # Composite the images (preserving transparency)
            img = Image.alpha_composite(img, frame)

            # Save with high quality settings
            img_io = io.BytesIO()
            img.save(img_io, format="PNG", dpi=(300, 300), quality=100, optimize=True)
            img_io.seek(0)

            return send_file(img_io, mimetype="image/png", as_attachment=True, download_name="framed.png")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
