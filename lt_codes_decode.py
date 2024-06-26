import os
import math
import argparse
import numpy as np
import core
from encoder import encode
from decoder import decode
from random import randrange

def blocks_write(blocks, file, filesize):
    """ Write the given blocks into a file
    """

    count = 0
    for data in recovered_blocks[:-1]:
        file_copy.write(data)
        count += len(data)

    # Convert back the bytearray to bytes and shrink back 
    last_bytes = bytes(recovered_blocks[-1])
    shrinked_data = last_bytes[:filesize % core.PACKET_SIZE]
    file_copy.write(shrinked_data)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Robust implementation of LT Codes encoding/decoding process.")
    parser.add_argument("filename", help="file path of the file to split in blocks")
    parser.add_argument("-r", "--redundancy", help="the wanted redundancy.", default=2.0, type=float)
    parser.add_argument("--systematic", help="ensure that the k first drops are exactaly the k first blocks (systematic LT Codes)", action="store_true")
    parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("--x86", help="avoid using np.uint64 for x86-32bits systems", action="store_true")
    args = parser.parse_args()

    core.NUMPY_TYPE = np.uint32 if args.x86 else core.NUMPY_TYPE
    core.SYSTEMATIC = True if args.systematic else core.SYSTEMATIC 
    core.VERBOSE = True if args.verbose else core.VERBOSE 

    # Recovering the blocks from symbols
    with open(args.filename, 'r') as f:
        lines = f.readlines()
        file_blocks_n = int(lines[-2])
        print("Block Count: " + str(file_blocks_n))

    
    filesize = int(lines[-1])

    #blocks_n = math.ceil(filesize / core.PACKET_SIZE)
    #blocks = []
    file_symbols = []

    #for i in range(blocks_n):

    for entry in lines[0:len(lines)-2]:
        splitSymbol = entry.split(", ")
 #       print(splitSymbol)
        data = splitSymbol[2]

        #file_symbols.append(symbol)
#        print()

        #ELIMINATE BRACKETS FROM SPLIT SYMBOL 2
        splitSymbol[2] = splitSymbol[2][1:-2].strip()

        #print(splitSymbol[2])
        dataArray = []
        data = " ".join(splitSymbol[2].split())
        for i in data.split(" "):
            #i = (i.strip())
            dataArray.append(int(i))
            #print(dataArray)
        dataArray = np.array(dataArray)
#        print(dataArray) 
        symbol = core.Symbol(int(splitSymbol[0]), int(splitSymbol[1]), dataArray)
        file_symbols.append(symbol)
    
        #print(type(np.frombuffer(splitSymbol[2].encode(), dtype=core.NUMPY_TYPE)))

    #print(type(file_symbols))
    #print(file_symbols)

                                                #list
    recovered_blocks, recovered_n = decode(file_symbols, blocks_quantity=file_blocks_n)
    
    if core.VERBOSE:
        print(recovered_blocks)
        #print("------ Blocks :  \t-----------")
        #print(file_blocks)

    if recovered_n != file_blocks_n:
        print("All blocks are not recovered, we cannot proceed the file writing")
        exit()

    splitted = args.filename.split(".")
    if len(splitted) > 1:
        filename_copy = "".join(splitted[:-1]) + "-output." + splitted[-1] 
    else:
        filename_copy = args.filename + "-output"

    # Write down the recovered blocks in a copy 
    with open(filename_copy, "wb") as file_copy:
        blocks_write(recovered_blocks, file_copy, filesize)

    print("Wrote {} bytes in {}".format(os.path.getsize(filename_copy), filename_copy))

