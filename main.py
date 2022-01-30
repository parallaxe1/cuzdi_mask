import cuzdi_toolbox as ctb
import configparser

class Conf(object):
    def __init__(self,filename):
        self.filename = filename
        self.config = configparser.ConfigParser(inline_comment_prefixes="#")
        self.config.read(self.filename, encoding='utf-8')
        self.mode = self.config.get("Main", 'input_mode').lower()
    def load_device(self):
        self.focal_length = self.config.getfloat("Device", 'focal_length')*1e-3
        self.apperture = self.config.getfloat("Device", 'apperture')*1e-3
        self.wavelength = self.config.getfloat("Device", 'wavelength')*1e-9
        self.slit_sep_factor = self.config.getint("Device", 'slit_sep_factor', fallback='7') # default: 7
        self.pixel_size = self.config.getfloat("Device", 'pixel_size')*1e-6
        self.num_pixel = self.config.getint("Device", 'num_pixel')
    def store_slit_width(self,slit_width):
        self.slit_width = slit_width
        self.config.set('Mask','slit_width',str(slit_width*1e3))
        file = open(self.filename,'w')
        self.config.write(file)
        file.close()
    def load_mask(self):
        self.slit_width = self.config.getfloat("Mask", 'slit_width')*1e-3
        self.slit_sep_factor = self.config.getint("Mask", 'slit_sep_factor', fallback=self.config.getfloat("Device", 'slit_sep_factor')) # default: 7
        self.apperture = self.config.getfloat("Mask", 'apperture', fallback=self.config.getfloat("Device", 'apperture')) * 1e-3
        self.diameter = self.config.getfloat("Mask", 'diameter') * 1e-3
        self.sep_horizontal = self.config.getfloat("Mask", 'sep_horizontal') * 1e-3
        self.sep_vertical = self.config.getfloat("Mask", 'sep_vertical') * 1e-3
        self.stroke_width = self.config.getfloat("Mask", 'stroke_width', fallback=10e-6)
        self.slit_angle_q2 = self.config.getfloat("Mask", 'slit_angle_q2')
        self.slit_angle_q3 = self.config.getfloat("Mask", 'slit_angle_q3')


def load_configuration(filename):

    conf = Conf(filename)
    if (conf.mode == 'device'):
        conf.load_device()
    conf.load_mask()

    return conf

def main():
    filename = "cuzdi.conf"
    conf = load_configuration(filename)
    if(conf.mode == 'device'):
        conf = ctb.calc_slit_width(conf)

    ctb.create_svg(conf)
    print("finished!")


if __name__ == "__main__":
    main()