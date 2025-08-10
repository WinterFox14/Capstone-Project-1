from .models import BlockchainBlock

def get_last_block():
    return BlockchainBlock.objects.order_by('-index').first()

def add_block(transaction):
    last_block = get_last_block()
    index = last_block.index + 1 if last_block else 0
    previous_hash = last_block.hash if last_block else '0'

    new_block = BlockchainBlock(index=index, transaction=transaction, previous_hash=previous_hash, hash='')
    new_block.hash = new_block.compute_hash()
    new_block.save()
    return new_block

def validate_chain():
    chain = BlockchainBlock.objects.all().order_by('index')
    prev_hash = '0'
    for block in chain:
        if block.previous_hash != prev_hash:
            return False
        if block.hash != block.compute_hash():
            return False
        prev_hash = block.hash
    return True
