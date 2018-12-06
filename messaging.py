from app import message, db


def get_messages(number):
	messages = []
	msgs = message.query.filter_by(receiver=number)
	for msg in msgs:
		data = {}
		data['sender']=msg.sender 
		data['receiver']=msg.receiver 
		data['content']=msg.content
		data['datetime']=msg.datetime
		messages.append(data)
	return messages

def send_message(sender_number,receiver_number,content):
	msgs = message(
		sender=sender_number,
		receiver=receiver_number,
		content=content
		)
	db.session.add(msgs)
	db.session.commit()
	return 1