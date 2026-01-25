from telebot.handler_backends import State, StatesGroup  # States

#For admin's dashboard
class Panel(StatesGroup):
    open_admin_st = State()
#For user's dashboard
class MyStates(StatesGroup):
    headers_st = State()
    contacts_st = State()
    settings_st = State()
    change_language_st = State()
    complaint_branch_st = State()
    get_answer  = State()
    order_func_st = State()
    pickup_func_st = State()
    menu_func_st = State()
#For user's registration
class Register(StatesGroup):
    lang_st = State()
    full_name_st = State()