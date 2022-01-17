import rest_framework.routers
from . import event

router = rest_framework.routers.SimpleRouter(trailing_slash=False)

router.register(prefix="events", viewset=event.ViewSet, basename="events")

urls = router.urls
