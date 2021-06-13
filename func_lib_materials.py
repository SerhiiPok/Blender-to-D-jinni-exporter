"""
    MISCELLANEOUS FUNCTION HELPERS FOR MATERIALS
"""

import bpy
import os

OUT_OF_RANGE = -1

def get_socket_index(socket, node):
    """
        find the index of this socket in this node
    """

    all_socks = len(node.inputs)
    for i in range(0, all_socks):
        if node.inputs[i] == socket:
            return i
    pass

def has_none_or_several_mat_output_nodes(material):
    """
        Returns True if there are 0 or >1 material output nodes in the material
    """

    material_outputs = []
    for node in material.node_tree.nodes:
        if node.type == 'OUTPUT_MATERIAL':
            material_outputs.append(node)
    if len(material_outputs) != 1:
        return True
    return False

def get_node_by_type(nodes, type):
    """
        Supply a collection of nodes and the desired node.type to this function.
        RETURNS: first match or None
    """
    for each_node in nodes:
        if each_node.type == type:
            return each_node
    return None

def get_node_by_name(nodes, name):
    
    """
        returns the f i r s t node matching the specified name
    """

    for each_node in nodes:
        if each_node.name == name:
            return each_node
    pass
    
def get_nodes_by_name(nodes, name):

	"""
		return all the nodes with teh name specified
	"""
	ret_nodes = []
	for nd in nodes:
		if nd.name == name:
			ret_nodes.append(nd)
	return(ret_nodes)
	
	
def has_connected_principled_BSDF(material):
    """
        Returns True if in the material, there is at least one BSDF shader connected to a material output node
    """

    mat_output = get_node_by_type(material.node_tree.nodes, 'OUTPUT_MATERIAL')
    if mat_output is None:
        return False
    if mat_output.inputs['Surface'].is_linked:
        if mat_output.inputs['Surface'].links[0].from_node.type == 'BSDF_PRINCIPLED':
            return True
    else: 
        return False

def mat_output_has_other_inputs(material):
    """
        True if a first matched matoutput node has connected sockets apart from 'Surface'
        Returns {'NO MATERIAL OUTPUT'} if no matoutput node was found
    """

    mat_output = get_node_by_type(material.node_tree.nodes, 'OUTPUT_MATERIAL')
    if mat_output is None:
        return False # <--- if there's no material output node, we do not care
    vol_links = mat_output.inputs['Volume'].is_linked
    disp_links = mat_output.inputs['Displacement'].is_linked
    if vol_links or disp_links:
        return True
    pass

def node_set_selected_and_active(node_input):
    """
        deselects all the nodes, selects and activates the specified node
        returns False if unable to perform the operation
        return True if done succesfully
    """
    try:
        for each_node in bpy.context.active_object.active_material.node_tree.nodes:
            each_node.select = False
        node_input.select = True
        bpy.context.active_object.active_material.node_tree.nodes.active = node_input
        return True
    except AttributeError:
        print('no active material present to do this operation')
        return False
    pass

def configureBaker(BakerSettings):
    
    """
        Supply settings for the baker as a dictionary with the following possible keys:
            'Diffuse direct influence' (True/False)
            'Diffuse indirect influence' (True/False)
            'Selected to active' (True/False)
            'Clear image' (True/False)
            'Margin' (integer value)
            'Normal space' ('TANGENT' and others)
            'Normal red' (default 'POS_X')
            'Normal green' (default 'POS_Y')
            'Normal blue' (default 'POS_Z')
            'Use cage' (True/False)
            'Ray distance' (float)
        Return True if carried out operations succesfully
    """
    try:
        baker_settings = bpy.context.scene.render.bake
        baker_settings.use_pass_direct = BakerSettings.get('Diffuse direct influence', False)
        baker_settings.use_pass_indirect = BakerSettings.get('Diffuse indirect influence', False)
        baker_settings.use_pass_color = BakerSettings.get('Diffuse color influence', True)
        baker_settings.use_selected_to_active = BakerSettings.get('Selected to active', False)
        baker_settings.use_clear = BakerSettings.get('Clear image', True)
        baker_settings.margin = BakerSettings.get('Margin', 16)
        baker_settings.normal_space = BakerSettings.get('Normal space', 'TANGENT')
        baker_settings.normal_r = BakerSettings.get('Normal red', 'POS_X')
        baker_settings.normal_g = BakerSettings.get('Normal green', 'POS_Y')
        baker_settings.normal_b = BakerSettings.get('Normal blue', 'POS_Z')
        baker_settings.use_cage = BakerSettings.get('Use cage', False)
        baker_settings.cage_extrusion = BakerSettings.get('Ray distance', 4.0)
    except Exception:
        return False
    return True

def swap_links(node, a, b):
    """
        for the given node, move link of a to b (if exists) and link of b to a (if exists)
        DOES NOT check whether the specified sockets do exist
    """

    node_tree = node.id_data
    A, B, a_out, b_out, a_link, b_link = node.inputs[a], node.inputs[b], None, None, None, None

    if A.is_linked:
        a_out = node.inputs[a].links[0].from_socket
        a_link = node.inputs[a].links[0]
    if B.is_linked:
        b_out = node.inputs[b].links[0].from_socket
        b_link = node.inputs[b].links[0]

    if A.is_linked and B.is_linked:
        node_tree.links.remove(a_link)
        node_tree.links.remove(b_link)
        node_tree.links.new(B, a_out)
        node_tree.links.new(A, b_out)
    elif A.is_linked:
        node_tree.links.remove(a_link)
        node_tree.links.new(B, a_out)
    elif B.is_linked:
        node_tree.links.remove(b_link)
        node_tree.links.new(A, b_out)
    else:
        pass
    pass

def get_socket_neighbor(node, socket, offset):
    """
        get the neighbor of this socket, whose position is specified by the offset
        RETURNS: a socket or OUT_OF_RANGE
        NOTE: offset is not for the Blender socket order, it's acual movement by 'offset' socket up or down in world coordinates
    """
    sock_ind = get_socket_index(socket, node)
    desired_position = sock_ind - offset # <--- the actual position in 'blender coordinates'
    if desired_position > (len(node.inputs)-1) or desired_position < 0:
        return OUT_OF_RANGE
    else: 
        return node.inputs[desired_position]

def has_no_materials(object):
    for mt in object.material_slots:
        if not mt.material is None:
            return True
    return False