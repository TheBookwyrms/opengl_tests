#version 330 core

in vec3 point_colour;
in float point_opacity;
in vec3 point_normals;
in vec3 fragment_position;


uniform mat4 world_transform;

out vec4 fragment_colour;

uniform float ambient_strength;
uniform vec3 ambient_colour;

uniform vec3 light_source_pos;
uniform vec3 light_source_colour;

uniform float specular_strength;
uniform vec3 camera_viewpos;
uniform float specular_power;

void main() {

    vec3 ambient_light = ambient_strength * ambient_colour;


    vec3 norm = normalize(point_normals);
    vec3 light_dir = normalize(light_source_pos - fragment_position);
    
    float diffuse_strength = max(dot(norm, light_dir), 0.0);
    vec3 diffuse_light = diffuse_strength * light_source_colour;


    vec3 view_direction = normalize(camera_viewpos - fragment_position);
    vec3 light_reflect_dir = normalize(reflect(-light_dir, norm));

    // specular nonsense that doesn't work
    // float specular_magnitude = pow(max(dot(view_direction, light_reflect_dir), 0.0), specular_power);
    // vec3 specular_light = specular_strength * specular_magnitude * light_source_colour;

    vec3 result = point_colour * (ambient_light + diffuse_light); // + specular_light);

    fragment_colour = vec4(result, point_opacity);
}