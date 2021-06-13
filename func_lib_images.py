############################################################################
############################################################################
############################################################################
################## CONTAINS MISC FUNCTIONS FOR IMAGES ######################
############################################################################
############################################################################
############################################################################

import bpy 
import os
from . import func_lib_misc as miscf


IMAGE_FORMATS = {
                            'BMP':'.bmp',
                            'IRIS':'.iris',
                            'PNG':'.png',
                            'JPEG':'.jpg',
                            'JPEG2000':'.jp2',
                            'TARGA':'.tga',
                            'CINEON':'.cin',
                            'DPX':'.dpx',
                            'OPEN_EXR_MULTILAYER':'.exr',
                            'OPEN_EXR':'.exr',
                            'HDR':'.hdr',
                            'TIFF':'.tiff'
                            }
COLOR_DEPTH = [
                        '8', 
                        '10', 
                        '12', 
                        '16', 
                        '32'
                        ]

COLOR_MODE = [
                        'BW', 
                        'RGB', 
                        'RGBA'
                        ]

def save_as_image(image, folder_path, format, color_mode, bit_depth):
        """
            Saves with specified parameters and reloads
            format in ['BMP',
                        'IRIS',
                        'PNG',
                        'JPEG',
                        'JPEG2000',
                        'TARGA',
                        'CINEON',
                        'DPX',
                        'OPEN_EXR_MULTILAYER',
                        'OPEN_EXR',
                        'HDR',
                        'TIFF'
                        ]
            color_mode in ['BW',
                            'RGBA',
                            'RGB']
            bit_depth in ['8', '16']
            RETURN: False if no success, pointer to an image variable storing the image
        """
        # TODO: raise an exception instead of 
        
        if not format in list(IMAGE_FORMATS.keys()):
            print('Format input must be a value in {}'.format(str(list(IMAGE_FORMATS.keys()))))
            return
        if not color_mode in COLOR_MODE:
            print('Color mode must be a value in {}'.format(str(COLOR_MODE)))
            return
        if not str(bit_depth) in COLOR_DEPTH:
            print('Color depth must be a value in {}'.format(str(COLOR_DEPTH)))
            return
        
        # set the settings of the image
        scn_rend_settings = bpy.data.scenes.new(name = 'scn_rend_settings')
        scn_rend_settings.render.image_settings.file_format = format
        scn_rend_settings.render.image_settings.color_mode = color_mode
        scn_rend_settings.render.image_settings.color_depth = bit_depth

        # construct the path
        if miscf.is_relative_path(folder_path):
            return False

        folder_path_ = miscf.format_folder_path(folder_path)

        if not os.path.exists(folder_path):
            return False

        full_path = folder_path_ + image.name + IMAGE_FORMATS[format]
            
        image.save_render(full_path, scene = scn_rend_settings)

        # reopen the image from its path
        bpy.data.images.remove(image)
        new_im = bpy.data.images.load(full_path)

        bpy.data.scenes.remove(scn_rend_settings)

        return new_im
		
		
def save_as_image2(image, folder_path, image_name, format, color_mode, bit_depth, reload):
		"""
            Saves with specified parameters and reloads on user discretion
            format in ['BMP',
                        'IRIS',
                        'PNG',
                        'JPEG',
                        'JPEG2000',
                        'TARGA',
                        'CINEON',
                        'DPX',
                        'OPEN_EXR_MULTILAYER',
                        'OPEN_EXR',
                        'HDR',
                        'TIFF'
                        ]
            color_mode in ['BW',
                            'RGBA',
                            'RGB']
            bit_depth in ['8', '16']
            RETURN: False if no success, pointer to an image variable storing the image
		"""
		# TODO: raise an exception instead of 
        
		if not format in list(IMAGE_FORMATS.keys()):
			print('Format input must be a value in {}'.format(str(list(IMAGE_FORMATS.keys()))))
			return
		if not color_mode in COLOR_MODE:
			print('Color mode must be a value in {}'.format(str(COLOR_MODE)))
			return
		if not str(bit_depth) in COLOR_DEPTH:
			print('Color depth must be a value in {}'.format(str(COLOR_DEPTH)))
			return
        
        # set the settings of the image
		scn_rend_settings = bpy.data.scenes.new(name = 'scn_rend_settings')
		scn_rend_settings.render.image_settings.file_format = format
		scn_rend_settings.render.image_settings.color_mode = color_mode
		scn_rend_settings.render.image_settings.color_depth = bit_depth

        # construct the path
		if miscf.is_relative_path(folder_path):
			return False

		folder_path_ = miscf.format_folder_path(folder_path)

		if not os.path.exists(folder_path):
			return False

		full_path = folder_path_ + image_name + IMAGE_FORMATS[format]
            
		image.save_render(full_path, scene = scn_rend_settings)

		if reload:# reopen the image from its path
			bpy.data.images.remove(image)
			new_im = bpy.data.images.load(full_path)
			return new_im

		# clean up the dummy scene settings
		bpy.data.scenes.remove(scn_rend_settings)

		return