from random import shuffle                              #z knižnice random importneme shuffle
import os                                               # importujem knižnicu os
###############################

player_name = input("Vitaj v kasíne! Ako sa voláš? ")   # spýtam sa na hráčove meno

#############################################################################################################################

class Dealer(object):                                   # klása Dealer 
    
    def __init__(self):                                 # konštruktor klásy Dealer

        self.name = "Dealer"                            # názov hráča je "Dealer"
        self.score = 0                                  # skore hráča je 0
        self.hand = []                                  # Dealer bude mať prázdnu ruku


class Player(Dealer):                                   # klása Player ktorá dedí z klásy Dealer

    def __init__(self, name):                           # konštruktor klásy Player
        super().__init__()                              # voláme konštruktor klásy Dealer
        self.name = name                                # názov hráča je v premenne name

    def hit_or_stick():                                 # funkcia hit_or_stick ktorá vráti True alebo False podľa toho či chce hráč dalšiu kartu alebo nie
        while True: 
            choice = input("Chceš dalšiu kartu? (A/N)? ")
            if choice.lower().startswith('a'):
                return True
            elif choice.lower().startswith('n'):
                return False
            else:                                       #ak zadáme niečo iné než A alebo N, tak sa opakuje
                print("Nechápe?!")
                continue


class Deck(object):                                     # klása Deck
    
    def __init__(self):                                 # konštruktor klásy Deck


        self.stack = [('|♠ A|', 1), ('|♠ 2|', 2), ('|♠ 3|', 3), ('|♠ 4|', 4), ('|♠ 5|', 5),      # zoznam kariet a ich symbolom
                      ('|♠ 6|', 6), ('|♠ 7|', 7), ('|♠ 8|', 8), ('|♠ 9|', 9), ('|♠ 10|', 10),
                      ('|♠ J|', 10), ('|♠ Q|', 10), ('|♠ K|', 10),('|♣ A|', 1), ('|♣ 2|', 2), ('|♣ 3|', 3), ('|♣ 4|', 4), ('|♣ 5|', 5),
                      ('|♣ 6|', 6), ('|♣ 7|', 7), ('|♣ 8|', 8), ('|♣ 9|', 9), ('|♣ 10|', 10),
                      ('|♣ J|', 10), ('|♣ Q|', 10), ('|♣ K|', 10),('|♥ A|', 1), ('|♥ 2|', 2), ('|♥ 3|', 3), ('|♥ 4|', 4), ('|♥ 5|', 5),
                      ('|♥ 6|', 6), ('|♥ 7|', 7), ('|♥ 8|', 8), ('|♥ 9|', 9), ('|♥ 10|', 10),
                      ('|♥ J|', 10), ('|♥ Q|', 10), ('|♥ K|', 10),('|♦ A|', 1), ('|♦ 2|', 2), ('|♦ 3|', 3), ('|♦ 4|', 4), ('|♦ 5|', 5),
                      ('|♦ 6|', 6), ('|♦ 7|', 7), ('|♦ 8|', 8), ('|♦ 9|', 9), ('|♦ 10|', 10),
                      ('|♦ J|', 10), ('|♦ Q|', 10), ('|♦ K|', 10)]
        
        self.shuffle()                                  # zamiešame karty

    def shuffle(self):                                  # funkcia na miešanie kariet

        shuffle(self.stack)                             # miešanie kariet

    def deal_card(self):                                # funkcia na dealnutie karty hráčovi / dealerovi

        card = self.stack.pop()                         # dealnutie karty z stacku, následne sa zo stacku zmaže
        return card



#####################################################################################################

class Table(object):                                    # klása Table v ktorej sa stretávajú vetky ďalšie funkcie
 
    def __init__(self, player):                         # konštruktor klásy Table

        self.dealer = Dealer()                          # klása Table bude mať hodnoty dealer, player, deck
        self.player = Player(player)
        self.deck = Deck()

        self.table_setup()                              # zavoláme metódu table_setup()

    def table_setup(self):

        self.deck.shuffle()                             # karty sa pred hraním zamiešajú

        self.deal_card(self.player)                     # nájskôr dostane kartu hráč, potom dealer, potom hráč
        self.deal_card(self.dealer)
        self.deal_card(self.player)
        self.calculate_score(self.player)               # calculate the player and dealer score at start to check for blackjack
        self.calculate_score(self.dealer)

        self.main()                                     # povoláme funkciu main()

    def main(self):                                     #fukncia main

        while True:
            print()
            print(self)
            player_move = Player.hit_or_stick()         # uložime si do premennej player_move output funkcie hit_or_stick()
            if player_move is True:                     # ak chce hráč ďalšiu kartu, hra mu dá kartu z kôpky kariet a vypočíta skóre
                self.deal_card(self.player)
                self.calculate_score(self.player)
            elif player_move is False:                  # ak hráč nechce ďalšiu kartu, konči jeho kolo a karty dostáva dealer
                self.dealer_hit()

    def dealer_hit(self):                               # funkcia pre dealera ktorý hraje kým nie je skóre 17 alebo viac

        score = self.dealer.score                       # uložíme skóre dealera do premenej score
        while True:
            if score < 17:                              # ak je skóre dealera menej ako 17, dealer dostane kartu a pripočíta sa mu skóre
                self.deal_card(self.dealer)
                self.calculate_score(self.dealer)
                print(self)
            elif score >= 17:                           # ak je skóre dealera 17 alebo viac, dealer končí kolo
                self.check_final_score()

    def __str__(self):                                  # funkcia __str__ vráti string pre výpis hry

        dealer_hand = [card for card, value in self.dealer.hand]    # premenná dealer_hand bude obsahovať karty dealera a ich hodnoty
        player_hand = [card for card, value in self.player.hand]    # premenná player_hand bude obsahovať karty hráča a ich hodnoty

        print("-" * 40)
        print("Ruka dealera : {}".format(dealer_hand))              # vypíše karty dealera
        print("Skóre dealera : {}".format(self.dealer.score))       # vypíše skóre dealera
        print()
        print("Ruka hráča {} : {}".format(self.player.name, player_hand))               # vypíše karty hráča
        print("Skóre hráča {} : {}".format(self.player.name, self.player.score))        # vypíše skóre hráča
        print("-" * 40)
        return ''

    def deal_card(self, player):                        # funkcia dávania karty

        card = self.deck.stack.pop()                    # do premennej card dáme kartu z kôpky kariet ktorá za z kôpky vezme (popne)
        player.hand.append(card)                        # hráčová ruka kartu dostane

    def calculate_score(self, player):                  # funkcia na vypočítanie skóre

        ace = False                                     # cesta na zistenie či má hráč eso
        score = 0                                       # skóre začne na 0
        for card in player.hand:                        # pre každú kartu v ruke hráča
            if card[1] == 1 and not ace: 
                ace = True
                card = ('A', 11)
            score += card[1]
        player.score = score                            # hráčove skóre sa updatne
        if player.score > 21 and ace:                   # ak má hráč viac ako 21 a má v ruke eso, jeho skóre sa zníži o 10
            player.score -= 10
            score = player.score                        # hráčove skóre sa updatne
        self.check_win(score, player)                   # skontroluje či hráč vyhral
        return

    def check_win(self, score, player):                 # fukncia na zistenie výhry
        if score > 21:                                  # ak má hráč skóre viac ako 21
            print()
            print(self)
            print("{} prestrelil 21".format(player.name))       # hráč prehral
            print()
            self.end_game()                             # hra skonči
        elif score == 21:                               # ak má hráč skóre 21
            print(self)
            print("{} dostal B L A C K J A C K !".format(player.name))      # hráč vyhrá BlACKJACK
            self.end_game()
        else:
            return

    def check_final_score(self):                        # funkcia na zistenie finalneho skóre

        dealer_score = self.dealer.score                # dealerove skore dame do premennej dealer_score
        player_score = self.player.score                # hráčove skore dame do premennej player_score

        
        if dealer_score > player_score:                 # ak dealerove skore je väčšie ako hráčove skore
            print("Dealer vyhral!")                     # vyhra dealer
            self.end_game()
            
        else:                                               # ak hráčove skore je väčšie ako dealerove skore
            print("{} vyhral!".format(self.player.name))    # vyhra hráč
            self.end_game()                                 #hra skonči

    def end_game(self):                                 # funkcia na koniec hry
        
            again = input("Chceš hrať znovu? (A/N)? ")  # ak chceme hrať znovu, do inputu dáme A, inak N
            if again.lower().startswith('a'):
                self.__init__(self.player.name)
                
            elif again.lower().startswith('n'):
                print("Ešte sa vráť!")
                exit()  

#############################
def main():                                             # main hra
    Table(player_name)                                  # vytvorím hru a zavolám funkciu na vytvorenie hry

if __name__ == '__main__': 

    main()