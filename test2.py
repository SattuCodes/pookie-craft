#Importing all the modules
import pygame
import os
import random
import sys
import mysql.connector
pygame.init()
config = {
    'user' : 'root',
    'password' : '25110505',
    'host' : 'localhost',
}
def sqlcon():
    return mysql.connector.connect(**config)
def dbmain(username):
    con = sqlcon()
    cursor = con.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS backend")
    cursor.execute("USE backend")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) UNIQUE,
            credits INT,
            health INT,
            points INT,
            items TEXT
        )
    """)
    cursor.execute("SELECT name FROM data WHERE name=%s", (username,))
    result = cursor.fetchone()
    if result:
        con.close()
        return False
    else:
        cursor.execute("INSERT INTO data (name, credits, health, points, items) VALUES (%s, %s, %s, %s, %s)", (username, 1000, 100, 0, ''))
        con.commit()
        con.close()
        return True
def fetch(n):
    con = sqlcon()
    cursor = con.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS backend")
    cursor.execute("USE backend")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) UNIQUE,
            credits INT,
            health INT,
            points INT,
            items TEXT
        )
    """)
    cursor.execute("SELECT credits, health, points, items FROM data WHERE name=%s", (n,))
    result = cursor.fetchone()
    con.close()
    return result

def fetch_all():
    con = sqlcon()
    cursor = con.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS backend")
    cursor.execute("USE backend")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) UNIQUE,
            credits INT,
            health INT,
            points INT,
            items TEXT
        )
    """)
    cursor.execute("SELECT name, credits, points FROM data")
    results = cursor.fetchall()
    con.close()
    return results

def update(n, credits, health, points, items):
    con = sqlcon()
    cursor = con.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS backend")
    cursor.execute("USE backend")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) UNIQUE,
            credits INT,
            health INT,
            points INT,
            items TEXT
        )
    """)
    cursor.execute("UPDATE data SET credits=%s, health=%s, points=%s, items=%s WHERE name=%s",
                   (credits, health, points, items, n))
    con.commit()
    con.close()

def deleteu(n):
    con = sqlcon()
    cursor = con.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS backend")
    cursor.execute("USE backend")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) UNIQUE,
            credits INT,
            health INT,
            points INT,
            items TEXT
        )
    """)
    cursor.execute("DELETE FROM data WHERE name=%s", (n,))
    con.commit()
    con.close()

def check_profile(screen):
    username = inp(screen, "Enter your username: ", "Press Home to go back to menu")
    profile = fetch(username)
    if profile:
        screen.fill((0, 0, 0))
        credits, hp, points, items = profile
        text(screen, f"Username: {username}", position=(638, 200), align_center=True)
        text(screen, f"Credits: {credits}", position=(638, 250), align_center=True)
        text(screen, f"Health: {hp}", position=(638, 300), align_center=True)
        text(screen, f"Points: {points}", position=(638, 350), align_center=True)
        text(screen, f"Items: {items if items else 'None'}", position=(638, 400), align_center=True)
        pygame.display.update()
        pygame.time.wait(4000)
    else:
        text(screen, "Username not found!", position=(250, 200))
        pygame.display.update()
        pygame.time.wait(2000)

def check_all_profiles(screen):
    profiles = fetch_all()

    if profiles:
        screen.fill((0,0,0))
        y = 100
        for profile in profiles:
            username, credits, points = profile
            text(screen, f"Username: {username}, Credits: {credits}, Points: {points}", position=(508, y), align_center=True)
            y += 50
        pygame.display.update()
        pygame.time.wait(4000)
    else:
        screen.fill((0,0,0))
        text(screen, "No profiles found!", position=(0,250), align_center=True)
        pygame.display.update()
        pygame.time.wait(2000)

def modify_profile(screen):
    username = inp(screen, "Enter your username: ", "Press Home to go back to menu")
    profile = fetch(username)
    
    if profile:
        credits, hp, points, items = profile
        
        # Display modification options
        while True:
            modification_choice = inp(screen, "What do you want to modify?", "Options: Credits, Health, Points, Items").lower()

            if modification_choice == "credits":
                new_credits = inp(screen, f"Modify credits (current: {credits}): ")
                update(username, int(new_credits), hp, points, items)
                break
            elif modification_choice == "health":
                new_hp = inp(screen, f"Modify health (current: {hp}): ")
                update(username, credits, int(new_hp), points, items)
                break
            elif modification_choice == "points":
                new_points = inp(screen, f"Modify points (current: {points}): ")
                update(username, credits, hp, int(new_points), items)
                break
            elif modification_choice == "items":
                new_items = inp(screen, f"Modify items (current: {items}): ")
                update(username, credits, hp, points, new_items)
                break
            else:
                text(screen, "Invalid choice! Please select again.", position=(screen.get_width()//2, 250), align_center=True)
                pygame.display.update()
                pygame.time.wait(1000)  # Pause briefly before retrying

        # Display update confirmation
        text(screen, "Profile updated successfully!", position=(700, 600), align_center=True)
        pygame.display.update()
        pygame.time.wait(2000)
    
    else:
        text(screen, "Username not found!", position=(screen.get_width()//2, 250), align_center=True)
        pygame.display.update()
        pygame.time.wait(2000)


def delete_profile(screen):
    username = inp(screen,"Enter your username to delete: ","Press Home to go back to menu")
    profile = fetch(username)

    if profile:
        confirmation = inp(screen, f"Are you sure you want to delete the profile '{username}'? (yes/no): ")
        if confirmation.lower() in ['yes', 'y']:
            deleteu(username)
            text(screen, f"Profile '{username}' deleted!", position=(638,250))
            pygame.display.update()
            pygame.time.wait(2000)
        else:
            text(screen, "Profile deletion canceled!", position=(638,250))
            pygame.display.update()
            pygame.time.wait(2000)
    else:
        text(screen, "Username not found!", position=(0, 450), align_center=True)
        pygame.display.update()
        pygame.time.wait(2000)

def drop_all(screen):
    screen.fill((0, 0, 0))
    con = sqlcon()
    cursor = con.cursor()
    cursor.execute('USE backend')
    try:
        cursor.execute("SHOW TABLES LIKE 'data'")
        result = cursor.fetchone()
        if result:
            x = inp(screen, "Are you sure you want to delete all the profiles?(y/n)", "Press Home to go back to menu")
            if x == 'y':    
                cursor.execute("DROP TABLE data")
                con.commit()
                screen.fill((0,0,0))
                text(screen, "Deleted all the profiles", position=(638, 250), align_center=True, font_size=40)
            else:
                main()
        else:
            text(screen, "No record or table found", position=(638, 250), align_center=True, font_size=40)
    except mysql.Error as err:
        text(screen, "Error occurred: " + str(err), position=(638, 250), align_center=True, font_size=40)
    con.close()
    pygame.display.update()
    pygame.time.wait(2000)
#Handling frame-to-frame animation
def animation(screen, folder=None, x=0, y=0, scl=3):
    frames = []
    for frame in sorted(os.listdir(folder)):
        img = pygame.image.load(os.path.join(folder, frame))
        scale = pygame.transform.scale(img, (img.get_width() * scl, img.get_height() * scl))
        frames.append(scale)
    def draw(frame_index):
        frame_index %= len(frames)
        screen.blit(frames[frame_index], (x, y))
    return draw, len(frames)
#Handling background images
def bgloader(path):
    return pygame.image.load(path)
#Handling text rendering
def text(screen, text, position, font_size=30, color=(255, 255, 255), align_center=False):
    font = pygame.font.Font("Exo-VariableFont_wght.ttf", font_size)
    surface = font.render(text, True, color)
    surfrect = surface.get_rect()
    if align_center:
        surfrect.midtop = (screen.get_width()//2, position[1])
    else:
        surfrect.topleft = position
    screen.blit(surface, surfrect.topleft)
    return surface, surfrect

#Displaying health bar
def healthbar(screen, health, maxhp, position=(50,50), barw=200, barh=20, color=(255,0,0), gc=(0,255,0), rc=(255,0,0), bg=(100,100,100)):
    fill = int((health/maxhp)*barw)
    color = (
        int(gc[0] + (rc[0] - gc[0]) * (1 - health / maxhp)),
        int(gc[1] + (rc[1] - gc[1]) * (1 - health / maxhp)),
        int(gc[2] + (rc[2] - gc[2]) * (1 - health / maxhp))
    )
    pygame.draw.rect(screen, bg, (*position, barw, barh))
    pygame.draw.rect(screen, color, (*position, fill, barh))


#Displaying credits
def creds(screen, currcred):
    text(screen, f'Credits: {currcred}', position=(1200,50), font_size=20)

#Make options visible
def option(screen, items, font_size=40, gap=20):
    font = pygame.font.Font("Exo-VariableFont_wght.ttf", font_size)
    buttons = []
    screen_rect = screen.get_rect()
    total_height = len(items) * (font_size + gap)
    start_y = (screen_rect.height - total_height) // 2

    for index, item in enumerate(items):
        text = font.render(item, True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (screen_rect.centerx, start_y + index * (font_size + gap))
        screen.blit(text, text_rect)
        buttons.append((item, text_rect))

    return buttons

def inp(screen, text1, text2="", font_size=40):
    output = ""
    input_active = True
    font = pygame.font.Font("Exo-VariableFont_wght.ttf", font_size)
    clock = pygame.time.Clock()
    redraw = True

    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_HOME:
                    main()
                elif event.key == pygame.K_BACKSPACE:
                    output = output[:-1]
                    redraw = True
                else:
                    output += event.unicode
                    redraw = True

        if redraw:
            screen.fill((0, 0, 0)) 

            if text2 == '':
                prompt = font.render(text1, True, (255, 255, 255))
                username_text = font.render(output, True, (255, 255, 255))
                screen.blit(prompt, (screen.get_width()//2 - prompt.get_width()//2, 200))
                screen.blit(username_text, (screen.get_width()//2 - username_text.get_width()//2, 300))
            else:
                text(screen, f"{text2}", position=(683, 568), align_center=True)
                prompt = font.render(text1, True, (255, 255, 255))
                username_text = font.render(output, True, (255, 255, 255))
                screen.blit(prompt, (screen.get_width()//2 - prompt.get_width()//2, 200))
                screen.blit(username_text, (screen.get_width()//2 - username_text.get_width()//2, 300))

            pygame.display.flip()
            redraw = False
        clock.tick(10)

    return output

def huntress(screen, knight_health, username):
    profile = fetch(username)
    credits, hp, points, items = profile
    background = bgloader("img/Background/wizard.png")

    draw_idle_knight, total_idle_knight_frames = animation(screen, "img/Knight/Idle", 100, 500, scl=3)
    draw_attack_knight, total_attack_knight_frames = animation(screen, "img/Knight/Attack", 100, 500, scl=3)
    draw_hurt_knight, total_hurt_knight_frames = animation(screen, "img/Knight/Hurt", 100, 500, scl=3)
    
    draw_idle_huntress, total_idle_huntress_frames = animation(screen, "img/Huntress/Idle", 1000, 500, scl=3)
    draw_attack_huntress, total_attack_huntress_frames = animation(screen, "img/Huntress/Attack", 1000, 500, scl=3)
    draw_hurt_huntress, total_hurt_huntress_frames = animation(screen, "img/Huntress/Hurt", 1000, 500, scl=3)

    huntress_hp = 100
    choose = False
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    fight_started = False
    helping_huntress = False
    frame_index_knight = 0
    frame_index_huntress = 0
    player_credits = credits

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif not choose and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y and player_credits >= 400:  # 'Y' for yes (help)
                    helping_huntress = True
                    player_credits -= 400
                    update(username, player_credits, hp, points, items)
                elif event.key == pygame.K_n:  # 'N' for no (fight starts)
                    fight_started = True

        screen.blit(background, (0, 0))

        # Initial Encounter
        if pygame.time.get_ticks() - start_time <= 2000:
            text(screen, "You encountered a huntress!", position=(screen.get_width()//2, 200), align_center=True)
            draw_idle_huntress(frame_index_huntress)
            frame_index_huntress = (frame_index_huntress + 1) % total_idle_huntress_frames
        
        # Choice: Help or Fight
        elif not choose:
            text(screen, "Help the huntress for 400 credits? (Y/N)", position=(screen.get_width()//2, 200), align_center=True)
            draw_idle_huntress(frame_index_huntress)
            frame_index_huntress = (frame_index_huntress + 1) % total_idle_huntress_frames
            choose = True
        
        # If player chooses to help
        if helping_huntress:
            text(screen, "You helped the huntress! She joins your side.", position=(screen.get_width()//2, 200), align_center=True)
            draw_idle_huntress(frame_index_huntress)
            frame_index_huntress = (frame_index_huntress + 1) % total_idle_huntress_frames
            pygame.time.wait(2000)
            break  # Return to the game logic after helping

        # Fight scene if player chooses not to help
        if fight_started:
            # Fight Logic - Player can click to attack, Huntress attacks randomly
            if event.type == pygame.MOUSEBUTTONDOWN:  # Player clicks to attack
                draw_attack_knight(frame_index_knight)
                frame_index_knight = (frame_index_knight + 1) % total_attack_knight_frames
                # Huntress takes damage logic here (e.g., reduce huntress HP)

            # Huntress random attack
            if random.choice([True, False]):  # Randomly choose attack
                draw_attack_huntress(frame_index_huntress)
                frame_index_huntress = (frame_index_huntress + 1) % total_attack_huntress_frames
                knight_health -= 10  # Decrease knight health

            # Display health bars
            healthbar(screen, knight_health, maxhp=100, position=(50, 50))
            healthbar(screen, huntress_hp, maxhp=100, position=(1000, 50))  # Assuming huntress_hp is defined

        pygame.display.flip()
        clock.tick(10)


def wizard(screen, knight_health, username):
    profile = fetch(username)
    credits, hp, points, items = profile
    background = bgloader("img/Background/wizard.png")

    # Set up animations
    draw_idle_knight, total_idle_knight_frames = animation(screen, "img/Knight/Idle", 100, 500, scl=3)
    draw_death_knight, total_death_knight_frames = animation(screen, "img/Knight/Death", 100, 500, scl=3)
    
    draw_idle_wizard, total_idle_wizard_frames = animation(screen, "img/Wizard/Idle", 1000, 500, scl=2)
    draw_attack_wizard, total_attack_wizard_frames = animation(screen, "img/Wizard/Attack", 1000, 500, scl=2)

    current_knight_animation = draw_idle_knight
    total_knight_frames = total_idle_knight_frames
    current_wizard_animation = draw_idle_wizard
    total_wizard_frames = total_idle_wizard_frames

    attempt = None
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    question_start_time = None
    question_asked = False
    correct_answer = None
    player_answer = ""
    answer_phase = False
    is_game_over = False
    death_animation_played = False
    wizard_attack_played = False
    frame_index_knight = 0
    frame_index_wizard = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN and question_asked and answer_phase:
                if event.key == pygame.K_RETURN:
                    if player_answer.isdigit() and int(player_answer) == correct_answer:
                        knight_health = 100 
                        points += 10
                        update(username, credits, knight_health, points, items)
                    else:
                        knight_health -= 50 
                        update(username, credits, knight_health, points, items)
                        if knight_health <= 0:
                            is_game_over = True
                            frame_index_knight = 0
                            frame_index_wizard = 0
                        question_asked = False
                        answer_phase = False
                        attempt = 1
                        player_answer = ""
                elif pygame.K_0 <= event.key <= pygame.K_9 and answer_phase:
                    player_answer += event.unicode

        screen.blit(background, (0, 0))
        if not is_game_over:
            if pygame.time.get_ticks() - start_time <= 2000:
                text(screen, "You encountered a wizard!", position=(screen.get_width()//2, 200), align_center=True)
            elif not question_asked and attempt is None:
                num1, num2 = random.randint(1, 10), random.randint(1, 10)
                correct_answer = num1 + num2
                question_start_time = pygame.time.get_ticks() 
                question_asked = True
            elif question_asked and question_start_time and (pygame.time.get_ticks() - question_start_time <= 3000):
                text(screen, f"What is {num1} + {num2}?", position=(screen.get_width()//2, 200), align_center=True)
            else:
                answer_phase = True
                text(screen, f"Your answer: {player_answer}", position=(screen.get_width()//2, 300), align_center=True)

            healthbar(screen, knight_health, maxhp=100, position=(50, 50))

            current_knight_animation(frame_index_knight)
            frame_index_knight = (frame_index_knight + 1) % total_knight_frames
            current_wizard_animation(frame_index_wizard)
            frame_index_wizard = (frame_index_wizard + 1) % total_wizard_frames

        else:
            if frame_index_knight < total_death_knight_frames and frame_index_wizard < total_attack_wizard_frames:
                current_knight_animation = draw_death_knight
                current_wizard_animation = draw_attack_wizard
                current_knight_animation(frame_index_knight)
                current_wizard_animation(frame_index_wizard)
                frame_index_knight += 1
                frame_index_wizard += 1
            else:
                death_animation_played = True
                wizard_attack_played = True
                huntress(screen, knight_health, username)

            if death_animation_played and wizard_attack_played:
                text(screen, "Game Over", position=(screen.get_width() // 2, 200), align_center=True)
                pygame.display.flip()
                pygame.time.wait(2000)
                main()

        pygame.display.flip()
        clock.tick(10)


#When torch is in inventory
def caveLight(screen, username, item_check=False):
    profile = fetch(username)
    credits, hp, points, items = profile
    running = True
    background = bgloader("img/Background/cavelight.png")
    background = pygame.transform.scale(background, screen.get_size())
    
    #Complicated part
    draw_idle_knight, total_idle_knight_frames = animation(screen, "img/Knight/Idle", 100, 500, scl=3)
    draw_attack_knight, total_attack_knight_frames = animation(screen, "img/Knight/Attack", 100, 500, scl=3)
    draw_hurt_knight, total_hurt_knight_frames = animation(screen, "img/Knight/Hurt", 100, 500, scl=3)
    
    draw_idle_monster, total_idle_monster_frames = animation(screen, "img/Monsters/Idle", 1000, 500, scl=3)
    draw_hurt_monster, total_hurt_monster_frames = animation(screen, "img/Monsters/Hurt", 1000, 500, scl=3)
    draw_attack_monster, total_attack_monster_frames = animation(screen, "img/Monsters/Attack", 1000, 500, scl=3)
    draw_death_monster, total_death_monster_frames = animation(screen, "img/Monsters/Death", 1000, 600, scl=3)
    
    #Idleing state
    current_knight_animation = draw_idle_knight
    total_knight_frames = total_idle_knight_frames
    current_monster_animation = draw_idle_monster
    total_monster_frames = total_idle_monster_frames
    attack_in_progress = False
    
    #Health and attack logic
    monster_hp = 200
    max_monster_hp = 200
    maxattack = 8
    attack = 0
    clock = pygame.time.Clock()
    frame_index_knight = 0
    frame_index_monster = 0
    start_time = pygame.time.get_ticks()
    buttons = None
    monster_dead = False
    knight_health = 100
    monster_attack_punches = random.sample(range(1, maxattack + 1), 5)

    #Actual game logic 🗣️
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main() 
            elif event.type == pygame.MOUSEBUTTONDOWN and buttons:
                mouse_pos = pygame.mouse.get_pos()
                for item, rect in buttons:
                    if rect.collidepoint(mouse_pos) and not monster_dead:
                        if item == "Attack" and not attack_in_progress:
                            current_knight_animation = draw_attack_knight
                            total_knight_frames = total_attack_knight_frames
                            frame_index_knight = 0  
                            attack_in_progress = True 
                            attack += 1
                            monster_hp -= 25  
                            if attack in monster_attack_punches:
                                current_knight_animation = draw_hurt_knight
                                total_attack_knight_frames = total_hurt_knight_frames
                                current_monster_animation = draw_attack_monster
                                total_monster_frames = total_attack_monster_frames
                                frame_index_monster = 0
                                knight_health -= 10
                                update(username, credits, hp, points, items)
                            if monster_hp > 0 and attack not in monster_attack_punches:
                                current_monster_animation = draw_hurt_monster
                                total_monster_frames = total_hurt_monster_frames
                                frame_index_monster = 0  
                            elif monster_hp <= 0:
                                defeat_time = pygame.time.get_ticks()
                                current_monster_animation = draw_death_monster
                                total_monster_frames = total_death_monster_frames
                                frame_index_monster = 0
                                points += 10
                                monster_dead = True
        screen.blit(background, (0, 0))
        if " |Torch| " in items and pygame.time.get_ticks() - start_time <= 2000 and item_check==True: 
            text(screen, "You already have a torch in your inventory!", position=(500, 200), align_center=True)
        elif pygame.time.get_ticks() - start_time <= 2000:
            text(screen, "You bought a torch and made everything visible.", position=(500, 200), align_center=True)
        if pygame.time.get_ticks() - start_time > 2000:
            text(screen, "You encountered a monster!", position=(500, 200), align_center=True)
            if pygame.time.get_ticks() - start_time > 4000:
                options = ["Attack"]
                buttons = option(screen, options, gap=10, font_size=30)
        creds(screen,credits)
        healthbar(screen, knight_health, 100, position=(50, 50))
        current_knight_animation(frame_index_knight)
        frame_index_knight = (frame_index_knight + 1) % total_knight_frames
        if attack_in_progress and frame_index_knight == 0:
            current_knight_animation = draw_idle_knight
            total_knight_frames = total_idle_knight_frames
            frame_index_knight = 0
            attack_in_progress = False
            if not monster_dead:
                current_monster_animation = draw_idle_monster
                total_monster_frames = total_idle_monster_frames
        current_monster_animation(frame_index_monster)
        if not monster_dead:
            frame_index_monster = (frame_index_monster + 1) % total_monster_frames
        else:
            frame_index_monster = min(frame_index_monster + 1, total_monster_frames - 1)
        if monster_hp > 0:
            healthbar(screen, monster_hp, max_monster_hp, position=(1020, 480), barw=80, barh=10)
        
        pygame.display.flip()
        if monster_dead and defeat_time and pygame.time.get_ticks() - defeat_time > 2000:
            text(screen, "Defeated the monster! You continued your journey", position=(500,500), align_center=True)
            pygame.display.flip()
            update(username, credits, hp, points, items)
            if monster_dead and defeat_time and pygame.time.get_ticks() - defeat_time > 5000:
                wizard(screen, knight_health, username)
        clock.tick(10)

#When torch not in inv
def caveDark(screen, username):
    profile = fetch(username)
    credits, hp, points, items = profile
    running = True
    background = bgloader("img/Background/cave.png")
    background = pygame.transform.scale(background, screen.get_size())
    
    #Complicated part
    draw_idle_knight, total_idle_knight_frames = animation(screen, "img/Knight/Idle", 100, 500, scl=3)
    draw_attack_knight, total_attack_knight_frames = animation(screen, "img/Knight/Attack", 100, 500, scl=3)
    draw_hurt_knight, total_hurt_knight_frames = animation(screen, "img/Knight/Hurt", 100, 500, scl=3)
    
    draw_idle_monster, total_idle_monster_frames = animation(screen, "img/Monsters/Idle", 1000, 500, scl=3)
    draw_hurt_monster, total_hurt_monster_frames = animation(screen, "img/Monsters/Hurt", 1000, 500, scl=3)
    draw_attack_monster, total_attack_monster_frames = animation(screen, "img/Monsters/Attack", 1000, 500, scl=3)
    draw_death_monster, total_death_monster_frames = animation(screen, "img/Monsters/Death", 1000, 600, scl=3)
    
    #Idleing state
    current_knight_animation = draw_idle_knight
    total_knight_frames = total_idle_knight_frames
    current_monster_animation = draw_idle_monster
    total_monster_frames = total_idle_monster_frames
    attack_in_progress = False
    
    #Health and attack logic
    monster_hp = 200
    max_monster_hp = 200
    maxattack = 8
    attack = 0
    clock = pygame.time.Clock()
    frame_index_knight = 0
    frame_index_monster = 0
    start_time = pygame.time.get_ticks()
    buttons = None
    monster_dead = False
    knight_health = 100
    monster_attack_punches = random.sample(range(1, maxattack + 1), 5)

    #Actual game logic 🗣️
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main() 
            elif event.type == pygame.MOUSEBUTTONDOWN and buttons:
                mouse_pos = pygame.mouse.get_pos()
                for item, rect in buttons:
                    if rect.collidepoint(mouse_pos) and not monster_dead:
                        if item == "Attack" and not attack_in_progress:
                            current_knight_animation = draw_attack_knight
                            total_knight_frames = total_attack_knight_frames
                            frame_index_knight = 0  
                            attack_in_progress = True 
                            attack += 1
                            monster_hp -= 25  
                            if attack in monster_attack_punches:
                                current_knight_animation = draw_hurt_knight
                                total_attack_knight_frames = total_hurt_knight_frames
                                current_monster_animation = draw_attack_monster
                                total_monster_frames = total_attack_monster_frames
                                frame_index_monster = 0
                                knight_health -= 12
                                update(username, credits, hp, points, items)
                            if monster_hp > 0 and attack not in monster_attack_punches:
                                current_monster_animation = draw_hurt_monster
                                total_monster_frames = total_hurt_monster_frames
                                frame_index_monster = 0  
                            elif monster_hp <= 0:
                                defeat_time = pygame.time.get_ticks()
                                current_monster_animation = draw_death_monster
                                total_monster_frames = total_death_monster_frames
                                frame_index_monster = 0
                                points += 10
                                monster_dead = True
        screen.blit(background, (0, 0))
        if pygame.time.get_ticks() - start_time <= 2000:
            text(screen, "You didn't bought a torch!", position=(500, 200), align_center=True)
        if pygame.time.get_ticks() - start_time > 2000:
            text(screen, "You encountered a monster!", position=(500, 200), align_center=True)
            if pygame.time.get_ticks() - start_time > 4000:
                options = ["Attack"]
                buttons = option(screen, options, gap=10, font_size=30)
        creds(screen,credits)
        healthbar(screen, knight_health, 100, position=(50, 50))
        current_knight_animation(frame_index_knight)
        frame_index_knight = (frame_index_knight + 1) % total_knight_frames
        if attack_in_progress and frame_index_knight == 0:
            current_knight_animation = draw_idle_knight
            total_knight_frames = total_idle_knight_frames
            frame_index_knight = 0
            attack_in_progress = False
            if not monster_dead:
                current_monster_animation = draw_idle_monster
                total_monster_frames = total_idle_monster_frames
        current_monster_animation(frame_index_monster)
        if not monster_dead:
            frame_index_monster = (frame_index_monster + 1) % total_monster_frames
        else:
            frame_index_monster = min(frame_index_monster + 1, total_monster_frames - 1)
        if monster_hp > 0:
            healthbar(screen, monster_hp, max_monster_hp, position=(1020, 480), barw=80, barh=10)
        
        pygame.display.flip()
        if monster_dead and defeat_time and pygame.time.get_ticks() - defeat_time > 2000:
            text(screen, "Monster dealt extra damage as you didn't have a torch!", position=(500,500), align_center=True)
            pygame.display.flip()
            update(username, credits, hp, points, items)
            if monster_dead and defeat_time and pygame.time.get_ticks() - defeat_time > 5000:
                wizard(screen, knight_health, username)
        clock.tick(10)



def cave(screen, username):
    profile = fetch(username)
    c, hp, points, items = profile
    running = True
    background = bgloader("img/Background/cave.png")
    background = pygame.transform.scale(background, screen.get_size())
    draw_animation, total_frames = animation(screen, "img/Knight/Idle", 100, 500)
    clock = pygame.time.Clock()
    frame_index = 0
    start_time = pygame.time.get_ticks()
    buttons = None
    insufficient_credits_time = None
    item_bought_time = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()
            elif " |Torch| " in items:
                item_bought_time = 1
            elif event.type == pygame.MOUSEBUTTONDOWN and buttons:
                mouse_pos = pygame.mouse.get_pos()
                for item, rect in buttons:
                    if rect.collidepoint(mouse_pos):
                        if item == "Yes":
                            if c >= 200:
                                items += " |Torch| " 
                                c -= 200
                                update(username, c, hp, points, items)
                                caveLight(screen, username) 
                            else:
                                insufficient_credits_time = pygame.time.get_ticks()
                                c = 0 
                                update(username, c, hp, points, items)
                        elif item == "No":
                            caveDark(screen, username)
        screen.blit(background, (0, 0))
        if pygame.time.get_ticks() - start_time <= 2000:
            text(screen, "You just entered a cave. It's too dark!", position=(500, 200), align_center=True)
        elif not insufficient_credits_time:
            text(screen, "Buy a torch for 200 credits?", position=(500, 200), align_center=True)
            options = ["Yes", "No"]
            buttons = option(screen, options, gap=10, font_size=30)
        if item_bought_time:
            caveLight(screen, username, item_check=True)
        if insufficient_credits_time:
            if pygame.time.get_ticks() - insufficient_credits_time <= 2000:
                text(screen, "Wakey wakey brookie", position=(638, 250), align_center=True)
            else:
                caveDark(screen, username)
        creds(screen, c)
        healthbar(screen, 100, 100)
        draw_animation(frame_index)
        frame_index = (frame_index + 1) % total_frames
        pygame.display.flip()
        clock.tick(10)

#Start screen
def main():
    screen = pygame.display.set_mode((1366, 736))
    pygame.display.set_caption("Pookie Craft🎀")
    background = bgloader("img/Background/background.png")
    background = pygame.transform.scale(background, screen.get_size())
    draw_animation, total_frames = animation(screen, "img/Knight/Idle", 100, 500)
    menu_items = [
        "Play", "Search a Profile", 
        "View All Profiles", "Modify Player",  "Delete Player", "Delete All Players", "Exit"
    ]
    clock = pygame.time.Clock()
    frame_index = 0
    running = True
    username = ""

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for item, rect in buttons:
                    if rect.collidepoint(mouse_pos):
                        if item == "Play":
                            username = inp(screen, "Enter your username: ","Press Home to go back to menu")
                            profile = fetch(username)
                            if profile:
                                c, hp, points, items = profile
                                if hp == 0:
                                    text(screen, "You have 0hp please make another profile", position=(0,400), align_center=True)
                                    pygame.display.flip()
                                    pygame.time.wait(2000)
                                elif points == 0:
                                    cave(screen, username)
                                elif points == 10:
                                    wizard(screen, hp, username)
                                elif points == 20:
                                    huntress(screen, hp, username)
                            else:
                                dbmain(username)
                                cave(screen, username)
                        elif item == "Modify Player":
                            modify_profile(screen)
                        elif item == "Delete Player":
                            delete_profile(screen)
                        elif item == "View All Profiles":
                            check_all_profiles(screen)
                        elif item == "Search a Profile":
                            check_profile(screen)
                        elif item == "Delete All Players":
                            drop_all(screen)
                        elif item == "Exit":
                            running = False

        screen.blit(background, (0, 0))
        buttons = option(screen, menu_items, font_size=35, gap=40)
        draw_animation(frame_index)
        frame_index = (frame_index + 1) % total_frames
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()
main()
