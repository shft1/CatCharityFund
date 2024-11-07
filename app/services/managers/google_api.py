from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"


async def spreadsheets_create(
        wrapper_service: Aiogoogle
):
    time_now = datetime.now().strftime(FORMAT)
    methods_sheets_api = await wrapper_service.discover(
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
        methods_sheets_api.spreadsheets.create(json=spreadsheets_body)
    )
    spreadsheets_id = response['spreadsheetId']
    print(f'https://docs.google.com/spreadsheets/d/{spreadsheets_id}')
    return spreadsheets_id


async def set_user_permissions(
        wrapper_service: Aiogoogle,
        spreadsheet_id: str
):
    methods_drive_api = await wrapper_service.discover(
        'drive', 'v3'
    )
    permission_body = {'type': 'user',
                       'role': 'writer',
                       'emailAddress': settings.service_email}
    await wrapper_service.as_service_account(
        methods_drive_api.permissions.create(
            fileId=spreadsheet_id,
            json=permission_body,
            fields='id'
        )
    )
