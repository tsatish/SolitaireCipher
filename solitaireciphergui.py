from tkinter import *
from tkinter.scrolledtext import ScrolledText


class CipherGUI(Frame):
    """
    Renders a GUI that allows enciphering/deciphering of text using Bruce Schneier's solitaire algorithm.
    """
    
    def __init__(self, parent):
        """
        Initializes the GUI elements.
        """
        Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title("Solitaire Cipher")

        self.helpFile = open("help.dat", "r")
        self.helpText = self.helpFile.read()

        self.aboutFile = open("about.dat", "r")
        self.aboutText = self.aboutFile.read()

        self.toCipher = Text(self.parent, undo = 1)
        self.toCipher.grid(row = 1, column = 1, padx = 10, pady = 10)
        self.toCipher.insert(END, "Type text to encipher...")
        self.toDecipher = Text(self.parent, undo = 1)
        self.toDecipher.grid(row = 2, column = 1, padx = 10, pady = 10)
        self.toDecipher.insert(END, "Type text to decipher...")
       
        lockImage = PhotoImage(file = "lock.gif")
        unlockImage = PhotoImage(file = "unlock.gif")
        self.encipherButton = Button(self.parent, text = "Encipher", command = self._encode, padx = 10, pady = 10, image = lockImage, compound = TOP)
        self.decipherButton = Button(self.parent, text = "Decipher", command = self._decode, padx = 10, pady = 10, image = unlockImage, compound = TOP)
        #Due to weirdness with Tk's handling of image references, need to keep a throwaway reference
        #to maintain iamge icons
        self.encipherButton.image = lockImage
        self.encipherButton.grid(row = 1, column = 2, padx = 10, pady = 10)
        self.decipherButton.image = unlockImage
        self.decipherButton.grid(row = 2, column = 2, padx = 10, pady = 10)

        splashImage = PhotoImage(file = "splash.gif")
        self.splashLabel = Label(self.parent, text = "Solitaire Cipher v1.0", image = splashImage, compound = TOP, font = "Courier")
        self.splashLabel.image = splashImage
        self.splashLabel.grid(row = 2, column = 0, padx = 10)

        self.log = ScrolledText(self.parent, width = 30, height = 22)
        #Can't use console log method yet.
        self.log.insert(END, ">> Ready. View Help for entry rules.")
        self.log.state = DISABLED
        self.log.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = S)
        self.log.config(state = DISABLED)

        self.passphrase = Entry(self.parent, show = "*", width = 30)
        self.passphrase.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = NE)
        self.passphrase.xview_moveto(0)
        self.passphraseLabel = Label(self.parent, text = "Passcode:", padx = 8).grid(row = 1, column = 0, sticky = NW, pady = 10)

        self.menubar = Menu(self.parent)
        self.menubar.add_command(label = "About", command = self._display_about)
        self.menubar.add_command(label = "Help", command = self._display_help)
        self.menubar.add_command(label = "Quit", command = self.quit)
        self.parent.config(menu = self.menubar)

        self.parent.iconbitmap("cards-64.ico")

    def _console_log(self, message):
        """
        Logs events like decode/encode to the console.
        """
        self.log.config(state = NORMAL)
        self.log.insert(END, "\n>> " + message)  
        self.log.config(state = DISABLED)
        self.log.see(END)

    def _encode(self):
        """
        Encodes the contents of toCipher using Cipher class and places in toDecipher.
        """
        passkey = self.passphrase.get()
        #If text is retrived to END, newline is added. Must go 1 character less.
        message = self.toCipher.get(1.0, END+"-1c")
        if self._validate(message, passkey):
            passkey = passkey.upper()
            message = message.replace(" ", "").upper()
            encode = Cipher(message, passkey)
            encodedMessage = encode.encipher()
            self._console_log("Encoding successful. \nSee lower box for result.")
            self.toDecipher.delete(1.0, END)
            self.toDecipher.insert(END, encodedMessage)
        elif passkey == "":
            self._console_log("Error: no passcode entered.")
        elif message == "":
            self._console_log("Error: no message entered.")
        else:
            self._console_log("Encoding unsuccessful. \nInput contains one or more \nillegal characters. See Help \nfor rules.")

    def _decode(self):
        """
        Decodes the contents of toDecipher using Cipher class and places in toCipher.
        """
        passkey = self.passphrase.get()
        #If text is retrived to END, newline is added. Must go 1 character less.
        message = self.toDecipher.get(1.0, END+"-1c")
        if self._validate(message, passkey):
            passkey = passkey.upper()
            message = message.replace(" ", "").upper()
            decode = Cipher(message, passkey)
            decodedMessage = decode.decipher()
            self._console_log("Decoding successful. \nSee upper box for result.")
            self.toCipher.delete(1.0, END)
            self.toCipher.insert(END, decodedMessage)
        elif passkey == "":
            self._console_log("Error: no passcode entered.")
        elif message == "":
            self._console_log("Error: no message entered.")
        else:
            self._console_log("Decoding unsuccessful. \nInput contains one or more \nillegal characters. See Help \nfor rules.")

    def _validate(self, message, passkey):
        """
        Checks text input from toCipher, toDecipher, and passphrase fields for illegal characters during cipher/decipher processes.
        """
        passkeyOK = passkey.isalpha()
        messageOK = message.replace(" ", "").isalpha()
        return passkeyOK and messageOK

    def _display_help(self):
        """
        Displays help dialog on menu press.
        """
        help = Toplevel()
        help.grab_set()
        help.title("Help")
        help.resizable(0,0)
        help.iconbitmap("cards-64.ico")
        helpMessage = Message(help, text = self.helpText, padx = 10, pady = 10)
        helpMessage.pack()


    def _display_about(self):
        """
        Displays about dialog on menu press.
        """
        about = Toplevel()
        about.grab_set()
        about.title("About")
        about.resizable(0,0)
        about.iconbitmap("cards-64.ico")
        aboutMessage = Message(about, text = self.aboutText, padx = 10, pady = 10)
        aboutMessage.pack()


class Cipher():
    """
    Takes text input and a passphrase. Using Bruce Schneier's solitaire algorithm, keys a virtual deck
    using the passphrases and uses the keyed deck to encipher/decipher the text input.
    For the purposes of the algorithm, clubs are 1-13 (A-K), diamonds are 14-26, hearts are 27-39, and spades are 40-52.
    Both jokers are 53, though Joker A and Joker B are represented as 53 and 54 in the deck, respectively.

    For more information, visit Bruce Schneier's website: https://www.schneier.com/solitaire.html
    """

    def __init__(self, message, passphrase):
        self.message = message
        self.passphrase = passphrase

    def _let_to_num(self, letter):
        """
        Converts letters to their position in the alphabet, e.g., Z becomes 26.
        """
        #Assuming caps.
        letter = letter.upper()
        #The ASCII value of A is 65. A should be 1, and Z should be 26.
        return ord(letter) - 64

    def _num_to_let(self, number):
        """
        Converts number n to the nth letter in the alphabet, e.g. 1 becomes A.
        """
        #The ASCII value of A is 65. A should come in as 1, must correct.
        return chr(number + 64)

    def _shift_jokers(self, deck):
        """
        Shifts Joker A forward 1 position in the deck, and Joker B forward two positions. 
        If the end of the deck is reached, the joker will be moved underneath the first cards of the deck.
        """
        a_joker_index = deck.index(53)
        new_a_joker_index = a_joker_index + 1
        if new_a_joker_index >= 54:
            #If A is at end of deck, mod will place at ind 0, at beginning.
            #Must be moved to after first card.
            new_a_joker_index = new_a_joker_index % 54 + 1
        deck.remove(53)
        deck.insert(new_a_joker_index, 53)
        
        b_joker_index = deck.index(54)
        new_b_joker_index = b_joker_index + 2
        if new_b_joker_index >= 54:
            #If B is at end of deck or one before, mod will be off by one.
            new_b_joker_index  = new_b_joker_index % 54 + 1
        deck.remove(54)
        deck.insert(new_b_joker_index, 54)

        return deck[:]

    def _triple_cut(self, deck):
        """
        Switches the segments of the deck not between (inclusive) of Joker A and Joker B.
        """
        a_joker_index = deck.index(53)
        b_joker_index = deck.index(54)
        if b_joker_index > a_joker_index:
            return deck[b_joker_index + 1:len(deck)] + deck[a_joker_index:b_joker_index + 1] + deck[0:a_joker_index]
        else:
            return deck[a_joker_index + 1:len(deck)] + deck[b_joker_index:a_joker_index + 1] + deck[0:b_joker_index]

    def _count_cut(self, deck,target = 999):
        """
        Using the numerical value of the bottommost card in the deck n (1-54), shifts a segment of n cards 
        beginning from the top of the deck to above the bottom card.
        """
        #if no val for target specified, target will be last card in deck, as in normal keystream gen
        #if val specified, as in deck keying with passphrase, target will change to specified val
        if target == 999:
            target = deck[53]
        #A and B jokers have same numeric value, despite representation in deck. Fixing.
        if target == 54:
            target = 53

        return deck[target:53] + deck[0:target] + [deck[53]]

    def _find_output(self, deck):
        """
        Using the numerical value n of the topmost card in the deck, selects the (n+1)th card in the deck 
        as the output number.
        """
        target = deck[0]
        #A and B jokers have same numeric value, despite representation in deck. Fixing.
        if target == 54:
            target = 53
        #Want card AFTER target, so no -1 to account for index/card number diff.
        output = deck[target]
        #A and B jokers have same numeric value, despite representation in deck. Fixing.
        if output == 54:
            output = 53
        return output

    def _key_deck(self, passphrase):
        """
        Prearranges the deck according to given passphrase.
        """
        deck = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54]
        for char in passphrase:
            deck = self._run_solitaire(deck)
            deck = self._count_cut(deck, self._let_to_num(char))
        return deck[:]

    def _run_solitaire(self, deck):
        """
        Performs first 4 cipher operations, not including output (step five).
        """
        deck = self._shift_jokers(deck)
        deck = self._triple_cut(deck)
        deck = self._count_cut(deck)
        return deck[:]

    def _generate_keystream(self, deck, length):
        """
        Generates a numerical keystream of given length using a given deck.
        """
        stream = []
        while (length > 0):
            deck = self._run_solitaire(deck)
            output = self._find_output(deck)
            #If a joker is output, must just redo the solitaire without getting an output
            if output == 53:
                continue
            stream.append(output)
            length -= 1
        return stream

    def encipher(self):
        """
        Enciphers the set message using the set passphrase.
        """
        plaintext = self.message
        passkey = self.passphrase
        deck = self._key_deck(passkey)
        keystream = self._generate_keystream(deck, len(plaintext))
        ciphertext = []
        for key, plain in zip(keystream, list(plaintext)):
            cipher_item = key + self._let_to_num(plain)
            while cipher_item > 26:
                cipher_item = cipher_item - 26
            ciphertext.append(self._num_to_let(cipher_item))
        return "".join(ciphertext)

    def decipher(self):
        """
        Deciphers the set message using the set passphrase.
        """
        ciphertext = self.message
        passkey = self.passphrase
        deck = self._key_deck(passkey)
        keystream = self._generate_keystream(deck, len(ciphertext))
        plaintext = []
        for key, cipher in zip(keystream, list(ciphertext)):
            plain_item = self._let_to_num(cipher) - key
            while plain_item <= 0:
                plain_item = plain_item + 26
            plaintext.append(self._num_to_let(plain_item))
        return "".join(plaintext)


def main():
    root = Tk()
    root.geometry("1100x825")
    root.resizable(0,0)
    app = CipherGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()


        