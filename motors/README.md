# Motors API for ROS

```

      ___           ___                 
     /\  \         /\  \          ___   
    /::\  \       /::\  \        /\  \  
   /:/\:\  \     /:/\:\  \       \:\  \ 
  /::\~\:\  \   /::\~\:\  \      /::\__\
 /:/\:\ \:\__\ /:/\:\ \:\__\  __/:/\/__/
 \/__\:\/:/  / \/__\:\/:/  / /\/:/  /   
      \::/  /       \::/  /  \::/__/    
      /:/  /         \/__/    \:\__\    
     /:/  /                    \/__/    
     \/__/                              

```

## Topics
### OUT
 * /odom type:nav_msgs/Odometry - одометрия
 * /encoder1 type:std_msgs/Float32 - положение в m
 * /encoder2 type:std_msgs/Float32 - положение в m
 * /encoder1_v type:std_msgs/Float32 - скорость в m/s
 * /encoder2_v type:std_msgs/Float32 - скорость в m/s

### IN
 * /motor1 type:std_msgs/Float32 - скорость в m/s
 * /motor2 type:std_msgs/Float32 - скорость в m/s

## Files
Motor.py - работа с моторами \
Odometry_calc.py - мат. модель робота \
PID.py - PID \
motor_ros.py - нода для высокоуровневой работы с моторами
\
\

by Vasily
