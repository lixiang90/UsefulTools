import random
import json
import base64
import requests
import time
# 基本提示词
basic_prompt = "master piece,best quality,beautiful,1girl,"

# 一些预设
hair_colors = ["red hair","blue hair","brown hair","yellow hair","golden hair","purple hair","white hair","pink hair","green hair","grey hair","blonde hair"]
hair_types = ["long hair","short hair","curly hair","straight hair","ponytail","twintails","cat ears","very long hair"]
eye_colors = ["red eyes","brown eyes","blue eyes","golden eyes","orange eyes","purple eyes","black eyes"]
body_types = ["full body", "half body","big breast","light smile","closed mouth","tears","medium breast","arms behind",
              "looking at the viewer","from side","laughing","from side","robotic"]
extra_body_types = ["ryougi shiki","misaka mikoto","hatsune miku","saber","violet evergarden","yukinoshita yukino","oyama mahiro","megumi kato","ganyu \(genshin impact\)"]
clothes = ["wearing school suit","wearing sailor suit","wearing jacket","wearing red kimino","wearing white kimino","wearing long dress","wearing skirt",
           "wearing red skirt","wearing blue skirt","wearing yellow skirt","wearing jean","wearing crop jean",
           "wearing wedding dress","wearing Tshirt","wearing military uniform","wearing armor","wearing pink lolita dress",
           "wearing black lolita dress","wearing witch costume","wearing spacesuit","wearing bikini","noble dress", "complicated decoration"]
extra_clothings = ["sports shoes","pantyhorse","wearing necklace","leather shoes","hairpin","gloves","wearing wreath","wearing crown",
                   "wearing pearl necklace","wearing CCCP badge","wearing glasses","wearing beret hat","wearing hat","wearing cloche hat",
                   "jewelry","wearing helmet"]
doing = ["playing guitar", "playing piano","swimming","reading a book","shopping","riding a horse","cooking","sitting on the grass","lying on bed",
         "laptop on knees","looking at the viewer","eating","in a car","driving a car","riding bicycle","riding motorcycle"]
timepoints = ["day","night","morning","noon","afternoon","dusk","rainy","sunny","outer space"]
background = ["stars","clouds","castle","blue sky","sunflowers","garden","big modern buildings","cherry blossoms","falling petals",
              "rain","church","street","cafeteria","library","light particle","in classroom","victorian era","beautiful detailed sky"]
painting = ["detailed","modelshoot style","ultra-detailed","various colors","volumetric light","hd photo","4k","raw photo","photorealistic"]
extra_painting = ["dramatic","psychedelic","god rays","vintage","hyperrealistic","cyberpunk"]

# 预设集，数字表示跳过该项预设的概率
settings = [(hair_colors,0.3),(hair_types,0.3),(eye_colors,0.3),(body_types,0.3),(extra_body_types,0.8),(clothes,0.4),(extra_clothings,0.5),
            (doing,0.6),(timepoints,0.6),(background,0.5),(painting,0.7),(extra_painting,0.8)]

# 负面词
negatives = ("(EasyNegative:1.2), (badhandv4:1.2), (bad_prompt_v2:0.8), (bad-hands-5:0.9), (ng_deepnegative_v1_75t:0.9),"
"(bad-artist:0.9), (worst quality:1.5), (low quality:1.5), (normal quality:1.5), (lowres), (normal quality:1.5), (monochrome:1.5),"
 "(worst quality, low quality:1.2), watermark, username, signature, bad anatomy, bad hands, text, error, missing fingers, extra digit, "
 "fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, bad feet, "
 "single color, (ugly), (duplicate), (morbid), (mutilated), (tranny), (trans), (trannsexual), (hermaphrodite), ((extra fingers)), mutated hands, "
 "(poorly drawn hands), (poorly drawn face), (mutation), (deformed), blurry, (bad anatomy), (bad proportions), (extra limbs), (disfigured), "
 "(bad anatomy), gross proportions, (malformed limbs), (missing arms), (missing legs), (extra arms), (extra legs), mutated hands,(fused fingers), "
 "(too many fingers), (long neck), (bad body perspect:1.1),(extra nipples:2),(multiple nipples:2),(many nipples:2),(extra hands),(many hands), (logo:2), "
 "(more than five fingers:1.2), (text:1.5), (extra arms), (multiple girls, multiple boys),nsfw")

def random_prompt():
    '''
    生成随机的妹子提示词
    '''
    prompt = basic_prompt
    # 随机选择各项预设
    for item in settings:
        randomnumber = random.random()
        if item[1] > randomnumber:
            prompt = prompt + f"{random.choice(item[0])},"
    # prompt += "trending"
    return prompt

def random_girl_reuqests(width=512,height=768):
    '''
    生成向webui的请求数据
    '''
    data = {"prompt":random_prompt(),"negative_prompt":negatives} # 随机生成正向词并写入固定的负向词
    data["sampler_name"] = "DPM++ 2M Karras" # 采样器
    data["width"] = width # 宽度
    data["height"] = height # 高度
    data["hr_upscaler"] = "Latent" # 超分辨率算法
    data["hr_scale"] = 2 # 超分辨倍数
    return data


def submit_post(url: str, data: dict):
    """
    Submit a POST request to the given URL with the given data.
    """
    return requests.post(url, data=json.dumps(data))


def save_encoded_image(b64_image: str, output_path: str):
    """
    Save the given image to the given output path.
    """
    with open(output_path, "wb") as image_file:
        image_file.write(base64.b64decode(b64_image))

def save_parms(params: json, output_path: str):
    '''
    保存原始请求数据
    '''
    with open(output_path,"w",encoding="utf-8") as f:
        f.write(json.dumps(params)) 

whscale = {"2:3":(512,768),"3:2":(768,512),"1:1":(512,512),"1:2":(512,1024),"2:1":(1024,512)}

def random_girl(savepath,width_height_scale="2:3"):
    '''
    生成随机妹子图并存储到指定文件夹
    '''
    w,h = whscale[width_height_scale] # 图像的宽度和高度
    
    data = random_girl_reuqests(width=w,height=h) # 生成随机妹子图请求数据
    txt2img_url = 'http://127.0.0.1:7860/sdapi/v1/txt2img' # sd webui api接口
    response = submit_post(txt2img_url, data) # 发送请求
    if response.status_code != 200: return 1 # 没有正确生成图片的情况
    filename = f"{int(time.time())}_{random.randint(0,10000000000)}" # 随机生成文件名

    save_encoded_image(response.json()['images'][0], f'{savepath}/{filename}.png')
    save_parms(data,f'{savepath}/{filename}.txt')
    return f"{savepath}/{filename}.png"