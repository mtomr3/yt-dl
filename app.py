import streamlit as st
import re
from api import get_audio, get_thumbnail_url, get_title
import time
import os


tmpdir = "./tmpmp3s/"
if not os.path.exists(tmpdir):
    os.mkdir(tmpdir)

def timed_success(body, icon=None, seconds=3):
	elem = st.empty()
	elem.success(body, icon=icon)
	time.sleep(seconds)
	elem.empty()
	return elem

st.set_page_config(page_title="YouTube MP3")
st.title("Simple YouTube MP3 Download")
link = st.text_input('Enter link')

if link:
	title = get_title(link)
	fname = f"{tmpdir}{title}.mp3"

	with st.expander(label=title, expanded=True):
		st.image(get_thumbnail_url(link), use_column_width=True)

		with st.spinner("Extracting audio..."):
			audio = get_audio(link, inmem=False, fldr=tmpdir)

			# with open(fname, "wb") as f:
			# 	f.write(audio.getvalue())

			with open(fname, "rb") as f:
				audio = f.read()

			st.audio(fname)

			if os.path.exists(fname):
				os.remove(fname)

			st.download_button(
			    label=f"Download {title}",
			    data=audio,
			    file_name=f"{title}.mp3",
			    mime="audio/mpeg"
			)

	timed_success("Ready for download", icon="✅", seconds=1.5)

else:
	st.write("No link yet")


