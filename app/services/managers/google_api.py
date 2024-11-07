from datetime import datetime

from aiogoogle import Aiogoogle

FORMAT = "%Y/%m/%d %H:%M:%S"


async def spreadsheets_create(
        wrapper_service: Aiogoogle
):
    time_now = datetime.now().strftime(FORMAT)
    methods_api = await wrapper_service.discover(
        'sheets', 'v4'
    )
    spreadsheets_body = {
        'properties': {'title': f'Отчёт на {time_now}',
                       'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetId': 0,
                                   'sheetType': 'GRID',
                                   'title': 'Лист1',
                                   'gridProperties': {'rowCount': 100,
                                                      'columnCount': 10}}}]
    }
    response = await wrapper_service.as_service_account(
        methods_api.spreadsheets.create(json=spreadsheets_body)
    )
    spreadsheets_id = response['spreadsheetId']
    print(f'https://docs.google.com/spreadsheets/d/{spreadsheets_id}')
    return spreadsheets_id
