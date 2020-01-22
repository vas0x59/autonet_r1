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
emergency_main type:Bool - аварийная остановка \
grab/cmd       type:String - тут мы ждем сообщение "take" для захвата и "throw" для выгрузки.
## FILES
#### TODO
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

### Code style
#### PYTHON 3!!!!!!! LINUX!!!!!!!
 - все радикальные изменения делаем в отдельной ветке !!!
 - разделяем код на классы 
 - делаем код кроссплатформенным (что-бы и на raspberry и на компе нормально работало!!!) 
 - создаем конфиг файлы для параметров (json наверное) (что-бы в коде долго не искать)
 - раскидываем все по папкам !!!
 - называть файлы нормльно (а не raaxcsdsline_qwertyBuratino-er_werpqsxwfec.py, q1.py, sdfsd23.py) !!!
 - все что сделали описывайте в changlog
 - реализовывать код в виде мат моделей узлов (манипулятор и колесная база)(все параметры в конфиги))))

### Архитектура 
#### TODO

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

