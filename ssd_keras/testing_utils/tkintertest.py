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
recipeJson = ''

root = Tk()
root.title("recipe")

canvas = Canvas(root, height = 350, width = 350, relief = RIDGE, bd = 2)
canvas.pack()
var = StringVar()
var.set('Now Loading')
StringLabel = Label(root, textvariable = var)
StringLabel.pack()

# 食材情報が記載されたローカルjsonファイルを削除（初期化）
if os.path.exists("ingredients.json"):
    os.remove("ingredients.json")

# サブプロセスでSSDで物体検出＋食材情報をローカルJSONファイルに追記させる
take_img = "python videotest_example.py"
subprocess.Popen(take_img.split())


def openLink(url):
    webbrowser.open(url)

# tkinterによるレシピ情報の提示
# 4秒ごとにループ実行
def change_flag():
    global ingredientsNum
    global recipeJson

    # ローカルのjsonファイル内の食材データをロード
    if os.path.exists("ingredients.json"):
        with open('ingredients.json') as f:
            jsn = json.load(f)

        # 食材が増えた時だけレシピAPIリクエスト(APIリクエスト数に分間5回までという制限があるため)
        if ingredientsNum < len(jsn["ingredients"]):
            ingredientsNum = len(jsn["ingredients"])
            # ランダムに食材を２件ピックアップしてレシピをAPIでレシピjsonを取得
            randomIngredientsList = random.choices(jsn["ingredients"],k=2)
            print(f'randomIngredientsList={randomIngredientsList}')
            tmp = getRecipeJson(randomIngredientsList)
            # 1個以上レシピが返ってくればレシピjsonを更新
            if tmp["count"] > 0:
                recipeJson = tmp

        # レシピjsonからランダムで１つレシピをチョイス
        randomRecipe = random.choices(recipeJson["hits"],k=1)

        # jsonから表示用にレシピ名、レシピ詳細URL、レシピサムネイル画像を取得
        recipeName = randomRecipe[0]['recipe']['label']
        recipe_url = randomRecipe[0]['recipe']['url']
        image_url = randomRecipe[0]['recipe']['image']

        # tkinterがjpgそのままだと表示できないらしいのでpng変換を経由して表示
        urllib.request.urlretrieve(image_url, "recipe.jpg")
        img = Image.open('./recipe.jpg')
        img.save('./recipe.png', 'png')
        canvas.photo = PhotoImage(file = 'recipe.png')
        canvas.create_image(175, 180, image = canvas.photo)

        # レシピ名更新
        var.set(recipeName)

        # クリックでレシピ詳細ページが開くボタンを設置
        btn = tkinter.Button(root, text='レシピを開く', command= lambda: openLink(recipe_url))
        btn.place(x=150, y=320)

    root.after(4000,change_flag)


# "edamam"という海外のレシピ情報サービス。無料会員登録でAPI利用可能。
# 無料版は分間5リクエスト、月間5000リクエストまで等制限有り。
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



