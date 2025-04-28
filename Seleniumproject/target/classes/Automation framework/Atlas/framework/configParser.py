import configparser
config = configparser.ConfigParser()

config.read('your_config_file.ini')

#Access data:
# Get sections:
sections = config.sections()
print(sections)

#Check section existence.
if 'section_name' in config:
    # Section exists
    pass

#Get options (keys) in a section
options = config.options('section_name')
print(options)

#Get value of an option.
value = config.get('section_name', 'option_name')
print(value)

#Get value with type conversion.
int_value = config.getint('section_name', 'int_option')
bool_value = config.getboolean('section_name', 'bool_option')
float_value = config.getfloat('section_name', 'float_option')

#Iterate through sections and options:
for section in config.sections():
    print(f"Section: {section}")
    for option in config.options(section):
        value = config.get(section, option)
        print(f"  {option} = {value}")

#Handle exceptions:
    try:
        value = config.get('section_name', 'option_name')
    except configparser.NoSectionError:
        print("Section not found")
    except configparser.NoOptionError:
        print("Option not found")

#Write to .ini file:
    config['new_section'] = {'new_option': 'new_value'}
    with open('your_config_file.ini', 'w') as configfile:
        config.write(configfile)
