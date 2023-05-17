import imaplib
import email

mail_pass = input("Введите пароль для внешних приложений: ")  # Пароль для внешних приложений 
username = input("Введите почту: ")  # почта
year_to_delete = input("Введите год на удаление: ")
imap_server = "imap.mail.ru"

m = imaplib.IMAP4_SSL(imap_server)
m.login(username, mail_pass) # подключаемся к почте

# получаем доступные ящики
list_of_mailboxes = m.list()
print(list_of_mailboxes)
# выбор ящика с которого нужно удалить письма
m.select("INBOX/Social")
# ищем все письма и получаем их uid
resp, data = m.uid('search', None, "ALL")
if resp == 'OK':
    uids = data[0].split()
    # цикл на поиск и удаление писем
    for i, uid in enumerate(uids):
        print(f"{i+1}/{len(uids)}")
        resp, data = m.uid('fetch', uid, "(BODY[HEADER])")
        # print(resp, data[0][1])
        msg = email.message_from_bytes(data[0][1])
        # если с письма не удается получить дату, программа его пропускает
        try:
            year = msg['Date'].split()[3]
            #print(year)
            if year == year_to_delete:
                m.uid('STORE', uid, '+FLAGS', '(\\Deleted)')
        except:
            print('nope')
            continue
    print(m.expunge())
    print(f"удалено {len(m.expunge()) - 1} писем") # сколько писем удалилось
    m.close()  # закрываем почтовый ящик
    m.logout()  # выходим из него
else:
    m.close()  # закрываем почтовый ящик
    m.logout()  # выходим из него
