import random


# Class for a BlackJackTable
class BlackJackTable:

    def __init__(self):
        # Create all available cards
        self.cards = ["ACE", "2", "3", "4", "5", "6", "7", "8", "9", "10", "JACK", "QUEEN", "KING"]

        # Randomly draw two cards for the player
        self.ownCards = [
            [self.cards[random.randint(0, len(self.cards) - 1)], self.cards[random.randint(0, len(self.cards) - 1)]]]

        # Randomly draw one card for the dealer
        self.dealerCards = [self.cards[random.randint(0, len(self.cards) - 1)]]

        # Set an internal variable for determining if the game is finished to False
        self.game_finished = False

    def reset_table(self):

        # Randomly draw two cards for the player
        self.ownCards = [
            [self.cards[random.randint(0, len(self.cards) - 1)], self.cards[random.randint(0, len(self.cards) - 1)]]]

        # Randomly draw one card for the dealer
        self.dealerCards = [self.cards[random.randint(0, len(self.cards) - 1)]]

        # Set an internal variable for determining if the game is finished to False
        self.game_finished = False

    def is_finished(self):
        # Returns if the game is finished
        return self.game_finished

    def __is_blackjack(self, cards):
        # Returns if the given cards are a BlackJack
        return self.get_final_value_of_deck(cards) == 21

    def get_final_value_of_deck(self, hand):
        # Returns the maximum value for a deck without exceeding 21 if possible

        # First calculate all ACEs as 1
        base = self.get_deck_value(hand, high=False)
        number_of_aces = sum([card == "ACE" for card in hand])

        # If possible without exceeding 21, turn one ACE from valued at 1 to valued at 2
        while number_of_aces > 0 and base < 12:
            base += 10
            number_of_aces -= 1
        return base

    def get_return(self):
        # Calculates the return of the game as percentage

        # First you loose for each hand you play the complete stake
        base = -len(self.ownCards)

        # Now calculate for each hand, if the player got back the complete stake plus return, only the stake or lost it
        for hand in self.ownCards.copy():

            # If the player has played a Double Down, increase inital lose
            dd = hand[-2] == "DD"
            if dd:
                base -= 1
            if self.__is_blackjack(self.dealerCards) and self.__is_blackjack(hand):
                # If dealer and player have BlackJack
                base += 2 if dd else 1
            elif self.__is_blackjack(hand) and not self.__is_blackjack(self.dealerCards):
                # If only player has BlackJack
                base += 4 if dd else 2
            elif self.__is_blackjack(self.dealerCards) and not self.__is_blackjack(hand):
                # If only dealer has BlackJack
                continue
            elif self.get_final_value_of_deck(hand) > 21:
                # If player is above 21
                continue
            elif self.get_final_value_of_deck(self.dealerCards) > 21:
                # If dealer is over 21 and player still alive
                base += 4 if dd else 2
            elif self.get_final_value_of_deck(self.dealerCards) == self.get_final_value_of_deck(hand):
                # If the dealer and player have the same value
                base += 2 if dd else 1
            elif self.get_final_value_of_deck(self.dealerCards) > self.get_final_value_of_deck(hand):
                # If the dealer has a greater value than the player
                continue
            elif self.get_final_value_of_deck(self.dealerCards) < self.get_final_value_of_deck(hand):
                # If the player has a smaller value than the player
                base += 4 if dd else 2
        return base

    def get_deck_value(self, cards, high=True):
        # Get the value of the deck, with either seeing ACEs as 1 or 11 (parameter high)
        return sum([self.__get_value(card, high) for card in cards])

    def __get_value(self, card, high=True):
        # Return the value of a single card, with either seeing ACES as 1 or 11 (parameter high)
        values_of_cards = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "JACK": 10,
                           "QUEEN": 10, "KING": 10, "ACE": 11 if high else 1, "TERMINATED": 0, "DD": 0}
        return values_of_cards[card]

    def get_game_state(self):
        # Return the current game state
        result = {
            "dealer": self.dealerCards,
            "player": self.ownCards
        }
        return result

    def do_action(self, actions):
        # Applies users action to the game

        # Check that for each hand an action is provided
        if len(actions) != len(self.ownCards):
            raise Exception("You have to submit an action for each hand you play")

        # Go through each hand and apply the action
        for index, action in enumerate(actions):
            # Skip hand that are already terminated
            if self.ownCards[index][-1] == "TERMINATED":
                continue

            # If the action is STAND, terminate the hand
            elif action == "STAND":
                self.ownCards[index].append("TERMINATED")

            # If the action is HIT, draw one more card and check if it exceeds 21
            elif action == "HIT":
                self.ownCards[index].append(self.cards[random.randint(0, len(self.cards) - 1)])
                sum_of_cards = sum([self.__get_value(card) for card in self.ownCards[index]])
                if sum_of_cards >= 21:
                    self.ownCards[index].append("TERMINATED")

            # If the action is DOUBLEDOWN, draw 1 card and terminate the hand
            elif action == "DOUBLEDOWN":
                self.ownCards[index].append(self.cards[random.randint(0, len(self.cards) - 1)])
                self.ownCards[index].append("DD")
                self.ownCards[index].append("TERMINATED")

            # If the action is SPLIT, split the current hand into two
            elif action == "SPLIT":
                if len(self.ownCards[index]) != 2:
                    raise "You can only split if you have 2 cards"
                if self.__get_value(self.ownCards[index][0]) != self.__get_value(self.ownCards[index][1]):
                    raise "You can only split if the value of both cards is the same"

                self.ownCards.append([self.ownCards[index].pop()])

        # Check if the game is finished (all hands are terminated
        self.game_finished = sum([hand[-1] != "TERMINATED" for hand in self.ownCards]) == 0
        if self.game_finished:

            # Apply the dealers steps
            dealer_is_finished = False
            while not dealer_is_finished:
                # Draw one card for the dealer
                self.dealerCards.append(self.cards[random.randint(0, len(self.cards) - 1)])

                # If the dealer has a BlackJack, stop
                if self.__is_blackjack(self.dealerCards):
                    dealer_is_finished = True

                # If the value with ACEs being seen as 11 is between 17 and 21, stop
                elif 17 <= self.get_deck_value(self.dealerCards, high=True) <= 21:
                    dealer_is_finished = True

                # If the value with ACEs being seen as 11 is below 17, continue to draw another card
                elif self.get_deck_value(self.dealerCards, high=True) < 17:
                    continue

                # If the value with ACEs being seen as 1 is between 17 and 21, stop
                elif 17 <= self.get_deck_value(self.dealerCards, high=False) <= 21:
                    dealer_is_finished = True

                # If the value with ACEs being seen as 1 is below 17, continue to draw another card
                elif self.get_deck_value(self.dealerCards, high=False) < 17:
                    continue

                # If the value is above 21, stop
                elif self.get_deck_value(self.dealerCards, high=False) > 21:
                    dealer_is_finished = True
