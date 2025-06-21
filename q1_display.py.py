
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


# QUESTION 1: DEFINING MODELS
models = {
    "cube": {
        "vertices": (
            (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
            (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1)
        ),
        "edges": (
            (0,1), (0,3), (0,4), (2,1), (2,3), (2,7),
            (6,3), (6,4), (6,7), (5,1), (5,4), (5,7)
        ),
        "faces": (
            (0,1,2,3), (4,5,1,0), (7,6,4,5),
            (2,3,6,7), (1,2,7,5), (0,3,6,4)
        )
    },
    "pyramid": {
        "vertices": (
            (1, -1, 1), (-1, -1, 1), (0, -1, -1), (1, 1, 0.5)
        ),
        "edges": (
            (0,1), (0,2), (0,3), (2,1), (2,3), (3,1)
        ),
        "faces": (
            (0, 1, 2), (0, 1, 3), (1, 2, 3), (2, 0, 3)
        )
    },
    "prism": {
        "vertices": (
            (-1, -1, 1), (1, -1, 1), (0, 1, 1),
            (-1, -1, -1), (1, -1, -1), (0, 1, -1)
        ),
        "edges": (
            (0,1), (0,2), (1,2), (3,4), (3,5),
            (4,5), (0,3), (1,4), (2,5)
        ),
        "faces": (
            (0,1,2), (3,4,5), (0,1,4,3), (1,2,5,4), (2,0,3,5)
        )
    }
}


# QUESTION 5: COLOURS FOR EACH FACE
colors = [
    (1, 0, 0),    # Red
    (0, 1, 0),    # Green
    (0, 0, 1),    # Blue
    (1, 1, 0),    # Yellow
    (1, 0, 1),    # Magenta
    (0, 1, 1),    # Cyan
    (0.5, 0.5, 1),  # Light Blue
    (1, 0.5, 0),    # Orange
]


# QUESTION 5: DRAWING COLOURED FACES
def draw_model(vertices, edges, faces):
    # Draw colored faces (quads and triangles)
    for i, face in enumerate(faces):
        glColor3fv(colors[i % len(colors)])
        if len(face) == 4:
            glBegin(GL_QUADS)
        elif len(face) == 3:
            glBegin(GL_TRIANGLES)
        else:
            continue
        for vertex in face:
            glVertex3fv(vertices[vertex])
        glEnd()

    # Draw edges in white
    glColor3f(1, 1, 1)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()


# MAIN PROGRAM 
def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    # QUESTION 1: Initial perspective/camera setup
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    # QUESTION 2: Translation state
    model_position = [0.0, 0.0, -5.0]

    # QUESTION 3: Rotation state
    rotation = [0, 0, 0]

    # QUESTION 4: Scaling state
    scale = [1.0, 1.0, 1.0]

    model_keys = list(models.keys())
    current_model_index = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            elif event.type == KEYDOWN:
                # QUESTION 1: Switch model
                if event.key == K_SPACE:
                    current_model_index = (current_model_index + 1) % len(model_keys)

                # QUESTION 2: Translation keys
                elif event.key == K_w: model_position[1] += 0.2
                elif event.key == K_s: model_position[1] -= 0.2
                elif event.key == K_a: model_position[0] -= 0.2
                elif event.key == K_d: model_position[0] += 0.2
                elif event.key == K_q: model_position[2] += 0.2
                elif event.key == K_e: model_position[2] -= 0.2

                # QUESTION 3: Rotation keys
                elif event.key == K_i: rotation[0] += 5
                elif event.key == K_k: rotation[0] -= 5
                elif event.key == K_j: rotation[1] += 5
                elif event.key == K_l: rotation[1] -= 5
                elif event.key == K_u: rotation[2] += 5
                elif event.key == K_o: rotation[2] -= 5

                # QUESTION 4: Scaling keys
                elif event.key == K_z: scale[0] += 0.1
                elif event.key == K_x: scale[0] = max(0.1, scale[0] - 0.1)
                elif event.key == K_c: scale[1] += 0.1
                elif event.key == K_v: scale[1] = max(0.1, scale[1] - 0.1)
                elif event.key == K_b: scale[2] += 0.1
                elif event.key == K_n: scale[2] = max(0.1, scale[2] - 0.1)

        # QUESTION 1: Frame setup
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)

        glLoadIdentity()
        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

        # Apply transformations in order
        glTranslatef(*model_position)       # QUESTION 2
        glRotatef(rotation[0], 1, 0, 0)      # QUESTION 3
        glRotatef(rotation[1], 0, 1, 0)
        glRotatef(rotation[2], 0, 0, 1)
        glScalef(*scale)                    # QUESTION 4

        # Draw model with colored faces and white edges
        current_model = models[model_keys[current_model_index]]
        draw_model(current_model["vertices"], current_model["edges"], current_model["faces"])

        pygame.display.set_caption(f"Model: {model_keys[current_model_index].capitalize()}")
        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

if __name__ == "__main__":
    main()
