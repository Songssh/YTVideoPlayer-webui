import gradio as gr
import youtube as yt

from modules import filemgr
from modules.config import Config

def play_audio(url):
    video = yt.Video(url)
    video.info['title'] = filemgr.preprocess_text(video.info['title'], exception=['(', ')', '-'])
    option = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': CACHE_PATH+video.info['title']+'.%(ext)s',
    }
    download_path = CACHE_PATH + video.info['title']+'.mp3'
    path = video.download(option)
    print(f'end : {download_path}')
    return f"Success: {download_path}", {"value": download_path, "__type__": "update"},


def play_video(url):
    video = yt.Video(url)
    video.info['title'] = filemgr.preprocess_text(video.info['title'], exception=['(', ')', '-'])
    option = {
        'format' : 'bestvideo+bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4'
        }],
        'outtmpl': CACHE_PATH+video.info['title']+'.%(ext)s',
        }
    download_path = CACHE_PATH + video.info['title']+'.mp4'
    path = video.download(option)
    return f"Success: {download_path}", {"value": download_path, "__type__": "update"}


def download_video(url, download_path, download_format, convert_format):
    video = yt.Video(url)
    try:
        ext = download_format.split('|')[-1]
    except:
        ext = 'auto'

    # Set download_path
    if download_path[-1] == '\\' or download_path[-1] == '/':
        if ext == 'auto':
            download_path += video.info['title']+'.%(ext)s'
        else:
            download_path += video.info['title']+'.'+ ext
    else:
        if ext == 'auto':
            download_path += '.%(ext)s'
        else:
            download_path += '.'+ ext


    # Set download format
    if convert_format == 'None':
        download_format = 'bestvideo+bestaudio/best'
        postprocess = []
        
    elif convert_format == 'mp4' or convert_format == 'webm':
        download_format = 'bestvideo+bestaudio/best'
        postprocess = [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': convert_format,
        }]
        
    else:
        download_format = 'bestaudio/best'
        postprocess = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': convert_format,
            'preferredquality': '192',
        }]

    # Download
    option = {
        'format' : download_format,
        'outtmpl': download_path,
        'postprocessors': postprocess,
        }
    
    path = video.download(option)
    return f"Success: {download_path}"


def search_video(url):
    video = yt.Video(url)
    video.info['title'] = filemgr.preprocess_text(video.info['title'], exception=['(', ')', '-'])
    
    thumbnail = video.info['thumbnail']
    info = video.info_str()
    formats = sorted(video.format_list())
    formats.append('auto')
    #print(formats)
    
    return ({"value": thumbnail, "__type__": "update"},
            {"value": info, "__type__": "update"},
            {"value": f"download\{video.info['title']}", "__type__": "update"},
            {"choices": formats, "value":'auto', "__type__": "update"})


def init(config):
    cache_path = config.config['cache_path']
    # clean cache
    if filemgr.is_exist(cache_path):
        filemgr.rmdir(cache_path)
    filemgr.mkdir(cache_path)


cfg = Config('data/config.yaml')
init(cfg)

CACHE_PATH = cfg.config['cache_path']
convert_format_list = ['None', 'mp4', 'webm', 'mp3', 'm4a', 'wav']

with gr.Blocks(title="YTDL-webui") as app:
    #gr.Markdown(value="des")
    with gr.Tabs():
        with gr.TabItem('Downloader'):
            with gr.Row():
                video_url = gr.Textbox(label="Input your url")
            with gr.Row():
                search_button = gr.Button("Search", variant="primary")

            with gr.Row():
                temp_video = gr.Video(scale=2)
                with gr.Column():
                    thumbnail = gr.Image(scale=2)
                    video_info = gr.Textbox(label="Video information", scale=1)

            with gr.Row():
                download_path = gr.Textbox(value="download", label="path to download", scale=2)
                video_format = gr.Dropdown(label='Select video format', choices=[])
                convert_format = gr.Dropdown(value='None', label='Convert format', choices=convert_format_list)
                with gr.Row():

                    play_video_button = gr.Button("play video", variant="primary")
                    play_audio_button = gr.Button("play audio", variant="primary")
                    download_button = gr.Button("Download", variant="primary")

            with gr.Row():
                download_result = gr.Textbox(label="result info", scale=2)
                temp_audio = gr.Audio(label="result audio")

            search_button.click(
                fn = search_video,
                inputs = [video_url],
                outputs = [thumbnail, video_info, download_path, video_format],
                api_name = "search",
                )
            download_button.click(
                fn = download_video,
                inputs = [video_url, download_path, video_format, convert_format],
                outputs = [download_result],
                api_name = "download",
                )
            play_video_button.click(
                fn = play_video,
                inputs = [video_url],
                outputs = [download_result, temp_video],
                api_name = "play video",
                )
            play_audio_button.click(
                fn = play_audio,
                inputs = [video_url],
                outputs = [download_result, temp_audio],
                api_name = "play audio",
                )


    app.queue().launch(
        server_name="0.0.0.0",
        share = False,
        inbrowser=not True,
        server_port=18282,
        #quiet=True,
    )
