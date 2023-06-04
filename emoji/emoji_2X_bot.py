# 이모티콘 입력시 크기를 키워주는 코드

from PIL import Image
from io import BytesIO


async def on_message(message):
    if message.author.bot:
        return
    
    # 이모티콘을 포함한 메시지를 받으면 실행
    if message.content and message.content.startswith("<:") and message.content.endswith(">"):
        # 이모티콘 이름과 URL 가져오기
        emoji_name = message.content.split(":")[1]
        emoji_url = message.content.split(":")[2][:-1]
        
        # URL로부터 이미지 객체 생성
        response = requests.get(emoji_url)
        img = Image.open(BytesIO(response.content))
        
        # 이미지 크기를 2배로 변경한 결과를 전송
        img_resized = img.resize((img.width*2, img.height*2))
        f = BytesIO()
        img_resized.save(f, format='JPEG')
        f.seek(0)
        await message.channel.send(file=discord.File(f, 'big_emoji.jpeg'))
