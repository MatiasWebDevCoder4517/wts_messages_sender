# from app.config import LOGGER


# import pandas as pd
# import pywhatkit
# import datetime import time


# def main():

#     # Read numbers from a CSV file
#     csv_file_path = 'path_to_your_csv_file.csv'
#     data = pd.read_csv(csv_file_path)

#     # Message you want to send
#     message = "Hello, this is a test message from Python!"

#     # Current time, to schedule messages
#     now = datetime.datetime.now()
#     hour = now.hour
#     minute = now.minute + 1  # Schedule the message 1 minute into the future

#     # Send message to each number
#     for index, row in data.iterrows():
#         number = row['number']
#         pywhatkit.sendwhatmsg(number, message, hour, minute)
#         time.sleep(20)  # Wait for 20 seconds before sending the next message to avoid clashes

#     LOGGER.info(f"Data inserted successfully! -> data_table modified: {data_table}")


# if __name__ == "__main__":
#     main()
