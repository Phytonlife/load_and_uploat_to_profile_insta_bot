import instaloader
import os
from time import sleep
from random import uniform, choice, randint
import schedule
import time
from instagrapi import Client

# Часть 1: Скачивание фото из профиля целевого пользователя

def get_last_downloaded_index(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return int(file.read().strip())
    return -1

def set_last_downloaded_index(file_path, index):
    with open(file_path, 'w') as file:
        file.write(str(index))

def download_photo(target_username, output_dir, index_file):
    L = instaloader.Instaloader(download_pictures=True, download_videos=False,
                                download_video_thumbnails=False, download_geotags=False,
                                download_comments=False, save_metadata=False,
                                post_metadata_txt_pattern="")

    # Создать папку, если она не существует
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Настроить папку для сохранения изображений
    L.dirname_pattern = output_dir

    # Получить профиль
    profile = instaloader.Profile.from_username(L.context, target_username)
    posts = list(profile.get_posts())

    last_index = get_last_downloaded_index(index_file)
    next_index = last_index + 1

    if next_index < len(posts):
        post = posts[next_index]
        L.download_post(post, target=target_username)
        set_last_downloaded_index(index_file, next_index)
        return True
    else:
        print("No more posts to download.")
        return False

# Часть 2: Загрузка фото в ваш профиль и удаление его

def upload_photo(cl, folder_path):
    praises = [
        "Наше оформление получилось великолепным! 🌟",
        "Посмотрите, какое изящное и стильное украшение! ✨",
        "Каждая деталь декора подобрана с огромной любовью и вниманием к мелочам. ❤️",
        "Этот декор добавляет волшебства и элегантности любому пространству! 🪄",
        "У нас получилось создать настоящее произведение искусства! 🎨",
        "Это оформление точно привлечет всеобщее внимание и восхищение. 👀",
        "Какое изысканное сочетание цветов и текстур! 🌈",
        "Каждый элемент декора отражает нашу страсть и креативность. 🌟",
        "Наше оформление подчеркивает уникальность и индивидуальность этого пространства. 🏠",
        "Это просто фантастическое оформление! Сложно отвести взгляд. 😍",
        "Каждая деталь здесь создана для того, чтобы радовать глаз. 😊",
        "Это настоящий праздник для любителей стильного декора! 🎉",
        "Наше оформление придает особую атмосферу и уют. 🏡",
        "Этот декор создан для того, чтобы вдохновлять и радовать. 💖",
        "У нас получилось создать гармоничное и утонченное оформление! 🌸",
        "Каждая деталь говорит о высоком уровне мастерства и вкуса. 💎",
        "Такое красивое оформление просто не может не нравиться! 😍",
        "Этот декор превращает любое пространство в сказку. 🏰",
        "Наше оформление – это воплощение красоты и элегантности. 🌹",
        "Мы гордимся тем, что создали такой потрясающий декор! 🎉",
        "Біздің дизайн керемет болды! 😍",
        "Мынау қандай әдемі және стильді безендіру! ✨",
        "Әрбір детальге үлкен махаббат пен ұқыптылықпен назар аударылған. ❤️",
        "Бұл декор кез-келген кеңістікке сиқыр мен әсемдік қосады! ✨",
        "Біз нағыз өнер туындысын жасадық! 🎨",
        "Бұл безендіру барлығын өзіне қарататыны сөзсіз. 👀",
        "Қандай нәзік түстер мен текстуралардың үйлесімі! 🌈",
        "Әрбір декор элементі біздің құмарлығымыз бен шығармашылығымызды көрсетеді. 🌟",
        "Біздің безендіру осы кеңістіктің бірегейлігі мен даралығын көрсетеді. 🌟",
        "Бұл тек қиял ғажайып безендіру! Көзді ала алмайсың. 😲",
        "Мұндағы әрбір деталь көзді қуантады. 😊",
        "Бұл нағыз стильді декорды сүйетіндерге арналған мереке! 🎉",
        "Біздің безендіру ерекше атмосфера мен жайлылық береді. 🏡",
        "Бұл декор шабыттандыру және қуаныш сыйлау үшін жасалған. 💖",
        "Біз үйлесімді және нәзік безендіру жасадық! 🌸",
        "Әрбір деталь жоғары деңгейдегі шеберлік пен талғамды көрсетеді. 💎",
        "Мұндай әдемі безендіру тек ұнамауы мүмкін емес! 😍",
        "Бұл декор кез келген кеңістікті ертегіге айналдырады. 🏰",
        "Біздің безендіру – бұл сұлулық пен әсемдіктің бейнесі. 🌹",
        "Біз осындай таңғажайып декор жасағанымызға мақтанамыз! 🎉"
    ]
    hashtags = "#Атырау#Atyrau#ОформлениеАтырау#БаннерАтырау#Atyraudecor#АтырауОформление#ТойАтырау#АтырауТой#"

    for filename in os.listdir(folder_path):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            photo_path = os.path.join(folder_path, filename)
            caption = f"{choice(praises)} {hashtags}"

            print(f"Загружаем {photo_path} с описанием: {caption}")
            try:
                cl.photo_upload(photo_path, caption)
                print(f"Успешно загружено {photo_path}")

                # Удаляем фото после успешной загрузки
                os.remove(photo_path)

                # Загружаем только одно фото и завершаем функцию
                return
            except Exception as e:
                print(f"Не удалось загрузить {photo_path}: {e}")

# Часть 3: Запланировать выполнение задачи с интервалами от 12 до 16 часов

def job():
    target_username = 'asruamina3'
    output_dir = 'images'
    index_file = 'last_downloaded_index.txt'

    # Скачать фото
    if not download_photo(target_username, output_dir, index_file):
        return  # Остановить выполнение, если больше нет постов для скачивания

    # Инициализировать клиента Instagrapi и войти в аккаунт
    username = "oformlenieatyrau06"
    password = "a9326191"
    cl = Client()
    cl.login(username, password)

    # Загрузить скачанное фото
    upload_photo(cl, output_dir)

# Запланировать выполнение задачи
def schedule_job():
    job()
    next_run_in = randint(12, 16) * 3600  # Случайное время от 12 до 16 часов в секундах
    print(f"Следующий запуск через: {next_run_in / 3600} часов")
    schedule.every(next_run_in).seconds.do(job)

# Первоначальное выполнение задачи и планирование следующих запусков
schedule_job()

# Бесконечный цикл для поддержания работы скрипта и проверки расписания
while True:
    schedule.run_pending()
    time.sleep(60)  # Проверка расписания каждую минуту
