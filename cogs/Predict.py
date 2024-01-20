from discord.ext import commands
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import discord, requests, os

class Predict(commands.Cog):
    def __init__(self, bot):
        load_dotenv()
        self.bot = bot
        self.dream_api = os.getenv("PREDICT_DREAM_API")

    async def types(self, ctx: discord.AutocompleteContext):
        return [
            "ความฝัน",
        ]

    async def predict_dream(self, prompt):
        try:
            search_param = self.dream_api
            search_param += prompt
            response = requests.get(search_param)
            soup = BeautifulSoup(response.text, 'html.parser')
            dream_title = soup.find_all("div", {"class": "dn"})
            dream_description = soup.find_all("div", {"class": "dx"})
            # get list of text limit to 5
            dream_title = [title.text for title in dream_title][:5]
            dream_description = [desc.text for desc in dream_description][:5]
            dream_description = [desc.replace("\n", "") for desc in dream_description]
            if len(dream_title) == 0 or len(dream_description) == 0:
                raise Exception
            return dream_title, dream_description
        except:
            return None, None

    @discord.slash_command(description="ทำนายเรื่องต่างๆที่เกิดขึ้นกับตัวเอง")
    async def predict(self, ctx, type: discord.Option(str, "หมวดหมู่",autocomplete=types, required=True), prompt: discord.Option(str, "เรื่องที่ต้องการทำนาย", required=True)):
        if type == "ความฝัน":
            title, description= await self.predict_dream(prompt)
            if(title != None or description != None):
                embed = discord.Embed(title=f"ทำนายความฝันเกี่ยวกับ {prompt} หรือที่เกี่ยวข้อง", description="* โปรดใช้วิจารณญาณในการอ่าน", color=0x00ff00)
                for title, desc in zip(title, description):
                    embed.add_field(name=title, value=desc, inline=False)
                await ctx.respond(embed=embed)
            else:
                await ctx.respond("ไม่พบข้อมูลที่ต้องการทำนาย")
def setup(bot):
    bot.add_cog(Predict(bot))
    print("Module Predict loaded")