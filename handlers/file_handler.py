import csv
import json
from ..extras import INFO, create_stream_logger


class FileHandler:
    _logger_ = create_stream_logger("FileHandler", fmt="[%(levelname)s] [%(asctime)s]: %(message)s", level=INFO)

    def __init__(self, items, file_name, field_names=None, mode="w", *args, **kwargs):
        self.fObj = open(file_name, mode, *args, **kwargs)
        self.file_name = file_name
        self.field_names = field_names
        self._items_ = items

    def to_txt(self):
        self._logger_.info("Menyimpan ke: {0}".format(self.file_name))
        try:
            self.fObj.writelines("\n".join(self._items_))
            self._logger_.info("Tersimpan")
            self.fObj.close()
        except Exception:
            self._logger_.info("Terjadi galat: ", exc_info=True)

    def to_csv(self, *args, **kwargs):
        self._logger_.info("Menyimpan ke: {0}".format(self.file_name))
        try:
            row_writer = csv.writer(self.fObj, *args, **kwargs)
            row_writer.writerow(self.field_names)
            for item in self._items_:
                row_writer.writerow(item)
            self._logger_.info("Tersimpan")
            self.fObj.close()
        except Exception:
            self._logger_.info("Terjadi galat: ", exc_info=True)

    def to_json(self, *args, **kwargs):
        self._logger_.info("Menyimpan ke: {0}".format(self.file_name))
        try:
            json_obj = json.dumps(self._items_, *args, **kwargs)
            self.fObj.write(json_obj)
            self._logger_.info("Tersimpan")
            self.fObj.close()
        except Exception:
            self._logger_.info("Terjadi galat: ", exc_info=True)
