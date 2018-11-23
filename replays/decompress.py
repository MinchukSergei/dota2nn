import bz2
import shutil
from pathlib import Path
import datetime


def main():
    decompress_bz2('H:/Minchuk/replays')


def decompress_bz2(input_folder, output_folder=None):
    if not output_folder:
        output_folder = input_folder

    output_folder = Path(output_folder) / 'decompressed'
    output_failed_folder = output_folder / 'failed'
    processed_folder = Path(input_folder) / 'processed'
    processed_failed_folder = Path(processed_folder) / 'failed'
    error_log_file = Path(input_folder) / 'error.log'

    if not output_folder.exists():
        output_folder.mkdir()

    if not output_failed_folder.exists():
        output_failed_folder.mkdir()

    if not processed_folder.exists():
        processed_folder.mkdir()

    if not processed_failed_folder.exists():
        processed_failed_folder.mkdir()

    if not error_log_file.exists():
        error_log_file.touch(exist_ok=False)

    compressed_files = sorted(Path(input_folder).glob('*.bz2'))
    with open(str(error_log_file), 'a') as errf:
        for cf in compressed_files:
            compressed_file = str(cf)
            decompressed_file = str(output_folder / cf.stem)

            print('Processing file: {} to {}'.format(compressed_file, decompressed_file))

            start_time = datetime.datetime.now()

            try:
                with bz2.open(compressed_file, 'rb') as r, open(decompressed_file, 'wb') as w:
                    shutil.copyfileobj(r, w)
                shutil.move(compressed_file, str(processed_folder / cf.name))
            except Exception as e:
                shutil.move(compressed_file, str(processed_failed_folder / cf.name))
                shutil.move(decompressed_file, str(output_failed_folder / cf.stem))
                errf.write('{} failed: {}.{}'.format(compressed_file, str(e), '\n'))

            end_time = datetime.datetime.now()
            print('Time taken: {}'.format(end_time - start_time))


if __name__ == "__main__":
    main()
