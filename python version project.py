# - In this project, I used objects to simulate a Mall's card system.
# - I assume there are 2 types of cards, Debit card and Credit card.
# - Two types of cards are different in many ways.
# - A card holder can deposit, expense, check statement, earn points and then redeem for lottery draws etc.
# - Mall hold records and need to pay for the management fee.

from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta
import numpy as np
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

# - Below is the parent class Account.
# - It has a holder.
# - It takes record for individuls and the total balance in the mall.

class Account:
    '''This class variable takes record of Mall's balance'''
    balance = 0
    
    '''owner arg is the account's owner's name.
    personal records are all initialized to blank series or 0.'''
    def __init__(self, owner):
        self.owner = owner
        self.point = pd.Series()
        self.depo = pd.Series()
        self.exp = pd.Series()
        self.withd = pd.Series()
        self.balance = 0
        
    def __str__(self):
        return 'Balance: {}'.format(Account.balance)
    
    def __repr__(self):
        return self.__str__()   
    
    '''deposit method will change the Mall's balance, personal balance, 
        personal points record, and personal deposit record.
        By depositing money, one can earn 0.1 points per dollar.'''
    def deposit(self, amount):
        time = str(datetime.now())
        Account.balance += amount
        self.balance += amount
        self.point.set_value(time, 0.1*amount)
        self.depo.set_value(time, amount)
        return None
    
    '''expense method will do similar jobs as the depostit method does.
        By expensing money, one can earn 0.05 points per dollar.'''
    def expense(self, amount):
        if amount > self.balance:
            print("Current Balance: {}".format(self.balance))
            raise ValueError("YOU HAVE LOW BALANCE")
        else:
            time = str(datetime.now())
            Account.balance -= amount
            self.balance -= amount
            self.point.set_value(time, 0.05*amount)
            self.exp.set_value(time, amount)
            return None
    
    '''One can withdraw money only if there is enough money in the account. 
        Otherwise, return an error.'''
    def withdraw(self, amount):
        if amount > self.balance:
            print("Current Balance: {}".format(self.balance))
            raise ValueError("YOU HAVE LOW BALANCE")
        else:
            time = str(datetime.now())
            Account.balance -= amount
            self.balance -= amount
            self.withd.set_value(time, amount)
            print("Current Balance: {}".format(self.balance))    
    
    '''One can check his/her own account statement. 
        It returns a table of records of transactions.'''
    def statement(self):
        d = {'deposit' : self.depo,
             'expense' : self.exp,
             'withdraw' : self.withd,
              'points' : self.point}
        state = pd.DataFrame(d)
        return(state.fillna(''))
    
    '''One can plot the statement.'''
    def plot(self):
        d = {'deposit' : self.depo,
             'expense' : self.exp,
             'withdraw' : self.withd,
              'points' : self.point}
        state = pd.DataFrame(d)
        ax = state[['deposit','expense','withdraw']].plot(kind='bar', title ="Statement", figsize=(15, 10), 
                                                          legend=True, fontsize=12)
        ax.set_xlabel("Transactions", fontsize=12)
        ax.set_ylabel("Amount", fontsize=12)
        plt.show()
    
    '''One can check the number of cumulated points.'''
    def points(self):
        print("Total Obtained Points: {}".format(self.point.sum()))
        return self.point
    
    '''One can redeem 50 points for once lottery draw.
        Reward gifts are specially chosed based on seasons, 
        and there are equal chances to get different levels of gifts. 
        It is all about luck.'''
    def reward(self):
        newyear = date(datetime.now().year,1,1)
        redeem_date = date.today()
        selection = np.random.uniform(0,4)
        if self.point.sum() >= 10:
            if ((redeem_date-newyear).days) <= 93:
                season = 'Spring'
                gift = ['Lip Balm', 'Perfume', 'Panini Maker', 'Bicycle']
            elif ((redeem_date-newyear).days) > 93 and ((redeem_date-newyear).days) <= 187:
                s = 'Summer'
                gift = ['T-shirt', 'Sun Cream', 'Cold Brew Coffee Machine', 'Air Conditioner']
            elif ((redeem_date-newyear).days) > 187 and ((redeem_date-newyear).days) <= 277:
                s = 'Fall'
                gift = ['Hand Cream', 'Yoga mat', 'Juice Mixer','VR Goggles']
            else:
                s = 'Winter'
                gift = ['Gloves', 'New York Times Best Seller Book', 'Heater', 'Over-ear Headphones']

            reward_gift = gift[math.floor(selection)]
            self.point.set_value(datetime.now(), -50)
            print('Now is {}, please enjoy it with your reward gift: {}.'.format(s, reward_gift))    
        else:
            print('Sorry, you do not have enough points to get a reward gift.')
        



# - Below is a subclass DebitCard.
# - It has a holder.
# - It inherits from the Accout class.


class DebitCard(Account):
    '''One can deposit to his/her credit card, can directly expense through it,
        can check the statement of the card, and can check how many points acumulated.'''
    
    def deposit(self, amount):
        return Account.deposit(self, amount)
    
    def expense(self, amount):
        return Account.expense(self, amount)
    
    def statement(self):
        print("Current Balance: {}".format(self.balance))
        return Account.statement(self)
    
    def points(self):
        print(Account.points(self))
        return None


# - Below is another subclass, CreditCard.
# - It has a holder.
# - It inherits from the Accout class.
# - Different from the debit card, credit card owner has a balance due statement.
# Once the due was not paid on time, compound interests will be applied onto the due every 31 days.
# [Notice: Here, for the convenience of simulation, I set the compound period as 15 seconds.]


class CreditCard(Account):
    
    def __init__(self, owner):
        self.balance_due = {}
        self.point = 0
        
    '''One can expense money via the credit card, this will leave records as Balance due.'''
    def expense(self, amount):
        expense_date = datetime.now()
        self.balance_due[expense_date] = amount
        self.point += 0.1*amount
        print(self.balance_due)
        return None
    
    '''One can check how much is due up to now.
       Also, one can get a statement containing the original expenses and due after interests added on.'''
    def balancedue(self):
        rate = 0.02
        n = len(self.balance_due)
        self.due = pd.DataFrame(self.balance_due, index = np.arange(1))
        self.due = self.due.T
        afterinterest = pd.Series()
        for time in self.balance_due.keys():
            period = ((datetime.now() - time).seconds)//15
            afterinterest = afterinterest.set_value(time, self.balance_due[time]*((1 + rate)**period))    
            self.due = self.due.assign(after_interest = afterinterest)
        self.due.columns = ['Expense Amount', 'Post-interest Amount']
        print(self.due) 
        return 'Balance due: {}'.format(self.due[['Post-interest Amount']].sum())
    
    '''One can clear his/her due.
        Once cleared, no further interests need to be paid.
        clear method has time arg indicating the date of due that needs to be removed.'''
    def clear(self, time):
        del self.balance_due[time]
        return None
    
    def plot(self):
        ax = self.due[['Expense Amount']].plot(kind='bar', title ="Expense", figsize=(15, 10), legend=True, fontsize=12)
        ax.set_xlabel("Expense", fontsize=12)
        ax.set_ylabel("Amount", fontsize=12)
        plt.show()


# - Below is a another class, Mall.
# - It has method related to the account records.
# - It has method giving the estimated management cost.


class Mall:
    accounts = {}
    
    def __str__(self):
        return 'Mall Info'
    def __repr__(self):
        return self.__str__() 
    
    '''This takes records of what kinds of card a customer has.'''
    def newaccount(self, owner, cardtype):
        self.opentime = date.today()
        if owner in Mall.accounts.keys():
            Mall.accounts[owner].append(cardtype)
        else:
            Mall.accounts.update({owner: [cardtype]})
        print(Mall.accounts)
    
    '''This givea a approximated management cost based on current total balance in the Mall card system.'''
    def approx_management_cost(self):
        if Account.balance > 0:
            management_cost_rate = 0.001
        else:
            management_cost_rate = 0.0005
        return (abs(Account.balance*management_cost_rate))



# below are test cases:
amy = Account('amy')
ben = DebitCard('ben')
dan = DebitCard('dan')
cindy = CreditCard('cindy')
emma = CreditCard('emma')

Mall().newaccount('ben', 'DebitCard')
Mall().newaccount('dan', 'DebitCard')
Mall().newaccount('ben', 'CeditCard')

ben.deposit(500)
ben.deposit(100)
ben.expense(200)
ben.statement()

ben.withdraw(300)

ben.withdraw(300)

ben.expense(300)

ben.statement()

ben.plot()

ben.points()

ben.reward()

ben.points()

dan.deposit(400)

dan.statement()

ben.statement()

Account('Mall')

Mall().approx_management_cost()

emma.expense(600)

emma.expense(300)

emma.balancedue()

emma.balancedue()

emma.clear(datetime(2017, 11, 13, 15, 57, 28, 353112))

emma.balancedue()

emma.expense(300)
emma.expense(560)
emma.expense(870)
emma.expense(10)
emma.expense(30)
emma.expense(270)

emma.balancedue()

emma.plot()

# Overall, I think Python fits well to my project. Most of the problems I met are related to recording data and then clearing them up for calculations. I think R would do a better job about this part. However, Python does a good job in building up the entire simulation system, which may be harder in R.







can you add the credit limit code to my code?
ChatGPT
Sure, in order to add a credit limit to your CreditCard class, we need to modify the constructor (init) to include a credit limit attribute and also modify the expense method to check the credit limit before allowing an expense. Here is the updated code:


class CreditCard(Account):
    
    def __init__(self, owner, credit_limit):
        self.owner = owner
        self.point = pd.Series()
        self.depo = pd.Series()
        self.exp = pd.Series()
        self.withd = pd.Series()
        self.balance = 0
        self.balance_due = {}
        self.credit_limit = credit_limit  # Set the credit limit when the account is created
        
    '''One can expense money via the credit card, this will leave records as Balance due.'''
    def expense(self, amount):
        # Check if the expense will exceed the credit limit
        if (self.balance + amount) > self.credit_limit:
            print("This expense will exceed your credit limit.")
            return None
        else:
            time = str(datetime.now())
            self.balance_due[time] = amount
            self.balance += amount
            self.point.set_value(time, 0.1*amount)
            print(self.balance_due)
            return None
        

In this code, the credit limit is set when a new CreditCard is created, like so:

cindy = CreditCard('cindy', 5000)  # Cindy's credit limit is $5000


The expense method now checks whether the new expense will exceed the credit limit before proceeding. If the expense is too large, a message is printed and the method returns None, signifying that the operation was unsuccessful. If the expense is within the limit, the method proceeds as before.