import xml.etree.ElementTree as ET
import os, sys
from time import sleep
from datetime import datetime

def getPath():
    try:
        # Get the real path for the folder 'Updated formator stuff' along with py file name 
        py_path = sys.executable
        py_filename = 'DID_XML_check_and_edit.exe'

        # Remove the py file name
        path_filename = py_path[:-len(py_filename)]

        # Replace "\" to "/"
        path = path_filename.replace('\\', '/')

        # Construction of input file path
        path_input_xml = os.path.join(path, 'Input/')
        xml_input_filename = os.listdir(path_input_xml)[0]
        input_path = os.path.join(path_input_xml, xml_input_filename)

        

        return (input_path, path)
    except Exception as e:
        print(e)
        sleep(5)

def xml_changeTrue(Ipath, path):

    # XML paths assigned
    Input_xmlFilePath = Ipath

    # Parse the XML file
    tree = ET.parse(Input_xmlFilePath)
    root = tree.getroot()

    # Find the FunctionalStatus element
    functional_status = root.find('FunctionalStatus')
    date_time = root.find('.//Date_Time')
    createdBy = root.find('.//Createdby')

    # Necessary initializations and declarations
    required_true_attr = []
    required_false_attr = []
    allAtributes = []
    consent = 'N'

    # Check if the FunctionalStatus element exists
    if functional_status is not None:
        for attr, value in functional_status.attrib.items():
            allAtributes.append(attr)
        # Iterate over all attributes in the FunctionalStatus element
        print('Please select the required attributes to make it "true" or "false.')
        while(allAtributes != []):
            selection = input(f'{allAtributes[0]} (T/F): ')
            if(selection == 'T' or selection == 't'):
                required_true_attr.append(allAtributes.pop(0))
                
            elif(selection == 'F' or selection == 'f'):
                required_false_attr.append(allAtributes.pop(0))
                
            else:
                print("\nError: Invalid Literal. Please try again!\n")


        print("\nAttributes selected to make 'true': ")
        for t in required_true_attr:
            print(t)
        print("\nAttributes selected to make 'false': ")
        for f in required_false_attr:
            print(f)
        
        while(consent != 'Y' or consent != 'y' or consent != 'N' or consent != 'n'):
            consent = input("\nDo you want to change the above attributes?(Y/N): ")
            
            if(consent == 'Y' or consent == 'y'):
                if(required_true_attr != []):
                    for att in required_true_attr:
                        if(functional_status.attrib[att] == 'false'):
                            functional_status.set(att, 'true')
                        else:
                            pass
                else:
                    print("\nNo attributes selected for change to 'true'.")
                if(required_false_attr != []):
                    for atr in required_false_attr:
                        if(functional_status.attrib[atr] == 'true'):
                                functional_status.set(atr, 'false')
                        else:
                            pass
                else:
                    print("\nNo attributes selected for change to 'false'.")

                project = input("Enter the project name for output file name: ")
                ecu = input("Enter ECU: ")
                
                # Construction of output file path
                dt = datetime.now()
                formatted_datetime = dt.strftime("%d%m%Y_%H%M%S")
                path_output_xml = os.path.join(path, 'Output/')
                xml_output_filename = f'Output_XML_{project}_{ecu}_{formatted_datetime}.xml'
                Output_xmlFilePath = os.path.join(path_output_xml, xml_output_filename)

                # XML createdBy and Date Time Input and formatting
                xml_dateTimeFormat = dt.strftime("%Y-%m-%d %H:%M:%S")
                try:
                    date_time.text = xml_dateTimeFormat
                    editor_name = input('CreatedBy: ')
                    createdBy.text = editor_name
                except:
                    pass

                tree.write(Output_xmlFilePath, encoding='utf-8', xml_declaration=True)

                return "\nFile created!\nChanges done successfully!"
            
            elif(consent == 'N' or consent == 'n'):
                return "\nConsent NOT given."
            else:
                print("Error: Invalid Literal. Please try again!") 
    else:
        return "Functional Status has no attributes defined."   

if __name__=='__main__':
    os.system('cls')
    IPath, temp_path = getPath()

    # Temporary paths for testing purpose
    # IPath = 'Input/JFWyhQcAGL404507_TEL_H105ADIDs.xml'
    # dt = datetime.now()
    # formatted_datetime = dt.strftime("%d%m%Y_%H%M%S")
    # OPath = f'Output/Output_XML_{formatted_datetime}.xml'

    print(xml_changeTrue(IPath, temp_path))
    print("\nClosing the terminal...")
    sleep(0.68)