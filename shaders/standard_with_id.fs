#version 330 core
out vec4 FragColor;

in vec2 TexCoords;
// in float meshID;
// in float vertID;
in float isChoose;
uniform sampler2D texture_diffuse1;
uniform vec4 chooseColor;

void main()
{   if (isChoose > 0.5f) {
        FragColor = mix(texture(texture_diffuse1, TexCoords), chooseColor, 0.5);
    } 
    else {
        FragColor = texture(texture_diffuse1, TexCoords) * 2.0f;
    }
}