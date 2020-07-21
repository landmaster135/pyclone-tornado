import os
import json
import datetime
# from cs50 import SQL
import sqlite3
from contextlib import closing
from flask import Flask, redirect, render_template, request, session, json, jsonify, Markup
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

import shutil
from PIL import Image, ImageFilter

import pandas as pd
from sklearn.linear_model import LinearRegression, ElasticNet
from sklearn.model_selection import train_test_split

from helpers import login_required, usd, get_weather_info, db_dictionary, category_dictionary, sleeve_list, color_dictionary, save_image, model_learning, apology

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"]

# make json not garbled
# app.config['JSON_AS_ASCII'] = False

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
dbpath = 'wwwardrobe.sqlite' # DB's path

# DB table
column_users         = db_dictionary()["column_users"]
column_wardrobes     = db_dictionary()["column_wardrobes"]
column_history_wear  = db_dictionary()["column_history_wear"]
column_history_own   = db_dictionary()["column_history_own"]
column_weather_today = db_dictionary()["column_weather_today"]

# Folder for wardrobe-images
image_path = os.path.join("static", "wardrobe_image")
# Directory of alternative image
alt_path = os.path.join(image_path, "Alternative.jpg")
# Directory of the image which portrays no wardrobe is selected
nowardrobe_path = os.path.join(image_path, "NoWardrobe.jpg")
# Folder for material
material_path = os.path.join("static", "material")
# Directory for temporary wardrobe-image
temp_directory = "temp"


@app.route("/")
@login_required
def index():
    """Show home page"""
    # DB connection and cursor generation
    connection = sqlite3.connect(dbpath)
    # connection.isolation_level = None # 自動コミットにする場合は下記を指定（コメントアウトを解除のこと）
    cursor = connection.cursor()
    # Get user
    cursor.execute("SELECT * FROM users WHERE id = :userid",
                    {'userid': session["user_id"]})
    rows_users = cursor.fetchall() # users row

    # Get weather and user information to display
    username     = rows_users[0][column_users["username"]] # Get user's name
    location     = rows_users[0][column_users["location"]] # Get user's location
    my_api_key   = '9e020c2778848bfdd79d50e5e4cdfff0'      # Get API Key
    dict_weather = get_weather_info(location, my_api_key)  # Get weather in the location
    weather = dict_weather['main'] # Today's weather
    t_max   = dict_weather['tmax'] # Maximum temperature
    t_min   = dict_weather['tmin'] # Minimum temperature
    img_url_w = os.path.join("..", material_path, "weather_{}.png".format(weather)) # Image of Today's weather


    # Get wardrobe-image url to display
    cursor.execute("SELECT * FROM history_wear WHERE userid = :userid AND wear_date = :today;",
                    {"userid": session["user_id"],
                     "today" : str(datetime.datetime.now().date())
                    })
    rows_hw = cursor.fetchone() # history_wear row
    # Dicionary which will put image-url on wardrobeid
    dict_image_url = {"wardrobeid_c": "", "wardrobeid_o": "", "wardrobeid_t": "",
                      "wardrobeid_i": "", "wardrobeid_b": "", "wardrobeid_s": ""
                     }
    # Message to display
    today_message = ""
    notice_message = ""
    print(rows_hw)
    
    # Variable to assess whether wardrobe is selected today
    have_selected = False
    # Display the wardrobes selected today
    if rows_hw == None: # if wardrobe haven't been selected yet,
        for key in dict_image_url.keys():
            dict_image_url[key] = nowardrobe_path
            today_message ="Not selected outfit today yet"
    else: # if wardrobe have been selected,
        if rows_hw[column_history_wear["comfort_score"]] != None:
            notice_message = "You have input comfort today."
        for key in dict_image_url.keys(): # if a wardrobe isn't selected,
            if rows_hw[column_history_wear[key]] == None:
                dict_image_url[key] = nowardrobe_path
            else: # if a wardrobe selected,
                # Select DB for wardrobes to get wardrobename from wardrobeid
                cursor.execute("SELECT wardrobename FROM wardrobes WHERE id = :wardrobeid;",
                                {"wardrobeid": rows_hw[column_history_wear[key]]
                                })
                # Get wardrobename
                rows_wn = cursor.fetchone()
                # Set image-url from wardrobename
                dict_image_url[key] = os.path.join("..", image_path, str(session["user_id"]), "{}.jpg".format(rows_wn[0]))
        today_message = "Your outfit today"
        have_selected = True

    # Forget which page user is in now (for ajax)
    session["nowpage"] = ""

    return render_template("index.html", username=username, location=location, weather=weather, img_url_w=img_url_w,
                           t_max=t_max, t_min=t_min, img_urls=dict_image_url, today_message=today_message,
                           message=notice_message, have_selected=have_selected)

@app.route("/recordcomfort", methods=["POST"])
def recordcomfort():
    """Record comfort-score today"""
    # User reached route via GET (as by clicking a link or via redirect)
    if not request.method == "POST":
        pass
    # User reached route via POST (as by submitting a form via POST)
    else:
        pass
    # DB connection and cursor generation
    connection = sqlite3.connect(dbpath)
    # connection.isolation_level = None # 自動コミットにする場合は下記を指定（コメントアウトを解除のこと）
    cursor = connection.cursor()
    # Update DB for history_wear
    cursor.execute("UPDATE history_wear SET comfort_score = :t_comfort_score WHERE userid = :t_userid;",
                    {"t_comfort_score": int(request.form.get("comfort")),
                     "t_userid"       : int(session["user_id"])
                    })

    connection.commit() # DB commit

    return redirect("/") # Display home page

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()
    # User reached route via GET (as by clicking a link or via redirect)
    if not request.method == "POST":
        return render_template("login.html") # Display login form
    # User reached route via POST (as by submitting a form via POST)
    else:
        # Exception handling
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username") # テスト
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password") # テスト
        # DB connection and cursor generation
        connection = sqlite3.connect(dbpath)
        # connection.isolation_level = None # 自動コミットにする場合は下記を指定（コメントアウトを解除のこと）
        cursor = connection.cursor()
        # Query DB for username
        cursor.execute("SELECT * FROM users WHERE username = :username",
                            {'username': request.form.get("username")})
        # Ensure username exists and password is correct
        rows = cursor.fetchall()
        if len(rows) != 1 or not check_password_hash(rows[0][column_users["hash"]], request.form.get("password")):
            return apology("invalid username and/or password", 403) # テスト？
        # Remember which user has logged in
        session["user_id"]       = rows[0][column_users["id"]]
        session["user_location"] = rows[0][column_users["location"]]
        # The value where user is from beforehand
        session["pagefrom"] = ""

        # Store weather-information today ------------------------------------
        cursor.execute("SELECT * FROM users WHERE username = :username",
                        {'username': request.form.get("username")})
        rows_users = cursor.fetchall()
        location   = rows_users[0][column_users["location"]] # Get user's location
        cursor.execute("SELECT * FROM weather_today WHERE location = :t_location;",
                        {'t_location': location})
        rows_weather = cursor.fetchall()                       # Get weather-information
        today        = str(datetime.datetime.now().date())     # Get today as string value
        my_api_key   = '9e020c2778848bfdd79d50e5e4cdfff0'      # Get API Key
        dict_weather = get_weather_info(location, my_api_key)  # Get weather in the location
        weather      = dict_weather['main'] # Today's weather
        t_max        = dict_weather['tmax'] # Maximum temperature
        t_min        = dict_weather['tmin'] # Minimum temperature
        humidity     = 0     # 作らねば # Average of humidity
        print(rows_weather)
        if len(rows_weather) == 0: # If there is no information on that "location",
            cursor.execute("INSERT INTO weather_today({0}, {1}, {2}, {3}, {4}, {5}) VALUES (:t_l, :t_d, :t_w, :t_tmax, :t_tmin, :t_h);".format(
                            "location", "date", "weather", "temperature_max", "temperature_min", "humidity"),
                            {"t_l": location, "t_d": today, "t_w": weather, "t_tmax": t_max, "t_tmin": t_min, "t_h": humidity})
        else:
            if today != rows_weather[0][column_weather_today['date']]: # If no information is about today,
                cursor.execute("UPDATE weather_today SET {0} = :t_d, {1} = :t_w, {2} = :t_tmax, {3} = :t_tmin, {4} = :t_h WHERE {5} = :t_l;".format(
                                "date", "weather", "temperature_max", "temperature_min", "humidity", "location"),
                                {"t_l": location, "t_d": today, "t_w": weather, "t_tmax": t_max, "t_tmin": t_min, "t_h": humidity})
            else:
                pass
        connection.commit() # DB commit

        # Redirect user to home page
        return redirect("/")

@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()      # Forget any user_id
    return redirect("/") # Redirect user to login form

@app.route("/register", methods=["GET"])
def register():
    """Entry information to register"""
    locations = [] # Get the JSON content
    locations = ["Tokyo", "Shanghai", "Bangkok"] # テスト

    return render_template("register.html", locations=locations) # complete registering

@app.route("/registered", methods=["GET", "POST"])
def registered():
    """Try to register"""
    # User reached route via GET (as by clicking a link or via redirect)
    if not request.method == "POST":
        return redirect("/") # Redirect user to login form
    # User reached route via POST (as by submitting a form via POST)
    else:
        # DB connection and cursor generation
        connection = sqlite3.connect(dbpath)
        # connection.isolation_level = None # 自動コミットにする場合は下記を指定（コメントアウトを解除のこと）
        cursor = connection.cursor()

        username    = request.form.get("username")
        location    = request.form.get("location")
        gender      = request.form.get("gender")
        password    = request.form.get("password")
        # Get today as string value
        dt = str(datetime.datetime.now())
        regist_date = dt[:dt.find(".")]
        # Select DB for users
        cursor.execute("SELECT * FROM users WHERE username = :username",
                        {'username': username
                        })
        checkname = cursor.fetchall()
        # Exception handling
        if len(checkname) > 0:
            return redirect("/") # Username is taken
        if location == "--Select location--":
            return redirect("/") # location is invalid
        if password != request.form.get("confirm"):
            return redirect("/") # passwords in disagreement
        # Insert DB for wardrobes
        cursor.execute("INSERT INTO users(username, location, gender, hash, regist_date) VALUES(:t_username, :t_location, :t_gender, :t_hash, :t_regist_date)",
                        {'t_username': username,
                         't_location': location,
                         't_gender': gender,
                         't_hash': generate_password_hash(password),
                         't_regist_date': regist_date
                        }) # 入力値をDBに格納する。
        connection.commit() # DB commit
        cursor.execute("SELECT * FROM users WHERE username = :username",
                        {'username': username
                        })
        row = cursor.fetchall()

        # Make a folder to hold user's wardrobe-image
        image_id_path = os.path.join(image_path, row[0][column_users["id"]])
        if not os.path.exists(image_id_path):
            os.mkdir(image_id_path)
            os.mkdir(os.path.join(image_id_path, temp_directory))

        return render_template("registered.html")

@app.route("/recommend", methods=["GET", "POST"])
@login_required
def recommend():
    """Recommend user's best cloth today"""
    # User reached route via GET (as by clicking a link or via redirect)
    if not request.method == "POST":
        pass
    # User reached route via POST (as by submitting a form via POST)
    else:
        pass
    # DB connection and cursor generation
    connection = sqlite3.connect(dbpath)
    # connection.isolation_level = None # 自動コミットにする場合は下記を指定（コメントアウトを解除のこと）
    cursor = connection.cursor()

    # Prepare csv file to Machine Learning --------------------------------------
    # Get wardrobe-image url to display
    cursor.execute("SELECT * FROM history_wear WHERE userid = :userid AND NOT comfort_score = '';",
                    {"userid": session["user_id"]
                    })
    rows_hw = cursor.fetchall() # history_wear row

    # Generate list of "history_wear" (wardrobeid is converted to warmscore AND wear_date is removed)
    list_hw  = [] # List about a record of history_wear
    list_hws = [] # List about records of history_wear
    for num in range(len(rows_hw)):
        for i in ['wardrobeid_c', 'wardrobeid_o', 'wardrobeid_t', 'wardrobeid_i', 'wardrobeid_b', 'wardrobeid_s']:
            # Select DB same as wardrobe-id.
            cursor.execute("SELECT * FROM wardrobes WHERE id = :wardrobeid;",
                            {"wardrobeid": rows_hw[num][column_history_wear[i]]
                            })
            rows_wr = cursor.fetchall() # wardorbes row
            if rows_wr == []: # If rows_wr is empty,
                warmscore = 0
            else:
                list_wr = [] # wardorbes list あとで使うかも
                list_wr.append(rows_wr) # あとで使うかも
                warmscore = rows_wr[0][column_wardrobes['warmscore']] # Get warmscore
            list_hw.append(warmscore) # Store in a list
        for i in ['temperature_max', 'temperature_min', 'comfort_score']:
            list_hw.append(round(rows_hw[num][column_history_wear[i]], 0))
        list_hws.append(list_hw) # Store in a list
        list_hw = [] # Set default value

    # Part of Machine Learning -----------------------------------------
    # Convert list of "history_wear" to pd.DataFrame of "history_wear"
    feature_names = ["warmscore_c", "warmscore_o", "warmscore_t",
                     "warmscore_i", "warmscore_b", "warmscore_s",
                     "temperature_max", "temperature_min", "comfort_score"]
    data = pd.DataFrame(list_hws, columns=feature_names)
    model = model_learning(data)

    # Part of Machine Predicting -------------------------------------------
    # Select DB for wardrobes
    cursor.execute("SELECT * FROM wardrobes WHERE userid = :t_userid AND inuse = 1;",
                    {"t_userid": session["user_id"]
                    })
    rows_wr = cursor.fetchall()
    dict_category = category_dictionary() # Dictionary about wardrobe's category
    dict_wr_category = {"-Outer Category-": [], "-Tops Category-": [],
                        "-Inner Category-": [], "-Bottoms Category-": []}
    combi_content = {} # wardrobe-combination on category
    combi_score   = {} # score on wardrobe-combination on category
    num           = 0  # for index of "combi_content"
    iter_num_o    = 0  # for iterate like MECE for '-Outer Category-'
    iter_num_b    = 0  # for iterate like MECE for '-Bottoms Category-'
    __len_combi__ = 20000
    for i in range(__len_combi__):
        combi_content[i] = {}
    # Generate dictionary on category
    for i in rows_wr:
        for key, value in dict_category.items():
            if i[column_wardrobes['category']] in value: # If category is same,
                dict_wr_category[key].append(i[column_wardrobes['id']])
                break
            else:
                pass
    # Append NULL to dictionary on category
    for key in dict_wr_category.keys():
        dict_wr_category[key].append(None)
    # Generate wardrobe-combination on category
    len_o = len(dict_wr_category['-Outer Category-'])   # Length of dictionary
    len_b = len(dict_wr_category['-Bottoms Category-']) # Length of dictionary
    for c in range(0, len_o):
        for o in range(iter_num_o, len_o):
            bool_co = c == len_o - 1 and o == len_o - 1
            if bool_co or c != o : # Same wardrobes cannot be combi except both are None
                for t in dict_wr_category['-Tops Category-']:
                    for i in dict_wr_category['-Inner Category-']:
                        iter_num_b = 0 # Reset start of counting
                        for b in range(0, len_b):
                            for s in range(iter_num_b, len_b):
                                bool_bs = b == len_b - 1 and s == len_b - 1
                                if b != s or bool_bs: # Same wardrobes cannot be combi except both are None
                                    combi_content[num]['wardrobeid_c'] = dict_wr_category['-Outer Category-'][c]
                                    combi_content[num]['wardrobeid_o'] = dict_wr_category['-Outer Category-'][o]
                                    combi_content[num]['wardrobeid_t'] = t
                                    combi_content[num]['wardrobeid_i'] = i
                                    combi_content[num]['wardrobeid_b'] = dict_wr_category['-Bottoms Category-'][b]
                                    combi_content[num]['wardrobeid_s'] = dict_wr_category['-Bottoms Category-'][s]
                                    num += 1 # Count dictionary-length
                                    if num >= __len_combi__:
                                        combi_content[num] = {}
                                    else:
                                        pass
                            iter_num_b += 1 # Shift start of counting
        iter_num_o += 1 # Shift start of counting

    # Generate predicted values on wardrobe-combination
    __best_score__ = 5 # Best comfort score
    for i in range(num):
        combi_score[i] = [0,0,0,0,0,0] # Set default value
    for key, value in combi_content.items(): # Search in the dictionaries about wardrobe-combination
        for k, v in value.items():           # Search in the dictionary about wardrobe-combination
            for i in rows_wr:                # Search in the list about wardrobes-DB
                if v == i[column_wardrobes['id']]: # If two wardrobe-id are same
                    combi_score[key][column_history_wear[k] - column_history_wear['wardrobeid_c']] = i[column_wardrobes['warmscore']] # Store warmscore
                    break
    # Append temperature
    location = session["user_location"] # Get user's location
    cursor.execute("SELECT * FROM weather_today WHERE location = :t_location;",
                    {'t_location': location})
    rows_weather = cursor.fetchall()
    for key, value in combi_score.items():
        combi_score[key].extend([rows_weather[0][column_weather_today["temperature_max"]],
                                 rows_weather[0][column_weather_today["temperature_min"]]
                                ])

    # # If you wanna execute other environment(ex. jupyternotebook)
    # path_w = "combi_score.py"
    # generate_function_to_text("generate_dict_score", path_w, combi_score)

    # Generate pandas-dataframe from dictionary
    data_warmscore = pd.DataFrame.from_dict(combi_score, orient='index', columns=feature_names[0:7+1])
    list_predict_score = model.predict(data_warmscore) # Predict (Linear Multiple Regression)
    dict_predict_score = {}                            # predict-scores by model of machine learning
    for i in range(0, num): # Store absolute value of difference between "__best_score__" and "list_predict_score"
        dict_predict_score[i] = abs(list_predict_score[i] - __best_score__)
    dict_predict_best = {}  # Store best comfort-score
    num_candidate = 3       # Number of candidates of combination

    # Get "num_candidate" of the best "comfort-score"
    for k, v in  sorted(dict_predict_score.items(), key=lambda x: x[1]):
        dict_predict_best[k] = v
        num_candidate -= 1
        if num_candidate == 0:
            break

    # Get wardrobeid-combination
    # dict_predict_best = {3761: 0.0006331531891259345, 19205: 0.0006331531891259345, 3597: 0.0012729990001982827}
    combi_content_best = []
    num_candidate = 0
    for k in dict_predict_best.keys():
        combi_content_best.append(combi_content[k])
        num_candidate += 1

    # Part of "Today's Recommend" -----------------------------------------
    # Dicionary which will put image-url on wardrobeid
    dict_image_url = {"wardrobeid_c": 2, "wardrobeid_o": None, "wardrobeid_t": 7,
                      "wardrobeid_i": None, "wardrobeid_b": 3, "wardrobeid_s": None
                     }
    # dict_image_url = combi_content_best[0]
    # Dictionary which will put wardrobe-name on wardrobeid
    dict_wardrobename = {}
    # Display the wardrobes selected today
    for key, value in dict_image_url.items(): # if a wardrobe isn't selected,
        if value == None:
            dict_image_url[key] = nowardrobe_path
            dict_wardrobename[key] = "~NoWardrobe~"
        else: # if a wardrobe is selected,
            # Select DB for wardrobes to get wardrobename from wardrobeid
            cursor.execute("SELECT wardrobename FROM wardrobes WHERE id = :wardrobeid;",
                            {"wardrobeid": value
                            })
            # Get wardrobename
            rows_wn = cursor.fetchone()
            # Set image-url from wardrobename
            dict_image_url[key] = os.path.join("..", image_path, str(session["user_id"]), "{}.jpg".format(rows_wn[0]))
            dict_wardrobename[key] = rows_wn[0]

    # Part of "What's your outfit today?" --------------------------------------
    # Select DB for wardrobes
    cursor.execute("SELECT * FROM wardrobes as T1 LEFT JOIN (SELECT wardrobeid, date_to FROM history_own) T2 ON T1.id = T2.wardrobeid WHERE userid = :t_userid AND date_to = 'ongoing';",
                    {'t_userid': session["user_id"]
                    })
    tuple_row = cursor.fetchall()

    dict_category = category_dictionary() # Dictionary about wardrobe's category
    list_wardrobe_o = []                  # outer category
    list_wardrobe_t = []                  # tops category
    list_wardrobe_i = []                  # inner category
    list_wardrobe_b = []                  # bottoms category
    # Put wardrobe-name in list for "select" tag
    for i in tuple_row:
        if i[column_wardrobes["category"]] in dict_category["-Outer Category-"]:
            list_wardrobe_o.append(i[column_wardrobes["wardrobename"]])
        elif i[column_wardrobes["category"]] in dict_category["-Tops Category-"]:
            list_wardrobe_t.append(i[column_wardrobes["wardrobename"]])
        elif i[column_wardrobes["category"]] in dict_category["-Inner Category-"]:
            list_wardrobe_i.append(i[column_wardrobes["wardrobename"]])
        elif i[column_wardrobes["category"]] in dict_category["-Bottoms Category-"]:
            list_wardrobe_b.append(i[column_wardrobes["wardrobename"]])
    dict_list_wardrobe = {"c": list_wardrobe_o, "o": list_wardrobe_o,
                          "t": list_wardrobe_t, "i": list_wardrobe_i,
                          "b": list_wardrobe_b, "s": list_wardrobe_b
                         }

    # Remember which page user is in now
    session["nowpage"] = "recommend"

    return render_template("recommend.html", img_urls=dict_image_url, names=dict_wardrobename, wardrobes=dict_list_wardrobe) # おすすめの服を反映。

@app.route("/decided", methods=["POST"])
@login_required
def decided():
    # User reached route via GET (as by clicking a link or via redirect)
    if not request.method == "POST":
        # return render_template("catalogcloth.html")
        pass
    # User reached route via POST (as by submitting a form via POST)
    else:
        pass

    # DB connection and cursor generation
    connection = sqlite3.connect(dbpath)
    # connection.isolation_level = None # 自動コミットにする場合は下記を指定（コメントアウトを解除のこと）
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM weather_today WHERE location = :t_location;",
                    {'t_location': session["user_location"]})
    rows_weather = cursor.fetchall()

    # Dictionary about DB
    list_history_wear = []
    # Get weather information from DB
    dict_weather = {"weather"        : rows_weather[0][column_weather_today['weather']],
                    "temperature_max": rows_weather[0][column_weather_today['temperature_max']],
                    "temperature_min": rows_weather[0][column_weather_today['temperature_min']],
                    "humidity"       : rows_weather[0][column_weather_today['humidity']]}

    # Store values into "list_history_wear"
    for key, value in column_history_wear.items():
        if key == 'id' or key == 'comfort_score': # index=0
            pass
        elif 'wardrobeid' in key: # index=1~6
            if "--" in request.form.get(key.replace('id', 'name')): # If nothing is selected,
                list_history_wear.append(None)
            else: # If wardrobe is selected,
                # Select DB for wardrobes (all the user's wardrobes)
                cursor.execute("SELECT * FROM wardrobes WHERE userid = :t_userid AND wardrobename = :t_wardrobename;",
                                {'t_userid': session["user_id"],
                                 't_wardrobename': request.form.get(key.replace('id', 'name'))
                                })
                tuple_row =  cursor.fetchone()
                list_history_wear.append(tuple_row[column_wardrobes["id"]])
        elif key == 'wear_date': # index=7
            # Get today as string value
            list_history_wear.append(str(datetime.datetime.now().date()))
        elif 'temperature' in key: # index=8,9
            list_history_wear.append(dict_weather[key])
        else:
            pass

    # Insert DB for history
    num_shift = 2
    cursor.execute("INSERT INTO history_wear({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}) VALUES ({10}, {11}, {12}, {13}, {14}, {15}, {16}, {17}, {18}, {19});".format(
                    "userid", "wardrobeid_c", "wardrobeid_o", "wardrobeid_t", "wardrobeid_i",
                    "wardrobeid_b", "wardrobeid_s", "wear_date", "temperature_max", "temperature_min",
                    ":t_userid", ":t_wardrobeid_c", ":t_wardrobeid_o", ":t_wardrobeid_t", ":t_wardrobeid_i",
                    ":t_wardrobeid_b", ":t_wardrobeid_s", ":t_wear_date", ":t_temperature_max", ":t_temperature_min"),
                    {'t_userid': int(session["user_id"]),
                     't_wardrobeid_c': list_history_wear[column_history_wear['wardrobeid_c'] - num_shift],
                     't_wardrobeid_o': list_history_wear[column_history_wear['wardrobeid_o'] - num_shift],
                     't_wardrobeid_t': list_history_wear[column_history_wear['wardrobeid_t'] - num_shift],
                     't_wardrobeid_i': list_history_wear[column_history_wear['wardrobeid_i'] - num_shift],
                     't_wardrobeid_b': list_history_wear[column_history_wear['wardrobeid_b'] - num_shift],
                     't_wardrobeid_s': list_history_wear[column_history_wear['wardrobeid_s'] - num_shift],
                     't_wear_date'      : list_history_wear[column_history_wear['wear_date'] - num_shift],
                     't_temperature_max': list_history_wear[column_history_wear['temperature_max'] - num_shift],
                     't_temperature_min': list_history_wear[column_history_wear['temperature_min'] - num_shift]
                    })
    connection.commit() # DB commit

    return redirect("/") # Redirect user to home page

@app.route("/catalogcloth", methods=["GET"])
@login_required
def catalogcloth():
    """Edit about user's cloth"""
    # User reached route via GET (as by clicking a link or via redirect)
    if not request.method == "POST":
        # return render_template("catalogcloth.html")
        pass
    # User reached route via POST (as by submitting a form via POST)
    else:
        pass

    # Generate message where user is from
    if session["pagefrom"] == None:
        message = ''
    elif session["pagefrom"] == "addedcloth":
        message = '新たな服を登録しました'
        message = 'New Wardrobe has been registered.'
    elif session["pagefrom"] == "editedcloth":
        message = '服の情報を変更しました'
        message = 'Wardrobe information has been changed.'
    elif session["pagefrom"] == "deletedcloth":
        message = '服の削除が完了しました'
        message = 'Wardrobe has been deleted.'
    else:
        message = ''
    # Forget any pagefrom
    session["pagefrom"] = ""
    # Forget which wardrobe has selected
    session["wardrobe_id"]   = ""
    session["wardrobe_info"] = ""

    # DB connection and cursor generation
    connection = sqlite3.connect(dbpath)
    # connection.isolation_level = None # 自動コミットにする場合は下記を指定（コメントアウトを解除のこと）
    cursor = connection.cursor()

    # Delete all temporary wardrobe-image file
    shutil.rmtree(os.path.join(image_path, str(session["user_id"]), temp_directory))
    os.mkdir(os.path.join(image_path, str(session["user_id"]), temp_directory))

    # Select DB for wardrobes
    cursor.execute("SELECT * FROM wardrobes WHERE NOT inuse = :t_inuse AND userid = :t_userid",
                        {'t_inuse' : 0,
                         't_userid': session["user_id"]
                        })
    rows = cursor.fetchall()
    # List up Catalog Cloth
    list_cloth = []
    for i in rows:
        list_cloth.append({"id": i[column_wardrobes["id"]],
                           "name": i[column_wardrobes["wardrobename"]],
                           "warmscore": i[column_wardrobes["warmscore"]],
                           "img_url": os.path.join("..", image_path, str(session["user_id"]), "{}.jpg".format(i[column_wardrobes["wardrobename"]]))
                          })
    # Forget which page user is in now (for ajax)
    session["nowpage"] = ""

    return render_template("catalogcloth.html", message=message, clothes=list_cloth)

@app.route("/addcloth", methods=["GET"])
@login_required
def addcloth():
    """Add cloth to DB"""
    # User reached route via GET (as by clicking a link or via redirect)
    if not request.method == "POST":
        # Generate dictionary and list for "select" tag
        dict_category   = category_dictionary()
        list_sleeve     = sleeve_list()
        dict_color      = color_dictionary()
        return render_template("addcloth.html", categories=dict_category, sleeves=list_sleeve, colors=dict_color.keys())

    # User reached route via POST (as by submitting a form via POST)
    else:
        return apology("POST is forbidden.")

@app.route("/checkcloth", methods=["POST"])
@login_required
def checkcloth():
    """Check cloth on DB"""

    # DB connection and cursor generation
    connection = sqlite3.connect(dbpath)
    # connection.isolation_level = None # 自動コミットにする場合は下記を指定（コメントアウトを解除のこと）
    cursor = connection.cursor()

    # alert message
    return_json = {
        'message': ''
    }

    if session["nowpage"] == "recommend": # If user is in "recommend.html",
        # Declare variable
        wardrobename_c = str(request.form.get("wardrobename_c"))
        wardrobename_o = str(request.form.get("wardrobename_o"))
        wardrobename_t = str(request.form.get("wardrobename_t"))
        wardrobename_i = str(request.form.get("wardrobename_i"))
        wardrobename_b = str(request.form.get("wardrobename_b"))
        wardrobename_s = str(request.form.get("wardrobename_s"))

        # Exception handling
        num_empty = 0
        if wardrobename_c == "--Select Coat--":
            return_json['message'] = "Coat category is invalid"
            num_empty += 1
        if wardrobename_o == "--Select Outer--" or wardrobename_o == wardrobename_c:
            return_json['message'] = "Outer category is invalid"
            num_empty += 1
        if wardrobename_t == "--Select Tops--":
            return_json['message'] = "Tops category is invalid"
            num_empty += 1
        if wardrobename_i == "--Select Inner--":
            return_json['message'] = "Inner category is invalid"
            num_empty += 1
        if wardrobename_b == "--Select Bottoms--":
            return_json['message'] = "Bottoms category is invalid"
            num_empty += 1
        if wardrobename_s == "--Select Spats--" or wardrobename_s == wardrobename_b:
            return_json['message'] = "Spats category is invalid"
            num_empty += 1
        
        # e = jsonify(json.dumps(return_json));
        # jsonファイルにフォーマットする。
        if num_empty == 6: # If there is invalid input,
            return jsonify(ResultSet=return_json), 400 # Return error code

    elif session["nowpage"] == "": # If user is not in "recommend.html",
        # Select DB for wardrobes
        cursor.execute("SELECT * FROM wardrobes WHERE wardrobename = :wardrobename AND userid = :userid",
                        {'wardrobename': request.form.get("wardrobename"),
                         'userid'      : session["user_id"]
                        })
        checkname = cursor.fetchall()
        wardrobename = request.form.get("wardrobename")
        category     = request.form.get("category")
        sleeve       = request.form.get("sleeve")
        color        = request.form.get("color")
        warmscore    = int(request.form.get("warmscore"))
        freq_inweek  = int(request.form.get("freq_inweek"))

        # Exception handling
        if len(checkname) > 0: # If same wardrobe-name,
            if session["wardrobe_info"] == "": # If session["wardrobe_info"] is empty (If in the case of addcloth) ,
                return_json['message'] = "wardrobename is taken"
            else: # (If in the case of editcloth)
                # If wardrobe-id from checkname is same as edited wardrobe-id ,
                if checkname[0][column_wardrobes["id"]] == session["wardrobe_info"]["wardrobe_id"]:
                    pass
                # If they are different,
                else:
                    return_json['message'] = "wardrobename is taken"
        if category == "--Select Category--":
            return_json['message'] = "category is invalid"
        if sleeve == "--Select Sleeve--":
            return_json['message'] = "sleeve is invalid"
        if color == "--Select Color--":
            return_json['message'] = "color is invalid"
        if warmscore < 1 or warmscore > 9:
            return_json['message'] = "warmscore is invalid"
        if freq_inweek < 1 or freq_inweek > 7:
            return_json['message'] = "freq_inweek is invalid"

        # e = jsonify(json.dumps(return_json));
        # jsonファイルにフォーマットする。
        if return_json["message"] != "": # If there is invalid input,
            return jsonify(ResultSet=return_json), 400 # Return error code

    return jsonify(ResultSet=return_json), 200

@app.route("/addedcloth", methods=["POST"])
@login_required
def addedcloth():
    """Add cloth to DB"""
    # User reached route via GET (as by clicking a link or via redirect)
    if not request.method == "POST":
        return render_template("editcloth.html")

    # User reached route via POST (as by submitting a form via POST)
    else:
        # DB connection and cursor generation
        connection = sqlite3.connect(dbpath)
        # connection.isolation_level = None # 自動コミットにする場合は下記を指定（コメントアウトを解除のこと）
        cursor = connection.cursor()

        # Select DB for wardrobes
        cursor.execute("SELECT * FROM wardrobes WHERE wardrobename = :wardrobename AND userid = :userid",
                        {'wardrobename': request.form.get("wardrobename"),
                         'userid'      : session["user_id"]
                        })
        checkname = cursor.fetchall()
        wardrobename = request.form.get("wardrobename")
        category     = request.form.get("category")
        sleeve       = request.form.get("sleeve")
        color        = request.form.get("color")
        warmscore    = int(request.form.get("warmscore"))
        freq_inweek  = int(request.form.get("freq_inweek"))

        # Exception handling
        if len(checkname) > 0:
            return redirect("/") # Wardrobename is taken
        if category == "--Select Category--":
            return redirect("/") # category is invalid
        if sleeve == "--Select Sleeve--":
            return redirect("/") # sleeve is invalid
        if color == "--Select Color--":
            return redirect("/") # color is invalid
        if warmscore < 1 or warmscore > 9:
            return redirect("/") # warmscore is invalid
        if freq_inweek < 1 or freq_inweek > 7:
            return redirect("/") # freq_inweek is invalid

        # Insert DB for wardrobes
        cursor.execute("INSERT INTO wardrobes(wardrobename, userid, category, sleeve, color, warmscore, freq_inweek, inuse) VALUES (:t_wardrobename, :t_userid, :t_category, :t_sleeve, :t_color, :t_warmscore, :t_freq_inweek, :t_inuse);",
                        {'t_wardrobename': wardrobename,
                         't_userid'      : session["user_id"],
                         't_category'    : category,
                         't_sleeve'      : sleeve,
                         't_color'       : color,
                         't_warmscore'   : warmscore,
                         't_freq_inweek' : freq_inweek,
                         't_inuse': 1
                        })
        # Select DB for wardrobes
        cursor.execute("SELECT id FROM wardrobes WHERE wardrobename = :t_wardrobename AND userid = :t_userid;",
                        {'t_wardrobename': wardrobename,
                         't_userid'      : session["user_id"]
                        })
        # Get the wardrobe_id registered now.
        w_id = int(cursor.fetchone()[column_wardrobes["id"]])

        # Get today as string value
        regist_date = str(datetime.datetime.now().date())
        # Insert DB for history
        cursor.execute("INSERT INTO history_own(wardrobeid, date_from, date_to) VALUES (:t_wardrobeid, :t_from, :t_to);",
                        {'t_wardrobeid': w_id,
                         't_from'      : regist_date,
                         't_to'        : "ongoing"
                        })
        connection.commit() # DB commit

        # Put image in the folder
        im_path = os.path.join(image_path, str(session["user_id"])) # "wardrobe_image" folder
        im_file = request.files['image']                            # Get image file from "file" tag
        save_image(im_file, im_path, '{}.jpg'.format(wardrobename), alt_path)

        # Remember which page user has come from
        session["pagefrom"] = "addedcloth"
        return redirect("/catalogcloth")

@app.route("/editcloth", methods=["GET", "POST"])
@login_required
def editcloth():
    """Edit about user's cloth"""
    # DB connection and cursor generation
    connection = sqlite3.connect(dbpath)
    # connection.isolation_level = None # 自動コミットにする場合は下記を指定（コメントアウトを解除のこと）
    cursor = connection.cursor()

    # User reached route via GET (as by clicking a link or via redirect)
    if not request.method == "POST":
        # Select DB for wardrobes
        cursor.execute("SELECT * FROM wardrobes WHERE id = :t_wardrobeid",
                        {'t_wardrobeid': session["wardrobe_info"]["wardrobe_id"]
                        })
        # Delete temp image from the folder
        temp_im_file = os.path.join(image_path, str(session["user_id"]), temp_directory, '{}.jpg'.format(session["wardrobe_info"]["wardrobe_name"]))
        if os.path.exists(temp_im_file):
            os.remove(temp_im_file)

    # User reached route via POST (as by submitting a form via POST)
    else:
        # Select DB for wardrobes
        cursor.execute("SELECT * FROM wardrobes WHERE id = :t_wardrobeid",
                        {'t_wardrobeid': request.form.get("wardrobeid")
                        })
    tuple_row = cursor.fetchone()
    if len(tuple_row) == 0:
        return redirect("/") # URL直打ちすんなよ

    # Get wardrobe infomation
    wardrobe_image       = "imageimage"
    wardrobe_name        = tuple_row[column_wardrobes["wardrobename"]]
    wardrobe_category    = tuple_row[column_wardrobes["category"]]
    wardrobe_sleeve      = tuple_row[column_wardrobes["sleeve"]]
    wardrobe_color       = tuple_row[column_wardrobes["color"]]
    wardrobe_warmscore   = int(tuple_row[column_wardrobes["warmscore"]])
    wardrobe_freq_inweek = int(tuple_row[column_wardrobes["freq_inweek"]])

    # Generate tag for name, warmscore and freq_inweek (no need)
    # tag_name        = Markup('<input autocomplete="off" autofocus class="form-control" name="wardrobename" placeholder="Wardrobe name" type="text" value="{}" required>'.format(wardrobe_name))
    # tag_warmscore   = Markup('<input type="range" class="custom-range" min="1" max="9" step="1" value="{}" id="warmscore" name="warmscore">'.format(wardrobe_warmscore))
    # tag_freq_inweek = Markup('<input type="range" class="custom-range" min="1" max="7" step="1" value="{}" id="freq_inweek" name="freq_inweek">'.format(wardrobe_freq_inweek))

    # Generate dictionary
    dict_wardrobeinfo = {"wardrobe_name": wardrobe_name, "wardrobe_category": wardrobe_category,
                         "wardrobe_sleeve": wardrobe_sleeve, "wardrobe_color": wardrobe_color,
                         "wardrobe_warmscore": wardrobe_warmscore, "wardrobe_freq_inweek": wardrobe_freq_inweek,
                         "wardrobe_img_url": os.path.join("..", image_path, str(session["user_id"], ), "{}.jpg".format(wardrobe_name))
                        }

    # Generate dictionary and list for "select" tag
    dict_category   = category_dictionary()
    list_sleeve     = sleeve_list()
    dict_color      = color_dictionary()

    # Remember which wardrobe has selected
    session["wardrobe_info"] = {"wardrobe_id": int(tuple_row[column_wardrobes["id"]]),
                                "wardrobe_name": wardrobe_name,
                                "wardrobe_category": wardrobe_category,
                                "wardrobe_sleeve": wardrobe_sleeve,
                                "wardrobe_color": wardrobe_color,
                                "wardrobe_warmscore": wardrobe_warmscore,
                                "wardrobe_freq_inweek": wardrobe_freq_inweek
                               }

    return render_template("editcloth.html", info=dict_wardrobeinfo, categories=dict_category, sleeves=list_sleeve, colors=dict_color.keys())

@app.route("/editingcloth", methods=["POST"])
@login_required
def editingcloth():
    """Edit about user's cloth"""
    # User reached route via GET (as by clicking a link or via redirect)
    if not request.method == "POST":
        return render_template("editcloth.html")
    # User reached route via POST (as by submitting a form via POST)
    else:
        # DB connection and cursor generation
        connection = sqlite3.connect(dbpath)
        # connection.isolation_level = None # 自動コミットにする場合は下記を指定（コメントアウトを解除のこと）
        cursor = connection.cursor()

        # Select DB for wardrobes
        cursor.execute("SELECT * FROM wardrobes WHERE wardrobename = :t_wardrobename AND NOT id = :t_wardrobeid",
                        {'t_wardrobename': request.form.get("wardrobename"),
                         't_wardrobeid': int(session["wardrobe_info"]["wardrobe_id"])
                        })
        checkname = cursor.fetchall()
        # Exception handling
        if len(checkname) > 0:
            return redirect("/") # Wardrobename is taken

        message = "Would you like to edit this cloth with these values?"

        # Generate "wardrobename" variable because of flequenting
        wardrobename = request.form.get("wardrobename")

        # Put image in the folder
        im_path = os.path.join(image_path, str(session["user_id"])) # "wardrobe_image" folder
        im_file = request.files['image']                            # Get image file from "file" tag
        temp_im_path = os.path.join(im_path, temp_directory)        # Folder for temporary wardrobe-images
        save_image(im_file, temp_im_path, '{}.jpg'.format(wardrobename), alt_path, True)

        # "wardrobe_img_url" varies whether generate temporary wardrobe-image file
        if im_file.filename == '':
            if wardrobename == str(session["wardrobe_info"]["wardrobe_name"]):  # if wardrobename is NOT changed
                wardrobe_img_url = os.path.join("..", image_path, str(session["user_id"]), "{}.jpg".format(wardrobename))
            else: # if wardrobename is changed,
                wardrobe_img_url = os.path.join("..", image_path, str(session["user_id"]), "{}.jpg".format(str(session["wardrobe_info"]["wardrobe_name"])))
                session["formaer_wardrobename"] = str(session["wardrobe_info"]["wardrobe_name"])
        else:
            wardrobe_img_url = os.path.join("..", image_path, str(session["user_id"]), temp_directory, "{}.jpg".format(wardrobename))

        # Generate dictionary
        dict_wardrobeinfo = {"wardrobe_name": wardrobename,
                             "wardrobe_category": request.form.get("category"),
                             "wardrobe_sleeve": request.form.get("sleeve"),
                             "wardrobe_color": request.form.get("color"),
                             "wardrobe_warmscore": int(request.form.get("warmscore")),
                             "wardrobe_freq_inweek": int(request.form.get("freq_inweek")),
                             "wardrobe_img_url": wardrobe_img_url
                            }

        # Temporary staging
        temp_id = int(session["wardrobe_info"]["wardrobe_id"])
        # Remember which wardrobe has selected
        session["wardrobe_info"] = {"wardrobe_id": temp_id,
                                    "wardrobe_name": dict_wardrobeinfo["wardrobe_name"],
                                    "wardrobe_category": dict_wardrobeinfo["wardrobe_category"],
                                    "wardrobe_sleeve": dict_wardrobeinfo["wardrobe_sleeve"],
                                    "wardrobe_color": dict_wardrobeinfo["wardrobe_color"],
                                    "wardrobe_warmscore": dict_wardrobeinfo["wardrobe_warmscore"],
                                    "wardrobe_freq_inweek": dict_wardrobeinfo["wardrobe_freq_inweek"]
                                   }

        return render_template("editingcloth.html", message=message, info=dict_wardrobeinfo)

@app.route("/editedcloth", methods=["POST"])
@login_required
def editedcloth():
    """Edit about user's cloth"""
    # User reached route via GET (as by clicking a link or via redirect)
    if not request.method == "POST":
        return render_template("editcloth.html")
    # User reached route via POST (as by submitting a form via POST)
    else:
        # DB connection and cursor generation
        connection = sqlite3.connect(dbpath)
        # connection.isolation_level = None # 自動コミットにする場合は下記を指定（コメントアウトを解除のこと）
        cursor = connection.cursor()
        # Select DB for wardrobes
        cursor.execute("SELECT * FROM wardrobes WHERE userid = :t_userid and wardrobename = :t_wardrobename",
                      {'t_userid': session["user_id"],
                       't_wardrobename': request.form.get("wardrobename")
                      })
        rows = cursor.fetchall()

        # Get entried value
        wardrobename = session["wardrobe_info"]["wardrobe_name"]
        category     = session["wardrobe_info"]["wardrobe_category"]
        sleeve       = session["wardrobe_info"]["wardrobe_sleeve"]
        color        = session["wardrobe_info"]["wardrobe_color"]
        warmscore    = int(session["wardrobe_info"]["wardrobe_warmscore"])
        freq_inweek  = int(session["wardrobe_info"]["wardrobe_freq_inweek"])
        # Update DB for wardrobes
        cursor.execute("UPDATE wardrobes SET wardrobename = :t_wardrobename, category = :t_category, sleeve = :t_sleeve, color = :t_color, warmscore = :t_warmscore, freq_inweek = :t_freq_inweek WHERE id = :t_id",
                        {'t_wardrobename': wardrobename,
                         't_category'    : category,
                         't_sleeve'      : sleeve,
                         't_color'       : color,
                         't_warmscore'   : warmscore,
                         't_freq_inweek' : freq_inweek,
                         't_id'          : session["wardrobe_info"]["wardrobe_id"]
                        })
        connection.commit() # DB commit

        # Copy temporary image-file to genuine image-file
        im_path = os.path.join(image_path, str(session["user_id"])) # "wardrobe_image" folder
        temp_im_path = os.path.join(im_path, temp_directory)        # Folder for temporary wardrobe-images
        im_filename = '{}.jpg'.format(session["wardrobe_info"]["wardrobe_name"]) # File name of wardrobe-image
        if os.path.exists(os.path.join(temp_im_path, im_filename)): # If temporary wardrobe-image file exists,
            shutil.copyfile(os.path.join(temp_im_path, im_filename), os.path.join(im_path, im_filename)) # Duplicate image file
        else:
            # Change image-file's name if wardrobename is changed and
            if wardrobename != session["formaer_wardrobename"]:
                # Rename image-file's name
                os.rename(os.path.join(im_path, '{}.jpg'.format(str(session["formaer_wardrobename"]))), os.path.join(im_path, im_filename))
                session["formaer_wardrobename"] == "" # Blank session variable
        # Remember which page user has come from
        session["pagefrom"] = "editedcloth"
        return redirect("/catalogcloth") # Redirect user to home page

@app.route("/deletecloth", methods=["POST"])
@login_required
def deletecloth():
    """Delete cloth from DB"""
    # User reached route via GET (as by clicking a link or via redirect)
    if not request.method == "POST":
        return render_template("deletecloth.html")
    # User reached route via POST (as by submitting a form via POST)
    else:
        # DB connection and cursor generation
        connection = sqlite3.connect(dbpath)
        # connection.isolation_level = None # 自動コミットにする場合は下記を指定（コメントアウトを解除のこと）
        cursor = connection.cursor()

        # Select DB for wardrobes
        cursor.execute("SELECT * FROM wardrobes WHERE id = :t_id",
                        {'t_id': request.form.get("wardrobeid")
                        })
        tuple_row = cursor.fetchone()
        wardrobe_name     = tuple_row[column_wardrobes["wardrobename"]]
        wardrobe_category = tuple_row[column_wardrobes["category"]]
        wardrobe_img_url  = os.path.join("..", image_path, str(session["user_id"], ), "{}.jpg".format(wardrobe_name))

        message = "Would you like to delete this wardrobe?"
        # Remember which wardrobe has selected
        session["wardrobe_id"] = int(tuple_row[column_wardrobes["id"]])

        return render_template("deletecloth.html", message=message, wardrobe_img_url=wardrobe_img_url, wardrobe_name=wardrobe_name, wardrobe_category=wardrobe_category)

@app.route("/deletedcloth", methods=["POST"])
@login_required
def deletedcloth():
    """Delete cloth from DB"""
    # User reached route via GET (as by clicking a link or via redirect)
    if not request.method == "POST":
        return render_template("editcloth.html")
    # User reached route via POST (as by submitting a form via POST)
    else:
        # DB connection and cursor generation
        connection = sqlite3.connect(dbpath)
        # connection.isolation_level = None # 自動コミットにする場合は下記を指定（コメントアウトを解除のこと）
        cursor = connection.cursor()
        # DB update wardrobes
        cursor.execute("UPDATE wardrobes SET inuse=:t_inuse WHERE id=:t_id",
                        {'t_inuse': 0,
                         't_id'   : int(session["wardrobe_id"])
                        })

        # Get today as string value
        delete_date = str(datetime.datetime.now().date())
        # DB update history
        cursor.execute("UPDATE history_own SET date_to=:t_date WHERE wardrobeid=:t_id",
                        {'t_date': delete_date,
                         't_id'  : int(session["wardrobe_id"])
                        })
        connection.commit() # DB commit

        # Remember which wardrobe has selected
        session["wardrobe_id"] = ""
        # Remember which page user has come from
        session["pagefrom"] = "deletedcloth"
        return redirect("/catalogcloth")

@app.route("/editinguser", methods=["GET", "POST"])
@login_required
def editinguser():
    # User reached route via GET (as by clicking a link or via redirect)
    if not request.method == "POST":
        return redirect("/") # Redirect user to home page
    # User reached route via POST (as by submitting a form via POST)
    else:
        return render_template("/editinguser") # Redirect user to home page


@app.route("/edituser", methods=["GET", "POST"])
@login_required
def edituser():
    """Delete cloth from DB"""
    # User reached route via GET (as by clicking a link or via redirect)
    if not request.method == "POST":
        return redirect("/") # Redirect user to home page
    # User reached route via POST (as by submitting a form via POST)
    else:
        # DB connection and cursor generation
        connection = sqlite3.connect(dbpath)
        # connection.isolation_level = None # 自動コミットにする場合は下記を指定（コメントアウトを解除のこと）
        cursor = connection.cursor()
        # Query DB for wardrobes
        cursor.execute("SELECT * FROM wardrobes WHERE id = :t_id",
                        {'t_id': 'いじったID'

                        })
        rows = cursor.fetchall()
        # Query DB for users
        cursor.execute("UPDATE users SET :parameter=:t_value WHERE id=:t_id",
                        {'parameter': 'いじったパラメータ',
                         't_value': '新しい値',
                         't_id': session["user_id"]
                        })
        return redirect("/") # Redirect user to home page
