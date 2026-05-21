import streamlit as st
import subprocess, os, uuid, re, tempfile

st.title("Universal Downloader")

url = st.text_input("Enter URL:")
mode = st.selectbox("Format", ["Video (MP4)", "Audio (MP3)"])

cookie_file = st.file_uploader(
    "Optional cookies.txt (for Reddit/private videos)",
    type=["txt"]
)

def run(cmd):
    return subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

def clean(t):
    return re.sub(r"[^a-zA-Z0-9._-]", "_", t)

if st.button("Download") and url:

    tmp = tempfile.gettempdir()
    uid = clean(str(uuid.uuid4()))

    ext = "mp4" if mode == "Video (MP4)" else "mp3"

    out = os.path.join(tmp, uid + ".%(ext)s")
    final_file = os.path.join(tmp, uid + "." + ext)

    cmd = [
        "yt-dlp",
        "--js-runtimes", "node",
        "--remote-components", "ejs:github",
        "--force-ipv4",
        "--extractor-retries", "3",
        "--no-playlist",
        "-o", out,
    ]

    # optional cookies
    cookie_path = None

    if cookie_file:
        cookie_path = os.path.join(tmp, uid + "_cookies.txt")

        with open(cookie_path, "wb") as f:
            f.write(cookie_file.read())

        cmd += ["--cookies", cookie_path]

    # format handling
    if mode == "Video (MP4)":
        cmd += [
            "-f", "bv*+ba/b",
            "--merge-output-format", "mp4",
            "--remux-video", "mp4"
        ]
    else:
        cmd += [
            "-x",
            "--audio-format", "mp3"
        ]

    cmd.append(url)

    with st.spinner("Downloading..."):
        r = run(cmd)

    if r.returncode != 0:
        st.error(r.stderr)

    elif os.path.exists(final_file):

        with open(final_file, "rb") as f:
            st.download_button(
                "Download File",
                f,
                file_name=os.path.basename(final_file)
            )

        os.remove(final_file)

    else:
        st.error("Download completed but file not found.")

    if cookie_path and os.path.exists(cookie_path):
        os.remove(cookie_path)

