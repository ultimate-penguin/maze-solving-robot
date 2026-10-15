#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/laser_scan.hpp"

class WallDetector : public rclcpp::Node
{
public:
    WallDetector() : Node("wall_detector")
    {
        // Subscribe to the /scan topic published by Gazebo
        subscription_ = this->create_subscription<sensor_msgs::msg::LaserScan>(
            "/scan", 10, std::bind(&WallDetector::scan_callback, this, std::placeholders::_1));
        
        RCLCPP_INFO(this->get_logger(), "Wall Detector Node Initialized.");
    }

private:
    void scan_callback(const sensor_msgs::msg::LaserScan::SharedPtr msg) const
    {
        if (msg->ranges.empty()) return;

        int total_samples = msg->ranges.size();

        // Assuming 360 samples uniformly distributed:
        // Index 0 = Front, 90 = Left, 180 = Back, 270 = Right
        float front = msg->ranges[0];
        float left  = msg->ranges[total_samples / 4];       // ~90 degrees
        float back  = msg->ranges[total_samples / 2];       // ~180 degrees
        float right = msg->ranges[3 * total_samples / 4];   // ~270 degrees

        float threshold = 0.4; // Distance threshold in meters

        // Determine wall (1) or open space (0)
        int f_wall = (front < threshold) ? 1 : 0;
        int l_wall = (left < threshold) ? 1 : 0;
        int b_wall = (back < threshold) ? 1 : 0;
        int r_wall = (right < threshold) ? 1 : 0;

        // Print wall status
        RCLCPP_INFO(this->get_logger(), "Walls -> Front: %d, Left: %d, Back: %d, Right: %d",
                    f_wall, l_wall, b_wall, r_wall);
    }

    rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr subscription_;
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<WallDetector>());
    rclcpp::shutdown();
    return 0;
}