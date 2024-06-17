import _hashlib


class Ex09Transaction(object):
    """
    Interface class for Ex09 Transaction Class
    """

    def __init__(self):
        """
        Constructor for the Ex09 Transaction Class.
        """
        self.inputs = []
        self.outputs = []

    def get_inputs(self) -> list:
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

    def get_outputs(self) -> list:
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

        `address`: str that represents the blockchain address that can
        spend this output. To keep it simple, the addresses are like
        'myaddress1', 'myaddress2', etc.
        
        `amount`: Integer that represents the amount of tokens being
        sent to this output.

        When the transaction is mined into a block, "amount" tokens
        are sent to this output from the pool of tokens being spent
        from the inputs.
        
        DO NOT OVERRIDE THIS METHOD

        """

        self.outputs.append({"address": address,
                             "amount": amount})

    def __str__(self) -> str:
        """Method that returns the string representation of the transaction
        
        You are free to choose whatever string representation you
        like, as long as it incorporates every input
        and every output

        OVERRIDE THIS METHOD

        """
        pass

    def __repr__(self) -> str:
        """Method that returns the string representation of the transaction

        DO NOT OVERRIDE THIS METHOD

        """
        return self.__str__()

    def hash(self) -> _hashlib.HASH:
        """Method that computes the sha512 hash of the transaction using the
        string representation of the transaction
        
        Return an instance of _hashlib.HASH

        OVERRIDE THIS METHOD
        """
        pass


class Ex09Block(object):
    """
    Interface class for Ex09 Block class
    """

    def __init__(self):
        """
        Constructor for Ex09 Block
        """
        self.transactions = {}
        self.block_number = None
        self.nonce = None
        self.previous_block_hash = None

    def compute_nonce(self):
        """Method that computes the proof of work.
        
        You dont have to implement anything here for now, we will deal
        with consensus in Ex09.

        """
        pass

    def add_transaction(self, transaction):
        """Method that adds a transaction to the block
        
        `transaction` should be an instance of Ex09Transaction

        DO NOT OVERRIDE THIS METHOD
        """
        if len(self.transactions) < 20:
            self.transactions[transaction.hash().digest().hex()] = transaction
        else:
            raise "Block is full"

    def __str__(self) -> str:
        """Method that returns the string representation of the block
        
        You are free to choose whatever string representation you
        like, as long as it incorporates every transaction, block
        number, nonce, and previous block hash 
        
        Hint: use python's str() magic function for transactions

        OVERRIDE THIS METHOD

        """
        pass

    def __repr__(self) -> str:
        """Method that returns the string representation of the block

        DO NOT OVERRIDE THIS METHOD

        """

        return self.__str__()

    def hash(self) -> _hashlib.HASH:
        """Method that computes the sha512 hash of the block using the
        string representation of the block
        
        Return an instance of _hashlib.HASH

        OVERRIDE THIS METHOD
        """
        pass


class Ex09Blockchain(object):
    """
    Interface class for Ex09 Blockchain Class
    """

    def __init__(self, initial_block):
        """`initial_block` should be an Ex09Block
        `addresses` should be a dictionary

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

    def validate_new_block(self, block) -> (bool, dict):
        """Method that validates a new block that is to be added to the
        blockchain.

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
        
        Important: The realtest autograding driver will use it's own
        implementation of this method to check whether your
        implementation is correct. So if you are not validating
        transactions and blocks correctly, and make invalid
        transactions, the handout driver may give you points however
        the realtest driver will not.

        OVERRIDE THIS METHOD

        """
        pass

    def add_block(self, block) -> bool:
        """Method that adds a block to the blockchain.        
        `block`: an Ex09Block instance
        
        DO NOT OVERRIDE THIS METHOD

        """
        valid, new_addresses = self.validate_new_block(block)
        if valid:
            self.blocks[block.hash().digest()] = block
            self.blocklist.append(block)
            self.addresses = new_addresses
            print("Block Mined", self.addresses)
            return True

        print("Block is invalid")
        return False
