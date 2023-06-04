from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"
NOW_DATE_TIME = datetime.now().strftime(FORMAT)

TITLE_DOCUMENT = f'Скорость сбора стредств. Отчет на {NOW_DATE_TIME}'
ROW_COUNT = 100
COLUMN_COUNT = 16

PERMISSIONS_BODY = {
    'type': 'user',
    'role': 'writer',
    'emailAddress': settings.email
}

RANGE_FOR_SPREADSHEETS_UPDATE = 'A1:E30'


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    service = await wrapper_services.discover('sheets', 'v4')

    properties = {
        'title': TITLE_DOCUMENT,
        'locale': 'ru_RU'
    }

    sheets = [{
        'properties': {
            'sheetType': 'GRID',
            'sheetId': 0,
            'title': 'Благотворительный проект',
            'gridProperties': {
                'rowCount': ROW_COUNT,
                'columnCount': COLUMN_COUNT
            }
        }
    }]

    spreadsheet_body = {
        'properties': properties,
        'sheets': sheets
    }

    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )

    return response['spreadsheetId']


async def set_user_permissions(spreadsheetid: str,
                               wrapper_services: Aiogoogle) -> None:

    service = await wrapper_services.discover('drive', 'v3')

    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=PERMISSIONS_BODY,
            fields="id"
        )
    )


async def spreadsheets_update_value(spreadsheetid: str,
                                    reservations: list[dict[str, str, str]],
                                    wrapper_services: Aiogoogle) -> None:

    service = await wrapper_services.discover('sheets', 'v4')

    table_values = [
        ['Отчет от', NOW_DATE_TIME],
        ['Тип проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]

    for res in reservations:
        new_row = [
            str(res['title']),
            str(res['donation_time']),
            str(res['description'])
        ]

        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }

    return await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=RANGE_FOR_SPREADSHEETS_UPDATE,
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
