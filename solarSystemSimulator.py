import pygame
import math

pygame.init()
WIDTH, HEIGHT = 1360, 697
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FONT1 = pygame.font.SysFont('arial', 10)
FONT2 = pygame.font.SysFont('arial', 20)
pygame.display.set_caption("Solar System Simulator")

AU = 149597870700
G = 6.674e-11
SCALE = 200 / AU
TIMESTEP = 86400

class Planet:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

        self.mass = 1
        self.x_vel = 0
        self.y_vel = 0
        self.vel = 0
        self.sun = False
        self.blackhole = False
        self.probe = False
        self.distance_to_sun = 0
        self.orbit = []

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance
        
        force = G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y
    
    def update_position(self, planets):
        total_fx = total_fy = 0

        for planet in planets:
            if self == planet:
                continue
            
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
            
        self.x_vel += total_fx / self.mass * TIMESTEP
        self.y_vel += total_fy / self.mass * TIMESTEP

        self.x += self.x_vel * TIMESTEP
        self.y += self.y_vel * TIMESTEP

        self.orbit.append((self.x, self.y))

    def draw(self, win):
        x = self.x * SCALE + WIDTH / 2
        y = self.y * SCALE + HEIGHT / 2
        radius = math.ceil(self.radius * SCALE)
        self.vel = math.sqrt(self.x_vel ** 2 + self.y_vel ** 2)
        pygame.draw.circle(win, self.color, (x, y), radius)

        name_text = FONT1.render(self.name, 1, (255, 255, 255))
        velocity_text = FONT1.render(f"{self.vel / 1000:.2f}km/s", 1, (255, 255, 255))
        fps_text = FONT2.render(f"{int(clock.get_fps())} FPS", 1, (255, 255, 255))
        time_text = FONT2.render(f"{(TIMESTEP * 60) / 86400:.2f} days per second", 1, (255, 255, 255))

        if self.blackhole:
            bhmass_text = FONT2.render(f"Blackhole mass: {self.mass:.2e}", 1, (255, 255, 255))
            win.blit(bhmass_text, (0, 20))


        win.blit(name_text, (x - name_text.get_width() / 2, y))
        win.blit(velocity_text, (x - velocity_text.get_width() / 2, y + name_text.get_height()))
        win.blit(fps_text, (0, 0))
        win.blit(time_text, (WIDTH - time_text.get_width(), 0))


def main():
    run = True
    global SCALE, TIMESTEP

    sun = Planet(0, 0, 696340000, (255, 255, 0))
    sun.mass = 1.989e30
    sun.sun = True
    sun.name = "Sun"

    mercury = Planet(-AU * 0.3871, 0, 2439700, (255, 255, 255))
    mercury.y_vel = 47360
    mercury.mass = 3.3e23
    mercury.name = "Mercury"

    venus = Planet(-AU * 0.7233, 0, 6051800, (255, 255, 167))
    venus.y_vel = 35020
    venus.mass = 4.87e24
    venus.name = "Venus"

    earth = Planet(-AU, 0, 6371000, (0, 0, 255))
    earth.y_vel = 29780
    earth.mass = 6e24
    earth.name = "Earth"

    mars = Planet(-AU * 1.5237, 0, 3390000, (255, 0, 0))
    mars.y_vel = 24140
    mars.mass = 6.4e23
    mars.name = "Mars"

    jupiter = Planet(-AU * 5.2028, 0, 69911000, (150, 150, 150))
    jupiter.y_vel = 13100
    jupiter.mass = 1.9e27
    jupiter.name = "Jupiter"

    saturn = Planet(-AU * 9.5388, 0, 58232000, (255, 255, 255))
    saturn.y_vel = 9690
    saturn.mass = 5.7e26
    saturn.name = "Saturn"

    uranus = Planet(-AU * 19.18171, 0, 25362000, (79, 205, 255))
    uranus.y_vel = 6800
    uranus.mass = 8.7e25
    uranus.name = "Uranus"

    neptune = Planet(-AU * 30.06971, 0, 24764000, (0, 0, 130))
    neptune.y_vel = 5500
    neptune.mass = 1e26
    neptune.name = "Neptune"

    sgr_A = Planet(0, 2.425e20, 0, (255, 255, 255))
    sgr_A.name = "Sgr A*"
    sgr_A.blackhole = True
    sgr_A.mass = 2.4e42

    probe = Planet(-AU * 0.999, 0, 0, (255, 255, 255))
    probe.y_vel = 30000
    probe.name = "Probe"
    probe.probe = True

    planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune, probe]

    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # quitting the simulator
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # zooming in and out using the scroll wheel
                if event.button == 4:
                    SCALE *= 1.1
                elif event.button == 5:
                    SCALE /= 1.1
            elif event.type == pygame.KEYDOWN:
                # increase or decrease the speed of the simulation using "-" and "+"
                if event.key == pygame.K_MINUS:
                    TIMESTEP /= 1.5
                elif event.key == pygame.K_EQUALS:
                    TIMESTEP *= 1.5

                # control the probe (if exists)
                if probe in planets:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        planets[planets.index(probe)].x_vel -= 1000
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        planets[planets.index(probe)].x_vel += 1000
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        planets[planets.index(probe)].y_vel += 1000
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        planets[planets.index(probe)].y_vel -= 1000

        for planet in planets:
            planet.update_position(planets)

            if planet.blackhole:  # if it's a blackhole, increase the mass in time
                planet.mass += TIMESTEP * (planet.mass / 2e6)

            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()

main()
