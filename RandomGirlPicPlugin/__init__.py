from nonebot import get_driver
from nonebot.plugin import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import MessageSegment,Message
from .config import Config
from .LocalDiffusionInfer import random_girl
import base64
from nonebot.params import CommandArg
import os

global_config = get_driver().config
config = Config.parse_obj(global_config)

girl = on_command("二次元", rule=to_me(), aliases={"妹子", "图片", "妹子图", "girl"}, priority=10, block=True)
savepath = 'images'
if not os.path.exists(savepath):
    os.mkdir('images')
    
@girl.handle()
async def handle_function(args: Message = CommandArg()):
    picsize = args.extract_plain_text()
    if picsize not in ["2:3","3:2","1:1","1:2","2:1",""]:
        await girl.finish("错误的尺寸数据(请输入以下之一：2:3,3:2,1:1,1:2,2:1)")
    else:
        await girl.send("正在生成图片...")
        if picsize=="":
            picsize = "2:3"
        picname = random_girl(savepath,width_height_scale=picsize)
        if picname == 1: # 返回1表示网络请求失败
            await girl.finish("生成图片失败！")
        else:
            await girl.send("完成！")
            with open(picname,'rb') as img:
                img_bytes = img.read()
            base64_str = "base64://" + base64.b64encode(img_bytes).decode()
            msg = MessageSegment.image(base64_str)
            await girl.finish(msg)