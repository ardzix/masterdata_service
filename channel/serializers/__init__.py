# serializers.py
from rest_framework import serializers
from ..models import Brand, Channel, Event

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['hash', 'name', 'description', 'is_active']

class ChannelSerializer(serializers.ModelSerializer):
    brand_hash = serializers.CharField(source='brand.hash')

    class Meta:
        model = Channel
        fields = ['hash', 'name', 'description', 'brand_hash']

    def create(self, validated_data):
        brand_hash = validated_data.pop('brand').get('hash') if validated_data.get('brand', None) else None
        brand = Brand.objects.get(hash=brand_hash)
        channel = Channel.objects.create(brand=brand, **validated_data)
        return channel

    def update(self, instance, validated_data):
        brand_hash = validated_data.pop('brand').get('hash') if validated_data.get('brand', None) else None
        if brand_hash:
            instance.brand = Brand.objects.get(hash=brand_hash)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

class EventSerializer(serializers.ModelSerializer):
    channel_hash = serializers.CharField(source='channel.hash')
    brand_hashes = serializers.ListField()

    class Meta:
        model = Event
        fields = ['hash', 'name', 'description', 'start_date', 'end_date', 'channel_hash', 'brand_hashes']

    def create(self, validated_data):
        brand_hashes = validated_data.pop('brand_hashes', None)
        channel_hash = validated_data.pop('channel').get('hash') if validated_data.get('channel', None) else None
        channel = Channel.objects.get(hash=channel_hash)
        event = Event.objects.create(channel=channel, **validated_data)
        if brand_hashes:
            event.brands.set(Brand.objects.filter(hash__in=brand_hashes))
        return event

    def update(self, instance, validated_data):
        brand_hashes = validated_data.pop('brand_hashes', None)
        channel_hash = validated_data.pop('channel').get('hash') if validated_data.get('channel', None) else None
        if channel_hash:
            instance.channel = Channel.objects.get(hash=channel_hash)
        if brand_hashes:
            instance.brands.set(Brand.objects.filter(hash__in=brand_hashes))
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.save()
        return instance