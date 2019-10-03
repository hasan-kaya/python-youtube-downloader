import youtube_dl

def get_download_links(video_id):

    with youtube_dl.YoutubeDL({}) as ydl:
        result = ydl.extract_info(
            'https://www.youtube.com/watch?v='+video_id,
            download=False
        )

    if 'entries' in result:
        videos = result['entries'][0]
    else:
        videos = result

    r_videos = []

    for video in videos['formats']:
        r_videos.append([{'url': video['url'], 'format': video['format'], 'size': video['filesize']}])

    return r_videos
    