#version 330 core
out vec3 FragColor;

// varying float fId;
varying vec3 fPos;
uniform float rate;
void main()
{   
    // float tmp = fId;
    vec3 tmp = fPos;
    FragColor = tmp / rate;
}