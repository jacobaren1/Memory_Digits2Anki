from DigitPalace import PAO_palace, create_palace

if __name__ == "__main__":

	header =(
		  "##### ##### ##### #####  ##### ##### ##### ##### #####\n"
		  "#####    This is an example script for e and π   #####\n"
		  "##### ##### ##### #####  ##### ##### ##### ##### #####\n\n"
		)

	print(header)
	print("---- Creating txt-file for e with Atlantis palace ----")
	

	Atlantis = create_palace("./input_files/Atlantis.xml")
	Atlantis.generate_decimals('e')
	Atlantis.palace_to_anki(
		deck_name = 'Decimaler::e',
		note_type = 'Kort med locus-visa locus',
		fID = './txt_files_anki/e_decimals.txt',
		n = 9, skipped_decimals = 0
	)
	print("---- File successfully created ----\n")


	print("---- Creating Anki files for π with Cyber Egypt palace ----")
	print("\t Note: first 2 decimals, skipped. 3.14 is to well known :)")

	skip_first = 2
	Cyber_Egypt = create_palace("./input_files/Cyber_Egypt.xml")
	Cyber_Egypt.generate_decimals('pi',skip_first=skip_first)
	Cyber_Egypt.palace_to_anki(
		deck_name = 'Decimaler::π',
		note_type = 'Kort med locus-visa locus',
		fID = './txt_files_anki/π_decimals.txt',
		skipped_decimals=skip_first
	)

	print("---- File successfully created ----\n")


	Cyber_Egypt.room_order_to_anki()
	Atlantis.room_order_to_anki()

	print("---- End of script ----\n\n")