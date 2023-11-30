import discord
from collections import defaultdict

intents = discord.Intents.all()
client = discord.Client(intents=intents)

emoji_cache = {}  # Cache for storing the emoji list  # 이모지 리스트를 저장하기 위한 캐시
reaction_queue = []  # Task queue for handling reactions  # 반응 처리를 위한 작업 큐

@client.event
async def on_raw_reaction_add(payload):
    if payload.channel_id == CHANNEL_ID and payload.emoji != "🔁":
        emoji = payload.emoji
        message_id = payload.message_id

        # Check if the emoji is already cached  # 이모지가 이미 캐시되어 있는지 확인
        if payload.emoji.id not in emoji_cache:
            # Fetch the emoji list from the Discord API  # Discord API에서 이모지 리스트 가져오기
            emoji_list = await client.fetch_emoji_list(payload.channel_id)
            emoji_cache = {emoji.id: emoji for emoji in emoji_list}

        # Check if the emoji is a duplicate  # 이모지가 중복되는지 확인
        if emoji_cache[payload.emoji.id] in payload.message.reactions:
            return

        # Add the reaction to the task queue  # 반응을 작업 큐에 추가
        reaction_queue.append((message_id, emoji))

        # Process reactions in batches  # 일괄적으로 반응 처리
        if len(reaction_queue) >= 100:
            await process_reactions()

async def process_reactions():
    # Fetch messages and reactions in bulk  # 메시지와 반응 일괄적으로 가져오기
    messages = await client.bulk_fetch_messages(reaction_queue[:100])
    reactions = []

    for message_id, emoji in reaction_queue[:100]:
        message = messages.get(message_id)
        if message is not None:
            reactions.append((message.id, emoji))

    # Add reactions in bulk  # 일괄적으로 반응 추가
    await client.bulk_add_reactions(reactions)

    # Clear the reaction queue  # 반응 큐 비우기
    del reaction_queue[:100]

client.run('YOUR_BOT_TOKEN')
