from random import choices, shuffle

suits = ("Hearts", "Diamonds", "Spades", "Clubs")
ranks = ("Two", "Three", "Four", "Five", "Six", "Seven", "Eight",
         "Nine", "Ten", "Jack", "Queen", "King", "Ace",)
values = {"Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven": 7, "Eight": 8,
          "Nine": 9, "Ten": 10, "Jack": 10, "Queen": 10, "King": 10, "Ace": 11}

# Global boolean
PLAYING = True


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:
    """ Creates a Deck of cards and
    Deals cards to both the player and the dealer (computer). """

    def __init__(self):
        self.deck = []
        self.player = []
        self.dealer = []
        # Adds the suits and their respective ranks to the deck
        for suit in suits:
            for rank in ranks:
                self.deck.append((suit, rank))

    def shuffle(self):
        # Uses shuffle from the random library to mix the deck
        shuffle(self.deck)

    def deal_cards(self):
        # Uses choices from the random library to pick two cards out for the player and the dealer
        self.player = choices(self.deck, k=2)
        self.remove(self.player)
        self.dealer = choices(self.deck, k=2)
        self.remove(self.dealer)
        return self.player, self.dealer

    def remove(self, drawn):
        # Removes card from the deck
        try:
            for i in drawn:
                self.deck.remove(i)
        except ValueError:
            pass


class Hand:
    """ Adding the values of player/dealer cards
    and change the values of Aces acc. to situation. """

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_cards(self, card):
        self.cards.extend(card)
        for count, ele in enumerate(card, 0):
            if ele[1] == "Ace":
                self.aces += 1
            self.value += values[ele[1]]
        self.ace()

    def ace(self):
        while self.aces > 0 and self.value > 21:
            self.value -= 10
            self.aces -= 1


class Money:
    """ Manages player gambling by keeping track of balance """

    def __init__(self):
        self.total = 250
        self.bet = 0

    def win(self):
        self.total += self.bet

    def loss(self):
        self.total -= self.bet


def take_bet(bet_amount, player_money):
    while bet_amount > player_money or bet_amount <= 49:
        print("\n INVALID BET AMOUNT!")
        bet_amount = int(input(" Enter bet again: (There is a minimum bet requirement of 50) "))
    return bet_amount


def hits(obj_de):
    new_card = [obj_de.deal_cards()[0][0]]
    # obj_h.add_cards(new_card)
    return new_card


def decisions(bal, d, hand, dealer):
    global PLAYING
    next_card = hits(d)
    choice = str(input(f"Your Choices: \n[H]IT | [S]TAND | [D]OUBLE DOWN - ")).lower()
    print("\n")
    if choice == "h":
        hand.add_cards(next_card)
        show_some(hand.cards, dealer, hand)

    elif choice == "s":
        PLAYING = False

    elif choice == "d":
        doubled = bal.bet * 2
        if doubled <= bal.total:
            bal.bet = doubled
            dealer_card = hits(d)
            hand.add_cards(dealer_card)
            PLAYING = False
        else:
            print("Unable to Double Down -- ERROR: Insufficient Balance\n")
    else:
        print("Invalid Choice")


def show_some(player_cards, dealer_cards, obj_h):
    print(f" -----\n Your Cards [{obj_h.value}] : {player_cards}")
    print(
        f" Dealer's Cards [{values[dealer_cards[1][1]]}] : {[dealer_cards[1]]} \n -----\n"
    )


def show_all(player_cards, dealer_cards, obj_h, obj_d):
    print(f" ------\n Your Cards [{obj_h.value}] : {player_cards}")
    print(f" Dealer's Cards [{obj_d.value}] : {dealer_cards} \n ------\n")


def player_bust(obj_h, obj_c):
    if obj_h.value > 21:
        obj_c.loss()
        return True
    return False


def player_wins(obj_h, obj_d, obj_c):
    if any((obj_h.value == 21, obj_h.value > obj_d.value and obj_h.value < 21)):
        obj_c.win()
        return True
    return False


def dealer_bust(obj_d, obj_h, obj_c):
    if obj_d.value > 21:
        if obj_h.value < 21:
            obj_c.win()
        return True
    return False


def dealer_wins(obj_h, obj_d, obj_c):
    if any((obj_d.value == 21, obj_d.value > obj_h.value and obj_d.value < 21)):
        obj_c.loss()
        return True
    return False


def push(obj_h, obj_d):
    if obj_h.value == obj_d.value:
        return True
    return False


def intro_screen():
    print("\nWelcome to BlackJack! The rules of the game are simple.")
    print("Try to beat the dealer by getting a card total close to '21' as possible without going over!")
    print("Good luck!")


def game():
    intro_screen()
    balance = Money()
    while True:
        deck = Deck()
        deck.shuffle()
        p_cards, d_cards = deck.deal_cards()
        hand = Hand()
        hand.add_cards(p_cards)
        print("\n Current Balance:", balance.total)
        bets = int(input(" Enter Bet amount : "))
        balance.bet = take_bet(bets, balance.total)
        print("\n")

        show_some(p_cards, d_cards, hand)
        global PLAYING
        while PLAYING:  # Recall var. from hit and stand function
            decisions(balance, deck, hand, d_cards)
            if player_bust(hand, balance):
                print("\n You have gone over 21! Bust!")
                break

        PLAYING = True

        if hand.value <= 21:
            dealer = Hand()
            dealer.add_cards(d_cards)
            while dealer.value < 17:
                d_card = hits(deck)
                dealer.add_cards(d_card)
                if dealer_bust(dealer, hand, balance):
                    print("\n The dealer has gone over 21! Bust!\n")
                    break
            show_all(hand.cards, dealer.cards, hand, dealer)

            if push(hand, dealer):
                print("Its a tie!")
                print("Your balance has been redeposited")
            elif player_wins(hand, dealer, balance):
                print("You Won", balance.bet, "credits!")
            elif dealer_wins(hand, dealer, balance):
                print("The dealer has won :(. You lost", balance.bet, "credits.")

        else:
            print("\nThe dealer has won :(. You lost", balance.bet, "credits.")

        print(f"\nAvailable Balance = {balance.total} \n")

        if balance.total < 1:
            print("You are out of money...")
            print("You were promptly kicked out of the casino.")
            break

        ans = str(input("Play again(Y/N) : ")).lower()
        if ans != "y":
            print("Thank you for playing blackjack!")
            break


game()
