'''
./main.native -input ./smartbugs-dashboard/smartbugs/dataset/reentrancy/etherstore.sol -verify_timeout 120 -z3timeout=10000 -mode verify re
dd
'''
from __future__ import annotations
from typing     import * 

import os 
import subprocess
import re 
import argparse


class Executer:

    def __init__(self
               , path: str 
               , vul: str | None 
               , save_path: str
               , main_path: str 
               ):

        self.path = path  
        self.vul = vul 
        self.save_path = save_path 
        self.main_path = main_path 


    def _comp_version(self, version: str, min_version: str = "0.4.24") -> str:
        '''Force to complile a code with solc above 0.4.24
        '''
        # return min_version

        # do not use it anymore.
        version_parts = list(map(int, version.split('.')))
        min_version_parts = list(map(int, min_version.split('.')))
        
        if version_parts < min_version_parts:
            return min_version
        return version


    def _get_version_aux(self, code: str) -> str | None:
        match = re.search(r'0\.\d+\.\d+', code)
        if match:
            version = match.group(0)
            refined = self._comp_version(version)
            return refined 
        else:
            return # comment case. 


    def _get_version(self) -> str:
        with open(self.path, 'r') as f:
            lines = f.readlines()
        for line in lines:
            if 'pragma' in line:
                res = self._get_version_aux(line) 
                if res is not None:
                    return res
        raise Exception


    def _tune_version(self) -> None:
        version = self._get_version()
        cmd = f'solc-select use {version}'
        os.system(cmd)
        return 


    def _gen_cmd(self) -> str:
        cmd = self.main_path
        # cmd += f' -input {self.path} -verify_timeout 120 -z3timeout 10000 -mode verify '
        cmd += f' -input {self.path} -verify_timeout 110 -z3timeout 10000 '
        if self.vul is not None:
            cmd += self.vul
        return cmd 


    def _execute(self, cmd: str) -> None:
        print(f'cmd -> {cmd}')  
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        bench_name = os.path.basename(self.path) + '.log'
        os.makedirs(self.save_path, exist_ok=True)
        save_path = os.path.join(self.save_path, bench_name)
        with open(save_path, "w") as file:
            file.write(result.stdout)  # 표준 출력
            file.write(result.stderr)  # 표준 에러 (필요시)
        return 


    def run(self) -> None:
        self._tune_version()
        cmd = self._gen_cmd()
        self._execute(cmd) 
        return



def main():
    # python3 ./executer.py --path=../smartbugs-dashboard/smartbugs/dataset/reentrancy/reentrancy_dao.sol --vul='re' --save_path='./anal_results' --main_path=../VeriSmart-public/main.native
    parser = argparse.ArgumentParser()
    parser.add_argument(f'--path')
    parser.add_argument(f'--vul')
    parser.add_argument(f'--save_path')
    parser.add_argument(f'--main_path')
    args = parser.parse_args()
    obj = Executer(args.path, args.vul, args.save_path, args.main_path)
    obj.run()
    return 


if __name__ == "__main__":
    main()