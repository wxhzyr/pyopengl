#version 330 core
out vec3 FragColor;

in vec4 worldPos;

void main()
{    
    FragColor = vec3(worldPos.x, worldPos.y, worldPos.z) / 20000.0f;
    //FragColor = vec3(0.85f, 0.4f, 0.75f);// / 20000;
}