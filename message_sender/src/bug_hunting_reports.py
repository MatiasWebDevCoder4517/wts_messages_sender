"""
ERROR1:
On line: pywhatkit.sendwhatmsg(cellphone, SPECIAL_MESSAGE, hour, minute, wait_time=5)

Exception has occurred: ValueError
sleep length must be non-negative
  File ".\wts_messages_sender\message_sender\src\main.py", line 74, in main
    pywhatkit.sendwhatmsg(cellphone, SPECIAL_MESSAGE, hour, minute, wait_time=5)
  File ".\wts_messages_sender\message_sender\src\main.py", line 83, in <module>
    main()
ValueError: sleep length must be non-negative

ERROR2:

Exception has occurred: CallTimeException
Call Time must be Greater than Wait Time as WhatsApp Web takes some Time to Load!
  File ".\wts_messages_sender\message_sender\src\main.py", line 74, in main
    pywhatkit.sendwhatmsg(cellphone, SPECIAL_MESSAGE, hour, minute)
  File ".\wts_messages_sender\message_sender\src\main.py", line 83, in <module>
    main()
pywhatkit.core.exceptions.CallTimeException: Call Time must be Greater than Wait Time as WhatsApp Web takes some Time to Load!







"""
