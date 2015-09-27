from swampdragon import route_handler
from swampdragon.route_handler import BaseRouter, ModelRouter, ModelPubRouter
from swampdragon.pubsub_providers.data_publisher import publish_data
from main.serializers import ChatSerializer, MarkerSerializer
from main.models import Event, Chat, Marker
from swampdragon.pubsub_providers.model_channel_builder import make_channels, filter_channels_by_model, filter_channels_by_dict
from swampdragon.pubsub_providers.publisher_factory import get_publisher
import logging

publisher = get_publisher()

class ChatListRouter(ModelRouter):
    route_name = 'chat-list'
    serializer_class = ChatSerializer
    model = Chat
    valid_verbs = ['subscribe','get_list','create']
    logger = logging.getLogger('main.routers.ChatListRouter')

    def get_initial(self, verb, **kwargs):
        self.logger.error('get_initial')
        event = Event.objects.get(identifier = kwargs['identifier'])
        return {'event' : event}
    
    def get_object(self, **kwargs):
        return self.model.objects.get(pk=kwargs['id'])
    def get_query_set(self, **kwargs):
        self.logger.error('get_query_set')
        event = Event.objects.filter(identifier = kwargs['identifier'])
        return self.model.objects.filter(event = event)
        
    def created(self, obj, **kwargs):
        data = self.serializer_class(instance=obj).serialize()
        chatData = dict({'data': data})
        base_channel = self.serializer_class.get_base_channel()
        identifier = kwargs['identifier']
        channel = base_channel + "identifier:" + identifier
        self.publish([channel], chatData)        
        super().created(obj, **kwargs)
            
class MarkerListRouter(BaseRouter):
    route_name = 'marker-list'
    valid_verbs = ['subscribe', 'get_markers']

    def get_markers(self, **kwargs):
        identifier = kwargs['identifier']
        local_channel = kwargs['local_channel']
        lat = kwargs['lat']
        lng = kwargs['lng']
        channel = "marker|identifier:" + identifier
        self.publish([channel], kwargs)
        
    def get_subscription_channels(self, **kwargs):
        identifier = kwargs['identifier']
        return ["marker|identifier:" + identifier]

route_handler.register(ChatListRouter)
route_handler.register(MarkerListRouter)
