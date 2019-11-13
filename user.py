
'''импортируем нужные модули'''
import os
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = 'sqlite:///sochi_athletes.sqlite3'
Base = declarative_base()

class User (Base):
	__tablename__ = 'user'

	id = sa.Column(sa.Integer, primary_key=True)
	first_name = sa.Column(sa.TEXT)
	last_name = sa.Column(sa.TEXT)
	gender = sa.Column(sa.TEXT)
	email = sa.Column(sa.TEXT)
	birthdate = sa.Column(sa.TEXT)
	height = sa.Column(sa.Float)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    
    return session()

'''функция ввода нового пользователя'''
def request_user_data ():
	print ('Привет! Сейчас я запишу твои данные.')
	
	first_name = input('Введите имя:')
	last_name = input('Введите фамилию:')
	gender = input('Ваш пол:')

	for count in range(3):
		email = input('Ваш email:')
		if email.count('@') == 1:
			if len(email.split('@')) > 1 and '.' in email.split('@')[-1]:
				print ('Валидный адрес почты')
				break
			else:
				print('Некорреткный адрес. Проверьте адрес и повторите снова')
		else:
			print('Некорреткный адрес. Проверьте адрес и повторите снова')
			continue

	birthdate = input('Дата рождения в формате (ЧЧ-ММ-ГГГГ):')

	height = input('Рост:')

	user = User(
		first_name = first_name,
		last_name = last_name,
		gender = gender,
		email = email,
		birthdate = birthdate,
		height = height)
	return user

def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    if os.path.exists('sochi_athletes.sqlite3'):
    	print('Файл БД sochi_athletes.sqlite3 найден')
    	session = connect_db()
    	user = request_user_data()
    	session.add(user)
    	session.commit()
    	print("Спасибо, данные сохранены!")
    	mode = input('Проверить наличие данных в БД? \n1 - Да \n2 - Нет \n')
    	if mode == '1':
    		for name, fullname, gen, eml, brd, het in session.query(User.first_name, User.last_name, User.gender, User.email, User.birthdate, User.height):
    			print (name, fullname, gen, eml, brd, het)
    	elif mode == '2':
    		print('')
    else:
    	print('Файл БД sochi_athletes.sqlite3 не найден ввод не возможен')
   

if __name__ == "__main__":
	main()