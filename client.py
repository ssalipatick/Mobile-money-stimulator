from app import *
import random
from messaging import *


class client():
	# Client methods
	# send money
	# withdraw money
	# check balance
	# change pin
	# authenticate -  to authenticate the user obj
	def send_money(self,user_receiving,amount):
		user_receiving = Clients.query.filter_by(phone_number=user_receiving).first()
		user_sending = Clients.query.filter_by(phone_number=self.db.phone_number).first()

		user_receiving_name = user_receiving.first_name+' '+user_receiving.last_name
		user_sending_name = user_sending.first_name+' '+user_sending.last_name

		# get the balances
		sender_balance = user_sending.balance
		receiver_balance = user_receiving.balance

		# perform the transaction
		user_sending.balance = sender_balance - amount
		user_receiving.balance = receiver_balance + amount
		# Add also part for the transactions tables
		db.session.commit()
		send_message('Swift',user_sending.phone_number,'You have sent '+str(amount)+'UGX to '+user_receiving_name+'. Your new Account balance is '+str(user_sending.balance))
		send_message('Swift',user_receiving.phone_number,'You have received '+str(amount)+'UGX from '+user_sending_name+'. Your new Account balance is '+str(user_receiving.balance))

		return 'Sucessfully sent '+str(amount)+'UGX to '+str(user_receiving_name)+'. Your new account balance is '+str(user_sending.balance)+'UGX.'

	def withdraw(self,amount):
		secrete_code = str(random.randrange(1000, 9000, 4))
		withdraw = client_withdraws(phone_number =self.db.phone_number,
									amount = amount,
									secrete_code = secrete_code
			)
		db.session.add(withdraw)
		db.session.commit()
		send_message('Swift',self.db.phone_number,'You have initiated a cash withdraw of '+str(amount)+'UGX. The secrete code is '+secrete_code)


		return 'withdraw initiated, secrete code is '+secrete_code

	def get_balance(self):

		return self.db.balance

	def change_pin(self,old_pin,new_pin):
		if old_pin == self.db.pin:
			# change pin
			self.db.pin = new_pin
			db.session.commit()
			return 'Pin sucessfully changed'
		return 'Error in changing PIN'

	def autho(self,phone_number,pin):

		self.db = Clients.query.filter_by(phone_number=phone_number,pin = pin).first()

	def create_account(self,details):
		client = Clients(first_name = details['first_name'],
						last_name = details['last_name'],
						phone_number = details['phone_number'],
						pin = details['pin']
			)
		db.session.add(client)
		db.session.commit()
		return '1'

	def check(self,phone_number):
		names = Clients.query.filter_by(phone_number=phone_number).first()
		return names.first_name+' '+names.last_name

	def check_pin(self,pin):
		if self.db.pin == pin:
			return 1
		return 0


# Tests below here
# Create new Account
# Send Money
# Withdraw money
# Get Balance
# Change PIN

# ssali = client()
# ssali.autho('0758894242','4567')
# print (ssali.db.pin)







