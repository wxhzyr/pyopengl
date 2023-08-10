#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aNormal;
layout (location = 2) in vec2 aTexCoords;
layout (location = 3) in float inMeshID;
layout (location = 4) in float inVertID;
out vec2 TexCoords;
out float meshID;
out float vertID;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
    TexCoords = aTexCoords;    
    gl_Position = projection * view * model * vec4(aPos, 1.0);
    meshID = inMeshID;
    vertID = inVertID;
}