from typing import Dict, Any
import yt_dlp
import re
import ffmpeg
import io



class YoutubeDownloader:
	def __init__(self, fldr=None):
		self.vid_fldr = fldr or "./YT/video/"
		self.audio_fldr = fldr or "./YT/audio/"

	def get_video(self, url):
		return self.get(url=url, opts=self.video_opts)

	def get_audio(self, url, inmem=False):
		if inmem:
			return self.get_audio_in_memory(url=url)
		print(self.audio_opts)
		return self.get(url=url, opts=self.audio_opts)

	def get(self, url: str, opts: Dict[str, Any]):
		with yt_dlp.YoutubeDL(opts) as ydl:
			ydl.download([url])

	@property
	def video_opts(self):
		return {
			**self.default_opts,
			"outtmpl": self.vid_fldr + "%(title)s.%(ext)s",
			"format": "best[ext=mp4]",
		}

	@property
	def audio_opts(self):
		return {
			**self.default_opts,
			"outtmpl": self.audio_fldr + "%(title)s.%(ext)s",
		    'postprocessors': [{
		        'key': 'FFmpegExtractAudio',
		        'preferredcodec': 'mp3',
		        'preferredquality': '192',
		    }],
		}

	@property
	def audio_mem_opts(self):
		return {
			**self.audio_opts,
			'format': 'bestaudio/best',
			'outtmpl': '-',
			'quiet': True
		}

	@property
	def default_opts(self):
		class MyLogger(object):
			def debug(self, msg):
				print("    debug:", msg)

			def warning(self, msg):
				print("  warn   :", msg)

			def error(self, msg):
				print("err      :", msg)

		def my_hook(d):
			if d['status'] == 'finished':
				print('Done downloading, now converting ...')

		return {
			# "outtmpl": "%(uploader)s%(title)s.%(ext)s",
			# "outtmpl": "%(title)s.%(ext)s",
			# "outtmpl": "./YT/%(title)s.%(ext)s",
			"logger": MyLogger(),
			"progress_hooks": [my_hook],
			"ffmpeg_location": "/usr/local/bin/ffmpeg",
		}


	def get_audio_in_memory(self, url):
		opts = self.audio_mem_opts
		with yt_dlp.YoutubeDL(opts) as ydl:
			result = ydl.extract_info(url, download=False)
			url = result['url']
			process = (
				ffmpeg
				.input(url)
				.output('pipe:1', format='mp3', audio_bitrate='192k')
				.run_async(pipe_stdout=True, pipe_stderr=True)
			)
			mp3_data = io.BytesIO(process.stdout.read())
			return mp3_data


class YoutubeMetadataProvider:
	@staticmethod
	def _type_cast_id(s):
		if "youtube.com" in s:
			s = YoutubeMetadataProvider.get_id(s)
		return s

	@staticmethod
	def get_id(url):
	    regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
	    match = re.search(regex, url)
	    return match.group(1) if match else None

	@staticmethod
	def get_thumbnail_url(id):
		data = YoutubeMetadataProvider.get_data(id)
		return data["thumbnail_url"]

	@staticmethod
	def get_data(id):
		id = YoutubeMetadataProvider._type_cast_id(id)
		# import urllib.request
		import json
		import urllib

		params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % id}
		url = "https://www.youtube.com/oembed"
		query_string = urllib.parse.urlencode(params)
		url = url + "?" + query_string

		with urllib.request.urlopen(url) as response:
		    response_text = response.read()
		    data = json.loads(response_text.decode())
		    return data

	@staticmethod
	def get_title(id):
		data = YoutubeMetadataProvider.get_data(id)
		return data["title"]
