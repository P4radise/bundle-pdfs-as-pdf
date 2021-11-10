from enum import Enum

import re
import os
import onevizion
import PyPDF2
import datetime

class Integration:
    def __init__(self, logger, url_onevizion, main_statuses, main_trackor, child_trackor, child_filter, error_field_name, dest_file_field_name, status_field_name):
        self.log = logger
        self.url_onevizion = url_onevizion
        self.statuses = main_statuses
        self.main_trackor = main_trackor
        self.child_trackor = child_trackor
        self.child_filter = child_filter
        self.error_field_name = error_field_name
        self.dest_file_field_name = dest_file_field_name
        self.status_field_name = status_field_name

    def start_integration(self):
        self.log.info('Starting integration')

        main_trackor_list = self.main_trackor.get_trackor_list()
        self.log.info(f'Found {len(main_trackor_list)} records')

        for main_trackor in main_trackor_list:
            mergeFile = PyPDF2.PdfFileMerger()
            filename = ""

            try:
                trackor_id = main_trackor['TRACKOR_ID']
                file = self.main_trackor.get_file(trackor_id)
                mergeFile.append(PyPDF2.PdfFileReader(file, 'rb'))
                os.remove(file)
            
                self.child_filter[self.main_trackor.trackor_type + ".TRACKOR_ID"] = trackor_id
                child_trackor_list = self.child_trackor.get_trackor_list(self.child_filter)

                for child_trackor in child_trackor_list:
                    self.log.info(child_trackor)

                    file = self.child_trackor.get_file(child_trackor)
                    if re.search('.pdf', file) is None:
                        os.remove(file)
                        continue

                    mergeFile.append(PyPDF2.PdfFileReader(file, 'rb'))
                    os.remove(file)

                filename = f'{main_trackor["TRACKOR_KEY"]} - Complete LTC Packet - {datetime.datetime.today().strftime("%m%d%Y")}.pdf'
                mergeFile.write(filename)

                self.main_trackor.update(trackor_id, onevizion.EFileEncode(filename), self.statuses.SUCCESS, self.dest_file_field_name, self.status_field_name)

            except Exception as e:
                self.log.warning(e)
                self.main_trackor.update(trackor_id, e, self.statuses.ERROR, self.error_field_name, self.status_field_name)
            finally:
                os.remove(filename)

        self.log.info('Integration has been completed')


class MainTrackor:
    def __init__(self, url_onevizion, ov_access_key, ov_secret_key, trackor_type, main_filter, main_fields, main_sort, main_source_file_field_name):
        self.main_filter = main_filter
        self.main_fields = main_fields
        self.main_sort = main_sort
        self.main_source_file_field_name = main_source_file_field_name
        self.trackor_type = trackor_type
        self.main_trackor = onevizion.Trackor(trackorType=trackor_type, URL=url_onevizion,
                                               userName=ov_access_key, password=ov_secret_key, isTokenAuth=True)
    
    def get_trackor_list(self):
        self.main_trackor.read(
            filters = self.main_filter,
            fields = self.main_fields,
            sort = self.main_sort,
            page = 1,
            perPage = 100
        )

        return self.main_trackor.jsonData

    def get_file(self, trackor_id):
        return self.main_trackor.GetFile(
                trackorId=trackor_id,
                fieldName=self.main_source_file_field_name
            )

    def update(self, trackor_id, filed_name, status, file_filed_name, status_field_name):
        update_fields = {}
        update_fields[file_filed_name] = filed_name
        update_fields[status_field_name] = status

        self.main_trackor.update(
            filters = {'TRACKOR_ID':trackor_id},
            fields = update_fields
            )


class MainStatuses:
    def __init__(self, main_statuses):
        self.SUCCESS = main_statuses[MainStatus.SUCCESS.value]
        self.ERROR = main_statuses[MainStatus.ERROR.value]


class MainStatus(Enum):
    SUCCESS = 'success'
    ERROR = 'error'


class ChildTrackor:
    def __init__(self, url_onevizion, ov_access_key, ov_secret_key, trackor_type, child_fields, child_sort, child_file_field_name):
        self.child_fields = child_fields
        self.child_sort = child_sort
        self.child_file_field_name = child_file_field_name
        self.child_trackor = onevizion.Trackor(trackorType=trackor_type, URL=url_onevizion,
                                               userName=ov_access_key, password=ov_secret_key, isTokenAuth=True)
    
    def get_trackor_list(self, filter):
        self.child_trackor.read(
            filters = filter,
            fields = self.child_fields,
            sort = self.child_sort
        )

        return self.child_trackor.jsonData

    def get_file(self, trackor):
        return self.child_trackor.GetFile(
                trackorId=trackor['TRACKOR_ID'],
                fieldName=self.child_file_field_name
            )
