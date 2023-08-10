#version 330 core
in vec4 a_Position;
in vec4 a_Color;
out vec4 v_Color;
void main() { 
    gl_Position = a_Position; // gl_Position是内置变量
    v_Color = a_Color;
}