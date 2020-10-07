from users import connectDB
from users import User
import datetime
import sqlalchemy as sa 
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_
from sqlalchemy.ext.declarative import declarative_base
"""Импортируем функцию соединения с базой и описание таблицы user"""
DB_PATH="sqlite:///sochi_athletes.sqlite3"
Base=declarative_base()
class Athelete(Base):
	"""Описываем таблицу athlete"""
	__tablename__= "athelete"
	id=sa.Column(sa.INTEGER,primary_key=True)
	age=sa.Column(sa.INTEGER)
	birthdate=sa.Column(sa.TEXT)
	gender=sa.Column(sa.TEXT)
	height=sa.Column(sa.REAL)
	name=sa.Column(sa.TEXT)
	weight=sa.Column(sa.INTEGER)
	gold_medals=sa.Column(sa.INTEGER)
	silver_medals=sa.Column(sa.INTEGER)
	bronze_medals=sa.Column(sa.INTEGER)
	total_medals=sa.Column(sa.INTEGER)
	sport=sa.Column(sa.TEXT)
	country=sa.Column(sa.TEXT)
	
def request_user_id(session):
	"""Запрашиваем ID пользователя ,находим его и выводим и возвращаем"""
	id_user=input("Введите ID пользователя: ")
	user=session.query(User).filter(User.id==id_user).first()
	if user is None:
		print ("Пользователя с таким ID не найдено")
	else:
		print("Имя:{} {} \nДата рождения: {}\nПол: {}\nРост в метрах {}\n".format(user.first_name,user.last_name,user.birthdate,user.gender,user.height))	
	return user
	
	

def height_plus(height):
	"""Увеличивает рост пользователя на 1 см """
	user_height_inc=round((height+0.01),3)
	return user_height_inc
def height_minus(height):
	"""Уменьшает рост пользователя на 1 см """
	user_height_dec=round((height-0.01),3)
	return user_height_dec	

def find_athelete_height(user):
	"""Проверяем есть ли в базе атлет с таким ростом,если нет то вызываем функции прибавить/убавить 1 см и сравниваем опять пока не найдем нужного""" 
	ath_height=session.query(Athelete).filter(Athelete.height==user.height).first()
	if ath_height is None:
		user_height_plus=user.height
		user_height_minus=user.height
		while ath_height is None:
			user_height_plus=height_plus(user_height_plus)
			user_height_minus=height_minus(user_height_minus)
			ath_height=session.query(Athelete).filter(or_(Athelete.height==user_height_plus,Athelete.height==user_height_minus)).first()
	print("Ближайший атлет к пользователю по росту - {}, с ростом {} м".format(ath_height.name,ath_height.height))
def date_plus_day(string):
	"""Прибавляем 1 день к дате рождения пользователя,для этого переводим в дату строку,прибавляем день и переводим обратно в строку"""
	iso_date=datetime.datetime.strptime(string,"%Y-%m-%d")
	day_plus_one=datetime.timedelta(days=1)
	new_date=iso_date+day_plus_one
	new_str_date=str(new_date).split(' ')
	return new_str_date[0]

def date_minus_day(string):
	"""Убавляем 1 день от даты рождения пользователя,для этого переводим в дату строку,убавляем день и переводим обратно в строку"""
	iso_date=datetime.datetime.strptime(string,"%Y-%m-%d")
	day_minus_one=datetime.timedelta(days=1)
	new_date=iso_date-day_minus_one
	new_str_date=str(new_date).split(' ')
	return new_str_date[0]	

def find_athelete_birthdate(user):
		"""Проверяем есть ли в базе атлет с такой датой рождения,если нет то вызываем функции прибавить/убавить 1 день и сравниваем опять пока не найдем нужного""" 

		ath_birthdate=session.query(Athelete).filter(Athelete.birthdate==user.birthdate).first()
		
		if ath_birthdate is None:
			user_date_plus=user.birthdate
			user_date_minus=user.birthdate
			
			while ath_birthdate is None :

				user_date_plus=date_plus_day(user_date_plus)
				user_date_minus=date_minus_day(user_date_minus)
				ath_birthdate=session.query(Athelete).filter(or_(Athelete.birthdate==user_date_plus,Athelete.birthdate==user_date_minus )).first()
			print("Ближайший атлет к пользователю по дате рождения - {}, с датой {}".format(ath_birthdate.name,ath_birthdate.birthdate))		
	
if __name__=="__main__":
	session=connectDB(DB_PATH)	
	user=request_user_id(session)
	find_athelete_height(user)
	find_athelete_birthdate(user)






