# grpc_client_channel.py
import grpc
import os
import django

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'masterdata.settings')
django.setup()

from google.protobuf import empty_pb2
from channel.grpc import channel_pb2, channel_pb2_grpc
from django.conf import settings

def print_channel(channel):
    print(f"hash: {channel.hash}")
    print(f"name: {channel.name}")
    print(f"description: {channel.description}")
    print(f"brand_hash: {channel.brand_hash}")

def print_brand(brand):
    print(f"hash: {brand.hash}")
    print(f"name: {brand.name}")
    print(f"description: {brand.description}")
    print(f"is_active: {brand.is_active}")

def print_event(event):
    print(f"hash: {event.hash}")
    print(f"name: {event.name}")
    print(f"description: {event.description}")
    print(f"start_date: {event.start_date}")
    print(f"end_date: {event.end_date}")
    print(f"channel_hash: {event.channel_hash}")
    print("brand_hashes:")
    for brand_hash in event.brand_hashes:
        print(f"  - {brand_hash}")

def run():
    with grpc.insecure_channel(f'{settings.MD_CHANNEL_SERVICE_HOST}:{settings.MD_CHANNEL_SERVICE_PORT}') as channel:
        stub = channel_pb2_grpc.ChannelServiceStub(channel)

        # Create a new brand
        create_brand_request = channel_pb2.CreateBrandRequest(
            name="Test Brand",
            description="A test brand",
            is_active=True
        )
        brand_response = stub.CreateBrand(create_brand_request)
        print("Created Brand:")
        print_brand(brand_response)

        # Create a new channel
        create_channel_request = channel_pb2.CreateChannelRequest(
            name="Test Channel",
            description="A test channel",
            brand_hash=brand_response.hash
        )
        channel_response = stub.CreateChannel(create_channel_request)
        print("Created Channel:")
        print_channel(channel_response)

        # Create a new event
        create_event_request = channel_pb2.CreateEventRequest(
            name="Test Event",
            description="A test event",
            start_date="2024-07-15T09:00:00Z",
            end_date="2024-07-16T09:00:00Z",
            channel_hash=channel_response.hash,
            brand_hashes=[brand_response.hash]
        )
        event_response = stub.CreateEvent(create_event_request)
        print("Created Event:")
        print_event(event_response)

        # Get the event
        get_event_request = channel_pb2.GetEventRequest(hash=event_response.hash)
        get_event_response = stub.GetEvent(get_event_request)
        print("\nRetrieved Event:")
        print_event(get_event_response)

        # List all events
        list_events_response = stub.ListEvents(empty_pb2.Empty())
        print("\nList of Events:")
        for event in list_events_response.events:
            print_event(event)
            print("\n")

        # Update the event
        update_event_request = channel_pb2.UpdateEventRequest(
            hash=event_response.hash,
            name="Updated Test Event",
            description="An updated test event",
            start_date="2024-07-15T10:00:00Z",
            end_date="2024-07-17T10:00:00Z",
            channel_hash=channel_response.hash,
            brand_hashes=[brand_response.hash]
        )
        update_event_response = stub.UpdateEvent(update_event_request)
        print("Updated Event:")
        print_event(update_event_response)

        # Add brand to event
        add_brand_to_event_request = channel_pb2.AddBrandToEventRequest(
            event_hash=event_response.hash,
            brand_hash=brand_response.hash
        )
        updated_event_response = stub.AddBrandToEvent(add_brand_to_event_request)
        print("Added Brand to Event:")
        print_event(updated_event_response)

        # Remove brand from event
        remove_brand_from_event_request = channel_pb2.RemoveBrandFromEventRequest(
            event_hash=event_response.hash,
            brand_hash=brand_response.hash
        )
        updated_event_response = stub.RemoveBrandFromEvent(remove_brand_from_event_request)
        print("Removed Brand from Event:")
        print_event(updated_event_response)

        # Set brands for event
        set_brands_for_event_request = channel_pb2.SetBrandsForEventRequest(
            event_hash=event_response.hash,
            brand_hashes=[brand_response.hash]
        )
        updated_event_response = stub.SetBrandsForEvent(set_brands_for_event_request)
        print("Set Brands for Event:")
        print_event(updated_event_response)

        # Delete the event
        delete_event_request = channel_pb2.DeleteEventRequest(hash=event_response.hash)
        stub.DeleteEvent(delete_event_request)
        print("\nDeleted Event")

        # Delete the channel
        delete_channel_request = channel_pb2.DeleteChannelRequest(hash=channel_response.hash)
        stub.DeleteChannel(delete_channel_request)
        print("\nDeleted Channel")

        # Delete the brand
        delete_brand_request = channel_pb2.DeleteBrandRequest(hash=brand_response.hash)
        stub.DeleteBrand(delete_brand_request)
        print("\nDeleted Brand")

if __name__ == '__main__':
    run()
