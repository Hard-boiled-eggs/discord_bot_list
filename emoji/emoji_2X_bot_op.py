#PIL 모듈에서 이미지를 리사이즈하는 resize 메서드를 사용하는 대신, 썸네일을 생성하는 thumbnail 메서드를 사용하여 더 빠르고 성능 좋은 코드로 개선

import asyncio
import discord
import numpy as np
import aiohttp


async def on_message(message):
    if message.author.bot:
        return
    
    if message.content and message.content.startswith("<:") and message.content.endswith(">"):
        emoji_name = message.content.split(":")[1]
        emoji_url = message.content.split(":")[2][:-1]
        
        async with aiohttp.ClientSession() as session:
            async with session.get(emoji_url) as response:
                content = await response.read()
                f = BytesIO(content)
        
        # 이미지 객체 생성
        img = Image.open(f)
        
        # 이미지 크기를 변경하고 전송
        img.thumbnail((img.size[0]*2, img.size[1]*2), Image.ANTIALIAS)
        arr = np.array(img)
        arr_resized = arr.repeat(2, axis=0).repeat(2, axis=1)
        img_resized = Image.fromarray(arr_resized)
        
        with BytesIO() as f:
            img_resized.save(f, 'jpeg')
            f.seek(0)
            await message.channel.send(file=discord.File(f, 'big_emoji.jpeg'))
