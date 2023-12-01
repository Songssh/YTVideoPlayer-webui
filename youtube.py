import youtube_dl

class Video:
    def __init__(self, url):
        self.url = url
        self.info = self.init_info(url)

    def init_info(self, url):
        ydl_opts = {'skip_download': True, 'quiet': True}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        return info

    def format_list(self):
        return [x['format']+'|'+x['ext'] for x in self.info['formats']]

    def info_str(self, thumb = False, f = False):
        text = f"title : {self.info['title']}\n" +\
               f"description : {self.info['description']}\n" +\
               f"duration : {self.info['duration']}\n" +\
               f"uploader : {self.info['uploader']}\n"
        if thumb:
            text += f"thumbnail : {self.info['thumbnail']}\n"
        if f:
            text += f"formats : {self.format_list()}\n"
        return text

    def download(self, opt):
        video = youtube_dl.YoutubeDL(opt)
        video.download([self.url])
        return opt['outtmpl']


def get_info(url):
    ydl_opts = {'skip_download': True, 'quiet': True}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
    
    return info


def download(url:str, opt:dict):
    """
example:
url = 'https://www.youtube.com/watch?v=A_g7fPjVxvg'

opt = {
    'format': 'bestvideo+bestaudio/best',
    'outtmpl': '%(title)s.%(ext)s',
}
"""
    try:
        video = youtube_dl.YoutubeDL(opt)
        video.download([url])
        return 0
    except exception as e:
        return e

def test():
    url = 'https://www.youtube.com/watch?v=A_g7fPjVxvg'
    v = Video(url)
    data = get_info(url)
    
    print(data['formats'])

if __name__ == "__main__":
    test()
