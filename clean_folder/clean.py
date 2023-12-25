import re
import sys
import shutil
from pathlib import Path

jpeg_files = list()
png_files = list()
jpg_files = list()
svg_files = list()
txt_files = list()
docx_files = list()
doc_files = list()
pdf_files = list()
xlsx_files = list()
pptx_files = list()
mp3_files = list()
ogg_files = list()
wav_files = list()
amr_files = list()
avi_files = list()
mp4_files = list()
mov_files = list()
mkv_files = list()
zip_files = list()
gz_files = list()
tar_files = list()
folders = list()
archives = list()
others = list()
unknown = set()
extensions = set()

registered_extensions = {'JPEG': jpeg_files, 'PNG': png_files, 'JPG': jpg_files, 'SVG': svg_files,
                         'DOC': doc_files, 'TXT': txt_files, 'DOCX': docx_files, 'PDF': pdf_files, 'XLSX': xlsx_files,
                         'PPTX': pptx_files,
                         'MP3': mp3_files, 'OGG': ogg_files, 'WAV': wav_files, "AMR": amr_files,
                         'AVI': avi_files, 'MP4': mp4_files, 'MOV': mov_files, 'MKV': mkv_files,
                         'ZIP': zip_files, 'GZ': gz_files, 'TAR': tar_files}

UKRAINIAN_SYMBOLS = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
TRANSLATION = (
    "a", "b", "v", "g", "d", "e", "je", "zh", "z", "y", "i", "ji", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t",
    "u",
    "f", "h", "ts", "ch", "sh", "sch", "", "ju", "ja")

TRANS = {}

for key, value in zip(UKRAINIAN_SYMBOLS, TRANSLATION):
    TRANS[ord(key)] = value
    TRANS[ord(key.upper())] = value.upper()


def normalize(name: str) -> str:
    name, *extension = name.split('.')
    new_name = name.translate(TRANS)
    new_name = re.sub(r'\W', '_', new_name)
    return f"{new_name}.{'.'.join(extension)}"


def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()


def scan(folder):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in (
                    'JPEG', 'PNG', 'JPG', 'SVG', 'TXT', 'DOCX', 'DOC', 'PDF', 'XLSX', 'PPTX', 'MP3', 'OGG', 'WAV',
                    'AMR', 'AVI',
                    'MP4', 'MOV', 'MKV', 'ZIP', 'GZ', 'TAR', 'OTHER'):
                folders.append(item)
                scan(item)
            continue

        extension = get_extensions(file_name=item.name)
        new_name = folder / item.name
        if not extension:
            others.append(new_name)
        else:
            try:
                container = registered_extensions[extension]
                extensions.add(extension)
                container.append(new_name)
            except KeyError:
                unknown.add(extension)
                others.append(new_name)


def handle_file(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    path.replace(target_folder / normalize(path.name))


def handle_archive(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    if path.name.endswith('.zip'):
        new_name = normalize(path.name).replace(".zip", '')
    elif path.name.endswith('.gz'):
        new_name = normalize(path.name).replace(".gz", '')
    elif path.name.endswith('.tar'):
        new_name = normalize(path.name).replace(".tar", '')

    archive_folder = target_folder / new_name
    archive_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(path, archive_folder)
    except shutil.ReadError:
        archive_folder.rmdir()
        return
    except FileNotFoundError:
        archive_folder.rmdir()
        return
    path.unlink()


def remove_empty_folders(path):
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass


def main():
    folder_path = Path(sys.argv[1])
    scan(folder_path)
    images_files = jpeg_files + jpg_files + png_files + svg_files
    documents_files = txt_files + doc_files + docx_files + pdf_files + xlsx_files + pptx_files
    audio_files = mp3_files + ogg_files + wav_files + amr_files
    video_files = avi_files + mp4_files + mov_files + mkv_files
    archive_files = zip_files + gz_files + tar_files
    # known_extension = images_files + documents_files + audio_files + video_files + archive_files
    dict_files = {"images": images_files, "documents": documents_files, 'audio': audio_files, 'video': video_files,
                  'other': others}
    for key, value in dict_files.items():
        for file in value:
            handle_file(file, folder_path, key)
    for file in archive_files:
        handle_archive(file, folder_path, 'archives')
    remove_empty_folders(folder_path)


if __name__ == '__main__':
    main()
