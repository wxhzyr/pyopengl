#version 330 core
out vec3 FragColor;

in float fId;

uniform float rate;
void main()
{   
    float tmp = fId;
    FragColor = vec3(tmp / rate, tmp / rate, 1.0f);
}