# bundle_pdfs
 
Integration to combine PDF files stored in OneVizon and store the output back into OneVizion.

## Requirements
- Python 3
- onevizion - library for python
- PyPDF2 - library for python - This is not a standard library so a case need to be opened with onevizion support to have it installed for integration hub.

## Usage
Create new integration with the following fields: 
- Integration Name: bundle_pdfs
- Command: python3 ./[file name]
- Repository: https://github.com/ov-integrations/bundle_pdfs
- Settings File: settings


## Example settings file

```json
{
	"OV":
		{
			"UserName":"service-account",
			"Password":"******",
			"Url":"xxx.onevizion.com"
		},
	"MainTrackor":
		{
			"TrackorType":"LTC",
			"Fields" : ["TRACKOR_KEY","LTC_COMPLETE_TITLE_PACKET_STAT"],
			"Filters" : {"LTC_COMPLETE_TITLE_PACKET_STAT":"Queued"},
			"Sort" : {"TRACKOR_KEY":"ASC"},
			"FirstFileFieldName" : "LTC_COMPLETED_LTC_DOCUMENT",
			"DestFileFieldName" : "LTC_COMPLETED_LTC_PACKET",
			"StatusField" : "LTC_COMPLETE_TITLE_PACKET_STAT",
			"ErrorField" : "LTC_COMPLETE_TITLE_PACKET_ERRO"
		},
	"ChildTrackor":
		{
			"TrackorType":"Title_Documents",
			"Fields" : ["TDOC_RECORDED_DATE", "TDOC_BOOKPAGE", "TDOC_PAGE", "TDOC_CLERKS_FILE__DOCUMENT_", "TRACKOR_KEY"],
			"Filters" : {"TDOC_DOCUMENT_FILE": "not null"},
			"Sort" : {"TDOC_RECORDED_DATE":"ASC", "TDOC_BOOKPAGE": "ASC", "TDOC_PAGE": "ASC", "TDOC_CLERKS_FILE__DOCUMENT_":"ASC"},
			"FileFieldName" : "TDOC_DOCUMENT_FILE"
		}
}
```

The settings file is in 3 parts.
- OV - how to log into OneVizion
- MainTrackor - Trackor that source and destination fields.
- ChildTrackor - Trackor with many source files.

| Field   | Purpose |
| ------- |:------- |
