from app import *
class swift():

	def send_money(self,user_sending,user_receiving,amount):
		user_sending = Clients.query.filter_by(phone_number=user_sending).first()
		user_receiving = Clients.query.filter_by(phone_number=user_receiving).first()
		# get the balances
		sender_balance = user_sending.balance
		receiver_balance = user_receiving.balance

		# perform the transaction
		user_sending.balance = sender_balance - amount
		user_receiving.balance = receiver_balance + amount
		# Add also part for the transactions tables
		db.session.commit()
		return 'Sucessfully sent '+str(amount)+'UGX to '+str(user_receiving)+'. Your new account balance is '+str(user_sending.balance)+'UGX.'

	def client_withdraw(self,phone_number,amount):
		# get secrete code
		user_withdrawing = Clients.query.filter_by(phone_number=phone_number).first()
		user_balance = user_withdrawing.balance
		user_withdrawing.balance = user_balance - amount
		db.session.commit()
		return 'Secrete pin for the withdraw of '


	def autho_client(self,number):
		# return the user object
		user = Clients.query.filter_by(phone_number=number).first()
		return user