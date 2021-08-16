
import glob
import re

# Need to commit and get karim to access this code so he can test with all files and cross reference with his handmade ones
# If the string does not match the format, note the page name and the line number. 

def string_replace():

    # Collect all files to edit
    xaml_files = []
    for file in glob.glob('C:/Users/stazy/Source/Repos/EmergConnect/EmergConnect/EmergConnect/Pages/*/*.xaml'):
        xaml_files.append(file)

    for file in glob.glob('C:/Users/stazy/Source/Repos/EmergConnect/EmergConnect/EmergConnect/Pages/*.xaml'):
        xaml_files.append(file)

    var_count = 1
    strings_dict = {}

    # Loop through each file
    for file in xaml_files:
        i = 0

        # read all lines of the file into list
        f = open(file, 'r')
        content = f.readlines()
        f.close()

        updated_content = []

        # iterate through lines
        for line in content:
            i += 1
            
            if 'Text=\"{' in line:
                updated_content.append(line)
            elif 'Text=' in line:
                re_str = re.compile('Text=\"[^\"]*\" ')
                str = re_str.findall(line)
                if str == []:
                    print(file)
                    print(i)
                    updated_content.append(line)
                    continue
                stripped = str[0][5:]

                if stripped not in strings_dict:
                    index = 'var%s' % var_count
                    var_count = var_count + 1
                    strings_dict[stripped] = index
                else:
                    index = strings_dict[stripped]

                # replace it in a new string and add that to updated_content
                original_str = str[0]
                updated_str = 'Text=\"{x:Static Resource:ApplicationResource.%s}\" ' % index
                updated_line = line.replace(original_str, updated_str)

                updated_content.append(updated_line)
                
            else:
                updated_content.append(line)
                # if this is the base pages line and there is not the line we want, append it next in line
                if 'd:BasePage' in line and 'xmlns:Resource=\"clr-namespace:EmergConnect.RecourseFiles\"' not in content:
                    updated_content.append('xmlns:Resource=\"clr-namespace:EmergConnect.RecourseFiles\"')

        # Write all of updated_content to a new file
        # Create new filepath name
        new_file = file[:-5] + 'DONE' + file[-5:]

        f = open(new_file, 'w')
        f.writelines(updated_content)
        f.close()


    # Need to add: RESOURCE FILE
    # Reverse dictionary
    reversed_dictionary = {value : key for (key, value) in strings_dict.items()}

    # Open file for writing and go to the right line in the code - 
    file = 'C:/Users/stazy/source/repos/EmergConnect/EmergConnect/EmergConnect/RecourseFiles/ApplicationResource2.resx'
    f = open(file, 'r')
    lines = f.readlines()
    f.close()
    file = 'C:/Users/stazy/source/repos/EmergConnect/EmergConnect/EmergConnect/RecourseFiles/ApplicationResource3.resx'
    index = 119
    f = open(file, 'w')
    p1 = '  <data name=\"'
    p2 = '\" xml:space=\"preserve\">\n    <value>'
    p3 = '</value>\n  </data>\n'
    for key in reversed_dictionary.keys():
        str = p1 + key + p2 + reversed_dictionary[key] + p3
        lines.insert(index, str)
        index += 3
    lines.append('</root>')
    f.writelines(lines)
    f.close()


string_replace()

