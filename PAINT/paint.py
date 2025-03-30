#Imports
import pygame
import sys
import math

#Initialization
pygame.init()

WIDTH, HEIGHT = 800, 600
COLORS = [
    (255, 0, 0),  # RED
    (0, 255, 0),  # GREEN
    (0, 0, 255),  # BLUE
    (255, 255, 0),  # YELLOW
    (0, 255, 255),  # TURQUOISE
    (255, 0, 255),  # PURPLE
    (255, 255, 255),  # WHITE (ERASER)
    (0, 0, 0)  # BLACK
]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Paint")
surface = pygame.Surface((WIDTH, HEIGHT))
surface.fill((255, 255, 255))

current_color = COLORS[0]
drawing = False
last_pos = None
tool = 'line'
brush_size = 5

#Function for drawing interface
def draw_interface():
    pygame.draw.rect(screen, (150, 150, 150), (0, 0, WIDTH, 60))
    #Color selection
    for i, color in enumerate(COLORS):
        pygame.draw.circle(screen, color, (30 + i * 40, 30), 15)
    #Current color
    pygame.draw.circle(screen, current_color, (WIDTH - 30, 30), 15)
    #Places for naming tools
    pygame.draw.rect(screen, (200, 200, 200), (10, 70, 70, 30))  # Line
    pygame.draw.rect(screen, (200, 200, 200), (90, 70, 70, 30))  # Square
    pygame.draw.rect(screen, (200, 200, 200), (170, 70, 70, 30))  # Circle
    pygame.draw.rect(screen, (200, 200, 200), (250, 70, 70, 30))  # Right Triangle
    pygame.draw.rect(screen, (200, 200, 200), (330, 70, 70, 30))  # Equilateral Triangle
    pygame.draw.rect(screen, (200, 200, 200), (410, 70, 70, 30))  # Rhombus
    pygame.draw.rect(screen, (200, 200, 200), (490, 70, 30, 30))  # Plus
    pygame.draw.rect(screen, (200, 200, 200), (530, 70, 30, 30))  # Minus

    #Font and brush size text
    font = pygame.font.Font(None, 24)
    size_text = font.render(str(brush_size), True, (0, 0, 0))
    screen.blit(size_text, (565, 80))
    #Naming all tools
    font = pygame.font.Font(None, 36)
    line_text = font.render("line", True, (0, 0, 0))
    square_text = font.render("sqr", True, (0, 0, 0))
    circle_text = font.render("circ", True, (0, 0, 0))
    rtri_text = font.render("rtri", True, (0, 0, 0))
    etri_text = font.render("etri", True, (0, 0, 0))
    rhombus_text = font.render("rhom", True, (0, 0, 0))
    plus_text = font.render("+", True, (0, 0, 0))
    minus_text = font.render("-", True, (0, 0, 0))
    #Blittinng on the screen
    screen.blit(line_text, (13, 73))
    screen.blit(square_text, (95, 73))
    screen.blit(circle_text, (175, 73))
    screen.blit(rtri_text, (255, 73))
    screen.blit(etri_text, (335, 73))
    screen.blit(rhombus_text, (415, 73))
    screen.blit(plus_text, (495, 73))
    screen.blit(minus_text, (535, 75))


running = True
#Main cycle
while running:
    #Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for i, color in enumerate(COLORS):
                if ((pos[0] - (30 + i * 40)) ** 2 + (pos[1] - 30) ** 2) ** 0.5 < 15:
                    current_color = color
                    #Check eraser
                    if color == (255, 255, 255):
                        tool = 'eraser'
                    else:
                        tool = 'line' if tool == 'eraser' else tool
                    break
            #Set every invisible square to each tool
            if 10 <= pos[0] <= 80 and 70 <= pos[1] <= 100:
                tool = 'line'
            elif 90 <= pos[0] <= 160 and 70 <= pos[1] <= 100:
                tool = 'square'
            elif 170 <= pos[0] <= 240 and 70 <= pos[1] <= 100:
                tool = 'circle'
            elif 250 <= pos[0] <= 320 and 70 <= pos[1] <= 100:
                tool = 'right_triangle'
            elif 330 <= pos[0] <= 400 and 70 <= pos[1] <= 100:
                tool = 'equilateral_triangle'
            elif 410 <= pos[0] <= 480 and 70 <= pos[1] <= 100:
                tool = 'rhombus'
            elif 490 <= pos[0] <= 520 and 70 <= pos[1] <= 100:
                brush_size = min(20, brush_size + 1)
            elif 530 <= pos[0] <= 560 and 70 <= pos[1] <= 100:
                brush_size = max(1, brush_size - 1)
            #The place to draw
            if pos[1] > 110:
                drawing = True
                last_pos = pos
        #Drawing for final result
        elif event.type == pygame.MOUSEBUTTONUP:
            if drawing and tool not in ['line', 'eraser']:
                current_pos = pygame.mouse.get_pos()
                if tool == 'square':
                    pygame.draw.rect(surface, current_color,
                                     (min(last_pos[0], current_pos[0]),
                                      min(last_pos[1], current_pos[1]),
                                      abs(current_pos[0] - last_pos[0]),
                                      abs(current_pos[1] - last_pos[1])), brush_size)
                elif tool == 'circle':
                    radius = int(((current_pos[0] - last_pos[0]) ** 2 +
                                  (current_pos[1] - last_pos[1]) ** 2) ** 0.5)
                    pygame.draw.circle(surface, current_color, last_pos, radius, brush_size)
                elif tool == 'right_triangle':
                    points = [last_pos,
                              (current_pos[0], last_pos[1]),
                              current_pos]
                    pygame.draw.polygon(surface, current_color, points, brush_size)
                elif tool == 'equilateral_triangle':
                    side_length = ((current_pos[0] - last_pos[0]) ** 2 +
                                   (current_pos[1] - last_pos[1]) ** 2) ** 0.5
                    height = side_length * (math.sqrt(3) / 2)
                    #Determining direction based on mouse position
                    if current_pos[1] < last_pos[1]:  #Apex up
                        points = [last_pos,
                                  (last_pos[0] + side_length, last_pos[1]),
                                  (last_pos[0] + side_length / 2, last_pos[1] - height)]
                    else:  #Apex down
                        points = [last_pos,
                                  (last_pos[0] + side_length, last_pos[1]),
                                  (last_pos[0] + side_length / 2, last_pos[1] + height)]
                    pygame.draw.polygon(surface, current_color, points, brush_size)
                elif tool == 'rhombus':
                    dx = (current_pos[0] - last_pos[0]) / 2
                    dy = (current_pos[1] - last_pos[1]) / 2
                    points = [(last_pos[0] + dx, last_pos[1]),
                              (current_pos[0], last_pos[1] + dy),
                              (last_pos[0] + dx, current_pos[1]),
                              (last_pos[0], last_pos[1] + dy)]
                    pygame.draw.polygon(surface, current_color, points, brush_size)
            drawing = False
        #If line or eraser
        elif event.type == pygame.MOUSEMOTION and drawing:
            current_pos = pygame.mouse.get_pos()
            if tool in ['line', 'eraser']:
                pygame.draw.line(surface, current_color, last_pos, current_pos,
                                 brush_size * 2 if tool == 'eraser' else brush_size)
                last_pos = current_pos

    screen.blit(surface, (0, 0))
    draw_interface()
    #Drawing in real time
    if drawing and tool not in ['line', 'eraser']:
        current_pos = pygame.mouse.get_pos()
        temp_surface = surface.copy()
        if tool == 'square':
            pygame.draw.rect(temp_surface, current_color,
                             (min(last_pos[0], current_pos[0]),
                              min(last_pos[1], current_pos[1]),
                              abs(current_pos[0] - last_pos[0]),
                              abs(current_pos[1] - last_pos[1])), brush_size)
        elif tool == 'circle':
            radius = int(((current_pos[0] - last_pos[0]) ** 2 +
                          (current_pos[1] - last_pos[1]) ** 2) ** 0.5)
            pygame.draw.circle(temp_surface, current_color, last_pos, radius, brush_size)
        elif tool == 'right_triangle':
            points = [last_pos,
                      (current_pos[0], last_pos[1]),
                      current_pos]
            pygame.draw.polygon(temp_surface, current_color, points, brush_size)
        elif tool == 'equilateral_triangle':
            side_length = ((current_pos[0] - last_pos[0]) ** 2 +
                           (current_pos[1] - last_pos[1]) ** 2) ** 0.5
            height = side_length * (math.sqrt(3) / 2)
            #Determining direction based on mouse position
            if current_pos[1] < last_pos[1]:  #Apex up
                points = [last_pos,
                          (last_pos[0] + side_length, last_pos[1]),
                          (last_pos[0] + side_length / 2, last_pos[1] - height)]
            else:  #Apex down
                points = [last_pos,
                          (last_pos[0] + side_length, last_pos[1]),
                          (last_pos[0] + side_length / 2, last_pos[1] + height)]
            pygame.draw.polygon(temp_surface, current_color, points, brush_size)
        elif tool == 'rhombus':
            dx = (current_pos[0] - last_pos[0]) / 2
            dy = (current_pos[1] - last_pos[1]) / 2
            points = [(last_pos[0] + dx, last_pos[1]),
                      (current_pos[0], last_pos[1] + dy),
                      (last_pos[0] + dx, current_pos[1]),
                      (last_pos[0], last_pos[1] + dy)]
            pygame.draw.polygon(temp_surface, current_color, points, brush_size)
        screen.blit(temp_surface, (0, 0))

    pygame.display.flip()
#Exit
pygame.quit()
sys.exit()