from flask import Flask , render_template,request, jsonify
from pytube import YouTube, Playlist
from requests.utils import requote_uri
import concurrent.futures
import threading
import re
import pytube
app = Flask(__name__)






rsra = {}
urls = []

@app.route('/', methods=['GET','POST'])
def me():
    if request.method == 'POST':
        try:
            url=request.form.get('url')
            yt=YouTube(url)
            streamss=yt.streams
            return render_template('index.html', thumbnail=thumbnail(yt), s1080=s1080(streamss) ,s720=s720(streamss), 
            s480=s480(streamss), s360=s360(streamss),s240=s240(streamss), s144=s144(streamss))
        except pytube.exceptions.RegexMatchError:
            return render_template('index.html', msg="invalid")
        except Exception as e:
            return render_template('index.html', msg=e)              
    return render_template('index.html')    
#mp4
def s1080(streamss):
    ls=streamss
    ys=ls.filter(mime_type="video/mp4", progressive="True", res="1080p").first()
    if not ys:
        return False
    else:
        la=ys.url.split("videoplayback?")
        join1="videoplayback?api=google.com&".join(la)
        return requote_uri(join1+"&title="+ys.title)

def s720(streamss):
    ls=streamss
    ys=ls.filter(mime_type="video/mp4",progressive="True", res="720p").first()
    if not ys:
        return False
    else:
        la=ys.url.split("videoplayback?")
        join1="videoplayback?api=google.com&".join(la)
        return requote_uri(join1+"&title="+ys.title)

def s480(streamss):
    ys=streamss.filter(mime_type="video/mp4",progressive="True", res="480p").first()
    if not ys:
        return False
    else:
        la=ys.url.split("videoplayback?")
        join1="videoplayback?api=google.com&".join(la)
        return requote_uri(join1+"&title="+ys.title)

def s360(streamss):
    ys=streamss.filter(mime_type="video/mp4",progressive="True", res="360p").first()
    if not ys:
        return False
    else:
        la=ys.url.split("videoplayback?")
        join1="videoplayback?api=google.com&".join(la)
        return requote_uri(join1+"&title="+ys.title)

def s240(streamss):
    ys=streamss.filter(mime_type="video/mp4",progressive="True", res="240p").first()
    if not ys:
        return False
    else:
        la=ys.url.split("videoplayback?")
        join1="videoplayback?api=google.com&".join(la)
        return requote_uri(join1+"&title="+ys.title)

def s144(streamss):
    ys=streamss.filter(mime_type="video/mp4",progressive="True", res="144p").first()
    if not ys:
        return False
    else:
        la=ys.url.split("videoplayback?")
        join1="videoplayback?api=google.com&".join(la)
        return requote_uri(join1+"&title="+ys.title)

def thumbnail(yt):
    return yt.thumbnail_url

@app.route('/playlist', methods=['GET','POST'])
def dk():
    rsra = {}
    if request.method == 'POST':
        try:
            url=request.form.get('url')
            yt=Playlist(url)
            yt._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
            urls=(yt.video_urls)
            for i in range(0, len(urls)):
                yop=YouTube(urls[i])
                streamss=yop.streams
                ys=streamss.filter(mime_type="video/mp4", progressive="True", res="720p").first()
                if not ys:
                    ys=streamss.filter(mime_type="video/mp4", progressive="True", res="360p").first()
                    la=ys.url.split("videoplayback?")
                    join1="videoplayback?api=google.com&".join(la)
                    rsra.update({i+1: { 'url': requote_uri(join1+"&title="+ys.title) , 'title': ys.title, 'res': ys.resolution }})
                else:
                    la=ys.url.split("videoplayback?")
                    join1="videoplayback?api=google.com&".join(la)
                    rsra.update({i+1: { 'url': requote_uri(join1+"&title="+ys.title) , 'title': ys.title , 'res': ys.resolution }})    

            return render_template('playlist.html', rsra=rsra)    
        except pytube.exceptions.RegexMatchError:
            return render_template('playlist.html', msg="invalid")
        except KeyError:
            return render_template('playlist.html', msg="list")    
        # except Exception as e:
        #     return render_template('playlist.html', msg=e)
    return render_template('playlist.html', rsra=rsra)                   
    




@app.errorhandler(404)
def errr(e):
    return render_template ('404.html'), 404

@app.errorhandler(405)
def errr(e):
    return render_template ('405.html'), 405










if __name__ == "__main__" :
    app.run(debug=True)


