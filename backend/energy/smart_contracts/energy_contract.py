def simulate_energy_settlement(sender_profile, receiver_profile, energy_kwh, price_per_kwh=1):
    tokens_required = energy_kwh * price_per_kwh
    if sender_profile.energy_tokens >= tokens_required:
        sender_profile.energy_tokens -= tokens_required
        receiver_profile.energy_tokens += tokens_required
        sender_profile.save()
        receiver_profile.save()
        return True
    return False
