from src.business.configuration.settingsCamera import SettingsCamera
from src.business.configuration.settingsImage import SettingsImage


def get_project_settings():
    """
    name_geographic_settings[0] = Latitude
    name_geographic_settings[1] = Longitude
    name_geographic_settings[2] = Elevation(m)
    name_geographic_settings[3] = Pressure(mb)
    name_geographic_settings[4] = Temperature(?)

    name_set_moonsun_settings[0] = Solar Elevation
    name_set_moonsun_settings[1] = Ignore Lunar Position
    name_set_moonsun_settings[2] = Lunar Elevation
    name_set_moonsun_settings[3] = Lunar Phase

    name_site_settings[0] = Name
    name_site_settings[1] = Observatory
    name_site_settings[2] = Imager ID
    """

    from src.business.configuration.configProject import ConfigProject
    ci = ConfigProject()

    name_geographic_settings = ci.get_geographic_settings()
    name_set_moonsun_settings = ci.get_moonsun_settings()
    name_site_settings = ci.get_site_settings()

    return name_geographic_settings, name_set_moonsun_settings, name_site_settings


def get_image_settings():
    """
    Pega os valores no ini image
    info_image[0] = get_level1
    info_image[1] = get_level2
    info_image[2] = crop_xi
    info_image[3] = crop_xf
    info_image[4] = crop_yi
    info_image[5] = crop_yf
    info_image[6] = ignore_crop
    info_image[7] = image_tif
    info_image[8] = image_fit
    """

    settings = SettingsImage()
    info_image = settings.get_image_settings()

    return info_image


def get_camera_settings():
    """
    Pega os valores no ini camera
    info_cam[0] = temperature_camera
    info_cam[1] = tempo de espera até atingir temperatura desejada
    info_cam[2] = dark(Open or close shutter)
    """
    settings = SettingsCamera()
    info_cam = settings.get_camera_settings()

    return info_cam
