"""
Recieve a string describing album personnel and generate a dictionary for each
artist on the album giving key:value access to data regarding name/s, 
instrument/s and track/s.

The AlbumPersonnel class recieves the personnel string and generates a list of artist
arrays broken down into two sub-lists [[name], [instruments/tracks]] stored in 
self.final_arrays.

The AlbumArtist class takes as input one partitioned artist array from the list
generated by the AlbumPersonnel class and generates an artist dictionary with
key:value pairings for each name (first, middle, last, nicknames), instrument,
and which tracks they performed on if specified. Said dict is stored in
self.artist_dict.
"""

import re

_digits = re.compile('\d')
def contains_digits(word):
	"""Return True if digits are present in a word (targets track info)."""
	return bool(_digits.search(word))

# Personnel String Templates (for testing):
# artists = "Nat Adderley (cornet -1,2,4/6) Donald Byrd (trumpet -1,2,4,5) Cannonball Adderley (alto saxophone) Jerome Richardson (tenor saxophone, flute -1,4/6) Horace Silver (piano) Paul Chambers (bass) Kenny Clarke (drums)"
# artists = 'Nat Adderley (cornet) Ernie Royal (trumpet) Bobby Byrne, Jimmy Cleveland (trombone) Cannonball Adderley (alto saxophone) Jerome Richardson (tenor saxophone, flute) Danny Bank (baritone saxophone) Junior Mance (piano) Keter Betts (bass) Charles "Specs" Wright (drums)'
# artists = "Pharoah Sanders (tenor,soprano saxophone, bells, percussion) Michael White (violin, percussion) Lonnie Liston Smith (piano, electric piano, claves, percussion) Cecil McBee (bass, finger cymbals, percussion) Clifford Jarvis (drums, maracas, bells, percussion) James Jordan (ring cymbals -3)"
# artists = "Clifford Brown, Art Farmer (trumpet) Ake Persson (trombone) Arne Domnerus (alto saxophone, clarinet) Lars Gullin (baritone saxophone) Bengt Hallberg (piano) Gunnar Johnson (bass) Jack Noren (drums) Quincy Jones (arranger, director)"
# artists = "Chet Baker (trumpet) Ted Ottison (trumpet -5,6) Sonny Criss (alto saxophone -1,2,6) Jack Montrose (tenor saxophone -1/3,6) Les Thompson (harmonica -7) Al Haig (piano) Dave Bryant (bass) Larry Bunker (drums)"
# artists = "Chet Baker, Pete Candoli (trumpet) Bob Enevoldsen (valve trombone) John Graas (French horn) Ray Siegel (tuba) Bud Shank (alto saxophone) Don Davidson (baritone saxophone) Gerry Mulligan (baritone saxophone, piano) Joe Mondragon (bass) Chico Hamilton (drums)"
artists = "Chet Baker (trumpet) with Siegfried Achhammer, Klaus Mitchele, Rolf Schneebiegl, Hans Wilfert (trumpet) Werner Betz, Otto Bredl, Helmut Hauck, Heinz Hermansdorfer (trombone) Franz Von Klenck, Helmut Rheinhardt (alto saxophone) Bubi Aderhold, Paul Martin (tenor saxophone) Johnny Feigl (baritone saxophone) Werner Drexler (piano) Werner Schulze (bass) Silo Deutsch (drums) Kurt Edelhagen (leader)"
# artists =
# artists =
# artists =
# artists =
# artists =

class AlbumPersonnel():

	def __init__(self, personnel_string):
		"""
		Recieve a string of personnel info for a given album and generate
		a list which has a sub-array for each artist. Each artist sub-array 
		has two further sub-arrays for that artist's name and instrument/track
		info.

		Once the various shorthand strategies employed in the initial personnel
		string have been corrected for, said list will be stored in
		self.final_artist_arrays in __init__.   
		"""
		self.personnel_string = personnel_string
		self.final_artist_arrays = []
	
	def initial_artist_arrays(self):
		"""
		Split personnel_string into words and return a list of arrays each
		containing an artist's name/s and instrument/track info.
		"""
		split_strings = self.personnel_string.split(")")
		split_artists = [string.lstrip(" ")  + ")" for string		# replace ")" delimiter for later use
						 in split_strings[:len(split_strings) - 1]]	# avoid last empty item
		initial_artist_arrays = [artist.split() for artist in split_artists]
		return initial_artist_arrays
	
	def partition_artist_array(self, artist_array):
		"""
		Recieve one of the artist arrays generated by initial_artist_arrays(),
		identify the first word starting with a "(", and return an array
		partitioned into two sub-arrays: [[names], [instruments_tracks]].
		"""
		for word in artist_array:
			if word.startswith("("):
				target = artist_array.index(word)
		partitioned_artist_array = []
		partitioned_artist_array.append(artist_array[:target])
		partitioned_artist_array.append(artist_array[target:])
		return partitioned_artist_array

	def partitioned_artist_arrays(self):
		"""
		Call partition_artist_array() on each array generated as a result of 
		calling initial_artist_arrays() and return a list of partitioned
		artist arrays.
		"""
		partitioned_artist_arrays = [self.partition_artist_array(array)
									 for array
									 in self.initial_artist_arrays()]
		return partitioned_artist_arrays
	
# # # The Rogue-Array Correction Suite # # #
	
	# The following methods are called in correct_problem_arrays()

	def contains_multiple_artists(self, name_array):
		"""
		Recieve the 'name' sub-array of a given artist array and return True
		if there appear to be multiple artists represented.
		"""
		contains_multiple_artists = False
		for name in name_array:
			if name.endswith(","):
				contains_multiple_artists = True
		return contains_multiple_artists
	
	def split_multiple_artists(self, name_array):
		"""
		Recieve the 'name' sub-array of a given artist array and return a new
		array which contains a sub-array for each artist represented.

			Example:
				['Bobby', 'Byrne,', 'Jimmy', 'Cleveland'] becomes:
				[['Bobby', 'Byrne,'], ['Jimmy', 'Cleveland']]
		"""
		endpoints = [word for word in name_array
					 if word.endswith(',')
					 or word == name_array[-1]]
		
		split_multiple_artists = []
		temporary_array = []
		for word in name_array:
			if word not in endpoints:
				temporary_array.append(word)
			else:
				temporary_array.append(word)
				split_multiple_artists.append(temporary_array)
				temporary_array = []
		return split_multiple_artists

		# # # # # # # # # # # # # # #

	def contains_multiple_range_word(self, word):
		"""
		Recieve a single word from the 'instrument/track' sub-array of a given
		artist array and return True if that word indicates multiple ranges.
		"""
		contains_multiple_range_word = False	
		for letter in word[:len(word) - 1]: # ignore trailing commas
				if letter == ",":
					contains_multiple_range_word = True
		return contains_multiple_range_word

	def array_containing_multiple_range_word(self, instrument_array):
		"""
		Recieve the 'instrument/track' sub-array of an artist array and return
		True if any of the words in that array indicate multiple ranges.
		"""
		array_containing_multiple_range_word = False
		for word in instrument_array:
			if self.contains_multiple_range_word(word) \
			and not contains_digits(word):
				array_containing_multiple_range_word = True
		return array_containing_multiple_range_word

	def revise_multiple_range_array(self, instrument_array):
		"""
		Recieve the 'instrument/track' sub-array of an artist array and return
		a revised array which unpacks the shorthand instrument notation from the
		initial personnel string into a new instrument string pairing each range
		with its base-instrument.

			Example:
				['soprano,alto,tenor', 'saxophone'] becomes:
				['soprano saxophone', 'alto saxophone', 'tenor saxophone'] 
		"""
		revised_array = []
		for word in instrument_array:
			if self.contains_multiple_range_word(word):
				base_instrument = (instrument_array[
								   instrument_array.index(word)+1])
				instrument_array.remove(base_instrument)
				map(lambda r: revised_array.append(r + " " + base_instrument),
					word.split(","))
			else:
				revised_array.append(word)
		return revised_array
			
		# # # # # # # # # # # # # # #	
			
	def contains_multiple_word_instrument(self, instrument_array):
		"""
		Recieve the 'instrument/track' sub-array of an artist array and return
		True if a multiple-word instrument appears to be present.
		"""
			# ['(ring', 'cymbals', '-3)']
			# ['(alto', 'saxophone)']

		contains_multiple_word_instrument = False
		# if len(instrument_array) == 2				\
		# and not (instrument_array[0]).endswith(",") \
		# and not contains_digits(instrument_array[1]):
		# 	contains_multiple_word_instrument = True
		
		# for word in instrument_array:
		# 	if word.endswith(",") and not contains_digits(word):
		# 		contains_multiple_word_instrument = True

		for word in instrument_array[:-1]:
			if "," not in word[:-1]:
				contains_multiple_word_instrument = True

		return contains_multiple_word_instrument

	def join_multiple_word_instrument(self, instrument_array):
		"""
		Recieve the 'instrument/track' sub-array of an artist array and return
		a revised array which combines the words of a multiple-word instrument
		into a single string.

			Example:
				['alto', 'saxophone'] becomes: ['alto saxophone']
		"""
		revised_array = []
		for word in instrument_array:
			next_word = instrument_array.index(word) + 1
			if "," not in word and not word.endswith(")") \
			and not contains_digits(word) 				  \
			and not contains_digits(instrument_array[next_word]):
				revised_array.append(word + " " + instrument_array[next_word])
				instrument_array.remove(instrument_array[next_word])
			else:
				revised_array.append(word)
		return revised_array

# #	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

	def correct_multiple_artists(self):
		"""
		Call split_multiple_artists() on any artist arrays deemed necessary
		by contains_multiple_artists() and return an array of artist arrays.
		"""
		correct_multiple_artists = []
		for artist_array in self.partitioned_artist_arrays():
			if self.contains_multiple_artists(artist_array[0]):
				for artist in self.split_multiple_artists(artist_array[0]):
					temporary_array = []
					temporary_array.append(artist)
					temporary_array.append(artist_array[1])
					correct_multiple_artists.append(temporary_array)
			else:
				correct_multiple_artists.append(artist_array)
		return correct_multiple_artists

	def correct_multiple_ranges(self):
		"""
		Call revise_multiple_range_array() on any artist arrays deemed necessary
		by array_containing_multiple_range_word() and return an array of artist
		arrays.
		""" 
		correct_multiple_ranges = []
		for artist_array in self.correct_multiple_artists():
			if self.array_containing_multiple_range_word(artist_array[1]):
				temporary_array = []
				instruments = self.revise_multiple_range_array(artist_array[1])
				temporary_array.append(artist_array[0])
				temporary_array.append(instruments)
				correct_multiple_ranges.append(temporary_array)
			else:
				correct_multiple_ranges.append(artist_array)
		return correct_multiple_ranges

	def correct_multiple_word_instruments(self):
		"""
		Call join_multiple_word_instrument() on any artist arrays deemed necessary
		by contains_multiple_word_instrument() and append the results to
		self.final_arrays in __init__.
		"""
		for artist_array in self.correct_multiple_ranges():
			if self.contains_multiple_word_instrument(artist_array[1]):
				temporary_array = []
				instruments = self.join_multiple_word_instrument(artist_array[1])
				temporary_array.append(artist_array[0])
				temporary_array.append(instruments)
				self.final_artist_arrays.append(temporary_array)
			else:
				self.final_artist_arrays.append(artist_array)


class AlbumArtist():

	def __init__(self, artist_array): 
		"""
		Recieve a single artist array from the list generated by the 
		AlbumPersonnel class and stored in its self.final_artist_arrays attribute.

		Example:
		[['Jerome', 'Richardson'], ['(tenor saxophone,', 'flute', '-1,4/6)']]

		Generate a dictionary which has key:value pairings for every piece of
		name, instrument, and track data given in the artist array and store
		that dict in the attribute self.artist_dict in __init__.
		"""
		self.artist_array = artist_array
		self.names = artist_array[0]
		self.instrument_track = artist_array[1]
		self.artist_dict = {}

	def clean_word(self, word):
		"""
		Recieve a word and return the word stripped of unnecessary
		characters.
		"""
		if word.startswith('(') and word.endswith(')'):
			x = word.lstrip('(')
			return x.rstrip(')')
		elif word.startswith('-') and word.endswith(')'):
			x = word.lstrip('-')
			return x.rstrip(')')
		elif word.startswith('('):
			return word.lstrip('(')
		elif word.endswith(')'):
			return word.rstrip(')')
		elif word.endswith(','):
			return word.rstrip(',')
		else:
			return word

	#	#	#	Assign artist_dict Info 	#	#	#

		# may eventually need to deal with track-info shorthand
		#	ex: "1, 4/7" - the backslash implies "1, 4,5,6,7"

	def tracks_to_dict(self):
		"""
		Identify any track info in the 'instrument_track' sub-array and assign
		a clean_word() version to self.artist_dict, then remove track info
		from the 'instrument_track' sub-array leaving only instrument info.
		"""
		for inst in self.instrument_track:
			if contains_digits(inst):
				self.artist_dict['tracks'] = self.clean_word(inst)
				self.instrument_track.remove(inst)

	def instruments_to_dict(self):
		"""Assign instrument info to artist_dict."""
		inst_num = 1
		for inst in self.instrument_track:
			key = "inst_" + str(inst_num)
			self.artist_dict[key] = self.clean_word(self.clean_word(inst)) # added comma protection
			inst_num += 1

	def names_to_dict(self):
		"""Assign name info to artist_dict."""
		name_num = 1
		for name in self.names:
			key = "name_" + str(name_num)
			self.artist_dict[key] = self.clean_word(name)
			name_num += 1

	#	#	#	#	#	#	#	#	#	#	#	#

	def create_artist_dict(self):
		"""
		Generate the final artist dictionary by calling each of the
		artist_dict assignment functions.
		"""
		self.tracks_to_dict()
		self.instruments_to_dict()
		self.names_to_dict()


def album_artists(personnel_string):
	"""
	Create an instance of an AlbumPersonnel object, and generate its
	final_artist_arrays attribute. Create an instance of an AlbumArtist object
	for each artist array in the AlbumPersonnel object, generate the
	artist_dict attribute. Return a list of artist dicts for each artist
	array.
	"""
	personnel = AlbumPersonnel(personnel_string)
	personnel.correct_multiple_word_instruments()
	artist_dicts = [] 
	for artist_array in personnel.final_artist_arrays:
		album_artist = AlbumArtist(artist_array)
		album_artist.create_artist_dict()
		artist_dicts.append(album_artist.artist_dict)
	return artist_dicts

def print_album_artists():
	artist_dict = album_artists(artists)
	for d in artist_dict:
		keys = d.keys()
		name = [word for word in keys if "name" in word]
		inst = [word for word in keys if "inst" in word]
		track = [word for word in keys if "track" in word]
		for n in name[::-1]:
			print d[n], " ",
		print " --- ",
		if len(track) > 0:
			for i in inst[:-1]:
				print d[i], ", ",
			print d[inst[-1]],
			print " --- tracks: ", d[track[0]]
		else:
			for i in inst[:-1]:
				print d[i], ", ",
			print d[inst[-1]]

print_album_artists()

# personnel = AlbumPersonnel(artists)
# target = personnel.partitioned_artist_arrays()[5]
# print personnel.contains_multiple_word_instrument(target[1])
# print personnel.join_multiple_word_instrument(target[1])


# To Do:
	# - set this module up to automatically take in a personnel string and return
	#	 organized artist data in json format?
