# from telegram.ext import ConversationHandler, MessageHandler, CallbackQueryHandler
# import os
# import json
# import logging
# import time
# import requests
# from telegram import Update
# from dotenv import load_dotenv
# from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext, Filters
# from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# # Enable logging
# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
# )
# logger = logging.getLogger(__name__)
# JSON_FILE_PATH = 'UserData.json'

# load_dotenv()
# TOKEN = os.getenv('TOKEN') # Replace token to client's token
# user_tokens = {}


# def save_registration_data(context):

#     if os.path.exists(JSON_FILE_PATH):
#         with open(JSON_FILE_PATH, 'r') as file:
#             try:
#                 data = json.load(file)
#             except json.JSONDecodeError as e:
#                 print("JSON decoding error:", str(e))
#                 data = {}
#     else:
#         data = {}
#     data[context.user_data['username']] = {
#         'app_user': context.user_data['UserUID'],
#         'app_username': context.user_data['app_username'],
#         # 'email': context.user_data['email'],
#         'phone': context.user_data['phone'],
#         'token': context.user_data['token'],
#         'auth_token' : context.user_data['auth_token'] if 'auth_token' in context.user_data else '',
#         'Crypto': context.user_data['Crypto'] if 'Crypto' in context.user_data else '0.0',
#         'Winning': context.user_data['Winning'] if 'Winning' in context.user_data else '0.0',
#         'Bonus': context.user_data['Bonus'] if 'Bonus' in context.user_data else '0.0',
#         'RealCash': context.user_data['RealCash'] if 'RealCash' in context.user_data else '0.0',
#         'Coin': context.user_data['Coin'] if 'Coin' in context.user_data else '0'
#     }
#     with open(JSON_FILE_PATH, 'w') as file:
#         json.dump(data, file, indent=4)
#     data[context.user_data['username']] = {
#         'app_user': context.user_data['UserUID'],
#         'app_username': context.user_data['app_username'],
#         # 'email': context.user_data['email'],
#         'phone': context.user_data['phone'],
#         'token': context.user_data['token'],
#         'auth_token' : context.user_data['auth_token'],
#         'Crypto': context.user_data['Crypto'],
#         'Winning': context.user_data['Winning'],
#         'Bonus': context.user_data['Bonus'],
#         'RealCash': context.user_data['RealCash'],
#         'Coin': context.user_data['Coin']
#     }

#     # Write the updated data back to the JSON file
#     with open(JSON_FILE_PATH, 'w') as file:
#         json.dump(data, file, indent=4)


# def start(update: Update, context: CallbackContext) -> None:
#     user = update.effective_user

#      # Check if the user is already logged in
#     if context.user_data.get('is_logged_in', False):
#         update.message.reply_text(f'Hello {user.first_name}. You are already logged in.')
#         return

#     # Check if the welcome message has already been displayed
#     if not context.user_data.get('welcome_message_displayed', False):
#         update.message.reply_text(f'Hello {user.first_name}. Welcome to Sports Fantasy World. '
#                                   f'I\'m here to help you to Create And manage Your Teams, Join Contests, and Win Exciting Prizes')
#         context.user_data['welcome_message_displayed'] = True
#         time.sleep(2)

#     # Ask the user to login or register
#     update.message.reply_text('To get started, please choose one of the following options:'
#                               '\n1. /Login - Login to your account'
#                               '\n2. /Register - Register a new account')



# def twelfthSighUp(phone):

#     url = 'https://fantasy-ci-dev.twelfthman.io/api/v2/Signup'
#     payload = {
#         "IsPlayStoreApp": False,
        
#         "Mobile": phone,
#         "ReferralCode": ""
#     }
#     headers = {'Content-Type': 'application/json',
#                'Host': 'fantasy-ci-dev.twelfthman.io'}

#     response = requests.post(url, data=json.dumps(payload), headers=headers)
#     response_txt = json.loads(response.text.encode('utf8'))
#     return response_txt


# def get_token_from_json(username):
#     if os.path.exists(JSON_FILE_PATH):
#         with open(JSON_FILE_PATH, 'r') as file:
#             data = json.load(file)
#             user_data = data.get(username, {})
#             return user_data.get('token')
#     else:
#         return None


# def twelfthVerifyOTP(username, user_input_otp, context):
#     print("Inside twelfthVerifyOTP function")
#     details = context.user_data
#     token = get_token_from_json(username)
#     url = "https://fantasy-ci-dev.twelfthman.io/api-qa/v2/VerifyOtp"

#     headers = {'Content-Type': 'application/json'  }
#     if token:
#         payload = json.dumps({

#             "AppVersion": "4.4.5",
#             "IsPlayStoreApp": False,
#             "OTP": user_input_otp,
#             "Token": details['token'],
#             "Username": details['phone']
#         })
#         response = requests.request("POST", url, headers=headers, data=payload)
#         return json.loads(response.text.encode('utf8'))
#     else:
#         return {
#             "success": False,
#             "token": None,
#             "message": "User Not Found."
#         }


# def twelfthSighIn(username):

#     url = 'https://fantasy-ci-dev.twelfthman.io/api/v2/Signin'
#     payload = {
#         "Username": username,
#         "IsPlayStoreApp": False,
#     }
#     headers = {'Content-Type': 'application/json'}
#     response = requests.post(url, data=json.dumps(payload), headers=headers)
#     response_txt = json.loads(response.text.encode('utf8'))
    
#     if 'data' in response_txt and response_txt['data'] and response_txt['code'] == 200:
#         return {
#             "success": True,
#             "code": response_txt['code'],
#             "message": response_txt['message'],
#             "token": response_txt['data']['token']
#         }
#     else:
#         return {
#             "success": False,
#             "code": response_txt['code'],
#             "message": response_txt['message'],
#             "token": None
#         }


# def twelfthSighOut(update: Update, context: CallbackContext) -> None:
#     url = 'https://fantasy-ci-dev.twelfthman.io/api/v2/Logout'
#     payload = {}
#     headers = {
#             'Content-Type': 'application/json',
#             'Token': ''
#         }

#     response = requests.post(url, data=json.dumps(payload), headers=headers)
#     response_txt = json.loads(response.text.encode('utf8'))

#     update.message.reply_text(response_txt['message'])


# # def ResendOTP(update: Update, context: CallbackContext) -> None:
# #     url = "https://fantasy-ci-dev.twelfthman.io/api-qa/v2/ResendOtp"

# #     payload = json.dumps({
# #     "Username": "7284906551",
# #     "Req": 1,
# #     "Token": "SkVLVTlTYVE4bjNCOWk5a0FxTFd3S0IwakcvSFZ0VjJqSlVUeitoOVdqTC90SThhUEF3cWNpL1drRTdOTGRuTQ==",
# #     "IsPlayStoreApp": False
# #     })
# #     headers = {
# #     'Content-Type': 'application/json',
# #     
# #     }

# #     response = requests.request("POST", url, headers=headers, data=payload)
# def check_auth_token():
#     pass
# def app_setting():
#     url = 'https://fantasy-ci-dev.twelfthman.io/api/v2/AppSetting'
#     response = requests.get(url)
#     response_text=json.loads(response.text.encode('utf8'))
    
#     return response_text

# # def sports_list(update: Update, context: CallbackContext) -> None:
    
# #     data=app_setting()
# #     game_list = data['data']['SportsList']

# #     # Create an inline keyboard with buttons for each game
# #     keyboard = [
# #         [InlineKeyboardButton(game['Name'], callback_data=str(game['SportsID']))]
# #         for game in game_list
# #     ]
# #     reply_markup = InlineKeyboardMarkup(keyboard)

# #     # Send the list of games to the user
# #     update.message.reply_text('Please select a game:',
# #                               reply_markup=reply_markup)
# #     return SELECT_SPORT

# # def sports_list(update: Update, context: CallbackContext) -> None:
    
# #     data = app_setting()
# #     game_list = data.get('data', {}).get('SportsList', [])  # Ensure 'data' and 'SportsList' keys exist

# #     # Add debug print to check the game_list
# #     print("Game List:", game_list)

# #     # Create an inline keyboard with buttons for each game
# #     keyboard = [
# #         [InlineKeyboardButton(game['Name'], callback_data=str(game['SportsID']))]
# #         for game in game_list
# #     ]
# #     reply_markup = InlineKeyboardMarkup(keyboard)

# #     # Use context.bot.send_message to send the message
# #     context.bot.send_message(
# #         chat_id=update.effective_chat.id,
# #         text='Please select a game:',
# #         reply_markup=reply_markup
# #     )

# #     return SELECT_SPORT

# def sports_list(update: Update, context: CallbackContext) -> None:
#     print("INSIDE SPORTS LIST API")
#     data = app_setting()
#     game_list = data.get('data', {}).get('SportsList', [])

#     keyboard = [
#         [InlineKeyboardButton(game['Name'], callback_data=str(game['SportsID']))]
#         for game in game_list
#         ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     if update.message:
#         update.message.reply_text('Please select a game:', reply_markup=reply_markup)
#     else:
#         context.bot.send_message(
#             chat_id=update.effective_chat.id,
#             text='Please select a game:',
#             reply_markup=reply_markup
#         )

#     return SELECT_SPORT

# def select_sport(update: Update, context: CallbackContext) -> int:
     
#     query = update.callback_query
#     selected_sport_id = query.data
    
#     phone_number = context.user_data["phone"]
#     with open(JSON_FILE_PATH, 'r') as file:
#             try:
#                 data = json.load(file)
#                 for i in data:
#                     if str(i['Phone']) == str(phone_number):
#                         i['SelectedSport'] = selected_sport_id

#             except:
#                 pass
#     query = update.callback_query
#     selected_sport_id = query.data

#     context.user_data['selected_sport_id'] = selected_sport_id
#     return display_static_menu(update, context)

# # def select_sport(update: Update, context: CallbackContext) -> int:
# #     query = update.callback_query
# #     selected_sport_id = query.data

# #     # Store the selected sport ID in user_data
# #     context.user_data['selected_sport'] = selected_sport_id

# #     # query.edit_message_text(
# #     #     f"You have selected sport with ID {selected_sport_id}")
    
# #     # Update the user's record in the JSON file with the selected sport
# #     username = context.user_data.get('login_username')
# #     if username:
# #         update_user_sport(username, selected_sport_id)

# #     # Initiate displaying the match list
# #     return display_matches(update, context)

# # def display_matches(update: Update, context: CallbackContext) -> int:

# #     selected_sport_id = context.user_data.get('selected_sport')
# #     api_response = GetMatcList(selected_sport_id, context)
# #     if api_response:
# #         Tournament = api_response['data']
# #         keyboard = [
# #             [InlineKeyboardButton(game['TournamentName'], callback_data=str(0))]
# #             for game in Tournament
# #         ]
# #         keyboard_columns = [keyboard[i:i + 2] for i in range(0, len(keyboard), 2)]
# #         reply_markup = InlineKeyboardMarkup(keyboard)
# #         if context.user_data.get('selected_sport'):
# #             update.message.reply_text('Please select a game:', reply_markup=reply_markup)
# #         else:
# #             context.bot.send_message(
# #                 chat_id=update.effective_chat.id,
# #                 text='Please select a game:',
# #                 reply_markup=reply_markup
# #             )

# #         if api_response['code'] == 200:
# #             pass
# #         else:
# #             error_message = extract_error_message(api_response)
# #             print("==>>", error_message)
# #             context.bot.send_message(chat_id=update.effective_chat.id, text=error_message)
# #             return ConversationHandler.END
# #     else:
# #         pass
# #     # return SUBMENU_OPTIONS

# def display_matches(update: Update, context: CallbackContext) -> int:

#     api_response = GetMatcList(1, context)
#     print("========GETMATCHLIST/TOURNAMENT LIST")
#     print(api_response)
#     if api_response:
#         Tournament = api_response.get('data', [])
#         keyboard = [
#             [InlineKeyboardButton(game['TournamentName'], callback_data=str(0))]
#             for game in Tournament
#         ]
#         keyboard_columns = [keyboard[i:i + 2] for i in range(0, len(keyboard), 2)]
#         reply_markup = InlineKeyboardMarkup(keyboard)
        
#         # Check if update.message is not None before using it
#         if update.message and update.message.reply_text:
#             update.message.reply_text('Please select a game:', reply_markup=reply_markup)
#         else:
#             # If update.message is None, use context.bot.send_message
#             context.bot.send_message(
#                 chat_id=update.effective_chat.id,
#                 text='Please select a game:',
#                 reply_markup=reply_markup
#             )

#         if api_response['code'] == 200:
#             pass
#         else:
#             error_message = extract_error_message(api_response)
#             print("==>>", error_message)
#             context.bot.send_message(chat_id=update.effective_chat.id, text=error_message)
#             return ConversationHandler.END
#     else:
#         pass
# def GetMatcList(selected_sport_id,context) :

#     url = "https://fantasy-ci-dev.twelfthman.io/api-qa/v2/GetMatchList"
#     payload = json.dumps({
#         "SportsID":selected_sport_id,
#         "WithAdditionalCards": "1"
#         })
#     headers = {
#         'Token': context.user_data['auth_token'],
#         'Content-Type': 'application/json'
#     }
#     response = requests.request("POST", url, headers=headers, data=payload)
#     response_txt = json.loads(response.text.encode('utf8'))
#     return response_txt

# def update_user_sport(username, selected_sport_id):
#     # Load the existing JSON data
#     if os.path.exists(JSON_FILE_PATH):
#         with open(JSON_FILE_PATH, 'r') as file:
#             try:
#                 data = json.load(file)
#             except json.JSONDecodeError as e:
#                 print("JSON decoding error:", str(e))
#                 data = {}
#     else:
#         data = {}

#     if username in data:
#         data[username]['selected_sport'] = selected_sport_id

#     with open(JSON_FILE_PATH, 'w') as file:
#         json.dump(data, file, indent=4)

# def select_match(update: Update, context: CallbackContext)-> int:
    
#     query = update.callback_query
#     selected_sport_id = query.data
#     context.user_data['selected_sport'] = selected_sport_id
#     query.edit_message_text(
#         f"You have selected sport with ID {selected_sport_id}")
#     username = context.user_data.get('login_username')
#     if username:
#         update_user_sport(username, selected_sport_id)
#     return display_matches(update, context)

# #  def twelfthUpcomingMatches(update: Update, context: CallbackContext) ->None:
# #     url="https://fantasy-ci-dev.twelfthman.io/api-qa/v2/GetGameList"

# # def twelfthLogJoinGame(update: Update, context: CallbackContext) ->None:
# #     pass
# def twelfthSignUpValidate(Version,context):
#     print("Inside twelfthSignUpValidate API")
#     url = "https://fantasy-ci-dev.twelfthman.io/api-qa/v2/SignupValidate"

#     payload = json.dumps({
#     "Mobile": context.user_data['phone'],
#     "ReferralCode": "",
#     "OTP": "123456",
#     "Token": context.user_data['token'],
#     "AppVersion": Version
#     })
#     headers = {
#     'Content-Type': 'application/json'
#     }

#     response = requests.request("POST", url, headers=headers, data=payload)
#     response_txt = json.loads(response.text.encode('utf8'))
#     return response_txt
    

# REGISTER_EMAIL, REGISTER_PHONE, VERIFY_OTP, LOGIN_USERNAME = range(4)
# DISPLAY_MATCHES = range(7, 8)

# def register_message(update: Update, context: CallbackContext) -> int:
#     update.message.reply_text('Please provide your phone number (e.g., +91 123456789)')
#     return REGISTER_PHONE


# # def register_email(update: Update, context: CallbackContext) -> int:
#     # context.user_data['email'] = update.message.text
#     # update.message.reply_text(
#     #     'Now, please provide your phone number (e.g., +91 123456789)')
#     # return REGISTER_PHONE


# def register_phone(update: Update, context: CallbackContext) -> int:
#     context.user_data['phone'] = update.message.text
#     user = update.effective_user
#     phone = context.user_data['phone']
#     username = user.username
#     api_response = twelfthSighUp(phone)

#     if api_response['code'] == 200:
#         data=app_setting()
        
#         if data['code']== 200:
#             context.user_data.clear()
#             context.user_data['username'] = username
#             # context.user_data['email'] = email
#             context.user_data['phone'] = phone
#             context.user_data['token'] = api_response['data']['token']
#             Version=data['data']['Android']['newVersionName']
#             signUpValidate=twelfthSignUpValidate(Version,context)

#             context.user_data['auth_token']=signUpValidate['data']['Token']
#             context.user_data['UserUID']=signUpValidate['data']['UserUID']
#             context.user_data['app_username']=signUpValidate['data']['Username']
#             context.user_data['Crypto']=signUpValidate['data']['Crypto']
#             context.user_data['Winning']=signUpValidate['data']['Winning']
#             context.user_data['Bonus']=signUpValidate['data']['Bonus']
#             context.user_data['RealCash']=signUpValidate['data']['RealCash']
#             context.user_data['Coin']=signUpValidate['data']['Coin']
#         save_registration_data(context)
#         update.message.reply_text(api_response['message'])

#         return WAITING_FOR_OTP
#     else:
#         error_message = extract_error_message(api_response)
#         update.message.reply_text(error_message)
#         start(update, context)
#         return ConversationHandler.END


# def extract_error_message(response_data):
#     if 'message' in response_data:
#         if isinstance(response_data['message'], dict):
#             return next(iter(response_data['message'].values()), '')
#         return response_data['message']
#     return response_data.get('message', 'Unknown error')



# # Define new states for the conversation
# LOGIN_USERNAME = 3
# SELECT_SPORT, WAITING_FOR_OTP= range(5, 7)
# SELECT_MATCH  = (5,7)
# SUBMENU_OPTIONS = range(8, 12)

# # ========================================================================================================
# def login_message(update: Update, context: CallbackContext) -> int:
    
#     if context.user_data.get('is_logged_in', False):
#         update.message.reply_text('You are already logged in.')
#         return ConversationHandler.END  # End the conversation

#     update.message.reply_text('Please provide your mobile number:')
#     return LOGIN_USERNAME
    

# def login_username(update: Update, context: CallbackContext) -> int:
#     username = update.message.text
#     context.user_data['login_username'] = username
#     api_response = twelfthSighIn(username)

#     if api_response.get('success', False):
#         update.message.reply_text(api_response['message'])
#         context.user_data.clear()
#         context.user_data['phone'] = username
#         context.user_data['token']= api_response['token']
#         return WAITING_FOR_OTP
#     else:
#         update.message.reply_text(api_response['message'])
#         return ConversationHandler.END


# def waiting_for_otp_input(update: Update, context: CallbackContext) -> int:
#     print("Waiting FOR OTP")
#     user_input_otp = update.message.text
#     if len(user_input_otp) == 6:
#         user = update.effective_user
#         data = twelfthVerifyOTP(user.username, user_input_otp, context)
#         if data['code'] == 200:
#             context.user_data['auth_token'] = data['data']['Token']
#             context.user_data['is_logged_in'] = True
#             update.message.reply_text(data['message'])
#             return sports_list(update, context)
#         else:
#             update.message.reply_text(data['message'])
#             return ConversationHandler.END 
#     #     if data['code'] == 200:
#     #         context.user_data['auth_token'] = data['data']['Token']
#     #         context.user_data['is_logged_in'] = True
#     #         update.message.reply_text(data['message'])
#     #         return sports_list(update, context)
#     #     else:
#     #         update.message.reply_text(f"Invalid OTP. {data['message']}. Please enter the correct OTP.")
#     #         return WAITING_FOR_OTP
#     else:
#         update.message.reply_text(f"Invalid OTP. Please enter the correct OTP.")
#         return WAITING_FOR_OTP

# def display_static_menu(update, context):
#     # menu_list=[{
#     #     "Upcoming Matches":'upcoming_matches',
#     #     "Logout": "logout",
#     #     "Check Wallet Balance": "check_wallet_balance",
#     #     "Recharge Wallet":"recharge_wallet"
#     # }]
#     # keyboard = [
#     #     [InlineKeyboardButton(game['Name'], callback_data=str(game['SportsID']))]
#     #     for game in menu_list
#     # ]
#     menu_buttons = [
#         InlineKeyboardButton("Upcoming Matches", callback_data='upcoming_matches'),
#         InlineKeyboardButton("Logout", callback_data='logout'),
#         InlineKeyboardButton("Check Wallet Balance", callback_data='check_wallet_balance'),
#         InlineKeyboardButton("Recharge Wallet", callback_data='recharge_wallet')
#     ]
#     reply_markup = InlineKeyboardMarkup([menu_buttons])
#     if update.message:
#         update.message.reply_text("Please select:", reply_markup=reply_markup)
#     elif update.callback_query and update.callback_query.message:
#         update.callback_query.message.reply_text("Please select an option from the menu:", reply_markup=reply_markup)
#     else:
#         context.bot.send_message(
#             chat_id=update.effective_chat.id,
#             text="Please select an option from the menu:",
#             reply_markup=reply_markup
#         )
#     return display_submenu(update,context)

# def display_submenu(update: Update, context: CallbackContext) -> int:
#     query = update.callback_query
#     selected_option = query.data
#     # print("selected_option",selected_option)

#     if selected_option == 'upcoming_matches':
#         print("==============================")
#         display_matches(update,context)
#         # return ConversationHandler.END
#     elif selected_option == 'logout':
#         # Handle logout
#         update.message.reply_text("Logging out...")
#         data=twelfthSighOut(update,context)
#         print(data)
#         return ConversationHandler.END
#     elif selected_option == 'check_wallet_balance':
#         # Handle checking wallet balance
#         update.message.reply_text("Checking wallet balance...")
#         return ConversationHandler.END
#     elif selected_option == 'recharge_wallet':
#         # Handle recharging wallet
#         update.message.reply_text("Recharging wallet...")
#         return ConversationHandler.END
#     else:
#         update.message.reply_text("Invalid option selected.")
#         return SUBMENU_OPTIONS

# # ==========ERROR HANDLING=============
# def unknown_command(update, context):
#     command = update.message.text
#     user_id = update.message.from_user.id

#     if command in ["/Login", "/Register"]:
#         logger.error(f"Error: {context.error}")
#         update.message.reply_text("You are already LoggedIn")
        
#         keyboard = [[InlineKeyboardButton("Show Sport Menu", callback_data='show_sport_menu')]]
#         # reply_markup = InlineKeyboardMarkup(keyboard)
#         # update.message.reply_text("Click the button below to show the sport menu:", reply_markup=reply_markup)
#         return button_click(update, context)

#     else:
#         logger.error(f"Error: {context.error}")
#         update.message.reply_text("Sorry, I don't understand that command.")

# def button_click(update, context):
#     # query = update.callback_query
#     # user_id = query.from_user.id
#     return sports_list(update, context)
    
# # ==========MAIN FUNCTION =============
# def main() -> None:
#     updater = Updater(TOKEN, use_context=True)
#     dp = updater.dispatcher

#     # Define the conversation handler with states
#     conv_handler = ConversationHandler(
#         entry_points=[
#             CommandHandler("Register", register_message),
#             CommandHandler("Login", login_message),
#             CommandHandler("twelfthVerifyOTP", twelfthVerifyOTP)
#         ],
#         states={
#             REGISTER_PHONE: [MessageHandler(Filters.text & ~Filters.command, register_phone)],
#             LOGIN_USERNAME: [MessageHandler(Filters.text & ~Filters.command, login_username)],
#             WAITING_FOR_OTP: [MessageHandler(Filters.text & ~Filters.command, waiting_for_otp_input)],
#             SELECT_SPORT: [CallbackQueryHandler(select_sport)],
#             SELECT_MATCH: [CallbackQueryHandler(display_matches)],
#             SUBMENU_OPTIONS: [CallbackQueryHandler(display_submenu)]
#         },
#         fallbacks=[],
#     )

#     dp.add_handler(CommandHandler("start", start))
#     dp.add_handler(CommandHandler("SportsList", sports_list))
#     dp.add_handler(CommandHandler("MatcList", display_matches))
#     dp.add_handler(conv_handler)
#     dp.add_handler(MessageHandler(Filters.text, unknown_command))
#     dp.add_handler(CallbackQueryHandler(button_click))

#     updater.start_polling()
#     updater.idle()
#     # try:
#     #     updater.idle()
#     # except KeyboardInterrupt:
#     #     updater.stop()


# if __name__ == '__main__':
#     main()



from telegram.ext import ConversationHandler, MessageHandler, CallbackQueryHandler
import os
import json
import logging
import time
import requests
from telegram import Update
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
JSON_FILE_PATH = 'user_data.json'

load_dotenv()
TOKEN = os.getenv('TOKEN') # Replace token to client's token
user_tokens = {}


# TOKEN="6836753500:AAEXnRFgGtSF46-bXG8DzB1RI0Yp_VoW0Vs"
updater = Updater(TOKEN, use_context=True)
def save_registration_data(context):

    if os.path.exists(JSON_FILE_PATH):
        with open(JSON_FILE_PATH, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError as e:
                print("JSON decoding error:", str(e))
                data = {}
    else:
        data = {}
    data[context.user_data['phone']] = {
        'app_user': context.user_data['UserUID'],
        'app_username': context.user_data['app_username'],
        # 'email': context.user_data['email'],
        'phone': context.user_data['phone'],
        'token': context.user_data['token'],
        'auth_token' : context.user_data['auth_token'] if 'auth_token' in context.user_data else '',
        'Crypto': context.user_data['Crypto'] if 'Crypto' in context.user_data else '0.0',
        'Winning': context.user_data['Winning'] if 'Winning' in context.user_data else '0.0',
        'Bonus': context.user_data['Bonus'] if 'Bonus' in context.user_data else '0.0',
        'RealCash': context.user_data['RealCash'] if 'RealCash' in context.user_data else '0.0',
        'Coin': context.user_data['Coin'] if 'Coin' in context.user_data else '0'
    }
    with open(JSON_FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4)
    data[context.user_data['username']] = {
        'app_user': context.user_data['UserUID'],
        'app_username': context.user_data['app_username'],
        # 'email': context.user_data['email'],
        'phone': context.user_data['phone'],
        'token': context.user_data['token'],
        'auth_token' : context.user_data['auth_token'],
        'Crypto': context.user_data['Crypto'],
        'Winning': context.user_data['Winning'],
        'Bonus': context.user_data['Bonus'],
        'RealCash': context.user_data['RealCash'],
        'Coin': context.user_data['Coin']
    }

    # Write the updated data back to the JSON file
    with open(JSON_FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4)


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user

     # Check if the user is already logged in
    if context.user_data.get('is_logged_in', False):
        update.message.reply_text(f'Hello {user.first_name}. You are already logged in.')
        return

    # Check if the welcome message has already been displayed
    if not context.user_data.get('welcome_message_displayed', False):
        update.message.reply_text(f'Hello {user.first_name}. Welcome to Sports Fantasy World. '
                                  f'I\'m here to help you to Create And manage Your Teams, Join Contests, and Win Exciting Prizes')
        context.user_data['welcome_message_displayed'] = True
        time.sleep(2)

    # Ask the user to login or register
    update.message.reply_text('To get started, please choose one of the following options:'
                              '\n1. /Login - Login to your account'
                              '\n2. /Register - Register a new account')



def twelfthSighUp(phone):

    url = 'https://fantasy-ci-dev.twelfthman.io/api/v2/Signup'
    payload = {
        "IsPlayStoreApp": False,
        
        "Mobile": phone,
        "ReferralCode": ""
    }
    headers = {'Content-Type': 'application/json',
               'Host': 'fantasy-ci-dev.twelfthman.io'}

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    response_txt = json.loads(response.text.encode('utf8'))
    return response_txt


def get_token_from_json(username):
    if os.path.exists(JSON_FILE_PATH):
        with open(JSON_FILE_PATH, 'r') as file:
            data = json.load(file)
            user_data = data.get(username, {})
            return user_data.get('token')
    else:
        return None


def twelfthVerifyOTP(username, user_input_otp, context):
    print("Inside twelfthVerifyOTP function")
    details = context.user_data
    token = get_token_from_json(username)
    url = "https://fantasy-ci-dev.twelfthman.io/api-qa/v2/VerifyOtp"

    headers = {'Content-Type': 'application/json'  }
    # if token:
    #     payload = json.dumps({

    #         "AppVersion": "4.4.5",
    #         "IsPlayStoreApp": False,
    #         "OTP": user_input_otp,
    #         "Token": details['token'],
    #         "Username": details['phone']
    #     })
    #     response = requests.request("POST", url, headers=headers, data=payload)
    #     return json.loads(response.text.encode('utf8'))
    # else:
    #     return {
    #         "success": False,
    #         "token": None,
    #         "message": "User Not Found."
    #     }
    payload = json.dumps({

            "AppVersion": "4.4.5",
            "IsPlayStoreApp": False,
            "OTP": user_input_otp,
            "Token": details['token'],
            "Username": details['phone']
        })
    response = requests.request("POST", url, headers=headers, data=payload)
    return json.loads(response.text.encode('utf8'))


def twelfthSighIn(username):

    url = 'https://fantasy-ci-dev.twelfthman.io/api/v2/Signin'
    payload = {
        "Username": username,
        "IsPlayStoreApp": False,
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    response_txt = json.loads(response.text.encode('utf8'))
    
    if 'data' in response_txt and response_txt['data'] and response_txt['code'] == 200:
        return {
            "success": True,
            "code": response_txt['code'],
            "message": response_txt['message'],
            "token": response_txt['data']['token']
        }
    else:
        return {
            "success": False,
            "code": response_txt['code'],
            "message": response_txt['message'],
            "token": None
        }


def twelfthSighOut(update: Update, context: CallbackContext) -> None:
    url = 'https://fantasy-ci-dev.twelfthman.io/api/v2/Logout'
    payload = {}
    headers = {
            'Content-Type': 'application/json',
            'Token': context.user_data['auth_token']
        }

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    response_txt = json.loads(response.text.encode('utf8'))
    return response_txt
    # update.message.reply_text(response_txt['message'])


# def ResendOTP(update: Update, context: CallbackContext) -> None:
#     url = "https://fantasy-ci-dev.twelfthman.io/api-qa/v2/ResendOtp"

#     payload = json.dumps({
#     "Username": "7284906551",
#     "Req": 1,
#     "Token": "SkVLVTlTYVE4bjNCOWk5a0FxTFd3S0IwakcvSFZ0VjJqSlVUeitoOVdqTC90SThhUEF3cWNpL1drRTdOTGRuTQ==",
#     "IsPlayStoreApp": False
#     })
#     headers = {
#     'Content-Type': 'application/json',
#     
#     }

#     response = requests.request("POST", url, headers=headers, data=payload)
def check_auth_token():
    pass
def app_setting():
    url = 'https://fantasy-ci-dev.twelfthman.io/api/v2/AppSetting'
    response = requests.get(url)
    response_text=json.loads(response.text.encode('utf8'))
    
    return response_text

# def sports_list(update: Update, context: CallbackContext) -> None:
    
#     data=app_setting()
#     game_list = data['data']['SportsList']

#     # Create an inline keyboard with buttons for each game
#     keyboard = [
#         [InlineKeyboardButton(game['Name'], callback_data=str(game['SportsID']))]
#         for game in game_list
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)

#     # Send the list of games to the user
#     update.message.reply_text('Please select a game:',
#                               reply_markup=reply_markup)
#     return SELECT_SPORT

# def sports_list(update: Update, context: CallbackContext) -> None:
    
#     data = app_setting()
#     game_list = data.get('data', {}).get('SportsList', [])  # Ensure 'data' and 'SportsList' keys exist

#     # Add debug print to check the game_list
#     print("Game List:", game_list)

#     # Create an inline keyboard with buttons for each game
#     keyboard = [
#         [InlineKeyboardButton(game['Name'], callback_data=str(game['SportsID']))]
#         for game in game_list
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)

#     # Use context.bot.send_message to send the message
#     context.bot.send_message(
#         chat_id=update.effective_chat.id,
#         text='Please select a game:',
#         reply_markup=reply_markup
#     )

#     return SELECT_SPORT

def sports_list(update: Update, context: CallbackContext) -> None:
    print("INSIDE SPORTS LIST API")
    data = app_setting()
    game_list = data.get('data', {}).get('SportsList', [])

    keyboard = [
        [InlineKeyboardButton(game['Name'], callback_data=str(game['SportsID']))]
        for game in game_list
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message:
        update.message.reply_text('Please select a game:', reply_markup=reply_markup)
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Please select a game:',
            reply_markup=reply_markup
        )
    return SELECT_SPORT

def select_sport(update: Update, context: CallbackContext) -> int:
     
    query = update.callback_query
    selected_sport_id = query.data
    
    phone_number = context.user_data["phone"]
    with open(JSON_FILE_PATH, 'r+') as file:
            try:
                data = json.load(file)
                for i in data:
                    if str(i['Phone']) == str(phone_number):
                        i['SelectedSport'] = selected_sport_id
            except:
                pass
    query = update.callback_query
    selected_sport_id = query.data

    context.user_data['selected_sport_id'] = selected_sport_id
    return display_static_menu(update, context)

# def display_matches(update: Update, context: CallbackContext) -> int:

#     api_response = GetMatcList(1, context)    
#     if api_response:
#         Tournament = api_response.get('data', [])
#         keyboard = [
#             [InlineKeyboardButton(game['TournamentName']+"-"+game['MaxPrize'], callback_data=str(0))]
#             for game in Tournament
#         ]
#         phone_number = context.user_data["phone"]
#         # with open(JSON_FILE_PATH, 'r') as file:
#         #         try:
#         #             data = json.load(file)
#         #             for i in data:
#         #                 if str(i['Phone']) == str(phone_number):
#         #                     i['SelectedSport'] = selected_sport_id
#         #         except:
#         #             pass
#         keyboard_columns = [keyboard[i:i + 2] for i in range(0, len(keyboard), 2)]
#         reply_markup = InlineKeyboardMarkup(keyboard)
        
#         # Check if update.message is not None before using it
#         if update.message and update.message.reply_text:
#             update.message.reply_text('Please select a game:', reply_markup=reply_markup)
#         else:
#             # If update.message is None, use context.bot.send_message
#             context.bot.send_message(
#                 chat_id=update.effective_chat.id,
#                 text='Please select a game:',
#                 reply_markup=reply_markup
#             )

#         if api_response['code'] == 200:
#             pass
#         else:
#             error_message = extract_error_message(api_response)
#             print("==>>", error_message)
#             context.bot.send_message(chat_id=update.effective_chat.id, text=error_message)
#             return ConversationHandler.END
#     else:
#         pass

def display_matches(update: Update, context: CallbackContext) -> int:
    api_response = GetMatcList(1, context)

    if api_response:
        Tournament = api_response.get('data', [])
        # keyboard = [
        #     [InlineKeyboardButton(game['TournamentName'], callback_data=str(game['GameGroupID']))]
        #     for game in Tournament
        # ]
        keyboard = []
        for game in Tournament:
                if game['GameGroupID'] != "":
                    keyboard.append([InlineKeyboardButton(f"{game['TournamentName']} - {game['MaxPrize']}", callback_data=game['GameGroupID'])])
        phone_number = context.user_data["phone"]

        keyboard_columns = [keyboard[i:i + 2] for i in range(0, len(keyboard), 2)]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if update.message and update.message.reply_text:
            update.message.reply_text('Please select a game:', reply_markup=reply_markup)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Please select a game:',
                reply_markup=reply_markup
            )

        if api_response['code'] == 200:
            pass
        else:
            error_message = extract_error_message(api_response)
            print("==>>", error_message)
            if update.message:
                update.message.reply_text(error_message)
            else:
                # If update.message is None, use context.bot.send_message
                context.bot.send_message(chat_id=update.effective_chat.id, text=error_message)
                return ConversationHandler.END
    else:
        # Handle the case where api_response is None
        print("Error: api_response is None")

    return DISPLAY_MATCHES

def GetMatcList(selected_sport_id,context) :

    url = "https://fantasy-ci-dev.twelfthman.io/api-qa/v2/GetMatchList"
    payload = json.dumps({
        "SportsID":selected_sport_id,
        "WithAdditionalCards": "1"
        })
    headers = {
        'Token': context.user_data['auth_token'],
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    response_txt = json.loads(response.text.encode('utf8'))
    return response_txt

def update_user_sport(username, selected_sport_id):
    # Load the existing JSON data
    if os.path.exists(JSON_FILE_PATH):
        with open(JSON_FILE_PATH, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError as e:
                print("JSON decoding error:", str(e))
                data = {}
    else:
        data = {}

    if username in data:
        data[username]['selected_sport'] = selected_sport_id

    with open(JSON_FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4)

def select_match(update: Update, context: CallbackContext)-> int:
    
    query = update.callback_query
    selected_sport_id = query.data
    context.user_data['selected_sport'] = selected_sport_id
    query.edit_message_text(
        f"You have selected sport with ID {selected_sport_id}")
    username = context.user_data.get('login_username')
    if username:
        update_user_sport(username, selected_sport_id)
    return display_matches(update, context)

#  def twelfthUpcomingMatches(update: Update, context: CallbackContext) ->None:
#     url="https://fantasy-ci-dev.twelfthman.io/api-qa/v2/GetGameList"

# def twelfthLogJoinGame(update: Update, context: CallbackContext) ->None:
#     pass
def twelfthSignUpValidate(Version,context):
    print("Inside twelfthSignUpValidate API")
    url = "https://fantasy-ci-dev.twelfthman.io/api-qa/v2/SignupValidate"

    payload = json.dumps({
    "Mobile": context.user_data['phone'],
    "ReferralCode": "",
    "OTP": "123456",
    "Token": context.user_data['token'],
    "AppVersion": Version
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response_txt = json.loads(response.text.encode('utf8'))
    return response_txt
    

REGISTER_EMAIL, REGISTER_PHONE, VERIFY_OTP, LOGIN_USERNAME = range(4)
DISPLAY_MATCHES = range(7, 8)

def register_message(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Please provide your phone number (e.g., +91 123456789)')
    return REGISTER_PHONE


# def register_email(update: Update, context: CallbackContext) -> int:
    # context.user_data['email'] = update.message.text
    # update.message.reply_text(
    #     'Now, please provide your phone number (e.g., +91 123456789)')
    # return REGISTER_PHONE


def register_phone(update: Update, context: CallbackContext) -> int:
    context.user_data['phone'] = update.message.text
    user = update.effective_user
    phone = context.user_data['phone']
    username = user.username
    api_response = twelfthSighUp(phone)

    if api_response['code'] == 200:
        data=app_setting()
        
        if data['code']== 200:
            context.user_data.clear()
            context.user_data['username'] = username
            # context.user_data['email'] = email
            context.user_data['phone'] = phone
            context.user_data['token'] = api_response['data']['token']
            Version=data['data']['Android']['newVersionName']
            signUpValidate=twelfthSignUpValidate(Version,context)

            context.user_data['auth_token']=signUpValidate['data']['Token']
            context.user_data['UserUID']=signUpValidate['data']['UserUID']
            context.user_data['app_username']=signUpValidate['data']['Username']
            context.user_data['Crypto']=signUpValidate['data']['Crypto']
            context.user_data['Winning']=signUpValidate['data']['Winning']
            context.user_data['Bonus']=signUpValidate['data']['Bonus']
            context.user_data['RealCash']=signUpValidate['data']['RealCash']
            context.user_data['Coin']=signUpValidate['data']['Coin']
        save_registration_data(context)
        update.message.reply_text(api_response['message'])

        return WAITING_FOR_OTP
    else:
        error_message = extract_error_message(api_response)
        update.message.reply_text(error_message)
        start(update, context)
        return ConversationHandler.END


def extract_error_message(response_data):
    if 'message' in response_data:
        if isinstance(response_data['message'], dict):
            return next(iter(response_data['message'].values()), '')
        return response_data['message']
    return response_data.get('message', 'Unknown error')



# Define new states for the conversation
LOGIN_USERNAME = 3
SELECT_SPORT, WAITING_FOR_OTP= range(5, 7)
SELECT_MATCH  = (5,7)
SUBMENU_OPTIONS = range(8, 12)

# ========================================================================================================
def login_message(update: Update, context: CallbackContext) -> int:
    
    if context.user_data.get('is_logged_in', False):
        update.message.reply_text('You are already logged in.')
        return ConversationHandler.END  # End the conversation

    update.message.reply_text('Please provide your mobile number:')
    return LOGIN_USERNAME
    

def login_username(update: Update, context: CallbackContext) -> int:
    username = update.message.text
    context.user_data['login_username'] = username
    api_response = twelfthSighIn(username)

    if api_response.get('success', False):
        update.message.reply_text(api_response['message'])
        context.user_data.clear()
        context.user_data['phone'] = username
        context.user_data['token']= api_response['token']
        return WAITING_FOR_OTP
    else:
        update.message.reply_text(api_response['message'])
        return ConversationHandler.END


def waiting_for_otp_input(update: Update, context: CallbackContext) -> int:
    print("Waiting FOR OTP")
    user_input_otp = update.message.text
    if len(user_input_otp) == 6:
        user = update.effective_user
        data = twelfthVerifyOTP(user.username, user_input_otp, context)
        print(data)
        if data['code'] == 200:
            context.user_data['auth_token'] = data['data']['Token']
            context.user_data['is_logged_in'] = True
            update.message.reply_text(data['message'])
            return sports_list(update, context)
        else:
            update.message.reply_text(data['message'])
            return ConversationHandler.END 
    #     if data['code'] == 200:
    #         context.user_data['auth_token'] = data['data']['Token']
    #         context.user_data['is_logged_in'] = True
    #         update.message.reply_text(data['message'])
    #         return sports_list(update, context)
    #     else:
    #         update.message.reply_text(f"Invalid OTP. {data['message']}. Please enter the correct OTP.")
    #         return WAITING_FOR_OTP
    else:
        update.message.reply_text(f"Invalid OTP. Please enter the correct OTP.")
        return WAITING_FOR_OTP

def display_static_menu(update, context):

    menu_buttons = [
        InlineKeyboardButton("Upcoming Matches", callback_data='upcoming_matches'),
        InlineKeyboardButton("Logout", callback_data='logout'),
        InlineKeyboardButton("Check Wallet Balance", callback_data='check_wallet_balance'),
        InlineKeyboardButton("Recharge Wallet", callback_data='recharge_wallet')
    ]
    reply_markup = InlineKeyboardMarkup([menu_buttons])
    if update.message:
        update.message.reply_text("Please select:", reply_markup=reply_markup)
    elif update.callback_query and update.callback_query.message:
        update.callback_query.message.reply_text("Please select an option from the menu:", reply_markup=reply_markup)
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Please select an option from the menu:",
            reply_markup=reply_markup
        )
    return display_submenu(update,context)

def display_submenu(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    selected_option = query.data
    print("selected_option===>",selected_option)
    if selected_option == 'upcoming_matches':
        print("==============================")
        display_matches(update,context)
        # return ConversationHandler.END
    elif selected_option == 'logout':
        
        data=twelfthSighOut(update,context)
        print(data)
        if data['code']:
            update.callback_query.message.reply_text(data['message'])  
        else:
            update.message.reply_text("Something Went Wrong...")  
        context.user_data.clear()
        updater.stop()
        return ConversationHandler.END
    elif selected_option == 'check_wallet_balance':
        # Handle checking wallet balance
        update.message.reply_text("Checking wallet balance...")
        return ConversationHandler.END
    elif selected_option == 'recharge_wallet':
        # Handle recharging wallet
        update.message.reply_text("Recharging wallet...")
        return ConversationHandler.END
    else:
        pass
        # update.message.reply_text("Invalid option selected.")
        # return SUBMENU_OPTIONS

# ==========ERROR HANDLING=============
def unknown_command(update, context):
    command = update.message.text
    user_id = update.message.from_user.id

    if command in ["/Login", "/Register"]:
        logger.error(f"Error: {context.error}")
        update.message.reply_text("You are already LoggedIn")
        
        keyboard = [[InlineKeyboardButton("Show Sport Menu", callback_data='show_sport_menu')]]
        # reply_markup = InlineKeyboardMarkup(keyboard)
        # update.message.reply_text("Click the button below to show the sport menu:", reply_markup=reply_markup)
        return button_click(update, context)

    else:
        logger.error(f"Error: {context.error}")
        update.message.reply_text("Sorry, I don't understand that command.")

def button_click(update, context):
    return sports_list(update, context)
    
# ==========MAIN FUNCTION =============
def main() -> None:
    dp = updater.dispatcher

    # Define the conversation handler with states
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("Register", register_message),
            CommandHandler("Login", login_message),
            CommandHandler("twelfthVerifyOTP", twelfthVerifyOTP)
        ],
        states={
            REGISTER_PHONE: [MessageHandler(Filters.text & ~Filters.command, register_phone)],
            LOGIN_USERNAME: [MessageHandler(Filters.text & ~Filters.command, login_username)],
            WAITING_FOR_OTP: [MessageHandler(Filters.text & ~Filters.command, waiting_for_otp_input)],
            SELECT_SPORT: [CallbackQueryHandler(select_sport)],
            SELECT_MATCH: [CallbackQueryHandler(display_matches)],
            SUBMENU_OPTIONS: [CallbackQueryHandler(display_submenu)]
        },
        fallbacks=[],
    )

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("SportsList", sports_list))
    dp.add_handler(CommandHandler("UpcomingMatches", display_matches))
    dp.add_handler(conv_handler)
    dp.add_handler(MessageHandler(Filters.text, unknown_command))
    dp.add_handler(CallbackQueryHandler(button_click))

    updater.start_polling()
    updater.idle()
    # try:
    #     updater.idle()
    # except KeyboardInterrupt:
    #     updater.stop()


if __name__ == '__main__':
    main()
