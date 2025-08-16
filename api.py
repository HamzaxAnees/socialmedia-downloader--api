from flask import Flask, request, jsonify, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route("/download", methods=["GET"])
def download_video():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "❌ Please provide a video URL"}), 400

    try:
        # Make sure downloads folder exists
        if not os.path.exists("downloads"):
            os.makedirs("downloads")

        # Download options
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        # Return file metadata + direct download URL
        return jsonify({
            "title": info.get("title"),
            "uploader": info.get("uploader"),
            "duration": info.get("duration"),
            "ext": info.get("ext"),
            "download_url": f"/file/{os.path.basename(filename)}"
        })

    except Exception as e:
        return jsonify({"error": f"❌ Failed: {str(e)}"}), 500

@app.route("/file/<filename>", methods=["GET"])
def serve_file(filename):
    try:
        return send_file(f"downloads/{filename}", as_attachment=True)
    except Exception as e:
        return jsonify({"error": f"File not found: {str(e)}"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
