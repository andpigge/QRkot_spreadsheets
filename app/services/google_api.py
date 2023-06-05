from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"

PERMISSIONS_BODY = {
    'type': 'user',
    'role': 'writer',
    'emailAddress': settings.email
}


def get_spreadsheet_body(datetime: datetime = {datetime.now().strftime(FORMAT)}):
    return {
        'properties': {
            'title': f'Скорость сбора стредств. Отчет на {datetime}',
            'locale': 'ru_RU'
        },

        'sheets': [{
            'properties': {
                'sheetType': 'GRID',
                'sheetId': 0,
                'title': 'Благотворительный проект',
                'gridProperties': {
                    'rowCount': 100,
                    'columnCount': 16
                }
            }
        }]
    }


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    service = await wrapper_services.discover('sheets', 'v4')

    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=get_spreadsheet_body())
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
                                    charity_projects: list[dict[str, str, str]],
                                    wrapper_services: Aiogoogle) -> None:

    service = await wrapper_services.discover('sheets', 'v4')

    now_date_time = datetime.now().strftime(FORMAT)

    table_values = [
        ['Отчет от', now_date_time],
        ['Тип проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]

    for charity_project in charity_projects:
        new_row = [
            str(charity_project['title']),
            str(charity_project['donation_time']),
            str(charity_project['description'])
        ]

        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }

    row = len(max(max(table_values, key=len), key=len))
    column = len(charity_projects) + len(table_values)
    range = f'R1C1:R{row}C{column}'

    return await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheetid,
            range=range,
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
