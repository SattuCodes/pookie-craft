# Importing all the modules 
import pygame
import mysql.connector
import sys
import random
from PIL import Image, ImageFilter
import pygame.image

# MySQL connection
config = {
    'user' : 'root',
    'password' : '25110505',
    'host' : 'localhost',
}

def sqlconnect():
    return mysql.connector.connect(**config)

# MySQL Workflow
def dbname(n):
    con = sqlconnect()
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
    cursor.execute("SELECT name FROM data WHERE name=%s", (n,))
    result = cursor.fetchone()
    if result:
        con.close()
        return False
    else:
        cursor.execute("INSERT INTO data (name, credits, health, points, items) VALUES (%s, %s, %s, %s, %s)",
                       (n, 1000, 100, 0, ''))
        con.commit()
        con.close()
        return True

def fetch(n):
    con = sqlconnect()
    cursor = con.cursor()
    cursor.execute('USE backend')
    cursor.execute("SELECT credits, health, points, items FROM data WHERE name=%s", (n,))
    result = cursor.fetchone()
    con.close()
    return result

def fetch_all():
    con = sqlconnect()
    cursor = con.cursor()
    cursor.execute('USE backend')
    cursor.execute("SELECT name, credits, points FROM data")
    results = cursor.fetchall()
    con.close()
    return results

def update(n, credits, health, points, items):
    con = sqlconnect()
    cursor = con.cursor()
    cursor.execute('USE backend')
    cursor.execute("UPDATE data SET credits=%s, health=%s, points=%s, items=%s WHERE name=%s",
                   (credits, health, points, items, n))
    con.commit()
    con.close()

def deleteu(n):
    con = sqlconnect()
    cursor = con.cursor()
    cursor.execute('USE backend')
    cursor.execute("DELETE FROM data WHERE name=%s", (n,))
    con.commit()
    con.close()

def check_profile():
    username = inputs("Enter your username: ", cave_menu)
    profile = fetch(username)

    if profile:
        credits, hp, points, items = profile
        cave()
        font_oth(f"Username: {username}", 200)
        font_oth(f"Credits: {credits}", 250)
        font_oth(f"Health: {hp}", 300)
        font_oth(f"Points: {points}", 350)
        font_oth(f"Items: {items if items else 'None'}", 400)
        pygame.display.update()
        pygame.time.wait(4000)
    else:
        cave()
        font_oth("Username not found!", 250)
        pygame.display.update()
        pygame.time.wait(2000)

def check_all_profiles():
    profiles = fetch_all()

    if profiles:
        cave()
        y = 100
        for profile in profiles:
            username, credits, points = profile
            font_oth(f"Username: {username}, Credits: {credits}, Points: {points}", y)
            y += 50
        pygame.display.update()
        pygame.time.wait(4000)
    else:
        cave()
        font_oth("No profiles found!", 250)
        pygame.display.update()
        pygame.time.wait(2000)

def modify_profile():
    username = inputs("Enter your username: ", cave_menu)
    profile = fetch(username)

    if profile:
        credits, hp, points, items = profile

        new_credits = inputs(f"Modify credits (current: {credits}): ", cave_menu)
        new_hp = inputs(f"Modify health (current: {hp}): ", cave_menu)
        new_points = inputs(f"Modify points (current: {points}): ", cave_menu)
        new_items = inputs(f"Modify items (current: {items}): ", cave_menu)

        update(username, int(new_credits), int(new_hp), int(new_points), new_items)
        cave()
        font_oth("Profile updated successfully!", 250)
        pygame.display.update()
        pygame.time.wait(2000)
    else:
        cave()
        font_oth("Username not found!", 250)
        pygame.display.update()
        pygame.time.wait(2000)

def delete_profile():
    username = inputs("Enter your username to delete: ", cave_menu)
    profile = fetch(username)

    if profile:
        confirmation = inputs(f"Are you sure you want to delete the profile '{username}'? (yes/no): ", cave_menu)
        if confirmation.lower() in ['yes', 'y']:
            deleteu(username)
            cave()
            font_oth(f"Profile '{username}' deleted!", 250)
            pygame.display.update()
            pygame.time.wait(2000)
        else:
            cave()
            font_oth("Profile deletion canceled!", 250)
            pygame.display.update()
            pygame.time.wait(2000)
    else:
        cave()
        font_oth("Username not found!", 250)
        pygame.display.update()
        pygame.time.wait(2000)

def shop(username):
    profile = fetch(username)
    credits, hp, points, items = profile

    shop_items = {
        "Health Potion": 200,
        "Sword": 500,
        "Shield": 300
    }

    run = True
    while run:
        cave_m()
        fontm("Shop", 50)
        y = 100
        for item, cost in shop_items.items():
            font_oth(f"{item}: {cost} credits", y)
            y += 50
        font_oth("Press ESC to exit the shop", y)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                else:
                    selected_item = list(shop_items.keys())[event.key - pygame.K_1]
                    if credits >= shop_items[selected_item]:
                        credits -= shop_items[selected_item]
                        items += f"{selected_item},"
                        update(username, credits, hp, points, items)
                        cave()
                        font_oth(f"Purchased {selected_item}!", 250)
                        pygame.display.update()
                        pygame.time.wait(2000)
                    else:
                        cave()
                        font_oth("Not enough credits!", 250)
                        pygame.display.update()
                        pygame.time.wait(2000)

# Initialize all things inside pygame
pygame.init()

# FPS system
clock = pygame.time.Clock()
fps = 30

# Screen size and screen variables
screenw = 1366
screenh = 763
screen = pygame.display.set_mode((screenw, screenh))

# Game name setup
pygame.display.set_caption('Pookie Craft')

# Cave Rendering
cave_unblur = Image.open("img/Background/background.png")
cave_blur = cave_unblur.filter(ImageFilter.GaussianBlur(5))

# Convert blurred image to Pygame surface
cave_menu = pygame.image.fromstring(cave_blur.tobytes(), cave_blur.size, cave_blur.mode).convert_alpha()
cave_menu = pygame.transform.scale(cave_menu, (screenw, screenh))

# Convert unblurred image to Pygame surface
cave_img = pygame.image.fromstring(cave_unblur.tobytes(), cave_unblur.size, cave_unblur.mode).convert_alpha()
cave_img = pygame.transform.scale(cave_img, (screenw, screenh))

# Rendering inside the cave
in_cave = pygame.image.load("img/Background/cave.png")
in_cave = pygame.transform.scale(in_cave, (screenw, screenh))
l_cave = pygame.image.load("img/Background/cavelight.png")
l_cave = pygame.transform.scale(l_cave, (screenw, screenh))
def cave(): 
    screen.blit(cave_img, (0, 0))
def cave_m():
    screen.blit(cave_menu, (0, 0))
def inside_cave():
    screen.blit(in_cave, (0, 0))
def light_cave():
    screen.blit(l_cave, (0, 0))

#Wizard background rendering
wiz = pygame.image.load("img/Background/wizard.png")
wiz = pygame.transform.scale(wiz, (screenw, screenh))
def wizard():
    screen.blit(wiz, (0, 0))

#Rendering man part background
mbg = pygame.image.load("img/Background/man.png")
mbg = pygame.transform.scale(mbg, (screenw, screenh))
def man():
    screen.blit(mbg, (0, 0))
# Font Rendering - Using this to display font
# Menu Font
menu_font = pygame.font.Font("Exo-VariableFont_wght.ttf", 40)
def fontm(text, y):
    disp = menu_font.render(text, True, (255, 255, 255))
    menu_shape = disp.get_rect(center=(screenw // 2, y))
    screen.blit(disp, menu_shape)
# All other Font
other_font = pygame.font.Font("Exo-VariableFont_wght.ttf", 30)
def font_oth(text, y):
    disp = other_font.render(text, True, (255, 255, 255))
    menu_shape = disp.get_rect(center=(screenw // 2, y))
    screen.blit(disp, menu_shape)

class Instance():
	def __init__(self, x, y, name, max_hp, strength, potions):
		self.name = name
		self.max_hp = max_hp
		self.hp = max_hp
		self.strength = strength
		self.start_potions = potions
		self.potions = potions
		self.alive = True
		self.animation_list = []
		self.frame_index = 0
		self.action = 0#0:idle, 1:attack, 2:hurt, 3:dead
		self.update_time = pygame.time.get_ticks()
		#load idle images
		temp_list = []
		for i in range(8):
			img = pygame.image.load(f'img/{self.name}/Idle/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#load attack images
		temp_list = []
		for i in range(8):
			img = pygame.image.load(f'img/{self.name}/Attack/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		self.image = self.animation_list[self.action][self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)


	def update(self):
		animation_cooldown = 100
		#handle animation
		#update image
		self.image = self.animation_list[self.action][self.frame_index]
		#check if enough time has passed since the last update
		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1
		#if the animation has run out then reset back to the start
		if self.frame_index >= len(self.animation_list[self.action]):
			self.frame_index = 0




	def draw(self):
		screen.blit(self.image, self.rect)
player = Instance(200, 600, 'Knight', 100, 0, 0)
# Menu
def menu():
    run = True
    while run:
        clock.tick(fps)
        cave_m()
        fontm("Menu", 50)
        opt = ["Play", "Display a profile", "Display all profiles", "Delete a profile", "Modify a profile", "Shop", "Exit"]
        poss = []
        for i, x in enumerate(opt):
            y = 150 + i * 75
            font_oth(x, y)
            poss.append((pygame.Rect((screenw // 2 - 150, y - 25), (300, 50)), i))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for rect, i in poss:
                    if rect.collidepoint(mouse_pos):
                        if i == 0:
                            play()
                        elif i == 1:
                            check_profile()
                        elif i == 2:
                            check_all_profiles()
                        elif i == 3:
                            delete_profile()
                        elif i == 4:
                            modify_profile()
                        elif i == 5:
                            shop()
                        elif i == 6:
                            sys.exit()
                            
        clock.tick(fps)
def inputs(prompt, bg):
    user_inp = '' 
    input_status = True # It will take input until it's false
    while input_status: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_RETURN:
                    input_status = False # When user presses enter the status will turn to false and stop the loop
                elif event.key == pygame.K_BACKSPACE: # When user presses backspace it will delete that word using slicing
                    user_inp = user_inp[:-1]
                else:
                    user_inp += event.unicode
        screen.blit(bg, (0, 0))
        font_oth(prompt + user_inp, 200)
        pygame.display.update()
        clock.tick(fps)
    return user_inp

# Creating initializing for the game (it will check if user exists or not and add the name to the database)
def play():
    username = inputs("Enter your username: ", cave_menu) # This will move this str as argument to inputs function
    if dbname(username):
        cave()
        font_oth("Profile created!", 250)
        pygame.display.update()
        pygame.time.wait(2000)  # Wait for a while to show the message
    else:
        cave()
        font_oth("Username already exists!", 250)
        pygame.display.update()
        pygame.time.wait(2000)

    profile = fetch(username)  # Fetch user profile data
    credits, hp, points, items = profile

    cave()
    font_oth(f"Welcome back, {username}!", 200)
    font_oth(f"Credits: {credits}", 250)
    font_oth(f"Health: {hp}", 300)
    font_oth(f"Points: {points}", 350)
    font_oth(f"Items: {items if items else 'None'}", 400)
    pygame.display.update()
    pygame.time.wait(4000)  # Display the profile information for 4 seconds

    logic(username)  # Continue to the game logic
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


def display_credits(credits):
    credits_text = other_font.render(f"Credits: {credits}", True, (255, 255, 255))
    screen.blit(credits_text, (screenw - credits_text.get_width() - 20, 20))

def logic(username):
    class HealthBar:
        def __init__(self, max_hp):
            self.hp = max_hp
            self.max_hp = max_hp

        def draw(self, surface):
            change = self.hp / self.max_hp
            pygame.draw.rect(surface, "red", (50, 20, 250, 30))
            pygame.draw.rect(surface, "green", (50, 20, 250 * change, 30))


    def purchase(i_name, cost, bg):
        nonlocal credits, items
        choice = inputs(f"Do you want to buy a {i_name} for {cost} credits? [You have {credits} credits left]: ", bg)
        if choice.lower() in ['yes', 'y'] and credits >= cost:
            credits -= cost
            items += f"{i_name},"
            return True
        elif choice.lower() in ['yes', 'y'] and credits < cost:
            health.draw(screen)
            display_credits(credits)
            font_oth("Not enough credits!", 250)
            pygame.display.update()
            pygame.time.wait(2000)
        return False

    profile = fetch(username)
    credits, hp, points, items = profile
    health = HealthBar(hp)
    run = True
    
    while run:
        inside_cave()
        player.update()
        player.draw()
        health.draw(screen)
        display_credits(credits)
        font_oth("You just entered a cave. It's too dark!", 200)
        player.draw()
        pygame.display.update()
        pygame.time.wait(2000)
        
        torch = "torch" not in items
        if torch:
            if purchase("torch", 200, in_cave):
                player.draw()
                light_cave()
                health.draw(screen)
                display_credits(credits)
                font_oth("You bought a torch! It made everything visible!", 300)
                pygame.display.update()
                pygame.time.wait(2000)
            else:
                player.draw()
                inside_cave()
                health.draw(screen)
                display_credits(credits)
                font_oth("You didn't buy a torch.", 300)
                pygame.display.update()
                pygame.time.wait(2000)
        else:
            player.draw()
            light_cave()
            health.draw(screen)
            display_credits(credits)
            font_oth("Torch is already in the inventory!", 300)
            pygame.display.update()
            pygame.time.wait(2000)
        player.draw()
        health.draw(screen)
        display_credits(credits)
        font_oth("You encounter a monster!", 200)
        pygame.display.update()
        pygame.time.wait(2000)

        mob_health = 100
        while mob_health > 0:
            if "torch" not in items:
                inside_cave()
            else:
                light_cave()
            health.draw(screen)
            display_credits(credits)
            font_oth(f"Mob health: {max(0, mob_health)}", 50)
            font_oth("Choose your attack:", 100)
            font_oth("1. Kick", 150)
            font_oth("2. Punch", 200)
            pygame.display.update()

            attack_choice = None
            while attack_choice is None:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            mob_health -= 15
                            attack_choice = 'kick'
                        elif event.key == pygame.K_2:
                            mob_health -= 20
                            attack_choice = 'punch'
                        elif event.key == pygame.K_SPACE:
                            screen.fill((0,0,0))
                        mob_health = max(0, mob_health)
            if "torch" not in items:
                inside_cave()
            else:
                light_cave()
            health.draw(screen)
            display_credits(credits)
            font_oth(f"Mob health: {mob_health}", 50)
            pygame.display.update()

        points += 1
        update(username, credits, health.hp, points, items)
        if "torch" not in items:
            inside_cave()
        else:
            light_cave()
        font_oth("Monster defeated!", 250)
        if "torch" not in items:
            hp -= 20
            font_oth("You tripped on a stone while fighting due to no torch and lost 20HP.", 300)
        else:
            hp -= 5
            font_oth("You lost 5HP while fighting!", 300)
        health.hp = hp
        health.draw(screen)
        display_credits(credits)
        pygame.display.update()
        pygame.time.wait(2000)
        update(username, credits, health.hp, points, items)

        if "torch" not in items:
            inside_cave()
        else:
            light_cave()
        font_oth("You encountered a more powerful monster!", 250)
        health.draw(screen)
        display_credits(credits)
        pygame.display.update()
        pygame.time.wait(2000)

        if "torch" not in items:
            inside_cave()
            if purchase("sword", 500, in_cave):
                font_oth("You bought a sword.", 300)
            else:
                font_oth("You did not buy a sword.", 300)
        else:
            light_cave()
            if purchase("sword", 500, l_cave):
                font_oth("You bought a sword.", 300)
            else:
                font_oth("You did not buy a sword.", 300)
        pygame.display.update()
        pygame.time.wait(2000)

        if 'sword' in items and 'torch' in items:
            hp -= 10
            health.hp = hp
            health.draw(screen)
            display_credits(credits)
            font_oth("You defeated the monster but lost 10HP.", 350)
        elif 'sword' in items and 'torch' not in items:
            hp -= 20
            health.hp = hp
            health.draw(screen)
            display_credits(credits)
            font_oth("You fought with the monster but due to low visibility monster was able to deal more damage and you lost 20HP!", 350)
        elif 'sword' not in items and 'torch' in items:
            hp -= 60
            health.hp = hp
            health.draw(screen)
            display_credits(credits)
            font_oth('You did not have a sword and the monster was very powerful making you lose 60HP!', 350)
        else:
            hp -= 65
            health.hp = hp
            health.draw(screen)
            display_credits(credits)
            font_oth("You didn't have anything dwag!", 350)
        pygame.display.update()
        pygame.time.wait(3000)
        clock.tick(fps)

        run = False
        wizard()
        font_oth("You just encountered a wizard.", 250)
        display_credits(credits)
        pygame.display.update()
        pygame.time.wait(2000)
        problem = random.choice(["5+3", "7-2", "6*2", "8*2", "9*5"])
        answer = inputs(f"The wizard asks: What is {problem}: ", wiz)
        correct = eval(problem)
        if int(answer) == correct:
            font_oth("Correct! The wizard gives you a health potion! Use this potion to retain all your health.", 300)
            items += "Health Potion,"
        else:
            font_oth("Incorrect! The wizard disappears.", 300)
        update(username, credits, health.hp, points, items)
        health.hp = hp
        health.draw(screen)
        display_credits(credits)
        pygame.display.update()
        pygame.time.wait(2000)

        man()
        font_oth("A stranger asks you for help!", 300)
        display_credits(credits)
        pygame.display.update()
        pygame.time.wait(2000)
        if inputs("Do you want to help him? (yes/no): ", mbg) in ['yes','y']:
            items += 'Revive Stone,'
            credits += 1000
            font_oth("You helped the man! He gave you a revive stone and 1000 credits as a token of appreciation!", 300)
        else: 
            hp -= 5
            font_oth("You did not help the man, he cursed you, which led you to lose 5hp!", 300)
        update(username, credits, health.hp, points, items)
        display_credits(credits)
        pygame.display.update()
        pygame.time.wait(2000)

        run = False

menu()