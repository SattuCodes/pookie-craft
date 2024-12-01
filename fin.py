#Importing all the modules
import pygame
import mysql.connector
import random
import os
import sys
import pygame.image
pygame.init()

#Main Global Variable
screen = pygame.display.set_mode((1366, 736))
pygame.display.set_caption("Pookie Craft 🎀")
clock = pygame.time.Clock()
fps = 10

#MySQL
sqlCred = {
    'user': 'root',
    'password': '2511007',
    'host': 'localhost',
}


def conn():
    return mysql.connector.connect(**sqlCred)

def insert(name):
    con = conn()
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
    cursor.execute("SELECT name FROM data WHERE name=%s", (name,))
    result = cursor.fetchone()
    if result:
        con.close()
        return False
    else:
        cursor.execute("INSERT INTO data (name, credits, health, points, items) VALUES (%s, %s, %s, %s, %s)", (name, 1000, 100, 0, ''))
        con.commit()
        con.close()
        return True

def fetch(name):
    con = conn()
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
    cursor.execute("SELECT credits, health, points, items FROM data WHERE name=%s", (name,))
    result = cursor.fetchone()
    con.close()
    return result

def fetch_all():
    con = conn()
    cursor = con.cursor()
    cursor.execute('USE backend')
    cursor.execute("SELECT name, credits, points FROM data")
    results = cursor.fetchall()
    con.close()
    return results

def update(name, credits, health, points, items):
    con = conn()
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
    cursor.execute("UPDATE data SET credits=%s, health=%s, points=%s, items=%s WHERE name=%s", (credits, health, points, items, name))
    con.commit()
    con.close()

def delete(name):
    con = conn()
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
    cursor.execute("DELETE FROM data WHERE name=%s", (name,))
    con.commit()
    con.close()


#pygame
def fetchprofile():
    username = inpoot("Enter your username: ", "Press Home to go back to menu")
    profile = fetch(username)
    if profile:
        screen.fill((0, 0, 0))
        credits, hp, points, items = profile
        text(f"Username: {username}", position=(638, 200), align_center=True)
        text(f"Credits: {credits}", position=(638, 250), align_center=True)
        text(f"Health: {hp}", position=(638, 300), align_center=True)
        text(f"Points: {points}", position=(638, 350), align_center=True)
        text(f"Items: {items if items else 'None'}", position=(638, 400), align_center=True)
        pygame.display.update()
        inpoot('', 'Press Home to go back to menu', clear=False)
    else:
        screen.fill((0, 0, 0))
        text("Username not found!", position=(250, 200), align_center=True)
        pygame.display.update()
        pygame.time.wait(2000)

def fetchallprofile():
    profiles = fetch_all()
    if profiles:
        screen.fill((0,0,0))
        y = 100
        for x in profiles:
            username, creds, points = x 
            text(f"Username: {username}, Credits: {creds}, Points: {points}", position=(508, y), align_center=True)
            y += 50
        pygame.display.update()
        inpoot('', 'Press Home to go back to menu', clear=False)
    else:
        screen.fill((0,0,0))
        text("No profiles found!", position=(0,250), align_center=True)
        pygame.display.update()
        pygame.time.wait(2000)

def modify():
    name = inpoot("Enter your username: ", "Press Home to go back to menu")
    profile = fetch(name)
    if profile:
        creds, hp, points, items = profile
        while True:
            choice = inpoot("What do you want to modify?", "Options: Credits, Health, Points, Items").lower()
            if choice == "credits":
                new_credits = inpoot(f"Modify credits (current: {creds}): ")
                update(name, int(new_credits), hp, points, items)
                break
            elif choice == "health":
                new_hp = inpoot(f"Modify health (current: {hp}): ")
                update(name, creds, int(new_hp), points, items)
                break
            elif choice == "points":
                new_points = inpoot(f"Modify points (current: {points}): ")
                update(name, creds, hp, int(new_points), items)
                break
            elif choice == "items":
                new_items = inpoot(f"Modify items (current: {items}): ")
                update(name, creds, hp, points, new_items)
                break
            else:
                text("Invalid choice! Please select again or Press Home.", position=(screen.get_width()//2, 250), align_center=True)
                pygame.display.update()
                pygame.time.wait(3000)
        text("Profile updated successfully!", position=(700, 600), align_center=True)
        pygame.display.update()
        pygame.time.wait(2000)

def pydel():
    name = inpoot("Enter your username to delete: ","Press Home to go back to menu")
    profile = fetch(name)
    if profile:
        conf = inpoot(f"Are you sure you want to delete the profile '{name}'? (yes/no): ", "Press Home to go back to menu")
        if conf.lower() in ['yes', 'y']:
            delete(name)
            text(f"Profile '{name}' deleted!", position=(638,250))
            pygame.display.update()
            pygame.time.wait(2000)
        else:
            text("Profile deletion canceled!", position=(638,250))
            pygame.display.update()
            pygame.time.wait(2000)
    else:
        text("Username not found!", position=(0, 450), align_center=True)
        pygame.display.update()
        pygame.time.wait(2000)

def pydelall():
    #including MySQL
    con = conn()
    cursor = con.cursor()
    cursor.execute("USE backend")
    try:
        x = inpoot("Are you sure you want to delete all the profiles?(y/n)", "Press Home to go back to menu").lower()
        if x == 'y':
            cursor.execute("DROP TABLE data")
            con.commit()
            screen.fill((0, 0, 0))
            text("Deleted all the profiles.", position=(638, 250), align_center=True, font_sz=40)
        else:
            text("No record found.", position=(638, 250), align_center=True, font_sz=40)
            menu()
    except:
        text("Error occured: ", position=(638, 250), align_center=True, font_sz=40)
    con.close()
    pygame.display.update()
    pygame.time.wait(2000)

def animation(folder=None, x=0, y=0, scl=3):
    frames = []
    for frame in sorted(os.listdir(folder)):
        img = pygame.image.load(os.path.join(folder, frame))
        scaled = pygame.transform.scale(img, (img.get_width()*scl, img.get_height()*scl))
        frames.append(scaled)
    def draw(frame_index):
        frame_index %= len(frames)
        screen.blit(frames[frame_index], (x, y))
    return draw, len(frames)

def bgloader(path):
    return pygame.image.load(path)

def text(text, position, font_sz=30, color=(255, 255, 255), align_center=False):
    font = pygame.font.Font('exo.ttf', font_sz)
    surf = font.render(text, True, color)
    surfbox = surf.get_rect()
    if align_center:
        surfbox.midtop = (screen.get_width()//2, position[1])
    else:
        surfbox.topleft = position
    screen.blit(surf, surfbox.topleft)
    return surf, surfbox

def healthbar(health, maxhp, position=(50,50), barw=200, barh=20, color=(255,0,0), gc=(0,255,0), rc=(255,0,0), bg=(100,100,100)):
    fill = int((health/maxhp)*barw)
    color = (
        int(gc[0] + (rc[0] - gc[0]) * (1 - health / maxhp)),
        int(gc[1] + (rc[1] - gc[1]) * (1 - health / maxhp)),
        int(gc[2] + (rc[2] - gc[2]) * (1 - health / maxhp))
    )
    pygame.draw.rect(screen, bg, (*position, barw, barh))
    pygame.draw.rect(screen, color, (*position, fill, barh))

def creds(currcred):
    text(f'Credits: {currcred}', position=(1200,50), font_sz=20)

def option(items, font_sz=40, gap=20):
    font = pygame.font.Font("exo.ttf", font_sz)
    buttons = []
    screen_rect = screen.get_rect()
    total_height = len(items) * (font_sz + gap)
    start_y = (screen_rect.height - total_height) // 2

    for index, item in enumerate(items):
        text = font.render(item, True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (screen_rect.centerx, start_y + index * (font_sz + gap))
        screen.blit(text, text_rect)
        buttons.append((item, text_rect))

    return buttons

def inpoot(text1, text2='', font_sz=40, clear=True):
    output = ''
    input_ongoing = True
    font = pygame.font.Font("exo.ttf", font_sz)
    drawing = True
    while input_ongoing:
        for x in pygame.event.get():
            if x.type == pygame.QUIT:
                sys.exit()
            elif x.type == pygame.KEYDOWN:
                if x.key == pygame.K_RETURN:
                    input_ongoing = False
                elif x.key == pygame.K_HOME:
                    menu()
                elif x.key == pygame.K_BACKSPACE:
                    output = output[:-1]
                    drawing = True
                else: 
                    output += x.unicode
                    drawing = True
        if drawing:
            if clear:
                screen.fill((0, 0, 0))
            if text2 == '':
                prompt = font.render(text1, True, (255, 255, 255))
                output_render = font.render(output, True, (255, 255, 255))
                screen.blit(prompt, (screen.get_width()//2 - prompt.get_width()//2, 200))
                screen.blit(output_render, (screen.get_width()//2 - output_render.get_width()//2, 300))
            else:
                text(f"{text2}", position=(683, 568), align_center=True)
                prompt = font.render(text1, True, (255, 255, 255))
                output_render = font.render(output, True, (255, 255, 255))
                screen.blit(prompt, (screen.get_width()//2 - prompt.get_width()//2, 200))
                screen.blit(output_render, (screen.get_width()//2 - output_render.get_width()//2, 300))
            pygame.display.flip()
            drawing = False
        clock.tick(fps)
    return output

def misc(knight_health, username):
    profile = fetch(username)
    credits, hp, points, items = profile
    background = bgloader("img/Background/misc.png")
    background = pygame.transform.scale(background, screen.get_size())
    
    draw_idle_knight, total_idle_knight_frames = animation("img/Knight/Idle", 100, 500, scl=3)
    draw_attack_knight, total_attack_knight_frames = animation("img/Knight/Attack", 100, 500, scl=3)
    draw_idle_huntress, total_idle_huntress_frames = animation("img/Huntress/Idle", 1000, 525, scl=3)
    draw_attack_huntress, total_attack_huntress_frames = animation("img/Huntress/Attack", 1000, 525, scl=3)
    draw_hurt_huntress, total_hurt_huntress_frames = animation("img/Huntress/Hurt", 1000, 525, scl=3)
    draw_death_huntress, total_death_huntress_frames = animation("img/Huntress/Death", 1000, 525, scl=3)
    draw_idle_princess, total_idle_princess_frames = animation("img/Win", 1000, 525, scl=2)

    current_knight_animation = draw_idle_knight
    total_knight_frames = total_idle_knight_frames
    current_huntress_animation = draw_idle_huntress
    total_huntress_frames = total_idle_huntress_frames

    frame_index_knight = 0
    frame_index_huntress = 0
    frame_index_princess = 0
    huntress_hp = 100
    max_huntress_hp = 100
    attack_in_progress = False
    huntress_dead = False
    victory_time = None
    start_time = pygame.time.get_ticks()
    buttons = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and buttons:
                mouse_pos = pygame.mouse.get_pos()
                for item, rect in buttons:
                    if rect.collidepoint(mouse_pos) and not huntress_dead:
                        if item == "Attack" and not attack_in_progress:
                            current_knight_animation = draw_attack_knight
                            total_knight_frames = total_attack_knight_frames
                            frame_index_knight = 0
                            attack_in_progress = True
                            huntress_hp -= 30
                            if huntress_hp > 0:
                                current_huntress_animation = draw_hurt_huntress
                                total_huntress_frames = total_hurt_huntress_frames
                                frame_index_huntress = 0
                            else:
                                huntress_dead = True
                                current_huntress_animation = draw_death_huntress
                                total_huntress_frames = total_death_huntress_frames
                                frame_index_huntress = 0
                                victory_time = pygame.time.get_ticks()
        screen.blit(background, (0, 0))
        elapsed_time = pygame.time.get_ticks() - start_time
        if elapsed_time <= 2000:
            text("You encountered a huntress!", position=(screen.get_width() // 2, 200), align_center=True)
        elif elapsed_time <= 4000:
            text("Since the wizard gave you a shield, you are immune to this attack!", position=(screen.get_width() // 2, 200), align_center=True)
            current_huntress_animation = draw_attack_huntress
            total_huntress_frames = total_attack_huntress_frames
        else:
            if not huntress_dead:
                current_huntress_animation = draw_idle_huntress
                total_huntress_frames = total_idle_huntress_frames
                buttons = option(["Attack"], gap=10, font_sz=30)
            else:
                buttons = None
        if huntress_dead:
            if frame_index_huntress < total_huntress_frames - 1:
                current_huntress_animation(frame_index_huntress)
                frame_index_huntress += 1
            else:
                draw_idle_princess(frame_index_princess)
                frame_index_princess = (frame_index_princess + 1) % total_idle_princess_frames
                text("You won! You found your princess!", position=(screen.get_width() // 2, 200), align_center=True, font_sz=50)
                if pygame.time.get_ticks() - victory_time >= 8000:
                    menu()
                    return
        current_knight_animation(frame_index_knight)
        frame_index_knight = (frame_index_knight + 1) % total_knight_frames
        if not huntress_dead:
            current_huntress_animation(frame_index_huntress)
            frame_index_huntress = (frame_index_huntress + 1) % total_huntress_frames
        else:
            frame_index_huntress = min(frame_index_huntress + 1, total_huntress_frames - 1)
        healthbar(knight_health, maxhp=100, position=(50, 50))
        if huntress_hp > 0:
            healthbar(huntress_hp, maxhp=max_huntress_hp, position=(1020, 480), barw=80, barh=10)
        pygame.display.flip()
        if attack_in_progress and frame_index_knight == 0:
            current_knight_animation = draw_idle_knight
            total_knight_frames = total_idle_knight_frames
            frame_index_knight = 0
            attack_in_progress = False
            if not huntress_dead:
                current_huntress_animation = draw_idle_huntress
                total_huntress_frames = total_idle_huntress_frames
        clock.tick(fps)

def wizard(knight_health, username):
    profile = fetch(username)
    credits, hp, points, items = profile
    background = bgloader("img/Background/wizard.png")
    draw_idle_knight, total_idle_knight_frames = animation("img/Knight/Idle", 100, 500, scl=3)
    draw_death_knight, total_death_knight_frames = animation("img/Knight/Death", 100, 500, scl=3)
    draw_idle_wizard, total_idle_wizard_frames = animation("img/Wizard/Idle", 1000, 500, scl=2)
    draw_attack_wizard, total_attack_wizard_frames = animation("img/Wizard/Attack", 1000, 500, scl=2)
    current_knight_animation = draw_idle_knight
    total_knight_frames = total_idle_knight_frames
    current_wizard_animation = draw_idle_wizard
    total_wizard_frames = total_idle_wizard_frames
    num1, num2 = None, None
    correct_answer = None
    player_answer = ""
    question_asked = False
    question_start_time = None
    answer_phase = False
    is_game_over = False
    success_display_start = None  
    frame_index_knight = 0
    frame_index_wizard = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if question_asked and answer_phase:
                    if event.key == pygame.K_RETURN:
                        if player_answer.isdigit() and int(player_answer) == correct_answer:
                            knight_health = 100 
                            points += 10
                            items += " |Totem| "
                            update(username, credits, knight_health, points, items)
                            success_display_start = pygame.time.get_ticks() 
                            question_asked = False
                            answer_phase = False
                        else:
                            knight_health -= 50
                            update(username, credits, knight_health, points, items)
                            if knight_health <= 0:
                                is_game_over = True
                            question_asked = False
                            answer_phase = False
                        player_answer = "" 
                    elif pygame.K_0 <= event.key <= pygame.K_9:
                        player_answer += event.unicode
        screen.blit(background, (0, 0))
        if success_display_start:
            text("You answered correctly! The wizard gave you a shield. You continued your journey.", position=(screen.get_width() // 2, 200), align_center=True)
            current_knight_animation(frame_index_knight)
            current_wizard_animation(frame_index_wizard)
            frame_index_knight = (frame_index_knight + 1) % total_knight_frames
            frame_index_wizard = (frame_index_wizard + 1) % total_wizard_frames
            if pygame.time.get_ticks() - success_display_start > 4000:
                misc(knight_health, username)
                return
        elif not is_game_over:
            if not question_asked:
                num1, num2 = random.randint(1, 10), random.randint(1, 10)
                correct_answer = num1 + num2
                question_start_time = pygame.time.get_ticks() 
                question_asked = True
            if question_asked:
                if pygame.time.get_ticks() - question_start_time <= 3000: 
                    text(f"What is {num1} + {num2}?", position=(screen.get_width() // 2, 200), align_center=True)
                else:
                    answer_phase = True
                    text(f"Your answer: {player_answer}", position=(screen.get_width() // 2, 300), align_center=True)
            healthbar(knight_health, maxhp=100, position=(50, 50))
            current_knight_animation(frame_index_knight)
            frame_index_knight = (frame_index_knight + 1) % total_knight_frames
            current_wizard_animation(frame_index_wizard)
            frame_index_wizard = (frame_index_wizard + 1) % total_wizard_frames
        else:
            current_knight_animation = draw_death_knight
            current_wizard_animation = draw_attack_wizard
            current_knight_animation(frame_index_knight)
            current_wizard_animation(frame_index_wizard)
            frame_index_knight += 1
            frame_index_wizard += 1
            if frame_index_knight >= total_death_knight_frames and frame_index_wizard >= total_attack_wizard_frames:
                text("Game Over", position=(screen.get_width() // 2, 200), align_center=True)
                pygame.display.flip()
                pygame.time.wait(2000)
                menu()
        pygame.display.flip()
        clock.tick(fps)

def caveLight(username, item_check=False):
    profile = fetch(username)
    credits, hp, points, items = profile
    running = True
    background = bgloader("img/Background/cavelight.png")
    background = pygame.transform.scale(background, screen.get_size())
    
    draw_idle_knight, total_idle_knight_frames = animation("img/Knight/Idle", 100, 500, scl=3)
    draw_attack_knight, total_attack_knight_frames = animation("img/Knight/Attack", 100, 500, scl=3)
    draw_hurt_knight, total_hurt_knight_frames = animation("img/Knight/Hurt", 100, 500, scl=3)
    
    draw_idle_monster, total_idle_monster_frames = animation("img/Monsters/Idle", 1000, 500, scl=3)
    draw_hurt_monster, total_hurt_monster_frames = animation("img/Monsters/Hurt", 1000, 500, scl=3)
    draw_attack_monster, total_attack_monster_frames = animation("img/Monsters/Attack", 1000, 500, scl=3)
    draw_death_monster, total_death_monster_frames = animation("img/Monsters/Death", 1000, 600, scl=3)
    
    current_knight_animation = draw_idle_knight
    total_knight_frames = total_idle_knight_frames
    current_monster_animation = draw_idle_monster
    total_monster_frames = total_idle_monster_frames
    attack_in_progress = False
    
    monster_hp = 200
    max_monster_hp = 200
    maxattack = 8
    attack = 0
    frame_index_knight = 0
    frame_index_monster = 0
    start_time = pygame.time.get_ticks()
    buttons = None
    monster_dead = False
    knight_health = 100
    monster_attack_punches = random.sample(range(1, maxattack + 1), 5)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu()
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
            text("You already have a torch in your inventory!", position=(500, 200), align_center=True)
        elif pygame.time.get_ticks() - start_time <= 2000:
            text("You bought a torch and made everything visible.", position=(500, 200), align_center=True)
        if pygame.time.get_ticks() - start_time > 2000:
            text("You encountered a monster!", position=(500, 200), align_center=True)
            if pygame.time.get_ticks() - start_time > 4000:
                options = ["Attack"]
                buttons = option(options, gap=10, font_sz=30)
        creds(credits)
        healthbar(knight_health, 100, position=(50, 50))
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
            healthbar(monster_hp, max_monster_hp, position=(1020, 480), barw=80, barh=10)
        
        pygame.display.flip()
        if monster_dead and defeat_time and pygame.time.get_ticks() - defeat_time > 2000:
            text("Defeated the monster! You continued your journey", position=(500,500), align_center=True)
            pygame.display.flip()
            update(username, credits, hp, points, items)
            if monster_dead and defeat_time and pygame.time.get_ticks() - defeat_time > 5000:
                wizard(knight_health, username)
        clock.tick(fps)

def caveDark(username):
    profile = fetch(username)
    credits, hp, points, items = profile
    running = True
    background = bgloader("img/Background/cave.png")
    background = pygame.transform.scale(background, screen.get_size())
    
    draw_idle_knight, total_idle_knight_frames = animation("img/Knight/Idle", 100, 500, scl=3)
    draw_attack_knight, total_attack_knight_frames = animation("img/Knight/Attack", 100, 500, scl=3)
    draw_hurt_knight, total_hurt_knight_frames = animation("img/Knight/Hurt", 100, 500, scl=3)
    
    draw_idle_monster, total_idle_monster_frames = animation("img/Monsters/Idle", 1000, 500, scl=3)
    draw_hurt_monster, total_hurt_monster_frames = animation("img/Monsters/Hurt", 1000, 500, scl=3)
    draw_attack_monster, total_attack_monster_frames = animation("img/Monsters/Attack", 1000, 500, scl=3)
    draw_death_monster, total_death_monster_frames = animation("img/Monsters/Death", 1000, 600, scl=3)
    
    current_knight_animation = draw_idle_knight
    total_knight_frames = total_idle_knight_frames
    current_monster_animation = draw_idle_monster
    total_monster_frames = total_idle_monster_frames
    attack_in_progress = False
    
    monster_hp = 200
    max_monster_hp = 200
    maxattack = 8
    attack = 0
    frame_index_knight = 0
    frame_index_monster = 0
    start_time = pygame.time.get_ticks()
    buttons = None
    monster_dead = False
    knight_health = 100
    monster_attack_punches = random.sample(range(1, maxattack + 1), 5)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_HOME:
                    menu
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
            text("You didn't bought a torch!", position=(500, 200), align_center=True)
        if pygame.time.get_ticks() - start_time > 2000:
            text("You encountered a monster!", position=(500, 200), align_center=True)
            if pygame.time.get_ticks() - start_time > 4000:
                options = ["Attack"]
                buttons = option(options, gap=10, font_sz=30)
        creds(credits)
        healthbar(knight_health, 100, position=(50, 50))
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
            healthbar(monster_hp, max_monster_hp, position=(1020, 480), barw=80, barh=10)
        
        pygame.display.flip()
        if monster_dead and defeat_time and pygame.time.get_ticks() - defeat_time > 2000:
            text("Monster dealt extra damage as you didn't have a torch!", position=(500,500), align_center=True)
            pygame.display.flip()
            update(username, credits, hp, points, items)
            if monster_dead and defeat_time and pygame.time.get_ticks() - defeat_time > 5000:
                wizard(knight_health, username)
        clock.tick(fps)

def cave(username):
    profile = fetch(username)
    c, hp, points, items = profile
    running = True
    background = bgloader("img/Background/cave.png")
    background = pygame.transform.scale(background, screen.get_size())
    draw_animation, total_frames = animation("img/Knight/Idle", 100, 500)
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
                if event.key == pygame.K_HOME:
                    menu()
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
                                caveLight(username) 
                            else:
                                insufficient_credits_time = pygame.time.get_ticks()
                                c = 0 
                                update(username, c, hp, points, items)
                        elif item == "No":
                            caveDark(username)
        screen.blit(background, (0, 0))
        if pygame.time.get_ticks() - start_time <= 2000:
            text("You just entered a cave. It's too dark!", position=(500, 200), align_center=True)
        elif not insufficient_credits_time:
            text("Buy a torch for 200 credits?", position=(500, 200), align_center=True)
            options = ["Yes", "No"]
            buttons = option(options, gap=10, font_sz=30)
        if item_bought_time:
            caveLight(username, item_check=True)
        if insufficient_credits_time:
            if pygame.time.get_ticks() - insufficient_credits_time <= 2000:
                text("You don't have sufficient funds!", position=(638, 250), align_center=True)
            else:
                caveDark(username)
        creds(c)
        healthbar(100, 100)
        draw_animation(frame_index)
        frame_index = (frame_index + 1) % total_frames
        pygame.display.flip()
        clock.tick(fps)

def admin():
    background = bgloader("img/Background/background.png")
    background = pygame.transform.scale(background, screen.get_size())
    image, frames = animation("img/Knight/Idle", 100, 500)
    items = ['Modify Profile', 'Delete Profile', 'Delete All Profiles', 'Back', 'Exit']
    current_frame = 0 
    running = True
    while running:
        for x in pygame.event.get():
            if x.type == pygame.QUIT:
                sys.exit()
            elif x.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for item, rect in buttons:
                    if rect.collidepoint(mouse_pos):
                        if item == "Modify Profile":
                            modify()
                        elif item == "Delete Profile":
                            pydel()
                        elif item == "Delete All Profiles":
                            pydelall()
                        elif item == "Back":
                            menu()
                        elif item == "Exit":
                            sys.exit()
        screen.blit(background, (0, 0))
        buttons = option(items, font_sz=35, gap=40)
        image(current_frame)
        current_frame = (current_frame + 1) % frames
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()

def menu():
    background = bgloader("img/Background/background.png")
    background = pygame.transform.scale(background, screen.get_size())
    image, frames = animation("img/Knight/Idle", 100, 500)
    items = ['Play', 'Search a Profile', 'View All Profiles', 'Admin Options','Exit']
    current_frame = 0
    running = True
    username = ''

    while running:
        for x in pygame.event.get():
            if x.type == pygame.QUIT:
                sys.exit()
            elif x.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for item, rect in buttons: 
                    if rect.collidepoint(mouse_pos):
                        if item == "Play":
                            username = inpoot("Enter your username: ", "Press Home to go back to menu")
                            profile = fetch(username)
                            if profile:
                                c, hp, points, items = profile
                                if hp == 0:
                                    text("You died. Please make another profile.", position=(0, 400), align_center=True)
                                    pygame.display.flip()
                                    pygame.time.wait(2000)
                                    menu()
                                elif points == 0:
                                    cave(username)
                                elif points == 10:
                                    wizard(hp, username)
                                elif points == 20:
                                    misc(hp, username)
                            else:
                                insert(username)
                                cave(username)
                        elif item == "Search a Profile":
                            fetchprofile()
                        elif item == "View All Profiles":
                            fetchallprofile()
                        elif item == "Admin Options":
                            admin()
                        elif item == "Exit":
                            sys.exit()

        screen.blit(background, (0, 0))
        buttons = option(items, font_sz=35, gap=40)
        image(current_frame)
        current_frame = (current_frame + 1) % frames
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
menu()
