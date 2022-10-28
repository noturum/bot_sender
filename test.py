import datetime
import time


import dbConn as db
user =db.executeSql('select UID from users')
a= ['@'+b[0] for b in user]
a=str(a).replace('[','').replace(']','')
import re
city='''Алматы 				
Анталья 				
Астрахань				
Баку 				
о. Бали 				
Бишкек 				
Владивосток				
Волгоград				
Грозный				
Дубай 				
Екатеринбург				
Ереван 				
Иркутск				
Казань				
Каир 				
Красноярск				
Лос-Анжелес 				
Майами 				
Махачкала				
Минеральные Воды				
Минск 				
Москва				
Нижний Новгород				
Новосибирск				
Нур-Султан 				
Нью-Йорк 				
Пермь				
Самара				
Санкт-Петербург				
Сан-Франциско 				
Саратов				
Сочи				
Стамбул 				
Сургут				
Томск				
Тюмень				
Улан-Удэ				
Хабаровск				
Ханты-Мансийск				
Челябинск'''

'''import datetime
newUser=0
activeUser=0
week=datetime.date.today()+datetime.timedelta(days=-7)
logs=db.executeSql('select * from log')
for log in logs:

    date=log[4].split(' ')[0].split('-')
    date=datetime.date(int(date[0]),int(date[1]),int(date[2]))
    if date >week and log[6]=='register':
        newUser+=1
print(f'новых пользователей за неделю: {newUser}')'''




'''import dbConn as db


with open('air.txt','r',encoding='utf-8') as f:
    for city in f.readlines():
        db.executeSql('insert into cities(name,local,type) values("{}",{},"{}")'.format(city.replace('\n',''),'777','Air'),True)'''

'''import csv
import dbConn as db
results = []
with open('city.csv') as File:
    reader = csv.DictReader(File)
    lastAirPort=''
    print(reader.fieldnames)'''

'''import telebot
from telebot import types
import configparser
config = configparser.ConfigParser()
config.read('settings.ini')
bot = telebot.TeleBot(config['telegram']['token'])

@bot.message_handler(commands=['start'])
def st(msg):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)

    keyboard.add(button_phone)
    bot.send_message(msg.chat.id,'contact',reply_markup=keyboard)
@bot.message_handler(content_types=['contact'])
def hadle_contact(message):
    print(message)
    bot.send_message(message.from_user.id, f'Я получил твой контакт: {message.contact.phone_number}')
bot.polling()'''



'''local=db.executeSql('select local from cities where name="{}"'.format('Екатеринбург'))
print(local)
if len(local)>0:
    cities=[city[0] for city in db.executeSql('select name from cities where local="{}" '.format(local[0][0]))]
    adds=db.executeSql("select * from adds where city1 in {}".format(tuple(cities)))
    print(adds)'''


class State():
    def __init__(self,arg,msgs):
        self.msgs=msgs
        self.args=arg

class Adds():
    def __init__(self,city1=None,city2=None,date=None,title=None,contact=None):
        self.city1 = city1
        self.city2 = city2
        self.date = date
        self.title = title
        self.contact = contact
    def commit(self):
        pass
    def getAdds(self):

def collapse(add):
    text = 'Заявка с ресурса: {}\n'.format(add[9]) if add[9] not in ['None', None, ''] and checkAdm(
        id) else ''
    text += 'Заявка  №{} {}'.format(add[1], '🚗') if add[7].find('Car') != -1 else 'Заявка  №{} {}'.format(add[1], '✈')
    text += ' Хочу отправить \n{} - {} : {}'.format(add[2], add[3], month(add[4])) if add[7].find(
        'Send') != -1 else 'Могу доставить {}\n{} - {} : {}'.format(
        '(возьму попутчика🙋🏻‍♂️)' if add[8] not in (None, 'False') else '', add[2], add[3], month(add[4]))
    text = entity(text)
    return text
def expand(add):
    user = db.executeSql('select * from users where UID={}'.format(add[0]))[0]
    username = user[3]
    text = 'Заявка с ресурса: {}\n'.format(add[9]) if add[9] not in ['None', None, ''] and checkAdm(
        id) else ''
    text += 'Заявка  №{} {}'.format(add[1], '🚗') if add[7].find('Car') != -1 else 'Заявка  №{} {}'.format(add[1],
                                                                                                           '✈')
    text += ' Хочу отправить \n{} - {} : {}\nКонтакты: {}'.format(add[2], add[3], month(add[4]), add[6]) if add[
                                                                                                                7].find(
        'Send') != -1 else 'Могу доставить {}\n{} - {} : {}\nКонтакты: {}'.format(
        '(возьму попутчика🙋🏻‍♂️)' if add[8] not in (None, 'False') else '', add[2], add[3], month(add[4]), add[6])

    reviews = db.executeSql('select * from reviews where contact="{}"'.format(username))
    reviews += db.executeSql('select * from reviews where contact="{}"'.format(add[6]))
    if len(reviews) > 0:
        help = ''
        for r in reviews: help += '@' + r + ', '
        text += '\ntg:@{} \n Помог пользователям:\n{}'.format(username,
                                                              help) if username != None else '\ntg:[{}](tg://user?id={})\nПомог пользователям:\n{}'.format(
            user[6], user[0], help)

    else:
        if user[1] != 'admin':
            text += '\ntg:@{}'.format(username) if username != None else '\ntg:[{}](tg://user?id={})'.format(
                user[6], user[0])
    text = entity(text)
    return text

def printAdds(id,adds,folding=None,edit=False,count=False,possible=None,mid=None):
    keyboard=types.InlineKeyboardMarkup()
    for add in adds:



        if edit:
            keyboard.add(types.InlineKeyboardButton('Редактировать', callback_data=f'edit@{add[1]}'),
                        types.InlineKeyboardButton('Удалить', callback_data=f'erase@{add[1]}'))
        if possible!=None:
            keyboard.add(types.InlineKeyboardButton('Отработано', callback_data=f'seen@{possible}@{add[1]}'))

        if folding!=None:
            call=f'expand/' if folding=='expand' else 'collaps/'
            call += 'Count/' if count else 'NoCount/'
            call += 'Seen' if possible else 'NoSeen'
            call += f'@{add[1]}'
            if folding=='expand':
                text = expand(add)

                keyboard.add(
                types.InlineKeyboardButton('Раскрыть', callback_data=call))
            else:
                text = collapse(add)
                keyboard.add(
                    types.InlineKeyboardButton('Cкрыть', callback_data=call))
            bot.edit_message_text(text, id,
                                  mid, parse_mode='MarkdownV2')
            bot.edit_message_reply_markup(id, mid, reply_markup=keyboard)


        else:
            text = expand(add)
            send_message(
                text,
                message,
                keyboard,
                state='adds')

    pass
def printAdds(message,adds,keyboardTitle,possibleAdd=False):
    '''idAdd = [k[0] for k in db.executeSql('select idAdds from adds where UID={}'.format(message.chat.id))]
    idAdd = str(idAdd).replace('[', '(').replace(']', ')')
    posSendAdds = db.executeSql('select * from possibleAdds where sendAdd in {}'.format(idAdd))
    posDelyAdds = db.executeSql('select * from possibleAdds where delyAdd in {}'.format(idAdd))'''

    for ad in adds:
        expandK = types.InlineKeyboardMarkup(row_width=1)
        call=f'expand@{ad[1]}' if keyboardTitle.find('Edit')==-1 else f'expandEdit@{ad[1]}'
        call+='@noCount' if keyboardTitle.find('noCount')!=-1 else '@count'


        text='Заявка с ресурса: {}\n'.format(ad[9]) if ad[9] not in ['None',None,''] and checkAdm(message.chat.id) else ''
        text += 'Заявка  №{} {}'.format(ad[1], '🚗') if ad[7].find('Car') != -1 else 'Заявка  №{} {}'.format(ad[1], '✈')
        text+=' Хочу отправить \n{} - {} : {}'.format(ad[2], ad[3],month(ad[4])) if ad[7].find('Send') != -1 else 'Могу доставить {}\n{} - {} : {}'.format('(возьму попутчика🙋🏻‍♂️)' if ad[8] not in (None, 'False') else '',ad[2], ad[3],month(ad[4]))
        if (possibleAdd!=False and checkAdm(message.chat.id)):
            call+='@seen'
            expandK.add(
                types.InlineKeyboardButton('Раскрыть', callback_data=call),types.InlineKeyboardButton('Отработано', callback_data=f'seen@{possibleAdd}@{ad[1]}'))
        else:
            expandK.add(
                types.InlineKeyboardButton('Раскрыть', callback_data=call))

        if text.find('отправить')!=-1 and keyboardTitle.find('expandEdit')!=-1:

            posDelyAdds = db.executeSql('select * from possibleAdds where sendAdd = {} and active="True"'.format(ad[1]))


            if len(posDelyAdds)>0:

                if ad[1]==posDelyAdds[0][1]:
                    print('poss')
                    keyPosAdd = types.InlineKeyboardButton(text='Могут доставить ({})'.format(len(posDelyAdds)), callback_data='posSendAdd@{}'.format(ad[1]))
                    expandK.add(keyPosAdd)


        if text.find('доставить')!=-1 and keyboardTitle.find('expandEdit')!=-1:

            posSendAdds = db.executeSql('select * from possibleAdds where delyAdd = {} and active="True"'.format(ad[1]))

            if len(posSendAdds) > 0:
                if ad[1]==posSendAdds[0][2]:
                    keyPosAdd = types.InlineKeyboardButton(text='Хотят отправить ({})'.format(len(posSendAdds)), callback_data='posDelyAdd@{}'.format(ad[1]))
                    expandK.add(keyPosAdd)



        send_message(
            text,
            message,
            expandK,
            state='adds')



        '''if ad[7].find('Car') != -1:
            if ad[7].find('Send') != -1:
                expandK = types.InlineKeyboardMarkup().add(
                    (types.InlineKeyboardButton('Раскрыть', callback_data=f'expand{ad[1]}')))
                send_message(
                    'Заявка  №{} 🚗 Хочу отправить \n{} - {} : {}'.format(ad[1], ad[2], ad[3],
                                                                          month(ad[4])),
                    message,
                    expandK,
                    state='search')
            if ad[7].find('Dely') != -1:
                if ad[8] in (None, 'False'):
                    text = 'Заявка  №{} 🚗 Могу доставить \n{} - {} : {}\nтел. {}'.format(ad[1], ad[2], ad[3],
                                                                                                  month(ad[4]),
                                                                                                  ad[6])
                else:
                    text = 'Заявка  №{} 🚗 Могу доставить (возьму попутчика🙋🏻‍♂️)\n{} - {} : {}\nтел. {}'.format(
                        ad[1], ad[2], ad[3],
                        month(ad[4]),
                        ad[6])
                expandK = types.InlineKeyboardMarkup().add(
                    (types.InlineKeyboardButton('Раскрыть', callback_data=f'expand{ad[1]}')))
                send_message(text,
                    message, expandK,
                    state='search')
        if ad[7].find('Air') != -1:
            if ad[7].find('Send') != -1:
                expandK = types.InlineKeyboardMarkup().add(
                    (types.InlineKeyboardButton('Раскрыть', callback_data=f'expand{ad[1]}')))
                send_message('Заявка  №{} ✈ Хочу отправить \n{} - {} : {}'.format(ad[1], ad[2], ad[3], month(ad[4])),
                             message, expandK,
                             state='search')
            if ad[7].find('Dely') != -1:
                expandK = types.InlineKeyboardMarkup().add(
                    (types.InlineKeyboardButton('Раскрыть', callback_data=f'expand{ad[1]}')))
                send_message(
                    'Заявка  №{} ✈ Могу доставить \n{} - {} : {}'.format(ad[1], ad[2], ad[3],
                                                                         month(ad[4])),
                    message, expandK,
                    state='search')'''