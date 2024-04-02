# module img_metadata

from exif import Image


if __name__ == '__main__':
    image = None
    with open("img2.jpg", "rb") as file:
        image = Image(file)

    # check if image contains metadata
    if image.has_exif:
        """
        ['<unknown EXIF tag 50341>', '_exif_ifd_pointer', '_interoperability_ifd_Pointer', '_segments', 
        'brightness_value', 'color_space', 'components_configuration', 'compressed_bits_per_pixel', 
        'compression', 'contrast', 'custom_rendered', 'datetime', 'datetime_digitized', 'datetime_original', 
        'delete', 'delete_all', 'digital_zoom_ratio', 'exif_version', 'exposure_bias_value', 'exposure_mode', 
        'exposure_program', 'exposure_time', 'f_number', 'file_source', 'flash', 'flashpix_version', 'focal_length', 
        'focal_length_in_35mm_film', 'get', 'get_all', 'get_file', 'get_thumbnail', 'has_exif', 'image_description', 
        'jpeg_interchange_format', 'jpeg_interchange_format_length', 'lens_model', 'lens_specification', 'light_source', 
        'list_all', 'make', 'maker_note', 'max_aperture_value', 'metering_mode', 'model', 'offset_time', 
        'offset_time_digitized', 'offset_time_original', 'orientation', 'photographic_sensitivity', 'pixel_x_dimension', 
        'pixel_y_dimension', 'recommended_exposure_index', 'resolution_unit', 'saturation', 'scene_capture_type', 'scene_type', 
        'sensitivity_type', 'sharpness', 'software', 'user_comment', 'white_balance', 'x_resolution', 'y_and_c_positioning', 
        'y_resolution']
        """
        print(f'{image.make}')
        print(f'{image.model}')
        print(f'f{image.f_number}')
        if image.exposure_time >= 1:
            print(f'{image.exposure_time} sec')
        else:
            print(f'1/{1/image.exposure_time} sec')
        print(f'{image.focal_length} mm')
        print(f'ISO {image.photographic_sensitivity}')

        # for key, value in image.get_all().items():
        #     print(f'{key:25s}\t{value}')

