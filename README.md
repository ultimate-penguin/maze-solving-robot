# Autonomous Maze-Solving Mobile Robot

A sensor-driven autonomous mobile robot simulation built from scratch using **ROS 2 (C++)** and **Gazebo Harmonic**. The robot employs a reactive **Left-Wall Following** control architecture, processing real-time 360° LiDAR data to navigate complex unknown environments and avoid obstacles dynamically.



https://github.com/user-attachments/assets/2fa15dab-3b51-481a-bdaa-e7d3794486dc





---

## 🚀 Key Engineering Highlights
- **ROS 2 C++ Development:** Built modular C++ nodes in ROS 2 to run real-time sensor loops and handle incoming data instantly as it arrives.
- **Sensor Data Integration:** Connected a simulated 360° LiDAR sensor from Gazebo to ROS 2, turning raw laser data into clean front, left, and right distance readings to track nearby walls.
- **Autonomous Movement Control:** Created a decision-making system that turns distance readings into smooth steering commands, helping the robot navigate hallways and follow walls automatically.
- **Physics & Stability Tuning:** Fixed robot jitter and wall-clipping issues in the simulation by organizing decision priorities and smoothing out speed changes.
---

## 🛠️ Tech Stack & Architecture
* **OS:** Ubuntu (Linux)
* **Middleware:** ROS 2 (Jazzy)
* **Simulation Engine:** Gazebo Harmonic
* **Key Packages:** `rclcpp`, `sensor_msgs`, `geometry_msgs`, `ros_gz_bridge`

---

## 🧠 Algorithmic Logic (Left-Wall Follower)
The control node runs on a fast, real-time loop checking incoming laser scans, using a simple priority rule system to navigate:
1. **Front Obstacle Check:** If a wall is directly ahead, the robot pivots right until the path is clear. It ignores minor side-sensor flickers to prevent jerky movements.
2. **Left Opening Detection:** If the left side opens up, it moves forward while turning left to explore the hallway.
3. **Wall-Hugging Mode:** If the left side is blocked and the front is clear, it drives straight to maintain a steady path alongside the wall.
---

## 📦 Installation & Setup

### Prerequisites
* ROS 2 installed (Jazzy)
* Gazebo Harmonic
* `ros_gz_bridge` package

### 1. Clone the Repository
cd ~/ros2_ws/src <br>
git clone https://github.com/ultimaze-penguin/maze-solving-robot.git

### 2. Build the Package
cd ~/ros2_ws<br>
colcon build --packages-select maze_bot<br>
source install/setup.bash<br>

### 3. Run the Simulation & Control Node
Terminal 1 (Launch Gazebo simulation):<br>
ros2 launch maze_bot maze_sim.launch.py<br>
Terminal 2 (Launch the motion controller node):<br>
ros2 run maze_bot motion_controller

---
## 🔮 Future Enhancements
- [ ] **Grid Mapping:** Build a live occupancy map using real-time LiDAR data.
- [ ] **Global Path Planning:** Upgrade from reactive wall-following to smart map routing using Dijkstra's algorithm.
- [ ] **Velocity & Physics Tuning:** Refine linear speed caps and collision boundaries to handle higher speeds without wheel clipping or wall trapping in simulation.
---

## 👤 Author
**Ultimate Penguin**  
[https://github.com/ultimate-penguin]
