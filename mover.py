import rospy # Импортируем библиотеку ROS
from geometry_msgs.msg import Twist # Импортируем тип сообщения Twist для управления движением
from nav_msgs.msg import Odometry # Импортируем тип сообщения Odometry для получения информации о позиции
from tf.transformations import euler_from_quaternion # Используем эту функцию для вычисления углов эйлера
import math # Используем математические функции для вычислений

class Robot:
   def __init__(self, id):
       self.id = id # Идентификатор комбайна
       self.x = 0 # Начальная координата X
       self.y = 0 # Начальная координата Y
       self.z = 0 # Начальная координата Z
       self.roll = 0 # Начальный угол крена
       self.pitch = 0 # Начальный угол тангажа
       self.yaw = 0 # Начальный угол рысканья
       self.radius = 25 # Радиус поворота
       self.angular_velocity = 0.5 # Угловая скорость поворота
       self.linear_velocity = 0.1 # Линейная скорость движения
       self.curr_angle = id * (2 * math.pi/3) # Текущий угол поворота, начальное значение отличается для каждого комбайна

def odom_callback(self, msg):
# Call back функция, которая получает информацию о позиции
   self.x = msg.pose.pose.position.x # Получаем координату X
   self.y = msg.pose.pose.position.y # Получаем координату Y
   self.z = msg.pose.pose.position.z # Получаем координату Z
   rot_q = msg.pose.pose.orientation # Получаем кватернион поворота комбайна
   (self.roll, self.pitch, self.yaw) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w]) # Вычисляем углы крена, тангажа и рысканья

def turn(self, angle, duration, cmd_pub):
# Функция поворота на заданный угол
   vel_msg = Twist() # Создаем объект сообщения Twist для отправки управляющих команд на комбайн
   vel_msg.angular.z = self.angular_velocity * abs(angle)/angle # Устанавливаем угловую скорость со знаком
   t0 = rospy.Time.now().to_sec() # Получаем текущее время
   current_angle = 0 # Начальное значение текущего угла поворота
   while current_angle < abs(angle): # Поворачиваем до тех пор, пока текущий угол не станет равным заданному
       cmd_pub.publish(vel_msg) # Отправляем управляющие команды на комбайн
       t1 = rospy.Time.now().to_sec() # Получаем текущее время
       current_angle = abs(vel_msg.angular.z) * (t1 - t0) # Вычисляем текущий угол поворота
       vel_msg.angular.z = 0 # Устанавливаем нулевую угловую скорость
       cmd_pub.publish(vel_msg) # Отправляем команду на остановку поворота

def move(self, distance, cmd_pub):
   # Функция движения на заданное расстояние
   vel_msg = Twist() # Создаем объект сообщения Twist для отправки управляющих команд на комбайн
   vel_msg.linear.x = self.linear_velocity # Устанавливаем линейную скорость со знаком
   t0 = rospy.Time.now().to_sec() # Получаем текущее время
   current_distance = 0 # Начальное значение текущего расстояния
   while current_distance < distance: # Движемся до тех пор, пока не пройдем заданное расстояние
       cmd_pub.publish(vel_msg) # Отправляем управляющие команды на комбайн
       t1 = rospy.Time.now().to_sec() # Получаем текущее время
       current_distance = vel_msg.linear.x * (t1 - t0) # Вычисляем текущее расстояние
       vel_msg.linear.x = 0 # Устанавливаем нулевую линейную скорость
       cmd_pub.publish(vel_msg) # Отправляем команду на остановку движения

def ackermann_steering_angle(self):
# Функция вычисления угла поворота с помощью функции Аккермана
   turning_radius = self.radius # Радиус поворота
   wheelbase_length = 2.8 # Длина между колесами
   steering_angle = self.curr_angle + math.atan(wheelbase_length / turning_radius) # Вычисляем угол поворота для передних колес
   return steering_angle # Возвращаем угол поворота

def move_in_circle(self, cmd_pub):
# Функция движения по круговому маршруту
   distance = math.pi * self.radius # Вычисляем длину окружности
   self.move(distance, cmd_pub) # Двигаемся по окружности
   self.turn(math.pi, 2, cmd_pub) # Поворачиваем на 180 градусов
   self.curr_angle += math.pi # Обновляем текущий угол поворота для следующего круга

def main():
   robots = []
   for i in range(3):
       robot = Robot(i) # Создаем объекты для каждого комбайна и добавляем их в список
       robots.append(robot)
       rospy.init_node('robot_mover', anonymous=True) # Инициализируем узел ROS с именем "robot_mover"

cmd_pubs = []
odom_subs = []
for i in range(3):
   cmd_pub = rospy.Publisher('/robot' + str(i+1) + '/cmd_vel', Twist, queue_size=10) # Создаем тему cmd_vel для отправки управляющих команд на комбайн
   cmd_pubs.append(cmd_pub) # Добавляем объект Publisher в список
   odom_sub = rospy.Subscriber('/robot' + str(i+1) + '/odom', Odometry, robots[i].odom_callback) # Создаем тему odom для получения информации о позиции
   odom_subs.append(odom_sub) # Добавляем объект Subscriber в список

rate = rospy.Rate(10) # Устанавливаем частоту опроса в 10 Гц

while not rospy.is_shutdown():
   for robot in robots:
       robot.move_in_circle(cmd_pubs[robot.id]) # Двигаем каждый комбайн по круговому маршруту, используя его собственный объект Publisher
       rate.sleep() # Останавливаем выполнение на заданное время для соблюдения частоты опроса

if __name__ == '__main__':
   try:
main() # Запускаем основную программу
except rospy.ROSInterruptException:
   pass
