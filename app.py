import streamlit as st
import subprocess, os, uuid, re, tempfile

st.title("Universal Downloader")

url = st.text_input("Enter video URL:")
mode = st.selectbox("Download format", ["Video (MP4)", "Audio (MP3)"])

def run_cmd(cmd):
    try:
        return subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    except FileNotFoundError:
        return subprocess.CompletedProcess(cmd, 1, "", "Command not found: yt-dlp or ffmpeg missing")
    except Exception as e:
        return subprocess.CompletedProcess(cmd, 1, "", str(e))

def clean_name(text):
    return re.sub(r"[^a-zA-Z0-9._-]", "_", text)

if st.button("Download") and url:
    tmp = tempfile.gettempdir()
    base = clean_name(str(uuid.uuid4()))

    # output file paths
    out_mp4 = os.path.join(tmp, base + ".mp4")
    out_mp3 = os.path.join(tmp, base + ".mp3")

    # main command (same as your working one)
    base_cmd = [
        "yt-dlp",
        "--remote-components", "ejs:github",
        "-o", out_mp4 if mode == "Video (MP4)" else out_mp3,
        url
    ]

    # apply options based on mode
    if mode == "Video (MP4)":
        base_cmd += ["-f", "bestvideo+bestaudio", "--merge-output-format", "mp4"]
    else:
        base_cmd += ["-x", "--audio-format", "mp3"]

    st.write("Starting download… please wait.")
    prog = st.progress(0)

    try:
        # run main command
        prog.progress(30)
        r = run_cmd(base_cmd)
        prog.progress(70)

        # fallback if needed (YouTube blocking formats)
        if r.returncode != 0:
            st.warning("Falling back to best available format…")
            fallback = [
                "yt-dlp",
                "--remote-components", "ejs:github",
                "-f", "best",
                "-o", out_mp4 if mode == "Video (MP4)" else out_mp3,
                url
            ]
            r = run_cmd(fallback)

        prog.progress(100)

        if r.returncode != 0:
            st.error(r.stderr)
        else:
            # choose correct file to serve
            final_file = out_mp4 if mode == "Video (MP4)" else out_mp3
            with open(final_file, "rb") as f:
                st.download_button(
                    "Download " + ("MP4" if mode == "Video (MP4)" else "MP3"),
                    f,
                    file_name=os.path.basename(final_file)
                )
            os.remove(final_file)

    except Exception as e:
        st.error(str(e))

