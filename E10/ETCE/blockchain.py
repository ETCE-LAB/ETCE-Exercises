import _hashlib
import hashlib


class Ex10Transaction(object):
    """
    Interface class for Ex10 Transaction Class
    """

    def __init__(self):
        """
        Constructor for the Ex10 Transaction Class.
        """
        self.inputs = []
        self.outputs = []

    def get_inputs(self) -> dict:
        """
        Method that returns the transaction inputs
        DO NOT OVERRIDE THIS METHOD
        """
        return self.inputs

    def set_inputs(self, inputs):
        """
        Method that sets the transaction inputs
        DO NOT OVERRIDE THIS METHOD
        """
        self.inputs = inputs

    def get_outputs(self) -> dict:
        """
        Method that returns the transaction outputs
        DO NOT OVERRIDE THIS METHOD
        """
        return self.outputs

    def set_outputs(self, outputs):
        """
        Method that sets the transaction outputs
        DO NOT OVERRIDE THIS METHOD
        """
        self.outputs = outputs

    def add_input(self, tx_hash, output_index):
        """Method that adds an input to the Transaction

        `tx_hash`: _hashlib.HASH object that is the hash of a
        transaction

        `output_index` must be the index [0,1,....] representing the
        output in the transaction with hash `tx_hash`

        When the transaction is mined into a block, ALL the tokens in
        this output will be spent in the transaction.
        
        DO NOT OVERRIDE THIS METHOD

        """

        self.inputs.append({"tx_hash": tx_hash,
                            "output_index": output_index})

    def add_output(self, address, amount):
        """Method that adds an output to the Transaction

        `address`: str that represents the address of a blockchain
        address. To keep it simple, the addresses are like
        'myaddress1', 'myaddress2', etc.
        
        `amount`: Integer that represents the amount of tokens that
        should be in the address after the transaction.
        
        `delta`: Integer that represents the amount of tokens that the
        address gains after the transaction
        
        DO NOT OVERRIDE THIS METHOD

        """

        self.outputs.append({"address": address,
                             "amount": amount})

    def __str__(self) -> str:
        """Method that returns the string representation of the transaction
        
        You are free to choose whatever string representation you
        like, as long as it incorporates every input
        and every output

        You can put your solution from Ex07 here, but we have already
        put a correct solution here.

        """
        return str({
            "inputs": [
                {"tx_hash": (v["tx_hash"].digest().hex() if v["tx_hash"] is not None else None),
                 "output_index": v["output_index"]}
                for v in self.get_inputs()],
            "outputs": self.get_outputs()})

    def __repr__(self) -> str:
        """Method that returns the string representation of the transaction

        DO NOT OVERRIDE THIS METHOD

        """
        return self.__str__()

    def hash(self) -> _hashlib.HASH:
        """Method that computes the sha512 hash of the transaction using the
        string representation of the transaction
        
        Return an instance of _hashlib.HASH
        
        You can put your solution from Ex08 here, but we have already
        put a correct solution here.

        """

        return hashlib.sha512(str(self).encode("utf-8"))


class Ex10Block(object):
    """
    Interface class for Ex10 Block class
    """

    def __init__(self):
        """
        Constructor for Ex10 Block
        """
        self.transactions = {}
        self.block_number = None
        self.difficulty = 0
        self.nonce = None
        self.previous_block_hash = None

    def compute_nonce(self):
        """Method that computes the proof of work.  Find the nonce that
        satisfies the difficulty set in `self.difficulty` and set
        `self.nonce`. Use `self.validate_nonce` to check if the
        current nonce is correct
        
        IMPORTANT: Please search for nonces from the subset of
        integers [0, 1, 2, 3, 4, .... ∞), incrementally, starting from
        0.
        
        OVERRIDE THIS METHOD!!

        """
        pass

    def validate_nonce(self) -> bool:
        """Method that checks whether `self.nonce` is correct w.r.t
        `self.difficulty`
        
        Return True if first `d` bits of self.hash() are `0`,
        where `d` = `self.difficulty`
        
        OVERRIDE THIS METHOD!!

        """
        pass

    def add_transaction(self, transaction):
        """Method that adds a transaction to the block
        
        `transaction` should be an instance of Ex10Transaction

        DO NOT OVERRIDE THIS METHOD
        """
        if len(self.transactions) <= 20:
            self.transactions[transaction.hash().digest()] = transaction
        else:
            raise "Block is full"

    def __str__(self) -> str:
        """Method that returns the string representation of the block
        
        You are free to choose whatever string representation you
        like, as long as it incorporates every transaction, block
        number, nonce, and previous block hash 
        
        Hint: use python's str() magic function for transactions

        You can put your solution from Ex07 here, but we have already
        put a correct solution here.

        """
        return str({"transactions": self.transactions,
                    "block_number": self.block_number,
                    "nonce": self.nonce,
                    "difficulty": self.difficulty,
                    "previous_block_hash": self.previous_block_hash.hexdigest() if self.previous_block_hash is not None else None})

    def __repr__(self) -> str:
        """Method that returns the string representation of the block

        DO NOT OVERRIDE THIS METHOD

        """

        return self.__str__()

    def hash(self) -> _hashlib.HASH:
        """Method that computes the sha512 hash of the block using the
        string representation of the block
        
        Return an instance of _hashlib.HASH
        
        You can put your solution from Ex08 here, but we have already
        put a correct solution here.

        """
        return hashlib.sha512(str(self).encode("utf-8"))


class Ex10Blockchain(object):
    """
    Interface class for Ex10 Blockchain Class
    """

    def __init__(self, initial_block):
        """
        initial_block should be an Ex10Block
        """
        self.blocks = {initial_block.hash().digest(): initial_block}
        self.addresses = {}  # Just an easily accessible dictionary to
        # (redundantly) cache the number of tokens
        # each address has.

        # Here we populate an initial address dictionary
        for transaction in initial_block.transactions.values():
            for output in transaction.get_outputs():
                if output["address"] in self.addresses:
                    self.addresses[output["address"]] += output["amount"]
                else:
                    self.addresses[output["address"]] = output["amount"]
        self.blocklist = [initial_block]
        print("New Blockchain Initialized", self.addresses)

    def validate_new_block(self, newblock) -> (bool, dict):
        """Method that validates a new block that is to be added to
        the blockchain.

        1. Validate the `block.previous_block_hash` and the
        transactions in the block, by checking whether the inputs
        contain enough tokens for the transactions, and also check the
        previous block hash and block number. For simplicity, you can
        assume that no two transactions in a block depend on each
        other, and transactions only depend on those from previous
        blocks

        2. Create a copy of self.addresses dictionary with updated
        token amounts, adding new addresses where necessary like in
        __init__, and additionally decreasing the token amount from
        the inputs.

        3. Return the boolean result of step 1, as well as a
        dictionary representing the new addresses.

        NOTE: the addresses dictionary is only used for easy
        validation of transactions. In a real scenario, every node in
        the blockchain computes this internally while doing the
        validation. When a new block is propagated/ blockchain is sent
        to other nodes, only the list of blocks is required.
        
        You can store whatever information you like in the addresses
        dict. A suggestion is to also store the tx_hash, or you could
        just store the last transaction with output to that address
        
        Important: The realtest autograding driver will validate any
        transactions (return True for any argument), since we already
        implemented transaction validation in the last exercise.

        We have already put a correct solution to this function,
        including the updates to the transactions here, however, this
        function will not be relevant for grading.

        """

        def find_mined_transaction(tx_hash):  # This scales very badly
            # computationally, merkel
            # trees are way better
            for block in reversed(self.blocklist):
                for tx_HASH, transaction in block.transactions.items():
                    if tx_HASH == tx_hash:
                        return transaction
            return None

        def spent_before(inp, transaction=None):  # Also scales very
            # badly
            if transaction == None:
                transaction = find_mined_transaction(inp["tx_hash"].digest())
            for block in self.blocklist:
                for tran in block.transactions.values():
                    if inp in tran.get_inputs():
                        return True
            return False

        def check_inputs(tx, nad):

            for i in range(len(tx.get_inputs())):
                for j in range(i + 1, len(tx.get_inputs())):
                    if tx.get_inputs()[i] == tx.get_inputs()[j]:
                        # Duplicate inputs
                        print("Duplicate Inputs Found")
                        return False, None, None

            token_count = 0

            new_addresses = dict(nad)

            for inp in tx.get_inputs():
                transaction = find_mined_transaction(inp["tx_hash"].digest())
                if not transaction:
                    print(f"Transaction {inp['tx_hash'].digest().hex()} not found")
                    return False, None, None
                if spent_before(inp, transaction):
                    print(f"Output {inp} spent before")
                    return False, None, None
                token_count += transaction.get_outputs()[inp["output_index"]]["amount"]
                new_addresses[transaction.get_outputs()[inp["output_index"]]["address"]] -= \
                transaction.get_outputs()[inp["output_index"]]["amount"]

            return True, token_count, new_addresses

        def check_tx(tx, nad):

            valid, token_count, new_addresses = check_inputs(tx, nad)

            if not valid:
                print(f"Transaction {tx} not valid")
                return False, None

            have = token_count
            spent = 0

            for op in tx.get_outputs():
                if op["address"] not in new_addresses:
                    new_addresses[op["address"]] = op["amount"]
                else:
                    new_addresses[op["address"]] += op["amount"]
                spent += op["amount"]

            if (spent > have):
                print("Not enough tokens in inputs to spend:", ">".join([str(spent), str(have)]))
                return False, None

            return True, new_addresses

        if self.blocklist[-1].hash().digest() != newblock.previous_block_hash.digest():
            print(self.blocklist[-1].hash().digest(),
                  newblock.previous_block_hash.digest())
            print("Previous block hash is not correct")
            return False, None
        block_new_addresses = dict(self.addresses)
        for transaction in newblock.transactions.values():
            valid, tnad = check_tx(transaction, block_new_addresses)
            if not valid:
                print(f"Transaction {transaction} not valid")
                return False, None
            block_new_addresses = dict(tnad)

        return True, block_new_addresses

    def add_block(self, block) -> bool:
        """Method that adds a block to the blockchain.        
        `block`: an Ex09Block instance
        
        DO NOT OVERRIDE THIS METHOD

        """
        valid, new_addresses = self.validate_new_block(block)
        nonce_valid = block.validate_nonce()
        if valid and nonce_valid:
            self.blocks[block.hash().digest()] = block
            self.blocklist.append(block)
            self.addresses = new_addresses
            return True
        else:
            if not valid:
                print("Block transactions are invalid")
            if not nonce_valid:
                print("Block proof of work is invalid")

        return False
