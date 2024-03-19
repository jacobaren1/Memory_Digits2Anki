from mpmath import mp
import xml.etree.ElementTree as ET

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
	"""
		The main palace consisting of rooms as subpalaces
	"""

	def __init__(self,name):
		self.name = name
		self.rooms = {}
		self.n_loci = 0
		self.locus_list = []

	def __str__(self):
		return f"Memory Palace: {self.name} # loci: {self.n_loci}"

	def display_info(self):
		s = (f'{self.name} is a palace with {len(self.rooms)} rooms '
			f'and a total of {self.n_loci} loci')

	def generate_locus_list(self):
		#populates locus_list with all loci in the palace

		for ri,room in self.rooms.items():

			for li,locus in room.loci.items():

				self.locus_list.append( locus )

	def room_order_to_anki(self,deck_name = None,note_type='Bas (och omvänt)',fID=None,sep='\t'):
		if deck_name is None:
			deck_name = f'PalacesOrder::{self.name}'
		if fID is None:
			fID = f"./txt_files_anki/{self.name}_to_anki.txt"

		s = (
			'#separator:tab\n'
			'#html:true\n'
			'#notetype column:1\n'
			'#deck column:2\n'
		)

		for ri,(room_name,room) in enumerate(self.rooms.items()):
			front = f'Room number {ri+1} in {self.name}'
			back = f'{room_name} ({len(room.loci)} loci)'

			s += sep.join([note_type,deck_name,front,back]) + '\n'

		with open(fID,'w') as f:
			f.write( s[:-1] )


class PAO_palace(Palace):

	"""
		Palace class with special methods to 
	"""

	def __init__(self,name):
		Palace.__init__(self,name)


	def __str__(self):
		return f"PAO Memory Palace: {self.name} # loci: {self.n_loci}"

	def palace_to_anki(self,deck_name,note_type,fID,n = 9, skipped_decimals = 0,sep='\t'):
		
		#initiating output string with header with metadata for anki-import
		s = (
			'#separator:tab\n'
			'#html:true\n'
			'#notetype column:1\n'
			'#deck column:2\n'
		)

		#loop over all rooms in the palace
		for r,room in self.rooms.items():

			#loop over all loci in each room
			for l,locus in room.loci.items():

				#
				x = n*locus.total_order + skipped_decimals
				
				front = f'Decimal nr {x+1} - {x+n}'
				locus_str = f'{r} : {l} ({locus.room_order+1})'
				back = locus.info

				s += sep.join([note_type,deck_name,front,locus_str,back]) + '\n'

		with open(fID,'w',encoding='utf-8') as f:
			f.write(s[:-1])

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

	def get_sequens(self,x):
		if self.locus_list == []:
			self.generate_locus_list()
		return self.locus_list[x].info

	

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