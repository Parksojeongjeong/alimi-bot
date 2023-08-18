import discord
import asyncio
from discord.ext import commands, tasks
from datetime import datetime, time, timedelta
from security import security

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print("봇이 온라인으로 전환되었습니다.")
    create_thread.start()  # 봇이 준비되었을 때 작업 시작

@tasks.loop(hours=24)  # 매일 24시간마다 작업 실행
async def create_thread():
    now = datetime.now()
    target_time = time(13, 19, 0)  # 오전 9시

    # 매일 오전 9시에 스레드 생성
    if now.time() >= target_time:
        next_target = datetime.combine(now.date() + timedelta(days=1), target_time)
    else:
        next_target = datetime.combine(now.date(), target_time)

    time_until_next = (next_target - now).total_seconds()
    await asyncio.sleep(time_until_next)  # 다음 실행 시간까지 대기

    channel = bot.get_channel(security.channel_id)
    if channel:
        thread_name = now.strftime('%m/%d') + " To-Do List"
        thread = await channel.create_thread(
            name=thread_name,
            auto_archive_duration=1440  # 24시간
        )

        thread_link = thread.jump_url  # 생성된 쓰레드의 링크

        await channel.send(f"Good Morning!  {thread_link}")
        await thread.send(f"기분 좋은 {now.strftime('%m')}월 {now.strftime('%d')}일 입니다. \n오늘 할 일을 입력해주세요 :)")

bot.run(security.token)