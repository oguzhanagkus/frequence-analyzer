import matplotlib.pyplot as plt  # Maybe you need to install this package for graphics
import string
import math
import csv


def order_fct(input_list: list):  # Order function, get an input as a list, and return an ordered list
    temp = input_list.copy()  # Do not change the original list
    n = len(temp)  # Size of list

    for j in range(0, n - 1):
        smallest = j
        for i in range(j + 1, n):
            if temp[i] < temp[smallest]:
                smallest = i

        temp[j], temp[smallest] = temp[smallest], temp[j]  # swap with the smallest element

    return temp


class Reader:  # Base class
    def __init__(self, path: str):
        self.file = ""
        self.dictionary = {}

        try:
            with open(path, "r") as temp:
                self.file = temp.read()  # Read the file as string

        except:
            print("File read error!")

    def create_dictionary(self):
        count = 0  # Total letter count
        self.dictionary = dict.fromkeys(string.ascii_lowercase, 0)  # Create a empty dictionary from letter 'a' to 'z'

        for character in self.file:
            if character.isalpha():  # If it is a alphabetical character, not newline, punctuation or whitespace
                count += 1  # Increase total letter count
                character = character.lower()  # For capital letters
                self.dictionary[character] += 1  # Update the letter count

        for i in self.dictionary:
            self.dictionary[i] = round(self.dictionary[i] / count * 100, 2)  # Convert to percentage, like %9.34


class Decipher(Reader):  # It inherits file and dictionary variables and create_dictionary() method from Reader class
    def __init__(self, path_1: str, path_2: str, format: str):
        super().__init__(path_1)
        self.coded = ""
        self.deciphered = ""
        self.format = "txt"  # It is txt as default
        self.hist = []
        self.ordered = []
        self.entropy = 0

        if format == "csv":  # If it is csv, then update the format.
            self.format = format

        try:
            with open(path_2, "r") as temp:
                self.coded = temp.read()  # Read coded text as string

        except:
            print("File read error!")

    def create_hist(self):
        self.hist = list(self.dictionary.values())

    def plot_hist(self):
        letters = list(self.dictionary.keys())

        plt.bar(letters, self.hist)
        plt.savefig("hist.png")

    def plot_pie(self):
        letters = list(self.dictionary.keys())

        figure_1, ax_1 = plt.subplots()
        ax_1.pie(self.hist, labels=letters, autopct='%1.1f%%', startangle=90)
        ax_1.axis('equal')
        plt.savefig("pie.png")

    def create_ordered(self):
        self.ordered = order_fct(self.hist)  # Using order_fct() function

    def compute_entropy(self):  # Shannon entropy of the first file
        for letter in self.dictionary:
            frequency = self.dictionary[letter] / 100  # We have frequencies of each letter, to ignore % divide by 100

            if frequency > 0:  # Some frequencies equals to zero, log2(0) is not defined
                self.entropy += frequency * math.log2(frequency)

        self.entropy = -self.entropy

        return self.entropy

    def decipher(self, reference="z"):  # Reference letter is 'z' as default, if you wish you can change it
        alphabet = string.ascii_letters  # Alphabet is: "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        alphabet_size = len(alphabet)  # Size of alphabet is 52

        key_list = list(self.dictionary.keys())
        value_list = list(self.dictionary.values())
        key = key_list[value_list.index(self.ordered[-1])]  # Most frequent letter in the first file

        key_index = alphabet.index(key)  # Index of the key according to alphabet
        reference_index = alphabet.index(reference)  # Index of the reference letter according to alphabet
        shift_amount = reference_index - key_index  # Calculate the shift amount

        for character in self.coded:  # Shift all letters in the coded, then add to deciphered variable
            if character.isalpha():  # Ignore numeric values, white spaces and punctuation
                temp = alphabet.index(character) + shift_amount  # Shift
                temp %= alphabet_size  # If overflow the alphabet size, return to beginning of alphabet
                self.deciphered += alphabet[temp]  # Add current letter

            else:
                self.deciphered += character  # Add non-alphabetical characters

    def write_code(self):
        if self.deciphered == "":  # If the coded text is not deciphered
            print("Call decipher() method!")

        else:
            if self.format == "txt":  # Write to txt
                with open("decoded.txt", "w") as output:
                    output.write(self.deciphered)

            elif self.format == "csv":  # Write to csv, each word in one column
                words = self.deciphered.split(" ")  # Split the message

                with open("decoded.csv", "w") as output:
                    writer = csv.writer(output)
                    writer.writerow(words)


def driver():  # My driver code
    # Write the path of files
    file_1 = "text1"
    file_2 = "text2"

    example = Decipher(file_1, file_2, "txt")
    example.create_dictionary()
    example.create_hist()
    example.create_ordered()
    # example.plot_hist()
    # example.plot_pie()
    example.decipher()
    example.write_code()
    print("Entropy of first file:", example.compute_entropy())


if __name__ == '__main__':
    driver()
