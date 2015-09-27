from swampdragon.serializers.model_serializer import ModelSerializer

class EventSerializer(ModelSerializer):
    class Meta:
        model = 'main.Event'
        publish_fields = ('lat','lng','deadline','term','identifier','message','created_at',)
        update_fields = ()
        
class ChatSerializer(ModelSerializer):
    event = EventSerializer
    
    class Meta:
        model = 'main.Chat'
        publish_fields = ('event', 'message', 'created_at',)
        update_fields = ('message', )

class MarkerSerializer(ModelSerializer):
    class Meta:
        model = 'main.Marker'
        publish_fields = ('lat', 'lng',)
        update_fields = ('lat', 'lng',)
                          
