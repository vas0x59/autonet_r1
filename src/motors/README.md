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

## Config
config.json
```cpp
{
    "wheel_d": 0.07,
    "robot_W": 0.2,             // ширина робота
    "update_rate": 20,    // частота обнавления данных
    "frame_name": "odom", // -----
    "motor_v_pid": {      // Параметры PID регулятора скорости моторов
        "p": 0.01,
        "i": 0,
        "d": 0
    }
}
```

by Vasily
