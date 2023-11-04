from apscheduler.schedulers.background import BackgroundScheduler
from api.views import view1,send_late


def start():
        scheduler=BackgroundScheduler()
        scheduler.add_job(view1,'cron',hour=14,minute=11,id="print_data",replace_existing=True)
        scheduler.add_job(view1,'cron',hour=10,minute=59,id="print_data",replace_existing=True)
        scheduler.add_job(view1,'cron',hour=11,minute=1,id="print_data",replace_existing=True)
        scheduler.add_job(view1,'cron',hour=17,minute=59,id="print_data1",replace_existing=True)
        scheduler.add_job(view1,'cron',hour=16,minute=0,id="print_data",replace_existing=True)
        scheduler.add_job(view1,'cron',hour=20,minute=0,id="print_data",replace_existing=True)
        scheduler.add_job(send_late,'cron',hour=14,minute=12,id='print_data2',replace_existing=True)
        scheduler.start()