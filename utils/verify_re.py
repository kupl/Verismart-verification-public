'''Get results about reentrancy contracts. 
'''
from __future__ import annotations 
from typing     import * 

import os 
import argparse
from executer import Executer

from tqdm import tqdm


class Verifier:

    def __init__(self
                , args
                ):
        self.args = args 
        self.path = args.path 
        self.main_path = args.main_path 


    def _get_all_paths(self) -> List[str]:  
        res = list()
        for root, dir, files in os.walk(self.path):
            for file in files:
                if "README" in file:
                    continue
                if "modifier_reentrancy.sol" in file:
                    continue # it does not involve ether sending functions(e.g., transfer, send, call)  
                res.append(os.path.join(root, file))
        return res


    def run(self) -> None:
        paths = self._get_all_paths()
        for path in tqdm(paths):
            print(f'current contract -> {path}')
            obj = Executer(path, 're', './anal_results/re', self.main_path)
            obj.run()
        return 


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path')
    parser.add_argument('--main_path')
    args = parser.parse_args()
    obj = Verifier(args)
    obj.run()
    return 


if __name__ == "__main__":
    main()  
