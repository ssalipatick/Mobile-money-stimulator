
from client import client
from agent import agent
class client_ussd_session():
    
    def __init__(self,phone_number,pin):
        self.client = client()
        self.client.autho(phone_number,pin)
        self.steps = []

    def resp(self, req_text = 0):
        if not self.steps:
            # Return the first menue
            # 1.Send Money
            # 2.Withdraw Cash
            # 3.My Account
            self.steps.append(0)
            return {'title' : 'Mobile Money', 'items' : ['Send Money','Withdraw Cash','My account']}
        else:
            if self.steps[0] == 0:
                # Get the response text
                self.steps[0] = req_text

            # Managing responses
            

            # _________SEND MONEY________
            if self.steps[0] == '1':

                # If they need a response
                if len(self.steps) == 1:
                    self.steps.append(0)
                    return {'title' : 'Enter Number', 'items' : []}
                
                if self.steps[1] == 0 or self.steps[1]:
                    #___________Enter Number________
                    # If they need a response
                    if len(self.steps) == 2:
                        self.steps[1] = req_text
                        self.steps.append(0)
                        return {'title' : 'Enter ammount ', 'items' : []}
                    
                    if self.steps[2] == 0 or self.steps[2]:
                        # __________Enter Ammount_____

                        # If they need a response
                        if len(self.steps) == 3:
                            self.steps[2] = req_text
                            ammount_to_send = self.steps[2]
                            receiver_number = self.steps[1]
                            self.steps.append(0)
                            # get the names of the number they are sendong to the money
                            receiver_names  = self.client.check(str(receiver_number))
                            return {'title' : 'Enter PIN to confirm transfer of '+ammount_to_send+'UGX to '+receiver_names+'.', 'items' : []}

                        if self.steps[3] == 0 or self.steps[3] == 0:
                            # __________Enter PIN_______

                            # If they need a response
                            if len(self.steps) == 4:
                                self.steps[3] = req_text
                                receiver_number = self.steps[1]
                                ammount_to_send = int(self.steps[2])
                                entered_pin = self.steps[3]
                                self.steps.append(0)
                                if self.client.check_pin(entered_pin):
                                    transaction = self.client.send_money(receiver_number,ammount_to_send)
                                    return {'title' : transaction, 'items' : [],'end':1}
                                return {'title' : 'Wrong PIN', 'items' : [],'end':1}


            # __________WITHDRAW CASH______________
            if self.steps[0] == '2':

                # If they need a response
                if len(self.steps) == 1:
                    #___________Enter Ammount________
                    self.steps.append(0)
                    return {'title' : 'Enter Ammount', 'items' : []}
                
                if self.steps[1] == 0 or self.steps[1]:
                    #___________Enter PIN________
                    # If they need a response
                    if len(self.steps) == 2:
                        self.steps[1] = req_text
                        ammount_to_withdraw = self.steps[1]
                        self.steps.append(0)
                        return {'title' : 'Enter PIN to confirm withdraw of '+str(ammount_to_withdraw)+'UGX', 'items' : []}
                    
                    if self.steps[2] == 0 or self.steps[2]:
                        # __________Enter PIN_____

                        # If they need a response
                        if len(self.steps) == 3:
                            self.steps[2] = req_text
                            ammount_to_withdraw = self.steps[1]
                            entered_pin = self.steps[2]
                            self.steps.append(0)

                            if self.client.check_pin(entered_pin):
                                transaction = self.client.withdraw(ammount_to_withdraw)
                                return {'title' : transaction, 'items' : [],'end':1}
                                return {'title' : 'Wrong PIN', 'items' : [],'end':1}


            # _________Account__________________
            if self.steps[0] == '3':

                # If they need a response
                if len(self.steps) == 1:
                    self.steps.append(0)
                    return {'title' : 'My Account', 'items' : ['Check Balance','Statement','Change PIN']}

                #___________Check Balance________
                if self.steps[1] == 0:

                    # If they need a response
                    if len(self.steps) == 2:
                        self.steps[1] = req_text
                        self.steps.append(0)
                        return {'title' : 'Enter PIN ', 'items' : []}
                    
                    # _________Sucess Response________
                    if self.steps[2] == 0 or self.steps[2]:

                        # If they need a response
                        if len(self.steps) == 3:
                            self.steps[2] = req_text
                            self.steps.append(0)
                            transaction = self.client.get_balance()
                            return {'title' : transaction, 'items' : [],'end':1}

                # __________ Statment_________
                if self.steps[1] == 0 or self.steps[1]:

                    # If they need a response
                    if len(self.steps) == 2:
                        self.steps[1] = req_text
                        self.steps.append(0)
                        return {'title' : 'Enter PIN ', 'items' : []}
                    
                    # _________Sucess Response________
                    if self.steps[2] == 0 or self.steps[2]:

                        # If they need a response
                        if len(self.steps) == 3:
                            self.steps[2] = req_text
                            self.steps.append(0)
                            return {'title' : 'Sucess', 'items' : [],'end':1}


                # __________ Change PIN_________
                if self.steps[1] == 0 or self.steps[1]:

                    # If they need a response
                    if len(self.steps) == 2:
                        self.steps[1] = req_text
                        self.steps.append(0)
                        return {'title' : 'Enter Old PIN ', 'items' : []}
                    
                    # _________Sucess Response________
                    if self.steps[2] == 0 or self.steps[2]:

                        # If they need a response
                        if len(self.steps) == 3:
                            self.steps[2] = req_text
                            self.steps.append(0)
                            return {'title' : 'Sucess', 'items' : []}


    def display(self,req_text = 0):
        resp_text = self.resp(req_text)
        if resp_text:
            print resp_text['title']
            i = 0
            for item in resp_text['items']:
                i +=1
                print str(i) +'.'+ item
        print ''


class agent_ussd_session():
    
    def __init__(self,phone_number,pin):
        self.agent = agent()
        self.agent.autho(phone_number,pin)
        self.steps = []

    def resp(self, req_text = 0):
        if not self.steps:
            # Return the first menue
            # 1.Cash Deposit
            # 2.Cash withdraw
            # 3.My Account
            self.steps.append(0)
            return {'title' : 'Mobile Money', 'items' : ['Cash Deposit','Cash Withdraw','My account']}
        else:
            if self.steps[0] == 0:
                # Get the response text
                self.steps[0] = req_text

            # Managing responses
            

            # _________Cash Deposit________
            if self.steps[0] == '1':

                # If they need a response
                if len(self.steps) == 1:
                    self.steps.append(0)
                    return {'title' : 'Enter Phone Number', 'items' : []}
                
                if self.steps[1] == 0 or self.steps[1]:
                    #___________Enter Number________
                    # If they need a response
                    if len(self.steps) == 2:
                        self.steps[1] = req_text
                        self.steps.append(0)
                        return {'title' : 'Enter ammount ', 'items' : []}
                    
                    if self.steps[2] == 0 or self.steps[2]:
                        # __________Enter Ammount_____

                        # If they need a response
                        if len(self.steps) == 3:
                            self.steps[2] = req_text
                            receiver_number = self.steps[1]
                            ammount = self.steps[2]
                            self.steps.append(0)
                            receiver_names = self.agent.check(receiver_number)
                            if receiver_names:
                                return {'title' : 'Enter PIN to confirm Cash Deposit of '+str(ammount)+'UGX to '+str(receiver_names), 'items' : []}
                            return {'title' : 'The number '+str(receiver_number)+' isnt registered. Please tell them to register', 'items' : [], 'end':1}


                        if self.steps[3] == 0 or self.steps[3] == 0:
                            # __________Enter PIN_______

                            # If they need a response
                            if len(self.steps) == 4:
                                self.steps[3] = req_text
                                receiver_number = self.steps[1]
                                amount = self.steps[2]
                                pin = self.steps[3]
                                self.steps.append(0)
                                if self.agent.check_pin(pin):
                                    transaction = self.agent.deposite(receiver_number,amount)
                                    return {'title' : transaction, 'items' : [],'end':1}
                                return {'title' : 'Wrong PIN', 'items' : [],'end':1}


            # __________WITHDRAW CASH______________
            if self.steps[0] == '2':

                # If they need a response
                if len(self.steps) == 1:
                    #___________Enter Number________
                    self.steps.append(0)
                    return {'title' : 'Enter Number', 'items' : []}
                
                if self.steps[1] == 0 or self.steps[1]:
                    #___________Enter Secrete Code________
                    # If they need a response
                    if len(self.steps) == 2:
                        self.steps[1] = req_text
                        self.steps.append(0)
                        return {'title' : 'Enter secrete code ', 'items' : []}
                    
                    if self.steps[2] == 0 or self.steps[2]:
                        # __________Enter PIN_____

                        # If they need a response
                        if len(self.steps) == 3:
                            self.steps[2] = req_text
                            self.steps.append(0)
                            return {'title' : 'Enter PIN', 'items' : []}

                        if self.steps[3] == 0 or self.steps[2]:
                        # __________Enter PIN_____

                            # If they need a response
                            if len(self.steps) == 4:
                                self.steps[3] = req_text
                                self.steps.append(0)
                                phone_number = self.steps[1]
                                secrete_code = self.steps[2]
                                pin = self.steps[3]
                                if self.agent.check_pin(pin):
                                    transaction = self.agent.cash_out(phone_number,secrete_code)
                                    return {'title' : transaction, 'items' : [],'end':1}
                                return {'title' : 'Wrong PIN', 'items' : [],'end':1}


                                return {'title' : 'Sucess', 'items' : []}




            # _________Account__________________
            if self.steps[0] == '3':

                # If they need a response
                if len(self.steps) == 1:
                    self.steps.append(0)
                    return {'title' : 'My Account', 'items' : ['Check Balance','Statement','Change PIN']}

                #___________Check Balance________
                if self.steps[1] == 0:

                    # If they need a response
                    if len(self.steps) == 2:
                        self.steps[1] = req_text
                        self.steps.append(0)
                        return {'title' : 'Enter PIN ', 'items' : []}
                    
                    # _________Sucess Response________
                    if self.steps[2] == 0 or self.steps[2]:

                        # If they need a response
                        if len(self.steps) == 3:
                            self.steps[2] = req_text
                            self.steps.append(0)
                            return {'title' : 'Sucess', 'items' : []}

                # __________ Statment_________
                if self.steps[1] == 0 or self.steps[1]:

                    # If they need a response
                    if len(self.steps) == 2:
                        self.steps[1] = req_text
                        self.steps.append(0)
                        return {'title' : 'Enter PIN ', 'items' : []}
                    
                    # _________Sucess Response________
                    if self.steps[2] == 0 or self.steps[2]:

                        # If they need a response
                        if len(self.steps) == 3:
                            self.steps[2] = req_text
                            self.steps.append(0)
                            return {'title' : 'Sucess', 'items' : []}


                # __________ Change PIN_________
                if self.steps[1] == 0 or self.steps[1]:

                    # If they need a response
                    if len(self.steps) == 2:
                        self.steps[1] = req_text
                        self.steps.append(0)
                        return {'title' : 'Enter Old PIN ', 'items' : []}
                    
                    # _________Sucess Response________
                    if self.steps[2] == 0 or self.steps[2]:

                        # If they need a response
                        if len(self.steps) == 3:
                            self.steps[2] = req_text
                            self.steps.append(0)
                            return {'title' : 'Sucess', 'items' : []}


    def display(self,req_text = 0):
        resp_text = self.resp(req_text)
        if resp_text:
            print resp_text['title']
            i = 0
            for item in resp_text['items']:
                i +=1
                print str(i) +'.'+ item
        print ''

           
