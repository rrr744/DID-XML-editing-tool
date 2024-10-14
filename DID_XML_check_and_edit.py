import xml.etree.ElementTree as ET
import os, sys
from time import sleep
from datetime import datetime

def outputPathContruction(path_t, projectName, ecu_name):
    dt = datetime.now()
    formatted_datetime = dt.strftime("%d%m%Y_%H%M%S")
    path_output_xml = os.path.join(path_t, 'Output/')
    xml_output_filename = f'Output_XML_{projectName}_{ecu_name}_{formatted_datetime}.xml'
    Output_xmlFilePath = os.path.join(path_output_xml, xml_output_filename)

    return Output_xmlFilePath, dt

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

def addDID(Ipath, path):
    Input_xmlFilePath = Ipath

    # Parse the XML file
    tree = ET.parse(Input_xmlFilePath)
    root = tree.getroot()

    choice = 'y'
    try:
        while(True):

            if(choice == 'y' or choice == 'Y'):

                did_hex = input("Did_hex: ")
                conv_rule = input("Conv_Rule: ")
                size_bytes = input("size_Bytes: ")
                desc = input("Desc: ")
                unit = input("Unit: ")
                scaling = input("scaling: ")
                offset = input("Offset: ")
                enum_list = input("Enum_List: ")
                access_pvg = input("AccessPvg: ")
                group_id = input("Group_ID: ")

                data_identifier = ET.Element('DataIdentifier')
                ET.SubElement(data_identifier, 'Did__hex').text = did_hex
                ET.SubElement(data_identifier, 'Conv_Rule').text = conv_rule
                ET.SubElement(data_identifier, 'size_Bytes').text = size_bytes
                ET.SubElement(data_identifier, 'Desc').text = desc
                ET.SubElement(data_identifier, 'Unit').text = unit
                ET.SubElement(data_identifier, 'scaling').text = scaling
                ET.SubElement(data_identifier, 'Offset').text = offset
                ET.SubElement(data_identifier, 'Enum_List').text = enum_list
                ET.SubElement(data_identifier, 'AccessPvg').text = access_pvg
                ET.SubElement(data_identifier, 'Group_ID').text = group_id

                root.append(data_identifier)
                project = input("Enter the project name for output file name: ")
                ecu = input("Enter ECU: ")

                Output_xmlFilePath, dateT = outputPathContruction(path, project, ecu)
                tree.write(Output_xmlFilePath, encoding='utf-8', xml_declaration=True)

            elif(choice == 'N' or choice == 'n'):
                return 0
            
            else:
                print("\nError: Invalid Literal! Please try again.")

            choice = input("Do you want to add more DID? (Y/N): ")
    except Exception as e:
        print(e)
        sleep(5)

def editDID(Ipath, path):
    try:
        Input_xmlFilePath = Ipath

        # Parse the XML file
        tree = ET.parse(Input_xmlFilePath)
        root = tree.getroot()

        find_DID = input('Enter the DID you want to edit (0xXXXX): ')
        find_status_flag = True

        def findDIDalgo(find_DID, find_status_flag):
            for data_identifier in root.findall('DataIdentifier'):
                did_hex = data_identifier.find('Did__hex').text
                if(did_hex == find_DID):
                    print('DID found')
                    find_status_flag = False
                    return data_identifier, find_status_flag

        find_status_identifier, status_flag = findDIDalgo(find_DID, find_status_flag)        

        if(status_flag):
            print('DID not found')
            sleep(2)
            return 0
        
        for child in find_status_identifier:
            new_value = input(f'{child.tag} (Current value: {child.text}): ')

            if(new_value):
                child.text = new_value
        project = input("Enter the project name for output file name: ")
        ecu = input("Enter ECU: ")

        Output_xmlFilePath, dateT = outputPathContruction(path, project, ecu)
        tree.write(Output_xmlFilePath, encoding='utf-8', xml_declaration=True) 
        return "\nFile created!\nChanges done successfully!\nFile saved."

    except Exception as e:
        print(e)
        sleep(5)
        

def deleteDID(Ipath, path):
    try:
        Input_xmlFilePath = Ipath

        # Parse the XML file
        tree = ET.parse(Input_xmlFilePath)
        root = tree.getroot()

        find_DID = input('Enter the DID you want to delete (0xXXXX): ')
        find_status_flag = True

        def findDIDalgo(find_DID, find_status_flag):
                for data_identifier in root.findall('DataIdentifier'):
                    did_hex = data_identifier.find('Did__hex').text
                    if(did_hex == find_DID):
                        print('DID found')
                        find_status_flag = False
                        return data_identifier, find_status_flag
        delete_data_identifier, find_result_flag = findDIDalgo(find_DID, find_status_flag)
        if(find_result_flag):
            print('DID not found')
            sleep(2)
            return 0
        root.remove(delete_data_identifier)
        print("\nDID deleted successfully!")

        project = input("\nEnter the project name for output file name: ")
        ecu = input("Enter ECU: ")

        Output_xmlFilePath, dateT = outputPathContruction(path, project, ecu)
        tree.write(Output_xmlFilePath, encoding='utf-8', xml_declaration=True) 
        return "\nFile created!\nChanges done successfully!\nFile saved."

    except Exception as e:
        print(e)
        sleep(4)
    

def editFunctionalStatus(Ipath, path):

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
                
                Output_xmlFilePath, dt = outputPathContruction(path, project, ecu)

                # XML createdBy and Date Time Input and formatting
                xml_dateTimeFormat = dt.strftime("%Y-%m-%d %H:%M:%S")
                try:
                    date_time.text = xml_dateTimeFormat
                    editor_name = input('CreatedBy: ')
                    createdBy.text = editor_name
                except:
                    pass

                tree.write(Output_xmlFilePath, encoding='utf-8', xml_declaration=True)

                return "\nFile created!\nChanges done successfully!\nFile saved."
            
            elif(consent == 'N' or consent == 'n'):
                return "\nConsent NOT given."
            else:
                print("Error: Invalid Literal. Please try again!") 
    else:
        return "Functional Status has no attributes defined."   

if __name__=='__main__':
    os.system('cls')
    IPath, temp_path = getPath()

    while(True):
        os.system('cls')
        print("""
    1. Add DID
    2. Delete DID
    3. Edit DID
    4. Edit Functional Status\n
To exit, type 'exit' and press enter. """)
        menu = input("\nSelect the action to perform: ")

        if(menu == '1'):
            print(addDID(IPath, temp_path))
            sleep(2)
        elif(menu == '2'):
            print(deleteDID(IPath, temp_path))
            sleep(2)
        elif(menu == '3'):
            print(editDID(IPath, temp_path))
            sleep(2)
        elif(menu == '4'):
            print(editFunctionalStatus(IPath, temp_path))
            sleep(2)
        elif(menu == 'exit'):
            break
        else:
            print("Invalid Input!")

    print("\nClosing the terminal...")
    sleep(0.68)