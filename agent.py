from app import *
from messaging import *
class agent():
	# Client methods
	# send money
	# withdraw money
	# check balance
	# change pin
	# authenticate -  to authenticate the user obj
	def deposite(self,user_receiving,amount):
		user_receiving = Clients.query.filter_by(phone_number=user_receiving).first()
		# get the balances
		amount = int(amount)
		user_sending =	Agents.query.filter_by(phone_number=self.db.phone_number,pin = self.db.pin).first()
		
		user_receiving_name = user_receiving.first_name+' '+user_receiving.last_name
		user_sending_name = user_sending.first_name+' '+user_sending.last_name


		sender_balance = user_sending.balance
		receiver_balance = user_receiving.balance

		# perform the transaction
		user_sending.balance = sender_balance - amount
		user_receiving.balance = receiver_balance + amount
		# Add also part for the transactions tables

		send_message('Swift',user_sending.phone_number,'You have sent '+str(amount)+'UGX to '+user_receiving_name+'. Your new Account balance is '+str(user_sending.balance))
		send_message('Swift',user_receiving.phone_number,'You have received '+str(amount)+'UGX from '+user_sending_name+'. Your new Account balance is '+str(user_receiving.balance))
		db.session.commit()
		return 'Sucessfully sent '+str(amount)+'UGX to '+str(user_receiving.phone_number)+'. Your new account balance is '+str(user_sending.balance)+'UGX.'

	def cash_out(self,phone_number,secrete_code):
		withdraw = client_withdraws.query.filter_by(
			phone_number = phone_number,secrete_code = secrete_code
			).first()
		if withdraw:
			client = Clients.query.filter_by(phone_number=withdraw.phone_number).first()
			agent =	Agents.query.filter_by(phone_number=self.db.phone_number,pin = self.db.pin).first()
			if client:
				amount = withdraw.amount
				client_balance = client.balance
				agent_balance = agent.balance
				# perform transaction
				client.balance = client_balance-amount
				agent.balance = agent_balance + amount

				agent_name = agent.first_name+' '+agent.last_name
				client_name = client.first_name+' '+client.last_name

				send_message('Swift',client.phone_number,'You have withdrawn '+str(amount)+'UGX from '+agent_name+'. Your new Account balance is '+str(client.balance))
				send_message('Swift',agent.phone_number,'Cash out of '+str(amount)+'UGX to '+client_name+' sucessfull. Your new Account balance is '+str(agent.balance))

				db.session.commit()
				return 'Cash out of '+str(withdraw.amount)+'UGX from '+str(withdraw.phone_number)+' sucessfull'

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

		self.db = Agents.query.filter_by(phone_number=phone_number,pin = pin).first()

	def create_account(self,details):
		agent = Agents(first_name = details['first_name'],
						last_name = details['last_name'],
						phone_number = details['phone_number'],
						pin = details['pin']
			)
		db.session.add(agent)
		db.session.commit()
		return '1'

	def check(self,phone_number):
		names = Clients.query.filter_by(phone_number=phone_number).first()
		if names:
			return names.first_name+' '+names.last_name

	def check_pin(self,pin):
		if self.db.pin == pin:
			return 1
		return 0


