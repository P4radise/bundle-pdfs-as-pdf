from jsonschema import validate
from bundle_pdfs_integration import ChildTrackor, Integration, MainStatus, MainStatuses, MainTrackor
from onevizion import IntegrationLog, LogLevel
import json



with open('settings.json', 'rb') as PFile:
    settings_data = json.loads(PFile.read().decode('utf-8'))

with open('settings_schema.json', 'rb') as PFile:
    data_schema = json.loads(PFile.read().decode('utf-8'))

try:
    validate(settings_data, data_schema)
except Exception as e:
    raise Exception(f'Incorrect value in the settings file\n{str(e)}')

ov_settings = settings_data['OV']
main_settings = settings_data['mainTrackor']
child_settings = settings_data['childTrackor']
statuses_settings = settings_data['mainStatuses']

url_onevizion = ov_settings['urlOneVizion']
ov_access_key = ov_settings['ovAccessKey']
ov_secret_key = ov_settings['ovSecretKey']

main_trackor_type = main_settings['TrackorType']
main_fields = main_settings['Fields']
main_filters = main_settings['Filters']
main_sort = main_settings['Sort']

main_source_file_field_name = main_settings['SourceFileFieldName']
main_dest_file_field_name = main_settings['DestFileFieldName']
main_status_field_name = main_settings['StatusField']
main_error_field_name = main_settings['ErrorField']

child_trackor_type = child_settings['TrackorType']
child_fields = child_settings['Fields']
child_filters = child_settings['Filters']
child_sort = child_settings['Sort']
child_file_field_name = child_settings['FileFieldName']

with open('ihub_parameters.json', 'rb') as PFile:
    ihub_data = json.loads(PFile.read().decode('utf-8'))

process_id = ihub_data['processId']
log_level = ihub_data['logLevel']

integration_log = IntegrationLog(process_id, url_onevizion, ov_access_key, ov_secret_key, None, True, log_level)
main_statuses = MainStatuses(statuses_settings)
main_trackor = MainTrackor(url_onevizion, ov_access_key, ov_secret_key, main_trackor_type, \
                                main_filters, main_fields, main_sort, main_source_file_field_name)
child_trackor = ChildTrackor(url_onevizion, ov_access_key, ov_secret_key, child_trackor_type, \
                                child_fields, child_sort, child_file_field_name)

integration = Integration(integration_log, url_onevizion, main_statuses, main_trackor, child_trackor, child_filters, \
                                    main_error_field_name, main_dest_file_field_name, main_status_field_name)

try:
    integration.start_integration()
except Exception as e:
    integration_log.add(LogLevel.ERROR, str(e))
    raise e
