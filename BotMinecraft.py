from javascript import require, On, Once, once
import time
import threading

from googletrans import Translator
translator = Translator()

Bot_Name = "My_Py_Bot"

MineFlayer = require('MineFlayer')
pathfinder = require('MineFlayer-pathfinder')
GoalFollow = pathfinder.goals.GoalFollow

bot = MineFlayer.createBot({
    'host':'Your_Host',
    'port': 'Your_Port',
    'username': Bot_Name,
    'version':'1.16.5'
})

bot.loadPlugin(pathfinder.pathfinder)

@On(bot, 'spawn')
def spawn(*args):
    mcData = require('minecraft-data')(bot.version)
    movements = pathfinder.Movements(bot, mcData)
    
    @On(bot, 'chat')
    def msgHandler(this, user, message, *args):
        player = bot.players[user]
        if user != Bot_Name:
            if 'Подойди' in message:
                player = bot.players[user]
                target = player.entity

                bot.pathfinder.setMovements(movements)
                goal = GoalFollow(target, 1)
                bot.pathfinder.setGoal(goal, True)
                
            elif 'Остановись' in message:
                # Как только бот достигнет цели, остановим его движение
                bot.pathfinder.stop()

            elif message == 'Выйди':
                bot.chat("Всем пока!")
                time.sleep(3)
                bot.end()  # Выход с сервера

            elif 'ТП ко мне' in message:
                time.sleep(1)
                bot.chat('Лады, пару сек')
                time.sleep(3)
                bot.chat(f'/tp {user}')
                time.sleep(1)
                bot.chat('Я тут!')
                Time = 0
                while Time < 6:
                      # Смотрим на игрока
                    bot.lookAt(player.entity.position.offset(0, player.entity.height, 0))
                    time.sleep(0.5)
                    Time += 1

attacked_mobs = {} #Словарь с мобами который были атакованы

# Функция, которая будет сбрасывать записи о мобах из attacked_mobs через определенное время
def reset_attacked_mobs():
    global attacked_mobs
    attacked_mobs = {}

@On(bot, "entityHurt")
def entityHurt(this, entity):
    global attacked_mobs

    if entity.type == "mob":
        mob_uuid = entity.uuid
        
        # Проверяем, не был ли моб уже атакован
        if mob_uuid not in attacked_mobs:
            mob_name = translator.translate(entity.displayName, dest='ru').text
            bot.chat(f"Где-то рядом {mob_name}")
            
            # Добавляем моба в словарь attacked_mobs
            attacked_mobs[mob_uuid] = True
            
            # Запускаем таймер для сброса записи о мобе из attacked_mobs через 30 секунд
            threading.Timer(30, reset_attacked_mobs).start()

    elif entity.type == "player":
        if entity.username in bot.players:
            bot.chat("Меня бъют")

while True:
    pass
