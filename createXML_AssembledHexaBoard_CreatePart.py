import createXML

def GetArg(argv):
    def print_help():
        raise IOError(f'''
        Input a csv file to modify template xml according csv entry.

        Args:
            arg1(str): csv file path
            arg2(int): start index of csv entry.
                       Set to 0 or negative value to show first 10 lines without modify XML template.
            ''')
    try:
        filename = argv[1]
        import os
        if not os.path.isfile(filename):
            print_help()
    except IndexError as e:
        print_help()
    startIDX = int(argv[2]) if len(argv) > 2 else 0
    return filename, startIDX



if __name__ == "__main__":
    import sys
    inCSVfile,startIDX = GetArg(sys.argv)
    #inCSVfile,startIDX = ('data/testsample_createXML_HexaBoard_Assembly.csv', 1)

    if startIDX<=0: createXML.show_first_10_lines(inCSVfile)

    kopSOURCE = 'data/Kind_of_parts.csv'
    xmlTEMPLATE = 'data/template_AssembledHexaboard_CreatePart.xml'
    outputTAG = 'AssembledHexBoard_CreatePart'
    outputVERSION = '1'

    createXML.main_func(
            inCSVfile = inCSVfile,
            startIDX = startIDX,
            xmlTEMPLATE = xmlTEMPLATE,
            outputTAG = outputTAG,
            kopSOURCEfile = kopSOURCE,
            version = outputVERSION
            )
