import hashlib
import _hashlib
import traceback
from copy import deepcopy


# try:
#    from solution import Ex09Transaction, Ex09Block, Ex09Blockchain, scenario
# except Exception as E:
#    traceback.print_exc()
#    print("0,0")


def check_tx(t):
    grades = [True, True, True]
    sample_tx = t()
    sample_tx.add_input(hashlib.sha512(b"0x00"), 0)
    sample_tx.add_output("address2", 100)
    try:
        str_rep1 = str(sample_tx)
    except Exception as E:
        print("Could not get string representation, check Ex09Transaction.__str__")
        traceback.print_exc()
        grades[0] = False

    try:
        hash1 = sample_tx.hash()
    except Exception as E:
        print("Could not get transaction hash, check Ex09Transaction.hash")
        traceback.print_exc()
        grades[1] = False

    sample_tx.add_output("address1", 199)
    try:
        str_rep2 = str(sample_tx)
    except Exception as E:
        print("Could not get string representation, check Ex09Transaction.__str__")
        traceback.print_exc()
        grades[0] = False

    try:
        hash2 = sample_tx.hash()
    except Exception as E:
        print("Could not get transaction hash, check Ex09Transaction.hash")
        traceback.print_exc()
        grades[1] = False

    sample_tx.add_input(hashlib.sha512(b"0x000"), 0)
    try:
        str_rep3 = str(sample_tx)
    except Exception as E:
        print("Could not get string representation, check Ex09Transaction.__str__")
        traceback.print_exc()
        grades[0] = False

    try:
        hash3 = sample_tx.hash()
    except Exception as E:
        print("Could not get transaction hash, check Ex09Transaction.hash")
        traceback.print_exc()
        grades[1] = False

    try:
        if not (str_rep1 != str_rep2 != str_rep3):
            print("String representation is not unique, check Ex09Transaction.__str__")
            grades[0] = False
    except Exception as E:
        traceback.print_exc()

    try:
        if not (isinstance(hash1, _hashlib.HASH) and
                isinstance(hash2, _hashlib.HASH) and
                isinstance(hash3, _hashlib.HASH)):
            print("Hashes are not valid _hashlib.HASH instances, check Ex09Transaction.hash")
            grades[1] = False
    except Exception as E:
        traceback.print_exc()

    try:
        if not (hash1.digest() != hash2.digest() != hash3.digest()):
            print("Hashes are not true hashes, check Ex09Transaction.hash")
            grades[2] = False
    except Exception as E:
        traceback.print_exc()

    return grades, sample_tx


def check_block(t, b):
    tx_grades, sample_tx = check_tx(t)
    sample_block = b()  # function call -> param

    grades = tx_grades + [True, True]

    sample_block.add_transaction(sample_tx)

    try:
        str_rep1 = str(sample_block)
    except Exception as E:
        print("Could not get block string representation, check Ex09Block.__str__")
        traceback.print_exc()
        grades[3] = False

    try:
        hash1 = sample_block.hash()
    except Exception as E:
        print("Could not get block hash")
        traceback.print_exc()
        grades[4] = False

    sample_tx2 = t()
    sample_tx2.set_inputs([{"tx_hash": hashlib.sha512(b"0x00"), "output_index": 0}])
    sample_tx2.set_outputs({"address5": 200})

    sample_block.add_transaction(sample_tx2)

    try:
        str_rep2 = str(sample_block)
    except Exception as E:
        print("Could not get block string representation, check Ex09Block.__str__")
        traceback.print_exc()
        grades[3] = False

    try:
        hash2 = sample_block.hash()
    except Exception as E:
        print("Could not get block hash, check Ex09Block.hash")
        traceback.print_exc()
        grades[4] = False

    try:
        if not (str_rep1 != str_rep2):
            print("String representation of Block is not unique, check Ex09Block.__str__")
            grades[3] = False
    except Exception as E:
        print("Could not get block string representation, check Ex09Block.__str__")
        traceback.print_exc()
        grades[3] = False

    try:
        if not (isinstance(hash1, _hashlib.HASH) and
                isinstance(hash2, _hashlib.HASH)):
            print("Block hash is not a valid _hashlib.HASH instance, check Ex09Block.hash")
            grades[4] = False

    except Exception as E:
        traceback.print_exc()

    try:
        if not (hash1 != hash2):
            print("Block hash is not a true hash, check Ex09Block.hash")
            grades[4] = False
    except Exception as E:
        print("Could not get block hash, check Ex09Block.hash")
        traceback.print_exc()
        grades[4] = False

    return grades


def check_scenario(t, b, sc):
    blockchain = sc()
    grades = [True, True]

    if len(blockchain.blocklist) != 4:
        print(
            "Your transactions are not valid/ block validation is incorrect. (There should be exactly 4 blocks in the blockchain)")
        grades[0] = grades[1] = False

    new_tx = t()
    invalid_tx = t()
    last_block = blockchain.blocklist[-1]

    req_transaction = None
    output_indices = [None, None, None]
    for tx_hash, transaction in last_block.transactions.items():
        if set(["address1", "address2", "address3"]).issubset(set(op["address"] for op in transaction.get_outputs())):
            print(transaction)
            req_transaction = transaction

            for index, output in enumerate(transaction.get_outputs()):
                if (output["address"] == "address1"):
                    output_indices[0] = index
                elif (output["address"] == "address2"):
                    output_indices[1] = index
                elif (output["address"] == "address3"):
                    output_indices[2] = index
            break

    if req_transaction is None:
        print(
            "Could not find the transaction from step 3, Make sure that all three addresses exist in the output for the transaction in step 3, and that this transaction is mined in the last block in the blockchain.")
        grades[1] = False

    if (output_indices[0] == None) or (output_indices[1] == None) or (output_indices[2] == None):
        print("The transaction from Step 3 does not contain an output for all three addresses.")
        grades[1] = False

    new_tx.add_input(req_transaction.hash(), output_indices[0])
    new_tx.add_input(req_transaction.hash(), output_indices[1])
    new_tx.add_input(req_transaction.hash(), output_indices[2])
    new_tx.add_output("address1", 48)
    new_tx.add_output("address2", 179)
    new_tx.add_output("address3", 60)

    new_tx.add_input(req_transaction.hash(), output_indices[0])
    new_tx.add_input(req_transaction.hash(), output_indices[1])
    new_tx.add_input(req_transaction.hash(), output_indices[2])
    invalid_tx.add_output("address1", 49)
    invalid_tx.add_output("address2", 180)
    invalid_tx.add_output("address3", 61)

    valid_block = b()
    invalid_block = b()

    valid_block.add_transaction(new_tx)

    invalid_block.add_transaction(invalid_tx)
    valid_block.previous_block_hash = invalid_block.previous_block_hash = blockchain.blocklist[-1].hash()

    bc1, bc2 = blockchain, sc()

    print("Trying invalid blocks")

    if not bc1.add_block(valid_block):
        print(
            "Transactions in the scenario are not correct (1); The correct amount of tokens spent in the outputs of the transaction from Step 3, should be 48, 179 and 60 to address1, address2 and address3 respectively. Your outputs may have less tokens than those specified.")
        grades[1] = False

    if bc2.add_block(invalid_block):
        print(
            "Transactions in the scenario are not correct (2); The correct amount of tokens spent in the outputs of the transaction from Step 3, should be 48, 179 and 60 to address1, address2 and address3 respectively. Your outputs may have more tokens than those specified.")
        grades[1] = False

    return grades


def check_solution(t, b, bc, sc):
    block_grades = [False, False, False, False, False]
    scenario_grades = [False, False]

    try:
        block_grades = check_block(t, b)
    except Exception as E:
        print("Could not check block and transaction classes, this could be a bug. Please report.")
        traceback.print_exc()

    try:
        scenario_grades = check_scenario(t, b, sc)
    except Exception as E:
        print("Could not check scenario")
        traceback.print_exc()

    return block_grades + scenario_grades


def evaluation(t, b, bc, sc):
    """
    This method computes the evaluation based on a weighting factor
    """
    weighting = (.1, .1, .1, .1, .1, .25, .25)

    evaluation = 0
    try:
        for (success, weight) in zip(check_solution(t, b, bc, sc), weighting):
            if success:
                evaluation += weight
    except Exception as E:
        print("Task failed to run:")
        traceback.print_exc()
    return (evaluation * 100,)


def evaluate(t, b, bc, sc):
    e = evaluation(t, b, bc, sc)
    print(f"Grade = {e[0]}%")
    if e[0] == 100:
        print("Perfect Score")
