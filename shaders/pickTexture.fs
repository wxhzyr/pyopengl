#version 330 core
out vec3 FragColor;

in vec2 TexCoords;
in float meshID;
in float vertID;
uniform sampler2D texture_diffuse1;

void main()
{   
    FragColor = vec3(meshID / 20000.0f, vertID / 20000.0f, 0.0f);
}