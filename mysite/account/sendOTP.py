from twilio.rest import Client
from .credentials import account_sid, auth_token, my_cell, my_twilio

# Find these values at https://twilio.com/user/account


my_msg = ''.join(['Hi Mayur!!\n' for i in range(100)])
my_msg+="-from MATHUR ;) "


mayur_cell="+917678599539"
def send_otp(reg_number,num):
    client = Client(account_sid, auth_token)
    reg_number=my_twilio
    otp= "Your One Time Password is: "
    print(otp+num)
    message = client.messages \
                    .create(
                         body=otp+num,
                         from_=reg_number,
                         status_callback='http://postb.in/1234abcd',
                         to=my_cell
                     )
    return message.sid

#print(message)
