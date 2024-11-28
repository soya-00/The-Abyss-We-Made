import pygame
from pygame import mixer
import random
import sys
import os

pygame.init()
mixer.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 1200
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Abyss We Made")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
DARK_BLUE = (0, 50, 120)
TEXT_COLOR = (255, 255, 0)
BUTTON_COLOR = (0, 150, 200)
HOVER_COLOR = (0, 200, 250)

# Variables
GRAVITY = 0.4
FISH_JUMP = -8
FISH_X = 50
OBSTACLE_WIDTH = 50
TRASH_HEIGHT = 60
FPS = 60
LEVELS = 5

# Load SFX

space_sfx = mixer.Sound(os.path.join("space_ui.mp3"))
click_sfx = mixer.Sound(os.path.join("button_ui.mp3"))


# Load Images and BGs

calmsea_bg = pygame.image.load(os.path.join("calm_sea.gif"))
calmsea_bg = pygame.transform.scale(calmsea_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
rainsea_bg = pygame.image.load(os.path.join("raining_sea.gif"))
rainsea_bg = pygame.transform.scale(rainsea_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
pol_bg = pygame.image.load(os.path.join("polluted_sea.gif"))
pol_bg = pygame.transform.scale(pol_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
start_bg = pygame.image.load(os.path.join("theabysswemade.png"))
start_bg = pygame.transform.scale(start_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))


background_sprites = [calmsea_bg, rainsea_bg, pol_bg]


try:
    fish_image = pygame.image.load(os.path.join('fish.png'))
    seaweed_image = pygame.image.load(os.path.join('seaweed.png'))
    crab_image = pygame.image.load(os.path.join('crab.png'))
    pearl_image = pygame.image.load(os.path.join('pearl.png'))
    trash_image = pygame.image.load(os.path.join('trash.png'))
    deadsw_image = pygame.image.load(os.path.join('deadseaweed.png'))
    deadcr_image = pygame.image.load(os.path.join('deadcrab.png'))
    deadprl_image = pygame.image.load(os.path.join('deadpearl.png'))
    print("Images loaded successfully")
    
except pygame.error as e:
    print(f"Error loading images: {e}")
    pygame.quit()
    exit()

fish_image = pygame.transform.scale(fish_image, (100,100))
seaweed_image = pygame.transform.scale(seaweed_image, (100,100))
crab_image = pygame.transform.scale(crab_image, (100,100))
pearl_image = pygame.transform.scale(pearl_image, (100,100))
trash_image = pygame.transform.scale(trash_image, (100,100))
deadcr_image = pygame.transform.scale(deadcr_image, (100,100))
deadsw_image = pygame.transform.scale(deadsw_image, (100,100))
deadprl_image = pygame.transform.scale(deadprl_image, (100,100))


obstacle_images = [seaweed_image, crab_image, pearl_image, trash_image]
obstacle_width = 1000
obstacle_gap = 50
obstacle_speed = 5

global bg_index

# Variables
fish_y = SCREEN_HEIGHT // 2
fish_velocity = 0
obstacles = []
score = 0
level = 1
level = int(level)
game_over = False
text = ''
visual_novel_index = 0
visual_novel_active = False
start_screen_active = True
intro_story_active = False
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
obs_ind = 0
bg_index = 0
end = False

# Messages

intro_text = [
    'I miss my home',
    'The ocean was once clean and vibrant.',
    'But one day, everything changed.',
    'The ocean darkened, and a massive, swirling cloud',
    'of pollution appeared above.',
    'Suddenly, darkness fell, and a storm of trash',
    'started raining down, disturbing the harmony of my world.',
    'The once vibrant ocean was now in chaos,',
    'and I knew I had to do something about it.',
    'I’m setting out to uncover the source of',
    'this pollution and restore balance to my home.'

]

collision_message = [
    [ 
    'You approached SEAWEED.',
    'SEAWEED: Hello, friend. How are you?',
    'SEAWEED: Things have changed so much recently.',
    'SEAWEED: I used to sway with the tides.',
    'SEAWEED: I provided shelter and food for many.',
    'SEAWEED: The ocean needs me to stay alive.',
    'SEAWEED: But the water feels heavier every day...',
    'SEAWEED: How long can I keep this up?'
    ],
    [
    'Ouch! You hit MR. CRAB.',
    'MR. CRAB: Ah, hello there, my friend!',
    'MR. CRAB: Oh? That’s quiet a journey you’re on.',
    'MR. CRAB: You know, crabs like me play a key role',
    'MR. CRAB: in the coastal ecosystem.',
    'MR. CRAB: We’re scavengers, cleaning the ocean floor',
    'MR. CRAB: and keeping things in balance.',
    'MR. CRAB: But things aren’t right. The trash...',
    'MR. CRAB: it’s everywhere. I fear for what’s to come.'


    ],
    [
    'You have met a MUSSEL.',
    'MUSSEL: Hello, my friend!',
    'MUSSEL: I may look rough on the outside, but inside,',
    'MUSSEL: I’m full of treasures—like pearls!',
    'MUSSEL: Did you know I’m an "ecosystem engineer"?',
    'MUSSEL: I help shape aquatic habitats and keep the',
    'MUSSEL: environment balanced.',
    'MUSSEL: Starfish and seabirds depend on me for food,',
    'MUSSEL: but humans are collecting too many of us',
    'MUSSEL: for pearls. Beauty is killing us all.',
    'MUSSEL: It’s harming underwater ecosystems...',

    ],
    [
    'Ouch! You hit an UNKNOWN BEING.', #3
    'FISH: Who is this stranger?',
    'FISH: He looks... unnatural, like something that',
    'FISH: doesn’t belong here.',
    'FISH: Perhaps he traveled from the South.'
    'FISH: Well, it doesn’t seem right. I should avoid him.'

    ],
    [

    'You approached SEAWEED.'
    'SEAWEED: This is my farewell, friend.',
    'SEAWEED: The tides no longer carry me.',
    'SEAWEED: I wither in poisoned waters, unseen, unheard.',
    'SEAWEED: No creatures hide in me anymore.',
    'SEAWEED: Even the ocean has turned its back.'

    ],
    [

    'You have met MR. CRAB.',
    'MR. CRAB: I should have done more...',
    'MR. CRAB: Now the ocean is silent. I failed it.',
    'MR. CRAB: The trash has consumed us all.',
    'MR. CRAB: I can’t feel the currents anymore,',
    'MR. CRAB: and there’s no one left to clean it.',
    'MR. CRAB: I never thought it would end like this...',
    'MR. CRAB: The ocean’s life is gone.'

    ],
    [
    'You have met a MUSSEL.',
    'MUSSEL: This used to be our home.',
    'MUSSEL: But the future is gone, and so am I.',
    'MUSSEL: There are no treasures to seek here.',
    'MUSSEL: Only the remnants of a world that once was.',
    'MUSSEL: I’ve faded away, just like the ocean’s',
    'MUSSEL: once-vibrant life. Who will save the rest?',

    ],
    [
        'Ouch! You hit a PLASTIC BOTTLE.', #7
    'FISH: It’s a water bottle...',
    'FISH: There are more of those now.',
    'FISH: I have seen more of them than my kin.',
    'FISH: ...Is this the end?'

    ]
]

transition_message = [
    [
    'The ocean feels heavier now.',
    'The pollution is spreading,',
    'and there’s more trash drifting around.',
    'The currents are getting stronger too—',
    'this won’t be easy, but I can’t turn back now!'
],
[
    'It’s getting darker…',
    'I can barely see through the growing cloud of pollution.',
    'I have to keep going. Something is wrong,',
    'and I’m getting closer to finding out what it is.'
],

[
    'The ocean is in chaos.',
    'I see fewer creatures, and they’re struggling to survive.',
    'The trash is everywhere, and the ocean is losing its life.',
    'I have to press on—there must be something I can do.'
],

[
    'This is… horrifying.',
    'The ocean is completely overwhelmed. All the creatures...',
    '... are gone, and it’s just trash, everywhere.',
    'I’ve reached the source of the destruction.',
    'Can I fix this before it’s too late?',
    'The ocean needs me now more than ever.'
]
]

end_game_message = [
    'I’ve uncovered the truth. It was never just a storm.',
    'The pollution... it’s not natural. It’s caused by humans.',
    'They’ve been poisoning the ocean for years.',
    'I tried to fight it, to restore what was lost,',
    'but the damage is too great. It’s too much for me',
    'to fix alone.',
    'The ocean, my home, is dying. The creatures,',
    'the life—it’s all slipping away.',
    'I can feel the poison inside me, choking my last breath.',
    'There’s no escaping it now.',
    'As I fade into darkness, I can’t help but wonder...',
    'will they ever understand what they’ve done?'

]

fall_out_message = [
    'Whoa, slow down there!',
    'You’re going too far!',
    'Remember where you are heading to.'

]

# Functions

def reset_game():
    fish_y = SCREEN_HEIGHT // 2
    fish_velocity = 0
    obstacles = []
    score = 0
    game_over = False
    level = 1
    visual_novel_active = False
    generate_obstacles()

global is_dead
def is_dead():
    dead_chance = min(level * 0.2, 1.0)  # Ensure the chance doesn't exceed 100%
    return random.random() < dead_chance

def generate_obstacles():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    obstacles.clear()
    for i in range(15):
        obs = ['seaweed','pearl','trash','crab']
        obs_choice = random.choice(obs)
        if obs_choice == 'seaweed':
            x = SCREEN_WIDTH + random.randint(300, 1200)
            y = random.randint(500,1100)
            obs_state = 4 if is_dead() else 0
            image = seaweed_image if obs_state == 0 else deadsw_image
            obstacles.append({"x": x, "y": y, "image": image, 'index': obs_state})
        elif obs_choice == 'pearl':
            x = SCREEN_WIDTH + random.randint(300, 1200)
            y = random.randint(500,1000)
            image = pearl_image
            obs_state = 6 if is_dead() else 2
            image = pearl_image if obs_state == 2 else deadprl_image
            obstacles.append({"x": x, "y": y, "image": image, 'index': obs_state})
        elif obs_choice == 'crab':
            x = SCREEN_WIDTH + random.randint(300, 1200)
            y = random.randint(500,1000)
            image = crab_image
            obs_state = 5 if is_dead() else 1
            image = crab_image if obs_state == 1 else deadcr_image
            obstacles.append({"x": x, "y": y, "image": image, 'index': obs_state})
        elif obs_choice == 'trash':
            x = SCREEN_WIDTH + random.randint(300, 1200)
            y = random.randint(200,750)
            image = trash_image
            obs_state = 7 if level>3 else 3
            obstacles.append({"x": x, "y": y, "image": image, 'index': obs_state})

def draw_text(text, x, y, color=TEXT_COLOR):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def next_level():
    global level, score
    fish_y = SCREEN_HEIGHT // 2
    fish_velocity = 0
    level += 1
    score = 0
    generate_obstacles()

def display_visual_novel(text):
    current_text = text[visual_novel_index]
    draw_text(current_text, SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2 - 20)
    draw_text("Press SPACE to continue", SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2 + 50)

def display_intro_story():
    bg_index = 0
    if intro_story_index >= 2:
        bg_index = 1
    screen.blit(background_sprites[bg_index], (0, 0))
    current_text = intro_text[intro_story_index]
    draw_text(current_text, SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2 - 20)
    draw_text("Press SPACE to continue", SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2 + 50)

def display_start_screen():
    screen.blit(start_bg, (0,0))
    play_button = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2, 150, 50)
    credits_button = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 70, 150, 50)

    pygame.draw.rect(screen, BUTTON_COLOR if not play_button.collidepoint(pygame.mouse.get_pos()) else HOVER_COLOR, play_button)
    pygame.draw.rect(screen, BUTTON_COLOR if not credits_button.collidepoint(pygame.mouse.get_pos()) else HOVER_COLOR, credits_button)
    
    draw_text("Play", play_button.x + 40, play_button.y + 50)
    draw_text("Credits", credits_button.x + 30, credits_button.y + 50)
    return play_button, credits_button

def end_game():
    fish_velocity = 0
    obstacles = []
    score = 0
    game_over = True
    level = 1
    text = end_game_message
    visual_novel_active = True
    intro_story_index = 0
    visual_novel_index = 0

# Main game loop
reset_game()
intro_story_index = 0
visual_novel_index = 0

# Cheat Code for easier Debug

# a = int(input('code: '))
# if a == 1:
#     level = 6
#     score = 15
# else:
#     pass


running = True
while running:
    screen.fill(BLUE)
    draw_text(f"Level: {level}", SCREEN_WIDTH // 6, SCREEN_HEIGHT // 16)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                mixer.Sound.play(click_sfx)
                if visual_novel_active:
                    visual_novel_index += 1
                    if visual_novel_index >= len(text):
                        visual_novel_active = False
                elif intro_story_active:
                    intro_story_index += 1
                    if intro_story_index >= len(intro_text):
                        intro_story_active = False
                #elif not visual_novel_active or not intro_story_active:
                    #screen.fill(BLUE)
                elif not game_over:
                    fish_velocity = FISH_JUMP
            elif game_over:
                display_start_screen()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mixer.Sound.play(space_sfx)
            if start_screen_active:
                play_button, credits_button = display_start_screen()
                if play_button.collidepoint(event.pos):
                    start_screen_active = False
                    intro_story_active = True
                elif credits_button.collidepoint(event.pos):
                    print('Created by Linh Anh and Dan Thu')

    # Display start screen
    if start_screen_active:
        play_button, credits_button = display_start_screen()
        pygame.display.flip()
        clock.tick(FPS)
        continue

    # Display intro story
    if intro_story_active:
        display_intro_story()
        pygame.display.flip()
        clock.tick(FPS)
        continue

    # Visual novel mode
    if visual_novel_active:
        display_visual_novel(text)
        pygame.display.flip()
        clock.tick(FPS)
        continue

    # Fish movement
    fish_velocity += GRAVITY
    fish_y += fish_velocity


    # Check if fish goes off screen
    if fish_y > SCREEN_HEIGHT or fish_y < 0:
        fish_y = SCREEN_HEIGHT // 2
        fish_velocity = 0
        text = fall_out_message
        visual_novel_active = True
        visual_novel_index = 0
        score = 0
        generate_obstacles()

    for obstacle in obstacles:
        obstacle["x"] -= obstacle_speed
        if obstacle["x"] < -obstacle_width:
            score += 1

        # Check for collision
        obstacle_rect = pygame.Rect(obstacle["x"], obstacle["y"], obstacle["image"].get_width(), obstacle["image"].get_height())
        fish_rect = pygame.Rect(FISH_X, fish_y, fish_image.get_width(), fish_image.get_height())
        if fish_rect.colliderect(obstacle_rect):
            fish_y = SCREEN_HEIGHT // 2
            fish_velocity = 0
            text = collision_message[obstacle['index']]
            visual_novel_active = True
            visual_novel_index = 0
            score = 0
            generate_obstacles()

        # Draw obstacle
        screen.blit(obstacle["image"], (obstacle["x"], obstacle["y"]))

    # Draw fish
    screen.blit(fish_image, (FISH_X,fish_y))

    # Display score and level

    # Check for level completion
    if score >= 15:
        if level >= 5:
            break
        elif level <=4:
            text = transition_message[level-1]
        visual_novel_active = True
        visual_novel_index = 0
        next_level()
              
    try:
        pygame.display.flip()
        clock.tick(FPS)
    except:
        print('Oops!') #Debug
        break

# GAME ENDING 
outro = True
visual_novel_index = 0
while outro == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                mixer.Sound.play(click_sfx)
                visual_novel_index += 1
    screen.blit(pol_bg, (0,0))
    text = end_game_message
    if visual_novel_index > 11:
        outro = False
        break
    draw_text(text[visual_novel_index], SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2 - 20)
    draw_text("Press SPACE to continue", SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2 + 50)
    pygame.display.flip()
    clock.tick(FPS)
        
# Quit game
print('''

  _______ _                 _           __                   _             _             _ 
 |__   __| |               | |         / _|                 | |           (_)           | |
    | |  | |__   __ _ _ __ | | _____  | |_ ___  _ __   _ __ | | __ _ _   _ _ _ __   __ _| |
    | |  | '_ \ / _` | '_ \| |/ / __| |  _/ _ \| '__| | '_ \| |/ _` | | | | | '_ \ / _` | |
    | |  | | | | (_| | | | |   <\__ \ | || (_) | |    | |_) | | (_| | |_| | | | | | (_| |_|
    |_|  |_| |_|\__,_|_| |_|_|\_\___/ |_| \___/|_|    | .__/|_|\__,_|\__, |_|_| |_|\__, (_)
                                                      | |             __/ |         __/ |  
                                                      |_|            |___/         |___/   
''')

pygame.quit()
sys.exit()
