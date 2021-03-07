#######START - IMPORTANT NOTICE TO READ###########
#                                                #
# This is an sample configuration file for       #
# people who self-host the userbot without using #
# environment variables and setting ENV to       #
# 'ANYTHING'.                                    #
#                                                #
# ============================================== #
#                                                #
# Duplicate this file into 'config.py', read the #
# comments before editing, save. Go to the last  #
# line and set the IS_THIS_CONFIG_EXAMPLE        #
# variable into "NOT ANYMORE" for the userbot to #
# start. This is to ensure that people           #
# understand how to configure this userbot.      #
#                                                #
#########END - IMPORTANT NOTICE TO READ###########

# Telegram API Info
# Replace placeholders with your own values. For sting token, use the sting session generator script.
API_ID = 123456
API_HASH = "YourApiHashHere"
STRING_SESSION = "YourSessionStringHere"
BOT_TOKEN = "YourBotAPITokenHere"

# The MongoDB URL
# Use the v3.4.x+ URL format. For 3.6.x+, make sure 'dnspython' is installed.
MONGO_DB_URL = "mongodb://SSCUserbotApiRoot:password@localhost:27017/apiMain?ssl=true&replicaSet=SSC-Userbot-DB-shard-0&authSource=admin&retryWrites=true&w=majority"

# These numbers below are real userids.
# Replace it with your own userids. Or, remove everything and manually paste userids in JSON format.
SIBYL = [709590349, 705519392, 652113804, 982858663]
ENFORCERS = [276375010, 370663289, 660565862, 528781117, 596701090, 472245282, 394012198, 771130169, 321750518, 799678999, 615304572, 486514034, 367222759, 59038234, 256304538, 745191358, 570787098, 439595878, 596701090, 459034222, 971324495, 365085145, 677721265, 1096215023, 608750088, 962286971, 565218601, 731736814, 239556789, 669152898]
INSPECTORS = [895373440, 792109647, 570787098, 615304572, 324460662, 425599267, 1045178534, 962286971, 591929714, 123006962, 808197325]

# These intergers below are real chatids.
# Replace it with your own chatids or the userbot will not start.
Sibyl_logs = -1001462662903
Sibyl_approved_logs = -1001190992619
GBAN_MSG_LOGS = -1001411763887

########################################
# IMPORTANT!                           #
# Set the variable below to            #
# "NOT ANYMORE" in order to run this   #
# userbot without using/going          #
# to environment variables/env mode.   #
########################################
IS_THIS_CONFIG_EXAMPLE = "READ THE COMMENTS ON L1-L17 FIRST!"