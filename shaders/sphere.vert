#version 330 core
layout (location = 0) in vec3 aPos;

out vec3 color; // output a color to the fragment shader

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform vec3 aColor;

void main()
{
    gl_Position = projection * view * model * vec4(aPos, 1.0);
    color = aColor; // set ourColor to the input color we got from the vertex data
}
