import sqlalchemy as sa 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH="sqlite:///sochi_athletes.sqlite3"
Base=declarative_base()
class User(Base):
	"""Описываем таблицу пользователей"""
	__tablename__= "user"
	id=sa.Column(sa.INTEGER,primary_key=True)
	first_name=sa.Column(sa.TEXT)
	last_name=sa.Column(sa.TEXT)
	gender=sa.Column(sa.TEXT)
	email=sa.Column(sa.TEXT)
	birthdate=sa.Column(sa.TEXT)
	height=sa.Column(sa.REAL)

def connectDB(DP_PATH):
	"""Подключение к базе данных""" 	
	engine=sa.create_engine(DB_PATH)
	Sessions=sessionmaker(engine)
	session=Sessions()
	return session
def check_height(height):
	"""Проверка на ввод символов"""
	if ("," or "-" or "'" or ":" or ";"	or "{" or "}" or "[" or "]" or "/" or "?" or "@" or "!" or "<" or ">" or "&" or "%" or "$" or "#") in height:
		return False
	else:
		return True			

def check_date(input_date):
	"""Простая проверка ввода даты"""
	if '-' not in input_date:
		return False
	else:	
		rip_date=input_date.split('-')
		if len(rip_date)==3 and len(rip_date[0])==4 and int(rip_date[1])<=12 and int(rip_date[2])<=31:
			return True
		else:
			return False		

def request_user(session):

	"""Запрашиваем пользователя и записываем в базу"""
	check_h=False
	check_d=False
	f_n_user=input("Введите имя: ")
	l_n_user=input("Введите фамилию: ")
	g_user=input("Введите пол (Male/Female): ")
	email_user=input("Введите email: ")
	while not check_d:
		b_d_user=input("Введите дату рождения(гггг-мм-дд): ")
		check_d=check_date(b_d_user)
	while not check_h:	
		height_user=input("Введите рост в метрах(через точку): ")
		check_h=check_height(height_user)
	user=User(first_name=f_n_user,last_name=l_n_user,gender=g_user,email=email_user,birthdate=b_d_user,height=height_user)
	session.add(user)
	session.commit()
	print("Данные сохранены в БД, ID пользователя - ",user.id)
if __name__=="__main__":
	session=connectDB(DB_PATH)	
	request_user(session)







