from module.database import select_all_manager
def chek_manager(telegram_id):
    list_manager = select_all_manager('manager')
    print(telegram_id, list_manager)
    return telegram_id in list_manager
