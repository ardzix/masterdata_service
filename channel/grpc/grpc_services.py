# channel_services.py
import grpc
import uuid
import logging
from django.core.exceptions import ObjectDoesNotExist
from google.protobuf import empty_pb2
from channel.models import Brand, Channel, Event
from channel.serializers import BrandSerializer, ChannelSerializer, EventSerializer
from . import channel_pb2, channel_pb2_grpc

class ChannelService(channel_pb2_grpc.ChannelServiceServicer):

    # Brand related methods
    def GetBrand(self, request, context):
        logger.info(f"Received GetBrand request with req: {request}")
        try:
            brand = Brand.objects.get(hash=request.hash)
            return self._get_brand_response(brand)
        except ObjectDoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Brand not found")

    def CreateBrand(self, request, context):
        logger.info(f"Received CreateBrand request with req: {request}")
        data = {
            "name": request.name,
            "description": request.description,
            "is_active": request.is_active,
            "hash": str(uuid.uuid4())
        }
        serializer = BrandSerializer(data=data)
        if serializer.is_valid():
            brand = serializer.save()
            return self._get_brand_response(brand)
        else:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(serializer.errors))

    def UpdateBrand(self, request, context):
        logger.info(f"Received UpdateBrand request with req: {request}")
        try:
            brand = Brand.objects.get(hash=request.hash)
            data = {
                "name": request.name,
                "description": request.description,
                "is_active": request.is_active,
            }
            serializer = BrandSerializer(brand, data=data, partial=True)
            if serializer.is_valid():
                brand = serializer.save()
                return self._get_brand_response(brand)
            else:
                context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(serializer.errors))
        except ObjectDoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Brand not found")

    def DeleteBrand(self, request, context):
        logger.info(f"Received DeleteBrand request with req: {request}")
        try:
            brand = Brand.objects.get(hash=request.hash)
            brand.delete()
            return empty_pb2.Empty()
        except ObjectDoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Brand not found")

    def ListBrands(self, request, context):
        logger.info(f"Received ListBrands request with req: {request}")
        brands = Brand.objects.all()
        response = channel_pb2.ListBrandsResponse()
        for brand in brands:
            response.brands.append(self._get_brand_response(brand))
        return response

    def _get_brand_response(self, brand):
        return channel_pb2.BrandResponse(
            hash=str(brand.hash),
            name=brand.name,
            description=brand.description,
            is_active=brand.is_active
        )

    # Channel related methods
    def GetChannel(self, request, context):
        logger.info(f"Received GetChannel request with req: {request}")
        try:
            channel = Channel.objects.get(hash=request.hash)
            return self._get_channel_response(channel)
        except ObjectDoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Channel not found")

    def CreateChannel(self, request, context):
        logger.info(f"Received CreateChannel request with req: {request}")
        data = {
            "name": request.name,
            "description": request.description,
            "brand_hash": request.brand_hash,
            "hash": str(uuid.uuid4())
        }
        serializer = ChannelSerializer(data=data)
        if serializer.is_valid():
            channel = serializer.save()
            return self._get_channel_response(channel)
        else:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(serializer.errors))

    def UpdateChannel(self, request, context):
        logger.info(f"Received UpdateChannel request with req: {request}")
        try:
            channel = Channel.objects.get(hash=request.hash)
            data = {
                "name": request.name,
                "description": request.description,
                "brand_hash": request.brand_hash,
            }
            serializer = ChannelSerializer(channel, data=data, partial=True)
            if serializer.is_valid():
                channel = serializer.save()
                return self._get_channel_response(channel)
            else:
                context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(serializer.errors))
        except ObjectDoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Channel not found")

    def DeleteChannel(self, request, context):
        logger.info(f"Received DeleteChannel request with req: {request}")
        try:
            channel = Channel.objects.get(hash=request.hash)
            channel.delete()
            return empty_pb2.Empty()
        except ObjectDoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Channel not found")

    def ListChannels(self, request, context):
        logger.info(f"Received ListChannels request with req: {request}")
        channels = Channel.objects.all()
        response = channel_pb2.ListChannelsResponse()
        for channel in channels:
            response.channels.append(self._get_channel_response(channel))
        return response

    def _get_channel_response(self, channel):
        return channel_pb2.ChannelResponse(
            hash=str(channel.hash),
            name=channel.name,
            description=channel.description,
            brand_hash=str(channel.brand.hash)
        )

    # Event related methods
    def GetEvent(self, request, context):
        logger.info(f"Received GetEvent request with req: {request}")
        try:
            event = Event.objects.get(hash=request.hash)
            return self._get_event_response(event)
        except ObjectDoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Event not found")

    def CreateEvent(self, request, context):
        logger.info(f"Received CreateEvent request with req: {request}")
        data = {
            "name": request.name,
            "description": request.description,
            "start_date": request.start_date,
            "end_date": request.end_date,
            "channel_hash": request.channel_hash,
            "brand_hashes": list(request.brand_hashes),
            "hash": str(uuid.uuid4())
        }
        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            event = serializer.save()
            return self._get_event_response(event)
        else:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(serializer.errors))

    def UpdateEvent(self, request, context):
        logger.info(f"Received UpdateEvent request with req: {request}")
        try:
            event = Event.objects.get(hash=request.hash)
            data = {
                "name": request.name,
                "description": request.description,
                "start_date": request.start_date,
                "end_date": request.end_date,
                "channel_hash": request.channel_hash,
                "brand_hashes": list(request.brand_hashes),
            }
            serializer = EventSerializer(event, data=data, partial=True)
            if serializer.is_valid():
                event = serializer.save()
                return self._get_event_response(event)
            else:
                context.abort(grpc.StatusCode.INVALID_ARGUMENT, str(serializer.errors))
        except ObjectDoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Event not found")

    def DeleteEvent(self, request, context):
        logger.info(f"Received DeleteEvent request with req: {request}")
        try:
            event = Event.objects.get(hash=request.hash)
            event.delete()
            return empty_pb2.Empty()
        except ObjectDoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Event not found")

    def ListEvents(self, request, context):
        logger.info(f"Received ListEvents request with req: {request}")
        events = Event.objects.all()
        response = channel_pb2.ListEventsResponse()
        for event in events:
            response.events.append(self._get_event_response(event))
        return response

    def _get_event_response(self, event):
        return channel_pb2.EventResponse(
            hash=str(event.hash),
            name=event.name,
            description=event.description,
            start_date=event.start_date.isoformat(),
            end_date=event.end_date.isoformat(),
            channel_hash=str(event.channel.hash),
            brand_hashes=[str(hash) for hash in list(event.brands.values_list('hash', flat=True))]
        )

    # Brand-Event relationship methods
    def AddBrandToEvent(self, request, context):
        logger.info(f"Received AddBrandToEvent request with req: {request}")
        try:
            event = Event.objects.get(hash=request.event_hash)
            if request.brand_hash not in event.brand_hashes:
                event.brands.add(Brand.objects.get(hash=request.brand_hash))
            return self._get_event_response(event)
        except ObjectDoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Event/brand not found")

    def RemoveBrandFromEvent(self, request, context):
        logger.info(f"Received RemoveBrandFromEvent request with req: {request}")
        try:
            event = Event.objects.get(hash=request.event_hash)
            if request.brand_hash in event.brand_hashes:
                event.brand_hashes.remove(request.brand_hash)
                event.save()
            return self._get_event_response(event)
        except ObjectDoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Event not found")

    def SetBrandsForEvent(self, request, context):
        logger.info(f"Received SetBrandsForEvent request with req: {request}")
        try:
            event = Event.objects.get(hash=request.event_hash)
            brands = Brand.objects.filter(hash__in=request.brand_hashes)
            event.brands.set(brands)
            event.save()
            return self._get_event_response(event)
        except ObjectDoesNotExist:
            context.abort(grpc.StatusCode.NOT_FOUND, "Event not found")
