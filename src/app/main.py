import cPickle
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from flask import Flask, request, render_template
from app import app
from app.models import *
from app.pclass import *
import json
import requests
import sys
import os

sys.dont_write_bytecode = True

@app.route('/', methods = ['GET', 'POST'])
def index():

    player_names, form, cost, fwds, mids, defs, gk = get_players()
    count = len(player_names)
    return render_template('index.html', player_names=player_names, form=form, cost=cost, count=count, fwds=fwds, mids=mids, defs=defs, gk=gk)

def get_players():

#    team = []
    fignum = 1
    current_path = os.getcwd()

    all_players = cPickle.load(open(current_path + "/app/players.data.pickle"))

    player_names = [(players["first_name"] + " " + players["second_name"]) for players in all_players["elements"] if players["status"] != "i"]
    form = [(float(players["form"])) for players in all_players["elements"] if players["status"] != "i"]
    cost = [(players["now_cost"]) for players in all_players["elements"] if players["status"] != "i"]
    position = [(players["element_type"]) for players in all_players["elements"] if players["status"] != "i"]

    length = len(player_names)
    player_arr = []             # List to hold form and cost for every player
    position_arr = []           # List to hold position and form for every player
    p_class_arr = []            # List to hold players in class form
    for i in range(length):
        player_arr.append([cost[i], form[i], position[i]])
        position_arr.append([position[i], form[i]])
        p_class_arr.append(Player(player_names[i], form[i], cost[i], position[i]))


    k_means_matrix = np.array(player_arr, dtype=float)
    position_form_matrix = np.array(position_arr, dtype=float)
    y_pred = KMeans(n_clusters= 4, init='k-means++', random_state=0, n_init=100).fit_predict(k_means_matrix)
    pos_form_labels = KMeans(n_clusters=3, init='k-means++', random_state=0, n_init=100).fit_predict(position_form_matrix)
    fig = plt.figure(fignum, figsize=(9, 6))
    ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
    ax.scatter(k_means_matrix[:,0], k_means_matrix[:,1], k_means_matrix[:,2], c=y_pred)
    plt.savefig("clustertest.png")
    plt.close()
    plt.scatter(position_form_matrix[:,0], position_form_matrix[:,1], c=pos_form_labels)
    plt.savefig("pos_form.png")
    plt.close()

    return pick_team(p_class_arr, player_names, form, cost)
    #return player_names, form, cost, position

def pick_team(p_class, player_names, form, cost):
    extra_cash = 0
    gks = []
    defs = []
    mids = []
    fwds = []

    for i in range(len(p_class)):
        if p_class[i].get_position() == 1:
            gks.append(p_class[i])
        elif p_class[i].get_position() == 2:
            defs.append(p_class[i])
        elif p_class[i].get_position() == 3:
            mids.append(p_class[i])
        else:
            fwds.append(p_class[i])

    fin_fwds, extra_cash = pick_players(fwds, 330, 2)
    fin_mids, extra_cash = pick_players(mids, 330+extra_cash, 4)
    fin_defs, extra_cash = pick_players(defs, 330+extra_cash, 4)
    fin_gk, extra_cash = pick_players(gks, extra_cash, 1)

    return player_names, form, cost, fin_fwds, fin_mids, fin_defs, fin_gk

def pick_players(players, budget, count):
    sort_by_form = sorted(players, key=lambda x:x.form, reverse=True)
    fin_arr = []
    for i in range(len(players)):
        if count == 0:
            break
        elif budget - sort_by_form[i].get_cost() < 0:
            continue
        else:
            budget = budget - sort_by_form[i].get_cost()
            fin_arr.append(sort_by_form[i])
            count = count - 1

    return fin_arr, budget
# print all_players["elements"][0]["first_name"] + " " + all_players["elements"][0]["second_name"]


# # This needs to be filled with the Page Access Token that will be provided
# # by the Facebook App that will be created.
#
# PAT = 'EAAZAuhEvzHlYBAKanMoNoBlKF2pZCeLZATKJOFjkcBAn4c0dy9Mb9cjHCP2X9LF5MnvPuU2MWWzUraBFBorYsyURbuVAbh0PioTNFZAqrQZApd7AWLCzylx2OESdL9RxpvbA2BLF94geswWwrOagX8RlZA0tYeCEAz1aZB0ZCTBqZCwZDZD'
#
# temp_sender = "hi"
# temp_user = "hi"
# temp_message = "hi"
#
# @app.route('/', methods=['GET'])
# def handle_verification():
#   if request.args.get('hub.verify_token', '') == 'my_voice_is_my_password_verify_me':
#     return request.args.get('hub.challenge', '')
#   else:
#     return 'Error, wrong validation token'
#
# @app.route('/', methods=['POST'])
# def handle_messages():
#     payload = request.get_data()
#
#     global temp_sender
#     global temp_message
#     global temp_user
#
#     current_state = State.query.filter_by(sid = 1).first()
#
#     if current_state:
#         if current_state.information == "store_user":
#             data = json.loads(payload)
#             message_events = data["entry"][0]["messaging"]
#             for event in message_events:
#               if "message" in event:
#                   temp_sender = event["sender"]["id"]
#                   temp_user = event["message"]["text"]
#             db.session.delete(current_state)
#             db.session.commit()
#             new_state = State("add_user")
#             db.session.add(new_state)
#             db.session.commit()
#             send_message(PAT, temp_sender, "What information would you like to store?".encode('unicode_escape'))
#             return "ok"
#
#         if current_state.information == "add_user":
#             data = json.loads(payload)
#             message_events = data["entry"][0]["messaging"]
#             for event in message_events:
#               if "message" in event:
#                   temp_sender = event["sender"]["id"]
#                   temp_message = event["message"]["text"]
#             add_user_info(current_state)
#             db.session.delete(current_state)
#             db.session.commit()
#             return "ok"
#
#         if current_state.information == "list_user":
#             data = json.loads(payload)
#             message_events = data["entry"][0]["messaging"]
#             for event in message_events:
#               if "message" in event:
#                   temp_sender = event["sender"]["id"]
#                   temp_message = event["message"]["text"]
#             list_user_info(current_state)
#             return "ok"
#
#         if current_state.information == "edit_user":
#             data = json.loads(payload)
#             message_events = data["entry"][0]["messaging"]
#             for event in message_events:
#                 if "message" in event:
#                     temp_sender = event["sender"]["id"]
#                     temp_user = event["message"]["text"]
#             db.session.delete(current_state)
#             db.session.commit()
#             new_state = State("edit_user_info")
#             db.session.add(new_state)
#             db.session.commit()
#             send_message(PAT, temp_sender, "What new information would you like to store".encode('unicode_escape'))
#             return "ok"
#
#         if current_state.information == "edit_user_info":
#             data = json.loads(payload)
#             message_events = data["entry"][0]["messaging"]
#             for event in message_events:
#                 if "message" in event:
#                     temp_sender = event["sender"]["id"]
#                     temp_message = event["message"]["text"]
#             edit_user_info(current_state)
#             db.session.delete(current_state)
#             db.session.commit()
#             return "ok"
#
#     else:
#         messaging_events(payload)
#         return "ok"
#
# def messaging_events(payload):
#   """Generate tuples of (sender_id, message_text) from the
#   provided payload.
#   """
#   global global_flag
#   data = json.loads(payload)
#   message_events = data["entry"][0]["messaging"]
#
#   for event in message_events:
#     if "message" in event:
#         if "Add" in event["message"]["text"]:
#             # ret_message = add_user_info(event["sender"]["id"])
#             new_state = State("store_user")
#             db.session.add(new_state)
#             db.session.commit()
#             send_message(PAT, event["sender"]["id"],"Full name of new entry".encode('unicode_escape'))
#
#         elif "List" in event["message"]["text"]:
#             # ret_message = list_user_info(event["sender"]["id"])
#             new_state = State("list_user")
#             db.session.add(new_state)
#             db.session.commit()
#             send_message(PAT, event["sender"]["id"], "Full name of user".encode('unicode_escape'))
#
#         elif "Edit" in event["message"]["text"]:
#             new_state = State("edit_user")
#             db.session.add(new_state)
#             db.session.commit()
#             send_message(PAT, event["sender"]["id"], "Name of user to edit".encode('unicode_escape'))
#
#         else:
#             send_message(PAT, event["sender"]["id"], "Not a recognized command".encode('unicode_escape'))
#
#
#
# def add_user_info(curr_state):
#
#     global temp_sender
#     global temp_message
#     global temp_user
#
#     user = User.query.filter_by(username = temp_user).first()
#     if (user):
#       db.session.delete(curr_state)
#       db.session.commit()
#
#       send_message(PAT, temp_sender, "User already exists".encode('unicode_escape'))
#       return
#
#     new_user = User(temp_user, temp_message)
#     db.session.add(new_user)
#     db.session.commit()
#     db.session.delete(curr_state)
#     db.session.commit()
#
#     send_message(PAT, temp_sender, "Success".encode('unicode_escape'))
#
# def list_user_info(curr_state):
#
#     global temp_sender
#     global temp_message
#     global information
#
#     user = User.query.filter_by(username = temp_message).first()
#
#     if user:
#       send_message(PAT, temp_sender, user.information.encode("unicode_escape"))
#     else:
#       send_message(PAT, temp_sender, "No such user".encode("unicode_escape"))
#
#     db.session.delete(curr_state)
#     db.session.commit()
#
# def edit_user_info(curr_state):
#
#     global temp_sender
#     global temp_message
#     global temp_user
#
#     user = User.query.filter_by(username = temp_user).first()
#     if (user):
#       user.information = temp_message
#       send_message(PAT, temp_sender, "Success".encode('unicode_escape'))
#       return
#
#     db.session.delete(curr_state)
#     db.session.commit()
#
#     send_message(PAT, temp_sender, "User does not exist".encode('unicode_escape'))
#     return
#
#
# def send_message(token, recipient, text):
#   """Send the message text to recipient with id recipient.
#   """
#
#   r = requests.post("https://graph.facebook.com/v2.6/me/messages",
#     params={"access_token": token},
#     data=json.dumps({
#       "recipient": {"id": recipient},
#       "message": {"text": text.decode('unicode_escape')}
#     }),
#     headers={'Content-type': 'application/json'})
