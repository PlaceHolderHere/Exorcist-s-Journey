import pygame
from random import randint


# Classes
class Button:
    def __init__(self, x, y, size_x, size_y, image):
        self.x = x
        self.y = y
        self.sizeX = size_x
        self.sizeY = size_y
        self.clicked = 0
        self.image = image
        self.rect = pygame.rect.Rect(x, y, image.get_width(), image.get_height())

    def blit(self, win):
        win.blit(self.image, (self.x, self.y))

        if self.clicked > 0:
            self.clicked -= 1

        mouse_position = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_position):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked <= 0:
                self.clicked = 10
                return True


class DemonCard:
    def __init__(self, x, y, sprite, health, damage, cost):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.sizeX = self.sprite.get_width()
        self.sizeY = self.sprite.get_height()
        self.rect = pygame.rect.Rect(x, y, self.sprite.get_width(), self.sprite.get_height())

        self.health = health
        self.damage = damage
        self.cost = cost

        self.clicked = 0
        self.selected = -1
        self.used = False
        self.card_type = -1  # 0-Gospel; 1-Artifact; 2-Prayer; 3-Latin Chant

    def blit(self, win):
        win.blit(self.sprite, (self.x, self.y))

    def is_selected(self):
        mouse_position = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_position):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked <= 0:
                self.clicked = 5
                return True

            if self.clicked > 0:
                self.clicked -= 1


class PlayerCard:
    def __init__(self, x, y, sprite, health, damage, cost):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.sizeX = self.sprite.get_width()
        self.sizeY = self.sprite.get_height()
        self.rect = pygame.rect.Rect(x, y, self.sprite.get_width(), self.sprite.get_height())

        self.health = health
        self.damage = damage
        self.cost = cost

        self.clicked = 0
        self.selected = -1
        self.used = False
        # 0-Gospel; 1-Artifact; 2-Prayer; 3-Latin Chant
        self.card_type = -1

    def blit(self, win):
        win.blit(self.sprite, (self.x, self.y))

    def is_selected(self):
        mouse_position = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_position):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked <= 0:
                self.clicked = 5
                return True

            if self.clicked > 0:
                self.clicked -= 1


# Functions
def display_text(win, x, y, msg, color, font, font_size):
    pygame.font.init()

    font = pygame.font.Font(font, font_size)
    text = font.render(msg, False, color)
    text_rect = text.get_rect(center=(x, y))

    win.blit(text, text_rect)


def get_card_costs(cards):
    card_costs = []
    for card_index, card in enumerate(cards):
        card_costs.append((card.cost, card_index))

    card_costs.sort()
    return card_costs


def get_empty_card_slots(card_list):
    cards = []
    for card_index, card in enumerate(card_list):
        if card.card_type == -1:
            cards.append(card_index)

    return cards


def get_card_health(card_list):
    cards = []
    for card_index, card in enumerate(card_list):
        if card.card_type >= 0:
            cards.append((card.health, card_index))

    cards.sort()
    return cards


def get_cost_and_damage(card_list):
    cards = []
    for card_index, card in enumerate(card_list):
        cards.append((card.cost, card.damage, card_index))

    cards.sort()
    return cards

def get_damage(card_list):
    cards = []
    for card_index, card in enumerate(card_list):
        cards.append((card.damage, card_index))

    cards.sort(reverse=True)
    return cards


# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CLOCK = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Init
pygame.init()
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Exorcist's Journey")
running = True
start = False

# Health, Damage, Cost
# 0-Gospel; 1-Artifact; 2-Prayer; 3-Latin Chant
card_types = ((3, 0, 0), (5, 1, 5), (3, 2, 10), (3, 5, 15))

# Player Variables
cards_in_player_hand = [
    PlayerCard(90, 480, pygame.image.load('assets/Blank Card.png'), 0, 0, 0),
    PlayerCard(180, 480, pygame.image.load('assets/Blank Card.png'), 0, 0, 0),
    PlayerCard(270, 480, pygame.image.load('assets/Blank Card.png'), 0, 0, 0),
    PlayerCard(360, 480, pygame.image.load('assets/Blank Card.png'), 0, 0, 0),
    PlayerCard(450, 480, pygame.image.load('assets/Blank Card.png'), 0, 0, 0)]
cards_on_player_table = [PlayerCard(90, 300, pygame.image.load('Assets/New Card.png'), 0, 0, 0),
                         PlayerCard(180, 300, pygame.image.load('Assets/New Card.png'), 0, 0, 0),
                         PlayerCard(270, 300, pygame.image.load('Assets/New Card.png'), 0, 0, 0),
                         PlayerCard(360, 300, pygame.image.load('Assets/New Card.png'), 0, 0, 0),
                         PlayerCard(450, 300, pygame.image.load('Assets/New Card.png'), 0, 0, 0), ]

player_health = 100
player_stamina = 50

# Stages: 1-Draw_Card; 2-Place Cards; 3-Play Cards; 4-Use Gospel Cards
player_turn_stage = 1

# Demon Variables
demon_health = 100
demon_stamina = 50

cards_in_demon_hand = [
    DemonCard(90, 20, pygame.image.load('Assets/blank_demon_card.png'), 0, 0, 0),
    DemonCard(180, 20, pygame.image.load('Assets/blank_demon_card.png'), 0, 0, 0),
    DemonCard(270, 20, pygame.image.load('Assets/blank_demon_card.png'), 0, 0, 0),
    DemonCard(360, 20, pygame.image.load('Assets/blank_demon_card.png'), 0, 0, 0),
    DemonCard(450, 20, pygame.image.load('Assets/blank_demon_card.png'), 0, 0, 0)]
cards_on_demon_table = [DemonCard(90, 180, pygame.image.load('Assets/blank_demon_card.png'), 0, 0, 0),
                        DemonCard(180, 180, pygame.image.load('Assets/blank_demon_card.png'), 0, 0, 0),
                        DemonCard(270, 180, pygame.image.load('Assets/blank_demon_card.png'), 0, 0, 0),
                        DemonCard(360, 180, pygame.image.load('Assets/blank_demon_card.png'), 0, 0, 0),
                        DemonCard(450, 180, pygame.image.load('Assets/blank_demon_card.png'), 0, 0, 0), ]

# Stages: 1-Draw_Card; 2-Place Cards; 3-Play Cards; 4-Use Gospel Cards
demon_turn_stage = 1
demon_turn = -1

# Buttons
start_button = Button(400 - (196 / 2), 300 - 32, 400, 160, pygame.image.load('Assets/Play.png'))

play_card_button = Button(600, 450, 100, 40, pygame.image.load('Assets/Play Card.png'))
next_stage_button = Button(600, 520, 100, 40, pygame.image.load('Assets/Next Stage.png'))
sacrifice_card_button = Button(600, 300, 100, 40, pygame.image.load('Assets/Burn Card.png'))

while running:
    # 60 fps
    CLOCK.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Display
    WIN.fill(BLACK)
    if not start:
        display_text(WIN, 400, 200, "An Exorcist's Journey", WHITE, 'Fonts/HEAVYWEI.TTF', 80)
        if start_button.blit(WIN):
            start = True

    if start:
        if demon_health > 0 and player_health > 0:
            # Draw Cards
            if player_turn_stage == 1:
                for card in cards_in_player_hand:
                    if card.card_type == -1:
                        chance = randint(0, 5)
                        if chance <= 5:
                            card.card_type = 0
                            card.sprite = pygame.image.load('Assets/gospel1.png')
                            card.health = card_types[card.card_type][0]
                            card.damage = card_types[card.card_type][1]
                            card.cost = card_types[card.card_type][2]

                        if chance <= 3:
                            card.card_type = 1
                            card.sprite = pygame.image.load('Assets/symbol1.png')
                            card.health = card_types[card.card_type][0]
                            card.damage = card_types[card.card_type][1]
                            card.cost = card_types[card.card_type][2]

                        if chance <= 1:
                            card.card_type = 2
                            card.sprite = pygame.image.load(f'Assets/prayer{randint(1, 3)}.png')
                            card.health = card_types[card.card_type][0]
                            card.damage = card_types[card.card_type][1]
                            card.cost = card_types[card.card_type][2]

                        if chance == 0:
                            card.card_type = 3
                            card.sprite = pygame.image.load('Assets/ritual1.png')
                            card.health = card_types[card.card_type][0]
                            card.damage = card_types[card.card_type][1]
                            card.cost = card_types[card.card_type][2]

                demon_turn = 1
                player_turn_stage += 1

            if demon_turn_stage == 1 and demon_turn == 1:
                for card in cards_in_demon_hand:
                    if card.card_type == -1:
                        card.sprite = pygame.image.load('Assets/Demon_Card.png')
                        chance = randint(0, 5)
                        if chance <= 5:
                            card.card_type = 0
                            card.health = card_types[card.card_type][0]
                            card.damage = card_types[card.card_type][1]
                            card.cost = card_types[card.card_type][2]

                        if chance <= 3:
                            card.card_type = 1
                            card.health = card_types[card.card_type][0]
                            card.damage = card_types[card.card_type][1]
                            card.cost = card_types[card.card_type][2]

                        if chance <= 1:
                            card.card_type = 2
                            card.health = card_types[card.card_type][0]
                            card.damage = card_types[card.card_type][1]
                            card.cost = card_types[card.card_type][2]

                        if chance == 0:
                            card.card_type = 3
                            card.health = card_types[card.card_type][0]
                            card.damage = card_types[card.card_type][1]
                            card.cost = card_types[card.card_type][2]

                demon_turn = -1
                demon_turn_stage += 1

            if player_turn_stage == 2:
                # Cards on Table
                for card_index, card in enumerate(cards_on_player_table):
                    # Selects Card
                    if card.is_selected():
                        card.selected *= -1
                        card.clicked = 10
                        if card.selected == 1:
                            for other_card_index, other_card in enumerate(cards_on_player_table):
                                if other_card_index != card_index:
                                    other_card.selected = -1

                # Cards in Hand
                for card_index, card in enumerate(cards_in_player_hand):
                    # Selects Card
                    if card.is_selected() and card.card_type >= 0:
                        card.selected *= -1
                        card.clicked = 10
                        if card.selected == 1:
                            card.y -= card.sizeY / 2
                            for other_card_index, other_card in enumerate(cards_in_player_hand):
                                if other_card_index != card_index:
                                    if other_card.selected == 1:
                                        other_card.y += card.sizeY / 2
                                    other_card.selected = -1

                        if card.selected == -1:
                            card.y += card.sizeY / 2

                # Places card in hand with card on table
                for in_hand_card in cards_in_player_hand:
                    for card_on_table in cards_on_player_table:
                        if in_hand_card.selected == 1:
                            if player_stamina < 100:
                                if sacrifice_card_button.blit(WIN):
                                    player_stamina += in_hand_card.cost
                                    in_hand_card.selected = -1
                                    in_hand_card.y += in_hand_card.sizeY / 2
                                    in_hand_card.card_type = -1
                                    in_hand_card.health = 0
                                    in_hand_card.damage = 0
                                    in_hand_card.cost = 0

                                    if player_stamina > 100:
                                        player_stamina = 100

                            if card_on_table.selected == 1:
                                if play_card_button.blit(WIN):
                                    if player_stamina >= in_hand_card.cost:
                                        card_on_table.selected = -1
                                        card_on_table.sprite = in_hand_card.sprite
                                        card_on_table.card_type = in_hand_card.card_type
                                        card_on_table.health = card_types[card_on_table.card_type][0]
                                        card_on_table.damage = card_types[card_on_table.card_type][1]
                                        card_on_table.cost = card_types[card_on_table.card_type][2]

                                        in_hand_card.selected = -1
                                        in_hand_card.y += in_hand_card.sizeY / 2
                                        in_hand_card.card_type = -1
                                        in_hand_card.health = 0
                                        in_hand_card.damage = 0
                                        in_hand_card.cost = 0

                                        player_stamina -= card_on_table.cost

                if next_stage_button.blit(WIN):
                    # Unselected Cards from Previous Stage
                    for card in cards_in_player_hand:
                        if card.selected == 1:
                            card.y += card.sizeY / 2
                        card.selected = -1

                    for card in cards_on_player_table:
                        card.selected = -1

                    demon_turn = 1
                    player_turn_stage += 1

            if demon_turn_stage == 2 and demon_turn == 1:
                counter = 0
                if len(get_card_costs(cards_in_demon_hand)) > 0:
                    for card in get_card_costs(cards_in_demon_hand):
                        card_cost, in_hand_card_index = card

                        # Counter = how many cards to play per turn - 1
                        if counter <= 1:
                            # Plays Cards from Hand to Empty Slots on Table
                            if len(get_empty_card_slots(cards_on_demon_table)) > 0:
                                counter += 1
                                for table_card_index in get_empty_card_slots(cards_on_demon_table):
                                    if cards_in_demon_hand[in_hand_card_index].card_type >= 0:
                                        if demon_stamina > cards_in_demon_hand[in_hand_card_index].cost:
                                            if demon_stamina > 40 or cards_in_demon_hand[in_hand_card_index].cost == 0:
                                                cards_on_demon_table[table_card_index].sprite = cards_in_demon_hand[
                                                    in_hand_card_index].sprite
                                                cards_on_demon_table[table_card_index].card_type = cards_in_demon_hand[
                                                    in_hand_card_index].card_type

                                                cards_on_demon_table[table_card_index].health = \
                                                    card_types[cards_on_demon_table[table_card_index].card_type][0]
                                                cards_on_demon_table[table_card_index].damage = \
                                                    card_types[cards_on_demon_table[table_card_index].card_type][1]
                                                cards_on_demon_table[table_card_index].cost = \
                                                    card_types[cards_on_demon_table[table_card_index].card_type][2]

                                                cards_in_demon_hand[in_hand_card_index].card_type = -1
                                                cards_in_demon_hand[in_hand_card_index].health = 0
                                                cards_in_demon_hand[in_hand_card_index].damage = 0
                                                cards_in_demon_hand[in_hand_card_index].cost = 0

                                                demon_stamina -= cards_on_demon_table[table_card_index].cost

                            else:
                                # Replaces "Weak" Cards on Table with new ones
                                for second_card_damage_index in get_damage(cards_in_demon_hand):
                                    card_damage, card_in_demon_hand_index = second_card_damage_index

                                    if demon_stamina > 60:
                                        for card_on_demon_table in cards_on_demon_table:
                                            if card_damage > card_on_demon_table.damage and cards_in_demon_hand[card_in_demon_hand_index].cost <= demon_stamina:
                                                card_on_demon_table.sprite = cards_in_demon_hand[
                                                    card_in_demon_hand_index].sprite
                                                card_on_demon_table.card_type = cards_in_demon_hand[
                                                    card_in_demon_hand_index].card_type

                                                card_on_demon_table.health = \
                                                    card_types[card_on_demon_table.card_type][0]
                                                card_on_demon_table.damage = \
                                                    card_types[card_on_demon_table.card_type][1]
                                                card_on_demon_table.cost = \
                                                    card_types[card_on_demon_table.card_type][2]

                                                cards_in_demon_hand[card_in_demon_hand_index].card_type = -1
                                                cards_in_demon_hand[card_in_demon_hand_index].health = 0
                                                cards_in_demon_hand[card_in_demon_hand_index].damage = 0
                                                cards_in_demon_hand[card_in_demon_hand_index].cost = 0

                                                demon_stamina -= card_on_demon_table.cost

                        # Sacrifice Cards if "Low" on Stamina
                        for second_card_cost_index in get_card_costs(cards_in_demon_hand):
                            card_cost, card_index = second_card_cost_index
                            if demon_stamina <= 40:
                                if card_cost > 0:
                                    demon_stamina += card_cost
                                    cards_in_demon_hand[card_index].card_type = -1
                                    cards_in_demon_hand[card_index].health = 0
                                    cards_in_demon_hand[card_index].damage = 0
                                    cards_in_demon_hand[card_index].cost = 0

                                    if demon_stamina > 100:
                                        demon_stamina = 100

                demon_turn = -1
                demon_turn_stage += 1

            if player_turn_stage == 3:
                # Cards on Table
                for card_index, card in enumerate(cards_on_player_table):
                    # Selects Card
                    if card.is_selected():
                        if card.card_type >= 0 and card.card_type != 0:
                            card.selected *= -1
                            card.clicked = 10
                            if card.selected == 1:
                                for other_card_index, other_card in enumerate(cards_on_player_table):
                                    if other_card_index != card_index:
                                        other_card.selected = -1

                # Cards on Table
                for card_index, card in enumerate(cards_on_demon_table):
                    # Selects Card
                    if card.is_selected():
                        if card.card_type >= 0:
                            card.selected *= -1
                            card.clicked = 10
                            if card.selected == 1:
                                for other_card_index, other_card in enumerate(cards_on_demon_table):
                                    if other_card_index != card_index:
                                        other_card.selected = -1

                for card_on_table in cards_on_player_table:
                    for card_on_demon_table in cards_on_demon_table:
                        if card_on_table.selected == 1:
                            # If Demon has no Cards
                            counter = 0
                            for other_card_on_demon_table in cards_on_demon_table:
                                if other_card_on_demon_table.card_type >= 0:
                                    counter += 1

                            if counter == 0:
                                if player_stamina >= card_on_table.cost:
                                    if play_card_button.blit(WIN):
                                        demon_health -= card_on_table.damage * 5
                                        player_stamina -= card_on_table.cost
                                        card_on_table.health -= 1
                                        card_on_table.selected = -1

                            # If Demon has Cards
                            if card_on_demon_table.selected == 1:
                                if player_stamina >= card_on_table.cost:
                                    if play_card_button.blit(WIN):
                                        if player_stamina >= card_on_table.cost:
                                            card_on_table.selected = -1
                                            card_on_demon_table.selected = -1

                                            card_on_table.health -= 1

                                            card_on_demon_table.health -= card_on_table.damage
                                            player_stamina -= card_on_table.cost

                if next_stage_button.blit(WIN):
                    # Unselected Cards from Previous Stage
                    for card in cards_on_demon_table:
                        card.selected = -1

                    for card in cards_on_player_table:
                        card.selected = -1

                    demon_turn = 1
                    player_turn_stage += 1

            if demon_turn_stage == 3 and demon_turn == 1:
                for card in get_cost_and_damage(cards_on_demon_table):
                    if cards_on_demon_table[card[2]].card_type >= 1:
                        demon_card_cost, demon_card_damage, demon_card_index = card
                        counter = 0
                        for second_card in cards_on_player_table: # Checks for cards on player table
                            if second_card.card_type >= 0:
                                counter += 1

                        if counter == 0:  # If Player has no cards played
                            if demon_card_cost <= demon_stamina:
                                player_health -= cards_on_demon_table[demon_card_index].damage * 5
                                demon_stamina -= cards_on_demon_table[demon_card_index].cost
                                cards_on_demon_table[demon_card_index].health -= 1

                        else:
                            if cards_on_demon_table[demon_card_index].cost <= demon_stamina:
                                PlayerCard_to_attack_index = get_card_health(cards_on_player_table)[0][1]
                                cards_on_demon_table[demon_card_index].health -= 1

                                cards_on_player_table[PlayerCard_to_attack_index].health -= cards_on_demon_table[
                                    demon_card_index].damage

                                demon_stamina -= cards_on_demon_table[demon_card_index].cost

                demon_turn = -1

            if player_turn_stage == 4:
                for card_index, card in enumerate(cards_on_player_table):
                    # Selects Card
                    if card.is_selected() and not card.used:
                        if card.card_type == 0:
                            card.selected *= -1
                            card.clicked = 10
                            if card.selected == 1:
                                for other_card_index, other_card in enumerate(cards_on_player_table):
                                    if other_card_index != card_index:
                                        other_card.selected = -1

                for card_on_table in cards_on_player_table:
                    if card_on_table.selected == 1:
                        if not card_on_table.used and player_stamina < 100:
                            if play_card_button.blit(WIN):
                                card_on_table.used = True
                                card_on_table.selected = -1
                                card_on_table.health -= 1
                                player_stamina += 15
                                if player_stamina > 100:
                                    player_stamina = 100

                if next_stage_button.blit(WIN):
                    # Unselected Cards from Previous Stage
                    for card in cards_on_demon_table:
                        card.selected = -1

                    for card in cards_on_player_table:
                        card.used = False
                        card.selected = -1

                    demon_turn = 1
                    demon_turn_stage += 1
                    player_turn_stage += 1

            if demon_turn_stage == 4 and demon_turn == 1:
                if demon_stamina < 100:
                    for card in cards_on_demon_table:
                        if card.card_type == 0:
                            card.health -= 1
                            demon_stamina += 10

                if demon_stamina > 100:
                    demon_stamina = 100

            if player_turn_stage == 5:
                player_turn_stage = 1
                demon_turn_stage = 1

            # Blit Demon Cards
            for card in cards_on_demon_table:
                if card.health <= 0:
                    card.card_type = -1
                    card.health = 0
                    card.damage = 0
                    card.cost = 0
                    card.sprite = pygame.image.load('Assets/blank_demon_card.png')

                if card.selected == 1:
                    pygame.draw.rect(WIN, (255, 255, 0), (card.x, card.y, card.sizeX, card.sizeY))

                card.blit(WIN)

                if card.card_type >= 0:
                    display_text(WIN, card.x + 25, card.y + card.sizeY - 15, str(card.health), WHITE,
                                 'Fonts/ChopinScript.ttf', 15)
                    display_text(WIN, card.x + 55, card.y + card.sizeY - 15, str(card.damage), WHITE,
                                 'Fonts/ChopinScript.ttf',  15)
                    display_text(WIN, card.x + 25, card.y + 12, str(card.cost), WHITE,
                                 'Fonts/ChopinScript.ttf', 15)

            # Blit PlayerCards
            for card in cards_on_player_table:
                if card.health <= 0:
                    card.sprite = pygame.image.load('Assets/Blank Card.png')
                    card.card_type = -1

                if player_turn_stage == 4:
                    if card.card_type == 0 and not card.used:
                        pygame.draw.rect(WIN, (0, 0, 255), (card.x, card.y, card.sizeX, card.sizeY))

                if player_turn_stage == 3:
                    if card.card_type >= 1:
                        pygame.draw.rect(WIN, RED, (card.x, card.y, card.sizeX, card.sizeY))

                if card.selected == 1:
                    pygame.draw.rect(WIN, (255, 255, 0), (card.x, card.y, card.sizeX, card.sizeY))

                card.blit(WIN)

                if card.card_type >= 0:
                    display_text(WIN, card.x + 25, card.y + card.sizeY - 15, str(card.health), WHITE,
                                 'Fonts/ChopinScript.ttf', 15)
                    display_text(WIN, card.x + 55, card.y + card.sizeY - 15, str(card.damage), WHITE,
                                 'Fonts/ChopinScript.ttf', 15)
                    display_text(WIN, card.x + 25, card.y + 12, str(card.cost), WHITE,
                                 'Fonts/ChopinScript.ttf', 15)

            for card in cards_in_player_hand:
                if card.card_type >= 0:
                    card.blit(WIN)
                    display_text(WIN, card.x + 25, card.y + card.sizeY - 15, str(card.health), WHITE,
                                 'Fonts/ChopinScript.ttf', 15)
                    display_text(WIN, card.x + 55, card.y + card.sizeY - 15, str(card.damage), WHITE,
                                 'Fonts/ChopinScript.ttf', 15)
                    display_text(WIN, card.x + 25, card.y + 12, str(card.cost), WHITE,
                                 'Fonts/ChopinScript.ttf', 15)

            # Blit Demon Stats
            pygame.draw.rect(WIN, WHITE, (545, 10, 250, 40))
            pygame.draw.rect(WIN, RED, (545, 10, demon_health * 2.5, 40))
            display_text(WIN, 670, 30, str(demon_health), BLACK, 'Fonts/ChopinScript.ttf', 35)

            # Blit Player Stats
            pygame.draw.rect(WIN, RED, (10, 10, 250, 40))
            pygame.draw.rect(WIN, WHITE, (10, 10, player_health * 2.5, 40))
            display_text(WIN, 125, 30, str(player_health), BLACK, 'Fonts/ChopinScript.ttf', 35)

            pygame.draw.rect(WIN, RED, (10, 60, 250, 40))
            pygame.draw.rect(WIN, (0, 0, 255), (10, 60, player_stamina * 2.5, 40))
            display_text(WIN, 125, 80, str(player_stamina), WHITE, 'Fonts/ChopinScript.ttf', 35)

            # Blit Player Stage
            display_text(WIN, 400, 20, f"Stage {player_turn_stage}", WHITE, 'Fonts/HEAVYWEI.TTF', 20)

        elif demon_health <= 0:
            display_text(WIN, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, "YOU WIN!", WHITE, 'Fonts/HEAVYWEI.TTF', 100)

        elif player_health <= 0:
            display_text(WIN, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, "YOU LOSE!", RED, 'Fonts/HEAVYWEI.TTF', 100)

    pygame.display.update()