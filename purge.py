async def purge(message, str):
    numMessages = int(str)
    if numMessages < 2 or numMessages > 100:
        return await message.reply('Please provide a number between 2 and 100 for the number of messages to delete.')
    
    deletedMessages = await message.channel.purge(limit=numMessages)
    await message.channel.send(f'Deleted {len(deletedMessages)} messages.')