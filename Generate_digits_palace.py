from mpmath import mp
from random import randint
import xml.etree.ElementTree as ET
import os

class InputError(Exception):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class Palace(object):

	def __init__(self,name):
		self.name = name
		self.rooms = {}
		self.n_loci = 0
		self.locus_list = []


	def display_info(self):
		s = (f'{self.name} is a palace with {len(self.rooms)} rooms '
			f'and a total of {self.n_loci} loci')
		

	def generate_locus_list(self):
		for ri,room in self.rooms.items():

			for li,locus in room.loci.items():

				self.locus_list.append( locus.info )

	def guess_before_after(self):

		guess_next = bool(randint(0,2))
		shift = guess_next - (guess_next==0)

		int_ref = randint(0,self.n_loci + 1)
		int_guess = int_ref + shift

		
		if int_guess == self.n_loci:
			
			int_ref = 1
			int_guess = 0
			guess_next = False

		elif int_guess == -1:
			
			int_ref = n_loci - 2
			int_guess = n_loci - 1
			guess_next = True

		before_after = ["before","after"][guess_next]
		ref_value = self.locus_list[int_ref]
		corr_guess = self.locus_list[int_guess]

		msg = "What decimals comes %s %s? (enter x to quit)\n\t" %(before_after,ref_value)
		ans = input( msg )
		if ans == 'x':
			pass
		else:
			if ans == corr_guess:
				print(f"\tNice work! {ans} comes {before_after} {ref_value}\n\n")
			else:
				print(f"\tNOOB, You guessed wrong! Correct answer is {corr_guess}!\n\n")

			self.guess_before_after()


class PAO_palace(Palace):

	def __init__(self,name):
		Palace.__init__(self,name)


	def palace_to_anki(self,deck_name,note_type,fID,n = 9, skipped_decimals = 0):
		header = (
			'#separator:tab\n'
			'#html:true\n'
			'#notetype column:1\n'
			'#deck column:2\n'
		)
		s = ''
		for r,room in self.rooms.items():

			for l,locus in room.loci.items():

				x = n*locus.total_order + skipped_decimals
				
				front = f'Decimal nr {x+1} - {x+n}'
				locus_str = f'{r} : {l} ({locus.room_order+1})'
				back = locus.info

				s += '\t'.join([note_type,deck_name,front,locus_str,back]) + '\n'

		with open(fID,'w',encoding='utf-8') as f:
			f.write(header + s[:-1])

	def generate_decimals(self,number = 'pi', n=9, skip_first=0):

		N = (self.n_loci)*n + skip_first + 2
		mp.dps = N

		if number == 'pi':
			digits = str(mp.pi)[2 + skip_first:N]
		elif number == 'e':
			digits = str(mp.exp(1))[2 + skip_first:N]
		else:
			raise InputError( number, "Invalid input, expected 'e' or 'pi'!" )

		x = 0
		for room_name,room in self.rooms.items():
			for locus_name,locus in room.loci.items():
				locus.info = digits[n*x:n*(x+1)]
				x+=1


class Room(object):

	def __init__(self,name):
		self.name = name
		self.loci = {}

	def __str__(self):
		return f"Room: {self.name}, #loci: {len(self.loci)}"

	def put(self,name,room_order,total_order):
		new_locus = Locus(name,room_order,total_order)
		self.loci[name] = new_locus

class Locus(object):

	def __init__(self,name,room_order,total_order):
		self.name = name
		self.info = None
		self.room_order = room_order
		self.total_order = total_order

	def __str__(self):
		n,N = self.room_order,self.total_order
		return f"{self.name} : {self.info} ({n:2d} - {N:3d})"


def create_palace(fID, PAO = True):

	tree = ET.parse( fID )
	root = tree.getroot()

	if PAO:
		P = PAO_palace( root.get("name") )
	else:
		P = Palace( root.get("name") )


	for room in root.findall("room"):
		room_name = room.get("name")

		new_room = Room( room_name )
		loci = [locus.text for locus in room.findall("locus")]

		for li, locus in enumerate(loci):
			new_room.put(locus,li,P.n_loci)
			P.n_loci += 1

		P.rooms[room_name] = new_room

	return P


if __name__ == "__main__":
	

	Atlantis = create_palace(f"{os.getcwd()}/input_files/Atlantis.xml")
	Atlantis.generate_decimals('e')
	Atlantis.palace_to_anki(
		deck_name = 'Decimaler::e',
		note_type = 'Kort med locus-visa locus',
		fID = './txt_files_anki/e_decimals.txt',
		n = 9, skipped_decimals = 0
	)


	skip_first = 2
	Cyber_Egypt = create_palace(f"{os.getcwd()}/input_files/Cyber_Egypt.xml")
	Cyber_Egypt.generate_decimals('pi',skip_first=skip_first)
	Cyber_Egypt.palace_to_anki(
		deck_name = 'Decimaler::π',
		note_type = 'Kort med locus-visa locus',
		fID = './txt_files_anki/π_decimals.txt',
		skipped_decimals=skip_first
	)