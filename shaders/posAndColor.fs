#version 330 core
in vec4 v_Color;
        
void main() { 
    gl_FragColor = v_Color;  // gl_FragColor是内置变量
}