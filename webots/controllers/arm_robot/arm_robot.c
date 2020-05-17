/*
 * File:          arm_robot.c
 * Date:
 * Description:
 * Author:
 * Modifications:
 */

/*
 * You may need to add include files like <webots/distance_sensor.h> or
 * <webots/motor.h>, etc.
 */
#include <webots/robot.h>
#include <webots/motor.h>
/*
 * You may want to add macros here.
 */
#define TIME_STEP 1

int main(int argc, char **argv) {
  /* necessary to initialize webots stuff */
  wb_robot_init();

 
  WbDeviceTag wheel1;
  WbDeviceTag wheel2;
  WbDeviceTag wheel3;
  WbDeviceTag wheel4;
  
  WbDeviceTag arm1;
  WbDeviceTag arm2;
  WbDeviceTag arm3;
  
  

  arm1 = wb_robot_get_device("A motor");
  arm2 = wb_robot_get_device("B motor");
  arm3 = wb_robot_get_device("C motor");
  
  
  wheel1 = wb_robot_get_device("wheel1");
  wheel2 = wb_robot_get_device("wheel2");
  wheel3 = wb_robot_get_device("wheel3");
  wheel4 = wb_robot_get_device("wheel4");
  
  
 
  wb_motor_set_position(wheel1,INFINITY);
  wb_motor_set_position(wheel2,INFINITY);
  wb_motor_set_position(wheel3,INFINITY);
  wb_motor_set_position(wheel4,INFINITY);
  
 
  
  
  double p1=1.6;
  double p2=-1.57;
  double p3=-3.14;
  
  
  //wb_motor_set_position(arm1,p1);
  //wb_motor_set_position(arm2,p2);
  //wb_motor_set_position(arm3,p3);  
  
  
  while (wb_robot_step(TIME_STEP) != -1) {
    /*
     * Read the sensors :
     * Enter here functions to read sensor data, like:
     *  double val = wb_distance_sensor_get_value(my_sensor);
     */

    /* Process sensor data here */
    
    //速度分解以及机械臂位置控制
    
    //第一阶段
    if(p1<3.14 && p2<-1.21 && p3>-3.5)
    {
      p1+=0.0154;
      p2+=0.0036;
      p3-=0.0036;
    }
    //第二阶段
    else if(p3>-6.5)
    {
    
      p3-=0.03;
    
    }
    
     
    
      
     
    
    wb_motor_set_velocity(wheel1,0);
    wb_motor_set_velocity(wheel2,0);
    wb_motor_set_velocity(wheel3,0);
    wb_motor_set_velocity(wheel4,0);
    
    wb_motor_set_position(arm1,p1);
    wb_motor_set_position(arm2,p2);
    wb_motor_set_position(arm3,p3);  
    
    
   
    /*
     * Enter here functions to send actuator commands, like:
     * wb_motor_set_position(my_actuator, 10.0);
     */
  };

  /* Enter your cleanup code here */

  /* This is necessary to cleanup webots resources */
  wb_robot_cleanup();

  return 0;
}
