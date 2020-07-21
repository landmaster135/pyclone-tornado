import os
import json
import datetime
import requests
from flask import redirect, render_template, request, session
from functools import wraps

import shutil
from PIL import Image, ImageFilter

import pandas as pd
from sklearn.linear_model import LinearRegression, ElasticNet
from sklearn.model_selection import train_test_split

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

def most_freq(data):
    """
    Get the most frequent element in data.

    data: (data of list)
    """
    list_freq = []
    for i in data:
        freq = data.count(i)   # count appearance frequency
        list_freq.append(freq) # Add freq to list_freq
    return data[list_freq.index(max(list_freq))] # determine data

def get_weather_info(location, api_key):
    """
    Get weather information from OpenWeatherMap.

    location： (prefecture name)
    api_key ： (API key of OpenWeatherMap)

    return: (dictionary about weather)
    """
    # APIが渡されていなければメッセージを返す
    assert api_key != '', 'Define API key' # assert 条件式, 条件式がFalseの場合に出力するメッセージ
    # Download JSON data from API of OpenWeatherMap.org
    url = "http://api.openweathermap.org/data/2.5/forecast?q={location}&mode=json&appid={key}"
    api_url = url.format(location = location, key = api_key)

    # os.environ['HTTP_PROXY'] = "http://150.67.140.80:3128"

    response = requests.get(api_url) # connect web-site
    response.raise_for_status() # ステータスコードが200番台以外であれば例外を発生

    weather_data = json.loads(response.text) # Load from JSON data
    w = weather_data['list']

    # Prepare to get weather information
    KELVIN = 273.15
    n_days = 3     # In this case: today, tomorrow and day-after-tomorrow.
    list_days       = [] # List about days (datetime format)
    for i in range(n_days):
        d = {'day': datetime.datetime.now() + datetime.timedelta(days=1) * i}
        d['list_tmax']        = [] # List about max temperature
        d['list_tmin']        = [] # List about min temperature
        d['list_description'] = [] # List about weather description
        d['list_main']        = [] # List about weather main
        list_days.append(d)
    # Get weather information from web
    for k in list_days:
        for i in w: # 気象リストを走査
            di = i['dt_txt']
            if di[:di.find(" ")] == str(k['day'].date()): # 同じ日付の要素だったら、 ex. 2019-12-05
                k['list_tmax'].append(round(i['main']['temp_max'] - KELVIN, 1)) # Add temp_max to list
                k['list_tmin'].append(round(i['main']['temp_min'] - KELVIN, 1)) # Add temp_min to list
                k['list_description'].append(i['weather'][0]['description'])    # Add description to list
                k['list_main'].append(i['weather'][0]['main'])                  # Add main to list

    # Get weather information from list
    tmax = max(list_days[0]['list_tmax'])                     # determine max temperature (Day 0)
    tmin = min(list_days[0]['list_tmin'])                     # determine min temperature (Day 0)
    description = most_freq(list_days[0]['list_description']) # determine weather description (Day 0)
    main = most_freq(list_days[0]['list_main'])               # determine weather main (Day 0)

    dict_weather = {'tmax': tmax, 'tmin': tmin, 'description': description, 'main': main}

    return dict_weather

def db_dictionary():
    # DB table
    column_users         = {'id': 0, 'username': 1, 'location': 2, 'gender': 3, 'hash': 4, 'regist_date': 5}
    column_wardrobes     = {'id': 0, 'wardrobename': 1, 'userid': 2, 'category': 3, 'sleeve': 4, 'color': 5, 'warmscore': 6, 'freq_inweek': 7, 'inuse': 8}
    column_history_wear  = {'id': 0, 'userid': 1, 'wardrobeid_c': 2, 'wardrobeid_o': 3, 'wardrobeid_t': 4, 'wardrobeid_i': 5, 'wardrobeid_b': 6, 'wardrobeid_s': 7, 'wear_date': 8, 'temperature_max': 9, 'temperature_min': 10, "comfort_score": 11}
    column_history_own   = {'id': 0, 'wardrobeid': 1, 'from': 2, 'to': 3}
    column_weather_today = {'id': 0, 'location': 1, 'date': 2, 'weather': 3, 'temperature_max': 4, 'temperature_min': 5, 'humidity': 6}
    return {"column_users": column_users, "column_wardrobes": column_wardrobes,
            "column_history_wear": column_history_wear, "column_history_own": column_history_own,
            "column_weather_today": column_weather_today
           }

def category_dictionary():
    """Rerutn category-dictionary"""
    # list_category = ["コート", ジャケット", "ニット", "カーディガン", "ベスト", "パーカー", "ジャージ", "アウター", "トレーナー", "Tシャツ", "カットソー", "シャツ", "ポロシャツ", "トップス", "上衣のインナー", "下衣のインナー", "インナー", "パンツ", "スカート", "ワンピース"]
    list_category_o = ["Coat", "Jacket", "Knitwear", "Cardigan", "Vest", "Hoodie", "Jersey", "Outer"]
    list_category_t = ["Sweatshirt", "T-shirt", "Cut-and-sew", "Shirt", "Polo shirt", "Tops"]
    list_category_i = ["Tanktop", "Camisole", "Inner"]
    list_category_b = ["Pants", "Skirt", "Dress", "Spats"]
    dict_category   = {"-Outer Category-": list_category_o,
                       "-Tops Category-": list_category_t,
                       "-Inner Category-": list_category_i,
                       "-Bottoms Category-": list_category_b}
    return dict_category

def sleeve_list():
    """Rerutn sleeve-dictionary"""
    # list_sleeve   = ["袖なし", "半袖", "七分袖", "九分袖", "長袖"]
    list_sleeve     = ["Sleeveless", "Short", "3/4", "9/10", "Long"]
    return list_sleeve

def color_dictionary():
    """Rerutn color-dictionary"""
    # list_color    = ["白", "黒", "グレー", "ブラウン", "ベージュ", "グリーン", "ブルー", "パープル", "イエロー", "ピンク", "レッド", "オレンジ", "シルバー", "ゴールド", "その他"]
    dict_color = {"White": "FFFFFF", "Black": "000000", "DimGray": "696969", "Gray": "808080", "Brown": "8B4513", "Beige": "F5F5DC", "Green": "008000", "Blue": "0000FF", "Purple": "800080", "Yellow": "FFFF00", "Pink": "FF69B4", "Red": "FF0000", "Orange": "FF8C00", "Silver": "C0C0C0", "Gold": "FFD700", "Others": "1000000"}
    return dict_color

def save_image(im_file, im_path, filename, alt_path, passing=False):
    """Put image file in the folder."""
    if im_file.filename == '': # If image file isn't submitted, alternative file is copied.
        if passing == True: # In case of editting
            pass # Do nothing
        else: # In the other case
            shutil.copyfile(alt_path, os.path.join(im_path, filename)) # Duplicate image file
        return True
    else:
        im_file.save(os.path.join(im_path, filename)) # Save image file
        return False
    # # Resize image
    # im = Image.open(os.path.join(im_path, '{}.jpg'.format(wardrobename)))
    # im_size = im.width + im.height
    # im_new_quality = 100
    # if im_size > 1024: # If size is over 1024, Resize immage
    #     im_new_quality = int(1024 / im_size * 100)
    # im.save(os.path.join(im_path, '{}.jpg'.format(wardrobename)), quality=im_new_quality)

def model_learning(data):
    # # 線形単回帰 Linear Regression
    # for i in feature_names:
    #     train_X, test_X, train_y, test_y = train_test_split(
    #         data[i],data["comfort_score"],random_state=42) # トレーニングとテストデータを作成
    #     print(data[i][0])
    #     # Xのデータの形を修正
    #     train_X = train_X.values.reshape((-1, 1))
    #     test_X = test_X.values.reshape((-1, 1))
    #     model = LinearRegression() # Generate model
    #     model.fit(train_X, train_y) # Let model learn
    #     print(model.predict(test_X))
    #     print("線形単回帰：{}".format(i)) # データ列
    #     print("決定係数：{}\n".format(model.score(test_X, test_y))) # テストして出た決定係数

    # 線形重回帰 Linear Multiple Regression
    train_X, test_X, train_y, test_y = train_test_split(
        data.drop("comfort_score", axis=1), data["comfort_score"], random_state=42)
    model = LinearRegression()
    model.fit(train_X, train_y)
    print(test_X)
    # print(model.predict(test_X))
    print("線形重回帰：{}".format("comfort_score")) # データ列
    print("決定係数：{}\n".format(model.score(test_X, test_y))) # テストして出た決定係数

    # # ElasticNet回帰
    # train_X, test_X, train_y, test_y = train_test_split(data.drop("comfort_score", axis=1), data["comfort_score"], random_state=42)
    # model = ElasticNet(l1_ratio=0.0) # ラッソで鑑みる割合
    # model.fit(train_X, train_y) # Let model learn
    # print("ElasticNet回帰：{}".format(model.score(test_X, test_y)))

    return model

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

def generate_function_to_text(func_name, path, data):
    with open(path, mode='w') as f:
        f.writelines("def {}():".format(str(func_name)))
        f.writelines("\n\tvalue = {}".format(str(data)))
        f.writelines("\n\treturn value")