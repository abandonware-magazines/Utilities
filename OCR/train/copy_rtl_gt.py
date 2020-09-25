import os
import shutil
import argparse

def main(src_dir, dest_dir):
    for filename in os.listdir(src_dir):
        dest_path = os.path.join(dest_dir, filename)
        if os.path.exists(dest_path):
            continue
        
        src_path = os.path.join(src_dir, filename)

        if filename.lower().endswith(".gt.txt"):
            with open(src_path, "r") as s, open(dest_path, "w") as d:
                d.write(s.read()[::-1])
        else:
            shutil.copy(src_path, dest_dir)
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Copy RTL Ground Truth')
    parser.add_argument('-s', '--source', action='store', required = True, help='Path to ground truth source folder')
    parser.add_argument('-d', '--destination', action = 'store', required = True, help = 'Path to ground truth destination folder')
    args = parser.parse_args()

    main(args.source, args.destination)