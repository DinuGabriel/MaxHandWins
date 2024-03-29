# Import necessary modules
from enum import Enum
from functools import total_ordering
import random
import time

# Define an enumeration for card suits
class Suit(Enum):
    SPADES = 4
    HEARTS = 3
    DIAMONDS = 2
    CLUBS = 1

# Implement total ordering for PlayingCard class for comparisons
@total_ordering
class PlayingCard:
    def __init__(self, rank, suit):
        self._rank = rank
        self._suit = suit

    # Getter methods for rank and suit
    def _get_rank(self):
        return self._rank

    def _get_suit(self):
        return self._suit

    # Define equality and greater-than comparisons for cards
    def __eq__(self, other):
        return (self._rank == other._rank and self._suit == other._suit)

    def __gt__(self, other):
        if self._rank > other._rank:
            return True
        elif self._rank == other._rank:
            return self._suit.value > other._suit.value
        else:
            return False

    # String representation of a card
    def __str__(self):
        return f'({self._get_rank()}, {self._get_suit().name})'

# Define a Player class
class Player:
    def __init__(self, name):
        self._name = name
        self._hand = []

    # Getter methods for player's name and hand
    def get_name(self):
        return self._name

    def get_hand(self):
        return self._hand

    # Setter method for player's hand
    def _set_hand(self, hand):
        self._hand = hand

    # Find the strongest card in the player's hand
    def _strongest_card(self):
        if self._hand:
            return max(self._hand)

# Define a Deck class
class Deck:
    def __init__(self):
        self._cards = []
        # Initialize a deck with 52 playing cards
        for i in range(13):
            self._cards.append(PlayingCard(i + 2, Suit.SPADES))
            self._cards.append(PlayingCard(i + 2, Suit.HEARTS))
            self._cards.append(PlayingCard(i + 2, Suit.DIAMONDS))
            self._cards.append(PlayingCard(i + 2, Suit.CLUBS))

    # Getter method for the deck's cards
    def _get_cards(self):
        return self._cards

    # Shuffle the deck by swapping cards randomly
    def shuffle(self):
        for _ in range(200):
            i, j = random.randint(0, 51), random.randint(0, 51)
            self._cards[i], self._cards[j] = self._cards[j], self._cards[i]

    # Draw n cards from the deck
    def _draw(self, n):
        if n > len(self._cards):
            return None

        drawn = []
        for i in range(n):
            c = self._cards.pop()
            drawn.append(c)
        return drawn

# Define a Game class
class Game:
    def __init__(self, players, deck):
        self._players = players
        self._deck = deck
        self._score = {}
        # Initialize the game score for each player
        for p in players:
            self._score[p.get_name()] = 0

    # Display the current game score
    def _show_score(self):
        print("Score:")
        print("------")
        for k, v in self._score.items():
            print(f'{k}: {v}')
        print('\n')

    # Check if there are enough cards for another round
    def _is_more_rounds(self):
        return len(self._deck._get_cards()) >= 2 * len(self._players)

    # Play a round of the game
    def _play_round(self):
        winning_card = None
        winning_player = None
        for p in self._players:
            hand = self._deck._draw(2)
            p._set_hand(hand)
            print(f'player {p.get_name()} is dealt: [{hand[0]}, {hand[1]}')
            if winning_card is None or (p._strongest_card() > winning_card):
                winning_card = p._strongest_card()
                winning_player = p

        print(f'PLAYER {winning_player.get_name()} WINS THIS ROUND\n')
        self._score[winning_player.get_name()] += 1
        self._show_score()
        time.sleep(6)

    # Play the game until there are no more rounds
    def play(self):
        while self._is_more_rounds():
            self._play_round()
        winner = max(self._score, key=self._score.get)
        print(f'\n\nPlayer {winner} won the game')

# Entry point of the program
if __name__ == '__main__':
    # Create three players and a shuffled deck
    p1 = Player(input('Enter the name of the first Player: '))
    p2 = Player(input('Enter the name of the second Player: '))
    p3 = Player(input('Enter the name of the third Player: '))
    d = Deck()
    d.shuffle()
    
    # Start the game with the players and deck
    g = Game([p1, p2, p3], d)
    g.play()