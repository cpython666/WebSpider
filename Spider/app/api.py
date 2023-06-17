from fastapi import APIRouter
from Spider.models import *
from Spider.app.main import *

router = APIRouter()

@router.get("/dailycount")
def get_daily_count_():
    data=get_daily_count()
    date_list,count_list=zip(*data)
    return [date_list,count_list]

@router.get("/pagecount")
def get_page_count_():
    return get_page_count()

@router.get("/linkcount")
def get_link_count_():
    return get_link_count()

@router.get("/scuessfail")
def get_scuess_and_fail_():
    return get_scuess_and_fail()

# @router.get("/dailycount")
# def init_():
#
#     return get_page_count()

app.include_router(router,prefix="/api")