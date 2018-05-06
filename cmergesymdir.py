import argparse
import os
import shutil

def main():
    parser = argparse.ArgumentParser(description='複数のリンク作成元ディレクトリからリンク作成先ディレクトリに対してサブディレクトリのシンボリックリンクを生成します')
    parser.add_argument('-l', '--level', type=int, default=2, help='階層を入力してください(既定値:2)')
    parser.add_argument('dstdir', help='リンク作成先ディレクトリを入力してください')
    parser.add_argument('srcdir', nargs='+', help='リンク作成元ディレクトリを入力してください')

    args = parser.parse_args()

    if not os.path.isdir(args.dstdir):
        print(f'リンク先ディレクトリ({args.dstdir})が存在しません')
        exit

    for dir in args.srcdir:
        if not os.path.isdir(dir):
            print(f'リンク作成元ディレクトリ({dir})が存在しません')
            exit

    added_paths_set = set()
    dst_dir = os.path.abspath(args.dstdir)

    for src_dir in args.srcdir:
        src_dir = os.path.abspath(src_dir)
        create_sym_recursived(dst_dir, src_dir, 1, args.level, added_paths_set)

def create_sym_recursived(dst_dir: str, src_dir: str, level: int, target_level: int, added_paths_set: set):
    for sub_dir_name in os.listdir(src_dir):
        src_sub_dir = os.path.join(src_dir, sub_dir_name)
        if not os.path.isdir(src_sub_dir):
            continue        
        new_dst_dir = os.path.join(dst_dir, sub_dir_name)
        if level < target_level:
            if not os.path.exists(new_dst_dir):
                os.mkdir(new_dst_dir)
            create_sym_recursived(new_dst_dir, src_sub_dir, level + 1, target_level, added_paths_set)
        else:
            if new_dst_dir in added_paths_set:
                continue

            if os.path.exists(new_dst_dir):
                if os.path.islink(new_dst_dir):
                    if os.path.realpath(new_dst_dir) == src_sub_dir:
                        continue
                    else:
                        os.unlink(new_dst_dir)
            
            os.symlink(src_sub_dir, new_dst_dir, True)
            added_paths_set.add(new_dst_dir)

main()

