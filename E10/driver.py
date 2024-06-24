import hashlib
import traceback


# try:
#    from solution import Ex0Transaction, Ex09Block, Ex09Blockchain, scenario
# except Exception as E:
#    traceback.print_exc()
#    print("0,0")m

def pseudoblock_helper(Block):
    class PseudoBlock(Block):
        def __int__(self):
            super(Block, self).__init__()

        def hash(self):
            return hashlib.sha512(("thisistechnicallynotablock" + str(self.nonce)).encode("utf-8"))

    return PseudoBlock()


def check_blockchain(Block):
    grades = [True]

    block = pseudoblock_helper(Block)
    block.difficulty = 9

    block.compute_nonce()
    nonce_hex = block.hash().hexdigest()

    if not (nonce_hex[:2] == "00" and
            int(nonce_hex[2]) < 8 and
            int(nonce_hex[2]) > 3):
        print(nonce_hex[:2] == "")
        print(
            "Nonce Computation does not correctly/efficiently satisfy block difficulty. Please check your Ex09Block.compute_nonce() and Ex09Block.validate_nonce()")
        grades[0] = False

    return grades


def check_scenario(sc):
    bc_tuple, index = sc(9, 11, 10, 9)
    grades = [True, True]

    if len(bc_tuple[0].blocklist) != 4:
        print("Your transactions are not valid/ block validation is incorrect. Please check the scenario()")
        grades[0] = grades[1] = False

    if not (bc_tuple[index].blocklist[-1].difficulty == 10 and
            bc_tuple[(index + 1) % 2].blocklist[-1].difficulty == 9):
        print("The longest chain returned is incorrect")
        grades[1] = False

    return grades


def check_solution(Transaction, Block, Blockchain, scenario):
    grades = []
    try:
        grades += check_blockchain(Block)
    except Exception as E:
        print("Could not check nonce computation")
        traceback.print_exc()
        grades = [False]

    try:
        grades += check_scenario(scenario)
    except Exception as E:
        print("Could not check scenario")
        traceback.print_exc()
        grades += [False, False]

    print(grades)

    return grades


def evaluation(Transaction, Block, Blockchain, scenario):
    """
    This method computes the evaluation based on a weighting factor
    """
    weighting = (.50, .25, .25)

    evaluation = 0
    try:
        for (success, weight) in zip(check_solution(Transaction, Block, Blockchain, scenario), weighting):
            if success:
                evaluation += weight
    except Exception as E:
        print("Task failed to run:")
        traceback.print_exc()
    return (evaluation * 100,)


def evaluate(Transaction, Block, Blockchain, scenario):
    e = evaluation(Transaction, Block, Blockchain, scenario)
    print(f"Grade = {e[0]}%")
    if e[0] == 100:
        print("Perfect Score")
