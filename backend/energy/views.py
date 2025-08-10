from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from .blockchain_utils import add_block, validate_chain

class EnergyInputAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        receiver_id = request.data.get('receiver_id')
        energy = float(request.data.get('energy_kwh'))

        if energy <= 0:
            return Response({"error": "Invalid energy amount."}, status=400)

        receiver = User.objects.get(id=receiver_id)
        transaction = EnergyTransaction.objects.create(sender=user, receiver=receiver, energy_kwh=energy)

        # Token logic
        receiver_profile, _ = UserProfile.objects.get_or_create(user=receiver)
        receiver_profile.energy_tokens += energy
        receiver_profile.save()

        block = add_block(transaction)
        return Response({"message": "Energy transaction recorded and block added.", "block_hash": block.hash}, status=201)

class BlockchainExplorerAPI(APIView):
    def get(self, request):
        blocks = BlockchainBlock.objects.all().order_by('index')
        data = BlockchainBlockSerializer(blocks, many=True).data
        return Response(data)

class ChainValidateAPI(APIView):
    def get(self, request):
        is_valid = validate_chain()
        return Response({"is_valid": is_valid})

class UserEnergyDashboardAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)
        transactions = EnergyTransaction.objects.filter(receiver=request.user)
        return Response({
            "profile": UserProfileSerializer(profile).data,
            "transactions": EnergyTransactionSerializer(transactions, many=True).data
        })
