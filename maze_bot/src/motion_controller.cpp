#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/laser_scan.hpp"
#include "geometry_msgs/msg/twist.hpp"
class WallDetector : public rclcpp::Node
{
public:
    WallDetector() : Node("wall_detector")
    {
        // Subscribe to the /scan topic published by Gazebo
        subscription_ = this->create_subscription<sensor_msgs::msg::LaserScan>(
            "/scan", 10, std::bind(&WallDetector::scan_callback, this, std::placeholders::_1));
        // Initialize the publisher for velocity commands
        publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("/cmd_vel", 10);
        
        RCLCPP_INFO(this->get_logger(), "Wall Detector Node Initialized.");
    }

private:
    void scan_callback(const sensor_msgs::msg::LaserScan::SharedPtr msg) const
    {
        if (msg->ranges.empty()) return;

        int total_samples = msg->ranges.size();

        // Assuming 360 samples uniformly distributed:
        // Index 0 = Back, 90 = right, 180 = front, 270 = left
        
        float back = msg->ranges[0];
        float right  = msg->ranges[total_samples / 4];       // ~90 degrees
        float front  = msg->ranges[total_samples / 2];       // ~180 degrees
        float left = msg->ranges[3 * total_samples / 4];

        float threshold = 0.8; // Distance threshold in meters
        float critical_stop = 0.4;
        auto twist_msg = geometry_msgs::msg::Twist();
        // --- SAFETY RECOVERY BEHAVIOR ---
        if (front < critical_stop) {
            // EMERGENCY: We are pinned or too close to the front wall! Back up!
            twist_msg.linear.x = -0.3;  // Drive backward
            twist_msg.angular.z = 0.3;  // Turn to escape the wall
            RCLCPP_WARN(this->get_logger(), "Too close! Backing up...");
        }

        // Determine wall (1) or open space (0)
        int f_wall = (front < threshold) ? 1 : 0;
        int l_wall = (left < threshold) ? 1 : 0;
        int b_wall = (back < threshold) ? 1 : 0;
        int r_wall = (right < threshold) ? 1 : 0;
        
        // --- STABILIZED PRIORITIZED LOGIC ---
        if (f_wall) {
            // Rule 1: If front is blocked, TURN RIGHT until it clears. 
           
            twist_msg.linear.x = 0.0;
            twist_msg.angular.z = -0.4; 
        }
        else if (!l_wall) {
            // Rule 2: Front is clear, but left is open -> Curve left into the opening
            twist_msg.linear.x = 0.08;
            twist_msg.angular.z = 0.4;  
        }
        else {
            // Rule 3: Front is clear and left has a wall -> Drive straight 
            twist_msg.linear.x = 0.3;
            twist_msg.angular.z = 0.0;
        }

        // Print wall status for debugging
        RCLCPP_INFO(this->get_logger(), "Walls -> Front: %d, Left: %d, Right: %d | Cmd: lin=%.2f, ang=%.2f",
                    f_wall, l_wall, r_wall, twist_msg.linear.x, twist_msg.angular.z);

        // Publish the velocity command to the robot
        publisher_->publish(twist_msg);


        
        
	    
    }

    rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr subscription_;
    rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr publisher_;
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<WallDetector>());
    rclcpp::shutdown();
    return 0;
}