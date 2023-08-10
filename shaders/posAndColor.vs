#version 330 core
in vec3 a_Position;
in vec4 a_Color;
out vec4 v_Color;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main() { 
    gl_Position = projection * view * model * vec4(a_Position, 1.0); // gl_Position是内置变量
    v_Color = a_Color;
}