import pytube

link = input("Input Youtube Video URL.")
video_download = pytube.Youtube(link)
video_download.streams.first().download()
print(f"Video Downloaded.{link}")
