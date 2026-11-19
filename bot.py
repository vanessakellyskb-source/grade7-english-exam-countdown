import io, os, time, logging
from datetime import datetime, timezone, timedelta
from PIL import Image, ImageDraw, ImageFont
import requests

TOKEN=os.environ['TELEGRAM_BOT_TOKEN']
CHAT_ID=os.environ['TELEGRAM_CHAT_ID']
API=f'https://api.telegram.org/bot{TOKEN}/'
TARGET=datetime(2026,11,26,tzinfo=timezone(timedelta(hours=4)))
INTERVAL=max(60,int(os.getenv('UPDATE_SECONDS','60')))
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
logging.basicConfig(level=logging.INFO)

def call(method, **kwargs):
    r=requests.post(API+method,timeout=35,**kwargs)
    r.raise_for_status()
    data=r.json()
    if not data.get('ok'): raise RuntimeError(data)
    return data['result']

def render():
    remaining=max(0,int((TARGET-datetime.now(timezone.utc)).total_seconds()))
    d,h,m,s=remaining//86400,(remaining%86400)//3600,(remaining%3600)//60,remaining%60
    im=Image.new('RGB',(1200,675)); draw=ImageDraw.Draw(im)
    for y in range(675):
        p=y/674
        draw.line((0,y,1200,y),fill=(int(38-19*p),int(41-15*p),int(121-53*p)))
    def font(sz):return ImageFont.truetype(FONT,sz)
    def center(text,y,f,fill):
        bb=draw.textbbox((0,0),text,font=f);draw.text(((1200-(bb[2]-bb[0]))/2,y),text,font=f,fill=fill)
    for x,y,r,c in [(100,90,7,'#ffe783'),(1080,100,9,'#7ee9ff'),(185,530,8,'#ffb6e4'),(1030,540,7,'#ffe783'),(920,65,5,'#ffffff'),(290,90,5,'#ffffff')]:
        draw.ellipse((x-r,y-r,x+r,y+r),fill=c)
    center('GRADE 7',54,font(45),'#9ceaff')
    center('END OF TERM ENGLISH EXAM',128,font(53),'#ffffff')
    center('26 NOVEMBER 2026  |  UAE TIME',220,font(29),'#ffe47e')
    values=[d,h,m,s]; labels=['DAYS','HOURS','MINUTES','SECONDS'];colors=['#ffe47e','#8ff3ff','#ffb4df','#b9ffb0']
    for i,(v,label,color) in enumerate(zip(values,labels,colors)):
        x=90+i*260
        draw.rounded_rectangle((x,320,x+240,495),radius=24,fill='#35447e',outline='#798ac7',width=3)
        value=f'{v:02d}'
        bb=draw.textbbox((0,0),value,font=font(85))
        draw.text((x+(240-(bb[2]-bb[0]))/2,334),value,font=font(85),fill=color)
        bb=draw.textbbox((0,0),label,font=font(23))
        draw.text((x+(240-(bb[2]-bb[0]))/2,455),label,font=font(23),fill='#ffffff')
    center('EXAM DAY IS HERE! YOU CAN DO IT!' if remaining==0 else 'STUDY  *  PRACTISE  *  BELIEVE  *  ACHIEVE',550,font(30),'#ffe47e')
    center('Countdown refreshes automatically every minute',608,font(18),'#d1d9ff')
    out=io.BytesIO();im.save(out,format='PNG');out.seek(0)
    return out,remaining

def main():
    message_id=None
    while True:
        try:
            photo,remaining=render()
            if message_id is None:
                result=call('sendPhoto',data={'chat_id':CHAT_ID,'caption':'Grade 7 End of Term English Exam countdown'},files={'photo':('countdown.png',photo,'image/png')})
                message_id=result['message_id']
                logging.info('Message sent: %s. Pin it in Telegram.',message_id)
            else:
                call('editMessageMedia',data={'chat_id':CHAT_ID,'message_id':message_id,'media':'{"type":"photo","media":"attach://photo"}'},files={'photo':('countdown.png',photo,'image/png')})
                logging.info('Countdown refreshed')
            if remaining==0:break
        except Exception:
            logging.exception('Telegram update failed; retrying')
        time.sleep(INTERVAL)

if __name__=='__main__':main()
