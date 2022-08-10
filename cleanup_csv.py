#!/bin/env python3

import argparse
import csv

## Constants ##

OUTPUT_FILE = "results.csv"

## Functions ##

def main():
    parser = argparse.ArgumentParser(
        description="Takes the wedding Google sheet and preps it for gLabel"
    )
    parser.add_argument("file", help="File to process")
    parser.add_argument(
        "out_file",
        nargs="?",
        default=OUTPUT_FILE,
        help="Where to put the output file"
    )
    args = parser.parse_args()

    addrTbl: dict[str, list[str]] = {}
    noAddrLst: list[str] = []

    with open(args.file) as csvFile:
        reader = csv.reader(csvFile)
        next(reader)
        for row in reader:
            name = row[0]
            addr = row[1]
            # Skip blanks
            if not name:
                continue
            # Track all records without an address (skipping +1s)
            if not addr:
                if not "+1" in name:
                    noAddrLst.append(name)
                continue
            if addr not in addrTbl:
                addrTbl[addr] = [name]
            else:
                addrTbl[addr].append(name)

    print(f"Number of addresses: {len(addrTbl.keys())}")
    print(f"Number of missing addresses: {len(noAddrLst)}")
    for name in noAddrLst:
        print(f"  {name}")

    outputRows: list[list[str]] = []
    for addr, nameLst in addrTbl.items():
        splitPt = addr.find(',')
        addr1 = addr[0:splitPt]
        addr2 = addr[splitPt+1:]
        
        name = ""
        if len(nameLst) == 1:
            name = nameLst[0]
        elif len(nameLst) == 2:
            if "+1" in nameLst[1]:
                name = nameLst[0]
            else:
                firstFirstName = nameLst[0].split()[0]
                name = f"{firstFirstName} & {nameLst[1]}"
        else:
            lastName = nameLst[0].split()[1]
            name = f"House of {lastName}"
        outputRows.append([name.strip(), addr1.strip(), addr2.strip()])

    outputRows.sort()
    with open(args.out_file, "w", newline='') as fd:
        writer = csv.writer(fd)
        writer.writerows(outputRows)

if __name__ == "__main__":
    main()