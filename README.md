# Autonet Liom Team

```

      ___           ___           ___           ___           ___           ___           ___     
     /\  \         /\__\         /\  \         /\  \         /\__\         /\  \         /\  \    
    /::\  \       /:/  /         \:\  \       /::\  \       /::|  |       /::\  \        \:\  \   
   /:/\:\  \     /:/  /           \:\  \     /:/\:\  \     /:|:|  |      /:/\:\  \        \:\  \  
  /::\~\:\  \   /:/  /  ___       /::\  \   /:/  \:\  \   /:/|:|  |__   /::\~\:\  \       /::\  \ 
 /:/\:\ \:\__\ /:/__/  /\__\     /:/\:\__\ /:/__/ \:\__\ /:/ |:| /\__\ /:/\:\ \:\__\     /:/\:\__\
 \/__\:\/:/  / \:\  \ /:/  /    /:/  \/__/ \:\  \ /:/  / \/__|:|/:/  / \:\~\:\ \/__/    /:/  \/__/
      \::/  /   \:\  /:/  /    /:/  /       \:\  /:/  /      |:/:/  /   \:\ \:\__\     /:/  /     
      /:/  /     \:\/:/  /     \/__/         \:\/:/  /       |::/  /     \:\ \/__/     \/__/      
     /:/  /       \::/  /                     \::/  /        /:/  /       \:\__\                  
     \/__/         \/__/                       \/__/         \/__/         \/__/        liom  2020

```
## Topics
 * /emergency_main type:std_msgs/Bool - аварийная остановка
 * /grab/cmd type:std_msgs/String - тут мы ждем сообщение "take" для захвата и "throw" для выгрузки.
 * /odom type:nav_msgs/Odometry - одометрия 
 * /cam1/image_raw type:sensor_msgs/Image - камера 1 
 * /cam2/image_raw type:sensor_msgs/Image - камера 2
 * /nav type:geometry_msgs/Pose - позиция робота
## Launch
 * motors.launch - запуск системы управления моторами
 * arduino.launch - запуск работы с arduino 
 * nav.launch - система навигации 
 * joy.launch
### Arduino
https://github.com/vas59/autonet_arduino
### Hardware
 - Ardunio Mega 2560 (more pins) or Arduino M0 (faster) or both)))
 - Raspberry pi 3b or 3b+
 - Camera 2x 
 - Range finders (Sharp or Ping or simple HC04)
 - Simple i2c lcd screan for fast debug 
 - Power supply !!! (for servos and for rpi)

### Roadmap
 - lanes detector
 - turns
 - crossroads
 - traffic light and road signs
 - navigation
 - payload delivery
 - parking
 - obstacles avoidance
 - debug tool
 - rviz?
 - urdf?
### Const
1426 - 1 оборот 
## FILES
#### TODO
### Code style
#### PYTHON 3!!!!!!! LINUX!!!!!!!
 - все радикальные изменения делаем в отдельной ветке !!!
 - разделяем код на классы 
 - делаем код кроссплатформенным (что-бы и на raspberry и на компе нормально работало!!!) 
 - создаем конфиг файлы для параметров (json наверное) (что-бы в коде долго не искать)
 - раскидываем все по папкам !!!
 - называть файлы нормльно (а не raaxcsdsline_qwertyBuratino-er_werpqsxwfec.py, q1.py, sdfsd23.py) !!!
 - реализовывать код в виде мат моделей узлов (манипулятор и колесная база)(все параметры в конфиги))))

### Архитектура 
![GitHub Logo](/readme_data/autonet_soft-Navigation system.png)

\
\
\
by Vasily, Viktor, Dmitrii, Georgy
```
    ___       ___       ___       ___   
   /\__\     /\  \     /\  \     /\__\  
  /:/  /    _\:\  \   /::\  \   /::L_L_ 
 /:/__/    /\/::\__\ /:/\:\__\ /:/L:\__\
 \:\  \    \::/\/__/ \:\/:/  / \/_/:/  /
  \:\__\    \:\__\    \::/  /    /:/  / 
   \/__/     \/__/     \/__/     \/__/  

```

