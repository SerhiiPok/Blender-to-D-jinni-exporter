############################################################################
############################################################################
############################################################################
######################## CONTAINS MISC FUNCTIONS  ##########################
############################################################################
############################################################################
############################################################################

import bpy 
import os
import re


def format_folder_path(str_path):
            """
                appends \\ at the end
            """
            
            # check that the path ends properly
            if re.search('.*\\\\$', str_path) is None:
                return str_path + '\\'
            else:
                return str_path
   
def is_relative_path(str_path):
    """
        returns True for a relative path
    """
    if str_path[:2] == '//':
        return True
    pass

def set_obj_select_active(object):
    """
        Deselects all the objects in the scene and selects the given object
    """

    for obj in bpy.context.scene.objects:
        if obj == object:
            obj.select_set(True)
        else:
            obj.select_set(False)
    bpy.context.view_layer.objects.active = object

def get_geometry_origin_co(object):
    """
        Returns x, y, z coordinates of the origin of geometry
    """

    # a bad solution! there must be another way to arrive at the origin of an object
    curs_loc = bpy.context.scene.cursor.location
    miscf.set_obj_select_active(object)
    bpy.ops.view3d.snap_cursor_to_active()
    # get the position of the cursor
    return curs_loc.x, curs_loc.y, curs_loc.z

def move_origin_to(object, coordinates):
    """
        Moves origin of geometry to a prespecified point
    """
    # move the cursor to the coordinates
    curs = bpy.context.scene.cursor
    curs.location.x, curs.location.y, curs.location.z = coordinates[0], coordinates[1], coordinates[2]
    # move origin to the cursor
    bpy.ops.object.origin_set(type = 'ORIGIN_CURSOR')

def read_text(path):
    """
        A simplifier function.Returns lines of a text file as a list, given the path to the file
    """
    file = open(path, 'r')
    file.seek(0)
    lines = file.readlines()
    file.close()
    return lines

def get_from_config(key):
    """
        gets a value of the key from the config file, returns None if the key wasn't found
    """
    filepath = format_folder_path(os.path.dirname(__file__))
    filepath = filepath + 'config.txt'
    text = read_text(filepath)
    for line in text:
        if line[0:len(key)] == key:
            return line[len(key)+1:].strip()
    return None

def UI_report_start(message, space_type, position = (15, 30), color = (0.8, 0.8, 0.8, 1.0)):


    """
        draws specified message, in the specified space_type. space_type is a value in:
            
        ['Image Editor',
        'Node Editor',
        'UV Editor', 
        '3D View']

        returns the draw handler and the space type
 for later deletion
    """

    try:
        blf
    except:
        import blf

    def draw_message(self, context):
        blf.position(0, position[0], position[1], 0)
        blf.size(0, 20, 72)
        blf.color(0, color[0], color[1], color[2], color[3])
        blf.draw(0, message)

    if space_type == 'Image Editor':
        handler = bpy.types.SpaceImageEditor.draw_handler_add(draw_message, (None, None), 'WINDOW', 'POST_PIXEL')
        return handler, space_type
    elif space_type == 'Node Editor':
        handler = bpy.types.SpaceNodeEditor.draw_handler_add(draw_message, (None, None), 'WINDOW', 'POST_PIXEL')
        print(message)
        print('succesfully started the new reporter')
        return handler, space_type
    elif space_type == '3D View':
        handler = bpy.types.SpaceView3D.draw_handler_add(draw_message, (None, None), 'WINDOW', 'POST_PIXEL')
        return handler, space_type
    elif space_type == 'UV Editor':
        handler = bpy.types.SpaceUVEditor.draw_handler_add(draw_message, (None, None), 'WINDOW', 'POST_PIXEL')
        return handler, space_type
    else:
        raise Exception('UI_report_start', 'Incorrect Window type specified')
    print('succesfully started the new UI reporter')

def UI_report_stop(reporter, space_type):
    """
        stops drawing the report
        the drawing handler and the space type must be input
    """

    if space_type == 'Image Editor':
        bpy.types.SpaceImageEditor.draw_handler_remove(reporter, 'WINDOW')
    elif space_type == 'Node Editor':
        bpy.types.SpaceNodeEditor.draw_handler_remove(reporter, 'WINDOW')
    elif space_type == '3D View':
        bpy.types.SpaceView3D.draw_handler_remove(reporter, 'WINDOW')
    elif space_type == 'UV Editor':
        bpy.types.SpaceUVEditor.draw_handler_remove(reporter, 'WINDOW')
    else:
        raise Exception('UI_report_stop', 'Incorrect Window type specified')
    print('succesfully stopped the reporter')

def scr_redraw():
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=3)
    print('succesfully redrawn')
    return # TODO <--- this is NOT robust: ammend and replace later

def cons_safe_toggle():
                try:
                    bpy.ops.wm.console_toggle()
                except:
                    pass
                return

def cons_report(msg):
    print(msg)
    return


def get_construct_cube(radius, position):
	"""
		Construct and place a cube into the scene, returns the cube
	"""
	v, f = get_cube_data(radius)
	mesh = bpy.data.meshes.new(name = 'mesh_instance')
	obj = bpy.data.objects.new('obj_instance', mesh)
	
	mesh.from_pydata(v, [], f)
	mesh.update(calc_edges = True)
        
	bpy.context.collection.objects.link(obj)
        
	return obj
	
	
def get_cube_data(radius):
	"""
		Returns the vector of vertices, and then the vector of faces
	"""
	r = radius
	verts = [(r, r, -r),
			 (r, -r, r),
			 (-r, r, r),
			 (r, r, r),
			 (-r, -r, -r),
			 (-r, -r, r),
			 (r, -r, -r),
			 (-r, r, -r)]
	faces = [(0, 1, 3),
			 (0, 1, 6),
			 (0, 7, 2),
			 (0, 2, 3),
			 (2, 3, 5),
			 (3, 1, 5),
			 (4, 5, 6),
			 (5, 1, 6),
			 (0, 4, 7),
			 (0, 4, 6),
			 (2, 4, 7),
			 (2, 4, 5)]
			 
	return verts, faces
	
	
def get_mesh_extrema(object):
	"""
		Get the extrema of the mesh along the axes x, y, z (returns 6 extrema: x_min, x_max, y_min, y_max, z_min, z_max)
	"""
	v = object.data.vertices
	
	x_min, x_max = v[0].co[0], v[0].co[0]
	y_min, y_max = v[0].co[1], v[0].co[1]
	z_min, z_max = v[0].co[2], v[0].co[2]
	
	for vertex in v:
		if vertex.co[0] < x_min:
			x_min = vertex.co[0]
		if vertex.co[0] > x_max:
			x_max = vertex.co[0]
		if vertex.co[1] < y_min:
			y_min = vertex.co[1]
		if vertex.co[1] > y_max:
			y_max = vertex.co[1]
		if vertex.co[2] < z_min:
			z_min = vertex.co[2]
		if vertex.co[2] > z_max:
			z_max = vertex.co[2]
	
	return x_min, x_max, y_min, y_max, z_min, z_max
	
	
def get_object_vertices(object):
	"""
		returns a 2d matrix of the vertex coordinates
	"""
	i = 0
	for v in object.data.vertices:
		verts[i] = [v.co.x, v.co.y, v.co.z]
		i = i + 1
	return verts