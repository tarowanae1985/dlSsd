from tkinter import *
import tkinter
from PIL import Image
import subprocess
import json
import cv2
import urllib.request
import urllib.parse
import os
import os.path
import random
import webbrowser

# 素材数の増加カウンタ
ingredientsNum = 0
# レシピAPIレスポンス
json_body = ''

root = Tk()
root.title("HOME")

if os.path.exists("ingredients.json"):
    os.remove("ingredients.json")

# take_img = "python getImage.py"# 写真撮影スクリプト
take_img = "python videotest_example.py"# 写真撮影スクリプト

canvas = Canvas(root, height = 350, width = 350, relief = RIDGE, bd = 2)
canvas.pack()
var = StringVar()
var.set('Now Loading')
StringLabel = Label(root, textvariable = var)
StringLabel.pack()

subprocess.Popen(take_img.split())


def openLink(url):
# def openLink():
    webbrowser.open(url)
    # return 0

# 写真更新
# 30秒毎に写真を撮影しcanvasの写真を更新させたい
def change_flag():
    global ingredientsNum
    global json_body

    # json内の食材データをロード
    if os.path.exists("ingredients.json"):
        with open('ingredients.json') as f:
            jsn = json.load(f)

        # 食材が増えた時だけレシピAPIリクエスト(APIリクエスト数に分間5回までという制限があるため)
        if ingredientsNum < len(jsn["ingredients"]):
            ingredientsNum = len(jsn["ingredients"])
            # ランダムに食材を最大２件ピックアップしてレシピをAPI取得
            newingredientsList = random.choices(jsn["ingredients"],k=2)
            print(f'newingredientsList={newingredientsList}')
            json_body = getRecipeJson(newingredientsList)

        #jsonレスポンスからレシピをランダムで１つチョイス
        randomRecipe = random.choices(json_body["hits"],k=1)

        recipeName = randomRecipe[0]['recipe']['label']
        recipe_url = randomRecipe[0]['recipe']['url']
        image_url = randomRecipe[0]['recipe']['image']
        urllib.request.urlretrieve(image_url, "recipe.jpg")
        img = Image.open('./recipe.jpg')
        img.save('./recipe.png', 'png')

        # Static1 = tkinter.Label(text=recipeName)
        # Static1.pack()
        var.set(recipeName)

        canvas.photo = PhotoImage(file = 'recipe.png')
        canvas.create_image(175, 180, image = canvas.photo)

        btn = tkinter.Button(root, text='レシピを開く', command= lambda: openLink(recipe_url))
        btn.place(x=150, y=300)
        # btn.pack(fill = 'x' ,side = 'top')

        # button_draw = tkinter.Button(root, text=u'レシピを開く',width=30)
        # # button_draw.bind("<Button-1>",command= lambda: openLink(recipe_url))
        # button_draw.bind("<Button-1>",command=openLink)
        # button_draw.place(x=75,y=400)

    root.after(4000,change_flag)


def getRecipeJson(ingredients):    
    param = {
        'q'      :','.join(ingredients),
        'app_id' :'1248d21d',
        'app_key':'856b2ea030700759e5e8763d585efc80',
        'from'   :'0',
        'to'     :'10',
    }
    query = urllib.parse.urlencode(param)
    url = 'https://api.edamam.com/search?' + query
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as res:
        body = json.load(res)

    return body

root.after(0, change_flag)
root.mainloop()



