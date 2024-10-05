'''Installd all versions of solidity compiler from 0.4 to 0.5. 
'''

import os

versions = [
    '0.4.1'
   , '0.4.3'
   , '0.4.4'
   , '0.4.5'
   , '0.4.6'
   , '0.4.7'
   , '0.4.9'
    ,'0.4.10'
    ,'0.4.11'
    ,'0.4.12'
    ,'0.4.13'
    ,'0.4.14'
    ,'0.4.17'
    ,'0.4.20'
    ,'0.4.21'
    ,'0.4.22'
    ,'0.4.25'
    ,'0.4.26'
   , '0.5.1'
   , '0.5.2'
   , '0.5.3'
   , '0.5.4'
   , '0.5.5'
   , '0.5.6'
   , '0.5.7'
   , '0.5.9'
    ,'0.5.10'
    ,'0.5.12'
    ,'0.5.13'
    ,'0.5.14'
    ,'0.5.15'
    ,'0.5.16'
    ,'0.5.17'
]


def main():
    for version in versions:
        cmd = f'solc-select install {version}' 
        os.system(cmd)
    return 


if __name__ == "__main__":
    main()