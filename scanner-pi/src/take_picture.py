import argparse
from gphoto2 import take_picture
from scanner import get_x_y_of_qr, save_as_csv
from upload_csv import upload_file
from pathlib import Path
import shutil


def move_file(original: Path):
    dest_dir = Path("img/backup/")
    dest_file = Path(dest_dir, original.name)
    print(f"original: {original.as_posix()}")
    print(f"destination: {dest_dir.as_posix()}")
    if not dest_dir.exists():
        dest_dir.mkdir()
    shutil.move(original.as_posix(), dest_file.as_posix())


def scan_img_folder():
    folder_path = "img/"
    p = Path(folder_path)
    for file in p.iterdir():
        if file.is_file() and file.suffix == ".jpg":
            print(file)
            coordinates = get_x_y_of_qr(file)
            print(coordinates)
            try:
                csv_file = prepare_csv_file(file)
                save_as_csv(coordinates, csv_file)
                if upload_file(csv_file):
                    print("upload success")
                else:
                    print("upload not done either failed or no internet")
            except Exception as e:
                print(f"error: {e}")
            move_file(file)


def prepare_csv_file(file: Path):
    path_csv = Path("csv")
    if not path_csv.exists():
        path_csv.mkdir()
    csv_file = Path(path_csv, f"{file.name}.csv")
    print(f"save as csv: {csv_file}")
    return csv_file


def main():
    print("get images")
    print(take_picture())
    print("scan img folder")
    scan_img_folder()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        help="path to the input folder containing all the image to be processed",
        required=False,
    )
    # parser.add_argument("--output", help="path to the output folder containing all output in the json format", required = True)
    args = parser.parse_args()
    print("take picture")
    main()
    # if args.input:
    #     print("scan folder")
    #     scan_img_folder()
    # else:
    #     print("take picture")
    #     main()
