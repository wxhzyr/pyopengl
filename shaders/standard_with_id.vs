#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aNormal;
layout (location = 2) in vec2 aTexCoords;
// layout (location = 3) in float inMeshID;
// layout (location = 4) in float inVertID;
// layout (location = 5) in float inIsChoose;
out vec2 TexCoords;
// out float meshID;
// out float vertID;
out float isChoose;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform vec4 choosePoint;
uniform float chooseRadius;

void main()
{
    TexCoords = aTexCoords;    
    gl_Position = projection * view * model * vec4(aPos, 1.0);
    // meshID = inMeshID;
    // vertID = inVertID;
    // isChoose = inIsChoose;
    isChoose = 0.0f;
    if (choosePoint.w > 0.0f) {
        float len = (aPos.x - choosePoint.x) * (aPos.x - choosePoint.x) + (aPos.y - choosePoint.y) * (aPos.y - choosePoint.y) + (aPos.z - choosePoint.z) * (aPos.z - choosePoint.z);
        if (len < chooseRadius)
            isChoose = 0.51f;
    }
}