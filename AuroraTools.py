# exports objects and character meshes, areas to the D'jinni Witcher Editor

EXPORTER_INTRO = "# Exported with the Knight Tools\n# Sergey Poklonskiy, serhii.poklonskyi@outlook.de, knight.tools.debug@gmail.com\n# special thanks to fantasta for his insightful export script for blender 2.49\n"

import bpy
import os
import shutil as sh
import webbrowser as wb
from . import func_lib_misc as miscf
from . import func_lib_images as imgs
from . import html_helpers as htm
from . import func_lib_materials as matr

# unsure imports
try:
	from PIL import Image as pillowimage
except:
	print("unable to import Pillow, some functionalities will be disabled!")
	
try:
	import numpy
except:
	print("unable to import numpy, some functionalities will be disabled!")
	
def ifel(condition, then_, else_):
	if condition:
		return then_
	else:
		return else_


		
#####################
# TEXTURE FUNCTIONS #
#####################

def saveDDS(img, destination, mip_map_count = 0, encoding):
	
	"""
		save a PIL Image as DDS
	"""
	
	# get the c++ dds library
	# test how to save .dds images with the function
		# build a python wrap around the function 'save'
		# this wrapper function takes image data and parameters as inputs: pixels, mip-map levels etc.
		# the types that it takes are pythonic
			# the wrapped procedure is tested as a standalone python C-module
				# the module is connected to Blender
					# PIL image passes its data to the wrapped function and save occurs - many congratulations
	
	return

def saveDDSCubemap(img, destination, encoding):
	"""
		save a dds cubemap !
	"""
	
	return
	
	
def saveTGA(img, destination):

	"""
		save a PIL Image as .tga
	"""
	return
	
def applyColorRamp(img):
	
	"""
		applies a color ramp to a given image
	"""
	return
	
def forceSquare(img, method):

	"""
		force a square size for an image, for methods 'SQUEEZE' or 'STRETCH'
	"""
	return
	
def getCubeMap(imgs):

	"""
		from the collection of 6 images, get a cubemap
	"""
	return
	
	
		
##################
# THE SHADER CLASS
##################
	



class djinni_shader:

	"""
		the virtual object that represents the blender shader node, textures and parameters that belong to it
	"""
	
	TYPES = ["norm_env_rim_l", "selfilum_b"] # collect all known shader types here
	
	def __init__(self, shdr_node):
		
		""" 
			try to initialize from the given shader node, throw error if unknown type
		"""
		
		return
	
class shdr_norm_env_rim_1:
	
	"""
		The unknown norm_env_rim_1 type of the shader
	"""
	
	# initialize from the corresponding node
		
	
	def __init__(self, shdr_node):
		"""
			initialization is from its corresponding shader node
		"""
		# collect textures
		self.textures = {}
		try:
			self.textures['color'] = tTexture(shdr_node.inputs['Color'].links[0].from_node.image, "tex", "COLOR")
		except:
			pass
			
		# if normal map and specularity is the same image then 
		# else
		
		# save the ambient occlusion map
		
		# save the environment map
	
	
################
# THE LOG_ CLASS
################
	
class Log_:
	"""
		a log that keeps errors, warnings, and messages
	"""
	
	def __init__(self):
		self._lines = [] # lines contain strings ['string_text', indent, type] which are then used to produce different reports on the log ...
		self.indent = 0
		
	def clear(self):
		self.__init__()
		
	def err(self, str_err):
		self._lines.append((str_err, self.indent, 'ERR'))
		
	def warn(self, str_warn):
		self._lines.append((str_warn, self.indent, 'WARN'))
		
	def msg(self, str_message):
		self._lines.append((str_message, self.indent, 'MSG'))
		
	def print(self, indent):
		txt = ""
		for l_ in self._lines:
			txt = txt + indent*l_[1] + l_[0] + "\n"
		print(txt)
		
	
###########################
# !!!!!!!!!!!!!!!!!!!!!!!!!

# PROPERTIES !!!!!!!!!!!!!!

# !!!!!!!!!!!!!!!!!!!!!!!!!
###########################


# 1. types of aurora exportable items

props_exportable_types = [
	('BASE', 'BASE', 'Aura base object', 1),
	('TRIMESH', 'TRIMESH', 'Basic trimesh node', 2),
	('SHADOW', 'SHADOW', 'Trimesh node that is a shadow', 3),
	('PWK', 'PWK', 'Trimesh that is a placeable walkmesh', 4),
	('LIGHT', 'LIGHT', 'A light source', 5),
	('NONE', 'NONE', 'The object is not an aurora exportable', 6)
]

aur_exportableType_ = bpy.props.EnumProperty(items = props_exportable_types)

# 2. trimesh writing settings (combined under an enum prop)

class aur_trimeshWriteSettings_(bpy.types.PropertyGroup): # TODO rework properties later to take less space in the code
	# contains the bool properties for 
	# the inputs that the user is wishing to bake
	write_normals:bpy.props.BoolProperty()
	write_binormals:bpy.props.BoolProperty()
	
class aur_trimeshEngineSettings_(bpy.types.PropertyGroup):
	# ammend others as they come !
	affected_by_wind:bpy.props.BoolProperty()

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# END PROPERTIES !!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!




# ##############################             ROOT CLASSES       ###########
# #########################################################################

class nodel:
	
	"""
		nodel represents an element of a node 
		the constructor sets the name and val attribute, and computes the retval
		if the retval cannot be computed, the NodelError type object is returned
		
		the text function produces a piece of text using the retval
		this piece of text contains the nodel name and value as a string
		the name must not be written separately
		
		for children classes, usually the get_retval method should be implemented
		the text method must be reimplemented as well
		
		for example, a nodel might be designed in such a way that it has a pointer
		to an object as a value and then computed the retval as an array of vertex indeces
		the text() function than writes the array as a string
	""" # rewrite documentation back to what it used to be
		
	def __init__(self, name, value, session):
		self.name = name
		self.value = value
		self.session = session
	
	def text(self): # dummy method, overload for child classes
		try:
			return self.name + " " + str(self.value) + "\n"
		except Exception as err:
			self.session.log.err("node " + self.name + " error: " + str(err))
			return self.name + " INVALID_VAL\n"
		
		
class node:
	
	"""
		the node is merely a collection of nodels.
		thanks to the fact that nodels all have the text() method, this class
		can afford to be contents-agnostic, i.e. it is just a container
		
		the class implements setitem and getitem methods.
		the class has an interface dictionary which defines simultanesously
		nodels allowed within the node and their default values and names
		only nodels present in the interface may be set or gotten
		Also, one is only allowed to set nodels to objects of the same class
		as the one declared in the interface
		the text method of the node merely calls the text() methods of members
		no functions of the node class are allowed to be reimplemented
		the interface variable needs to be redefined each time as instance variables!
		the interface and initialization must be defined in __init__ !
		if declared at the class level, the behvaior is undefined ...
		child nodes and different types of nodes are created by creating children
		of 'node' and setting the 'type' and 'interface' member variables
	"""
	
	name = 'dummy_name'
	type = 'dummy'
	
	#TODO why each time reset the name in the __init__ ? 
	#the name is shared by all isntances of a subclass ...
	
	def __init__(self, name, session):
		self.name = name
		self.data = ['Specify interface and initialization here when declaring children']
		self.session = session
	
	def __getitem__(self, key):
		if not key in self.data.keys():
			raise NameError('Node\'s interface does not contain this element')
			return
		else:
			return self.data[key]
	
	# TODO currently, the data can be changed directly from the code - need to prevent this ?
	# overwriting the nodel name is not allowed !!!
	def __setitem__(self, key, value):
		
		if not key in self.data.keys():
			raise NameError('Node\'s interface does not contain this element')
		else:
			proper_class = True
			if not value.__class__ == self.data[key].__class__:
				proper_class = False
			if not proper_class:
				raise NameError('Only nodel and its subclasses may be added to the node')
			else:
				if not key == value.name:
					raise NameError('Nodel name must correspond to the attribute name')
				else:
					self.data[key] = value
		
		
	def text(self, *argv):
	
		"""
			write whole node, or only some nodels (specify), or without 
			particular nodels (specify and supply '-' sign at the end)
		"""
		
		text = "node " + self.type + " " + self.name + "\n"
		if len(argv) == 0:
			# write all
			for x in self.data.keys():
				text = text + "    " + self.data[x].text()
		else:
			# exclue the nodels in argv?
			if argv[len(argv)-1] == '-':
				for x in self.data.keys():
					if not x in argv[0:(len(argv)-1)]:
						text = text + "    " + self.data[x].text()
			else:
				for x in argv:
					text = text + "    " + self.data[x].text()
		text = text + "endnode \n"
		return text	
		

class Djinni_exporter_session:
	
	"""
		a global exporting session!
	"""
	
	def __init__(self):
		self.exporters = []
		self.log = Log_()
	
	def _plcbl_prepare_folders(self, root_dir, object, overwrite):
	
	"""
		prepares the folder tree to export the object
	"""
	
		def get_folders(session, root_dir, object):
			try:
				os.mkdir(os.path.abspath(root_dir) + '\\' + object.name + '\\')
				os.mkdir(os.path.abspath(root_dir) + '\\' + object.name + '\\' + 'Textures' + '\\')
				return True
			except Exception as err:
				session.log.err("Error on create directories: " + str(err))
				return False
			
		try:
			if os.path.exists(os.path.abspath(root_dir) + '\\' + object.name + '\\'):
				if overwrite:
					sh.rmtree(os.path.abspath(root_dir) + '\\' + object.name + '\\') # removing works properly, creating new directory does not
					attempt = 0
					while (not get_folders(self, root_dir, object)) | (attempt > 100):
						attempt = attempt + 1
					if (attempt == 101):
						self.log.err("Could not create directories after 100 attempts, exiting")
						return False
					else:
						return True
				else:
					self.log.msg("This object already exists, with no overwrite specification. Skipping this one")
					return True
			else:
				return get_folders(self, root_dir, object)
		except Exception as err:
			self.log.err("Error occured while creating directories: " + str(err))
			return False
		return
		
	@classmethod
	def export_placeable(self):
		self.log.clear()
		return
	
	def __call__(self, objects):
	
		"""
			objects is a collection of any objects that can be exported by the exporter
			the exporting procedure is chosen according to type of the object to export
		"""
		
		root_dir = bpy.context.scene.world.aurora_wd
		
		for obj in objects:
			if obj.aur_exportableType == 'BASE':
				e = export_placeable()
				e(root_dir, obj, True) # overwrite for all, ammend later
				self.exporters.append(e)
		return
		
	def html_report(self):
		# loop over all the exporters in the collection and report them ! (each can return the html div element to use in the report)
		"""
		<!doctypeHTML>

		<head>
		</head>

		<body style="background-color:black">
		# here comes the stuff
		</body>
		"""
		
		# get the text of the html report
		htm_text = "<!doctypeHTML><head></head><body style=\"background-color:black\">"
		for exprter in self.exporters:
			htm_text = htm_text + exprter.report_html()
		htm_text = htm_text + "</body>"
		
		# write to the text file in the aurora directory
		aurora_dir = bpy.path.abspath(bpy.context.scene.world.aurora_wd)
		try:
			os.remove(os.path.abspath(aurora_dr) + '\\' + 'DjinniExport.html')
		except:
			pass
		f = open(os.path.abspath(aurora_dir) + '\\' + 'DjinniExport.html', 'w+')
		f.write(htm_text)
		f.close()
		
		# open with browser
		wb.open(os.path.abspath(aurora_dir) + '\\' + 'DjinniExport.html')
		
		# return
		return
		
		
	
# ###########################                 NODEL SUBCLASSES         #######
# ############################################################################

class nodel_lst(nodel):
	
	"""
		a node that contains a 1-dimensional list of values
	"""
	
	def text(self):
		try:
			text = self.name + " "
			for x in self.value:
				text = text + str(x) + " "
			text = text + "\n"
			return text
		except Exception as err:
			self.session.log.err("node " + self.name + " error: " + str(err))
			return self.name + " INVALID_VAL \n"
	
class nodel_mesh(nodel): # legacy nodel, is no longer used

	"""
		a node element that designates different types of meshes like verts etc.
	"""
	
	def text(self):
		try:
			text = self.name + " " + str(len(self.value)) + "\n"
			for x in self.value:
				text = text + "    "
				for y in x:
					text = text + str(y) + " "
				text = text + "\n"
			return text
		except:
			text = self.name + " INVALID_VAL \n"
			return text
	

class nodel_arraylike(nodel):

	"""
		this is a class from which to inherit, 
		it represents a nodel whose value is an array
		text method ideally should not be redefined 
	"""
	
	def _get_array(self): # overwrite this for children, DO NOT protect this against errors
		
		"""
			get the array of whatever it is
		"""
		return [[1,2],[2,4]]
		
	def text(self): # do not overwrite this
		try:
			arr = self._get_array()
			txt = self.name + ' ' + str(len(arr)) + '\n'
			for line_ in arr:
				txt = txt + "    "
				for l_ in line_:
					txt = txt + str(l_) + ' '
				txt = txt + '\n'
			return txt
		except Exception as err:
			self.session.log.err("node " + self.name + " error: " + str(err))
			return self.name + ' ERROR\n'
		return
		

class nodel_verts(nodel_arraylike):

	"""
		return the matrix with the vertices of the model ...
	"""
	def _get_array(self):
		if not type(self.value) == bpy.types.Object:
			self.session.log.err("node " + self.name + " error: cannot get vertices of a non-mesh " + self.value.name)
			return "ERROR"
		
		arr = []
		
		for v in self.value.data.vertices:
			arr.append([v.co.x, v.co.y, v.co.z])
			
		return arr


class nodel_faces(nodel_arraylike):
	
	"""
		return the matrix with face coordinates, smooth groups, and texture coordinates of a mesh
	"""
	
	def _get_array(self):
		if not type(self.value) == bpy.types.Object:
			self.session.log.err("node " + self.name + " error: cannot get faces of a non-mesh " + self.value.name)
			return "ERROR"
		
		arr = []
		
		for f in self.value.data.polygons:
			if (len(f.vertices) < 3) | (len(f.vertices) > 4):
				self.session.log.err("Bad geometry detected for object " + self.value.name)
				return "ERROR"
			elif (len(f.vertices) == 3):
				arr.append([f.vertices[0], f.vertices[1], f.vertices[2], 0, f.loop_indices[0], f.loop_indices[1], f.loop_indices[2], 1])
			else:
				arr.append([f.vertices[0], f.vertices[1], f.vertices[2], 0, f.loop_indices[0], f.loop_indices[1], f.loop_indices[2], 1])
				arr.append([f.vertices[2], f.vertices[3], f.vertices[0], 0, f.loop_indices[2], f.loop_indices[3], f.loop_indices[0], 1])
		
		return arr
		
		
class nodel_tverts(nodel_arraylike):
	
	"""
		returns texture vertices of an object
	"""
	
	def _get_array(self):
		arr = []
		
		if not type(self.value) == bpy.types.Object:
			self.session.log.err("Cannot get tverts of a non-mesh " + self.value.name)
			return "ERROR"
			
		uv_dat = self.value.data.uv_layers[0].data
		for l in self.value.data.loops:
			arr.append([uv_dat[l.index].uv.x, uv_dat[l.index].uv.y, 0])
			
		return arr


class nodel_materialdesc(nodel):
	
	"""
		this is a large node class that works with the material of an object
		THIS IS A SPECIAL CASE : not only writes text, but also keeps infos about the material, shaders, textures, etc.
	"""
	
	# this class is to amend in future
	
	# a collection of all known shaders
	SHADERS = ['selfilum_b', # selfillumination shader, emission shader in Blender
			   'norm_env_rim_1'] # unknown'
	
	TEXTURE_TYPES = ['tex', # unknown, seems like a simple texture
					 'ambOcclMap', # TODO
					 'envmap', # TODO
					 'texture_layer0'] # encountered this once in the selfilum_b shader
					 
	PARAMETER_TYPES = []
	
	"""
		will have the following instance-members:
			inapplicable - whether the material node is applicable or not
			shader_type - which shader type it has
			shader_node - is a pointer to the relevant shader node of the material
			textures - the dict with Blender image objects and texture types (these images can then be directly taken by Pillow and exported
	"""
	
	def _has_material(self):
		try:
			mat = self.value.material_slots[0].material
		except:
			if not ((self.value.aur_exportableType == 'SHADOW') | (self.value.aur_exportableType == 'PWK')):
				self.session.log.warn("Cannot get material of object " + self.value.name)
			return False
			
	def _get_shader_type(self):
		# if found the emission shader, then set accordingly
		# if principled BSDF connected, choose norm_env_rim_1 for now
		
		outp_node = matr.get_nodes_by_name(mat.node_tree.nodes, "Material Output")
		if len(outp_node) == 0:
			self.session.log.warn("No material output nodes found for object " + self.value.name ": this material will not be written")
			return False
		if len(outp_node) > 1:
			self.session.log.warn("Several output nodes detected for " + self.value.name + ": picking one randomly... ")
		try:
			shdr_node = outp_node[0].inputs['Surface'].links[0].from_node
		except:
			self.session.log.error("No shader input for the material output node in object " + self.value.name + ": this material will not be written")
			return False
		
		if shdr_node.type == 'EMISSION':
			self.shader_type = self.SHADERS[0]
			self.shader_node = shdr_node
			return True
		elif shdr_node.type == 'BSDF_PRINCIPLED':
			self.shader_type = self.SHADERS[1] # this is to be amended ...
			self.shader_node = shdr_node
			return True
		else:
			self.session.log.error("The shader type of object " + self.value.name + " cannot be exported")
			return False
		
	def __init__(self, name, value, session):
		# if it has material
			# if can detect shader
				# collect textures and parameter infos
			# send a warning to log and set necessary parameters for text generation
		# same as before, set self.inapplicable = True
		
		self.inapplicable = False
		self.shader_type = 'NA'
		self.shader_node = None
		self.textures = {}
		
		if self._has_material():
			if self._get_shader_type():
				# collect textures !
				
				
				if self.shader_type == self.SHADERS[0]: # emissive shader - selfilum_b # NOTE: this will fail if no texture inputs were found
					# here just have to collect all the actual images found ...
					try:
						img_clr = self.shader_node.inputs['Color'].links[0].from_node.image
					except:
						self.session.log.err("No color input for selfilum_b shader found for object " + self.value.name + ": this material will not be written")
						self.inapplicable = True
						return
					try:
						img_emis = self.shader_node.inputs['Strength'].links[0].from_node.image
					except:
						self.session.log.err("No emission strength input fro selfilum_b shader found for object " + self.value.name + ": this material will not be written")
						self.inapplicable = True
						return
					if img_clr == img_emis:
						self.textures['selfilum_both'] = img_clr # why texture_layer0 ??
					else:
						self.textures['selfilum_color'] = img_clr
						self.textures['selfilum_strength'] = img_emis
					
					
				elif self.shader_type == self.SHADERS[1]: # norm_env_rim_1 shader (?)
					
					# collect the textures of the principled bsdf node
					
					"""
						textures in this area:
							{tex} type - DXGI_FORMAT_BC1_UNORM - this is a texture with rgb channels only, specifying the color alone, with mipmaping possibly, up to 2Kx2K resolution, maybe more
							{bumpmap normalmap} type - DXGI_FORMAT_BC3_UNORM - a texture that bears normalmap color in rgb channels and specularity in the alpha channel!
							{ambOcclMap} type - DXGI_FORMAT_BC1_UNORM - just a black-and-white map - surprisingly, this has another uv_layout !!
							{texture envmap} type - 32bpp BGRA - this is a texture not only with mipmap levels but also with the frames ! perhaps for more realistic reflections
							
							the mess with ambOcclMap different coordinates is one big TODO! in the tent_ob there is a different set of texture coordinates present as well...
							so probably this one is exactly for the ambient occlusion map
							the question is then how the program knows which set of uv coordinates to use for which map!
							and god damn - it looks like this all happens by default because there are no additional infos in the .txi file...
					"""
					
					
				else:
					self.session.log.err("Shader type " + self.shader_type + " for object " + self.value.name + " has not been implemented yet! This material will not be written")
					self.inapplicable = True
					return
			else:
				self.inapplicable = True
		else:
			self.inapplicable = True
	
	
class nodel_textures(nodel):
	
	"""
		a node element that decides which texture info to write for the model
	"""
	
	def text(self):
		
		hasColorInput = False
		hasNormalInput = False
		
		try:
			dummy = self.value.material_slots[0].material.node_tree.nodes['Principled BSDF'].inputs['Base Color'].links[0].from_node.image.name
			hasColorInput = True
		except:
			pass
			
		try:
			textures['Normal'] = self.value.material_slots[0].material.node_tree.nodes['Principled BSDF'].inputs['Normal'].links[0].from_node.inputs['Color'].links[0].from_node.image.name
			hasNormalInput = False
		except:
			pass
			
		if hasColorInput & hasNormalInput:
			return 'TODO: color and normal textures'
		elif hasColorInput:
			return 'bitmap tex_' + self.value.name + '\n'
		elif hasNormalInput:
			return 'TODO: normal texture only'
		else:
			try:
				return 'bitmap dummytex_' + self.value.name + '\n'
			except: # this except must usually hapen for shadow and pwk objects
				return 'bitmap NULL\n'
	

class nodel_light_props(nodel):
	
	"""
		a nodel that collects and writes some light properties from the blender pointlight object
	"""
	
	def text(self):
		
		lght = self.value
		
		radius = lght.data.shadow_soft_size
		shadowradius = 0.0 # nor sure what exactly this represents
		multiplier = light.data.energy # this is in watts, have to translate to the djinni comparable units ! this must be easy to do by taking a reference light and calibrating !
		color = lght.data.color
		shadow = int(lght.data.use_shadow)
		shadow_intens = lght.data.shadow_buffer_soft # probably there is reversed proportional change there ...
		
		txt = "radius " + radius + "\n" + "shadowradius " + shadowradius + "\n" + "multiplier " + multiplier + "\n"
		txt = txt + "color " + color[0] + " " + color[1] + " " + color[2] + "\n" + "shadow " + shadow + "\n"
		txt = txt + "shadowintensity " + shadow_intens + "\n"
		
		return txt
	
# ###############################################         NODE SUBCLASSES         ######
# ######################################################################################
		
class node_light(node):

	type = 'light'
	
	def __init__(self, name, object):
		self.name = name
		self.object_ref = object
		self.data = {
			'parent':ifel(object.parent is None, nodel('parent', 'NULL'), nodel('parent', object.parent.name)),
			'position':nodel_lst('position', list(object.location)),
			'orientation':nodel_lst('orientation', [0.0, 0.0, 0.0]),
			'wirecolor':nodel_lst('wirecolor', [0.7, 0.7, 0.7]),
			'light_props':nodel_light_props('light_props', object),
			'ambientonly':nodel('ambientonly', 1), # amend later
			'prebaked_light':nodel('prebaked_light', 0),
			'lightpriority':nodel('lightpriority', 3),
			'lensflares':nodel('lensflares', 0),
			'fadingLight':nodel('fadingLight', 1),
			'fadingShadow':nodel('fadingShadow', 1),
			'walkmesh_light':nodel('walkmesh_light', 0),
			'walkmesh_intensity_threshold':nodel('walkmesh_intensity_threshold', 0.0),
			'walkmesh_intensity_multiplier':nodel('walkmesh_intensity_multiplier', 2.0),
			'nonmoving_light':nodel('nonmoving_light', 0)
		}
		
class node_trimesh(node):

    type = 'trimesh'

    def __init__(self, name, object):
		self.name = name
		self.object_ref = object
		self.data = {
			'parent':ifel(object.parent is None, nodel('parent', 'NULL'), nodel('parent', object.parent.name)),
			'position':nodel_lst('position', [0.0, 0.0, 0.0]),
			'orientation':nodel_lst('orientation', [0.000000, 0.000000, 0.000000, 0.000000]),
			'wirecolor':nodel_lst('wirecolor', [0.800000, 0.800000, 0.800000]),
			'lightmapped':nodel('lightmapped', 0),
			'daynightlightmaps':nodel('daynightlightmaps', 0),
			# the daynighttransitionstring is wrong, everything is mixed up
			'daynighttransitionstring':nodel('daynighttransitionstring', '6:00-%s!n;7:00-%s!r;8:00-%s!r;9:00-%s!p;18:00-%s!p;19:00-%s!w;20:00-%s!w;21:00-%s!n'),
			'danglymesh':nodel('danglymesh', 0),
			'period':nodel('period', 1.000000),
			'tightness':nodel('tightness', 1.000000),
			'displacement':nodel('displacement', 0.025000),
			'showdispl':nodel('showdispl', 1),
			'displtype':nodel('displtype', 1),
			'detail_map_scale':nodel('detail_map_scale', 6.0),
			'alpha':nodel('alpha', 1.000000),
			'tilefade':nodel('tilefade', 0),
			'scale':nodel('scale', 1.000000),
			'render':ifel((object.aur_exportableType == 'PWK') | (object.aur_exportableType == 'SHADOW'), nodel('render', 0), nodel('render', 1)),
			'shadow':ifel(object.aur_exportableType == 'SHADOW', nodel('shadow', 1), nodel('shadow', 0)),
			'beaming':nodel('beaming', 0),
			'inheritcolor':nodel('inheritcolor', 0),
			'selfillumcolor':nodel_lst('selfillumcolor', [0.000000, 0.000000, 0.000000]),
			'rotatetexture':nodel('rotatetexture', 0),
			'texture_trans_rot':nodel_lst('texture_trans_rot', [0.500000, 0.500000, 0.500000]),
			'transparencyhint':nodel('transparencyhint', 0),
			'transparency_shift':nodel('transparency_shift', 0.000000),
			'default_renderlist':nodel('default_renderlist', 1),
			'preserve_vcolors':nodel('preserve_vcolors', 0),
			'list_fourcc':nodel('list_fourcc', 'OPQE'),
			'depth_offset':nodel('depth_offset', 0.000000),
			'corona_center_mult':nodel('corona_center_mult', 1.000000),
			'fading_start_distance':nodel('fading_start_distance', 0.000000),
			'enlarge_start_distance':nodel('enlarge_start_distance', 20.000000),
			'dist_from_screen_center_fade':nodel('dist_from_screen_center_fade', 0),
			'affected_by_wind':ifel(object.aur_trimeshEngineSettings.affected_by_wind, nodel('affected_by_wind', 1), nodel('affected_by_wind', 0)),
			'damp_factor':nodel('damp_factor', 0.000000),
			'blend_group':nodel('blend_group', 0),
			'impostor_group':nodel('impostor_group', -1),
			'ignore_hitcheck':nodel('ignore_hitcheck', 0),
			'fade_on_camera_collision':nodel('fade_on_camera_collision', 0), 
			'lightmap_name':nodel('lightmap_name', ''),
			'no_selfshadow':nodel('no_selfshadow', 1),
			'controllable_fade':nodel('controllable_fade', 0),
			'is_reflected':nodel('is_reflected', 1),
			'only_reflected':nodel('only_reflected', 0),
			'volfogscale':nodel('volfogscale', 0.000000),
			'can_decal':nodel('can_decal', 1),
			'multibillboard':nodel('multibillboard', 0),
			'minLOD':nodel('minLOD', -1),
			'maxLOD':nodel('maxLOD', -1),
			'ignore_LOD_in_reflections':nodel('ignore_LOD_in_reflections', 0),
			'ambient':nodel_lst('ambient', [1.000000, 1.000000, 1.000000]),
			'diffuse':nodel_lst('diffuse', [1.000000, 1.000000, 1.000000]),
			'specular':nodel_lst('specular', [0.000000, 0.000000, 0.000000]),
			'shininess':nodel('shininess', 1.1),
			'texture_data':nodel_textures('texture_data', object), 
			'verts':nodel_verts('verts', object),
			'faces':nodel_faces('faces', object),
			'tverts':nodel_tverts('tverts', object)
		}
		
class node_dummy(node):
		
	type = 'dummy'
	
	def __init__(self, name):
		self.name = name
		self.data = {
				 'parent':nodel('parent', 'NULL'),
				 'position':nodel_lst('position', [0.000, 0.000, 0.000]),
				 'orientation':nodel_lst('orientation', [0.000000, 0.000000, 0.000000, 0.000000]),
				 'wirecolor':nodel_lst('wirecolor', [0.600000, 0.600000, 0.600000])
		}


# #############################         SUBROUTINES           #################
# #############################################################################


			
	
	
class export_mdl(subroutine):

	"""
		exports (writes) the .mdl file, it only operates on an 'Aurora Base' object 
	"""
	
	def get_mesh_text(self, object):
		"""
			gets text for a trimesh node
		"""
		try:
			trimesh_nd = node_trimesh(object.name, object)
			txt = trimesh_nd.text()
		except Exception as err:
			self.errors.append("error in " + object.name + " while getting trimesh node:" + str(err))
			self.success = False
			return
		if not (len(trimesh_nd.get_errors()) == 0):
			self.errors.append(trimesh_nd.get_errors())
			self.success = False
			return
		return txt
		
	def get_shadow_text(self, object):
		"""
			gets the text if this is a shadow node!
		"""
		try:
			shdw_trimesh = node_trimesh(object.name + '_shadow', object) # TODO ammend later when writing for multiple objects !
			txt = shdw_trimesh.text('tverts', 'normals', 'binormals', 'tangents', '-') # does not fail even if some of the nodels are not there yet !
		except Exception as err:
			self.errors.append("error while writing shadow node " + object.name + ": " + str(err))
			self.success = False
			return
		if not (len(txt.get_errors()) == 0):
			self.errors.append(shdw_trimesh.get_errors())
			self.success = False
			return
		return txt
		
	def get_light_node_text(self, object):
		"""
			gets the text for the light node
		"""
		try:
			node_lght = node_light(object.name, object)
			txt = node_lght.text()
		except Exception as err:
			self.errors.append("error while writing light node for " + object.name + ": " + str(err))
			self.success = False
			return
		return txt
		
	def __call__(self, object, root_folder):
		
		try:
			main_output = open(os.path.abspath(root_folder) + '\\' + object.name + '\\' + object.name + '.mdl', 'w+') # TODO naming rules ? 
		except Exception as err:
			self.errors.append(err)
			self.success = False
			return
			
		main_output.write(EXPORTER_INTRO)
		
		# WRITE NODES !
		
		# TODO do not write the texture if it's not there !!! might be that it leads to crash of Djinni
		# TODO do not write parent when there is none! leads to crashes ...
		main_output.write(nodel('filedependancy', 'NULL').text())
		main_output.write(nodel('newmodel', object.name).text())
		main_output.write(nodel_lst('setsupermodel', [object.name, 'NULL']).text())
		main_output.write(nodel('classification', 'Item').text())
		main_output.write(nodel('setdetailmap', '100_detailmap').text())
		main_output.write(nodel('placeholder', 1).text())
		main_output.write(nodel('renderModelCoherrently', 0).text())
		main_output.write(nodel('forceDontUseWalkmeshLighting', 0).text())
		main_output.write(nodel('forceDontUseStaticLights', 0).text())
		main_output.write(nodel('firstLODdistance', -1.0).text())
		main_output.write(nodel('lastLODdistance', -1.0).text())
		main_output.write(nodel('beginmodelgeom', object.name).text())
		
		# --- ! dummy node !
		dummynode_main = node_dummy(object.name)
		main_output.write(dummynode_main.text('parent'))
		
		# get all children of the base, loop through them, and add text depending on the type of the children and other settings ...
		all_children = miscf.get_all_children(object)
		
		if len(all_children) == 0:
			self.errors.append("the base object has no children! exiting")
			self.success = False
			return
			
		for ch in all_children:
			if ch.aur_exportableType == 'TRIMESH':
				main_output.write(self.get_mesh_text(object))
			elif ch.aur_exportableType == 'PWK':
				pass # pwk is written in another procedure
			elif ch.aur_exportableType == 'SHADOW':
				main_output.write(self.get_shadow_text(object))
			elif ch.aur_exportableType == 'BASE':
				self.errors.append("Base objects cannot be parented to other base objects: exiting now")
				self.success = False
				return
			elif ch.aur_exportableType == 'LIGHT':
				main_output.write(self.get_light_node_text(object))
				pass
			else
				self.warnings.append("Unrecognized aurora exportable type in object " + ch.name + ": ignoring")
		
		main_output.write(nodel('endmodelgeom', object.name).text())
		main_output.write(nodel('donemodel', object.name).text())
		
		main_output.close()
		
		self.success = True
		return

		
class export_pwk(subroutine):
	
	"""
		a subroutine that exports the pwk file !
	"""
	
	def __call__(self, object, root_dir):
		
		# OPEN THE PWK STREAM
		try:
			pwk_output = open(os.path.abspath(root_dir) + '\\' + object.name + '\\' + object.name + '.pwk', 'w+')
		except Exception as err:
			self.errors.append('Could not open file stream: ' + err)
			self.success = False
			return
		
		# WRITE
		pwk_dummynode = node_dummy(object.name + '_pwk')
		pwk_dummynode['parent'].value = object.name
		pwk_output.write(EXPORTER_INTRO)
		pwk_output.write(nodel('filedependancy', 'NULL').text())
		pwk_output.write(pwk_dummynode.text())
		
		all_children = miscf.get_all_children(object)
		for ch in all_children:
			if ch.aur_exportableType == 'PWK':
				try:
					pwk_trimeshnode = node_trimesh(ch.name)
					pwk_trimeshnode['parent'].value = object.name + '_pwk'
					pwk_trimeshnode['verts'].value = pwk_trimeshnode['faces'].value = ch
					txt = pwk_trimeshnode.text('parent', 'position', 'orientation', 'wirecolor', 'texture_data', 'verts', 'faces')
				except Exception as err:
					self.errors.append("error while writing pwk node for pwk object " + ch.name + ": " + str(err))
					self.success = False
					return
				if not (len(pwk_trimeshnode.get_errors()) == 0):
					self.errors.append(pwk_trimeshnode.get_errors())
					self.success = False
					return
				else:
					pwk_output.write(txt)
					
		pwk_output.close()
		
		self.success = True
		return
	
		
class export_textures(subroutine):

	"""
		exports textures belonging to the object ! 
	"""
	
	def __call__(self, object, root_dir):
		all_children = miscf.get_all_children(object)
		for ch in all_children:
			if ch.aur_exportableType == 'TRIMESH':
				get_and_save_textures(object, root_dir)
		return True
		
	def get_and_save_textures(self, object, root_dir):
		
		textures = {}
	
		# TRY TO FIND THE DIRECTORY WHERE TO SAVE TO
		try:
			save_path = os.path.abspath(root_dir) + '\\' + object.name + '\\Textures\\'
		except Exception as err:
			self.errors.append(err)
			self.success = False
			return
			
		# COLLECT ALL THE TEXTURES AS A COLLECTION OF PILLOW IMAGES !
		for input_name in ['Base Color', 'Specular']:
			try:
				textures[input_name] = pillowimage.open(bpy.path.abspath(object.material_slots[0].material.node_tree.nodes['Principled BSDF'].inputs[input_name].links[0].from_node.image.filepath))
			except:
				pass
		try:
			textures['Normal'] = pillowimage.open(bpy.path.abspath(object.material_slots[0].material.node_tree.nodes['Principled BSDF'].inputs['Normal'].links[0].from_node.inputs['Color'].links[0].from_node.image.filepath))
		except:
			pass	
			
		# IF NO TEXTURES FOUND, CREATE ONE
		# TODO if, instead of the textures, values are specified, this needs to get appropriate treatment
		if len(textures) == 0: # TODO return some exports codes/reports instead
			# create a simple grey texture to give the object some color
			try:
				dummy_img = pillowimage.new('RGBA', (512, 512))
				for wdt in range(0, 512):
					for hgt in range(0, 512):
						dummy_img.putpixel((wdt, hgt), (180, 180, 180, 250)) #TODO replace 
						# the grey color with user choice
				dummy_img.save(save_path + 'dummytex_' + object.name + '.tga')
				self.success = True
				self.messages.append('No textures to export, exported a dummy texture')
				return
			except:
				self.success = True
				self.warnings.append('Attempted to save a duumy texture and failed. No textures exported')
				return
		
		# IMAGES HAVE EQUAL SIZE ?
		have_equal_size = True
		for tex_name in textures:
			for tex_name2 in textures:
				if not textures[tex_name].size == textures[tex_name2].size:
					have_equal_size = False			
		if not have_equal_size:
			self.errors.append('Textures of different proportions. Canno export')
			self.success = False
			return
		
		
		# CROP IMAGES IF WRONG SIZE 
		# if want to crop, then have to crop in acceptable sizes like 512x512 and not 375x375
		for kkey in textures:
			if not (textures[kkey].size[0] == textures[kkey].size[1]):
				# try to crop
				try:
					max_dim = min(textures[kkey].width, textures[kkey].height)-1
					textures[kkey] = textures[kkey].crop((0, 0, max_dim, max_dim))
					self.warnings.append('Texture ' + kkey + ' of invalid size! Succesfully cropped')
				except Exception as err:
					self.warnings.append('Attempt to crop a texture, failed with message: ' + str(err))
			else:
				# pass
				pass
		
		
		# SAVE IMAGES AS TGA TO THE OBJECT FOLDER !
		# TODO needs to check whether the specularity is already packed together in the normal map
		if textures.get('Base Color', 'noVal') == 'noVal':
			self.messages.append('No color texture found')
		else:
			try:
					textures['Base Color'].save(save_path + 'tex_' + object.name + '.tga')
			except Exception as err:
				self.errors.append('could not save color texture: ' + err)
		if (not textures.get('Normal', 'noVal') == 'noVal') & (not textures.get('Specular', 'noVal') == 'noVal'):
			# both normal and specular there, pack together!
			try:
				textures['Normal'].putalpha(textures['Specular'].getchannel(0))
				textures['Normal'].save(save_path + 'ntex_' + object.name + '.tga')
				self.messages.append('Succesfully packed specularity into normal and exported')
			except Exception as err:
				self.errors.append('Error when trying to pack and export normals and specularity')
		# only one of them present, or none
		if (textures.get('Normal', 'noVal') == 'noVal') & (textures.get('Specular', 'noVal') == 'noVal'):
			self.messages.append('Neither normals, nor specularity found, exiting!')
			self.success = True
			return
		if not textures.get('Specular', 'noVal') == 'noVal':
			self.warnings.append('Cannot write specularity separately, reconsider!')
		if not textures.get('Normal', 'noVal') == 'noVal':
			try:
				textures['Normal'].save(save_path + 'ntex_' + object.name + '.tga')
				self.messages.append('No specularity found, succesfully saved normals')
				self.success = True
				return
			except Exception as err:
				self.errors.append('Cannot save normal map: ' + err)
				return
				
		# case if one of the branches could not resolve - set to success = True and exit
		self.success = True
		return

		
# ######################################################         EXPORTERS     #######
# ####################################################################################

class export_placeable(exporter):
	
	""" 
		a child class that implements export of an elementary placeable object
	"""
	
	def write_meta(self):
		return 'Placealbe EXPORT: ' + 'Stone' + '\n' # TODO some quick summary on the export
		
	def __init__(self):
		# fill with the subroutine function-like objects ! 
		self.subroutines = {
			'Prepare folders':_plcbl_prepare_folders(), # initializes the subroutine object which can then be called as a function
			'Export .mdl':export_mdl(),
			'Export .pwk':export_pwk(),
			'Export textures':export_textures()
		}
	
	def html_report_header(self):
		"""
			a header that will be used in the html to print infos about the exporter
		"""
		# example html
		"""
			<p style="padding-left:50px">
				<a style="background-color:deeppink;padding-left:5px;padding-right:5px;color:white">PLACEABLE EXPORT</a>
				<a style="padding-left:10px;padding-right:10px"></a> <!--just a black box-->
				<a style="background-color:white;padding-left:10px;padding-right:10px"></a> <!--just a white box-->
				<a style="padding-left:10px;padding-right:10px"></a> <!--a black box again ...-->
				<a style="color:white">Cube</a>
				<a style="padding-left:10px;padding-right:10px"></a> <!--a black box again ...-->
				<a style="background-color:white;padding-left:10px;padding-right:10px"></a> <!--just a white box-->
				<a style="padding-left:10px;padding-right:10px"></a> <!--a black box again ...-->
				<a style="background-color:greenyellow;padding-left:5px;padding-right:5px">SUCCESS</a>
			</p>
		"""
		BLACK_BOX_htm = "<a style=\"padding-left:10px;padding-right:10px\"></a>"
		WHITE_BOX_htm = "<a style=\"background-color:white;padding-left:10px;padding-right:10px\"></a>"
		
		htm_export = htm.enclose('a', 'PLACEABLE EXPORT', {'style':'background-color:deeppink;padding-left:5px;padding-right:5px;color:white'})
		htm_export = htm_export + BLACK_BOX_htm + WHITE_BOX_htm + BLACK_BOX_htm
		htm_export = htm_export + htm.enclose('a', self.object.name, {'style':'color:white'}) + BLACK_BOX_htm + WHITE_BOX_htm + BLACK_BOX_htm
		
		# if all subroutines returned 'Done', that set to 'Done' as well ...
		exported_successfully = True
		for subr_name in self.subroutines:
			if len(self.subroutines[subr_name].errors) != 0:
				exported_successfully = False
				
		if exported_successfully:
			htm_export = htm_export + htm.enclose('a', 'DONE', {'style':'background-color:greenyellow;padding-left:5px;padding-right:5px'})
		else:
			htm_export = htm_export + htm.enclose('a', 'FAILED', {'style':'background-color:red;padding-left:5px;padding-right:5px'})
		
		htm_export = htm.enclose('p', htm_export, {'style':'padding-left:50px'})
		
		return htm_export	
		
		
	def __call__(self, root_dir, object, overwrite):
		# basically, no need to check whether object is base if chosen properly beforehand ... or ?
		self.object = object
		sr = self.subroutines
		sr['Prepare folders'](root_dir, object, overwrite)
		if sr['Prepare folders'].success:
			sr['Export .mdl'](object, root_dir)
			sr['Export .pwk'](object, root_dir)
			sr['Export textures'](object, root_dir)
			self.success = ((sr['Export .mdl'].success == True) & (sr['Export .pwk'].success == True) & (sr['Export textures'].success == True))
			return
		else:
			self.success = False
			return
	

# ###############
# MAIN PROCEDURES
# ###############

def DJINNI_EXPORT():
	"""
		this is just a wrapper function that is used to save place in the operator code
	"""
	
	s = Djinni_exporter_session()
	s(bpy.context.selected_objects)
	s.html_report()
	return
	
	
def convert_to_aurora_errors(object):
	""" 
		This function checks if there are potential erros on conversion of the geometry to an aurora exportable
	"""
	if not object.type == 'MESH':
		return True
	
	# check that there is no name overwriting by the exporter
	for ob in bpy.data.objects:
		if ((ob.name == (object.name + "_shdw")) | (ob.name == (object.name + "_pwk"))):
			return True
	
	return False	
	

def geometry_to_Item(object):
	"""
		Converts a piece of geometry to a D'jinni item preset
	"""
	# create a preset for a shadow and pwk (TODO: later, let the user choose between the types of gizmo (cube, sphere, cylinder etc.)
	# 1. get the mesh extrema
	x_, x, y_, y, z_, z = miscf.get_mesh_extrema(object)
	# 2. construct the vertices from the extrema
	v = [(x, y, z),
		 (x_, y_, z_),
		 (x, y, z_),
		 (x, y_, z),
		 (x_, y, z),
		 (x_, y_, z),
		 (x, y_, z_),
		 (x_, y, z_)]
	# 3. construct the parallelepiped from the extrema
	f = [(7, 4, 0, 2),
		 (0, 2, 6, 3),
		 (4, 7, 1, 5),
		 (3, 6, 1, 5),
		 (0, 4, 5, 3),
		 (2, 7, 1, 6)
		 ]
		 
	mesh = bpy.data.meshes.new(name = object.name + '_aux_mesh')
	mesh.from_pydata(v, [], f)
	
	shdw = bpy.data.objects.new(object.name + '_shdw', mesh)
	pwk = bpy.data.objects.new(object.name + '_pwk', mesh)
	
	mesh.update(calc_edges = True)

	bpy.context.collection.objects.link(shdw)
	bpy.context.collection.objects.link(pwk)
	
	# 4. place the objects, affect viewport display type
	print('check')
	shdw.location = (0.0, 0.0, 0.0)
	pwk.location = (0.0, 0.0, 0.0)
	shdw.parent = object
	pwk.parent = object
	shdw.display_type = 'WIRE'
	pwk.display_type = 'WIRE'
	
	object.is_aurora_item = True
	
	return
	
	
########################## ---------- !!!!!!!!!!!!!!

# GUI

######################### ----------- !!!!!!!!!!!!!!

class AURORA_PT_0(bpy.types.Panel):
	bl_idname = "AURORA_PT_0"
	bl_label = "Aurora Exporter"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'object'

	@classmethod
	def poll(self, context): # any conditions here ?
		return True

	def draw(self, context):
		layout = self.layout
		columns = layout.column()
		activeObject = bpy.context.object
		columns.label(text = "General properties")
		# TODO improve the panel appearance here
		# TODO reset the property from the 'world' to a more general category
		columns.prop(context.scene.world, "aurora_wd", text = "Aurora working directory")
		columns.operator("aurora.geometry_to_item", text = 'Geometry to Aurora Item')
		

		
class AURORA_PT_0_general_settings(bpy.types.Panel):
	bl_idname = "AURORA_PT_0_general_settings"
	bl_label = "General"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_parent_id = 'AURORA_PT_0'
	bl_context = 'object'
	
	@classmethod
	def poll(self, context):
		return True
		
	def draw(self, context):
		layout = self.layout
		columns = layout.column()
		columns.prop(context.active_object, "aur_exportableType", expand=True)
		

# spawn the trimesh settings here ! # and don't forget to register the new panel class afterwards !
class AURORA_PT_0_trimesh_settings(bpy.types.Panel):
	bl_idname = "AURORA_PT_0_trimesh_settings"
	bl_label = "Trimesh"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_parent_id = 'AURORA_PT_0'
	bl_context = 'object'
	
	@classmethod
	def poll(self, context):
		return True
		
	def draw(self, context):
		layout = self.layout
		# this would be two rows in the layour, each having a box
		eng_settings_row = layout.row() # engine settings
		write_settings_row = layout.row() # writing settings
		eng_settings_box = eng_settings_row.box()
		write_settings_box = write_settings_row.box()
		eng_settings_box.prop(context.active_object.aur_trimeshEngineSettings, "affected_by_wind", text = "Affected by wind")
		write_settings_box.prop(context.active_object.aur_trimeshWriteSettings, "write_normals", text = "Write normals")
		write_settings_box.prop(context.active_object.aur_trimeshWriteSettings, "write_binormals", text = "Write binormals")
		
		
class AURORA_PT_0_export_placeable(bpy.types.Panel):
	bl_idname = "AURORA_PT_0_export_placeable"
	bl_label = "Actions"
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_parent_id = 'AURORA_PT_0'
	bl_context = 'object'
	
	@classmethod
	def poll(self, context):
		return True
		
	def draw(self, context):
		layout = self.layout
		col = layout.column()
		col.operator("aurora.export_placeable", text = "Export placeable item")
		


		
########################## ---------- !!!!!!!!!!!!!!

# OPERATORS (ACTIONS)

######################### ----------- !!!!!!!!!!!!!!


class AURORA_GEOMTOITEM_OT_0(bpy.types.Operator):
    
	bl_idname = "aurora.geometry_to_item"
	bl_label = "Convert geometry to an Aurora exportable item"

	def invoke(self, context, event):
		if convert_to_aurora_errors(context.active_object):
			self.report({'INFO'}, "Naming or type error, check documentation")
			return {'CANCELLED'}
		return self.execute(context)

	def execute(self, context):
		geometry_to_Item(context.active_object)
		return {'FINISHED'}
		
		
class AURORA_EXPORTAURPLACEABLE_OT_0(bpy.types.Operator):
	
	bl_idname = "aurora.export_placeable"
	bl_label = "Export to Aurora placeable"
	
	def invoke(self, context, event):
		if context.scene.world.aurora_wd == "":
			self.report({'INFO'}, "Aurora working directory not set! Cannot proceed")
			return {'CANCELLED'}
		if context.active_object.is_aurora_item == False:
			self.report({'INFO'}, "The object is not an Aurora item")
			return {'CANCELLED'}
		return self.execute(context)
		
	def execute(self, context):
		DJINNI_EXPORT()
		return {'FINISHED'}

		
		
######## ---> REGISTER THE MODULE
		
def register_props():
		# clean up images on finish or not (only can be set if previous is true)
	bpy.types.Object.is_aurora_item = bpy.props.BoolProperty(description = \
					"""Is this object an aurora item?""") # this property is const safe, is set only by invoking the operators of the exporter
	bpy.types.World.aurora_wd = bpy.props.StringProperty(description = "Working directory of the Aurora Exporter", default = "", subtype = 'DIR_PATH')
	bpy.types.Object.aur_exportableType = aur_exportableType_
	
	# the trimesh group properties (require registering additional classes)
	bpy.utils.register_class(aur_trimeshEngineSettings_)
	bpy.utils.register_class(aur_trimeshWriteSettings_)
	bpy.types.Object.aur_trimeshEngineSettings = bpy.props.PointerProperty(type = aur_trimeshEngineSettings_) 
	bpy.types.Object.aur_trimeshWriteSettings = bpy.props.PointerProperty(type = aur_trimeshWriteSettings_)
	
					
def unregister_props():
	del bpy.types.Object.is_aurora_item
	del bpy.types.World.aurora_wd
	del bpy.types.Object.aur_exportableType
	
	# unregister the trimesh group properties
	del bpy.types.Object.aur_trimeshEngineSettings
	del bpy.types.Object.aur_trimeshWriteSettings
	bpy.utils.unregister_class(aur_trimeshEngineSettings_)
	bpy.utils.unregister_class(aur_trimeshWriteSettings_)
	
	
def register_operators():
	bpy.utils.register_class(AURORA_GEOMTOITEM_OT_0)
	bpy.utils.register_class(AURORA_EXPORTAURPLACEABLE_OT_0)

def unregister_operators():
	bpy.utils.unregister_class(AURORA_GEOMTOITEM_OT_0)
	bpy.utils.unregister_class(AURORA_EXPORTAURPLACEABLE_OT_0)

def register_ui_panels():
	bpy.utils.register_class(AURORA_PT_0)
	bpy.utils.register_class(AURORA_PT_0_general_settings)
	bpy.utils.register_class(AURORA_PT_0_export_placeable)
	bpy.utils.register_class(AURORA_PT_0_trimesh_settings)
	

def unregister_ui_panels():
	bpy.utils.unregister_class(AURORA_PT_0)
	bpy.utils.unregister_class(AURORA_PT_0_general_settings)
	bpy.utils.unregister_class(AURORA_PT_0_export_placeable)
	bpy.utils.unregister_class(AURORA_PT_0_trimesh_settings)
	
def register():
	"""
		register the workdir property, the panel, and 
		the operator to open the working directory
	"""
	register_props()
	register_operators()
	register_ui_panels()

def unregister():
	""" unregister the workdir property, the panel, and
		the operator to opne the working directory
	"""
	unregister_props()
	unregister_operators()
	unregister_ui_panels()
