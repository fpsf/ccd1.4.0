import sys
from datetime import datetime

import numpy
import pyfits as fits
from PIL import Image, ImageDraw, PngImagePlugin
from skimage import exposure

software_version = "CCD Controller 1 - V 1.0"

def set_header(fitname):
    # Abrindo o arquivo
    fits_file = fits.open(fitname)
    # Escrevendo o Header
    # Can't get the temperature because have a locker locking shooter process
    # fits_file[0].header["TEMP"] = tuple(get_temperature())[3]
    fits_file[0].header["DATE"] = datetime.utcnow().strftime('%Y-%m-%d_%H:%M:%S')

    # Criando o arquivo final
    try:
        print("Tricat of set_header")
        # Fechando e removendo o arquivo temporario
        # fits_file.flush()
        fits_file.close()
    except OSError as e:
        print(fitname)
        print("Exception ->" + str(e))


def save_tif(img, newname):
    print("Opening filename")
    try:
        print("tricat of save_tif")

        try:
            if sys.platform.startswith("linux"):
                imgarray = numpy.array(img, dtype='uint16')
            elif sys.platform.startswith("win"):
                imgarray = numpy.array(img, dtype='int16')
        except Exception as e:
            print(e)

        im3 = Image.fromarray(imgarray)
        im3.save(newname)

        '''
        salvar tif via tifffile.py
        img2 = numpy.array(img, dtype='uint16')
        skimage.io.imsave(newname, img2, plugin='tifffile')
        '''
    except Exception as e:
        print("Exception -> {}".format(e))


def save_png(img, newname, headers):
    mantenha_variavel_name(newname)
    # print(type(headers))
    # print("\n\n- HEADERS -")
    # print(type(headers))
    # for keys, values in headers.items():
    #     print(str(keys))
    #     print(str(values) + "\n")
    # print("- END HEADERS -\n\n")

    try:
        binning = int(headers['Binning'])
        binning += 1
    except Exception as e:
        print("Binning Type Error ->" + str(e))
        binning = " ??? "

    newname_png = newname + ".png"
    img_png = img

    print("Opening filename")
    try:
        print("Tricat of save_png")
        imgarray = numpy.asarray(img_png, dtype=numpy.int32)

        info = PngImagePlugin.PngInfo()
        day_hour = get_date_hour_image_for_headers(str(headers['Start Time']))

        try:
            info.add_text('Binning: ', str(binning) + "x" + str(binning))
            info.add_text('CCD SET TEMP: ', str(headers['Set Temperature']) + u"\u00b0C")
            info.add_text('CCD Temperature: ', str(headers['Temperature']) + u"\u00b0C")
            info.add_text('CCD Type: ', str(headers['Imager ID']))
            info.add_text('Exposure: ', str(headers['Exposure']) + "0 ms")
            info.add_text('Filter Label: ', str(headers['Filter Label']))
            info.add_text('Filter Position: ', str(headers['Filter Position']))
            info.add_text('Filter Wavelength: ', str(headers['Filter Wavelength']))
            info.add_text('Filter Wheel Temperature: ', "25" + u"\u00b0C")
            info.add_text('Image Type: ', 'PNG')
            info.add_text('Latitude: ', str(headers['Latitude']) + u"\u00b0")
            info.add_text('Longitude: ', str(headers['Longitude']) + u"\u00b0")
            info.add_text('Moon Elevation: ', str(headers['Moon Elevation']) + u"\u00b0")
            info.add_text('Moon Phase: ', str(headers['Moon Phase']) + " %")
            info.add_text('Shutter CCD: ', str(headers['Open or close shutter']))
            info.add_text('Shutter Lenz: ', str(headers['Open or close shutter']))
            info.add_text('Site ID: ', str(headers['Observatory']))
            info.add_text('Start Time: ', str(day_hour) + " UTC")
            info.add_text('Sun Elevation:', str(headers['Sun Elevation']) + u"\u00b0")
            info.add_text('Version: ', str(software_version))
        except Exception as e:
            print("info.add_text: " + e)

        image = Image.fromarray(imgarray)
        image.save(newname_png, "PNG", pnginfo=info)
        # set_headers_png(newname_png)

    except Exception as e:
        print("Exception save_png -> {}".format(e))
        # finally:
        #     try:
        #         set_headers_png(newname_png)
        #     except Exception as e:
        #         print("Exception set_headers_png -> {}".format(e))

'''def save_png(img, newname, get_level1, get_level2):
    """
    :param img: 
    :param newname: 
    :param get_level1: 
    :param get_level2: 
    :return: 
    """
    print("Opening filename")
    try:
        print("tricat of save_png")
        img_aux = toimage(img)
        im2 = img_aux

        variavel = get_level(im2, get_level1, get_level2)

        im2 = bytscl(img, variavel[1], variavel[0])
        img_aux.save(newname)

        im3 = toimage(im2)
        im3.save(newname)

        # resize_image_512x512(newname)
        # draw_image(newname)

    except Exception as e:
        print("Exception -> {}".format(e))'''


def retorna_imagem(img):
    """ 
    :param name_png: 
    :return: 
    """
    img2 = Image.open(img)
    img2.show()


def resize_image_512x512(img):
    """
    :param img: 
    :return: 
    """
    resized_img = img.resize((int(512), int(512)))
    #resized_img = ImageOps.autocontrast(resized_img, 2)

    return resized_img


def draw_image(img, file_name):
    """
    :param img: 
    :param file_name: 
    :return: 
    """
    hora_img, data_img = get_date_hour_image(file_name)
    filter_img, observatory_img = get_filter_observatory(file_name)

    fontsFolder = '/usr/share/fonts/truetype'
    # times_nr_Font = ImageFont.truetype(os.path.join(fontsFolder, 'Times_New_Roman_Bold.ttf'), 16)
    # draw.text((10, 10), observatory_img, fill='white', font=times_nr_font)
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), observatory_img, fill='white')
    draw.text((470, 10), filter_img, fill='white')
    draw.text((420, 490), hora_img, fill='white')
    draw.text((10, 490), data_img, fill='white')
    del draw

    return img
    #mostra imagem unicamente
    #img.show()

def img_hist_equal(img, sref_min, sref_max):
    img = numpy.array(img, dtype=numpy.uint16)
    #Tuple = 6 & 7
    p2, p98 = numpy.percentile(img,(sref_min, sref_max))
    img_hist = exposure.rescale_intensity(img, in_range=(p2, p98))
    return img_hist


def get_level(im2, sref_min, sref_max):
    '''
    :param im2: imagem tipo float
    :param sref_min: nivel de referencia normalizado
    :param sref_max: nivel de referencia normalizado
    :return: limites inferior e superior da imagem para exibição na tela, baseado nos niveis de referencia.
    '''
    #
    x_min, x_max = numpy.min(im2), numpy.max(im2)

    # bin_size precisa ser 1 para analisar ponto à ponto
    bin_size = 1
    x_min = 0.0

    nbins = numpy.floor(((x_max - x_min) / bin_size))

    try:
        hist, bins = numpy.histogram(im2, int(nbins), range=[x_min, x_max])

        sum_histogram = numpy.sum(hist)

        sref = numpy.zeros(2)
        sref[0] = sref_min
        sref[1] = sref_max

        res_sa = numpy.zeros(len(hist))

        sa = 0.
        for i in range(len(hist)):
            sa += hist[i]
            res_sa[i] = sa

        res_sa2 = res_sa.tolist()
        res = res_sa[numpy.where((res_sa > sum_histogram * sref[0]) & (res_sa < sum_histogram * sref[1]))]
        nr = len(res)

        sl0 = res_sa2.index(res[0])
        sl1 = res_sa2.index(res[nr - 1])
        slevel = [sl0, sl1]
    except Exception as e:
        print("Exception get_level ->" + str(e))
        print("slevel = [10, 20]")
        slevel = [10, 20]

    return slevel


def get_date_hour(tempo):
    data = tempo[0:4] + "_" + tempo[4:6] + tempo[6:8]
    hora = tempo[9:11] + ":" + tempo[11:13] + ":" + tempo[13:15]

    return data, hora


def get_date_hour_image(tempo):
    hora_img = tempo[-10:-8] + ":" + tempo[-8:-6] + ":" + tempo[-6:-4] + " UT"
    data_img = tempo[-13:-11] + "/" + tempo[-15:-13] + "/" + tempo[-19:-15]

    return hora_img, data_img

def get_date_hour_image_for_headers(tempo):
    date_hour_header = tempo[:4] + "-" + tempo[4:6] + "-" + tempo[6:8] + " " + tempo[-6:-4] + ":" + tempo[-4:-2] + ":" \
                       + tempo[-2:]

    return date_hour_header


def get_filter_observatory(name):
    name_aux = name.split('/')[-1]
    name_filter = name_aux.split('_')[0]
    name_observatory = name_aux.split('_')[1]

    return name_filter, name_observatory


def get_observatory(name):
    name_aux = str(name).split(',')[1]
    name_aux = name_aux.replace("\'", "")
    name_aux = name_aux.replace(" ", "")

    return name_aux

def mantenha_variavel_name(newname):
    variavel = newname
    return 0