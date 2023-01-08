from setuptools import setup
import re
import os

version = ""
with open("disnake/ext/dashboard/__init__.py") as f:
	version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
	raise RuntimeError("version is not set")
		

readme = '''
## Установка
```py
pip install --upgrade disnake-ext-dashboard

python3 -m pip install --upgrade disnake-ext-dashboard
```

## Применение
### Предпосылки
Прежде чем приступить к работе, вам понадобится несколько вещей:
 - Вебхук в секретном канале (если у кого-то есть доступ, он сможет все получить лягушку а это плохо).
 - Правильно размещенный бот [**disnake.py**](https://github.com/DisnakeDev/disnake)
 
 И так поехали!(жабы топ)

### Примеры
#### Бот
```py
import disnake
from disnake.ext import commands
from disnake.ext.dashboard import Dashboard

bot = commands.Bot(command_prefix="!")
bot_dashboard = Dashboard(bot,
	"secret_key", 
	"https://your-bot-website.com/dashboard"
)

@bot.event
async def on_ready():
	print(f"Bot is online as {bot.user}")

@bot.event
async def on_message(message):
	await bot_dashboard.process_request(message)

@bot_dashboard.route
async def guild_count(data):
	return len(bot.guilds)

@bot_dashboard.route
async def member_count(data):
	return await bot.fetch_guild(data["guild_id"]).member_count

bot.run("your-token-here")
```


#### Веб-сервер
```py
from quart import Quart, request
from disnake.ext.dashboard import Server

app = Quart(__name__)
app_dashboard = Server(
	app,
	"secret_key", 
	webhook_url="https://your-private-discord-webhook.com",
	sleep_time=1
)

@app.route("/")
async def index():
	guild_count = await app_dashboard.request("guild_count")
	member_count = await app_dashboard.request("member_count", guild_id=776230580941619251)

	return f"Guild count: {guild_count}, Server member count: {member_count}"

@app.route("/dashboard", methods=["POST"])
async def dashboard():
	# Don't worry about authorization, the bot will handle it
	await app_dashboard.process_request(request)
        
        
if __name__ == "__main__":
        app.run()
```


Обратите внимание, что Cogs в настоящее время не поддерживаются.'''

	

requirements = ["disnake>=2.7.0"]

setup(name='disnake-ext-dashboard',
      author='MaseZev',
      url='https://github.com/MaseZev/disnake-ext-dashboard',
      version=version,
      packages=['disnake.ext.dashboard'],
      license='MIT',
      description='Веб-перехватчик и расширение disnake на основе запросов для создания панели управления ботом.',
      long_description=readme,
      long_description_content_type="text/markdown",
      install_requires=requirements,
      python_requires='>=3.8.0',
      classifiers=[
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
      ]
)
