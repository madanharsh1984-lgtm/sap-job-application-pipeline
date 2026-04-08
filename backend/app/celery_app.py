from celery import Celery

celery_app = Celery(
    'sap_pipeline',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0',
)

celery_app.conf.task_routes = {
    'app.tasks.automation.*': {'queue': 'automation'},
}

celery_app.autodiscover_tasks(['app.tasks'])
