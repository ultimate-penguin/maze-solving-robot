#!/usr/bin/env python3
import random
import sys
import os

def generate_maze_sdf(width=5, height=5, cell_size=2.0, wall_height=1.5, wall_thickness=0.1):
    # Simple grid representation for maze generation
    # For a grid of W x H cells, we have vertical and horizontal walls.
    
    # Initialize grid walls (True means wall exists)
    v_walls = [[True for _ in range(width + 1)] for _ in range(height)]
    h_walls = [[True for _ in range(width)] for _ in range(height + 1)]
    
    visited = [[False for _ in range(width)] for _ in range(height)]
    
    # Depth-First Search (DFS) maze generation
    def carve(cx, cy):
        visited[cy][cx] = True
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < width and 0 <= ny < height and not visited[ny][nx]:
                # Remove wall between (cx, cy) and (nx, ny)
                if dx == 1:
                    v_walls[cy][cx + 1] = False
                elif dx == -1:
                    v_walls[cy][cx] = False
                elif dy == 1:
                    h_walls[cy + 1][cx] = False
                elif dy == -1:
                    h_walls[cy][cx] = False
                carve(nx, ny)

    carve(0, 0)
    # Create an entrance/exit by removing outer boundary walls
    h_walls[0][0] = False            # Opens an exit at the bottom-left start
    h_walls[height][width - 1] = False # Opens an exit at the top-right finish
    
    # Start building SDF content
    sdf_lines = [
        '<?xml version="1.0" ?>',
        '<sdf version="1.9">',
        '  <world name="generated_maze_world">',
        '    <physics name="1ms" type="override">',
        '      <max_step_size>0.001</max_step_size>',
        '      <real_time_factor>1.0</real_time_factor>',
        '    </physics>',
        '    <plugin filename="libgz-sim-physics-system.so" name="gz::sim::systems::Physics"/>',
        '    <plugin filename="libgz-sim-user-commands-system.so" name="gz::sim::systems::UserCommands"/>',
        '    <plugin filename="libgz-sim-scene-broadcaster-system.so" name="gz::sim::systems::SceneBroadcaster"/>',
        '',
        '    <include>',
        '      <uri>https://fuel.gazebosim.org/1.0/OpenRobotics/models/Sun</uri>',
        '    </include>',
        '    <include>',
        '      <uri>https://fuel.gazebosim.org/1.0/OpenRobotics/models/Ground Plane</uri>',
        '    </include>'
    ]
    
    wall_id = 0
    
    # Add outer boundary and internal vertical walls
    for r in range(height):
        for c in range(width + 1):
            if v_walls[r][c]:
                # Calculate position
                x = (c * cell_size) - (width * cell_size / 2.0)
                y = (r * cell_size) - (height * cell_size / 2.0) + (cell_size / 2.0)
                z = wall_height / 2.0
                
                wall_xml = f"""
    <model name="v_wall_{wall_id}">
      <static>true</static>
      <pose>{x} {y} {z} 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry><box><size>{wall_thickness} {cell_size} {wall_height}</size></box></geometry>
        </collision>
        <visual name="visual">
          <geometry><box><size>{wall_thickness} {cell_size} {wall_height}</size></box></geometry>
        </visual>
      </link>
    </model>"""
                sdf_lines.append(wall_xml)
                wall_id += 1

    # Add horizontal walls
    for r in range(height + 1):
        for c in range(width):
            if h_walls[r][c]:
                x = (c * cell_size) - (width * cell_size / 2.0) + (cell_size / 2.0)
                y = (r * cell_size) - (height * cell_size / 2.0)
                z = wall_height / 2.0
                
                wall_xml = f"""
    <model name="h_wall_{wall_id}">
      <static>true</static>
      <pose>{x} {y} {z} 0 0 1.5708</pose>
      <link name="link">
        <collision name="collision">
          <geometry><box><size>{wall_thickness} {cell_size} {wall_height}</size></box></geometry>
        </collision>
        <visual name="visual">
          <geometry><box><size>{wall_thickness} {cell_size} {wall_height}</size></box></geometry>
        </visual>
      </link>
    </model>"""
                sdf_lines.append(wall_xml)
                wall_id += 1

    sdf_lines.append('  </world>')
    sdf_lines.append('</sdf>')
    
    return "\n".join(sdf_lines)

if __name__ == "__main__":
    # Generate a 6x6 maze
    maze_sdf = generate_maze_sdf(width=6, height=6, cell_size=1.5, wall_height=1.0)
    
    output_filename = "worlds/maze_generated.sdf"
    if len(sys.argv) > 1:
        output_filename = sys.argv[1]
        
    with open(output_filename, "w") as f:
        f.write(maze_sdf)
    print(f"Maze SDF successfully generated and saved to {output_filename}")